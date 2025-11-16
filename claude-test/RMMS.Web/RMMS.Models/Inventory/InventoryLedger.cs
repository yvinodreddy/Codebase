using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;

namespace RMMS.Models.Inventory
{
    [Table("InventoryLedger")]
    public class InventoryLedger
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [Required]
        [Display(Name = "Warehouse")]
        public int WarehouseId { get; set; }

        [Display(Name = "Storage Zone")]
        public int? ZoneId { get; set; }

        [Display(Name = "Current Stock")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal CurrentStock { get; set; }

        [Display(Name = "Minimum Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal MinimumLevel { get; set; }

        [Display(Name = "Maximum Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal MaximumLevel { get; set; }

        [Display(Name = "Reorder Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal ReorderLevel { get; set; }

        [Display(Name = "Unit Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UnitCost { get; set; }

        [Display(Name = "Total Value")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalValue { get; set; }

        [Display(Name = "Last Movement Date")]
        public DateTime? LastMovementDate { get; set; }

        [Display(Name = "Last Updated")]
        public DateTime LastUpdated { get; set; } = DateTime.Now;

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

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
        public decimal AvailableStock => CurrentStock;

        [NotMapped]
        public bool IsLowStock => CurrentStock <= MinimumLevel;

        [NotMapped]
        public bool IsOverStock => CurrentStock >= MaximumLevel;

        [NotMapped]
        public bool NeedsReorder => CurrentStock <= ReorderLevel;

        [NotMapped]
        public decimal UtilizationPercentage => MaximumLevel > 0 ? (CurrentStock / MaximumLevel) * 100 : 0;

        [NotMapped]
        public string StockStatus
        {
            get
            {
                if (CurrentStock <= 0) return "Out of Stock";
                if (IsLowStock) return "Low Stock";
                if (IsOverStock) return "Overstock";
                if (NeedsReorder) return "Reorder Required";
                return "Normal";
            }
        }
    }
}
