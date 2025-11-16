using System.Data;
using System.Threading.Tasks;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for exporting data to PDF with professional formatting
    /// </summary>
    public interface IPdfExportService
    {
        /// <summary>
        /// Generate PDF report from data table
        /// </summary>
        Task<byte[]> GeneratePdfReportAsync(DataTable data, PdfReportOptions options);

        /// <summary>
        /// Generate simple PDF report with default formatting
        /// </summary>
        Task<byte[]> GenerateSimplePdfAsync(DataTable data, string title);
    }

    /// <summary>
    /// Configuration options for PDF reports
    /// </summary>
    public class PdfReportOptions
    {
        public string Title { get; set; } = string.Empty;
        public string Subtitle { get; set; } = string.Empty;
        public bool IncludePageNumbers { get; set; } = true;
        public bool IncludeGeneratedDate { get; set; } = true;
        public bool IncludeWatermark { get; set; } = false;
        public string WatermarkText { get; set; } = "CONFIDENTIAL";
        public string CompanyName { get; set; } = "RMMS - Rice Mill Management System";
    }
}
