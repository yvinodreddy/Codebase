using RMMS.Models.Mobile.DTOs;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for tracking and analyzing mobile app analytics
    /// </summary>
    public interface IMobileAnalyticsService
    {
        /// <summary>
        /// Track a single analytics event
        /// </summary>
        Task<bool> TrackEventAsync(int? deviceId, string? userId, AnalyticsEventDto eventDto);

        /// <summary>
        /// Track multiple analytics events in batch
        /// </summary>
        Task<int> TrackBatchEventsAsync(int? deviceId, string? userId, BatchAnalyticsDto batchDto);

        /// <summary>
        /// Get analytics summary for a date range
        /// </summary>
        Task<object> GetAnalyticsSummaryAsync(DateTime startDate, DateTime endDate);

        /// <summary>
        /// Get most popular screens
        /// </summary>
        Task<List<object>> GetPopularScreensAsync(int topN = 10);

        /// <summary>
        /// Get user engagement metrics
        /// </summary>
        Task<object> GetEngagementMetricsAsync(string userId);

        /// <summary>
        /// Get app version distribution
        /// </summary>
        Task<Dictionary<string, int>> GetVersionDistributionAsync(string platform);

        /// <summary>
        /// Get error events
        /// </summary>
        Task<List<object>> GetErrorEventsAsync(int pageSize = 50);
    }
}
