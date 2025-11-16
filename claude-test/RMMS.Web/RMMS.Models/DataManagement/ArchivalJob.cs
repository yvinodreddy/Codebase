using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class ArchivalJob
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string TableName { get; set; } = string.Empty;

        public DateTime ArchiveBefore { get; set; }

        [StringLength(50)]
        public string Status { get; set; } = "Pending";

        public int RecordsArchived { get; set; } = 0;

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
