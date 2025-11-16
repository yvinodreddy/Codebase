using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Inventory
{
    [Table("StorageZones")]
    public class StorageZone
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int WarehouseId { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Zone Code")]
        public string ZoneCode { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        [Display(Name = "Zone Name")]
        public string ZoneName { get; set; } = string.Empty;

        [StringLength(50)]
        [Display(Name = "Zone Type")]
        public string? ZoneType { get; set; } // Rice Section, Paddy Section, By-Products, Packaging, Other

        [Display(Name = "Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal Capacity { get; set; }

        [Display(Name = "Used Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UsedCapacity { get; set; }

        [Display(Name = "Available Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal AvailableCapacity { get; set; }

        [Display(Name = "Temperature (°C)")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? Temperature { get; set; }

        [Display(Name = "Humidity (%)")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? Humidity { get; set; }

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Full, Maintenance

        [StringLength(200)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        // Navigation property
        [ForeignKey("WarehouseId")]
        public virtual Warehouse? Warehouse { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
