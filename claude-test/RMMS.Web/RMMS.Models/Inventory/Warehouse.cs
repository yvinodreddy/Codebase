using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Inventory
{
    [Table("Warehouses")]
    public class Warehouse
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Warehouse Code")]
        public string WarehouseCode { get; set; } = string.Empty;

        [Required]
        [StringLength(200)]
        [Display(Name = "Warehouse Name")]
        public string WarehouseName { get; set; } = string.Empty;

        [StringLength(200)]
        [Display(Name = "Location")]
        public string? Location { get; set; }

        [StringLength(500)]
        [Display(Name = "Address")]
        public string? Address { get; set; }

        [StringLength(100)]
        [Display(Name = "City")]
        public string? City { get; set; }

        [StringLength(100)]
        [Display(Name = "State")]
        public string? State { get; set; }

        [StringLength(10)]
        [Display(Name = "Pincode")]
        public string? Pincode { get; set; }

        [Display(Name = "Total Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalCapacity { get; set; }

        [Display(Name = "Used Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UsedCapacity { get; set; }

        [Display(Name = "Available Capacity (MT)")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal AvailableCapacity { get; set; }

        [StringLength(100)]
        [Display(Name = "Contact Person")]
        public string? ContactPerson { get; set; }

        [StringLength(15)]
        [Display(Name = "Mobile")]
        public string? Mobile { get; set; }

        [StringLength(100)]
        [EmailAddress]
        [Display(Name = "Email")]
        public string? Email { get; set; }

        [StringLength(50)]
        [Display(Name = "Warehouse Type")]
        public string? WarehouseType { get; set; } // Main Godown, Sub Godown, Open Storage, Cold Storage

        [Display(Name = "Temperature Controlled")]
        public bool IsTemperatureControlled { get; set; }

        [Display(Name = "Temperature (°C)")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? Temperature { get; set; }

        [Display(Name = "Humidity (%)")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? Humidity { get; set; }

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Maintenance, Full

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        // Navigation property
        public virtual ICollection<StorageZone>? Zones { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
