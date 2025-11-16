using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;

namespace RMMS.Models.Inventory
{
    [Table("StockMovements")]
    public class StockMovement
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Movement Code")]
        public string MovementCode { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [Required]
        [Display(Name = "Warehouse")]
        public int WarehouseId { get; set; }

        [Display(Name = "Storage Zone")]
        public int? ZoneId { get; set; }

        [Required]
        [StringLength(10)]
        [Display(Name = "Movement Type")]
        public string MovementType { get; set; } = string.Empty; // IN, OUT

        [Required]
        [StringLength(50)]
        [Display(Name = "Movement Category")]
        public string MovementCategory { get; set; } = string.Empty;
        // Procurement, Sales, Production, Transfer, Adjustment, Return

        [Required]
        [Display(Name = "Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal Quantity { get; set; }

        [Display(Name = "Unit Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UnitCost { get; set; }

        [Display(Name = "Total Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalCost { get; set; }

        [StringLength(50)]
        [Display(Name = "Reference Type")]
        public string? ReferenceType { get; set; } // PO, SO, Production, Transfer

        [Display(Name = "Reference ID")]
        public int? ReferenceId { get; set; }

        [StringLength(50)]
        [Display(Name = "Reference Number")]
        public string? ReferenceNumber { get; set; }

        [Required]
        [Display(Name = "Movement Date")]
        public DateTime MovementDate { get; set; } = DateTime.Now;

        [StringLength(100)]
        [Display(Name = "Performed By")]
        public string? PerformedBy { get; set; }

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        [Display(Name = "Approved")]
        public bool IsApproved { get; set; } = true;

        [StringLength(100)]
        [Display(Name = "Approved By")]
        public string? ApprovedBy { get; set; }

        [Display(Name = "Approval Date")]
        public DateTime? ApprovalDate { get; set; }

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
        public string MovementTypeDisplay => MovementType == "IN" ? "Stock IN" : "Stock OUT";

        [NotMapped]
        public string MovementIcon => MovementType == "IN" ? "fa-arrow-down" : "fa-arrow-up";

        [NotMapped]
        public string MovementBadgeClass => MovementType == "IN" ? "bg-success" : "bg-warning";
    }
}
