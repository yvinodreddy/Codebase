using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Mobile
{
    /// <summary>
    /// Represents a push notification sent to mobile devices
    /// </summary>
    public class PushNotification
    {
        [Key]
        public int Id { get; set; }

        /// <summary>
        /// Target user ID (null for broadcast to all)
        /// </summary>
        [MaxLength(100)]
        public string? UserId { get; set; }

        /// <summary>
        /// Target device ID (null to send to all user's devices)
        /// </summary>
        public int? DeviceId { get; set; }

        /// <summary>
        /// Notification name/identifier (for management UI)
        /// </summary>
        [MaxLength(200)]
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Description (for management UI)
        /// </summary>
        [MaxLength(1000)]
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Notification title
        /// </summary>
        [Required]
        [MaxLength(100)]
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Notification body/message
        /// </summary>
        [Required]
        [MaxLength(500)]
        public string Body { get; set; } = string.Empty;

        /// <summary>
        /// Notification type/category (e.g., "production", "sales", "inventory", "alert")
        /// </summary>
        [MaxLength(50)]
        public string? Type { get; set; }

        /// <summary>
        /// Additional data payload (JSON)
        /// </summary>
        public string? Data { get; set; }

        /// <summary>
        /// Priority: high, normal, low
        /// </summary>
        [MaxLength(20)]
        public string Priority { get; set; } = "normal";

        /// <summary>
        /// Notification icon/image URL
        /// </summary>
        [MaxLength(500)]
        public string? ImageUrl { get; set; }

        /// <summary>
        /// Deep link URL to open when notification is tapped
        /// </summary>
        [MaxLength(500)]
        public string? ActionUrl { get; set; }

        /// <summary>
        /// When the notification was created
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// When the notification should be sent (for scheduled notifications)
        /// </summary>
        public DateTime? ScheduledFor { get; set; }

        /// <summary>
        /// When the notification was actually sent
        /// </summary>
        public DateTime? SentAt { get; set; }

        /// <summary>
        /// Delivery status: pending, sent, delivered, failed
        /// </summary>
        [MaxLength(20)]
        public string Status { get; set; } = "pending";

        /// <summary>
        /// Error message if delivery failed
        /// </summary>
        public string? ErrorMessage { get; set; }

        /// <summary>
        /// Number of delivery attempts
        /// </summary>
        public int AttemptCount { get; set; } = 0;

        /// <summary>
        /// Whether the notification was read/opened
        /// </summary>
        public bool IsRead { get; set; } = false;

        /// <summary>
        /// When the notification was read/opened
        /// </summary>
        public DateTime? ReadAt { get; set; }

        /// <summary>
        /// Whether this notification template is active
        /// </summary>
        public bool IsActive { get; set; } = true;

        /// <summary>
        /// Creation date (alias for CreatedAt for UI compatibility)
        /// </summary>
        public DateTime CreatedDate
        {
            get => CreatedAt;
            set => CreatedAt = value;
        }

        /// <summary>
        /// Last modified date
        /// </summary>
        public DateTime? ModifiedDate { get; set; }

        /// <summary>
        /// User who last modified this notification
        /// </summary>
        [MaxLength(450)]
        public string? ModifiedBy { get; set; }

        [ForeignKey("DeviceId")]
        public virtual MobileDevice? Device { get; set; }
    }
}
