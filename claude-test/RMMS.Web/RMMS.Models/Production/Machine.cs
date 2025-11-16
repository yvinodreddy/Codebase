using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Production
{
    public class Machine
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        [Display(Name = "Machine Code")]
        public string MachineCode { get; set; } = string.Empty;

        [Required]
        [StringLength(100)]
        [Display(Name = "Machine Name")]
        public string MachineName { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        [Display(Name = "Machine Type")]
        public string MachineType { get; set; } = string.Empty; // Cleaner, Husker, Polisher, Grader, Separator, Dryer, Weighbridge

        [StringLength(100)]
        public string? Manufacturer { get; set; }

        [StringLength(50)]
        [Display(Name = "Model Number")]
        public string? ModelNumber { get; set; }

        [Display(Name = "Capacity")]
        public decimal Capacity { get; set; }

        [StringLength(20)]
        [Display(Name = "Capacity Unit")]
        public string? CapacityUnit { get; set; } = "tons/hour"; // tons/hour, bags/hour, kg/hour

        [Display(Name = "Purchase Date")]
        [DataType(DataType.Date)]
        public DateTime? PurchaseDate { get; set; }

        [Display(Name = "Purchase Price")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? PurchasePrice { get; set; }

        [Display(Name = "Current Value")]
        [Column(TypeName = "decimal(18,2)")]
        public decimal? CurrentValue { get; set; }

        [StringLength(100)]
        [Display(Name = "Location/Section")]
        public string? Location { get; set; }

        [Required]
        [StringLength(20)]
        public string Status { get; set; } = "Operational"; // Operational, Maintenance, Breakdown, Idle

        [Display(Name = "Running Hours")]
        public decimal RunningHours { get; set; } = 0;

        [Display(Name = "Last Maintenance Date")]
        [DataType(DataType.Date)]
        public DateTime? LastMaintenanceDate { get; set; }

        [Display(Name = "Next Maintenance Due")]
        [DataType(DataType.Date)]
        public DateTime? NextMaintenanceDue { get; set; }

        [Display(Name = "Maintenance Interval (Hours)")]
        public int? MaintenanceIntervalHours { get; set; }

        [StringLength(500)]
        public string? Specifications { get; set; }

        [StringLength(500)]
        public string? Remarks { get; set; }

        // Audit Fields
        [Display(Name = "Created Date")]
        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(100)]
        [Display(Name = "Created By")]
        public string? CreatedBy { get; set; }

        [Display(Name = "Modified Date")]
        public DateTime? ModifiedDate { get; set; }

        [StringLength(100)]
        [Display(Name = "Modified By")]
        public string? ModifiedBy { get; set; }

        [Display(Name = "Active")]
        public bool IsActive { get; set; } = true;

        // Computed Properties
        [NotMapped]
        public string StatusBadgeClass => Status switch
        {
            "Operational" => "bg-success",
            "Maintenance" => "bg-warning",
            "Breakdown" => "bg-danger",
            "Idle" => "bg-secondary",
            _ => "bg-secondary"
        };

        [NotMapped]
        public string StatusIcon => Status switch
        {
            "Operational" => "fa-check-circle",
            "Maintenance" => "fa-wrench",
            "Breakdown" => "fa-exclamation-triangle",
            "Idle" => "fa-pause-circle",
            _ => "fa-circle"
        };

        [NotMapped]
        public string TypeIcon => MachineType switch
        {
            "Cleaner" => "fa-broom",
            "Husker" => "fa-hammer",
            "Polisher" => "fa-gem",
            "Grader" => "fa-sort-amount-down",
            "Separator" => "fa-filter",
            "Dryer" => "fa-fire",
            "Weighbridge" => "fa-weight",
            _ => "fa-cog"
        };

        [NotMapped]
        public bool IsMaintenanceDue
        {
            get
            {
                if (NextMaintenanceDue.HasValue)
                {
                    return NextMaintenanceDue.Value <= DateTime.Now.AddDays(7);
                }
                return false;
            }
        }

        [NotMapped]
        public decimal DepreciationPercent
        {
            get
            {
                if (PurchasePrice.HasValue && PurchasePrice.Value > 0 && CurrentValue.HasValue)
                {
                    return ((PurchasePrice.Value - CurrentValue.Value) / PurchasePrice.Value) * 100;
                }
                return 0;
            }
        }

        [NotMapped]
        public string CapacityDisplay => $"{Capacity:N2} {CapacityUnit}";
    }
}
