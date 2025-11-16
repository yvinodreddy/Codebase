using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class BulkOperation
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(50)]
        public string OperationType { get; set; } = "Import";

        [StringLength(100)]
        public string EntityType { get; set; } = string.Empty;

        [StringLength(500)]
        public string FilePath { get; set; } = string.Empty;

        public int TotalRecords { get; set; } = 0;

        public int ProcessedRecords { get; set; } = 0;

        public int SuccessfulRecords { get; set; } = 0;

        public int FailedRecords { get; set; } = 0;

        [StringLength(50)]
        public string Status { get; set; } = "Pending";

        public string ErrorLog { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
