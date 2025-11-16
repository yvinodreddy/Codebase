using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.API
{
    public class ApiKey
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [Required]
        [StringLength(500)]
        public string KeyValue { get; set; } = string.Empty;

        [StringLength(450)]
        public string UserId { get; set; } = string.Empty;

        public DateTime? ExpiresAt { get; set; }

        public bool IsActive { get; set; } = true;

        public int RequestCount { get; set; } = 0;

        public int RateLimit { get; set; } = 1000;

        public DateTime? LastUsed { get; set; }

        [StringLength(500)]
        public string Permissions { get; set; } = string.Empty;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
