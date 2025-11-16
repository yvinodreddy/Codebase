using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;

namespace RMMS.Services.Services.Notifications
{
    /// <summary>
    /// TASK 4.4.4: Push Notification Service (Firebase) Implementation
    /// Sends push notifications to mobile devices
    /// This is a lightweight adapter that wraps the comprehensive Mobile.PushNotificationService
    /// </summary>
    public class PushNotificationService : IPushNotificationService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<PushNotificationService> _logger;
        private readonly Interfaces.Mobile.IPushNotificationService _mobilePushService;

        public PushNotificationService(
            ApplicationDbContext context,
            ILogger<PushNotificationService> logger,
            Interfaces.Mobile.IPushNotificationService mobilePushService)
        {
            _context = context;
            _logger = logger;
            _mobilePushService = mobilePushService;
        }

        public async Task<bool> SendNotificationAsync(string userId, string title, string body, object? data = null)
        {
            try
            {
                var dto = new SendPushNotificationDto
                {
                    Title = title,
                    Body = body,
                    Data = data as System.Collections.Generic.Dictionary<string, string> ?? new System.Collections.Generic.Dictionary<string, string>()
                };

                var result = await _mobilePushService.SendToUserAsync(userId, dto);

                _logger.LogInformation($"Push notification sent to user {userId}: {title}");
                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending push notification to user {userId}");
                return false;
            }
        }

        public async Task<bool> SendToTokenAsync(string deviceToken, string title, string body, object? data = null)
        {
            try
            {
                // Find device by token
                var device = await _context.MobileDevices
                    .FirstOrDefaultAsync(d => d.PushToken == deviceToken && d.IsActive);

                if (device == null)
                {
                    _logger.LogWarning($"Device not found for token: {deviceToken}");
                    return false;
                }

                var dto = new SendPushNotificationDto
                {
                    Title = title,
                    Body = body,
                    Data = data as System.Collections.Generic.Dictionary<string, string> ?? new System.Collections.Generic.Dictionary<string, string>()
                };

                var result = await _mobilePushService.SendToDeviceAsync(device.Id, dto);

                _logger.LogInformation($"Push notification sent to device token: {title}");
                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending push notification to device token");
                return false;
            }
        }

        public async Task<bool> SendToTopicAsync(string topic, string title, string body, object? data = null)
        {
            try
            {
                var dto = new SendPushNotificationDto
                {
                    Title = title,
                    Body = body,
                    Data = data as System.Collections.Generic.Dictionary<string, string> ?? new System.Collections.Generic.Dictionary<string, string>()
                };

                // Send broadcast to all active devices (simulates topic)
                var result = await _mobilePushService.SendBroadcastAsync(dto);

                _logger.LogInformation($"Push notification sent to topic {topic}: {title} (reached {result} devices)");
                return result > 0;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error sending push notification to topic {topic}");
                return false;
            }
        }

        public async Task<bool> RegisterDeviceTokenAsync(string userId, string deviceToken, string platform)
        {
            try
            {
                // Check if device already exists
                var existingDevice = await _context.MobileDevices
                    .FirstOrDefaultAsync(d => d.PushToken == deviceToken);

                if (existingDevice != null)
                {
                    // Update existing device
                    existingDevice.UserId = userId;
                    existingDevice.Platform = platform;
                    existingDevice.LastActiveAt = DateTime.UtcNow;
                    existingDevice.IsActive = true;
                }
                else
                {
                    // Create new device
                    var newDevice = new MobileDevice
                    {
                        UserId = userId,
                        DeviceId = Guid.NewGuid().ToString(), // Generate unique device ID
                        Platform = platform,
                        PushToken = deviceToken,
                        IsActive = true,
                        NotificationsEnabled = true,
                        RegisteredAt = DateTime.UtcNow,
                        LastActiveAt = DateTime.UtcNow
                    };
                    _context.MobileDevices.Add(newDevice);
                }

                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device token registered for user {userId} on {platform}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error registering device token for user {userId}");
                return false;
            }
        }

        public async Task<bool> UnregisterDeviceTokenAsync(string deviceToken)
        {
            try
            {
                var device = await _context.MobileDevices
                    .FirstOrDefaultAsync(d => d.PushToken == deviceToken);

                if (device == null)
                {
                    _logger.LogWarning($"Device not found for unregistration: {deviceToken}");
                    return false;
                }

                device.IsActive = false;
                device.PushToken = string.Empty; // Clear token instead of null
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device token unregistered successfully");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error unregistering device token");
                return false;
            }
        }
    }
}
