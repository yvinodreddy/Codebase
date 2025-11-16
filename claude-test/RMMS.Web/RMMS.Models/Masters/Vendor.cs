using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Masters
{
    [Table("Vendors")]
    public class Vendor
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Vendor Code")]
        public string VendorCode { get; set; } = string.Empty;

        [Required]
        [StringLength(200)]
        [Display(Name = "Vendor Name")]
        public string VendorName { get; set; } = string.Empty;

        [StringLength(50)]
        [Display(Name = "Vendor Type")]
        public string? VendorType { get; set; } // Farmer, Trader, Commission Agent

        [StringLength(50)]
        [Display(Name = "Category")]
        public string? Category { get; set; }

        [StringLength(15)]
        [Display(Name = "GSTIN")]
        public string? GSTIN { get; set; }

        [StringLength(10)]
        [Display(Name = "PAN")]
        public string? PAN { get; set; }

        [StringLength(50)]
        [Display(Name = "Payment Terms")]
        public string? PaymentTerms { get; set; }

        [StringLength(100)]
        [Display(Name = "Bank Name")]
        public string? BankName { get; set; }

        [StringLength(20)]
        [Display(Name = "Bank Account Number")]
        public string? BankAccountNumber { get; set; }

        [StringLength(11)]
        [Display(Name = "IFSC Code")]
        public string? IFSCCode { get; set; }

        [Display(Name = "Rating")]
        [Range(1, 5)]
        public int? Rating { get; set; } // 1-5 stars

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Blocked

        // Navigation properties
        public virtual ICollection<VendorContact>? Contacts { get; set; }
        public virtual ICollection<VendorAddress>? Addresses { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }

    [Table("VendorContacts")]
    public class VendorContact
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int VendorId { get; set; }

        [Required]
        [StringLength(100)]
        public string ContactPerson { get; set; } = string.Empty;

        [StringLength(100)]
        public string? Designation { get; set; }

        [Required]
        [StringLength(15)]
        public string Mobile { get; set; } = string.Empty;

        [StringLength(100)]
        [EmailAddress]
        public string? Email { get; set; }

        public bool IsPrimary { get; set; }

        [ForeignKey("VendorId")]
        public virtual Vendor? Vendor { get; set; }
    }

    [Table("VendorAddresses")]
    public class VendorAddress
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int VendorId { get; set; }

        [Required]
        [StringLength(50)]
        public string AddressType { get; set; } = "Office";

        [Required]
        [StringLength(200)]
        public string AddressLine1 { get; set; } = string.Empty;

        [StringLength(200)]
        public string? AddressLine2 { get; set; }

        [Required]
        [StringLength(100)]
        public string City { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        public string State { get; set; } = string.Empty;

        [StringLength(50)]
        public string Country { get; set; } = "India";

        [Required]
        [StringLength(10)]
        public string Pincode { get; set; } = string.Empty;

        public bool IsDefault { get; set; }

        [ForeignKey("VendorId")]
        public virtual Vendor? Vendor { get; set; }
    }
}
