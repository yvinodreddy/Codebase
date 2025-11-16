using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using RMMS.Models.Reporting;
using RMMS.Services.Services.Reporting;
using System;
using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    /// <summary>
    /// Controller for data export operations (Excel, PDF, CSV)
    /// </summary>
    public class ExportController : Controller
    {
        private readonly IExcelExportService _excelService;
        private readonly IPdfExportService _pdfService;
        private readonly ILogger<ExportController> _logger;

        public ExportController(
            IExcelExportService excelService,
            IPdfExportService pdfService,
            ILogger<ExportController> logger)
        {
            _excelService = excelService;
            _pdfService = pdfService;
            _logger = logger;
        }

        /// <summary>
        /// Test Excel export with sample data
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> TestExportToExcel()
        {
            try
            {
                _logger.LogInformation("Testing Excel export with sample data");

                // Create sample data
                var dataTable = new DataTable("Sample Report");
                dataTable.Columns.Add("ID", typeof(int));
                dataTable.Columns.Add("Date", typeof(DateTime));
                dataTable.Columns.Add("Description", typeof(string));
                dataTable.Columns.Add("Amount", typeof(decimal));
                dataTable.Columns.Add("Status", typeof(string));

                // Add sample rows
                for (int i = 1; i <= 100; i++)
                {
                    dataTable.Rows.Add(
                        i,
                        DateTime.Now.AddDays(-i),
                        $"Sample Transaction {i}",
                        1000.50m * i,
                        i % 2 == 0 ? "Completed" : "Pending"
                    );
                }

                // Configure export options
                var options = new ExcelExportOptions
                {
                    SheetName = "Sample Report",
                    ApplyHeaderFormatting = true,
                    ApplyAlternateRowColors = true,
                    AutoFitColumns = true,
                    FreezePanes = true,
                    ApplyFilters = true,
                    IncludeSummaryRow = true,
                    ColumnFormats = new List<ExcelColumnFormat>
                    {
                        new ExcelColumnFormat { ColumnName = "Amount", NumberFormat = "₹#,##0.00", IsBold = true }
                    }
                };

                // Export
                var result = await _excelService.ExportToExcelWithFormattingAsync(dataTable, options);

                if (!result.Success)
                {
                    return BadRequest($"Export failed: {result.ErrorMessage}");
                }

                _logger.LogInformation($"Excel export successful. File size: {result.FileSizeBytes} bytes");

                return File(result.FileData,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    result.FileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during test Excel export");
                return StatusCode(500, $"An error occurred during export: {ex.Message}");
            }
        }

        /// <summary>
        /// Test multi-sheet Excel export
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> TestMultiSheetExport()
        {
            try
            {
                _logger.LogInformation("Testing multi-sheet Excel export");

                var sheets = new Dictionary<string, DataTable>();

                // Sheet 1: Sales Summary
                var salesTable = new DataTable("Sales");
                salesTable.Columns.Add("Month", typeof(string));
                salesTable.Columns.Add("Revenue", typeof(decimal));
                salesTable.Columns.Add("Orders", typeof(int));
                salesTable.Rows.Add("January", 50000.00m, 120);
                salesTable.Rows.Add("February", 45000.00m, 110);
                salesTable.Rows.Add("March", 55000.00m, 130);
                sheets.Add("Sales Summary", salesTable);

                // Sheet 2: Production Summary
                var productionTable = new DataTable("Production");
                productionTable.Columns.Add("Month", typeof(string));
                productionTable.Columns.Add("Output (Bags)", typeof(decimal));
                productionTable.Columns.Add("Yield %", typeof(decimal));
                productionTable.Rows.Add("January", 1000.00m, 72.5m);
                productionTable.Rows.Add("February", 950.00m, 71.8m);
                productionTable.Rows.Add("March", 1100.00m, 73.2m);
                sheets.Add("Production Summary", productionTable);

                // Sheet 3: Inventory Summary
                var inventoryTable = new DataTable("Inventory");
                inventoryTable.Columns.Add("Item", typeof(string));
                inventoryTable.Columns.Add("Stock", typeof(decimal));
                inventoryTable.Columns.Add("Unit", typeof(string));
                inventoryTable.Rows.Add("Rice - Premium", 500.00m, "Bags");
                inventoryTable.Rows.Add("Rice - Standard", 750.00m, "Bags");
                inventoryTable.Rows.Add("Paddy", 1200.00m, "Bags");
                sheets.Add("Inventory Summary", inventoryTable);

                var result = await _excelService.ExportMultipleSheetsAsync(sheets);

                if (!result.Success)
                {
                    return BadRequest($"Export failed: {result.ErrorMessage}");
                }

                _logger.LogInformation($"Multi-sheet export successful. File size: {result.FileSizeBytes} bytes");

                return File(result.FileData,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    $"RMMS_Complete_Report_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during multi-sheet export");
                return StatusCode(500, $"An error occurred during export: {ex.Message}");
            }
        }

        /// <summary>
        /// Test PDF export with sample data
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> TestExportToPdf()
        {
            try
            {
                _logger.LogInformation("Testing PDF export with sample data");

                // Create sample data
                var dataTable = new DataTable("Sample Report");
                dataTable.Columns.Add("ID", typeof(int));
                dataTable.Columns.Add("Date", typeof(DateTime));
                dataTable.Columns.Add("Description", typeof(string));
                dataTable.Columns.Add("Amount", typeof(decimal));
                dataTable.Columns.Add("Status", typeof(string));

                for (int i = 1; i <= 50; i++)
                {
                    dataTable.Rows.Add(
                        i,
                        DateTime.Now.AddDays(-i),
                        $"Sample Transaction {i}",
                        1000.50m * i,
                        i % 2 == 0 ? "Completed" : "Pending"
                    );
                }

                var options = new PdfReportOptions
                {
                    Title = "Sample Report",
                    Subtitle = "Generated from RMMS System",
                    IncludePageNumbers = true,
                    IncludeGeneratedDate = true,
                    CompanyName = "RMMS - Rice Mill Management System"
                };

                var pdfBytes = await _pdfService.GeneratePdfReportAsync(dataTable, options);

                _logger.LogInformation($"PDF export successful. File size: {pdfBytes.Length} bytes");

                return File(pdfBytes, "application/pdf", $"Sample_Report_{DateTime.Now:yyyyMMdd_HHmmss}.pdf");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during test PDF export");
                return StatusCode(500, $"An error occurred during PDF export: {ex.Message}");
            }
        }

        /// <summary>
        /// Export test view
        /// </summary>
        public IActionResult Index()
        {
            return View();
        }
    }
}
