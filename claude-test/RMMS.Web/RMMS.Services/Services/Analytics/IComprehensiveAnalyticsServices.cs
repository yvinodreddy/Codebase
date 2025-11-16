using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Analytics
{
    // ================================================================
    // COMPREHENSIVE ANALYTICS SERVICE INTERFACES & DTOs
    // ================================================================

    #region Sales Trend Analytics

    public interface ISalesTrendAnalyticsService
    {
        Task<List<SalesTrendDto>> GetSalesTrends(DateTime startDate, DateTime endDate, string groupBy = "Daily");
        Task<List<ProductSalesDto>> GetTopSellingProducts(DateTime startDate, DateTime endDate, int top = 10);
        Task<List<RegionalSalesDto>> GetSalesByRegion(DateTime startDate, DateTime endDate);
        Task<SalesForecastDto> ForecastSales(int monthsAhead);
    }

    public class SalesTrendDto
    {
        public string Period { get; set; } = string.Empty;
        public decimal TotalSales { get; set; }
        public decimal TotalQuantity { get; set; }
        public int OrderCount { get; set; }
        public decimal AverageOrderValue { get; set; }
    }

    public class ProductSalesDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal TotalQuantity { get; set; }
        public decimal TotalRevenue { get; set; }
        public int OrderCount { get; set; }
        public decimal AveragePrice { get; set; }
    }

    public class RegionalSalesDto
    {
        public string Region { get; set; } = string.Empty;
        public decimal TotalSales { get; set; }
        public decimal TotalQuantity { get; set; }
        public int CustomerCount { get; set; }
        public int OrderCount { get; set; }
    }

    public class SalesForecastDto
    {
        public DateTime ForecastPeriod { get; set; }
        public decimal ForecastedAmount { get; set; }
        public decimal ConfidenceLower { get; set; }
        public decimal ConfidenceUpper { get; set; }
        public string Method { get; set; } = string.Empty;
    }

    #endregion

    #region Profit Margin Analysis

    public interface IProfitMarginAnalysisService
    {
        Task<List<ProductProfitabilityDto>> GetProductProfitability(DateTime startDate, DateTime endDate);
        Task<List<MarginTrendDto>> GetMarginTrends(DateTime startDate, DateTime endDate);
        Task<decimal> CalculateOverallProfitMargin(DateTime startDate, DateTime endDate);
    }

    public class ProductProfitabilityDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal TotalRevenue { get; set; }
        public decimal TotalCost { get; set; }
        public decimal GrossProfit { get; set; }
        public decimal ProfitMargin { get; set; }
        public decimal UnitsSold { get; set; }
    }

    public class MarginTrendDto
    {
        public DateTime Date { get; set; }
        public decimal TotalRevenue { get; set; }
        public decimal TotalCost { get; set; }
        public decimal GrossMargin { get; set; }
    }

    #endregion

    #region Customer Behavior Analytics

    public interface ICustomerBehaviorAnalyticsService
    {
        Task<List<CustomerSegmentDto>> GetCustomerSegments();
        Task<List<CustomerRetentionDto>> AnalyzeCustomerRetention(DateTime startDate, DateTime endDate);
        Task<decimal> CalculateCustomerLifetimeValue(int customerId);
        Task<List<ChurnRiskDto>> PredictCustomerChurn();
    }

    public class CustomerSegmentDto
    {
        public int CustomerId { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public string Segment { get; set; } = string.Empty;
        public decimal TotalSpent { get; set; }
        public int OrderCount { get; set; }
        public int RecencyDays { get; set; }
    }

    public class CustomerRetentionDto
    {
        public int CustomerId { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public DateTime FirstPurchaseDate { get; set; }
        public DateTime LastPurchaseDate { get; set; }
        public int TotalOrders { get; set; }
        public string RetentionStatus { get; set; } = string.Empty;
        public int DaysSinceFirstPurchase { get; set; }
    }

    public class ChurnRiskDto
    {
        public int CustomerId { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public int DaysSinceLastPurchase { get; set; }
        public string ChurnRisk { get; set; } = string.Empty;
        public DateTime LastPurchaseDate { get; set; }
        public decimal LastPurchaseAmount { get; set; }
    }

    #endregion

    #region Supplier Performance

    public interface ISupplierPerformanceService
    {
        Task<List<SupplierPerformanceDto>> GetSupplierPerformance(DateTime startDate, DateTime endDate);
        Task<List<SupplierReliabilityDto>> AssessSupplierReliability();
        Task<List<SupplierCostComparisonDto>> CompareSupplierCosts(int productId);
    }

    public class SupplierPerformanceDto
    {
        public int SupplierId { get; set; }
        public string SupplierName { get; set; } = string.Empty;
        public int TotalOrders { get; set; }
        public decimal TotalValue { get; set; }
        public decimal AverageOrderValue { get; set; }
        public int OnTimeDeliveries { get; set; }
        public decimal OnTimePercentage { get; set; }
        public decimal QualityScore { get; set; }
    }

    public class SupplierReliabilityDto
    {
        public int SupplierId { get; set; }
        public string SupplierName { get; set; } = string.Empty;
        public int TotalOrders { get; set; }
        public int SuccessfulDeliveries { get; set; }
        public decimal ReliabilityScore { get; set; }
        public int AverageLeadTime { get; set; }
        public decimal DefectRate { get; set; }
    }

    public class SupplierCostComparisonDto
    {
        public int SupplierId { get; set; }
        public string SupplierName { get; set; } = string.Empty;
        public decimal AverageUnitCost { get; set; }
        public decimal TotalQuantity { get; set; }
        public decimal TotalSpent { get; set; }
        public int OrderCount { get; set; }
    }

    #endregion

    #region Cost Analysis

    public interface ICostAnalysisService
    {
        Task<CostBreakdownDto> GetCostBreakdown(DateTime startDate, DateTime endDate);
        Task<List<CostVarianceDto>> AnalyzeCostVariance(DateTime startDate, DateTime endDate);
        Task<List<ProductCostDto>> GetProductCostAnalysis();
    }

    public class CostBreakdownDto
    {
        public decimal MaterialCosts { get; set; }
        public decimal LaborCosts { get; set; }
        public decimal OverheadCosts { get; set; }
        public decimal ProductionCosts { get; set; }
        public decimal TotalCosts { get; set; }
        public decimal MaterialPercentage { get; set; }
        public decimal LaborPercentage { get; set; }
        public decimal OverheadPercentage { get; set; }
        public decimal ProductionPercentage { get; set; }
    }

    public class CostVarianceDto
    {
        public string CostCategory { get; set; } = string.Empty;
        public decimal ExpectedCost { get; set; }
        public decimal ActualCost { get; set; }
        public decimal Variance { get; set; }
        public decimal VariancePercentage { get; set; }
    }

    public class ProductCostDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal UnitCost { get; set; }
        public decimal SellingPrice { get; set; }
        public decimal GrossMargin { get; set; }
    }

    #endregion

    #region Business Intelligence

    public interface IBusinessIntelligenceService
    {
        Task<BusinessDashboardDto> GetComprehensiveDashboard();
        Task<List<KPIDto>> GetKeyPerformanceIndicators(DateTime startDate, DateTime endDate);
        Task<List<BusinessAlertDto>> GetBusinessAlerts();
    }

    public class BusinessDashboardDto
    {
        public decimal TotalRevenue { get; set; }
        public decimal RevenueGrowth { get; set; }
        public decimal InventoryValue { get; set; }
        public int TotalCustomers { get; set; }
        public int ActiveCustomers { get; set; }
        public int ProductionBatches { get; set; }
        public decimal AverageEfficiency { get; set; }
        public int PendingOrders { get; set; }
    }

    public class KPIDto
    {
        public string Name { get; set; } = string.Empty;
        public decimal Value { get; set; }
        public string Unit { get; set; } = string.Empty;
        public decimal Target { get; set; }
        public decimal Achievement { get; set; }
        public string Trend { get; set; } = string.Empty;
    }

    public class BusinessAlertDto
    {
        public string AlertType { get; set; } = string.Empty;
        public string Severity { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public string ActionRequired { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; }
    }

    #endregion
}
