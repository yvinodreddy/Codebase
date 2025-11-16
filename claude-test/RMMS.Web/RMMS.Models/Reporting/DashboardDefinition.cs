using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Reporting
{
    public class DashboardDefinition
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        public string WidgetConfiguration { get; set; } = string.Empty; // JSON

        public string Layout { get; set; } = string.Empty; // JSON

        [StringLength(50)]
        public string Template { get; set; } = "Custom";

        public bool IsPublic { get; set; } = false;

        public bool IsActive { get; set; } = true;

        public int RefreshInterval { get; set; } = 60; // seconds

        [StringLength(450)]
        public string CreatedBy { get; set; } = string.Empty;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
