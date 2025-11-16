using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class ComparisonReportsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IComparisonReportService _comparisonService;
        private readonly ILogger<ComparisonReportsController> _logger;

        public ComparisonReportsController(
            IComparisonReportService comparisonService,
            ILogger<ComparisonReportsController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _comparisonService = comparisonService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<ComparisonReport>());
        }

        [HttpPost]
        public async Task<IActionResult> GenerateMonthOverMonth(DateTime currentMonth, string category)
        {
            try
            {
                var report = await _comparisonService.GenerateMonthOverMonthReportAsync(currentMonth, category);
                return View("ComparisonResult", report);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating month-over-month report");
                TempData["Error"] = "Error generating report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> GenerateYearOverYear(int currentYear, string category)
        {
            try
            {
                var report = await _comparisonService.GenerateYearOverYearReportAsync(currentYear, category);
                return View("ComparisonResult", report);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating year-over-year report");
                TempData["Error"] = "Error generating report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> GenerateQuarterOverQuarter(int currentYear, int currentQuarter, string category)
        {
            try
            {
                var report = await _comparisonService.GenerateQuarterOverQuarterReportAsync(currentYear, currentQuarter, category);
                return View("ComparisonResult", report);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating quarter-over-quarter report");
                TempData["Error"] = "Error generating report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> GenerateCustomComparison(ComparisonReportOptions options)
        {
            try
            {
                var report = await _comparisonService.GenerateCustomComparisonReportAsync(options);
                return View("ComparisonResult", report);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating custom comparison report");
                TempData["Error"] = "Error generating report: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportToExcel(ComparisonReport report)
        {
            try
            {
                var result = await _comparisonService.ExportComparisonToExcelAsync(report);
                return File(result.FileData, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", result.FileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting to Excel");
                TempData["Error"] = "Error exporting: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportToPdf(ComparisonReport report)
        {
            try
            {
                var pdfBytes = await _comparisonService.ExportComparisonToPdfAsync(report);
                return File(pdfBytes, "application/pdf", $"ComparisonReport_{DateTime.Now:yyyyMMdd}.pdf");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting to PDF");
                TempData["Error"] = "Error exporting: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ComparisonReport());
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
        public async Task<IActionResult> Create(ComparisonReport model)
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

                await _context.Set<ComparisonReport>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ComparisonReport created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ComparisonReport");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
