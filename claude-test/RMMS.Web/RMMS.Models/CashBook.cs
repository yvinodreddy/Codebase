using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class CashBook
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Transaction Date")]
        [DataType(DataType.Date)]
        public DateTime TransactionDate { get; set; }

        [Display(Name = "Voucher No/Transaction ID")]
        [StringLength(50)]
        public string? VoucherNumber { get; set; }

        [Required]
        [Display(Name = "Particulars/Description")]
        [StringLength(500)]
        public string? Particulars { get; set; }

        [Display(Name = "Receipts (₹)")]
        [Range(0, double.MaxValue)]
        public decimal Receipts { get; set; }

        [Display(Name = "Payments (₹)")]
        [Range(0, double.MaxValue)]
        public decimal Payments { get; set; }

        [Display(Name = "Balance (₹)")]
        public decimal Balance { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public string? CreatedBy { get; set; }
        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}