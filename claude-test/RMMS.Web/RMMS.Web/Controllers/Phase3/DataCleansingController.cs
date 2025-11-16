using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class DataCleansingController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IDataCleansingService _cleansingService;
        private readonly ILogger<DataCleansingController> _logger;

        public DataCleansingController(
            IDataCleansingService cleansingService,
            ILogger<DataCleansingController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _cleansingService = cleansingService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<CleansingJob>());
        }

        [HttpGet]
        public async Task<IActionResult> FindDuplicates(string entityType)
        {
            try
            {
                var duplicates = await _cleansingService.FindDuplicateRecordsAsync(entityType);
                return Json(new { success = true, data = duplicates });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error finding duplicates");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> MergeDuplicates(string entityType, List<int> duplicateIds, int masterRecordId)
        {
            try
            {
                var success = await _cleansingService.MergeDuplicatesAsync(entityType, duplicateIds, masterRecordId);
                if (success)
                {
                    TempData["Success"] = $"Successfully merged {duplicateIds.Count} records";
                }
                else
                {
                    TempData["Error"] = "Failed to merge records";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error merging duplicates");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> StandardizeData(string entityType, string field)
        {
            try
            {
                var count = await _cleansingService.StandardizeDataAsync(entityType, field);
                TempData["Success"] = $"Standardized {count} records in {field}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error standardizing data");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> CleanInvalidData(string entityType)
        {
            try
            {
                var count = await _cleansingService.CleanInvalidDataAsync(entityType);
                TempData["Success"] = $"Cleaned {count} invalid records";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cleaning data");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new CleansingJob());
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
        public async Task<IActionResult> Create(CleansingJob model)
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

                await _context.Set<CleansingJob>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "CleansingJob created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating CleansingJob");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
