using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class AuditLog
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(450)]
        public string UserId { get; set; } = string.Empty;

        [StringLength(200)]
        public string UserName { get; set; } = string.Empty;

        [StringLength(50)]
        public string Action { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityType { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityId { get; set; } = string.Empty;

        public string OldValue { get; set; } = string.Empty;

        public string NewValue { get; set; } = string.Empty;

        [StringLength(50)]
        public string IpAddress { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
