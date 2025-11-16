using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.Security.Claims;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers.API.v1.Mobile
{
    /// <summary>
    /// API controller for mobile analytics tracking
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    public class MobileAnalyticsController : BaseApiController
    {
        private readonly IMobileAnalyticsService _analyticsService;

        public MobileAnalyticsController(IMobileAnalyticsService analyticsService)
        {
            _analyticsService = analyticsService;
        }

        /// <summary>
        /// Track a single analytics event
        /// </summary>
        [HttpPost("track")]
        public async Task<IActionResult> TrackEvent([FromBody] AnalyticsEventDto eventDto, [FromQuery] int? deviceId)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

            var success = await _analyticsService.TrackEventAsync(deviceId, userId, eventDto);
            return success
                ? Success("Event tracked successfully")
                : Error("Failed to track event");
        }

        /// <summary>
        /// Track multiple analytics events in batch
        /// </summary>
        [HttpPost("track-batch")]
        public async Task<IActionResult> TrackBatch([FromBody] BatchAnalyticsDto batchDto, [FromQuery] int? deviceId)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

            var count = await _analyticsService.TrackBatchEventsAsync(deviceId, userId, batchDto);
            return Success(new { trackedCount = count }, $"Tracked {count} events");
        }

        /// <summary>
        /// Get analytics summary (Admin only)
        /// </summary>
        [HttpGet("summary")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetSummary([FromQuery] DateTime? startDate, [FromQuery] DateTime? endDate)
        {
            var start = startDate ?? DateTime.UtcNow.AddDays(-30);
            var end = endDate ?? DateTime.UtcNow;

            var summary = await _analyticsService.GetAnalyticsSummaryAsync(start, end);
            return Success(summary);
        }

        /// <summary>
        /// Get popular screens (Admin only)
        /// </summary>
        [HttpGet("popular-screens")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetPopularScreens([FromQuery] int topN = 10)
        {
            var screens = await _analyticsService.GetPopularScreensAsync(topN);
            return Success(screens);
        }

        /// <summary>
        /// Get engagement metrics for current user
        /// </summary>
        [HttpGet("my-engagement")]
        public async Task<IActionResult> GetMyEngagement()
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var metrics = await _analyticsService.GetEngagementMetricsAsync(userId);
            return Success(metrics);
        }

        /// <summary>
        /// Get version distribution (Admin only)
        /// </summary>
        [HttpGet("version-distribution")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetVersionDistribution([FromQuery] string platform)
        {
            if (string.IsNullOrEmpty(platform))
                return ValidationError("Platform is required");

            var distribution = await _analyticsService.GetVersionDistributionAsync(platform);
            return Success(distribution);
        }

        /// <summary>
        /// Get error events (Admin only)
        /// </summary>
        [HttpGet("errors")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> GetErrors([FromQuery] int pageSize = 50)
        {
            var errors = await _analyticsService.GetErrorEventsAsync(pageSize);
            return Success(errors);
        }
    }
}
