// RMMS.Models/PaddyProcurement.cs
using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models
{
    public class PaddyProcurement
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Receipt date is required")]
        [Display(Name = "Receipt Date")]
        [DataType(DataType.Date)]
        public DateTime ReceiptDate { get; set; }

        [Required(ErrorMessage = "Voucher number is required")]
        [Display(Name = "Voucher Number")]
        [StringLength(50)]
        public string? VoucherNumber { get; set; }

        [Required(ErrorMessage = "Supplier name is required")]
        [Display(Name = "Supplier Name")]
        [StringLength(200)]
        public string? SupplierName { get; set; }

        [Display(Name = "Purchase Order Number")]
        [StringLength(50)]
        public string? PurchaseOrderNumber { get; set; }

        [Required(ErrorMessage = "Paddy variety is required")]
        [Display(Name = "Paddy Variety")]
        [StringLength(100)]
        public string? PaddyVariety { get; set; }

        [Display(Name = "Grade")]
        [StringLength(50)]
        public string? Grade { get; set; }

        [Display(Name = "Moisture Content (%)")]
        [Range(0, 100, ErrorMessage = "Moisture content must be between 0 and 100")]
        public decimal? MoistureContent { get; set; }

        [Required(ErrorMessage = "Quantity received is required")]
        [Display(Name = "Quantity Received")]
        [Range(0.001, double.MaxValue, ErrorMessage = "Quantity must be greater than 0")]
        public decimal QuantityReceived { get; set; }

        [Display(Name = "Weight Per Bag")]
        public decimal? WeightPerBag { get; set; }

        [Required(ErrorMessage = "Total net weight is required")]
        [Display(Name = "Total Net Weight")]
        [Range(0.001, double.MaxValue, ErrorMessage = "Weight must be greater than 0")]
        public decimal TotalNetWeight { get; set; }

        [Display(Name = "Storage Date")]
        [DataType(DataType.Date)]
        public DateTime? StorageDate { get; set; }

        [Display(Name = "Storage Location")]
        [StringLength(200)]
        public string? StorageLocation { get; set; }

        [Display(Name = "Opening Stock")]
        public decimal? OpeningStock { get; set; }

        [Display(Name = "Issues")]
        public decimal? Issues { get; set; }

        [Display(Name = "Closing Stock")]
        public decimal? ClosingStock { get; set; }

        [Display(Name = "Loss/Shrinkage")]
        public decimal? LossShrinkage { get; set; }

        [Display(Name = "Remarks")]
        [StringLength(500)]
        public string? Remarks { get; set; }

        [Display(Name = "Responsible Person")]
        [StringLength(100)]
        public string? ResponsiblePerson { get; set; }

        public DateTime CreatedDate { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? CreatedBy { get; set; }  // Add ? to make nullable
        public string? ModifiedBy { get; set; } // Add ? to make nullable
        public bool IsActive { get; set; }
    }
}

// Similar models for all other tables...