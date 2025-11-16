using RMMS.Models.Production;

namespace RMMS.Services.Services.Analytics
{
    // ================================================================
    // PHASE 3.1 - TASKS 1, 7, 8, 9: PRODUCTION ANALYTICS
    // ================================================================

    #region View Models

    public class ProductionEfficiencyDto
    {
        public int MachineId { get; set; }
        public string MachineName { get; set; } = string.Empty;
        public decimal EfficiencyPercentage { get; set; }
        public decimal OEE { get; set; } // Overall Equipment Effectiveness
        public decimal AvailabilityPercentage { get; set; }
        public decimal PerformancePercentage { get; set; }
        public decimal QualityPercentage { get; set; }
        public int TotalDowntimeMinutes { get; set; }
        public int PlannedProductionMinutes { get; set; }
        public decimal ActualOutput { get; set; }
        public decimal PlannedOutput { get; set; }
        public string Status { get; set; } = string.Empty; // Excellent/Good/Average/Poor
    }

    public class ShiftPerformanceDto
    {
        public string ShiftName { get; set; } = string.Empty;
        public DateTime Date { get; set; }
        public decimal TotalOutput { get; set; }
        public decimal PlannedOutput { get; set; }
        public decimal EfficiencyPercentage { get; set; }
        public int NumberOfBatches { get; set; }
        public decimal AverageYieldPercentage { get; set; }
        public int DowntimeMinutes { get; set; }
    }

    public class DowntimeAnalysisDto
    {
        public int MachineId { get; set; }
        public string MachineName { get; set; } = string.Empty;
        public string DowntimeReason { get; set; } = string.Empty;
        public int TotalMinutes { get; set; }
        public int OccurrenceCount { get; set; }
        public decimal ImpactOnProduction { get; set; }
        public DateTime? LastOccurrence { get; set; }
    }

    public class QualityMetricsDto
    {
        public DateTime Date { get; set; }
        public int TotalBatches { get; set; }
        public int QualityPassedBatches { get; set; }
        public decimal QualityPassPercentage { get; set; }
        public decimal AverageYieldPercentage { get; set; }
        public decimal DefectRate { get; set; }
        public decimal ReworkRate { get; set; }
    }

    public class MachineUtilizationDto
    {
        public int MachineId { get; set; }
        public string MachineName { get; set; } = string.Empty;
        public decimal UtilizationPercentage { get; set; }
        public int TotalRunningHours { get; set; }
        public int TotalAvailableHours { get; set; }
        public int IdleHours { get; set; }
        public DateTime? NextMaintenanceDate { get; set; }
        public int DaysSinceLastMaintenance { get; set; }
        public string CapacityStatus { get; set; } = string.Empty; // Under/Optimal/Over
    }

    public class WasteTrackingDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public string ProcessName { get; set; } = string.Empty;
        public decimal TotalWasteQuantity { get; set; }
        public string UnitOfMeasure { get; set; } = string.Empty;
        public decimal WastePercentage { get; set; }
        public decimal EstimatedCost { get; set; }
        public DateTime PeriodStart { get; set; }
        public DateTime PeriodEnd { get; set; }
    }

    public class ProductionDashboardDto
    {
        public decimal OverallOEE { get; set; }
        public decimal OverallEfficiency { get; set; }
        public int ActiveMachines { get; set; }
        public int TotalMachines { get; set; }
        public decimal TodayOutput { get; set; }
        public decimal TodayTarget { get; set; }
        public int RunningBatches { get; set; }
        public int CompletedBatchesToday { get; set; }
        public List<ProductionEfficiencyDto> MachineEfficiencies { get; set; } = new();
        public List<DowntimeAnalysisDto> TopDowntimeReasons { get; set; } = new();
        public List<QualityMetricsDto> RecentQualityMetrics { get; set; } = new();
    }

    #endregion

    public interface IProductionAnalyticsService
    {
        // Task 1: Production Efficiency Dashboard
        Task<ProductionDashboardDto> GetProductionDashboard(DateTime? date = null);
        Task<List<ProductionEfficiencyDto>> GetMachineEfficiencies(DateTime startDate, DateTime endDate);
        Task<ProductionEfficiencyDto> CalculateMachineEfficiency(int machineId, DateTime startDate, DateTime endDate);
        Task<List<ShiftPerformanceDto>> GetShiftPerformance(DateTime startDate, DateTime endDate);
        Task<decimal> CalculateOEE(int machineId, DateTime startDate, DateTime endDate);
        Task<List<DowntimeAnalysisDto>> GetDowntimeAnalysis(DateTime startDate, DateTime endDate, int? machineId = null);

        // Task 7: Machine Utilization Reports
        Task<List<MachineUtilizationDto>> GetMachineUtilization(DateTime startDate, DateTime endDate);
        Task<Dictionary<string, decimal>> GetCapacityPlanningData(DateTime futureDate);
        Task<List<Machine>> GetMachinesRequiringMaintenance(int daysAhead = 30);

        // Task 8: Quality Control Analytics
        Task<List<QualityMetricsDto>> GetQualityTrends(DateTime startDate, DateTime endDate);
        Task<Dictionary<string, int>> GetDefectAnalysis(DateTime startDate, DateTime endDate);
        Task<List<YieldOptimizationDto>> GetYieldOptimizationSuggestions();

        // Task 9: Waste Reduction Tracking
        Task<List<WasteTrackingDto>> GetWasteByProduct(DateTime startDate, DateTime endDate);
        Task<List<WasteTrackingDto>> GetWasteByProcess(DateTime startDate, DateTime endDate);
        Task<decimal> CalculateTotalWasteCost(DateTime startDate, DateTime endDate);
        Task<List<WasteReductionTargetDto>> GetWasteReductionTargets();
    }

    public class YieldOptimizationDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal CurrentAverageYield { get; set; }
        public decimal BestYieldAchieved { get; set; }
        public decimal ImprovementPotential { get; set; }
        public string Recommendation { get; set; } = string.Empty;
        public decimal EstimatedSavings { get; set; }
    }

    public class WasteReductionTargetDto
    {
        public string Category { get; set; } = string.Empty;
        public decimal CurrentWastePercentage { get; set; }
        public decimal TargetWastePercentage { get; set; }
        public decimal ReductionGoal { get; set; }
        public string Status { get; set; } = string.Empty; // On Track/Behind/Exceeded
    }
}
