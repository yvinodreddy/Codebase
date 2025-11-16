using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Mobile
{
    /// <summary>
    /// Tracks data synchronization between mobile devices and server
    /// </summary>
    public class SyncLog
    {
        [Key]
        public int Id { get; set; }

        /// <summary>
        /// Device that performed the sync
        /// </summary>
        public int DeviceId { get; set; }

        /// <summary>
        /// User who performed the sync
        /// </summary>
        [Required]
        [MaxLength(100)]
        public string UserId { get; set; } = string.Empty;

        /// <summary>
        /// Entity type being synced (e.g., "ProductionBatch", "Inventory", "Sales")
        /// </summary>
        [Required]
        [MaxLength(100)]
        public string EntityType { get; set; } = string.Empty;

        /// <summary>
        /// Sync operation: pull, push, conflict
        /// </summary>
        [Required]
        [MaxLength(20)]
        public string Operation { get; set; } = string.Empty;

        /// <summary>
        /// Number of records synced
        /// </summary>
        public int RecordCount { get; set; }

        /// <summary>
        /// Timestamp on client when sync started
        /// </summary>
        public DateTime ClientTimestamp { get; set; }

        /// <summary>
        /// Timestamp on server when sync was processed
        /// </summary>
        public DateTime ServerTimestamp { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Sync status: success, partial, failed
        /// </summary>
        [MaxLength(20)]
        public string Status { get; set; } = "success";

        /// <summary>
        /// Error message if sync failed
        /// </summary>
        public string? ErrorMessage { get; set; }

        /// <summary>
        /// Number of conflicts detected during sync
        /// </summary>
        public int ConflictCount { get; set; } = 0;

        /// <summary>
        /// Data size transferred in bytes
        /// </summary>
        public long DataSizeBytes { get; set; }

        /// <summary>
        /// Duration of sync operation in milliseconds
        /// </summary>
        public int DurationMs { get; set; }

        /// <summary>
        /// Additional sync metadata (JSON)
        /// </summary>
        public string? Metadata { get; set; }

        [ForeignKey("DeviceId")]
        public virtual MobileDevice? Device { get; set; }
    }
}
