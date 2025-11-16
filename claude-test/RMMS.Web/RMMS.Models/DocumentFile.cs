using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models
{
    /// <summary>
    /// Document File for File Manager - Phase 2
    /// </summary>
    public class DocumentFile
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(255)]
        public string FileName { get; set; } = string.Empty;

        [Required]
        [StringLength(255)]
        public string OriginalFileName { get; set; } = string.Empty;

        [Required]
        [StringLength(500)]
        public string FilePath { get; set; } = string.Empty;

        [StringLength(100)]
        public string? FileExtension { get; set; }

        public long FileSize { get; set; } // in bytes

        [StringLength(100)]
        public string? MimeType { get; set; }

        // Categorization
        [Required]
        [StringLength(50)]
        public string Category { get; set; } = "General"; // Invoice, Certificate, Report, Contract, Other

        [StringLength(100)]
        public string? SubCategory { get; set; }

        [StringLength(500)]
        public string? Description { get; set; }

        [StringLength(200)]
        public string? Tags { get; set; } // Comma-separated tags for searching

        // Relationships
        public int? RelatedEntityId { get; set; } // SaleId, PurchaseId, BatchId, etc.

        [StringLength(50)]
        public string? RelatedEntityType { get; set; } // Sale, Purchase, ProductionBatch, etc.

        // Upload tracking
        public int? UploadedBy { get; set; }

        public DateTime UploadedDate { get; set; } = DateTime.Now;

        // Access control
        public bool IsPublic { get; set; } = false;

        public bool IsActive { get; set; } = true;

        public DateTime? DeletedDate { get; set; }

        public int? DeletedBy { get; set; }

        // Version control
        public int Version { get; set; } = 1;

        public int? ParentFileId { get; set; } // For versioning

        [ForeignKey("ParentFileId")]
        public DocumentFile? ParentFile { get; set; }

        // Download tracking
        public int DownloadCount { get; set; } = 0;

        public DateTime? LastDownloadDate { get; set; }

        // Computed properties
        [NotMapped]
        public string FileSizeFormatted
        {
            get
            {
                string[] sizes = { "B", "KB", "MB", "GB", "TB" };
                double len = FileSize;
                int order = 0;
                while (len >= 1024 && order < sizes.Length - 1)
                {
                    order++;
                    len = len / 1024;
                }
                return $"{len:0.##} {sizes[order]}";
            }
        }
    }
}
