using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Monitoring;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class RealtimeMonitoringController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<RealtimeMonitoringController> _logger;
        private static readonly DateTime _appStartTime = DateTime.Now;
        private static int _activeConnections = 0;
        private static int _peakConnections = 0;

        public RealtimeMonitoringController(ILogger<RealtimeMonitoringController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Get recent metrics
                var metrics = await _context.Set<RealtimeMetric>()
                    .OrderByDescending(m => m.CreatedDate)
                    .Take(100)
                    .ToListAsync();

                var now = DateTime.Now;
                var last5Minutes = now.AddMinutes(-5);
                var lastHour = now.AddHours(-1);

                // System statistics
                var process = Process.GetCurrentProcess();
                ViewBag.ActiveConnections = _activeConnections;
                ViewBag.PeakConnections = _peakConnections;
                ViewBag.CurrentMemoryMB = Math.Round(process.WorkingSet64 / 1024.0 / 1024.0, 2);
                ViewBag.TotalProcessorTime = Math.Round(process.TotalProcessorTime.TotalSeconds, 2);
                ViewBag.Uptime = FormatUptime(now - _appStartTime);

                // Recent activity
                ViewBag.RecentMetricsCount = metrics.Count(m => m.CreatedDate >= last5Minutes);
                ViewBag.HourlyMetricsCount = metrics.Count(m => m.CreatedDate >= lastHour);
                ViewBag.TotalMetrics = metrics.Count;

                // Performance metrics
                if (metrics.Any())
                {
                    ViewBag.AverageLatency = Math.Round(metrics.Average(m => m.Value), 2);
                    ViewBag.MaxLatency = Math.Round(metrics.Max(m => m.Value), 2);
                    ViewBag.MinLatency = Math.Round(metrics.Min(m => m.Value), 2);
                }
                else
                {
                    ViewBag.AverageLatency = 0;
                    ViewBag.MaxLatency = 0;
                    ViewBag.MinLatency = 0;
                }

                // Health status
                var avgLatency = metrics.Any() ? metrics.Average(m => m.Value) : 0;
                ViewBag.HealthStatus = avgLatency < 100 ? "Healthy" :
                                      avgLatency < 500 ? "Warning" : "Critical";
                ViewBag.HealthStatusClass = ViewBag.HealthStatus == "Healthy" ? "success" :
                                           ViewBag.HealthStatus == "Warning" ? "warning" : "danger";

                // Load level
                var requestsPerMinute = metrics.Count(m => m.CreatedDate >= last5Minutes) / 5.0;
                ViewBag.LoadLevel = requestsPerMinute < 10 ? "Low" :
                                   requestsPerMinute < 50 ? "Medium" : "High";
                ViewBag.RequestsPerMinute = Math.Round(requestsPerMinute, 2);

                // By metric type
                var metricsByType = metrics.GroupBy(m => m.MetricType)
                    .Select(g => new {
                        Type = g.Key,
                        Count = g.Count(),
                        AvgValue = Math.Round(g.Average(m => m.Value), 2)
                    })
                    .OrderByDescending(x => x.Count)
                    .ToList();

                ViewBag.MetricTypes = metricsByType.Count;
                ViewBag.TopMetricType = metricsByType.FirstOrDefault()?.Type ?? "N/A";
                ViewBag.TopMetricTypeCount = metricsByType.FirstOrDefault()?.Count ?? 0;

                return View(metrics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading realtime monitoring");
                TempData["Error"] = "Error loading realtime monitoring: " + ex.Message;
                return View(new List<RealtimeMetric>());
            }
        }

        [HttpGet]
        public IActionResult GetConnectionStats()
        {
            try
            {
                var uptime = DateTime.Now - _appStartTime;

                var stats = new
                {
                    activeConnections = _activeConnections,
                    peakConnections = _peakConnections,
                    uptime = FormatUptime(uptime),
                    uptimeSeconds = (int)uptime.TotalSeconds,
                    status = "Online"
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting connection stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetPerformanceMetrics()
        {
            try
            {
                var process = Process.GetCurrentProcess();
                var metrics = await _context.Set<RealtimeMetric>()
                    .Where(m => m.CreatedDate >= DateTime.Now.AddMinutes(-5))
                    .ToListAsync();

                var data = new
                {
                    memoryUsageMB = Math.Round(process.WorkingSet64 / 1024.0 / 1024.0, 2),
                    cpuTimeSeconds = Math.Round(process.TotalProcessorTime.TotalSeconds, 2),
                    threadCount = process.Threads.Count,
                    handleCount = process.HandleCount,
                    activeMetrics = metrics.Count,
                    averageLatency = metrics.Any() ? Math.Round(metrics.Average(m => m.Value), 2) : 0,
                    requestsPerMinute = metrics.Count / 5.0
                };

                return Json(new { success = true, data });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting performance metrics");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetRealtimeData()
        {
            try
            {
                var last30Seconds = DateTime.Now.AddSeconds(-30);
                var recentMetrics = await _context.Set<RealtimeMetric>()
                    .Where(m => m.CreatedDate >= last30Seconds)
                    .OrderBy(m => m.CreatedDate)
                    .Select(m => new {
                        timestamp = m.CreatedDate.ToString("HH:mm:ss"),
                        value = Math.Round(m.Value, 2),
                        type = m.MetricType
                    })
                    .ToListAsync();

                return Json(new { success = true, data = recentMetrics });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting realtime data");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public IActionResult GetSystemHealth()
        {
            try
            {
                var process = Process.GetCurrentProcess();
                var memoryMB = process.WorkingSet64 / 1024.0 / 1024.0;
                var uptime = DateTime.Now - _appStartTime;

                var health = new
                {
                    status = memoryMB < 500 && uptime.TotalMinutes > 1 ? "Healthy" :
                            memoryMB < 1000 ? "Warning" : "Critical",
                    memory = Math.Round(memoryMB, 2),
                    uptime = FormatUptime(uptime),
                    connections = _activeConnections,
                    timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                };

                return Json(new { success = true, data = health });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting system health");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public IActionResult IncrementConnections()
        {
            _activeConnections++;
            if (_activeConnections > _peakConnections)
                _peakConnections = _activeConnections;
            return Json(new { success = true, active = _activeConnections, peak = _peakConnections });
        }

        [HttpPost]
        public IActionResult DecrementConnections()
        {
            if (_activeConnections > 0)
                _activeConnections--;
            return Json(new { success = true, active = _activeConnections });
        }

        [HttpPost]
        public async Task<IActionResult> RecordMetric(string metricType, double value)
        {
            try
            {
                var metric = new RealtimeMetric
                {
                    MetricType = metricType,
                    Value = value,
                    CreatedDate = DateTime.Now,
                    IsActive = true
                };

                await _context.Set<RealtimeMetric>().AddAsync(metric);
                await _context.SaveChangesAsync();

                return Json(new { success = true });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error recording metric");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> ClearOldMetrics(int minutesToKeep = 60)
        {
            try
            {
                var cutoffDate = DateTime.Now.AddMinutes(-minutesToKeep);
                var oldMetrics = await _context.Set<RealtimeMetric>()
                    .Where(m => m.CreatedDate < cutoffDate)
                    .ToListAsync();

                var count = oldMetrics.Count;
                _context.Set<RealtimeMetric>().RemoveRange(oldMetrics);
                await _context.SaveChangesAsync();

                TempData["Success"] = $"Cleared {count} old metrics";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error clearing old metrics");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        private string FormatUptime(TimeSpan uptime)
        {
            if (uptime.TotalDays >= 1)
                return $"{(int)uptime.TotalDays}d {uptime.Hours}h {uptime.Minutes}m";
            else if (uptime.TotalHours >= 1)
                return $"{(int)uptime.TotalHours}h {uptime.Minutes}m {uptime.Seconds}s";
            else
                return $"{uptime.Minutes}m {uptime.Seconds}s";
        }
    }
}
