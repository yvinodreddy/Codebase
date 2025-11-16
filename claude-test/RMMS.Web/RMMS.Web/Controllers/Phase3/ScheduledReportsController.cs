using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class ScheduledReportsController : Controller
    {
        private readonly IReportSchedulingService _schedulingService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<ScheduledReportsController> _logger;

        public ScheduledReportsController(
            IReportSchedulingService schedulingService,
            ApplicationDbContext context,
            ILogger<ScheduledReportsController> logger)
        {
            _schedulingService = schedulingService;
            _context = context;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                // In a real implementation, you'd retrieve scheduled jobs from Hangfire
                // For now, return an empty list to prevent null reference errors
                var emptyList = new List<ScheduledReport>();
                return View(emptyList);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading scheduled reports");
                TempData["Error"] = "Error loading scheduled reports: " + ex.Message;
                return View(new List<ScheduledReport>());
            }
        }

        [HttpPost]
        public async Task<IActionResult> ScheduleReport(string reportName, string cronExpression, string recipients)
        {
            try
            {
                var jobId = await _schedulingService.ScheduleRecurringReportAsync(reportName, cronExpression, recipients);
                TempData["Success"] = $"Report '{reportName}' scheduled successfully. Job ID: {jobId}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error scheduling report");
                TempData["Error"] = "Error scheduling report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExecuteNow(string reportName, string recipients)
        {
            try
            {
                await _schedulingService.ExecuteScheduledReportAsync(reportName, recipients);
                TempData["Success"] = $"Report '{reportName}' executed successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing report");
                TempData["Error"] = "Error executing report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> CancelSchedule(string jobId)
        {
            try
            {
                var success = await _schedulingService.CancelScheduledReportAsync(jobId);
                if (success)
                {
                    TempData["Success"] = "Scheduled report cancelled successfully";
                }
                else
                {
                    TempData["Error"] = "Failed to cancel scheduled report";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cancelling scheduled report");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ScheduledReport());
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
        public async Task<IActionResult> Create(ScheduledReport model)
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

                await _context.Set<ScheduledReport>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ScheduledReport created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ScheduledReport");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
