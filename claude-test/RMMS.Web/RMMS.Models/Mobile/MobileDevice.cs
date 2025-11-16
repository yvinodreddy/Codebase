using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Mobile
{
    /// <summary>
    /// Represents a registered mobile device for push notifications and tracking
    /// </summary>
    public class MobileDevice
    {
        [Key]
        public int Id { get; set; }

        /// <summary>
        /// User ID associated with this device
        /// </summary>
        [Required]
        [MaxLength(100)]
        public string UserId { get; set; } = string.Empty;

        /// <summary>
        /// Unique device identifier (UDID, Android ID, etc.)
        /// </summary>
        [Required]
        [MaxLength(200)]
        public string DeviceId { get; set; } = string.Empty;

        /// <summary>
        /// Device platform: Android or iOS
        /// </summary>
        [Required]
        [MaxLength(20)]
        public string Platform { get; set; } = string.Empty; // "Android" or "iOS"

        /// <summary>
        /// Device model (e.g., "iPhone 14 Pro", "Samsung Galaxy S23")
        /// </summary>
        [MaxLength(100)]
        public string? DeviceModel { get; set; }

        /// <summary>
        /// Operating system version
        /// </summary>
        [MaxLength(50)]
        public string? OSVersion { get; set; }

        /// <summary>
        /// Mobile app version
        /// </summary>
        [MaxLength(20)]
        public string? AppVersion { get; set; }

        /// <summary>
        /// Push notification token (FCM for Android, APNS for iOS)
        /// </summary>
        [Required]
        [MaxLength(500)]
        public string PushToken { get; set; } = string.Empty;

        /// <summary>
        /// Device language/locale (e.g., "en-US", "es-ES")
        /// </summary>
        [MaxLength(10)]
        public string? Language { get; set; }

        /// <summary>
        /// Whether push notifications are enabled on this device
        /// </summary>
        public bool NotificationsEnabled { get; set; } = true;

        /// <summary>
        /// Whether biometric authentication is enabled
        /// </summary>
        public bool BiometricEnabled { get; set; } = false;

        /// <summary>
        /// Last time the device was active/synced
        /// </summary>
        public DateTime? LastActiveAt { get; set; }

        /// <summary>
        /// When the device was registered
        /// </summary>
        public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Whether the device is currently active
        /// </summary>
        public bool IsActive { get; set; } = true;

        /// <summary>
        /// Additional device metadata (JSON)
        /// </summary>
        public string? Metadata { get; set; }
    }
}
