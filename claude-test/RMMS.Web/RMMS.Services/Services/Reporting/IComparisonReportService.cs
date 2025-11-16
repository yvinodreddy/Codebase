using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for generating comparative analysis reports (Period-over-Period)
    /// </summary>
    public interface IComparisonReportService
    {
        /// <summary>
        /// Generate Month-over-Month comparison report
        /// </summary>
        Task<ComparisonReport> GenerateMonthOverMonthReportAsync(DateTime currentMonth, string category);

        /// <summary>
        /// Generate Year-over-Year comparison report
        /// </summary>
        Task<ComparisonReport> GenerateYearOverYearReportAsync(int currentYear, string category);

        /// <summary>
        /// Generate custom period comparison report
        /// </summary>
        Task<ComparisonReport> GenerateCustomComparisonReportAsync(ComparisonReportOptions options);

        /// <summary>
        /// Generate Quarter-over-Quarter comparison report
        /// </summary>
        Task<ComparisonReport> GenerateQuarterOverQuarterReportAsync(int currentYear, int currentQuarter, string category);

        /// <summary>
        /// Export comparison report to Excel
        /// </summary>
        Task<ExcelExportResult> ExportComparisonToExcelAsync(ComparisonReport report);

        /// <summary>
        /// Export comparison report to PDF
        /// </summary>
        Task<byte[]> ExportComparisonToPdfAsync(ComparisonReport report);
    }
}
