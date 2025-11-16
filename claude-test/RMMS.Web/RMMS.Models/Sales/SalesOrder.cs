using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Sales
{
    [Table("SalesOrders")]
    public class SalesOrder
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Order Number")]
        public string OrderNumber { get; set; } = string.Empty;

        [Required]
        [Display(Name = "Order Date")]
        public DateTime OrderDate { get; set; } = DateTime.Now;

        [Required]
        [Display(Name = "Customer")]
        public int CustomerId { get; set; }

        [ForeignKey("CustomerId")]
        public virtual RMMS.Models.Masters.Customer? Customer { get; set; }

        [Display(Name = "Quotation")]
        public int? QuotationId { get; set; }

        [ForeignKey("QuotationId")]
        public virtual Quotation? Quotation { get; set; }

        [Required]
        [Display(Name = "Delivery Date")]
        public DateTime DeliveryDate { get; set; }

        [StringLength(200)]
        [Display(Name = "Delivery Address")]
        public string? DeliveryAddress { get; set; }

        [StringLength(100)]
        [Display(Name = "Payment Terms")]
        public string? PaymentTerms { get; set; }

        [StringLength(100)]
        [Display(Name = "Delivery Terms")]
        public string? DeliveryTerms { get; set; }

        [Display(Name = "Subtotal Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal SubtotalAmount { get; set; }

        [Display(Name = "Discount Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? DiscountAmount { get; set; }

        [Display(Name = "Tax Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TaxAmount { get; set; }

        [Display(Name = "Freight Charges")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? FreightCharges { get; set; }

        [Display(Name = "Other Charges")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? OtherCharges { get; set; }

        [Display(Name = "Total Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalAmount { get; set; }

        [StringLength(50)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Pending"; // Pending, Confirmed, In Production, Ready to Ship, Shipped, Delivered, Cancelled

        [StringLength(50)]
        [Display(Name = "Priority")]
        public string Priority { get; set; } = "Normal"; // Low, Normal, High, Urgent

        [Display(Name = "Approved By")]
        public int? ApprovedByEmployeeId { get; set; }

        [ForeignKey("ApprovedByEmployeeId")]
        public virtual RMMS.Models.Masters.Employee? ApprovedByEmployee { get; set; }

        [Display(Name = "Approval Date")]
        public DateTime? ApprovalDate { get; set; }

        [Display(Name = "Stock Reserved")]
        public bool StockReserved { get; set; } = false;

        [Display(Name = "Stock Reserved Date")]
        public DateTime? StockReservedDate { get; set; }

        [StringLength(500)]
        [Display(Name = "Special Instructions")]
        public string? SpecialInstructions { get; set; }

        [StringLength(500)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        // Navigation properties
        public virtual ICollection<SalesOrderItem> SalesOrderItems { get; set; } = new List<SalesOrderItem>();

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
