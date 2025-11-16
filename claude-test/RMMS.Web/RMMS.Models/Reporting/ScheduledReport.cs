using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Reporting
{
    public class ScheduledReport
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        public int ReportDefinitionId { get; set; }

        [StringLength(50)]
        public string ScheduleType { get; set; } = "Daily"; // Once, Daily, Weekly, Monthly

        public DateTime? ScheduledTime { get; set; }

        [StringLength(500)]
        public string EmailRecipients { get; set; } = string.Empty;

        [StringLength(50)]
        public string OutputFormat { get; set; } = "PDF";

        public bool IsActive { get; set; } = true;

        public DateTime? LastRunDate { get; set; }

        public DateTime? NextRunDate { get; set; }

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
