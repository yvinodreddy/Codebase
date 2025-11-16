using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class ExportJob
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityType { get; set; } = string.Empty;

        [StringLength(50)]
        public string ExportFormat { get; set; } = "Excel";

        [StringLength(500)]
        public string ExportPath { get; set; } = string.Empty;

        public int RecordCount { get; set; } = 0;

        public long FileSize { get; set; } = 0;

        [StringLength(50)]
        public string Status { get; set; } = "Pending";

        public DateTime? CompletedAt { get; set; }

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
