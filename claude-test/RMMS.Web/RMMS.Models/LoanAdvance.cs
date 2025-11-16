using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class LoanAdvance
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Date")]
        [DataType(DataType.Date)]
        public DateTime Date { get; set; }

        [Display(Name = "Voucher Number")]
        [StringLength(50)]
        public string? VoucherNumber { get; set; }

        [Required]
        [Display(Name = "Particulars")]
        [StringLength(500)]
        public string? Particulars { get; set; }

        [Required]
        [Display(Name = "Name of Party/Employee")]
        [StringLength(200)]
        public string? PartyName { get; set; }

        [Required]
        [Display(Name = "Amount Given")]
        [Range(0.01, double.MaxValue)]
        public decimal AmountGiven { get; set; }

        [Display(Name = "Repayment Amount")]
        [Range(0, double.MaxValue)]
        public decimal Repayment { get; set; }

        [Display(Name = "Date of Repayment")]
        [DataType(DataType.Date)]
        public DateTime? RepaymentDate { get; set; }

        [Display(Name = "Balance")]
        public decimal Balance { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}