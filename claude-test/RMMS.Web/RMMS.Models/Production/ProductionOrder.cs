using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;

namespace RMMS.Models.Production
{
    public class ProductionOrder
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Order Number")]
        public string OrderNumber { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Order Date")]
        [DataType(DataType.Date)]
        public DateTime OrderDate { get; set; } = DateTime.Now;

        [Required]
        [Display(Name = "Scheduled Date")]
        [DataType(DataType.Date)]
        public DateTime ScheduledDate { get; set; }

        // Source Information
        [Required]
        [StringLength(20)]
        [Display(Name = "Source Type")]
        public string SourceType { get; set; } = "Inventory"; // Procurement, Inventory

        [Display(Name = "Source Reference")]
        public int? SourceId { get; set; }

        [StringLength(100)]
        [Display(Name = "Source Reference Number")]
        public string? SourceReferenceNumber { get; set; }

        // Paddy Information
        [Required]
        [Display(Name = "Paddy Product")]
        public int PaddyProductId { get; set; }

        [ForeignKey(nameof(PaddyProductId))]
        public virtual Product? PaddyProduct { get; set; }

        [StringLength(50)]
        [Display(Name = "Paddy Variety")]
        public string? PaddyVariety { get; set; }

        [Required]
        [Display(Name = "Paddy Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal PaddyQuantity { get; set; }

        [StringLength(10)]
        [Display(Name = "Paddy UOM")]
        public string PaddyUOM { get; set; } = "Quintals";

        // Target Rice Information
        [Display(Name = "Target Rice Product")]
        public int? TargetRiceProductId { get; set; }

        [ForeignKey(nameof(TargetRiceProductId))]
        public virtual Product? TargetRiceProduct { get; set; }

        [StringLength(50)]
        [Display(Name = "Target Rice Grade")]
        public string? TargetRiceGrade { get; set; } // Premium, Grade A, Grade B, etc.

        [Display(Name = "Target Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? TargetQuantity { get; set; }

        [Display(Name = "Expected Yield %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? ExpectedYieldPercent { get; set; } = 65.00M;

        // Planning Information
        [Required]
        [StringLength(20)]
        public string Priority { get; set; } = "Normal"; // Low, Normal, High, Urgent

        [Display(Name = "Assigned Machine")]
        public int? AssignedMachineId { get; set; }

        [ForeignKey(nameof(AssignedMachineId))]
        public virtual Machine? AssignedMachine { get; set; }

        [Display(Name = "Assigned Supervisor")]
        public int? AssignedSupervisorId { get; set; }

        [ForeignKey(nameof(AssignedSupervisorId))]
        public virtual Employee? AssignedSupervisor { get; set; }

        // Customer Order Linking (Future)
        [Display(Name = "Customer Order")]
        public int? CustomerOrderId { get; set; }

        [StringLength(50)]
        [Display(Name = "Customer Order Number")]
        public string? CustomerOrderNumber { get; set; }

        // Status Management
        [Required]
        [StringLength(20)]
        public string Status { get; set; } = "Draft"; // Draft, Scheduled, In Progress, Completed, Closed, Cancelled

        [Display(Name = "Start Date")]
        public DateTime? ActualStartDate { get; set; }

        [Display(Name = "Completion Date")]
        public DateTime? ActualCompletionDate { get; set; }

        [Display(Name = "Actual Quantity Produced")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? ActualQuantityProduced { get; set; }

        [Display(Name = "Actual Yield %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? ActualYieldPercent { get; set; }

        // Additional Information
        [StringLength(500)]
        public string? Remarks { get; set; }

        [StringLength(500)]
        [Display(Name = "Special Instructions")]
        public string? SpecialInstructions { get; set; }

        // Audit Fields
        [Display(Name = "Created Date")]
        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(100)]
        [Display(Name = "Created By")]
        public string? CreatedBy { get; set; }

        [Display(Name = "Modified Date")]
        public DateTime? ModifiedDate { get; set; }

        [StringLength(100)]
        [Display(Name = "Modified By")]
        public string? ModifiedBy { get; set; }

        [Display(Name = "Active")]
        public bool IsActive { get; set; } = true;

        // Computed Properties
        [NotMapped]
        public string StatusBadgeClass => Status switch
        {
            "Draft" => "bg-secondary",
            "Scheduled" => "bg-info",
            "In Progress" => "bg-primary",
            "Completed" => "bg-success",
            "Closed" => "bg-dark",
            "Cancelled" => "bg-danger",
            _ => "bg-secondary"
        };

        [NotMapped]
        public string StatusIcon => Status switch
        {
            "Draft" => "fa-file",
            "Scheduled" => "fa-calendar-check",
            "In Progress" => "fa-cog fa-spin",
            "Completed" => "fa-check-circle",
            "Closed" => "fa-lock",
            "Cancelled" => "fa-times-circle",
            _ => "fa-circle"
        };

        [NotMapped]
        public string PriorityBadgeClass => Priority switch
        {
            "Urgent" => "bg-danger",
            "High" => "bg-warning",
            "Normal" => "bg-info",
            "Low" => "bg-secondary",
            _ => "bg-secondary"
        };

        [NotMapped]
        public bool IsOverdue
        {
            get
            {
                if (Status == "Scheduled" || Status == "In Progress")
                {
                    return ScheduledDate < DateTime.Now;
                }
                return false;
            }
        }

        [NotMapped]
        public int DaysToScheduled => (ScheduledDate - DateTime.Now).Days;

        [NotMapped]
        public string YieldVariance
        {
            get
            {
                if (ActualYieldPercent.HasValue && ExpectedYieldPercent.HasValue)
                {
                    var variance = ActualYieldPercent.Value - ExpectedYieldPercent.Value;
                    return variance > 0 ? $"+{variance:N2}%" : $"{variance:N2}%";
                }
                return "N/A";
            }
        }

        [NotMapped]
        public string YieldVarianceClass
        {
            get
            {
                if (ActualYieldPercent.HasValue && ExpectedYieldPercent.HasValue)
                {
                    var variance = ActualYieldPercent.Value - ExpectedYieldPercent.Value;
                    return variance >= 0 ? "text-success" : "text-danger";
                }
                return "text-muted";
            }
        }
    }
}
