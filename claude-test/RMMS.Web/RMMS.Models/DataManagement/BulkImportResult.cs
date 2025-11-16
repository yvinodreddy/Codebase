using System.Collections.Generic;

namespace RMMS.Models.DataManagement
{
    public class BulkImportResult
    {
        public bool Success { get; set; }
        public int TotalRecords { get; set; }
        public int SuccessCount { get; set; }
        public int FailedCount { get; set; }
        public List<string> Errors { get; set; } = new();
        public List<string> Warnings { get; set; } = new();
        public string Message { get; set; } = string.Empty;
    }

    public class BulkExportOptions
    {
        public string EntityType { get; set; } = string.Empty;
        public string Format { get; set; } = "Excel"; // Excel, CSV
        public bool IncludeHeaders { get; set; } = true;
        public Dictionary<string, string> Filters { get; set; } = new();
    }
}
