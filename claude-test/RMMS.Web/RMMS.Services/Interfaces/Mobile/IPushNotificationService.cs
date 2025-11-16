using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for sending push notifications to mobile devices
    /// </summary>
    public interface IPushNotificationService
    {
        /// <summary>
        /// Send a push notification to a specific user
        /// </summary>
        Task<bool> SendToUserAsync(string userId, SendPushNotificationDto dto);

        /// <summary>
        /// Send a push notification to a specific device
        /// </summary>
        Task<bool> SendToDeviceAsync(int deviceId, SendPushNotificationDto dto);

        /// <summary>
        /// Send a push notification to all active devices
        /// </summary>
        Task<int> SendBroadcastAsync(SendPushNotificationDto dto);

        /// <summary>
        /// Send push notification to multiple users
        /// </summary>
        Task<int> SendToMultipleUsersAsync(List<string> userIds, SendPushNotificationDto dto);

        /// <summary>
        /// Schedule a push notification for later delivery
        /// </summary>
        Task<int> ScheduleNotificationAsync(SendPushNotificationDto dto);

        /// <summary>
        /// Get notification history for a user
        /// </summary>
        Task<List<NotificationDto>> GetUserNotificationsAsync(string userId, int pageSize = 50, int pageNumber = 1);

        /// <summary>
        /// Mark notification as read
        /// </summary>
        Task<bool> MarkAsReadAsync(int notificationId, string userId);

        /// <summary>
        /// Mark all notifications as read for a user
        /// </summary>
        Task<int> MarkAllAsReadAsync(string userId);

        /// <summary>
        /// Get unread notification count
        /// </summary>
        Task<int> GetUnreadCountAsync(string userId);

        /// <summary>
        /// Process scheduled notifications (called by background job)
        /// </summary>
        Task ProcessScheduledNotificationsAsync();
    }
}
