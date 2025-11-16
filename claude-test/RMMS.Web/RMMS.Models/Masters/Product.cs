using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Masters
{
    [Table("Products")]
    public class Product
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Product Code")]
        public string ProductCode { get; set; } = string.Empty;

        [Required]
        [StringLength(200)]
        [Display(Name = "Product Name")]
        public string ProductName { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        [Display(Name = "Product Category")]
        public string ProductCategory { get; set; } = string.Empty; // Rice, By-Product, Paddy

        [StringLength(100)]
        [Display(Name = "Product Type")]
        public string? ProductType { get; set; } // Basmati, Sona Masuri, Non-Basmati, Bran, Husk, etc.

        [StringLength(50)]
        [Display(Name = "Grade")]
        public string? Grade { get; set; } // A, B, C, Premium, Standard

        [StringLength(500)]
        [Display(Name = "Description")]
        public string? Description { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Unit of Measure")]
        public string UnitOfMeasure { get; set; } = "Kg"; // Kg, Quintal, Ton, Bag

        [Display(Name = "Unit Weight (Kg)")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? UnitWeight { get; set; } // For bags: 25kg, 50kg

        [Display(Name = "HSN Code")]
        [StringLength(12)]
        public string? HSNCode { get; set; }

        [Display(Name = "GST Rate (%)")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? GSTRate { get; set; }

        [Display(Name = "Standard Cost")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? StandardCost { get; set; }

        [Display(Name = "Selling Price")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? SellingPrice { get; set; }

        [Display(Name = "Minimum Stock Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? MinimumStockLevel { get; set; }

        [Display(Name = "Maximum Stock Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? MaximumStockLevel { get; set; }

        [Display(Name = "Reorder Level")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? ReorderLevel { get; set; }

        [StringLength(100)]
        [Display(Name = "Storage Location")]
        public string? StorageLocation { get; set; }

        [Display(Name = "Shelf Life (Days)")]
        public int? ShelfLifeDays { get; set; }

        [StringLength(50)]
        [Display(Name = "Packaging Type")]
        public string? PackagingType { get; set; } // Jute Bag, PP Bag, Bulk, etc.

        [Display(Name = "Is Raw Material")]
        public bool IsRawMaterial { get; set; } // true for Paddy

        [Display(Name = "Is Finished Product")]
        public bool IsFinishedProduct { get; set; } // true for Rice

        [Display(Name = "Is By-Product")]
        public bool IsByProduct { get; set; } // true for Bran, Husk

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Discontinued

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
