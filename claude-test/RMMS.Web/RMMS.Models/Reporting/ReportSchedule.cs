using System;

namespace RMMS.Models.Reporting
{
    /// <summary>
    /// Scheduled report configuration
    /// </summary>
    public class ReportSchedule
    {
        public int ReportScheduleId { get; set; }
        public string ReportName { get; set; } = string.Empty;
        public string ReportType { get; set; } = string.Empty; // Excel, PDF, Both
        public string CronExpression { get; set; } = string.Empty; // "0 8 * * *" = Daily at 8 AM
        public string EmailRecipients { get; set; } = string.Empty; // Comma-separated emails
        public bool IsActive { get; set; } = true;
        public DateTime? LastRunDate { get; set; }
        public DateTime? NextRunDate { get; set; }
        public DateTime CreatedDate { get; set; }
        public string CreatedBy { get; set; } = string.Empty;
    }

    /// <summary>
    /// Scheduled report execution log
    /// </summary>
    public class ReportScheduleLog
    {
        public int LogId { get; set; }
        public int ReportScheduleId { get; set; }
        public DateTime ExecutionDate { get; set; }
        public bool Success { get; set; }
        public string ErrorMessage { get; set; } = string.Empty;
        public int RecordCount { get; set; }
        public long FileSizeBytes { get; set; }
        public TimeSpan Duration { get; set; }
    }
}
