using System;
using System.Collections.Generic;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// Mobile app configuration DTO
    /// </summary>
    public class MobileAppConfigDto
    {
        public string? MinAppVersion { get; set; }
        public string? LatestAppVersion { get; set; }
        public bool ForceUpdate { get; set; }
        public string? UpdateMessage { get; set; }
        public bool MaintenanceMode { get; set; }
        public string? MaintenanceMessage { get; set; }
        public Dictionary<string, bool>? FeatureFlags { get; set; }
        public string? ApiEndpoint { get; set; }
        public int SyncIntervalMinutes { get; set; }
        public int MaxOfflineDataDays { get; set; }
        public bool EnableCrashReporting { get; set; }
        public bool EnableAnalytics { get; set; }
        public bool EnableDebugLogging { get; set; }
        public int MaxImageSizeMB { get; set; }
        public int ImageCompressionQuality { get; set; }
    }
}
