using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;

namespace RMMS.Models.Production
{
    public class ProductionBatch
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Batch Number")]
        public string BatchNumber { get; set; } = string.Empty;

        // Link to Production Order
        [Display(Name = "Production Order")]
        public int? ProductionOrderId { get; set; }

        [ForeignKey(nameof(ProductionOrderId))]
        public virtual ProductionOrder? ProductionOrder { get; set; }

        // Batch Information
        [Required]
        [Display(Name = "Batch Date")]
        [DataType(DataType.Date)]
        public DateTime BatchDate { get; set; } = DateTime.Now;

        [Required]
        [StringLength(20)]
        [Display(Name = "Shift Type")]
        public string ShiftType { get; set; } = "Morning"; // Morning, Evening, Night

        // Personnel
        [Display(Name = "Operator")]
        public int? OperatorId { get; set; }

        [ForeignKey(nameof(OperatorId))]
        public virtual Employee? Operator { get; set; }

        [Display(Name = "Supervisor")]
        public int? SupervisorId { get; set; }

        [ForeignKey(nameof(SupervisorId))]
        public virtual Employee? Supervisor { get; set; }

        // Timing
        [Display(Name = "Start Time")]
        public DateTime? StartTime { get; set; }

        [Display(Name = "End Time")]
        public DateTime? EndTime { get; set; }

        [NotMapped]
        [Display(Name = "Duration (Hours)")]
        public decimal? DurationHours
        {
            get
            {
                if (StartTime.HasValue && EndTime.HasValue)
                {
                    return (decimal)(EndTime.Value - StartTime.Value).TotalHours;
                }
                return null;
            }
        }

        // Status Management
        [Required]
        [StringLength(20)]
        public string Status { get; set; } = "Planned"; // Planned, In Progress, Completed, Verified, Cancelled

        [Display(Name = "Completion %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal CompletionPercent { get; set; } = 0;

        // Quality Information
        [Display(Name = "Quality Score")]
        [Column(TypeName = "decimal(3,1)")]
        public decimal? QualityScore { get; set; } // 1-10 scale

        [StringLength(500)]
        [Display(Name = "Quality Remarks")]
        public string? QualityRemarks { get; set; }

        // Additional Information
        [StringLength(500)]
        public string? Remarks { get; set; }

        [StringLength(500)]
        [Display(Name = "Issues/Problems")]
        public string? Issues { get; set; }

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

        // Navigation Properties
        public virtual ICollection<BatchInput> Inputs { get; set; } = new List<BatchInput>();
        public virtual ICollection<BatchOutput> Outputs { get; set; } = new List<BatchOutput>();
        public virtual YieldRecord? YieldRecord { get; set; }

        // Computed Properties
        [NotMapped]
        public string StatusBadgeClass => Status switch
        {
            "Planned" => "bg-secondary",
            "In Progress" => "bg-primary",
            "Completed" => "bg-success",
            "Verified" => "bg-info",
            "Cancelled" => "bg-danger",
            _ => "bg-secondary"
        };

        [NotMapped]
        public string StatusIcon => Status switch
        {
            "Planned" => "fa-calendar",
            "In Progress" => "fa-cog fa-spin",
            "Completed" => "fa-check-circle",
            "Verified" => "fa-check-double",
            "Cancelled" => "fa-times-circle",
            _ => "fa-circle"
        };

        [NotMapped]
        public string ShiftBadgeClass => ShiftType switch
        {
            "Morning" => "bg-warning",
            "Evening" => "bg-info",
            "Night" => "bg-dark",
            _ => "bg-secondary"
        };

        [NotMapped]
        public decimal TotalInputQuantity
        {
            get
            {
                decimal total = 0;
                foreach (var input in Inputs)
                {
                    total += input.Quantity;
                }
                return total;
            }
        }

        [NotMapped]
        public decimal TotalOutputQuantity
        {
            get
            {
                decimal total = 0;
                foreach (var output in Outputs)
                {
                    total += output.Quantity;
                }
                return total;
            }
        }

        [NotMapped]
        public decimal TotalInputCost
        {
            get
            {
                decimal total = 0;
                foreach (var input in Inputs)
                {
                    total += input.TotalCost;
                }
                return total;
            }
        }

        [NotMapped]
        public decimal TotalOutputValue
        {
            get
            {
                decimal total = 0;
                foreach (var output in Outputs)
                {
                    total += output.TotalValue;
                }
                return total;
            }
        }
    }
}
