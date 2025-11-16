using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Mobile
{
    public class MobileConfigService : IMobileConfigService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MobileConfigService> _logger;

        public MobileConfigService(
            ApplicationDbContext context,
            ILogger<MobileConfigService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<MobileAppConfigDto?> GetConfigAsync(string platform, string appVersion)
        {
            try
            {
                // Get platform-specific config first, fallback to "All" platform
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && (c.Platform == platform || c.Platform == "All"))
                    .OrderByDescending(c => c.Platform == platform ? 1 : 0)
                    .FirstOrDefaultAsync();

                if (config == null) return null;

                return new MobileAppConfigDto
                {
                    MinAppVersion = config.MinAppVersion,
                    LatestAppVersion = config.LatestAppVersion,
                    ForceUpdate = config.ForceUpdate,
                    UpdateMessage = config.UpdateMessage,
                    MaintenanceMode = config.MaintenanceMode,
                    MaintenanceMessage = config.MaintenanceMessage,
                    FeatureFlags = config.FeatureFlags != null
                        ? JsonSerializer.Deserialize<Dictionary<string, bool>>(config.FeatureFlags)
                        : new Dictionary<string, bool>(),
                    ApiEndpoint = config.ApiEndpoint,
                    SyncIntervalMinutes = config.SyncIntervalMinutes,
                    MaxOfflineDataDays = config.MaxOfflineDataDays,
                    EnableCrashReporting = config.EnableCrashReporting,
                    EnableAnalytics = config.EnableAnalytics,
                    EnableDebugLogging = config.EnableDebugLogging,
                    MaxImageSizeMB = config.MaxImageSizeMB,
                    ImageCompressionQuality = config.ImageCompressionQuality
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting config for platform {platform}");
                return null;
            }
        }

        public async Task<List<MobileAppConfig>> GetAllConfigsAsync()
        {
            return await _context.MobileAppConfigs
                .Where(c => c.IsActive)
                .OrderBy(c => c.Platform)
                .ToListAsync();
        }

        public async Task<MobileAppConfig> SaveConfigAsync(MobileAppConfig config)
        {
            try
            {
                if (config.Id > 0)
                {
                    config.UpdatedAt = DateTime.UtcNow;
                    _context.MobileAppConfigs.Update(config);
                }
                else
                {
                    config.CreatedAt = DateTime.UtcNow;
                    _context.MobileAppConfigs.Add(config);
                }

                await _context.SaveChangesAsync();
                _logger.LogInformation($"Mobile config saved for platform {config.Platform}");

                return config;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error saving mobile config");
                throw;
            }
        }

        public async Task<bool> IsVersionSupportedAsync(string platform, string appVersion)
        {
            try
            {
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && (c.Platform == platform || c.Platform == "All"))
                    .OrderByDescending(c => c.Platform == platform ? 1 : 0)
                    .FirstOrDefaultAsync();

                if (config == null || string.IsNullOrEmpty(config.MinAppVersion))
                    return true; // No restrictions

                return CompareVersions(appVersion, config.MinAppVersion) >= 0;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking version support");
                return true; // Allow by default on error
            }
        }

        public async Task<bool> IsForceUpdateRequiredAsync(string platform, string appVersion)
        {
            try
            {
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && (c.Platform == platform || c.Platform == "All"))
                    .OrderByDescending(c => c.Platform == platform ? 1 : 0)
                    .FirstOrDefaultAsync();

                if (config == null || !config.ForceUpdate)
                    return false;

                if (string.IsNullOrEmpty(config.MinAppVersion))
                    return false;

                return CompareVersions(appVersion, config.MinAppVersion) < 0;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking force update");
                return false;
            }
        }

        public async Task<bool> IsMaintenanceModeAsync(string platform)
        {
            try
            {
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && (c.Platform == platform || c.Platform == "All"))
                    .OrderByDescending(c => c.Platform == platform ? 1 : 0)
                    .FirstOrDefaultAsync();

                return config?.MaintenanceMode ?? false;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking maintenance mode");
                return false;
            }
        }

        public async Task<bool> GetFeatureFlagAsync(string platform, string featureName)
        {
            try
            {
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && (c.Platform == platform || c.Platform == "All"))
                    .OrderByDescending(c => c.Platform == platform ? 1 : 0)
                    .FirstOrDefaultAsync();

                if (config == null || string.IsNullOrEmpty(config.FeatureFlags))
                    return false;

                var flags = JsonSerializer.Deserialize<Dictionary<string, bool>>(config.FeatureFlags);
                return flags != null && flags.ContainsKey(featureName) && flags[featureName];
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting feature flag {featureName}");
                return false;
            }
        }

        public async Task<bool> UpdateFeatureFlagsAsync(string platform, Dictionary<string, bool> flags)
        {
            try
            {
                var config = await _context.MobileAppConfigs
                    .Where(c => c.IsActive && c.Platform == platform)
                    .FirstOrDefaultAsync();

                if (config == null) return false;

                config.FeatureFlags = JsonSerializer.Serialize(flags);
                config.UpdatedAt = DateTime.UtcNow;

                _context.MobileAppConfigs.Update(config);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Feature flags updated for platform {platform}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating feature flags");
                return false;
            }
        }

        private int CompareVersions(string version1, string version2)
        {
            try
            {
                var v1Parts = version1.Split('.').Select(int.Parse).ToArray();
                var v2Parts = version2.Split('.').Select(int.Parse).ToArray();

                int length = Math.Max(v1Parts.Length, v2Parts.Length);

                for (int i = 0; i < length; i++)
                {
                    int v1Part = i < v1Parts.Length ? v1Parts[i] : 0;
                    int v2Part = i < v2Parts.Length ? v2Parts[i] : 0;

                    if (v1Part > v2Part) return 1;
                    if (v1Part < v2Part) return -1;
                }

                return 0;
            }
            catch
            {
                return 0; // Equal if parsing fails
            }
        }
    }
}
