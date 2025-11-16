using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile
{
    /// <summary>
    /// Mobile app configuration and feature flags
    /// </summary>
    public class MobileAppConfig
    {
        [Key]
        public int Id { get; set; }

        /// <summary>
        /// Platform: Android, iOS, or "All"
        /// </summary>
        [Required]
        [MaxLength(20)]
        public string Platform { get; set; } = "All";

        /// <summary>
        /// Minimum supported app version
        /// </summary>
        [MaxLength(20)]
        public string? MinAppVersion { get; set; }

        /// <summary>
        /// Latest available app version
        /// </summary>
        [MaxLength(20)]
        public string? LatestAppVersion { get; set; }

        /// <summary>
        /// Whether this version is forced (users must update)
        /// </summary>
        public bool ForceUpdate { get; set; } = false;

        /// <summary>
        /// Update message to display to users
        /// </summary>
        [MaxLength(500)]
        public string? UpdateMessage { get; set; }

        /// <summary>
        /// Whether the app is in maintenance mode
        /// </summary>
        public bool MaintenanceMode { get; set; } = false;

        /// <summary>
        /// Maintenance message
        /// </summary>
        [MaxLength(500)]
        public string? MaintenanceMessage { get; set; }

        /// <summary>
        /// Feature flags (JSON object)
        /// </summary>
        public string? FeatureFlags { get; set; }

        /// <summary>
        /// API endpoint configuration
        /// </summary>
        [MaxLength(500)]
        public string? ApiEndpoint { get; set; }

        /// <summary>
        /// Sync interval in minutes
        /// </summary>
        public int SyncIntervalMinutes { get; set; } = 15;

        /// <summary>
        /// Maximum offline data age in days
        /// </summary>
        public int MaxOfflineDataDays { get; set; } = 7;

        /// <summary>
        /// Whether to enable crash reporting
        /// </summary>
        public bool EnableCrashReporting { get; set; } = true;

        /// <summary>
        /// Whether to enable analytics
        /// </summary>
        public bool EnableAnalytics { get; set; } = true;

        /// <summary>
        /// Whether to enable debug logging
        /// </summary>
        public bool EnableDebugLogging { get; set; } = false;

        /// <summary>
        /// Maximum image upload size in MB
        /// </summary>
        public int MaxImageSizeMB { get; set; } = 10;

        /// <summary>
        /// Image compression quality (0-100)
        /// </summary>
        public int ImageCompressionQuality { get; set; } = 80;

        /// <summary>
        /// When this configuration was created
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// When this configuration was last updated
        /// </summary>
        public DateTime? UpdatedAt { get; set; }

        /// <summary>
        /// Whether this configuration is active
        /// </summary>
        public bool IsActive { get; set; } = true;
    }
}
