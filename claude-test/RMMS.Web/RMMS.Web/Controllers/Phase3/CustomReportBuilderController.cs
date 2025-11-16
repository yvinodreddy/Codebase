using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using System.Security.Claims;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class CustomReportBuilderController : Controller
    {
        private readonly ICustomReportBuilderService _reportBuilderService;
        private readonly ILogger<CustomReportBuilderController> _logger;

        public CustomReportBuilderController(
            ICustomReportBuilderService reportBuilderService,
            ILogger<CustomReportBuilderController> logger)
        {
            _reportBuilderService = reportBuilderService;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "unknown";
                var reports = await _reportBuilderService.GetUserReportsAsync(userId);
                var dataSources = await _reportBuilderService.GetAvailableDataSourcesAsync();

                ViewBag.DataSources = dataSources;
                return View(reports);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading custom report builder");
                TempData["Error"] = "Error loading report builder: " + ex.Message;
                return View(new List<CustomReportDefinition>());
            }
        }

        [HttpGet]
        public async Task<IActionResult> Create()
        {
            try
            {
                var dataSources = await _reportBuilderService.GetAvailableDataSourcesAsync();
                ViewBag.DataSources = dataSources;
                return View(new CustomReportDefinition());
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create report page");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> Create(CustomReportDefinition report)
        {
            try
            {
                var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "unknown";
                report.CreatedBy = userId;
                report.CreatedDate = DateTime.Now;

                var reportId = await _reportBuilderService.SaveReportDefinitionAsync(report);

                TempData["Success"] = "Report definition saved successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating report");
                TempData["Error"] = "Error creating report: " + ex.Message;
                return View(report);
            }
        }

        [HttpGet]
        public async Task<IActionResult> Execute(int id)
        {
            try
            {
                var report = await _reportBuilderService.GetReportDefinitionAsync(id);
                if (report == null)
                {
                    TempData["Error"] = "Report not found";
                    return RedirectToAction(nameof(Index));
                }

                ViewBag.ReportDefinition = report;
                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading report execution page");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> Execute(int id, Dictionary<string, string> parameters)
        {
            try
            {
                var result = await _reportBuilderService.ExecuteReportAsync(id, parameters);
                return View("Results", result);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing report {ReportId}", id);
                TempData["Error"] = "Error executing report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExecuteCustomSQL(string sql)
        {
            try
            {
                var result = await _reportBuilderService.ExecuteCustomSQLAsync(sql);
                return Json(new { success = true, data = result });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing custom SQL");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var success = await _reportBuilderService.DeleteReportAsync(id);
                if (success)
                {
                    TempData["Success"] = "Report deleted successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to delete report";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting report {ReportId}", id);
                TempData["Error"] = "Error: " + ex.Message;
            }
            return RedirectToAction(nameof(Index));
        }

        [HttpGet]
        public async Task<IActionResult> GetColumns(string dataSource)
        {
            try
            {
                var columns = await _reportBuilderService.GetDataSourceColumnsAsync(dataSource);
                return Json(new { success = true, columns });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = ex.Message });
            }
        }
    }
}
