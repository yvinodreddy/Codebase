using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class BankTransaction
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Transaction Date")]
        [DataType(DataType.Date)]
        public DateTime TransactionDate { get; set; }

        [Display(Name = "Cheque/UTR No")]
        [StringLength(50)]
        public string? ChequeUtrNumber { get; set; }

        [Required]
        [Display(Name = "Bank Name")]
        [StringLength(100)]
        public string? BankName { get; set; }

        [Required]
        [Display(Name = "Account Number")]
        [StringLength(50)]
        public string? AccountNumber { get; set; }

        [Required]
        [Display(Name = "Particulars")]
        [StringLength(500)]
        public string? Particulars { get; set; }

        [Display(Name = "Deposits (₹)")]
        [Range(0, double.MaxValue)]
        public decimal Deposits { get; set; }

        [Display(Name = "Withdrawals (₹)")]
        [Range(0, double.MaxValue)]
        public decimal Withdrawals { get; set; }

        [Display(Name = "Balance (₹)")]
        public decimal Balance { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}