using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using RMMS.DataAccess.Context;
using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Mobile
{
    public class PushNotificationService : IPushNotificationService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<PushNotificationService> _logger;
        private readonly IConfiguration _configuration;
        private readonly HttpClient _httpClient;

        public PushNotificationService(
            ApplicationDbContext context,
            ILogger<PushNotificationService> logger,
            IConfiguration configuration,
            HttpClient httpClient)
        {
            _context = context;
            _logger = logger;
            _configuration = configuration;
            _httpClient = httpClient;
        }

        public async Task<bool> SendToUserAsync(string userId, SendPushNotificationDto dto)
        {
            try
            {
                // Get all active devices for the user
                var devices = await _context.MobileDevices
                    .Where(d => d.UserId == userId && d.IsActive && d.NotificationsEnabled)
                    .ToListAsync();

                if (!devices.Any())
                {
                    _logger.LogWarning($"No active devices found for user {userId}");
                    return false;
                }

                int successCount = 0;
                foreach (var device in devices)
                {
                    var sent = await SendToDeviceInternalAsync(device, dto);
                    if (sent) successCount++;
                }

                return successCount > 0;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending notification to user {userId}");
                return false;
            }
        }

        public async Task<bool> SendToDeviceAsync(int deviceId, SendPushNotificationDto dto)
        {
            try
            {
                var device = await _context.MobileDevices
                    .FirstOrDefaultAsync(d => d.Id == deviceId && d.IsActive && d.NotificationsEnabled);

                if (device == null)
                {
                    _logger.LogWarning($"Device {deviceId} not found or notifications disabled");
                    return false;
                }

                return await SendToDeviceInternalAsync(device, dto);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending notification to device {deviceId}");
                return false;
            }
        }

        public async Task<int> SendBroadcastAsync(SendPushNotificationDto dto)
        {
            try
            {
                var devices = await _context.MobileDevices
                    .Where(d => d.IsActive && d.NotificationsEnabled)
                    .ToListAsync();

                int successCount = 0;
                foreach (var device in devices)
                {
                    var sent = await SendToDeviceInternalAsync(device, dto);
                    if (sent) successCount++;
                }

                _logger.LogInformation($"Broadcast sent to {successCount} devices");
                return successCount;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending broadcast notification");
                return 0;
            }
        }

        public async Task<int> SendToMultipleUsersAsync(List<string> userIds, SendPushNotificationDto dto)
        {
            try
            {
                var devices = await _context.MobileDevices
                    .Where(d => userIds.Contains(d.UserId) && d.IsActive && d.NotificationsEnabled)
                    .ToListAsync();

                int successCount = 0;
                foreach (var device in devices)
                {
                    var sent = await SendToDeviceInternalAsync(device, dto);
                    if (sent) successCount++;
                }

                return successCount;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending notification to multiple users");
                return 0;
            }
        }

        public async Task<int> ScheduleNotificationAsync(SendPushNotificationDto dto)
        {
            try
            {
                var notification = new PushNotification
                {
                    UserId = dto.UserId,
                    DeviceId = dto.DeviceId,
                    Title = dto.Title,
                    Body = dto.Body,
                    Type = dto.Type,
                    Data = dto.Data != null ? JsonSerializer.Serialize(dto.Data) : null,
                    Priority = dto.Priority,
                    ImageUrl = dto.ImageUrl,
                    ActionUrl = dto.ActionUrl,
                    ScheduledFor = dto.ScheduledFor ?? DateTime.UtcNow,
                    Status = "pending",
                    CreatedAt = DateTime.UtcNow
                };

                _context.PushNotifications.Add(notification);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Notification scheduled for {notification.ScheduledFor}");
                return notification.Id;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error scheduling notification");
                return 0;
            }
        }

        public async Task<List<NotificationDto>> GetUserNotificationsAsync(string userId, int pageSize = 50, int pageNumber = 1)
        {
            var notifications = await _context.PushNotifications
                .Where(n => n.UserId == userId)
                .OrderByDescending(n => n.CreatedAt)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return notifications.Select(n => new NotificationDto
            {
                Id = n.Id,
                Title = n.Title,
                Body = n.Body,
                Type = n.Type,
                Data = n.Data != null ? JsonSerializer.Deserialize<Dictionary<string, string>>(n.Data) : null,
                ImageUrl = n.ImageUrl,
                ActionUrl = n.ActionUrl,
                CreatedAt = n.CreatedAt,
                IsRead = n.IsRead,
                ReadAt = n.ReadAt
            }).ToList();
        }

        public async Task<bool> MarkAsReadAsync(int notificationId, string userId)
        {
            try
            {
                var notification = await _context.PushNotifications
                    .FirstOrDefaultAsync(n => n.Id == notificationId && n.UserId == userId);

                if (notification == null) return false;

                notification.IsRead = true;
                notification.ReadAt = DateTime.UtcNow;

                _context.PushNotifications.Update(notification);
                await _context.SaveChangesAsync();

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error marking notification {notificationId} as read");
                return false;
            }
        }

        public async Task<int> MarkAllAsReadAsync(string userId)
        {
            try
            {
                var unreadNotifications = await _context.PushNotifications
                    .Where(n => n.UserId == userId && !n.IsRead)
                    .ToListAsync();

                foreach (var notification in unreadNotifications)
                {
                    notification.IsRead = true;
                    notification.ReadAt = DateTime.UtcNow;
                }

                await _context.SaveChangesAsync();
                return unreadNotifications.Count;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error marking all notifications as read for user {userId}");
                return 0;
            }
        }

        public async Task<int> GetUnreadCountAsync(string userId)
        {
            return await _context.PushNotifications
                .CountAsync(n => n.UserId == userId && !n.IsRead);
        }

        public async Task ProcessScheduledNotificationsAsync()
        {
            try
            {
                var now = DateTime.UtcNow;
                var pendingNotifications = await _context.PushNotifications
                    .Where(n => n.Status == "pending" && n.ScheduledFor <= now)
                    .ToListAsync();

                foreach (var notification in pendingNotifications)
                {
                    try
                    {
                        bool sent = false;

                        if (notification.DeviceId.HasValue)
                        {
                            var device = await _context.MobileDevices.FindAsync(notification.DeviceId.Value);
                            if (device != null)
                            {
                                sent = await SendToDeviceInternalAsync(device, new SendPushNotificationDto
                                {
                                    Title = notification.Title,
                                    Body = notification.Body,
                                    Type = notification.Type,
                                    Priority = notification.Priority,
                                    ImageUrl = notification.ImageUrl,
                                    ActionUrl = notification.ActionUrl
                                });
                            }
                        }
                        else if (!string.IsNullOrEmpty(notification.UserId))
                        {
                            sent = await SendToUserAsync(notification.UserId, new SendPushNotificationDto
                            {
                                Title = notification.Title,
                                Body = notification.Body,
                                Type = notification.Type,
                                Priority = notification.Priority,
                                ImageUrl = notification.ImageUrl,
                                ActionUrl = notification.ActionUrl
                            });
                        }

                        notification.Status = sent ? "sent" : "failed";
                        notification.SentAt = DateTime.UtcNow;
                        notification.AttemptCount++;
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, $"Error processing scheduled notification {notification.Id}");
                        notification.Status = "failed";
                        notification.ErrorMessage = ex.Message;
                        notification.AttemptCount++;
                    }
                }

                await _context.SaveChangesAsync();
                _logger.LogInformation($"Processed {pendingNotifications.Count} scheduled notifications");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing scheduled notifications");
            }
        }

        private async Task<bool> SendToDeviceInternalAsync(MobileDevice device, SendPushNotificationDto dto)
        {
            try
            {
                // Save notification to database
                var notification = new PushNotification
                {
                    UserId = device.UserId,
                    DeviceId = device.Id,
                    Title = dto.Title,
                    Body = dto.Body,
                    Type = dto.Type,
                    Data = dto.Data != null ? JsonSerializer.Serialize(dto.Data) : null,
                    Priority = dto.Priority,
                    ImageUrl = dto.ImageUrl,
                    ActionUrl = dto.ActionUrl,
                    CreatedAt = DateTime.UtcNow,
                    Status = "pending"
                };

                _context.PushNotifications.Add(notification);

                bool sent = false;

                // Send based on platform
                if (device.Platform == "Android")
                {
                    sent = await SendFCMNotificationAsync(device.PushToken, dto);
                }
                else if (device.Platform == "iOS")
                {
                    sent = await SendAPNSNotificationAsync(device.PushToken, dto);
                }

                notification.Status = sent ? "sent" : "failed";
                notification.SentAt = sent ? DateTime.UtcNow : null;
                notification.AttemptCount = 1;

                await _context.SaveChangesAsync();

                return sent;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending notification to device {device.Id}");
                return false;
            }
        }

        private async Task<bool> SendFCMNotificationAsync(string token, SendPushNotificationDto dto)
        {
            try
            {
                var fcmServerKey = _configuration["Firebase:ServerKey"];
                if (string.IsNullOrEmpty(fcmServerKey))
                {
                    _logger.LogWarning("FCM server key not configured");
                    return false;
                }

                var payload = new
                {
                    to = token,
                    priority = dto.Priority,
                    notification = new
                    {
                        title = dto.Title,
                        body = dto.Body,
                        image = dto.ImageUrl,
                        click_action = dto.ActionUrl
                    },
                    data = dto.Data
                };

                var request = new HttpRequestMessage(HttpMethod.Post, "https://fcm.googleapis.com/fcm/send");
                request.Headers.Add("Authorization", $"key={fcmServerKey}");
                request.Content = new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json");

                var response = await _httpClient.SendAsync(request);
                var success = response.IsSuccessStatusCode;

                if (!success)
                {
                    var error = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"FCM send failed: {error}");
                }

                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending FCM notification");
                return false;
            }
        }

        private Task<bool> SendAPNSNotificationAsync(string token, SendPushNotificationDto dto)
        {
            try
            {
                // NOTE: APNS requires more complex setup with certificates
                // This is a placeholder implementation
                // In production, use a library like dotAPNS or Apple's official SDK

                var apnsKeyId = _configuration["APNS:KeyId"];
                var apnsTeamId = _configuration["APNS:TeamId"];
                var apnsBundleId = _configuration["APNS:BundleId"];

                if (string.IsNullOrEmpty(apnsKeyId))
                {
                    _logger.LogWarning("APNS not configured");
                    return Task.FromResult(false);
                }

                // TODO: Implement actual APNS sending using JWT or certificate-based authentication
                // For now, log that APNS would be sent
                _logger.LogInformation($"APNS notification would be sent to token: {token.Substring(0, 10)}...");

                return Task.FromResult(true);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending APNS notification");
                return Task.FromResult(false);
            }
        }
    }
}
