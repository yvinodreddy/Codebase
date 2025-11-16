using System;
using System.Collections.Generic;
using RMMS.Models.Production;

namespace RMMS.Services.Interfaces.Production
{
    public interface IYieldAnalysisService
    {
        // Overall Yield Statistics
        YieldStatistics GetOverallYieldStatistics(DateTime? fromDate = null, DateTime? toDate = null);

        // Yield Trends
        List<YieldTrendData> GetYieldTrends(DateTime fromDate, DateTime toDate, string groupBy = "Daily");

        // Yield by Paddy Variety
        List<YieldByVarietyData> GetYieldByPaddyVariety(DateTime? fromDate = null, DateTime? toDate = null);

        // Yield by Machine
        List<YieldByMachineData> GetYieldByMachine(DateTime? fromDate = null, DateTime? toDate = null);

        // Yield Comparison
        YieldComparisonData GetYieldComparison(DateTime? fromDate = null, DateTime? toDate = null);

        // Low Yield Batches
        List<ProductionBatch> GetLowYieldBatches(decimal threshold, DateTime? fromDate = null, DateTime? toDate = null);

        // High Yield Batches
        List<ProductionBatch> GetHighYieldBatches(decimal threshold, DateTime? fromDate = null, DateTime? toDate = null);

        // Yield Variance Analysis
        List<YieldVarianceData> GetYieldVarianceAnalysis(DateTime? fromDate = null, DateTime? toDate = null);

        // Production Summary
        ProductionSummaryData GetProductionSummary(DateTime? fromDate = null, DateTime? toDate = null);

        // Batch Performance Details
        List<BatchPerformanceData> GetBatchPerformanceDetails(DateTime? fromDate = null, DateTime? toDate = null);
    }

    // View Models for Yield Analysis
    public class YieldStatistics
    {
        public int TotalBatches { get; set; }
        public decimal TotalInputQuantity { get; set; }
        public decimal TotalOutputQuantity { get; set; }
        public decimal AverageYieldPercent { get; set; }
        public decimal MinYieldPercent { get; set; }
        public decimal MaxYieldPercent { get; set; }
        public decimal StandardYieldPercent { get; set; } = 65.0m;
        public decimal YieldVariance { get; set; }
        public int BatchesAboveStandard { get; set; }
        public int BatchesBelowStandard { get; set; }
    }

    public class YieldTrendData
    {
        public string Period { get; set; } = string.Empty;
        public DateTime PeriodDate { get; set; }
        public int BatchCount { get; set; }
        public decimal AverageYield { get; set; }
        public decimal HeadRicePercent { get; set; }
        public decimal BrokenRicePercent { get; set; }
        public decimal BranPercent { get; set; }
        public decimal HuskPercent { get; set; }
    }

    public class YieldByVarietyData
    {
        public string PaddyVariety { get; set; } = string.Empty;
        public int BatchCount { get; set; }
        public decimal TotalInputQuantity { get; set; }
        public decimal TotalOutputQuantity { get; set; }
        public decimal AverageYieldPercent { get; set; }
        public decimal BestYieldPercent { get; set; }
        public decimal WorstYieldPercent { get; set; }
    }

    public class YieldByMachineData
    {
        public string MachineName { get; set; } = string.Empty;
        public string MachineCode { get; set; } = string.Empty;
        public int BatchCount { get; set; }
        public decimal AverageYieldPercent { get; set; }
        public decimal TotalInputQuantity { get; set; }
        public decimal TotalOutputQuantity { get; set; }
    }

    public class YieldComparisonData
    {
        public decimal CurrentPeriodAverage { get; set; }
        public decimal PreviousPeriodAverage { get; set; }
        public decimal PercentChange { get; set; }
        public string Trend { get; set; } = string.Empty; // Improving, Declining, Stable
        public int CurrentPeriodBatches { get; set; }
        public int PreviousPeriodBatches { get; set; }
    }

    public class YieldVarianceData
    {
        public string BatchNumber { get; set; } = string.Empty;
        public DateTime BatchDate { get; set; }
        public string PaddyVariety { get; set; } = string.Empty;
        public decimal ActualYield { get; set; }
        public decimal StandardYield { get; set; }
        public decimal Variance { get; set; }
        public decimal VariancePercent { get; set; }
        public string VarianceType { get; set; } = string.Empty; // Positive, Negative
    }

    public class ProductionSummaryData
    {
        public int TotalBatches { get; set; }
        public decimal TotalPaddyProcessed { get; set; }
        public decimal TotalRiceProduced { get; set; }
        public decimal TotalBranProduced { get; set; }
        public decimal TotalHuskProduced { get; set; }
        public decimal TotalBrokenRice { get; set; }
        public decimal AverageYield { get; set; }
        public int MachinesUsed { get; set; }
        public decimal TotalProcessingHours { get; set; }
        public decimal AverageBatchDuration { get; set; }
    }

    public class BatchPerformanceData
    {
        public string BatchNumber { get; set; } = string.Empty;
        public DateTime BatchDate { get; set; }
        public string ShiftType { get; set; } = string.Empty;
        public string OperatorName { get; set; } = string.Empty;
        public decimal InputQuantity { get; set; }
        public decimal OutputQuantity { get; set; }
        public decimal YieldPercent { get; set; }
        public decimal ProcessingHours { get; set; }
        public decimal QualityScore { get; set; }
        public string Status { get; set; } = string.Empty;
        public string PerformanceRating { get; set; } = string.Empty; // Excellent, Good, Average, Poor
    }
}
