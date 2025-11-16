using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.API
{
    public class Webhook
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [Required]
        [StringLength(500)]
        public string Url { get; set; } = string.Empty;

        [StringLength(100)]
        public string EventType { get; set; } = string.Empty;

        [StringLength(50)]
        public string Method { get; set; } = "POST";

        public string Headers { get; set; } = string.Empty;

        public string PayloadTemplate { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        public int RetryCount { get; set; } = 3;

        public int TimeoutSeconds { get; set; } = 30;

        public DateTime? LastTriggered { get; set; }

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
