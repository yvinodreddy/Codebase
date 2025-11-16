using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class VersionControlController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IVersionControlService _versionService;
        private readonly ILogger<VersionControlController> _logger;

        public VersionControlController(
            IVersionControlService versionService,
            ILogger<VersionControlController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _versionService = versionService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<DataVersion>());
        }

        [HttpPost]
        public async Task<IActionResult> CreateSnapshot(string entityType, int entityId, object currentState)
        {
            try
            {
                var versionId = await _versionService.CreateSnapshotAsync(entityType, entityId, currentState);
                TempData["Success"] = $"Snapshot created successfully. Version ID: {versionId}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating snapshot");
                TempData["Error"] = "Error creating snapshot: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> Rollback(string entityType, int entityId, int versionId)
        {
            try
            {
                var success = await _versionService.RollbackToVersionAsync(entityType, entityId, versionId);
                if (success)
                {
                    TempData["Success"] = "Rollback completed successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to rollback";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error rolling back");
                TempData["Error"] = "Error rolling back: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetVersionHistory(string entityType, int entityId)
        {
            try
            {
                var history = await _versionService.GetVersionHistoryAsync(entityType, entityId);
                return Json(new { success = true, data = history });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting version history");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> CompareVersions(int version1Id, int version2Id)
        {
            try
            {
                var comparison = await _versionService.CompareVersionsAsync(version1Id, version2Id);
                return Json(new { success = true, data = comparison });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error comparing versions");
                return Json(new { success = false, message = ex.Message });
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new DataVersion());
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
        public async Task<IActionResult> Create(DataVersion model)
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

                await _context.Set<DataVersion>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "DataVersion created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating DataVersion");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
