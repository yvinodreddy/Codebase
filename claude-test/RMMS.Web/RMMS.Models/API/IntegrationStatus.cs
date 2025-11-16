using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.API
{
    public class IntegrationStatus
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string IntegrationType { get; set; } = string.Empty;

        [StringLength(500)]
        public string Endpoint { get; set; } = string.Empty;

        [StringLength(50)]
        public string Status { get; set; } = "Unknown";

        public DateTime? LastChecked { get; set; }

        public DateTime? LastSuccess { get; set; }

        public int SuccessCount { get; set; } = 0;

        public int FailureCount { get; set; } = 0;

        public int ResponseTime { get; set; } = 0;

        [StringLength(500)]
        public string LastError { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
