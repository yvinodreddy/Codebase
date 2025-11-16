using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class ReceivableOverdue
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Invoice Date")]
        [DataType(DataType.Date)]
        public DateTime InvoiceDate { get; set; }

        [Required]
        [Display(Name = "Invoice Number")]
        [StringLength(50)]
        public string? InvoiceNumber { get; set; }

        [Required]
        [Display(Name = "Customer Name")]
        [StringLength(200)]
        public string? CustomerName { get; set; }

        [Required]
        [Display(Name = "Item Supplied")]
        [StringLength(500)]
        public string? ItemSupplied { get; set; }

        [Required]
        [Display(Name = "Invoice Amount")]
        [Range(0.01, double.MaxValue)]
        public decimal InvoiceAmount { get; set; }

        [Display(Name = "Amount Received")]
        [Range(0, double.MaxValue)]
        public decimal AmountReceived { get; set; }

        [Display(Name = "Balance Due")]
        public decimal BalanceDue { get; set; }

        [Required]
        [Display(Name = "Due Date")]
        [DataType(DataType.Date)]
        public DateTime DueDate { get; set; }

        [Display(Name = "Days Overdue")]
        public int DaysOverdue
        {
            get
            {
                if (DateTime.Today > DueDate && BalanceDue > 0)
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