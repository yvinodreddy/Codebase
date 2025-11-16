using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class ByProductSales
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Sale Date")]
        [DataType(DataType.Date)]
        public DateTime SaleDate { get; set; }

        [Display(Name = "Transaction Number")]
        [StringLength(50)]
        public string? TransactionNumber { get; set; }

        [Required]
        [Display(Name = "Product Type")]
        [StringLength(100)]
        public string? ProductType { get; set; } // Bran, Husk, Broken Rice, etc.

        [Required]
        [Display(Name = "Buyer Name")]
        [StringLength(200)]
        public string? BuyerName { get; set; }

        [Display(Name = "Buyer Contact")]
        [StringLength(20)]
        public string? BuyerContact { get; set; }

        [Required]
        [Display(Name = "Quantity (kg)")]
        [Range(0.01, double.MaxValue)]
        public decimal Quantity { get; set; }

        [Required]
        [Display(Name = "Rate per kg")]
        [Range(0.01, double.MaxValue)]
        public decimal Rate { get; set; }

        [Display(Name = "Total Amount")]
        public decimal TotalAmount { get; set; }

        [Display(Name = "Payment Mode")]
        [StringLength(50)]
        public string? PaymentMode { get; set; }

        [Display(Name = "Payment Status")]
        [StringLength(20)]
        public string? PaymentStatus { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        // Audit fields - these were missing and causing your errors
        [Display(Name = "Created By")]
        [StringLength(100)]
        public string? CreatedBy { get; set; }

        [Display(Name = "Created Date")]
        public DateTime CreatedDate { get; set; }

        [Display(Name = "Modified By")]
        [StringLength(100)]
        public string? ModifiedBy { get; set; }

        [Display(Name = "Modified Date")]
        public DateTime? ModifiedDate { get; set; }

        [Display(Name = "Is Active")]
        public bool IsActive { get; set; } = true;
    }
}