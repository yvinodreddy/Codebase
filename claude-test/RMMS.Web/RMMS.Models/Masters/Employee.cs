using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Masters
{
    [Table("Employees")]
    public class Employee
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Employee Code")]
        public string EmployeeCode { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        [Display(Name = "Employee Name")]
        public string EmployeeName { get; set; } = string.Empty;

        [StringLength(50)]
        [Display(Name = "Department")]
        public string? Department { get; set; } // Production, Quality Control, Admin, Sales, Accounts, Warehouse

        [StringLength(100)]
        [Display(Name = "Designation")]
        public string? Designation { get; set; }

        [Required]
        [StringLength(15)]
        [Display(Name = "Mobile")]
        public string Mobile { get; set; } = string.Empty;

        [StringLength(100)]
        [EmailAddress]
        [Display(Name = "Email")]
        public string? Email { get; set; }

        [Display(Name = "Date of Joining")]
        [DataType(DataType.Date)]
        public DateTime? DateOfJoining { get; set; }

        [Display(Name = "Date of Birth")]
        [DataType(DataType.Date)]
        public DateTime? DateOfBirth { get; set; }

        [StringLength(200)]
        [Display(Name = "Address")]
        public string? Address { get; set; }

        [StringLength(100)]
        [Display(Name = "City")]
        public string? City { get; set; }

        [StringLength(100)]
        [Display(Name = "State")]
        public string? State { get; set; }

        [StringLength(10)]
        [Display(Name = "Pincode")]
        public string? Pincode { get; set; }

        [StringLength(12)]
        [Display(Name = "Aadhar Number")]
        public string? AadharNumber { get; set; }

        [StringLength(10)]
        [Display(Name = "PAN")]
        public string? PAN { get; set; }

        [Display(Name = "Basic Salary")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? BasicSalary { get; set; }

        [StringLength(50)]
        [Display(Name = "Employment Type")]
        public string? EmploymentType { get; set; } // Permanent, Contract, Daily Wage

        [StringLength(100)]
        [Display(Name = "Bank Account Number")]
        public string? BankAccountNumber { get; set; }

        [StringLength(11)]
        [Display(Name = "IFSC Code")]
        public string? IFSCCode { get; set; }

        [StringLength(20)]
        [Display(Name = "Status")]
        public string Status { get; set; } = "Active"; // Active, Inactive, Resigned, Terminated

        // Audit fields
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? CreatedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
        public string? ModifiedBy { get; set; }
        public bool IsActive { get; set; } = true;
    }
}
