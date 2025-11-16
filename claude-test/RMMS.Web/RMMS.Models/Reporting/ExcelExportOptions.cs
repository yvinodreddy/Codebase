using System;
using System.Collections.Generic;

namespace RMMS.Models.Reporting
{
    /// <summary>
    /// Configuration options for Excel export formatting
    /// </summary>
    public class ExcelExportOptions
    {
        public string SheetName { get; set; } = "Sheet1";
        public bool ApplyHeaderFormatting { get; set; } = true;
        public bool ApplyAlternateRowColors { get; set; } = true;
        public bool AutoFitColumns { get; set; } = true;
        public bool FreezePanes { get; set; } = true;
        public bool ApplyFilters { get; set; } = true;
        public bool IncludeSummaryRow { get; set; } = false;
        public List<ExcelColumnFormat> ColumnFormats { get; set; } = new();
    }

    /// <summary>
    /// Format specification for individual columns
    /// </summary>
    public class ExcelColumnFormat
    {
        public string ColumnName { get; set; } = string.Empty;
        public string NumberFormat { get; set; } = string.Empty; // "#,##0.00", "0.00%", "₹#,##0"
        public bool IsBold { get; set; }
        public string BackgroundColor { get; set; } = string.Empty; // Hex color like "#FF0000"
        public int? ColumnWidth { get; set; }
    }

    /// <summary>
    /// Result of Excel export operation
    /// </summary>
    public class ExcelExportResult
    {
        public bool Success { get; set; }
        public byte[] FileData { get; set; } = Array.Empty<byte>();
        public string FileName { get; set; } = string.Empty;
        public long FileSizeBytes { get; set; }
        public string ErrorMessage { get; set; } = string.Empty;
        public int RowCount { get; set; }
        public int ColumnCount { get; set; }
    }
}
