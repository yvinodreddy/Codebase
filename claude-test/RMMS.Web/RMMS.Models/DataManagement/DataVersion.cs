using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class DataVersion
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityType { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityId { get; set; } = string.Empty;

        public int VersionNumber { get; set; } = 1;

        public string DataSnapshot { get; set; } = string.Empty;

        [StringLength(450)]
        public string ChangedBy { get; set; } = string.Empty;

        public string ChangeReason { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
