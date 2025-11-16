using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Mobile
{
    /// <summary>
    /// Tracks analytics events from mobile apps
    /// </summary>
    public class MobileAnalyticsEvent
    {
        [Key]
        public int Id { get; set; }

        /// <summary>
        /// Device that generated the event
        /// </summary>
        public int? DeviceId { get; set; }

        /// <summary>
        /// User who performed the action
        /// </summary>
        [MaxLength(100)]
        public string? UserId { get; set; }

        /// <summary>
        /// Event category (e.g., "navigation", "action", "error", "performance")
        /// </summary>
        [Required]
        [MaxLength(50)]
        public string Category { get; set; } = string.Empty;

        /// <summary>
        /// Event action (e.g., "screen_view", "button_click", "api_call")
        /// </summary>
        [Required]
        [MaxLength(100)]
        public string Action { get; set; } = string.Empty;

        /// <summary>
        /// Event label/description
        /// </summary>
        [MaxLength(200)]
        public string? Label { get; set; }

        /// <summary>
        /// Numeric value associated with event
        /// </summary>
        public decimal? Value { get; set; }

        /// <summary>
        /// Screen/page where event occurred
        /// </summary>
        [MaxLength(100)]
        public string? Screen { get; set; }

        /// <summary>
        /// Session ID
        /// </summary>
        [MaxLength(100)]
        public string? SessionId { get; set; }

        /// <summary>
        /// Additional event properties (JSON)
        /// </summary>
        public string? Properties { get; set; }

        /// <summary>
        /// Client timestamp when event occurred
        /// </summary>
        public DateTime ClientTimestamp { get; set; }

        /// <summary>
        /// Server timestamp when event was received
        /// </summary>
        public DateTime ServerTimestamp { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Platform (Android or iOS)
        /// </summary>
        [MaxLength(20)]
        public string? Platform { get; set; }

        /// <summary>
        /// App version
        /// </summary>
        [MaxLength(20)]
        public string? AppVersion { get; set; }

        [ForeignKey("DeviceId")]
        public virtual MobileDevice? Device { get; set; }
    }
}
