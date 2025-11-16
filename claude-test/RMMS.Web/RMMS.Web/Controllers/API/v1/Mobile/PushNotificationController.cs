using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System.Security.Claims;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers.API.v1.Mobile
{
    /// <summary>
    /// API controller for push notifications
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    public class PushNotificationController : BaseApiController
    {
        private readonly IPushNotificationService _notificationService;

        public PushNotificationController(IPushNotificationService notificationService)
        {
            _notificationService = notificationService;
        }

        /// <summary>
        /// Get notification history for current user
        /// </summary>
        [HttpGet("history")]
        public async Task<IActionResult> GetHistory([FromQuery] int pageSize = 50, [FromQuery] int pageNumber = 1)
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var notifications = await _notificationService.GetUserNotificationsAsync(userId, pageSize, pageNumber);
            return Success(notifications);
        }

        /// <summary>
        /// Get unread notification count
        /// </summary>
        [HttpGet("unread-count")]
        public async Task<IActionResult> GetUnreadCount()
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var count = await _notificationService.GetUnreadCountAsync(userId);
            return Success(new { unreadCount = count });
        }

        /// <summary>
        /// Mark a notification as read
        /// </summary>
        [HttpPost("{notificationId}/mark-read")]
        public async Task<IActionResult> MarkAsRead(int notificationId)
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var success = await _notificationService.MarkAsReadAsync(notificationId, userId);
            return success
                ? Success("Notification marked as read")
                : Error("Notification not found", null, 404);
        }

        /// <summary>
        /// Mark all notifications as read
        /// </summary>
        [HttpPost("mark-all-read")]
        public async Task<IActionResult> MarkAllAsRead()
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var count = await _notificationService.MarkAllAsReadAsync(userId);
            return Success(new { markedCount = count }, $"Marked {count} notifications as read");
        }

        /// <summary>
        /// Send a push notification (Admin only)
        /// </summary>
        [HttpPost("send")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Send([FromBody] SendPushNotificationDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            bool success;
            if (dto.DeviceId.HasValue)
            {
                success = await _notificationService.SendToDeviceAsync(dto.DeviceId.Value, dto);
            }
            else if (!string.IsNullOrEmpty(dto.UserId))
            {
                success = await _notificationService.SendToUserAsync(dto.UserId, dto);
            }
            else
            {
                return ValidationError("Either DeviceId or UserId must be specified");
            }

            return success
                ? Success("Notification sent successfully")
                : Error("Failed to send notification");
        }

        /// <summary>
        /// Schedule a push notification (Admin only)
        /// </summary>
        [HttpPost("schedule")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Schedule([FromBody] SendPushNotificationDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            if (!dto.ScheduledFor.HasValue)
                return ValidationError("ScheduledFor is required for scheduled notifications");

            var notificationId = await _notificationService.ScheduleNotificationAsync(dto);
            return notificationId > 0
                ? Success(new { notificationId }, "Notification scheduled successfully")
                : Error("Failed to schedule notification");
        }
    }
}
