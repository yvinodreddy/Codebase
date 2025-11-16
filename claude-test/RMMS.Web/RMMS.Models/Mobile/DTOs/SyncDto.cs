using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// DTO for data synchronization requests
    /// </summary>
    public class SyncRequestDto
    {
        [Required]
        [MaxLength(100)]
        public string EntityType { get; set; } = string.Empty;

        public DateTime? LastSyncTimestamp { get; set; }

        public int PageSize { get; set; } = 100;

        public int PageNumber { get; set; } = 1;

        public bool IncludeDeleted { get; set; } = false;
    }

    /// <summary>
    /// Generic sync response with pagination
    /// </summary>
    public class SyncResponseDto<T>
    {
        public List<T> Data { get; set; } = new List<T>();

        public DateTime ServerTimestamp { get; set; }

        public int TotalRecords { get; set; }

        public int PageNumber { get; set; }

        public int PageSize { get; set; }

        public bool HasMore { get; set; }

        public SyncMetadata? Metadata { get; set; }
    }

    /// <summary>
    /// Sync metadata
    /// </summary>
    public class SyncMetadata
    {
        public int ConflictCount { get; set; }
        public List<string>? ConflictIds { get; set; }
        public DateTime? NextSyncRecommended { get; set; }
    }

    /// <summary>
    /// DTO for batch sync operations
    /// </summary>
    public class BatchSyncRequestDto
    {
        [Required]
        public List<SyncRequestDto> Requests { get; set; } = new List<SyncRequestDto>();

        public DateTime ClientTimestamp { get; set; }
    }

    /// <summary>
    /// Batch sync response
    /// </summary>
    public class BatchSyncResponseDto
    {
        public Dictionary<string, object> Results { get; set; } = new Dictionary<string, object>();

        public DateTime ServerTimestamp { get; set; }

        public int TotalRecords { get; set; }

        public int SuccessCount { get; set; }

        public int ErrorCount { get; set; }

        public List<string>? Errors { get; set; }
    }
}
