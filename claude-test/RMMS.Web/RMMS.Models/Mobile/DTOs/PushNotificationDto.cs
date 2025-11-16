using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// DTO for sending push notifications
    /// </summary>
    public class SendPushNotificationDto
    {
        [MaxLength(100)]
        public string? UserId { get; set; }

        public int? DeviceId { get; set; }

        [Required]
        [MaxLength(100)]
        public string Title { get; set; } = string.Empty;

        [Required]
        [MaxLength(500)]
        public string Body { get; set; } = string.Empty;

        [MaxLength(50)]
        public string? Type { get; set; }

        public Dictionary<string, string>? Data { get; set; }

        [MaxLength(20)]
        public string Priority { get; set; } = "normal";

        [MaxLength(500)]
        public string? ImageUrl { get; set; }

        [MaxLength(500)]
        public string? ActionUrl { get; set; }

        public DateTime? ScheduledFor { get; set; }
    }

    /// <summary>
    /// DTO for notification history
    /// </summary>
    public class NotificationDto
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Body { get; set; } = string.Empty;
        public string? Type { get; set; }
        public Dictionary<string, string>? Data { get; set; }
        public string? ImageUrl { get; set; }
        public string? ActionUrl { get; set; }
        public DateTime CreatedAt { get; set; }
        public bool IsRead { get; set; }
        public DateTime? ReadAt { get; set; }
    }
}
