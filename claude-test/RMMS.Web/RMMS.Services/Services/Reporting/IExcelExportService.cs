using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for exporting data to Excel with advanced formatting
    /// </summary>
    public interface IExcelExportService
    {
        /// <summary>
        /// Export data table to Excel with basic formatting
        /// </summary>
        Task<ExcelExportResult> ExportToExcelAsync(DataTable data, string sheetName);

        /// <summary>
        /// Export data table to Excel with advanced formatting options
        /// </summary>
        Task<ExcelExportResult> ExportToExcelWithFormattingAsync(DataTable data, ExcelExportOptions options);

        /// <summary>
        /// Export multiple sheets to a single Excel file
        /// </summary>
        Task<ExcelExportResult> ExportMultipleSheetsAsync(Dictionary<string, DataTable> sheets);

        /// <summary>
        /// Export with custom styling for header, alternating rows, and summary
        /// </summary>
        Task<ExcelExportResult> ExportWithStylingAsync(DataTable data, ExcelExportOptions options);

        /// <summary>
        /// Export generic list of objects to Excel
        /// </summary>
        Task<ExcelExportResult> ExportListToExcelAsync<T>(List<T> data, string sheetName) where T : class;
    }
}
