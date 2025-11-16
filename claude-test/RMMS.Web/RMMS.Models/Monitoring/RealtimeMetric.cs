using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Monitoring
{
    public class RealtimeMetric
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string MetricType { get; set; } = string.Empty;

        public double Value { get; set; } = 0;

        [StringLength(50)]
        public string Unit { get; set; } = string.Empty;

        public DateTime Timestamp { get; set; } = DateTime.Now;

        [StringLength(100)]
        public string Source { get; set; } = string.Empty;

        public string Metadata { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
