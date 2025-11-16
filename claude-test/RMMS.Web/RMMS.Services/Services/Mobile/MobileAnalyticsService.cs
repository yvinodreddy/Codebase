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
    public class MobileAnalyticsService : IMobileAnalyticsService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MobileAnalyticsService> _logger;

        public MobileAnalyticsService(
            ApplicationDbContext context,
            ILogger<MobileAnalyticsService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<bool> TrackEventAsync(int? deviceId, string? userId, AnalyticsEventDto eventDto)
        {
            try
            {
                var analyticsEvent = new MobileAnalyticsEvent
                {
                    DeviceId = deviceId,
                    UserId = userId,
                    Category = eventDto.Category,
                    Action = eventDto.Action,
                    Label = eventDto.Label,
                    Value = eventDto.Value,
                    Screen = eventDto.Screen,
                    SessionId = eventDto.SessionId,
                    Properties = eventDto.Properties != null ? JsonSerializer.Serialize(eventDto.Properties) : null,
                    ClientTimestamp = eventDto.ClientTimestamp,
                    ServerTimestamp = DateTime.UtcNow,
                    Platform = await GetDevicePlatformAsync(deviceId),
                    AppVersion = eventDto.AppVersion
                };

                _context.MobileAnalyticsEvents.Add(analyticsEvent);
                await _context.SaveChangesAsync();

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error tracking analytics event");
                return false;
            }
        }

        public async Task<int> TrackBatchEventsAsync(int? deviceId, string? userId, BatchAnalyticsDto batchDto)
        {
            try
            {
                var platform = await GetDevicePlatformAsync(deviceId);
                var events = new List<MobileAnalyticsEvent>();

                foreach (var eventDto in batchDto.Events)
                {
                    events.Add(new MobileAnalyticsEvent
                    {
                        DeviceId = deviceId,
                        UserId = userId,
                        Category = eventDto.Category,
                        Action = eventDto.Action,
                        Label = eventDto.Label,
                        Value = eventDto.Value,
                        Screen = eventDto.Screen,
                        SessionId = eventDto.SessionId,
                        Properties = eventDto.Properties != null ? JsonSerializer.Serialize(eventDto.Properties) : null,
                        ClientTimestamp = eventDto.ClientTimestamp,
                        ServerTimestamp = DateTime.UtcNow,
                        Platform = platform,
                        AppVersion = eventDto.AppVersion
                    });
                }

                _context.MobileAnalyticsEvents.AddRange(events);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Tracked {events.Count} analytics events in batch");
                return events.Count;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error tracking batch analytics events");
                return 0;
            }
        }

        public async Task<object> GetAnalyticsSummaryAsync(DateTime startDate, DateTime endDate)
        {
            try
            {
                var events = await _context.MobileAnalyticsEvents
                    .Where(e => e.ServerTimestamp >= startDate && e.ServerTimestamp <= endDate)
                    .ToListAsync();

                var summary = new
                {
                    TotalEvents = events.Count,
                    UniqueUsers = events.Where(e => e.UserId != null).Select(e => e.UserId).Distinct().Count(),
                    UniqueDevices = events.Where(e => e.DeviceId != null).Select(e => e.DeviceId).Distinct().Count(),
                    UniqueSessions = events.Where(e => e.SessionId != null).Select(e => e.SessionId).Distinct().Count(),
                    EventsByCategory = events.GroupBy(e => e.Category)
                        .Select(g => new { Category = g.Key, Count = g.Count() })
                        .OrderByDescending(x => x.Count)
                        .ToList(),
                    EventsByPlatform = events.GroupBy(e => e.Platform)
                        .Select(g => new { Platform = g.Key, Count = g.Count() })
                        .ToList(),
                    TopScreens = events.Where(e => e.Screen != null)
                        .GroupBy(e => e.Screen)
                        .Select(g => new { Screen = g.Key, Count = g.Count() })
                        .OrderByDescending(x => x.Count)
                        .Take(10)
                        .ToList(),
                    ErrorCount = events.Count(e => e.Category == "error"),
                    DateRange = new { Start = startDate, End = endDate }
                };

                return summary;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting analytics summary");
                throw;
            }
        }

        public async Task<List<object>> GetPopularScreensAsync(int topN = 10)
        {
            try
            {
                var popularScreens = await _context.MobileAnalyticsEvents
                    .Where(e => e.Screen != null && e.Action == "screen_view")
                    .GroupBy(e => e.Screen)
                    .Select(g => new
                    {
                        Screen = g.Key,
                        ViewCount = g.Count(),
                        UniqueUsers = g.Where(e => e.UserId != null).Select(e => e.UserId).Distinct().Count(),
                        AvgTimeSpent = g.Where(e => e.Value.HasValue).Average(e => e.Value) ?? 0
                    })
                    .OrderByDescending(x => x.ViewCount)
                    .Take(topN)
                    .ToListAsync<object>();

                return popularScreens;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting popular screens");
                throw;
            }
        }

        public async Task<object> GetEngagementMetricsAsync(string userId)
        {
            try
            {
                var events = await _context.MobileAnalyticsEvents
                    .Where(e => e.UserId == userId)
                    .ToListAsync();

                var sessions = events.Where(e => e.SessionId != null)
                    .GroupBy(e => e.SessionId)
                    .ToList();

                var metrics = new
                {
                    TotalEvents = events.Count,
                    TotalSessions = sessions.Count,
                    AvgEventsPerSession = sessions.Any() ? events.Count / (double)sessions.Count : 0,
                    ScreensVisited = events.Where(e => e.Screen != null).Select(e => e.Screen).Distinct().Count(),
                    LastActiveDate = events.Max(e => e.ServerTimestamp),
                    FirstActiveDate = events.Min(e => e.ServerTimestamp),
                    FavoriteScreens = events.Where(e => e.Screen != null && e.Action == "screen_view")
                        .GroupBy(e => e.Screen)
                        .Select(g => new { Screen = g.Key, Count = g.Count() })
                        .OrderByDescending(x => x.Count)
                        .Take(5)
                        .ToList(),
                    MostUsedFeatures = events.Where(e => e.Action == "button_click" || e.Action == "feature_use")
                        .GroupBy(e => e.Label)
                        .Select(g => new { Feature = g.Key, Count = g.Count() })
                        .OrderByDescending(x => x.Count)
                        .Take(5)
                        .ToList()
                };

                return metrics;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting engagement metrics for user {userId}");
                throw;
            }
        }

        public async Task<Dictionary<string, int>> GetVersionDistributionAsync(string platform)
        {
            try
            {
                var distribution = await _context.MobileAnalyticsEvents
                    .Where(e => e.Platform == platform && e.AppVersion != null)
                    .GroupBy(e => e.AppVersion)
                    .Select(g => new { Version = g.Key ?? "Unknown", Count = g.Count() })
                    .OrderByDescending(x => x.Count)
                    .ToDictionaryAsync(x => x.Version, x => x.Count);

                return distribution;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting version distribution for {platform}");
                throw;
            }
        }

        public async Task<List<object>> GetErrorEventsAsync(int pageSize = 50)
        {
            try
            {
                var errorEvents = await _context.MobileAnalyticsEvents
                    .Where(e => e.Category == "error")
                    .OrderByDescending(e => e.ServerTimestamp)
                    .Take(pageSize)
                    .ToListAsync();

                return errorEvents.Select(e => new
                {
                    e.Id,
                    e.UserId,
                    e.DeviceId,
                    e.Action,
                    e.Label,
                    e.Screen,
                    e.Platform,
                    e.AppVersion,
                    e.ServerTimestamp,
                    Properties = e.Properties != null ? JsonSerializer.Deserialize<Dictionary<string, object>>(e.Properties) : null
                } as object).ToList();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting error events");
                throw;
            }
        }

        private async Task<string?> GetDevicePlatformAsync(int? deviceId)
        {
            if (!deviceId.HasValue) return null;

            try
            {
                var device = await _context.MobileDevices.FindAsync(deviceId.Value);
                return device?.Platform;
            }
            catch
            {
                return null;
            }
        }
    }
}
