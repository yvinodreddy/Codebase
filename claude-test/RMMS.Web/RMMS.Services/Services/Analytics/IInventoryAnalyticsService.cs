namespace RMMS.Services.Services.Analytics
{
    // ================================================================
    // PHASE 3.1 - TASKS 2 & 10: INVENTORY ANALYTICS & PREDICTIVE ALERTS
    // ================================================================

    #region View Models

    public class StockAgingDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public int WarehouseId { get; set; }
        public string WarehouseName { get; set; } = string.Empty;
        public decimal CurrentStock { get; set; }
        public int DaysInStock { get; set; }
        public string AgingBucket { get; set; } = string.Empty; // 0-30, 31-60, 61-90, 90+
        public decimal StockValue { get; set; }
        public DateTime OldestStockDate { get; set; }
    }

    public class StockMovementClassificationDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal TurnoverRatio { get; set; }
        public string MovementClass { get; set; } = string.Empty; // Fast/Medium/Slow/Dead
        public decimal AverageMonthlyMovement { get; set; }
        public int DaysSinceLastMovement { get; set; }
        public decimal CurrentStock { get; set; }
        public string Recommendation { get; set; } = string.Empty;
    }

    public class ABCClassificationDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal AnnualConsumptionValue { get; set; }
        public decimal AnnualConsumptionQuantity { get; set; }
        public decimal PercentageOfTotalValue { get; set; }
        public decimal CumulativePercentage { get; set; }
        public string ABCClass { get; set; } = string.Empty; // A, B, or C
        public string ManagementStrategy { get; set; } = string.Empty;
    }

    public class ReorderPointDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal CurrentStock { get; set; }
        public decimal ReorderPoint { get; set; }
        public decimal SafetyStock { get; set; }
        public decimal EconomicOrderQuantity { get; set; }
        public decimal AverageDailyUsage { get; set; }
        public int LeadTimeDays { get; set; }
        public bool RequiresReorder { get; set; }
        public int DaysUntilStockout { get; set; }
        public string UrgencyLevel { get; set; } = string.Empty; // Critical/High/Medium/Low
    }

    public class DemandForecastDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public DateTime ForecastDate { get; set; }
        public decimal PredictedDemand { get; set; }
        public decimal ConfidenceLevel { get; set; }
        public decimal HistoricalAverage { get; set; }
        public decimal TrendAdjustment { get; set; }
        public decimal SeasonalFactor { get; set; }
    }

    public class StockValuationDto
    {
        public string Method { get; set; } = string.Empty; // FIFO/LIFO/Weighted Average
        public decimal TotalInventoryValue { get; set; }
        public Dictionary<string, decimal> ValueByCategory { get; set; } = new();
        public Dictionary<string, decimal> ValueByWarehouse { get; set; } = new();
        public decimal MonthOverMonthChange { get; set; }
        public decimal YearOverYearChange { get; set; }
    }

    public class InventoryDashboardDto
    {
        public decimal TotalInventoryValue { get; set; }
        public int TotalSKUs { get; set; }
        public int LowStockItems { get; set; }
        public int OutOfStockItems { get; set; }
        public int OverstockItems { get; set; }
        public int DeadStockItems { get; set; }
        public decimal InventoryTurnoverRatio { get; set; }
        public int DaysInventoryOutstanding { get; set; }
        public List<StockAgingDto> AgingAnalysis { get; set; } = new();
        public List<ABCClassificationDto> ABCAnalysis { get; set; } = new();
        public List<ReorderPointDto> ReorderAlerts { get; set; } = new();
    }

    public class StockAlertDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public string AlertType { get; set; } = string.Empty; // LowStock/OutOfStock/Overstock/Expiring
        public string Severity { get; set; } = string.Empty; // Critical/High/Medium/Low
        public decimal CurrentStock { get; set; }
        public decimal RecommendedOrderQuantity { get; set; }
        public string Message { get; set; } = string.Empty;
        public DateTime AlertDate { get; set; }
        public bool IsAcknowledged { get; set; }
    }

    #endregion

    public interface IInventoryAnalyticsService
    {
        // Task 2: Real-time Inventory Analytics
        Task<InventoryDashboardDto> GetInventoryDashboard();
        Task<List<StockAgingDto>> GetStockAgingAnalysis();
        Task<List<StockMovementClassificationDto>> GetStockMovementClassification(DateTime startDate, DateTime endDate);
        Task<List<ABCClassificationDto>> GetABCClassification(DateTime startDate, DateTime endDate);
        Task<StockValuationDto> GetStockValuation(string method = "FIFO");
        Task<decimal> CalculateInventoryTurnoverRatio(DateTime startDate, DateTime endDate);
        Task<int> CalculateDaysInventoryOutstanding(DateTime startDate, DateTime endDate);

        // Task 10: Predictive Stock Alerts
        Task<List<ReorderPointDto>> CalculateReorderPoints();
        Task<List<DemandForecastDto>> GetDemandForecast(int productId, int daysAhead = 30);
        Task<List<StockAlertDto>> GetStockAlerts();
        Task<decimal> CalculateEconomicOrderQuantity(int productId);
        Task<decimal> CalculateReorderPoint(int productId);
        Task<List<StockAlertDto>> GenerateAutoReorderSuggestions();
        Task<List<ProductStockoutRiskDto>> PredictStockoutRisk(int daysAhead = 30);
    }

    public class ProductStockoutRiskDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal CurrentStock { get; set; }
        public decimal PredictedDemand { get; set; }
        public int DaysUntilStockout { get; set; }
        public decimal StockoutProbability { get; set; }
        public string RiskLevel { get; set; } = string.Empty; // Critical/High/Medium/Low
        public decimal RecommendedOrderQuantity { get; set; }
    }
}
