using System;

namespace RMMS.Models.Reporting
{
    public class ComparisonPeriod
    {
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public string PeriodLabel { get; set; } = string.Empty;
    }

    public class ComparisonResult
    {
        public string Metric { get; set; } = string.Empty;
        public decimal Period1Value { get; set; }
        public decimal Period2Value { get; set; }
        public decimal Variance { get; set; }
        public decimal VariancePercentage { get; set; }
        public string Trend { get; set; } = string.Empty; // "Up", "Down", "Flat"
        public string TrendIcon { get; set; } = string.Empty; // "↑", "↓", "→"
    }

    public class ComparisonReportOptions
    {
        public ComparisonPeriod Period1 { get; set; } = new();
        public ComparisonPeriod Period2 { get; set; } = new();
        public string ComparisonType { get; set; } = "MoM"; // MoM, YoY, Custom
        public List<string> Metrics { get; set; } = new();
        public string Category { get; set; } = "Sales"; // Sales, Inventory, Production, Financial
    }

    public class ComparisonReport
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string ReportTitle { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public DateTime GeneratedDate { get; set; } = DateTime.Now;
        public ComparisonPeriod Period1 { get; set; } = new();
        public ComparisonPeriod Period2 { get; set; } = new();
        public List<ComparisonResult> Results { get; set; } = new();
        public string Summary { get; set; } = string.Empty;
        public decimal OverallVariancePercentage { get; set; }
        public bool IsActive { get; set; } = true;
        public string CreatedBy { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? ModifiedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
    }
}
