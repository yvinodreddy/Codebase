using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using System.Security.Claims;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class AuditTrailController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IAuditTrailService _auditService;
        private readonly ILogger<AuditTrailController> _logger;

        public AuditTrailController(
            IAuditTrailService auditService,
            ILogger<AuditTrailController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _auditService = auditService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<AuditLog>());
        }

        [HttpGet]
        public async Task<IActionResult> GetEntityHistory(string entityType, int entityId)
        {
            try
            {
                var history = await _auditService.GetEntityAuditHistoryAsync(entityType, entityId);
                return Json(new { success = true, data = history });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting entity history");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetUserActivity(DateTime from, DateTime to)
        {
            try
            {
                var userId = User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "unknown";
                var activity = await _auditService.GetUserActivityAsync(userId, from, to);
                return Json(new { success = true, data = activity });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting user activity");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> EnableAuditing(string entityType)
        {
            try
            {
                var success = await _auditService.EnableAuditingAsync(entityType);
                if (success)
                {
                    TempData["Success"] = $"Auditing enabled for {entityType}";
                }
                else
                {
                    TempData["Error"] = $"Failed to enable auditing for {entityType}";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error enabling auditing");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new AuditLog());
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
        public async Task<IActionResult> Create(AuditLog model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            try
            {
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;

                await _context.Set<AuditLog>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "AuditLog created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating AuditLog");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
