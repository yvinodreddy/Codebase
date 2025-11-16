using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for managing mobile app configuration and feature flags
    /// </summary>
    public interface IMobileConfigService
    {
        /// <summary>
        /// Get configuration for a specific platform
        /// </summary>
        Task<MobileAppConfigDto?> GetConfigAsync(string platform, string appVersion);

        /// <summary>
        /// Get active configuration for all platforms
        /// </summary>
        Task<List<MobileAppConfig>> GetAllConfigsAsync();

        /// <summary>
        /// Create or update configuration
        /// </summary>
        Task<MobileAppConfig> SaveConfigAsync(MobileAppConfig config);

        /// <summary>
        /// Check if app version is supported
        /// </summary>
        Task<bool> IsVersionSupportedAsync(string platform, string appVersion);

        /// <summary>
        /// Check if force update is required
        /// </summary>
        Task<bool> IsForceUpdateRequiredAsync(string platform, string appVersion);

        /// <summary>
        /// Check if app is in maintenance mode
        /// </summary>
        Task<bool> IsMaintenanceModeAsync(string platform);

        /// <summary>
        /// Get feature flag value
        /// </summary>
        Task<bool> GetFeatureFlagAsync(string platform, string featureName);

        /// <summary>
        /// Update feature flags
        /// </summary>
        Task<bool> UpdateFeatureFlagsAsync(string platform, Dictionary<string, bool> flags);
    }
}
