using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class InteractiveDashboardsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IRealtimeDashboardService _dashboardService;
        private readonly ILogger<InteractiveDashboardsController> _logger;

        public InteractiveDashboardsController(
            IRealtimeDashboardService dashboardService,
            ILogger<InteractiveDashboardsController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _dashboardService = dashboardService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<DashboardDefinition>());
        }

        [HttpGet]
        public async Task<IActionResult> GetSalesData()
        {
            try
            {
                var data = await _dashboardService.GetSalesDashboardDataAsync();
                return Json(new { success = true, data });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting sales dashboard data");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetProductionData()
        {
            try
            {
                var data = await _dashboardService.GetProductionDashboardDataAsync();
                return Json(new { success = true, data });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting production dashboard data");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetInventoryData()
        {
            try
            {
                var data = await _dashboardService.GetInventoryDashboardDataAsync();
                return Json(new { success = true, data });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting inventory dashboard data");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetFinancialData()
        {
            try
            {
                var data = await _dashboardService.GetFinancialDashboardDataAsync();
                return Json(new { success = true, data });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting financial dashboard data");
                return Json(new { success = false, message = ex.Message });
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new DashboardDefinition());
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
        public async Task<IActionResult> Create(DashboardDefinition model)
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

                await _context.Set<DashboardDefinition>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "DashboardDefinition created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating DashboardDefinition");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
