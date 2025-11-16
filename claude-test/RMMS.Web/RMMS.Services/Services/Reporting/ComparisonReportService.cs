using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for generating comparative analysis reports with period-over-period variance
    /// </summary>
    public class ComparisonReportService : IComparisonReportService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<ComparisonReportService> _logger;
        private readonly IExcelExportService _excelService;
        private readonly IPdfExportService _pdfService;

        public ComparisonReportService(
            ApplicationDbContext context,
            ILogger<ComparisonReportService> logger,
            IExcelExportService excelService,
            IPdfExportService pdfService)
        {
            _context = context;
            _logger = logger;
            _excelService = excelService;
            _pdfService = pdfService;
        }

        public async Task<ComparisonReport> GenerateMonthOverMonthReportAsync(DateTime currentMonth, string category)
        {
            var period2Start = new DateTime(currentMonth.Year, currentMonth.Month, 1);
            var period2End = period2Start.AddMonths(1).AddDays(-1);

            var period1Start = period2Start.AddMonths(-1);
            var period1End = period1Start.AddMonths(1).AddDays(-1);

            var options = new ComparisonReportOptions
            {
                Period1 = new ComparisonPeriod
                {
                    StartDate = period1Start,
                    EndDate = period1End,
                    PeriodLabel = $"{period1Start:MMM yyyy}"
                },
                Period2 = new ComparisonPeriod
                {
                    StartDate = period2Start,
                    EndDate = period2End,
                    PeriodLabel = $"{period2Start:MMM yyyy}"
                },
                ComparisonType = "MoM",
                Category = category
            };

            return await GenerateCustomComparisonReportAsync(options);
        }

        public async Task<ComparisonReport> GenerateYearOverYearReportAsync(int currentYear, string category)
        {
            var period2Start = new DateTime(currentYear, 1, 1);
            var period2End = new DateTime(currentYear, 12, 31);

            var period1Start = new DateTime(currentYear - 1, 1, 1);
            var period1End = new DateTime(currentYear - 1, 12, 31);

            var options = new ComparisonReportOptions
            {
                Period1 = new ComparisonPeriod
                {
                    StartDate = period1Start,
                    EndDate = period1End,
                    PeriodLabel = $"{currentYear - 1}"
                },
                Period2 = new ComparisonPeriod
                {
                    StartDate = period2Start,
                    EndDate = period2End,
                    PeriodLabel = $"{currentYear}"
                },
                ComparisonType = "YoY",
                Category = category
            };

            return await GenerateCustomComparisonReportAsync(options);
        }

        public async Task<ComparisonReport> GenerateQuarterOverQuarterReportAsync(int currentYear, int currentQuarter, string category)
        {
            var period2Start = new DateTime(currentYear, (currentQuarter - 1) * 3 + 1, 1);
            var period2End = period2Start.AddMonths(3).AddDays(-1);

            var period1Start = period2Start.AddMonths(-3);
            var period1End = period1Start.AddMonths(3).AddDays(-1);

            var options = new ComparisonReportOptions
            {
                Period1 = new ComparisonPeriod
                {
                    StartDate = period1Start,
                    EndDate = period1End,
                    PeriodLabel = $"Q{currentQuarter - 1} {period1Start:yyyy}"
                },
                Period2 = new ComparisonPeriod
                {
                    StartDate = period2Start,
                    EndDate = period2End,
                    PeriodLabel = $"Q{currentQuarter} {currentYear}"
                },
                ComparisonType = "QoQ",
                Category = category
            };

            return await GenerateCustomComparisonReportAsync(options);
        }

        public async Task<ComparisonReport> GenerateCustomComparisonReportAsync(ComparisonReportOptions options)
        {
            _logger.LogInformation($"Generating {options.ComparisonType} comparison report for {options.Category}");

            var results = new List<ComparisonResult>();

            switch (options.Category.ToLower())
            {
                case "sales":
                    results = await GetSalesComparisonAsync(options.Period1, options.Period2);
                    break;
                case "inventory":
                    results = await GetInventoryComparisonAsync(options.Period1, options.Period2);
                    break;
                case "production":
                    results = await GetProductionComparisonAsync(options.Period1, options.Period2);
                    break;
                case "financial":
                    results = await GetFinancialComparisonAsync(options.Period1, options.Period2);
                    break;
                default:
                    _logger.LogWarning($"Unknown category: {options.Category}");
                    break;
            }

            var report = new ComparisonReport
            {
                ReportTitle = $"{options.ComparisonType} {options.Category} Comparison Report",
                GeneratedDate = DateTime.Now,
                Period1 = options.Period1,
                Period2 = options.Period2,
                Results = results,
                OverallVariancePercentage = results.Any() ? results.Average(r => r.VariancePercentage) : 0,
                Summary = GenerateSummary(results, options)
            };

            return await Task.FromResult(report);
        }

        #region Category-Specific Comparisons

        private async Task<List<ComparisonResult>> GetSalesComparisonAsync(ComparisonPeriod period1, ComparisonPeriod period2)
        {
            var results = new List<ComparisonResult>();

            // Total Sales
            var sales1 = _context.RiceSales
                .Where(s => s.SaleDate >= period1.StartDate && s.SaleDate <= period1.EndDate)
                .Sum(s => (decimal?)s.TotalInvoiceValue) ?? 0;

            var sales2 = _context.RiceSales
                .Where(s => s.SaleDate >= period2.StartDate && s.SaleDate <= period2.EndDate)
                .Sum(s => (decimal?)s.TotalInvoiceValue) ?? 0;

            results.Add(CreateComparisonResult("Total Sales", sales1, sales2));

            // Sales Count
            var count1 = _context.RiceSales
                .Count(s => s.SaleDate >= period1.StartDate && s.SaleDate <= period1.EndDate);

            var count2 = _context.RiceSales
                .Count(s => s.SaleDate >= period2.StartDate && s.SaleDate <= period2.EndDate);

            results.Add(CreateComparisonResult("Number of Sales", count1, count2));

            // Average Sale Value
            var avgSale1 = count1 > 0 ? sales1 / count1 : 0;
            var avgSale2 = count2 > 0 ? sales2 / count2 : 0;

            results.Add(CreateComparisonResult("Average Sale Value", avgSale1, avgSale2));

            // Total Quantity
            var qty1 = _context.RiceSales
                .Where(s => s.SaleDate >= period1.StartDate && s.SaleDate <= period1.EndDate)
                .Sum(s => (decimal?)s.Quantity) ?? 0;

            var qty2 = _context.RiceSales
                .Where(s => s.SaleDate >= period2.StartDate && s.SaleDate <= period2.EndDate)
                .Sum(s => (decimal?)s.Quantity) ?? 0;

            results.Add(CreateComparisonResult("Total Quantity Sold (kg)", qty1, qty2));

            return await Task.FromResult(results);
        }

        private async Task<List<ComparisonResult>> GetInventoryComparisonAsync(ComparisonPeriod period1, ComparisonPeriod period2)
        {
            var results = new List<ComparisonResult>();

            // Total Product Count
            var productCount1 = _context.Products.Count(p => p.IsActive);
            var productCount2 = productCount1; // Same products

            results.Add(CreateComparisonResult("Active Products", productCount1, productCount2));

            // Stock Movements
            var movements1 = _context.StockMovements
                .Count(s => s.MovementDate >= period1.StartDate && s.MovementDate <= period1.EndDate);

            var movements2 = _context.StockMovements
                .Count(s => s.MovementDate >= period2.StartDate && s.MovementDate <= period2.EndDate);

            results.Add(CreateComparisonResult("Stock Movements", movements1, movements2));

            // Stock Adjustments
            var adjustments1 = _context.StockAdjustments
                .Count(s => s.AdjustmentDate >= period1.StartDate && s.AdjustmentDate <= period1.EndDate);

            var adjustments2 = _context.StockAdjustments
                .Count(s => s.AdjustmentDate >= period2.StartDate && s.AdjustmentDate <= period2.EndDate);

            results.Add(CreateComparisonResult("Stock Adjustments", adjustments1, adjustments2));

            return await Task.FromResult(results);
        }

        private async Task<List<ComparisonResult>> GetProductionComparisonAsync(ComparisonPeriod period1, ComparisonPeriod period2)
        {
            var results = new List<ComparisonResult>();

            // Production Batches
            var batches1 = _context.ProductionBatches
                .Count(p => p.BatchDate >= period1.StartDate && p.BatchDate <= period1.EndDate);

            var batches2 = _context.ProductionBatches
                .Count(p => p.BatchDate >= period2.StartDate && p.BatchDate <= period2.EndDate);

            results.Add(CreateComparisonResult("Production Batches", batches1, batches2));

            // Completed Batches
            var completed1 = _context.ProductionBatches
                .Count(p => p.BatchDate >= period1.StartDate && p.BatchDate <= period1.EndDate && p.Status == "Completed");

            var completed2 = _context.ProductionBatches
                .Count(p => p.BatchDate >= period2.StartDate && p.BatchDate <= period2.EndDate && p.Status == "Completed");

            results.Add(CreateComparisonResult("Completed Batches", completed1, completed2));

            // Average Quality Score
            var avgQuality1 = _context.ProductionBatches
                .Where(p => p.BatchDate >= period1.StartDate && p.BatchDate <= period1.EndDate && p.QualityScore.HasValue)
                .Average(p => (decimal?)p.QualityScore) ?? 0;

            var avgQuality2 = _context.ProductionBatches
                .Where(p => p.BatchDate >= period2.StartDate && p.BatchDate <= period2.EndDate && p.QualityScore.HasValue)
                .Average(p => (decimal?)p.QualityScore) ?? 0;

            results.Add(CreateComparisonResult("Avg Quality Score", avgQuality1, avgQuality2));

            return await Task.FromResult(results);
        }

        private async Task<List<ComparisonResult>> GetFinancialComparisonAsync(ComparisonPeriod period1, ComparisonPeriod period2)
        {
            var results = new List<ComparisonResult>();

            // Total Revenue
            var revenue1 = _context.RiceSales
                .Where(s => s.SaleDate >= period1.StartDate && s.SaleDate <= period1.EndDate)
                .Sum(s => (decimal?)s.GrossInvoiceAmount) ?? 0;

            var revenue2 = _context.RiceSales
                .Where(s => s.SaleDate >= period2.StartDate && s.SaleDate <= period2.EndDate)
                .Sum(s => (decimal?)s.GrossInvoiceAmount) ?? 0;

            results.Add(CreateComparisonResult("Total Revenue", revenue1, revenue2));

            // Cash Receipts
            var cash1 = _context.CashBooks
                .Where(c => c.TransactionDate >= period1.StartDate && c.TransactionDate <= period1.EndDate)
                .Sum(c => (decimal?)c.Receipts) ?? 0;

            var cash2 = _context.CashBooks
                .Where(c => c.TransactionDate >= period2.StartDate && c.TransactionDate <= period2.EndDate)
                .Sum(c => (decimal?)c.Receipts) ?? 0;

            results.Add(CreateComparisonResult("Cash Receipts", cash1, cash2));

            // Cash Payments
            var expenses1 = _context.CashBooks
                .Where(c => c.TransactionDate >= period1.StartDate && c.TransactionDate <= period1.EndDate)
                .Sum(c => (decimal?)c.Payments) ?? 0;

            var expenses2 = _context.CashBooks
                .Where(c => c.TransactionDate >= period2.StartDate && c.TransactionDate <= period2.EndDate)
                .Sum(c => (decimal?)c.Payments) ?? 0;

            results.Add(CreateComparisonResult("Cash Payments", expenses1, expenses2));

            return await Task.FromResult(results);
        }

        #endregion

        #region Export Methods

        public async Task<ExcelExportResult> ExportComparisonToExcelAsync(ComparisonReport report)
        {
            var dataTable = new DataTable(report.ReportTitle);
            dataTable.Columns.Add("Metric", typeof(string));
            dataTable.Columns.Add(report.Period1.PeriodLabel, typeof(decimal));
            dataTable.Columns.Add(report.Period2.PeriodLabel, typeof(decimal));
            dataTable.Columns.Add("Variance", typeof(decimal));
            dataTable.Columns.Add("Variance %", typeof(decimal));
            dataTable.Columns.Add("Trend", typeof(string));

            foreach (var result in report.Results)
            {
                dataTable.Rows.Add(
                    result.Metric,
                    result.Period1Value,
                    result.Period2Value,
                    result.Variance,
                    result.VariancePercentage,
                    result.TrendIcon
                );
            }

            var options = new ExcelExportOptions
            {
                SheetName = report.ReportTitle,
                ApplyHeaderFormatting = true,
                ApplyAlternateRowColors = true,
                AutoFitColumns = true,
                FreezePanes = true,
                ApplyFilters = true
            };

            return await _excelService.ExportToExcelWithFormattingAsync(dataTable, options);
        }

        public async Task<byte[]> ExportComparisonToPdfAsync(ComparisonReport report)
        {
            var dataTable = new DataTable(report.ReportTitle);
            dataTable.Columns.Add("Metric", typeof(string));
            dataTable.Columns.Add(report.Period1.PeriodLabel, typeof(string));
            dataTable.Columns.Add(report.Period2.PeriodLabel, typeof(string));
            dataTable.Columns.Add("Variance", typeof(string));
            dataTable.Columns.Add("Trend", typeof(string));

            foreach (var result in report.Results)
            {
                dataTable.Rows.Add(
                    result.Metric,
                    result.Period1Value.ToString("N2"),
                    result.Period2Value.ToString("N2"),
                    $"{result.Variance:N2} ({result.VariancePercentage:N1}%)",
                    result.TrendIcon
                );
            }

            var pdfOptions = new PdfReportOptions
            {
                Title = report.ReportTitle,
                Subtitle = $"{report.Period1.PeriodLabel} vs {report.Period2.PeriodLabel}",
                CompanyName = "RMMS Rice Mill",
                IncludeGeneratedDate = true,
                IncludePageNumbers = true
            };

            return await _pdfService.GeneratePdfReportAsync(dataTable, pdfOptions);
        }

        #endregion

        #region Helper Methods

        private ComparisonResult CreateComparisonResult(string metric, decimal value1, decimal value2)
        {
            var variance = value2 - value1;
            var variancePercentage = value1 != 0 ? (variance / value1) * 100 : 0;
            var trend = variance > 0 ? "Up" : variance < 0 ? "Down" : "Flat";
            var trendIcon = variance > 0 ? "↑" : variance < 0 ? "↓" : "→";

            return new ComparisonResult
            {
                Metric = metric,
                Period1Value = value1,
                Period2Value = value2,
                Variance = variance,
                VariancePercentage = variancePercentage,
                Trend = trend,
                TrendIcon = trendIcon
            };
        }

        private string GenerateSummary(List<ComparisonResult> results, ComparisonReportOptions options)
        {
            if (!results.Any())
                return "No data available for comparison.";

            var improvements = results.Count(r => r.Variance > 0);
            var declines = results.Count(r => r.Variance < 0);
            var flat = results.Count(r => r.Variance == 0);

            return $"Comparison of {results.Count} metrics between {options.Period1.PeriodLabel} and {options.Period2.PeriodLabel}: " +
                   $"{improvements} improved, {declines} declined, {flat} unchanged. " +
                   $"Overall average variance: {results.Average(r => r.VariancePercentage):N1}%.";
        }

        #endregion
    }
}
