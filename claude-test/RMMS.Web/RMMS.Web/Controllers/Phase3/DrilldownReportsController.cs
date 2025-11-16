using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class DrilldownReportsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IDrilldownReportService _drilldownService;
        private readonly ILogger<DrilldownReportsController> _logger;

        public DrilldownReportsController(
            IDrilldownReportService drilldownService,
            ILogger<DrilldownReportsController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _drilldownService = drilldownService;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                var availableDefinitions = await _drilldownService.GetAvailableReportsAsync();

                // Convert DrilldownReportDefinition to DrilldownReport for view
                var availableReports = availableDefinitions.Select((def, index) => new DrilldownReport
                {
                    Id = index + 1,
                    Name = def.ReportName,
                    Description = $"Category: {def.Category}",
                    Category = def.Category,
                    Hierarchy = def.Hierarchy,
                    IsActive = true,
                    CreatedBy = def.CreatedBy,
                    CreatedDate = def.CreatedDate
                }).ToList();

                return View(availableReports);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading drilldown reports");
                TempData["Error"] = "Error loading reports: " + ex.Message;
                return View(new List<DrilldownReport>());
            }
        }

        [HttpGet]
        public async Task<IActionResult> SalesDrilldown(string filters, int level = 0)
        {
            try
            {
                var filterDict = ParseFilters(filters);
                var result = await _drilldownService.GetSalesDrilldownAsync(filterDict, level);
                return Json(new { success = true, data = result });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in sales drilldown");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> InventoryDrilldown(string filters, int level = 0)
        {
            try
            {
                var filterDict = ParseFilters(filters);
                var result = await _drilldownService.GetInventoryDrilldownAsync(filterDict, level);
                return Json(new { success = true, data = result });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in inventory drilldown");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> ProductionDrilldown(string filters, int level = 0)
        {
            try
            {
                var filterDict = ParseFilters(filters);
                var result = await _drilldownService.GetProductionDrilldownAsync(filterDict, level);
                return Json(new { success = true, data = result });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in production drilldown");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> NavigateUp(string reportType, string filters, int level)
        {
            try
            {
                var filterDict = ParseFilters(filters);
                var result = await _drilldownService.NavigateUpAsync(reportType, filterDict, level);
                return Json(new { success = true, data = result });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error navigating up");
                return Json(new { success = false, message = ex.Message });
            }
        }

        private Dictionary<string, string> ParseFilters(string filters)
        {
            var result = new Dictionary<string, string>();
            if (string.IsNullOrEmpty(filters)) return result;

            var pairs = filters.Split('&');
            foreach (var pair in pairs)
            {
                var parts = pair.Split('=');
                if (parts.Length == 2)
                {
                    result[parts[0]] = parts[1];
                }
            }
            return result;
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new DrilldownReport());
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
        public async Task<IActionResult> Create(DrilldownReport model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            try
            {
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;
                model.CreatedBy = User.Identity?.Name ?? "system";

                await _context.Set<DrilldownReport>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "DrilldownReport created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating DrilldownReport");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
