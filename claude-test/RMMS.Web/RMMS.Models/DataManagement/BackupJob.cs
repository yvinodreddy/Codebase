using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class BackupJob
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(50)]
        public string BackupType { get; set; } = "Full";

        [StringLength(500)]
        public string BackupPath { get; set; } = string.Empty;

        public long BackupSize { get; set; } = 0;

        [StringLength(50)]
        public string Status { get; set; } = "Pending";

        public DateTime? StartedAt { get; set; }

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
