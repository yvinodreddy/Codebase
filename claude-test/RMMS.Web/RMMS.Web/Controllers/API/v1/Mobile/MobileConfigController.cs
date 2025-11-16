using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Interfaces.Mobile;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers.API.v1.Mobile
{
    /// <summary>
    /// API controller for mobile app configuration
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    public class MobileConfigController : BaseApiController
    {
        private readonly IMobileConfigService _configService;

        public MobileConfigController(IMobileConfigService configService)
        {
            _configService = configService;
        }

        /// <summary>
        /// Get configuration for mobile app (public endpoint)
        /// </summary>
        [HttpGet]
        [AllowAnonymous]
        public async Task<IActionResult> GetConfig([FromQuery] string platform, [FromQuery] string appVersion)
        {
            if (string.IsNullOrEmpty(platform) || string.IsNullOrEmpty(appVersion))
                return ValidationError("Platform and appVersion are required");

            var config = await _configService.GetConfigAsync(platform, appVersion);

            if (config == null)
                return Error("Configuration not found", null, 404);

            return Success(config);
        }

        /// <summary>
        /// Check if app version is supported
        /// </summary>
        [HttpGet("version-check")]
        [AllowAnonymous]
        public async Task<IActionResult> CheckVersion([FromQuery] string platform, [FromQuery] string appVersion)
        {
            var isSupported = await _configService.IsVersionSupportedAsync(platform, appVersion);
            var forceUpdate = await _configService.IsForceUpdateRequiredAsync(platform, appVersion);
            var maintenanceMode = await _configService.IsMaintenanceModeAsync(platform);

            return Success(new
            {
                isSupported,
                forceUpdate,
                maintenanceMode
            });
        }

        /// <summary>
        /// Get feature flag value
        /// </summary>
        [HttpGet("feature-flag/{featureName}")]
        [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
        public async Task<IActionResult> GetFeatureFlag(string featureName, [FromQuery] string platform)
        {
            var isEnabled = await _configService.GetFeatureFlagAsync(platform, featureName);
            return Success(new { featureName, isEnabled });
        }
    }
}
