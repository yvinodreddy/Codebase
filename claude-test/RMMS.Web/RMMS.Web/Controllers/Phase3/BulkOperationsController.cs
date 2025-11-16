using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class BulkOperationsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IBulkOperationsService _bulkService;
        private readonly ILogger<BulkOperationsController> _logger;

        public BulkOperationsController(
            IBulkOperationsService bulkService,
            ILogger<BulkOperationsController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _bulkService = bulkService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<BulkOperation>());
        }

        [HttpPost]
        public async Task<IActionResult> ImportProducts(IFormFile file)
        {
            try
            {
                if (file == null || file.Length == 0)
                {
                    TempData["Error"] = "Please select a file to upload";
                    return RedirectToAction(nameof(Index));
                }

                using var stream = file.OpenReadStream();
                var result = await _bulkService.ImportProductsFromExcelAsync(stream);

                TempData["Success"] = $"Imported {result.SuccessCount} products. Errors: {result.FailedCount}";
                if (result.Errors.Count > 0)
                {
                    ViewBag.Errors = result.Errors;
                }
                return View("ImportResult", result);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error importing products");
                TempData["Error"] = "Error importing products: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ImportCustomers(IFormFile file)
        {
            try
            {
                if (file == null || file.Length == 0)
                {
                    TempData["Error"] = "Please select a file to upload";
                    return RedirectToAction(nameof(Index));
                }

                using var stream = file.OpenReadStream();
                var result = await _bulkService.ImportCustomersFromExcelAsync(stream);

                TempData["Success"] = $"Imported {result.SuccessCount} customers. Errors: {result.FailedCount}";
                return View("ImportResult", result);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error importing customers");
                TempData["Error"] = "Error importing customers: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> ExportProducts()
        {
            try
            {
                var excelBytes = await _bulkService.ExportProductsToExcelAsync();
                return File(excelBytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", $"Products_{DateTime.Now:yyyyMMdd}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting products");
                TempData["Error"] = "Error exporting products: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportSales(BulkExportOptions options)
        {
            try
            {
                var excelBytes = await _bulkService.ExportSalesToExcelAsync(options);
                return File(excelBytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", $"Sales_{DateTime.Now:yyyyMMdd}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting sales");
                TempData["Error"] = "Error exporting sales: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> ExportInventory()
        {
            try
            {
                var excelBytes = await _bulkService.ExportInventoryToExcelAsync();
                return File(excelBytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", $"Inventory_{DateTime.Now:yyyyMMdd}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting inventory");
                TempData["Error"] = "Error exporting inventory: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new BulkOperation());
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
        public async Task<IActionResult> Create(BulkOperation model)
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

                await _context.Set<BulkOperation>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "BulkOperation created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating BulkOperation");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
