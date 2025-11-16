using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// DTO for tracking mobile analytics events
    /// </summary>
    public class AnalyticsEventDto
    {
        [Required]
        [MaxLength(50)]
        public string Category { get; set; } = string.Empty;

        [Required]
        [MaxLength(100)]
        public string Action { get; set; } = string.Empty;

        [MaxLength(200)]
        public string? Label { get; set; }

        public decimal? Value { get; set; }

        [MaxLength(100)]
        public string? Screen { get; set; }

        [MaxLength(100)]
        public string? SessionId { get; set; }

        public Dictionary<string, object>? Properties { get; set; }

        public DateTime ClientTimestamp { get; set; }

        [MaxLength(20)]
        public string? AppVersion { get; set; }
    }

    /// <summary>
    /// DTO for batch analytics event submission
    /// </summary>
    public class BatchAnalyticsDto
    {
        [Required]
        public List<AnalyticsEventDto> Events { get; set; } = new List<AnalyticsEventDto>();

        public DateTime ClientTimestamp { get; set; }
    }
}
