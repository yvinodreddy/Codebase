// RMMS.Models/BankTransactions.cs
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class BankTransactions
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Transaction Date")]
        [DataType(DataType.Date)]
        public DateTime TransactionDate { get; set; }

        [Display(Name = "Cheque/UTR Number")]
        [StringLength(100)]
        public string? ChequeUTRNumber { get; set; }

        [Required]
        [Display(Name = "Bank Name")]
        [StringLength(200)]
        public string? BankName { get; set; }

        [Required]
        [Display(Name = "Account Number")]
        [StringLength(50)]
        public string? AccountNumber { get; set; }

        [Required]
        [Display(Name = "Particulars")]
        [StringLength(500)]
        public string? Particulars { get; set; }

        [Display(Name = "Deposits")]
        [Range(0, double.MaxValue)]
        public decimal Deposits { get; set; }

        [Display(Name = "Withdrawals")]
        [Range(0, double.MaxValue)]
        public decimal Withdrawals { get; set; }

        [Required]
        [Display(Name = "Balance")]
        public decimal Balance { get; set; }

        [Display(Name = "Transaction Type")]
        [StringLength(50)]
        public string? TransactionType { get; set; }

        [Display(Name = "Reconciliation Status")]
        [StringLength(50)]
        public string? ReconciliationStatus { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? CreatedBy { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; }
    }
}