using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using RMMS.Models.Masters;
using RMMS.Models.Inventory;

namespace RMMS.Models.Production
{
    public class BatchOutput
    {
        [Key]
        public int Id { get; set; }

        // Link to Production Batch
        [Required]
        [Display(Name = "Production Batch")]
        public int BatchId { get; set; }

        [ForeignKey(nameof(BatchId))]
        public virtual ProductionBatch? Batch { get; set; }

        // Output Information
        [Required]
        [StringLength(50)]
        [Display(Name = "Output Type")]
        public string OutputType { get; set; } = "Rice"; // Rice, Bran, Husk, Broken Rice

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [ForeignKey(nameof(ProductId))]
        public virtual Product? Product { get; set; }

        [StringLength(50)]
        [Display(Name = "Grade/Quality")]
        public string? Grade { get; set; } // Premium, Grade A, Grade B, Super Fine, Fine, Medium, Coarse (for broken)

        [Required]
        [Display(Name = "Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal Quantity { get; set; }

        [Required]
        [StringLength(10)]
        [Display(Name = "UOM")]
        public string UOM { get; set; } = "Quintals";

        // Destination Warehouse/Zone
        [Required]
        [Display(Name = "Destination Warehouse")]
        public int WarehouseId { get; set; }

        [ForeignKey(nameof(WarehouseId))]
        public virtual Warehouse? Warehouse { get; set; }

        [Display(Name = "Destination Zone")]
        public int? ZoneId { get; set; }

        [ForeignKey(nameof(ZoneId))]
        public virtual StorageZone? Zone { get; set; }

        // Quality Information
        [Display(Name = "Quality Score")]
        [Column(TypeName = "decimal(3,1)")]
        public decimal? QualityScore { get; set; } // 1-10 scale

        [Display(Name = "Moisture Content %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? MoistureContent { get; set; }

        [StringLength(50)]
        [Display(Name = "Batch/Lot Number")]
        public string? BatchLotNumber { get; set; }

        // Costing/Valuation
        [Display(Name = "Unit Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UnitCost { get; set; }

        [Display(Name = "Total Value")]
        [NotMapped]
        public decimal TotalValue => Quantity * UnitCost;

        // Packaging Information (optional)
        [Display(Name = "Bags Count")]
        public int? BagsCount { get; set; }

        [Display(Name = "Bags Weight (kg)")]
        [Column(TypeName = "decimal(8,2)")]
        public decimal? BagsWeight { get; set; }

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
        public string DisplayName => $"{Product?.ProductName} {Grade} - {Quantity:N2} {UOM}";

        [NotMapped]
        public string DestinationLocation
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

        [NotMapped]
        public string OutputTypeBadgeClass => OutputType switch
        {
            "Rice" => "bg-success",
            "Broken Rice" => "bg-warning",
            "Bran" => "bg-info",
            "Husk" => "bg-secondary",
            _ => "bg-secondary"
        };

        [NotMapped]
        public string OutputTypeIcon => OutputType switch
        {
            "Rice" => "fa-seedling",
            "Broken Rice" => "fa-layer-group",
            "Bran" => "fa-cube",
            "Husk" => "fa-layer-group",
            _ => "fa-box"
        };
    }
}
