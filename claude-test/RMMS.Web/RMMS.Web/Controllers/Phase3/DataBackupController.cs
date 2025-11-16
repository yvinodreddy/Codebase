using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class DataBackupController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IDataBackupService _backupService;
        private readonly ILogger<DataBackupController> _logger;

        public DataBackupController(
            IDataBackupService backupService,
            ILogger<DataBackupController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _backupService = backupService;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                var backupFiles = await _backupService.GetAvailableBackupsAsync();

                // Convert backup file names to BackupJob objects
                var backups = backupFiles.Select((file, index) => new BackupJob
                {
                    Id = index + 1,
                    Name = System.IO.Path.GetFileNameWithoutExtension(file),
                    BackupPath = file,
                    Status = "Completed",
                    CreatedDate = DateTime.Now,
                    CreatedBy = "system"
                }).ToList();

                return View(backups);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading backups");
                TempData["Error"] = "Error loading backups: " + ex.Message;
                return View(new List<BackupJob>());
            }
        }

        [HttpPost]
        public async Task<IActionResult> CreateBackup(string backupName)
        {
            try
            {
                var success = await _backupService.CreateDatabaseBackupAsync(backupName);
                if (success)
                {
                    TempData["Success"] = $"Backup '{backupName}' created successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to create backup";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating backup");
                TempData["Error"] = "Error creating backup: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> RestoreBackup(string backupPath)
        {
            try
            {
                var success = await _backupService.RestoreDatabaseBackupAsync(backupPath);
                if (success)
                {
                    TempData["Success"] = "Database restored successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to restore database";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error restoring backup");
                TempData["Error"] = "Error restoring backup: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ScheduleAutomaticBackup(string schedule)
        {
            try
            {
                var success = await _backupService.ScheduleAutomaticBackupAsync(schedule);
                if (success)
                {
                    TempData["Success"] = $"Automatic backup scheduled: {schedule}";
                }
                else
                {
                    TempData["Error"] = "Failed to schedule automatic backup";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error scheduling backup");
                TempData["Error"] = "Error scheduling backup: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new BackupJob());
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
        public async Task<IActionResult> Create(BackupJob model)
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

                await _context.Set<BackupJob>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "BackupJob created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating BackupJob");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
