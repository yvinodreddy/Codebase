using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Interfaces.Production;
using System;
using System.Linq;

namespace RMMS.Web.Controllers
{
    public class YieldAnalysisController : Controller
    {
        private readonly IYieldAnalysisService _yieldAnalysisService;
        private readonly IProductionBatchService _batchService;

        public YieldAnalysisController(
            IYieldAnalysisService yieldAnalysisService,
            IProductionBatchService batchService)
        {
            _yieldAnalysisService = yieldAnalysisService;
            _batchService = batchService;
        }

        // GET: YieldAnalysis
        public IActionResult Index(DateTime? fromDate, DateTime? toDate)
        {
            // Default to last 30 days
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;

            var statistics = _yieldAnalysisService.GetOverallYieldStatistics(fromDate, toDate);
            var comparison = _yieldAnalysisService.GetYieldComparison(fromDate, toDate);
            var summary = _yieldAnalysisService.GetProductionSummary(fromDate, toDate);

            ViewBag.Statistics = statistics;
            ViewBag.Comparison = comparison;
            ViewBag.Summary = summary;

            return View();
        }

        // GET: YieldAnalysis/Trends
        public IActionResult Trends(DateTime? fromDate, DateTime? toDate, string groupBy = "Daily")
        {
            // Default to last 30 days
            var endDate = toDate ?? DateTime.Today;
            var startDate = fromDate ?? endDate.AddDays(-30);

            ViewBag.FromDate = startDate;
            ViewBag.ToDate = endDate;
            ViewBag.GroupBy = groupBy;

            var trends = _yieldAnalysisService.GetYieldTrends(startDate, endDate, groupBy);

            return View(trends);
        }

        // GET: YieldAnalysis/ByVariety
        public IActionResult ByVariety(DateTime? fromDate, DateTime? toDate)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;

            var varietyData = _yieldAnalysisService.GetYieldByPaddyVariety(fromDate, toDate);

            return View(varietyData);
        }

        // GET: YieldAnalysis/ByMachine
        public IActionResult ByMachine(DateTime? fromDate, DateTime? toDate)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;

            var machineData = _yieldAnalysisService.GetYieldByMachine(fromDate, toDate);

            return View(machineData);
        }

        // GET: YieldAnalysis/Variance
        public IActionResult Variance(DateTime? fromDate, DateTime? toDate)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;

            var varianceData = _yieldAnalysisService.GetYieldVarianceAnalysis(fromDate, toDate);

            return View(varianceData);
        }

        // GET: YieldAnalysis/Performance
        public IActionResult Performance(DateTime? fromDate, DateTime? toDate)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;

            var performanceData = _yieldAnalysisService.GetBatchPerformanceDetails(fromDate, toDate);

            return View(performanceData);
        }

        // GET: YieldAnalysis/LowYield
        public IActionResult LowYield(decimal threshold = 60, DateTime? fromDate = null, DateTime? toDate = null)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;
            ViewBag.Threshold = threshold;

            var lowYieldBatches = _yieldAnalysisService.GetLowYieldBatches(threshold, fromDate, toDate);

            return View(lowYieldBatches);
        }

        // GET: YieldAnalysis/HighYield
        public IActionResult HighYield(decimal threshold = 70, DateTime? fromDate = null, DateTime? toDate = null)
        {
            ViewBag.FromDate = fromDate ?? DateTime.Today.AddDays(-30);
            ViewBag.ToDate = toDate ?? DateTime.Today;
            ViewBag.Threshold = threshold;

            var highYieldBatches = _yieldAnalysisService.GetHighYieldBatches(threshold, fromDate, toDate);

            return View(highYieldBatches);
        }

        // API: Get Yield Trend Data for Charts
        [HttpGet]
        public JsonResult GetYieldTrendData(DateTime? fromDate, DateTime? toDate, string groupBy = "Daily")
        {
            var endDate = toDate ?? DateTime.Today;
            var startDate = fromDate ?? endDate.AddDays(-30);

            var trends = _yieldAnalysisService.GetYieldTrends(startDate, endDate, groupBy);

            var chartData = new
            {
                labels = trends.Select(t => t.Period).ToArray(),
                datasets = new[]
                {
                    new
                    {
                        label = "Average Yield %",
                        data = trends.Select(t => t.AverageYield).ToArray(),
                        borderColor = "rgb(75, 192, 192)",
                        backgroundColor = "rgba(75, 192, 192, 0.2)",
                        tension = 0.1
                    },
                    new
                    {
                        label = "Head Rice %",
                        data = trends.Select(t => t.HeadRicePercent).ToArray(),
                        borderColor = "rgb(54, 162, 235)",
                        backgroundColor = "rgba(54, 162, 235, 0.2)",
                        tension = 0.1
                    },
                    new
                    {
                        label = "Broken Rice %",
                        data = trends.Select(t => t.BrokenRicePercent).ToArray(),
                        borderColor = "rgb(255, 206, 86)",
                        backgroundColor = "rgba(255, 206, 86, 0.2)",
                        tension = 0.1
                    }
                }
            };

            return Json(chartData);
        }

        // API: Get Yield by Variety Data for Charts
        [HttpGet]
        public JsonResult GetYieldByVarietyData(DateTime? fromDate, DateTime? toDate)
        {
            var varietyData = _yieldAnalysisService.GetYieldByPaddyVariety(fromDate, toDate);

            var chartData = new
            {
                labels = varietyData.Select(v => v.PaddyVariety).ToArray(),
                datasets = new[]
                {
                    new
                    {
                        label = "Average Yield %",
                        data = varietyData.Select(v => v.AverageYieldPercent).ToArray(),
                        backgroundColor = new[]
                        {
                            "rgba(255, 99, 132, 0.8)",
                            "rgba(54, 162, 235, 0.8)",
                            "rgba(255, 206, 86, 0.8)",
                            "rgba(75, 192, 192, 0.8)",
                            "rgba(153, 102, 255, 0.8)",
                            "rgba(255, 159, 64, 0.8)"
                        }
                    }
                }
            };

            return Json(chartData);
        }

        // API: Get Yield by Machine Data for Charts
        [HttpGet]
        public JsonResult GetYieldByMachineData(DateTime? fromDate, DateTime? toDate)
        {
            var machineData = _yieldAnalysisService.GetYieldByMachine(fromDate, toDate);

            var chartData = new
            {
                labels = machineData.Select(m => m.MachineName).ToArray(),
                datasets = new[]
                {
                    new
                    {
                        label = "Average Yield %",
                        data = machineData.Select(m => m.AverageYieldPercent).ToArray(),
                        backgroundColor = new[]
                        {
                            "rgba(54, 162, 235, 0.8)",
                            "rgba(255, 99, 132, 0.8)",
                            "rgba(75, 192, 192, 0.8)",
                            "rgba(255, 206, 86, 0.8)",
                            "rgba(153, 102, 255, 0.8)"
                        }
                    }
                }
            };

            return Json(chartData);
        }
    }
}
