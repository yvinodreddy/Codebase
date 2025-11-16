using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.DataManagement;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class DataValidationController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IDataValidationService _validationService;
        private readonly ILogger<DataValidationController> _logger;

        public DataValidationController(
            IDataValidationService validationService,
            ILogger<DataValidationController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _validationService = validationService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<ValidationRule>());
        }

        [HttpPost]
        public async Task<IActionResult> ValidateEntity(string entityType, object entity)
        {
            try
            {
                var errors = await _validationService.ValidateEntityAsync(entityType, entity);
                return Json(new { success = errors.Count == 0, errors });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating entity");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> AddValidationRule(string entityType, string ruleName, string ruleExpression)
        {
            try
            {
                var success = await _validationService.AddValidationRuleAsync(entityType, ruleName, ruleExpression);
                if (success)
                {
                    TempData["Success"] = $"Validation rule '{ruleName}' added successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to add validation rule";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error adding validation rule");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetValidationRules(string entityType)
        {
            try
            {
                var rules = await _validationService.GetValidationRulesAsync(entityType);
                return Json(new { success = true, data = rules });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting validation rules");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExecuteValidation(int ruleId, object entity)
        {
            try
            {
                var success = await _validationService.ExecuteValidationAsync(ruleId, entity);
                return Json(new { success, message = success ? "Validation passed" : "Validation failed" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing validation");
                return Json(new { success = false, message = ex.Message });
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ValidationRule());
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
        public async Task<IActionResult> Create(ValidationRule model)
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

                await _context.Set<ValidationRule>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ValidationRule created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ValidationRule");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
