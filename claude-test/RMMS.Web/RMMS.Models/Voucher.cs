using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class Voucher
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Voucher Date")]
        [DataType(DataType.Date)]
        public DateTime VoucherDate { get; set; }

        [Required]
        [Display(Name = "Voucher Number")]
        [StringLength(50)]
        public string? VoucherNumber { get; set; }

        [Required]
        [Display(Name = "Voucher Type")]
        [StringLength(20)]
        public string? VoucherType { get; set; } // Payment, Receipt, Journal, Contra

        [Required]
        [Display(Name = "Particulars/Description")]
        [StringLength(1000)]
        public string? Particulars { get; set; }

        [Required]
        [Display(Name = "Amount")]
        [Range(0.01, double.MaxValue)]
        public decimal Amount { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public string? CreatedBy { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}