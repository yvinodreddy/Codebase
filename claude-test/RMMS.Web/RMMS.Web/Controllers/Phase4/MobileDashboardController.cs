using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using RMMS.Models.Mobile;

namespace RMMS.Web.Controllers.Phase4
{
    [Authorize]
    public class MobileDashboardController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MobileDashboardController> _logger;

        public MobileDashboardController(
            ApplicationDbContext context,
            ILogger<MobileDashboardController> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Get all mobile devices
                var devices = await _context.MobileDevices.ToListAsync();
                var analyticsEvents = await _context.Set<MobileAnalyticsEvent>().ToListAsync();

                // Device statistics
                ViewBag.TotalDevices = devices.Count;
                ViewBag.AndroidCount = devices.Count(d => d.Platform == "Android");
                ViewBag.iOSCount = devices.Count(d => d.Platform == "iOS");

                // Calculate platform percentages (capped at 100%)
                ViewBag.AndroidPercent = devices.Any()
                    ? Math.Min(100, Math.Round((devices.Count(d => d.Platform == "Android") / (double)devices.Count) * 100, 1))
                    : 0;
                ViewBag.iOSPercent = devices.Any()
                    ? Math.Min(100, Math.Round((devices.Count(d => d.Platform == "iOS") / (double)devices.Count) * 100, 1))
                    : 0;

                // Daily Active Users (DAU) - devices active today
                var today = DateTime.UtcNow.Date;
                ViewBag.DAU = devices.Count(d =>
                    d.LastActiveAt.HasValue && d.LastActiveAt.Value.Date == today);

                // Monthly Active Users (MAU) - devices active in last 30 days
                var thirtyDaysAgo = DateTime.UtcNow.AddDays(-30);
                ViewBag.MAU = devices.Count(d =>
                    d.LastActiveAt.HasValue && d.LastActiveAt.Value > thirtyDaysAgo);

                // Weekly Active Users (WAU)
                var sevenDaysAgo = DateTime.UtcNow.AddDays(-7);
                ViewBag.WAU = devices.Count(d =>
                    d.LastActiveAt.HasValue && d.LastActiveAt.Value > sevenDaysAgo);

                // Push notification opt-in rate (capped at 100%)
                ViewBag.PushEnabledCount = devices.Count(d => d.NotificationsEnabled);
                ViewBag.PushOptInRate = devices.Any()
                    ? Math.Min(100, Math.Round((devices.Count(d => d.NotificationsEnabled) / (double)devices.Count) * 100, 1))
                    : 0;

                // Active vs Inactive devices
                ViewBag.ActiveDevicesCount = devices.Count(d => d.IsActive);
                ViewBag.InactiveDevicesCount = devices.Count(d => !d.IsActive);

                // Average session duration (from analytics events)
                var sessionEvents = analyticsEvents
                    .Where(e => e.Category == "performance" && e.Value > 0)
                    .ToList();
                ViewBag.AvgSessionDuration = sessionEvents.Any()
                    ? Math.Round(sessionEvents.Average(e => (double)e.Value!.Value), 1)
                    : 0;

                // Recent activity count (last 24 hours)
                var oneDayAgo = DateTime.UtcNow.AddDays(-1);
                ViewBag.RecentActivityCount = analyticsEvents
                    .Count(e => e.ServerTimestamp > oneDayAgo);

                // Most active screen
                var screenActivity = analyticsEvents
                    .Where(e => !string.IsNullOrEmpty(e.Screen))
                    .GroupBy(e => e.Screen)
                    .Select(g => new { Screen = g.Key, Count = g.Count() })
                    .OrderByDescending(x => x.Count)
                    .FirstOrDefault();
                ViewBag.MostActiveScreen = screenActivity?.Screen ?? "N/A";
                ViewBag.MostActiveScreenViews = screenActivity?.Count ?? 0;

                // Error rate (capped at 100%)
                var errorEvents = analyticsEvents.Count(e => e.Category == "error");
                var totalEvents = analyticsEvents.Count;
                ViewBag.ErrorRate = totalEvents > 0
                    ? Math.Min(100, Math.Round((errorEvents / (double)totalEvents) * 100, 2))
                    : 0;

                // New users this week
                ViewBag.NewUsersThisWeek = devices.Count(d =>
                    d.RegisteredAt > sevenDaysAgo);

                // Engagement metrics for chart
                ViewBag.ChartData = new
                {
                    labels = new[] { "DAU", "WAU", "MAU" },
                    values = new[] { ViewBag.DAU, ViewBag.WAU, ViewBag.MAU }
                };

                return View(devices);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading mobile dashboard");
                TempData["Error"] = "Error loading mobile dashboard: " + ex.Message;
                return View(new List<MobileDevice>());
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetDeviceStats()
        {
            try
            {
                var devices = await _context.MobileDevices.ToListAsync();

                var stats = new
                {
                    total = devices.Count,
                    byPlatform = devices.GroupBy(d => d.Platform)
                        .Select(g => new { platform = g.Key, count = g.Count() })
                        .ToList(),
                    byStatus = devices.GroupBy(d => d.IsActive)
                        .Select(g => new {
                            status = g.Key ? "Active" : "Inactive",
                            count = g.Count()
                        })
                        .ToList(),
                    pushEnabled = devices.Count(d => d.NotificationsEnabled),
                    pushDisabled = devices.Count(d => !d.NotificationsEnabled),
                    recentlyActive = devices.Count(d =>
                        d.LastActiveAt.HasValue &&
                        d.LastActiveAt.Value > DateTime.UtcNow.AddHours(-24))
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting device stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetRecentActivity()
        {
            try
            {
                var recentActivity = await _context.Set<MobileAnalyticsEvent>()
                    .OrderByDescending(e => e.ServerTimestamp)
                    .Take(50)
                    .Select(e => new
                    {
                        e.UserId,
                        e.Category,
                        e.Action,
                        e.Label,
                        e.Screen,
                        e.Platform,
                        e.ServerTimestamp
                    })
                    .ToListAsync();

                return Json(new { success = true, data = recentActivity });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting recent activity");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetUserEngagement()
        {
            try
            {
                var devices = await _context.MobileDevices.ToListAsync();
                var today = DateTime.UtcNow.Date;
                var sevenDaysAgo = DateTime.UtcNow.AddDays(-7);
                var thirtyDaysAgo = DateTime.UtcNow.AddDays(-30);

                var engagement = new
                {
                    dau = devices.Count(d =>
                        d.LastActiveAt.HasValue && d.LastActiveAt.Value.Date == today),
                    wau = devices.Count(d =>
                        d.LastActiveAt.HasValue && d.LastActiveAt.Value > sevenDaysAgo),
                    mau = devices.Count(d =>
                        d.LastActiveAt.HasValue && d.LastActiveAt.Value > thirtyDaysAgo),
                    // DAU/MAU ratio - stickiness metric (capped at 100%)
                    stickinessRatio = devices.Count(d => d.LastActiveAt.HasValue && d.LastActiveAt.Value > thirtyDaysAgo) > 0
                        ? Math.Min(100, Math.Round((devices.Count(d => d.LastActiveAt.HasValue && d.LastActiveAt.Value.Date == today) /
                          (double)devices.Count(d => d.LastActiveAt.HasValue && d.LastActiveAt.Value > thirtyDaysAgo)) * 100, 2))
                        : 0
                };

                return Json(new { success = true, data = engagement });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting user engagement");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetTopScreens()
        {
            try
            {
                var topScreens = await _context.Set<MobileAnalyticsEvent>()
                    .Where(e => !string.IsNullOrEmpty(e.Screen))
                    .GroupBy(e => e.Screen)
                    .Select(g => new
                    {
                        screen = g.Key,
                        views = g.Count(),
                        uniqueUsers = g.Select(x => x.UserId).Distinct().Count()
                    })
                    .OrderByDescending(x => x.views)
                    .Take(10)
                    .ToListAsync();

                return Json(new { success = true, data = topScreens });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting top screens");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetEventsByCategory()
        {
            try
            {
                var eventsByCategory = await _context.Set<MobileAnalyticsEvent>()
                    .GroupBy(e => e.Category)
                    .Select(g => new
                    {
                        category = g.Key,
                        count = g.Count()
                    })
                    .OrderByDescending(x => x.count)
                    .ToListAsync();

                return Json(new { success = true, data = eventsByCategory });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting events by category");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> ToggleDevice(int id)
        {
            try
            {
                var device = await _context.MobileDevices.FindAsync(id);
                if (device == null)
                {
                    TempData["Error"] = "Device not found";
                    return RedirectToAction(nameof(Index));
                }

                device.IsActive = !device.IsActive;
                await _context.SaveChangesAsync();

                TempData["Success"] = $"Device {device.DeviceId} {(device.IsActive ? "activated" : "deactivated")} successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error toggling device");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> DeleteDevice(int id)
        {
            try
            {
                var device = await _context.MobileDevices.FindAsync(id);
                if (device == null)
                {
                    TempData["Error"] = "Device not found";
                    return RedirectToAction(nameof(Index));
                }

                _context.MobileDevices.Remove(device);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device deleted: {device.DeviceId}");
                TempData["Success"] = "Device removed successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting device");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
