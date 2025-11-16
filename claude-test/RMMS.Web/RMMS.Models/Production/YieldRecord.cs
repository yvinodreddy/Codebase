using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Models.Production
{
    public class YieldRecord
    {
        [Key]
        public int Id { get; set; }

        // Link to Production Batch (One-to-One)
        [Required]
        [Display(Name = "Production Batch")]
        public int BatchId { get; set; }

        [ForeignKey(nameof(BatchId))]
        public virtual ProductionBatch? Batch { get; set; }

        // Input Information
        [StringLength(100)]
        [Display(Name = "Paddy Variety")]
        public string? PaddyVariety { get; set; }

        [Required]
        [Display(Name = "Input Paddy Quantity")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal InputPaddyQuantity { get; set; }

        // Output Quantities
        [Display(Name = "Head Rice Output")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal OutputHeadRice { get; set; }

        [Display(Name = "Broken Rice Output")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal OutputBrokenRice { get; set; }

        [Display(Name = "Bran Output")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal OutputBran { get; set; }

        [Display(Name = "Husk Output")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal OutputHusk { get; set; }

        [Display(Name = "Wastage")]
        [Column(TypeName = "decimal(18,3)")]
        public decimal OutputWastage { get; set; }

        // Calculated Percentages
        [Display(Name = "Head Rice %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal HeadRicePercent { get; set; }

        [Display(Name = "Broken Rice %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal BrokenRicePercent { get; set; }

        [Display(Name = "Bran %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal BranPercent { get; set; }

        [Display(Name = "Husk %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal HuskPercent { get; set; }

        [Display(Name = "Wastage %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal WastagePercent { get; set; }

        [Display(Name = "Total Yield %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal TotalYieldPercent { get; set; }

        // Standard/Expected Yields
        [Display(Name = "Standard Head Rice %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? StandardHeadRicePercent { get; set; } = 65.00M;

        [Display(Name = "Standard Total Yield %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? StandardTotalYieldPercent { get; set; } = 98.00M;

        // Variance Analysis
        [Display(Name = "Head Rice Variance %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal HeadRiceVariance => HeadRicePercent - (StandardHeadRicePercent ?? 65.00M);

        [Display(Name = "Total Yield Variance %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal TotalYieldVariance => TotalYieldPercent - (StandardTotalYieldPercent ?? 98.00M);

        // Quality Grade
        [Required]
        [StringLength(20)]
        [Display(Name = "Yield Grade")]
        public string YieldGrade { get; set; } = "Average"; // Excellent, Good, Average, Poor

        [Display(Name = "Quality Score")]
        [Column(TypeName = "decimal(3,1)")]
        public decimal? QualityScore { get; set; } // 1-10 scale

        // Additional Metrics
        [Display(Name = "Milling Recovery %")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? MillingRecovery { get; set; } // Head Rice + Broken Rice

        [Display(Name = "Head Rice to Broken Ratio")]
        [Column(TypeName = "decimal(5,2)")]
        public decimal? HeadRiceToBrokenRatio { get; set; }

        // Remarks
        [StringLength(500)]
        public string? Remarks { get; set; }

        [StringLength(500)]
        [Display(Name = "Variance Analysis")]
        public string? VarianceAnalysis { get; set; }

        // Audit Fields
        [Display(Name = "Calculated Date")]
        public DateTime CalculatedDate { get; set; } = DateTime.Now;

        [StringLength(100)]
        [Display(Name = "Calculated By")]
        public string? CalculatedBy { get; set; }

        [Display(Name = "Verified")]
        public bool IsVerified { get; set; } = false;

        [Display(Name = "Verified By")]
        [StringLength(100)]
        public string? VerifiedBy { get; set; }

        [Display(Name = "Verified Date")]
        public DateTime? VerifiedDate { get; set; }

        // Computed Properties
        [NotMapped]
        public string GradeBadgeClass => YieldGrade switch
        {
            "Excellent" => "bg-success",
            "Good" => "bg-info",
            "Average" => "bg-warning",
            "Poor" => "bg-danger",
            _ => "bg-secondary"
        };

        [NotMapped]
        public string VarianceBadgeClass
        {
            get
            {
                if (HeadRiceVariance >= 2) return "bg-success";
                if (HeadRiceVariance >= -2) return "bg-warning";
                return "bg-danger";
            }
        }

        [NotMapped]
        public string VarianceIcon
        {
            get
            {
                if (HeadRiceVariance > 0) return "fa-arrow-up text-success";
                if (HeadRiceVariance < 0) return "fa-arrow-down text-danger";
                return "fa-minus text-warning";
            }
        }

        [NotMapped]
        public bool IsExcellentYield => YieldGrade == "Excellent" && HeadRicePercent >= 68;

        [NotMapped]
        public bool IsLowYield => YieldGrade == "Poor" || HeadRicePercent < 55;

        /// <summary>
        /// Calculate all yield percentages based on input and output quantities
        /// </summary>
        public void CalculateYields()
        {
            if (InputPaddyQuantity > 0)
            {
                HeadRicePercent = Math.Round((OutputHeadRice / InputPaddyQuantity) * 100, 2);
                BrokenRicePercent = Math.Round((OutputBrokenRice / InputPaddyQuantity) * 100, 2);
                BranPercent = Math.Round((OutputBran / InputPaddyQuantity) * 100, 2);
                HuskPercent = Math.Round((OutputHusk / InputPaddyQuantity) * 100, 2);
                WastagePercent = Math.Round((OutputWastage / InputPaddyQuantity) * 100, 2);
                TotalYieldPercent = HeadRicePercent + BrokenRicePercent + BranPercent + HuskPercent + WastagePercent;

                // Calculate milling recovery
                MillingRecovery = HeadRicePercent + BrokenRicePercent;

                // Calculate head rice to broken rice ratio
                if (OutputBrokenRice > 0)
                {
                    HeadRiceToBrokenRatio = Math.Round(OutputHeadRice / OutputBrokenRice, 2);
                }

                // Determine yield grade
                if (HeadRicePercent >= 68)
                    YieldGrade = "Excellent";
                else if (HeadRicePercent >= 62)
                    YieldGrade = "Good";
                else if (HeadRicePercent >= 55)
                    YieldGrade = "Average";
                else
                    YieldGrade = "Poor";
            }
        }
    }
}
