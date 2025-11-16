using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Reporting;
using RMMS.Models.Reporting;
using System.Data;
using RMMS.Models.DataManagement;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers.Phase3
{
    [Authorize]
    public class ExportCenterController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IExcelExportService _excelService;
        private readonly IPdfExportService _pdfService;
        private readonly ILogger<ExportCenterController> _logger;

        public ExportCenterController(
            IExcelExportService excelService,
            IPdfExportService pdfService,
            ILogger<ExportCenterController> logger,
            ApplicationDbContext context)
        {
            _context = context;
            _excelService = excelService;
            _pdfService = pdfService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new List<ExportJob>());
        }

        [HttpPost]
        public async Task<IActionResult> ExportToExcel(DataTable data, string sheetName)
        {
            try
            {
                var result = await _excelService.ExportToExcelAsync(data, sheetName);
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
        public async Task<IActionResult> ExportToExcelWithFormatting(DataTable data, ExcelExportOptions options)
        {
            try
            {
                var result = await _excelService.ExportToExcelWithFormattingAsync(data, options);
                return File(result.FileData, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", result.FileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting to Excel with formatting");
                TempData["Error"] = "Error exporting: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportMultipleSheets(Dictionary<string, DataTable> sheets)
        {
            try
            {
                var result = await _excelService.ExportMultipleSheetsAsync(sheets);
                return File(result.FileData, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", result.FileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting multiple sheets");
                TempData["Error"] = "Error exporting: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportToPdf(DataTable data, PdfReportOptions options)
        {
            try
            {
                var pdfBytes = await _pdfService.GeneratePdfReportAsync(data, options);
                return File(pdfBytes, "application/pdf", $"Export_{DateTime.Now:yyyyMMdd}.pdf");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting to PDF");
                TempData["Error"] = "Error exporting: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ExportSimplePdf(DataTable data, string title)
        {
            try
            {
                var pdfBytes = await _pdfService.GenerateSimplePdfAsync(data, title);
                return File(pdfBytes, "application/pdf", $"Export_{DateTime.Now:yyyyMMdd}.pdf");
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
                return View(new ExportJob());
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
        public async Task<IActionResult> Create(ExportJob model)
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

                await _context.Set<ExportJob>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ExportJob created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ExportJob");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
