using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Masters
{
    [Table("Customers")]
    public class Customer
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Customer Code")]
        public string CustomerCode { get; set; } = string.Empty;

        [Required]
        [StringLength(200)]
        [Display(Name = "Customer Name")]
        public string CustomerName { get; set; } = string.Empty;

        [StringLength(50)]
        [Display(Name = "Customer Type")]
        public string? CustomerType { get; set; } // Wholesaler, Retailer, Distributor, Export

        [StringLength(50)]
        [Display(Name = "Category")]
        public string? Category { get; set; } // A, B, C classification

        [StringLength(15)]
        [Display(Name = "GSTIN")]
        public string? GSTIN { get; set; }

        [StringLength(10)]
        [Display(Name = "PAN")]
        public string? PAN { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        [Display(Name = "Credit Limit")]
        public decimal? CreditLimit { get; set; }

        [Display(Name = "Credit Days")]
        public int? CreditDays { get; set; }

        [StringLength(50)]
        [Display(Name = "Payment Terms")]
        public string? PaymentTerms { get; set; }

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Blocked

        // Navigation properties
        public virtual ICollection<CustomerContact>? Contacts { get; set; }
        public virtual ICollection<CustomerAddress>? Addresses { get; set; }

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }

    [Table("CustomerContacts")]
    public class CustomerContact
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(100)]
        [Display(Name = "Contact Person")]
        public string ContactPerson { get; set; } = string.Empty;

        [StringLength(100)]
        [Display(Name = "Designation")]
        public string? Designation { get; set; }

        [Required]
        [StringLength(15)]
        [Display(Name = "Mobile")]
        public string Mobile { get; set; } = string.Empty;

        [StringLength(100)]
        [Display(Name = "Email")]
        [EmailAddress]
        public string? Email { get; set; }

        [Display(Name = "Is Primary Contact")]
        public bool IsPrimary { get; set; }

        // Navigation
        [ForeignKey("CustomerId")]
        public virtual Customer? Customer { get; set; }
    }

    [Table("CustomerAddresses")]
    public class CustomerAddress
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(50)]
        [Display(Name = "Address Type")]
        public string AddressType { get; set; } = "Billing"; // Billing, Shipping, Both

        [Required]
        [StringLength(200)]
        [Display(Name = "Address Line 1")]
        public string AddressLine1 { get; set; } = string.Empty;

        [StringLength(200)]
        [Display(Name = "Address Line 2")]
        public string? AddressLine2 { get; set; }

        [Required]
        [StringLength(100)]
        [Display(Name = "City")]
        public string City { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        [Display(Name = "State")]
        public string State { get; set; } = string.Empty;

        [StringLength(50)]
        [Display(Name = "Country")]
        public string Country { get; set; } = "India";

        [Required]
        [StringLength(10)]
        [Display(Name = "Pincode")]
        public string Pincode { get; set; } = string.Empty;

        [Display(Name = "Is Default Address")]
        public bool IsDefault { get; set; }

        // Navigation
        [ForeignKey("CustomerId")]
        public virtual Customer? Customer { get; set; }
    }
}
