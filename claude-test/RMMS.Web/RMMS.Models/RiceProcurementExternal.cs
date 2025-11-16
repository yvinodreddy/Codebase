using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class RiceProcurementExternal
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Date")]
        [DataType(DataType.Date)]
        public DateTime Date { get; set; }

        [Required]
        [Display(Name = "Item Description")]
        [StringLength(200)]
        public string? ItemDescription { get; set; } // Mansuri, Katrni, Sonam, etc.

        [Required]
        [Display(Name = "Procured From")]
        [StringLength(200)]
        public string? ProcuredFrom { get; set; } // Shopkeeper/Rice Mill name

        [Required]
        [Display(Name = "Procured By")]
        [StringLength(100)]
        public string? ProcuredBy { get; set; } // Employee name

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
        public string? PaymentMode { get; set; } // Cash/Online

        [Display(Name = "Payment Status")]
        [StringLength(20)]
        public string? PaymentStatus { get; set; }

        [Display(Name = "Balance Amount")]
        public decimal Balance { get; set; }

        [Display(Name = "Date of Full Payment")]
        [DataType(DataType.Date)]
        public DateTime? FullPaymentDate { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}