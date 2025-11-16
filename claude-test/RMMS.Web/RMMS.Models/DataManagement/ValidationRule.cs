using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.DataManagement
{
    public class ValidationRule
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(100)]
        public string EntityType { get; set; } = string.Empty;

        [StringLength(100)]
        public string FieldName { get; set; } = string.Empty;

        [StringLength(50)]
        public string ValidationType { get; set; } = "Required";

        public string ValidationExpression { get; set; } = string.Empty;

        [StringLength(500)]
        public string ErrorMessage { get; set; } = string.Empty;

        public int Priority { get; set; } = 0;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
