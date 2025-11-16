using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class RiceSales
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Sale Date")]
        [DataType(DataType.Date)]
        public DateTime SaleDate { get; set; }

        [Required]
        [Display(Name = "Invoice/Challan No")]
        [StringLength(50)]
        public string? InvoiceNumber { get; set; }

        [Required]
        [Display(Name = "Buyer Name & Address")]
        [StringLength(200)]
        public string? BuyerName { get; set; }

        [Display(Name = "Buyer Address")]
        [StringLength(500)]
        public string? BuyerAddress { get; set; }

        [Display(Name = "Buyer GSTIN")]
        [StringLength(20)]
        public string? BuyerGSTIN { get; set; }

        [Required]
        [Display(Name = "Item/Grade of Rice")]
        [StringLength(100)]
        public string? RiceGrade { get; set; }

        [Required]
        [Display(Name = "Quantity (kg)")]
        [Range(0.01, double.MaxValue, ErrorMessage = "Quantity must be greater than 0")]
        public decimal Quantity { get; set; }

        [Required]
        [Display(Name = "Unit Price (₹ per kg)")]
        [Range(0.01, double.MaxValue)]
        public decimal UnitPrice { get; set; }

        [Display(Name = "Total Invoice Value")]
        public decimal TotalInvoiceValue { get; set; }

        [Display(Name = "Discount/Deduction")]
        public decimal Discount { get; set; }

        [Display(Name = "Taxable Value")]
        public decimal TaxableValue { get; set; }

        [Display(Name = "CGST Amount")]
        public decimal CGSTAmount { get; set; }

        [Display(Name = "SGST Amount")]
        public decimal SGSTAmount { get; set; }

        [Display(Name = "IGST Amount")]
        public decimal IGSTAmount { get; set; }

        [Display(Name = "Total Tax Amount")]
        public decimal TotalTaxAmount { get; set; }

        [Display(Name = "Freight/Transport Charges")]
        public decimal FreightCharges { get; set; }

        [Display(Name = "Other Charges")]
        public decimal OtherCharges { get; set; }

        [Display(Name = "Gross Invoice Amount")]
        public decimal GrossInvoiceAmount { get; set; }

        [Display(Name = "Payment Mode")]
        [StringLength(50)]
        public string? PaymentMode { get; set; }

        [Display(Name = "Due Date")]
        [DataType(DataType.Date)]
        public DateTime? DueDate { get; set; }

        [Display(Name = "Payment Status")]
        [StringLength(20)]
        public string? PaymentStatus { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        // Audit fields
        public string? CreatedBy { get; set; }
        public DateTime CreatedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}