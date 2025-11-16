using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;
using RMMS.Models.Inventory;

namespace RMMS.Models.Production
{
    public class BatchInput
    {
        [Key]
        public int Id { get; set; }

        // Link to Production Batch
        [Required]
        [Display(Name = "Production Batch")]
        public int BatchId { get; set; }

        [ForeignKey(nameof(BatchId))]
        public virtual ProductionBatch? Batch { get; set; }

        // Input Information
        [Required]
        [StringLength(50)]
        [Display(Name = "Input Type")]
        public string InputType { get; set; } = "Paddy"; // Paddy (main), Water, Energy, etc.

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [ForeignKey(nameof(ProductId))]
        public virtual Product? Product { get; set; }

        [Required]
        [Display(Name = "Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal Quantity { get; set; }

        [Required]
        [StringLength(10)]
        [Display(Name = "UOM")]
        public string UOM { get; set; } = "Quintals";

        // Source Warehouse/Zone
        [Required]
        [Display(Name = "Source Warehouse")]
        public int WarehouseId { get; set; }

        [ForeignKey(nameof(WarehouseId))]
        public virtual Warehouse? Warehouse { get; set; }

        [Display(Name = "Source Zone")]
        public int? ZoneId { get; set; }

        [ForeignKey(nameof(ZoneId))]
        public virtual StorageZone? Zone { get; set; }

        // Quality Information
        [Display(Name = "Moisture Content %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? MoistureContent { get; set; }

        [StringLength(50)]
        [Display(Name = "Batch/Lot Number")]
        public string? BatchLotNumber { get; set; }

        [StringLength(50)]
        [Display(Name = "Grade/Quality")]
        public string? Grade { get; set; }

        // Costing
        [Display(Name = "Unit Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UnitCost { get; set; }

        [Display(Name = "Total Cost")]
        [NotMapped]
        public decimal TotalCost => Quantity * UnitCost;

        // Additional Information
        [StringLength(500)]
        public string? Remarks { get; set; }

        // Audit Fields
        [Display(Name = "Created Date")]
        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(100)]
        [Display(Name = "Created By")]
        public string? CreatedBy { get; set; }

        // Computed Properties
        [NotMapped]
        public string DisplayName => $"{Product?.ProductName} - {Quantity:N2} {UOM}";

        [NotMapped]
        public string SourceLocation
        {
            get
            {
                if (Zone != null)
                {
                    return $"{Warehouse?.WarehouseName} - {Zone.ZoneName}";
                }
                return Warehouse?.WarehouseName ?? "Unknown";
            }
        }
    }
}
