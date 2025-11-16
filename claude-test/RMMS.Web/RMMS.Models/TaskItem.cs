using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models
{
    /// <summary>
    /// Task Item for Task Management - Phase 2
    /// </summary>
    public class TaskItem
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Title { get; set; } = string.Empty;

        [StringLength(1000)]
        public string? Description { get; set; }

        // Priority and Status
        [Required]
        [StringLength(20)]
        public string Priority { get; set; } = "Medium"; // Low, Medium, High, Urgent

        [Required]
        [StringLength(20)]
        public string Status { get; set; } = "Pending"; // Pending, InProgress, Completed, Cancelled

        // Dates
        public DateTime CreatedDate { get; set; } = DateTime.Now;

        public DateTime? DueDate { get; set; }

        public DateTime? CompletedDate { get; set; }

        // Assignment
        public int? AssignedTo { get; set; }

        public int? CreatedBy { get; set; }

        [StringLength(100)]
        public string? AssignedToName { get; set; } // Denormalized for quick display

        // Categorization
        [StringLength(50)]
        public string? Category { get; set; } // Production, Procurement, Maintenance, Quality, General

        [StringLength(200)]
        public string? Tags { get; set; } // Comma-separated tags

        // Relationships
        public int? RelatedEntityId { get; set; }

        [StringLength(50)]
        public string? RelatedEntityType { get; set; } // ProductionBatch, PurchaseOrder, Sale, etc.

        // Progress tracking
        [Range(0, 100)]
        public int ProgressPercentage { get; set; } = 0;

        // Checklist support (for subtasks)
        [StringLength(2000)]
        public string? ChecklistJson { get; set; } // JSON array of subtasks

        // Reminders
        public DateTime? ReminderDate { get; set; }

        public bool ReminderSent { get; set; } = false;

        // Notes and updates
        [StringLength(2000)]
        public string? Notes { get; set; }

        public DateTime? LastUpdatedDate { get; set; }

        public int? LastUpdatedBy { get; set; }

        // Soft delete
        public bool IsActive { get; set; } = true;

        public bool IsDeleted { get; set; } = false;

        // Computed properties
        [NotMapped]
        public bool IsOverdue
        {
            get
            {
                return DueDate.HasValue
                    && DueDate.Value < DateTime.Now
                    && Status != "Completed"
                    && Status != "Cancelled";
            }
        }

        [NotMapped]
        public string PriorityBadgeClass
        {
            get
            {
                return Priority switch
                {
                    "Urgent" => "badge-danger",
                    "High" => "badge-warning",
                    "Medium" => "badge-info",
                    "Low" => "badge-secondary",
                    _ => "badge-secondary"
                };
            }
        }

        [NotMapped]
        public string StatusBadgeClass
        {
            get
            {
                return Status switch
                {
                    "Completed" => "badge-success",
                    "InProgress" => "badge-primary",
                    "Pending" => "badge-warning",
                    "Cancelled" => "badge-secondary",
                    _ => "badge-secondary"
                };
            }
        }
    }
}
