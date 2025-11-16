using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using RMMS.Models.API;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class ApiAnalyticsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<ApiAnalyticsController> _logger;

        public ApiAnalyticsController(
            ApplicationDbContext context,
            ILogger<ApiAnalyticsController> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Query API analytics data
                var analytics = await _context.Set<ApiAnalytic>()
                    .OrderByDescending(a => a.CreatedDate)
                    .Take(1000) // Limit to recent 1000 requests
                    .ToListAsync();

                var now = DateTime.Now;
                var today = DateTime.Today;
                var thisWeek = today.AddDays(-7);
                var thisMonth = today.AddMonths(-1);
                var thisHour = now.AddHours(-1);

                // Overall statistics
                ViewBag.TotalRequests = analytics.Count;
                ViewBag.TotalToday = analytics.Count(a => a.CreatedDate.Date == today);
                ViewBag.TotalThisWeek = analytics.Count(a => a.CreatedDate >= thisWeek);
                ViewBag.TotalThisMonth = analytics.Count(a => a.CreatedDate >= thisMonth);
                ViewBag.TotalThisHour = analytics.Count(a => a.CreatedDate >= thisHour);

                // Success vs Error statistics
                var successCount = analytics.Count(a => a.StatusCode >= 200 && a.StatusCode < 300);
                var errorCount = analytics.Count(a => a.StatusCode >= 400);
                var totalCount = analytics.Count;

                ViewBag.SuccessCount = successCount;
                ViewBag.ErrorCount = errorCount;
                ViewBag.SuccessRate = totalCount > 0
                    ? Math.Round((successCount / (double)totalCount) * 100, 2)
                    : 0;
                ViewBag.ErrorRate = totalCount > 0
                    ? Math.Round((errorCount / (double)totalCount) * 100, 2)
                    : 0;

                // Response time statistics
                if (analytics.Any())
                {
                    ViewBag.AverageResponseTime = Math.Round(analytics.Average(a => a.ResponseTime), 2);
                    ViewBag.MinResponseTime = analytics.Min(a => a.ResponseTime);
                    ViewBag.MaxResponseTime = analytics.Max(a => a.ResponseTime);
                    ViewBag.MedianResponseTime = CalculateMedian(analytics.Select(a => (double)a.ResponseTime).ToList());
                }
                else
                {
                    ViewBag.AverageResponseTime = 0;
                    ViewBag.MinResponseTime = 0;
                    ViewBag.MaxResponseTime = 0;
                    ViewBag.MedianResponseTime = 0;
                }

                // Most active endpoint
                var topEndpoint = analytics.GroupBy(a => a.Endpoint)
                    .OrderByDescending(g => g.Count())
                    .FirstOrDefault();

                ViewBag.TopEndpoint = topEndpoint?.Key ?? "N/A";
                ViewBag.TopEndpointRequests = topEndpoint?.Count() ?? 0;

                // Slowest endpoint
                var slowestEndpoint = analytics.GroupBy(a => a.Endpoint)
                    .Select(g => new {
                        Endpoint = g.Key,
                        AvgTime = g.Average(a => a.ResponseTime)
                    })
                    .OrderByDescending(x => x.AvgTime)
                    .FirstOrDefault();

                ViewBag.SlowestEndpoint = slowestEndpoint?.Endpoint ?? "N/A";
                ViewBag.SlowestEndpointTime = slowestEndpoint != null
                    ? Math.Round(slowestEndpoint.AvgTime, 2)
                    : 0;

                // Most common error
                var topError = analytics.Where(a => a.StatusCode >= 400)
                    .GroupBy(a => a.StatusCode)
                    .OrderByDescending(g => g.Count())
                    .FirstOrDefault();

                ViewBag.TopErrorCode = topError?.Key ?? 0;
                ViewBag.TopErrorCount = topError?.Count() ?? 0;

                // Hourly request distribution
                var hourlyStats = analytics.Where(a => a.CreatedDate.Date == today)
                    .GroupBy(a => a.CreatedDate.Hour)
                    .Select(g => new {
                        Hour = g.Key,
                        Count = g.Count()
                    })
                    .OrderByDescending(x => x.Count)
                    .ToList();

                ViewBag.PeakHour = hourlyStats.FirstOrDefault()?.Hour ?? 0;
                ViewBag.PeakHourRequests = hourlyStats.FirstOrDefault()?.Count ?? 0;

                // Top consumers by IP
                var topConsumers = analytics.GroupBy(a => a.IpAddress)
                    .Select(g => new {
                        IP = g.Key,
                        Count = g.Count()
                    })
                    .OrderByDescending(x => x.Count)
                    .Take(5)
                    .ToList();

                ViewBag.TopConsumerIP = topConsumers.FirstOrDefault()?.IP ?? "N/A";
                ViewBag.TopConsumerRequests = topConsumers.FirstOrDefault()?.Count ?? 0;

                // Performance trends (comparing today vs yesterday)
                var yesterday = today.AddDays(-1);
                var yesterdayRequests = analytics.Count(a => a.CreatedDate.Date == yesterday);
                var todayRequests = analytics.Count(a => a.CreatedDate.Date == today);

                ViewBag.RequestTrend = yesterdayRequests > 0
                    ? Math.Round(((todayRequests - yesterdayRequests) / (double)yesterdayRequests) * 100, 1)
                    : 0;
                ViewBag.TrendDirection = todayRequests > yesterdayRequests ? "up" : "down";

                return View(analytics.Take(100).ToList()); // Show recent 100 in table
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading API analytics");
                TempData["Error"] = "Error loading API analytics: " + ex.Message;
                return View(new List<ApiAnalytic>());
            }
        }

        private double CalculateMedian(List<double> values)
        {
            if (!values.Any()) return 0;

            var sorted = values.OrderBy(x => x).ToList();
            int count = sorted.Count;

            if (count % 2 == 0)
            {
                return (sorted[count / 2 - 1] + sorted[count / 2]) / 2.0;
            }
            else
            {
                return sorted[count / 2];
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetUsageStats(DateTime? from, DateTime? to)
        {
            try
            {
                var fromDate = from ?? DateTime.Today.AddDays(-30);
                var toDate = to ?? DateTime.Now;

                var analytics = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate >= fromDate && a.CreatedDate <= toDate)
                    .ToListAsync();

                var successCount = analytics.Count(a => a.StatusCode >= 200 && a.StatusCode < 300);
                var errorCount = analytics.Count(a => a.StatusCode >= 400);

                var topEndpoints = analytics.GroupBy(a => a.Endpoint)
                    .Select(g => new {
                        endpoint = g.Key,
                        requestCount = g.Count(),
                        avgResponseTime = Math.Round(g.Average(a => a.ResponseTime), 2),
                        successRate = Math.Round((g.Count(a => a.StatusCode >= 200 && a.StatusCode < 300) / (double)g.Count()) * 100, 2)
                    })
                    .OrderByDescending(x => x.requestCount)
                    .Take(10)
                    .ToList();

                var recentErrors = analytics.Where(a => a.StatusCode >= 400)
                    .OrderByDescending(a => a.CreatedDate)
                    .Take(20)
                    .Select(a => new {
                        endpoint = a.Endpoint,
                        statusCode = a.StatusCode,
                        errorMessage = a.ErrorMessage ?? "No error message",
                        timestamp = a.CreatedDate.ToString("yyyy-MM-dd HH:mm:ss"),
                        ipAddress = a.IpAddress
                    })
                    .ToList();

                var stats = new
                {
                    totalRequests = analytics.Count,
                    successfulRequests = successCount,
                    failedRequests = errorCount,
                    successRate = analytics.Any()
                        ? Math.Round((successCount / (double)analytics.Count) * 100, 2)
                        : 0,
                    averageResponseTime = analytics.Any()
                        ? Math.Round(analytics.Average(a => a.ResponseTime), 2)
                        : 0,
                    topEndpoints = topEndpoints,
                    recentErrors = recentErrors
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting usage stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetEndpointStats()
        {
            try
            {
                var analytics = await _context.Set<ApiAnalytic>().ToListAsync();

                var endpointStats = analytics.GroupBy(a => a.Endpoint)
                    .Select(g => new {
                        endpoint = g.Key,
                        totalRequests = g.Count(),
                        avgResponseTime = Math.Round(g.Average(a => a.ResponseTime), 2),
                        minResponseTime = g.Min(a => a.ResponseTime),
                        maxResponseTime = g.Max(a => a.ResponseTime),
                        successCount = g.Count(a => a.StatusCode >= 200 && a.StatusCode < 300),
                        errorCount = g.Count(a => a.StatusCode >= 400),
                        successRate = Math.Round((g.Count(a => a.StatusCode >= 200 && a.StatusCode < 300) / (double)g.Count()) * 100, 2),
                        lastAccessed = g.Max(a => a.CreatedDate).ToString("yyyy-MM-dd HH:mm:ss")
                    })
                    .OrderByDescending(x => x.totalRequests)
                    .ToList();

                return Json(new { success = true, data = endpointStats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting endpoint stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetHourlyStats()
        {
            try
            {
                var today = DateTime.Today;
                var analytics = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate.Date == today)
                    .ToListAsync();

                var hourlyStats = Enumerable.Range(0, 24)
                    .Select(hour => {
                        var hourData = analytics.Where(a => a.CreatedDate.Hour == hour).ToList();
                        return new {
                            hour = hour,
                            label = $"{hour:D2}:00",
                            requests = hourData.Count,
                            errors = hourData.Count(a => a.StatusCode >= 400),
                            avgResponseTime = hourData.Any()
                                ? Math.Round(hourData.Average(a => a.ResponseTime), 2)
                                : 0
                        };
                    })
                    .ToList();

                return Json(new { success = true, data = hourlyStats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting hourly stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetTopConsumers()
        {
            try
            {
                var analytics = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate >= DateTime.Today.AddDays(-7))
                    .ToListAsync();

                var topConsumers = analytics.GroupBy(a => a.IpAddress)
                    .Select(g => new {
                        ipAddress = g.Key,
                        requestCount = g.Count(),
                        successRate = Math.Round((g.Count(a => a.StatusCode >= 200 && a.StatusCode < 300) / (double)g.Count()) * 100, 2),
                        avgResponseTime = Math.Round(g.Average(a => a.ResponseTime), 2),
                        lastRequest = g.Max(a => a.CreatedDate).ToString("yyyy-MM-dd HH:mm:ss")
                    })
                    .OrderByDescending(x => x.requestCount)
                    .Take(10)
                    .ToList();

                return Json(new { success = true, data = topConsumers });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting top consumers");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetStatusCodeDistribution()
        {
            try
            {
                var analytics = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate >= DateTime.Today.AddDays(-7))
                    .ToListAsync();

                var distribution = analytics.GroupBy(a => a.StatusCode)
                    .Select(g => new {
                        statusCode = g.Key,
                        count = g.Count(),
                        percentage = Math.Round((g.Count() / (double)analytics.Count) * 100, 2)
                    })
                    .OrderByDescending(x => x.count)
                    .ToList();

                return Json(new { success = true, data = distribution });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting status code distribution");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetPerformanceTrends()
        {
            try
            {
                var last30Days = DateTime.Today.AddDays(-30);
                var analytics = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate >= last30Days)
                    .ToListAsync();

                var dailyTrends = Enumerable.Range(0, 30)
                    .Select(daysAgo => {
                        var date = DateTime.Today.AddDays(-daysAgo);
                        var dayData = analytics.Where(a => a.CreatedDate.Date == date).ToList();
                        return new {
                            date = date.ToString("MM/dd"),
                            requests = dayData.Count,
                            avgResponseTime = dayData.Any()
                                ? Math.Round(dayData.Average(a => a.ResponseTime), 2)
                                : 0,
                            errorCount = dayData.Count(a => a.StatusCode >= 400)
                        };
                    })
                    .OrderBy(x => x.date)
                    .ToList();

                return Json(new { success = true, data = dailyTrends });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting performance trends");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> ClearOldRecords(int daysToKeep = 90)
        {
            try
            {
                var cutoffDate = DateTime.Now.AddDays(-daysToKeep);
                var oldRecords = await _context.Set<ApiAnalytic>()
                    .Where(a => a.CreatedDate < cutoffDate)
                    .ToListAsync();

                var count = oldRecords.Count;
                _context.Set<ApiAnalytic>().RemoveRange(oldRecords);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Cleared {count} old API analytics records older than {daysToKeep} days");
                TempData["Success"] = $"Successfully cleared {count} old records";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error clearing old records");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ApiAnalytic());
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create page");
                TempData["Error"] = $"Error loading create page: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(ApiAnalytic model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            try
            {
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;

                await _context.Set<ApiAnalytic>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ApiAnalytic created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ApiAnalytic");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
