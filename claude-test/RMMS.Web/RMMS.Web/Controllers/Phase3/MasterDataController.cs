using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class MasterDataController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IMasterDataService _masterDataService;
        private readonly ILogger<MasterDataController> _logger;

        public MasterDataController(
            IMasterDataService masterDataService,
            ILogger<MasterDataController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _masterDataService = masterDataService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<MasterDataEntity>());
        }

        [HttpGet]
        public async Task<IActionResult> GetGoldenRecord(string entityType, int entityId)
        {
            try
            {
                var goldenRecord = await _masterDataService.GetGoldenRecordAsync(entityType, entityId);
                return Json(new { success = true, data = goldenRecord });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting golden record");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> PromoteToGoldenRecord(string entityType, int entityId)
        {
            try
            {
                var success = await _masterDataService.PromoteToGoldenRecordAsync(entityType, entityId);
                if (success)
                {
                    TempData["Success"] = "Record promoted to golden record successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to promote to golden record";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error promoting to golden record");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetDataQualityScores(string entityType)
        {
            try
            {
                var scores = await _masterDataService.GetDataQualityScoresAsync(entityType);
                return Json(new { success = true, data = scores });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting data quality scores");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> SyncMasterData(string entityType)
        {
            try
            {
                var success = await _masterDataService.SyncMasterDataAsync(entityType);
                if (success)
                {
                    TempData["Success"] = $"Master data synchronized for {entityType}";
                }
                else
                {
                    TempData["Error"] = $"Failed to sync master data for {entityType}";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error syncing master data");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new MasterDataEntity());
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
        public async Task<IActionResult> Create(MasterDataEntity model)
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

                await _context.Set<MasterDataEntity>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "MasterDataEntity created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating MasterDataEntity");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
