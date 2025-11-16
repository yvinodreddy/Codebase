using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile
{
    public class MobileDashboard
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(450)]
        public string UserId { get; set; } = string.Empty;

        public string WidgetConfiguration { get; set; } = string.Empty;

        public string Layout { get; set; } = string.Empty;

        [StringLength(50)]
        public string Theme { get; set; } = "Light";

        public bool IsDefault { get; set; } = false;

        public bool IsActive { get; set; } = true;

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
