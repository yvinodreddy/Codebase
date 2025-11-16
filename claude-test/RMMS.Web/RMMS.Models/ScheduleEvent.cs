using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models
{
    /// <summary>
    /// Schedule Event for Production Calendar - Phase 2
    /// </summary>
    public class ScheduleEvent
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Title { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        public string EventType { get; set; } = string.Empty; // Production, Procurement, Delivery, Maintenance, Quality

        [Required]
        public DateTime StartDateTime { get; set; }

        public DateTime? EndDateTime { get; set; }

        public bool AllDay { get; set; } = false;

        [StringLength(1000)]
        public string? Description { get; set; }

        [StringLength(50)]
        public string? Color { get; set; } // Background color for calendar

        // Relationships
        public int? CreatedBy { get; set; }

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        public int? UpdatedBy { get; set; }

        public DateTime? UpdatedDate { get; set; }

        public bool IsActive { get; set; } = true;

        // Additional fields for specific event types
        [StringLength(100)]
        public string? ReferenceNumber { get; set; } // Batch number, PO number, etc.

        public int? RelatedEntityId { get; set; } // ProductionBatchId, PurchaseOrderId, etc.

        [StringLength(50)]
        public string? RelatedEntityType { get; set; } // ProductionBatch, PurchaseOrder, etc.

        [StringLength(100)]
        public string? Location { get; set; }

        [StringLength(100)]
        public string? AssignedTo { get; set; }

        // Status tracking
        [StringLength(50)]
        public string Status { get; set; } = "Planned"; // Planned, InProgress, Completed, Cancelled
    }
}
