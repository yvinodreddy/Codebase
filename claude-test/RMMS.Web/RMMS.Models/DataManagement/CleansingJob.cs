using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class CleansingJob
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string TableName { get; set; } = string.Empty;

        public string CleansingRules { get; set; } = string.Empty;

        public int RecordsCleaned { get; set; } = 0;

        public int IssuesFound { get; set; } = 0;

        [StringLength(50)]
        public string Status { get; set; } = "Pending";

        public string CleansingReport { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
