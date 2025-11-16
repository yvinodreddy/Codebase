using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class PayableOverdue
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Purchase Date")]
        [DataType(DataType.Date)]
        public DateTime PurchaseDate { get; set; }

        [Required]
        [Display(Name = "Invoice Number")]
        [StringLength(50)]
        public string? InvoiceNumber { get; set; }

        [Required]
        [Display(Name = "Supplier Name")]
        [StringLength(200)]
        public string? SupplierName { get; set; }

        [Required]
        [Display(Name = "Item Purchased")]
        [StringLength(500)]
        public string? ItemPurchased { get; set; }

        [Required]
        [Display(Name = "Invoice Amount")]
        [Range(0.01, double.MaxValue)]
        public decimal InvoiceAmount { get; set; }

        [Display(Name = "Amount Paid")]
        [Range(0, double.MaxValue)]
        public decimal AmountPaid { get; set; }

        [Display(Name = "Balance Payable")]
        public decimal BalancePayable { get; set; }

        [Required]
        [Display(Name = "Due Date")]
        [DataType(DataType.Date)]
        public DateTime DueDate { get; set; }

        [Display(Name = "Days Overdue")]
        public int DaysOverdue
        {
            get
            {
                if (DateTime.Today > DueDate && BalancePayable > 0)
                    return (DateTime.Today - DueDate).Days;
                return 0;
            }
        }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        public DateTime CreatedDate { get; set; }
        public bool IsActive { get; set; } = true;
    }
}