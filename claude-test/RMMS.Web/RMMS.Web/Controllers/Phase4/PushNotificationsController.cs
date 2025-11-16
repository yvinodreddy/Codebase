using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Notifications;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using RMMS.Models.Mobile;
using System.Text.Json;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class PushNotificationsController : Controller
    {
        private readonly IPushNotificationService _pushService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<PushNotificationsController> _logger;

        public PushNotificationsController(
            IPushNotificationService pushService,
            ApplicationDbContext context,
            ILogger<PushNotificationsController> logger)
        {
            _pushService = pushService;
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Get recent notifications with statistics
                var notifications = await _context.PushNotifications
                    .OrderByDescending(n => n.CreatedAt)
                    .Take(100)
                    .ToListAsync();

                // Calculate statistics
                var today = DateTime.UtcNow.Date;
                ViewBag.TotalNotifications = notifications.Count;
                ViewBag.SentToday = notifications.Count(n => n.CreatedAt.Date == today);
                ViewBag.SentThisWeek = notifications.Count(n => n.CreatedAt > DateTime.UtcNow.AddDays(-7));
                ViewBag.SentThisMonth = notifications.Count(n => n.CreatedAt > DateTime.UtcNow.AddDays(-30));

                // Delivery statistics
                var deliveredCount = notifications.Count(n => n.Status == "sent" || n.Status == "delivered");
                ViewBag.DeliveredCount = deliveredCount;
                ViewBag.PendingCount = notifications.Count(n => n.Status == "pending");
                ViewBag.FailedCount = notifications.Count(n => n.Status == "failed");

                // Calculate delivery rate (capped at 100%)
                ViewBag.DeliveryRate = notifications.Any()
                    ? Math.Min(100, Math.Round((deliveredCount / (double)notifications.Count) * 100, 1))
                    : 0;

                // Get available devices for targeting
                var devices = await _context.MobileDevices.Where(d => d.IsActive).ToListAsync();
                ViewBag.TotalDevices = devices.Count;
                ViewBag.AndroidDevices = devices.Count(d => d.Platform == "Android");
                ViewBag.iOSDevices = devices.Count(d => d.Platform == "iOS");
                ViewBag.PushEnabledDevices = devices.Count(d => d.NotificationsEnabled);

                // Target options for dropdown
                ViewBag.TargetOptions = new List<string>
                {
                    "All Devices",
                    "Android Only",
                    "iOS Only",
                    "Specific User",
                    "Push Enabled Only"
                };

                return View(notifications);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading push notifications");
                TempData["Error"] = "Error loading push notifications: " + ex.Message;
                return View(new List<PushNotification>());
            }
        }

        [HttpGet]
        public IActionResult SendNew()
        {
            ViewBag.TargetOptions = new List<string>
            {
                "All Devices",
                "Android Only",
                "iOS Only",
                "Specific User",
                "Push Enabled Only"
            };

            return View(new PushNotification
            {
                CreatedAt = DateTime.UtcNow
            });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SendNew(string title, string body, string target, string? userId = null, string? customData = null)
        {
            try
            {
                // Input validation
                if (string.IsNullOrWhiteSpace(title))
                {
                    TempData["Error"] = "Notification title is required";
                    return RedirectToAction(nameof(Index));
                }

                if (string.IsNullOrWhiteSpace(body))
                {
                    TempData["Error"] = "Notification body is required";
                    return RedirectToAction(nameof(Index));
                }

                if (title.Length > 200)
                {
                    TempData["Error"] = "Title must be 200 characters or less";
                    return RedirectToAction(nameof(Index));
                }

                if (body.Length > 500)
                {
                    TempData["Error"] = "Body must be 500 characters or less";
                    return RedirectToAction(nameof(Index));
                }

                if (string.IsNullOrWhiteSpace(target))
                {
                    TempData["Error"] = "Target selection is required";
                    return RedirectToAction(nameof(Index));
                }

                // Get target devices based on selection
                var devices = await GetTargetDevices(target, userId);

                if (!devices.Any())
                {
                    TempData["Error"] = $"No active devices found for target: {target}";
                    return RedirectToAction(nameof(Index));
                }

                // Simulate sending to each device and track results
                int successCount = 0;
                int failureCount = 0;

                foreach (var device in devices)
                {
                    try
                    {
                        // Create notification record
                        var notification = new PushNotification
                        {
                            Name = $"Notification to {device.UserId}",
                            Title = title,
                            Body = body,
                            UserId = device.UserId,
                            DeviceId = device.Id,
                            Data = customData,
                            CreatedAt = DateTime.UtcNow,
                            SentAt = DateTime.UtcNow,
                            Status = "sent"
                        };

                        _context.PushNotifications.Add(notification);
                        successCount++;

                        _logger.LogInformation($"Push notification sent to device: {device.DeviceId}");
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, $"Failed to send notification to device: {device.DeviceId}");

                        var notification = new PushNotification
                        {
                            Name = $"Failed notification to {device.UserId}",
                            Title = title,
                            Body = body,
                            UserId = device.UserId,
                            DeviceId = device.Id,
                            Data = customData,
                            CreatedAt = DateTime.UtcNow,
                            ErrorMessage = ex.Message,
                            Status = "failed"
                        };

                        _context.PushNotifications.Add(notification);
                        failureCount++;
                    }
                }

                await _context.SaveChangesAsync();

                var deliveryRate = devices.Count > 0
                    ? Math.Min(100, Math.Round((successCount / (double)devices.Count) * 100, 1))
                    : 0;

                TempData["Success"] = $"✓ Notification sent! Target: {target} | " +
                    $"Devices: {devices.Count} | Delivered: {successCount} | Failed: {failureCount} | " +
                    $"Delivery Rate: {deliveryRate}%";

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending push notification");
                TempData["Error"] = $"Error sending notification: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        private async Task<List<MobileDevice>> GetTargetDevices(string target, string? userId = null)
        {
            var query = _context.MobileDevices.Where(d => d.IsActive);

            switch (target)
            {
                case "Android Only":
                    return await query.Where(d => d.Platform == "Android").ToListAsync();

                case "iOS Only":
                    return await query.Where(d => d.Platform == "iOS").ToListAsync();

                case "Specific User":
                    if (!string.IsNullOrWhiteSpace(userId))
                        return await query.Where(d => d.UserId == userId).ToListAsync();
                    return new List<MobileDevice>();

                case "Push Enabled Only":
                    return await query.Where(d => d.NotificationsEnabled).ToListAsync();

                case "All Devices":
                default:
                    return await query.ToListAsync();
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetHistory(string userId)
        {
            try
            {
                var history = await _context.PushNotifications
                    .Include(n => n.Device)
                    .Where(n => string.IsNullOrEmpty(userId) || n.UserId == userId)
                    .OrderByDescending(n => n.CreatedAt)
                    .Take(50)
                    .Select(n => new
                    {
                        n.Id,
                        n.Title,
                        n.Body,
                        n.UserId,
                        Platform = n.Device != null ? n.Device.Platform : "Unknown",
                        n.CreatedAt,
                        n.SentAt,
                        n.Status
                    })
                    .ToListAsync();

                return Json(new { success = true, data = history });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting notification history");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetStatistics()
        {
            try
            {
                var notifications = await _context.PushNotifications
                    .Include(n => n.Device)
                    .ToListAsync();
                var today = DateTime.UtcNow.Date;
                var sevenDaysAgo = DateTime.UtcNow.AddDays(-7);

                var stats = new
                {
                    total = notifications.Count,
                    delivered = notifications.Count(n => n.Status == "sent" || n.Status == "delivered"),
                    failed = notifications.Count(n => n.Status == "failed"),
                    pending = notifications.Count(n => n.Status == "pending"),
                    sentToday = notifications.Count(n => n.CreatedAt.Date == today),
                    sentThisWeek = notifications.Count(n => n.CreatedAt > sevenDaysAgo),
                    deliveryRate = notifications.Any()
                        ? Math.Min(100, Math.Round((notifications.Count(n => n.Status == "sent" || n.Status == "delivered") / (double)notifications.Count) * 100, 2))
                        : 0,
                    byPlatform = notifications
                        .Where(n => n.Device != null)
                        .GroupBy(n => n.Device!.Platform)
                        .Select(g => new { platform = g.Key, count = g.Count() })
                        .ToList(),
                    recentNotifications = notifications
                        .OrderByDescending(n => n.CreatedAt)
                        .Take(10)
                        .Select(n => new
                        {
                            n.Title,
                            n.CreatedAt,
                            n.Status,
                            Platform = n.Device != null ? n.Device.Platform : "Unknown"
                        })
                        .ToList()
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting statistics");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> ResendFailed(int id)
        {
            try
            {
                var notification = await _context.PushNotifications.FindAsync(id);
                if (notification == null)
                {
                    TempData["Error"] = "Notification not found";
                    return RedirectToAction(nameof(Index));
                }

                if (notification.Status != "failed")
                {
                    TempData["Error"] = "This notification was not failed";
                    return RedirectToAction(nameof(Index));
                }

                // Reset and retry
                notification.ErrorMessage = null;
                notification.SentAt = DateTime.UtcNow;
                notification.Status = "sent";
                notification.AttemptCount++;

                await _context.SaveChangesAsync();

                TempData["Success"] = "Notification resent successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error resending notification");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var notification = await _context.PushNotifications.FindAsync(id);
                if (notification == null)
                {
                    TempData["Error"] = "Notification not found";
                    return RedirectToAction(nameof(Index));
                }

                _context.PushNotifications.Remove(notification);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Notification deleted: {notification.Title}");
                TempData["Success"] = "Notification deleted successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting notification");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> SendTestNotification()
        {
            try
            {
                var devices = await _context.MobileDevices
                    .Where(d => d.IsActive && d.NotificationsEnabled)
                    .Take(1)
                    .ToListAsync();

                if (!devices.Any())
                {
                    TempData["Error"] = "No active devices with notifications enabled found";
                    return RedirectToAction(nameof(Index));
                }

                var device = devices.First();
                var notification = new PushNotification
                {
                    Name = "Test Notification",
                    Title = "Test Notification",
                    Body = "This is a test notification from RMMS",
                    UserId = device.UserId,
                    DeviceId = device.Id,
                    Data = JsonSerializer.Serialize(new { type = "test", timestamp = DateTime.UtcNow }),
                    CreatedAt = DateTime.UtcNow,
                    SentAt = DateTime.UtcNow,
                    Status = "sent"
                };

                _context.PushNotifications.Add(notification);
                await _context.SaveChangesAsync();

                TempData["Success"] = $"✓ Test notification sent successfully to {device.Platform} device (User: {device.UserId})";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending test notification");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
