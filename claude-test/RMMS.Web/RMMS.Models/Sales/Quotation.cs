using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Sales
{
    [Table("Quotations")]
    public class Quotation
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Quotation Number")]
        public string QuotationNumber { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Quotation Date")]
        public DateTime QuotationDate { get; set; } = DateTime.Now;

        [Display(Name = "Inquiry")]
        public int? InquiryId { get; set; }

        [ForeignKey("InquiryId")]
        public virtual Inquiry? Inquiry { get; set; }

        [Required]
        [Display(Name = "Customer")]
        public int CustomerId { get; set; }

        [ForeignKey("CustomerId")]
        public virtual RMMS.Models.Masters.Customer? Customer { get; set; }

        [Required]
        [Display(Name = "Valid Until")]
        public DateTime ValidUntil { get; set; }

        [StringLength(100)]
        [Display(Name = "Payment Terms")]
        public string? PaymentTerms { get; set; } // Advance, 30 Days, 60 Days, etc.

        [StringLength(100)]
        [Display(Name = "Delivery Terms")]
        public string? DeliveryTerms { get; set; } // Ex-Works, FOB, CIF, etc.

        [Display(Name = "Subtotal Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal SubtotalAmount { get; set; }

        [Display(Name = "Discount %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? DiscountPercent { get; set; }

        [Display(Name = "Discount Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? DiscountAmount { get; set; }

        [Display(Name = "Tax Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TaxAmount { get; set; }

        [Display(Name = "Total Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalAmount { get; set; }

        [StringLength(50)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Draft"; // Draft, Sent, Accepted, Rejected, Expired, Converted

        [Display(Name = "Approved By")]
        public int? ApprovedByEmployeeId { get; set; }

        [ForeignKey("ApprovedByEmployeeId")]
        public virtual RMMS.Models.Masters.Employee? ApprovedByEmployee { get; set; }

        [Display(Name = "Approval Date")]
        public DateTime? ApprovalDate { get; set; }

        [Display(Name = "Converted to Sales Order")]
        public int? ConvertedToSalesOrderId { get; set; }

        [StringLength(500)]
        [Display(Name = "Terms and Conditions")]
        public string? TermsAndConditions { get; set; }

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        // Navigation property
        public virtual ICollection<QuotationItem> QuotationItems { get; set; } = new List<QuotationItem>();

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
