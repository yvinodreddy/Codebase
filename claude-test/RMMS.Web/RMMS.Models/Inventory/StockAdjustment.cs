using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;

namespace RMMS.Models.Inventory
{
    [Table("StockAdjustments")]
    public class StockAdjustment
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Adjustment Code")]
        public string AdjustmentCode { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [Required]
        [Display(Name = "Warehouse")]
        public int WarehouseId { get; set; }

        [Display(Name = "Storage Zone")]
        public int? ZoneId { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Adjustment Type")]
        public string AdjustmentType { get; set; } = string.Empty; // Increase, Decrease, Transfer

        [Required]
        [Display(Name = "Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal Quantity { get; set; }

        [Required]
        [StringLength(50)]
        [Display(Name = "Reason")]
        public string Reason { get; set; } = string.Empty;
        // Damage, Theft, Spoilage, Counting Error, Physical Verification, Other

        [Display(Name = "Before Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal BeforeQuantity { get; set; }

        [Display(Name = "After Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal AfterQuantity { get; set; }

        [Required]
        [Display(Name = "Adjustment Date")]
        public DateTime AdjustmentDate { get; set; } = DateTime.Now;

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        [Display(Name = "Requires Approval")]
        public bool RequiresApproval { get; set; } = true;

        [Display(Name = "Approved")]
        public bool IsApproved { get; set; } = false;

        [StringLength(100)]
        [Display(Name = "Approved By")]
        public string? ApprovedBy { get; set; }

        [Display(Name = "Approval Date")]
        public DateTime? ApprovalDate { get; set; }

        [StringLength(500)]
        [Display(Name = "Approval Remarks")]
        public string? ApprovalRemarks { get; set; }

        [Display(Name = "Rejected")]
        public bool IsRejected { get; set; } = false;

        [StringLength(500)]
        [Display(Name = "Rejection Reason")]
        public string? RejectionReason { get; set; }

        // Navigation properties
        [ForeignKey("ProductId")]
        public virtual Product? Product { get; set; }

        [ForeignKey("WarehouseId")]
        public virtual Warehouse? Warehouse { get; set; }

        [ForeignKey("ZoneId")]
        public virtual StorageZone? Zone { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;

        // Calculated properties
        [NotMapped]
        public decimal AdjustmentAmount => AfterQuantity - BeforeQuantity;

        [NotMapped]
        public string AdjustmentTypeDisplay
        {
            get
            {
                return AdjustmentType switch
                {
                    "Increase" => "Stock Increase",
                    "Decrease" => "Stock Decrease",
                    "Transfer" => "Stock Transfer",
                    _ => AdjustmentType
                };
            }
        }

        [NotMapped]
        public string StatusDisplay
        {
            get
            {
                if (IsRejected) return "Rejected";
                if (IsApproved) return "Approved";
                if (RequiresApproval) return "Pending Approval";
                return "Draft";
            }
        }

        [NotMapped]
        public string StatusBadgeClass
        {
            get
            {
                if (IsRejected) return "bg-danger";
                if (IsApproved) return "bg-success";
                if (RequiresApproval) return "bg-warning";
                return "bg-secondary";
            }
        }

        [NotMapped]
        public string AdjustmentIcon
        {
            get
            {
                return AdjustmentType switch
                {
                    "Increase" => "fa-arrow-up",
                    "Decrease" => "fa-arrow-down",
                    "Transfer" => "fa-exchange-alt",
                    _ => "fa-edit"
                };
            }
        }
    }
}
