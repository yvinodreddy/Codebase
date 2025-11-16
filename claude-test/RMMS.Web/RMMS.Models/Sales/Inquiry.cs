using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Sales
{
    [Table("Inquiries")]
    public class Inquiry
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Inquiry Number")]
        public string InquiryNumber { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Inquiry Date")]
        public DateTime InquiryDate { get; set; } = DateTime.Now;

        [Required]
        [Display(Name = "Customer")]
        public int CustomerId { get; set; }

        [ForeignKey("CustomerId")]
        public virtual RMMS.Models.Masters.Customer? Customer { get; set; }

        [Required]
        [StringLength(50)]
        [Display(Name = "Source")]
        public string Source { get; set; } = string.Empty; // Phone, Email, Walk-in, Website, Referral

        [StringLength(100)]
        [Display(Name = "Product Type")]
        public string? ProductType { get; set; } // Basmati, Non-Basmati, Broken Rice, etc.

        [Display(Name = "Approximate Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal? ApproximateQuantity { get; set; }

        [StringLength(20)]
        [Display(Name = "Unit of Measure")]
        public string? UnitOfMeasure { get; set; } = "Quintals";

        [Display(Name = "Expected Delivery Date")]
        public DateTime? ExpectedDeliveryDate { get; set; }

        [StringLength(50)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "New"; // New, In Progress, Quoted, Converted, Lost, Closed

        [Display(Name = "Assigned To")]
        public int? AssignedToEmployeeId { get; set; }

        [ForeignKey("AssignedToEmployeeId")]
        public virtual RMMS.Models.Masters.Employee? AssignedToEmployee { get; set; }

        [StringLength(50)]
        [Display(Name = "Priority")]
        public string Priority { get; set; } = "Normal"; // Low, Normal, High, Urgent

        [StringLength(1000)]
        [Display(Name = "Customer Requirements")]
        public string? CustomerRequirements { get; set; }

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        [Display(Name = "Follow-up Date")]
        public DateTime? FollowUpDate { get; set; }

        [StringLength(50)]
        [Display(Name = "Lost Reason")]
        public string? LostReason { get; set; } // Price, Quality, Delivery Time, Competition, etc.

        [Display(Name = "Converted to Quotation")]
        public int? ConvertedToQuotationId { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
