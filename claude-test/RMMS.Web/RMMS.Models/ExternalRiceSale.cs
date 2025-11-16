using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class ExternalRiceSale
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Date")]
        [DataType(DataType.Date)]
        public DateTime Date { get; set; }

        [Required]
        [Display(Name = "Item Description")]
        [StringLength(200)]
        public string? ItemDescription { get; set; }

        [Required]
        [Display(Name = "Sold To")]
        [StringLength(200)]
        public string? SoldTo { get; set; } // PACs name/local purchaser with GST

        [Required]
        [Display(Name = "Sold By")]
        [StringLength(100)]
        public string? SoldBy { get; set; } // Employee name

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

        [Display(Name = "Balance Amount")]
        public decimal Balance { get; set; }

        [Display(Name = "Date of Full Payment")]
        [DataType(DataType.Date)]
        public DateTime? FullPaymentClearanceDate { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}