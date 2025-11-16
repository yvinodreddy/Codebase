using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class FixedAsset
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Asset ID")]
        [StringLength(50)]
        public string? AssetId { get; set; }

        [Required]
        [Display(Name = "Date of Purchase")]
        [DataType(DataType.Date)]
        public DateTime PurchaseDate { get; set; }

        [Required]
        [Display(Name = "Asset Name")]
        [StringLength(200)]
        public string? AssetName { get; set; }

        [Display(Name = "Description")]
        [StringLength(500)]
        public string? Description { get; set; }

        [Required]
        [Display(Name = "Supplier")]
        [StringLength(200)]
        public string? Supplier { get; set; }

        [Required]
        [Display(Name = "Purchase Value (₹)")]
        [Range(0.01, double.MaxValue)]
        public decimal PurchaseValue { get; set; }

        [Display(Name = "Depreciation Rate (%)")]
        [Range(0, 100)]
        public decimal DepreciationRate { get; set; }

        [Display(Name = "Accumulated Depreciation")]
        public decimal AccumulatedDepreciation { get; set; }

        [Display(Name = "Net Book Value")]
        public decimal NetBookValue { get; set; }

        [Display(Name = "Present Value (Approx)")]
        public decimal PresentValueApprox { get; set; }

        [Display(Name = "Status")]
        [StringLength(50)]
        public string? Status { get; set; } // Active, Sold, Scrapped

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}