using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Sales
{
    [Table("QuotationItems")]
    public class QuotationItem
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [Display(Name = "Quotation")]
        public int QuotationId { get; set; }

        [ForeignKey("QuotationId")]
        public virtual Quotation? Quotation { get; set; }

        [Required]
        [Display(Name = "Product")]
        public int ProductId { get; set; }

        [ForeignKey("ProductId")]
        public virtual RMMS.Models.Masters.Product? Product { get; set; }

        [StringLength(200)]
        [Display(Name = "Product Description")]
        public string? ProductDescription { get; set; }

        [Required]
        [Display(Name = "Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal Quantity { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Unit of Measure")]
        public string UnitOfMeasure { get; set; } = "Quintals";

        [Required]
        [Display(Name = "Unit Price")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal UnitPrice { get; set; }

        [Display(Name = "Discount %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? DiscountPercent { get; set; }

        [Display(Name = "Discount Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? DiscountAmount { get; set; }

        [Display(Name = "Tax %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? TaxPercent { get; set; }

        [Display(Name = "Tax Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? TaxAmount { get; set; }

        [Display(Name = "Total Amount")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalAmount { get; set; }

        [StringLength(200)]
        [Display(Name = "Remarks")]
        public string? Remarks { get; set; }

        [NotMapped]
        [Display(Name = "Line Total")]
        public decimal LineTotal => Quantity * UnitPrice - (DiscountAmount ?? 0) + (TaxAmount ?? 0);
    }
}
