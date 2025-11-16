using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class DataArchivalController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IDataArchivalService _archivalService;
        private readonly ILogger<DataArchivalController> _logger;

        public DataArchivalController(
            IDataArchivalService archivalService,
            ILogger<DataArchivalController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _archivalService = archivalService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<ArchivalJob>());
        }

        [HttpPost]
        public async Task<IActionResult> ArchiveOldSales(DateTime beforeDate)
        {
            try
            {
                var count = await _archivalService.ArchiveOldSalesAsync(beforeDate);
                TempData["Success"] = $"Archived {count} sales records";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error archiving sales");
                TempData["Error"] = "Error archiving sales: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ArchiveOldBatches(DateTime beforeDate)
        {
            try
            {
                var count = await _archivalService.ArchiveOldBatchesAsync(beforeDate);
                TempData["Success"] = $"Archived {count} production batches";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error archiving batches");
                TempData["Error"] = "Error archiving batches: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> CompressArchive()
        {
            try
            {
                var success = await _archivalService.CompressArchivedDataAsync();
                if (success)
                {
                    TempData["Success"] = "Archived data compressed successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to compress archived data";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error compressing archive");
                TempData["Error"] = "Error compressing archive: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> DeleteArchived(DateTime beforeDate)
        {
            try
            {
                var count = await _archivalService.DeleteArchivedDataAsync(beforeDate);
                TempData["Success"] = $"Deleted {count} archived records";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting archived data");
                TempData["Error"] = "Error deleting archived data: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ArchivalJob());
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
        public async Task<IActionResult> Create(ArchivalJob model)
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

                await _context.Set<ArchivalJob>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ArchivalJob created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ArchivalJob");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
