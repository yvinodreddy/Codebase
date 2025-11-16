using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using System.Linq;
using RMMS.Services.Services.Analytics;

namespace RMMS.Services.Services.Analytics.Implementations
{
    // ================================================================
    // PHASE 3.1 - TASKS 3-6, 11-12: COMPREHENSIVE ANALYTICS SERVICES
    // ================================================================

    #region Task 3: Sales Trend Analytics

    public class SalesTrendAnalyticsService : ISalesTrendAnalyticsService
    {
        private readonly ApplicationDbContext _context;

        public SalesTrendAnalyticsService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<SalesTrendDto>> GetSalesTrends(DateTime startDate, DateTime endDate, string groupBy = "Daily")
        {
            var sales = await _context.RiceSales
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .ToListAsync();

            var trends = new List<SalesTrendDto>();

            switch (groupBy.ToUpper())
            {
                case "DAILY":
                    trends = sales.GroupBy(s => s.SaleDate.Date)
                        .Select(g => new SalesTrendDto
                        {
                            Period = g.Key.ToString("yyyy-MM-dd"),
                            TotalSales = g.Sum(s => s.TotalAmount),
                            TotalQuantity = g.Sum(s => s.Quantity),
                            OrderCount = g.Count(),
                            AverageOrderValue = g.Average(s => s.TotalAmount)
                        })
                        .OrderBy(t => t.Period)
                        .ToList();
                    break;

                case "WEEKLY":
                    trends = sales.GroupBy(s => new { Year = s.SaleDate.Year, Week = GetWeekNumber(s.SaleDate) })
                        .Select(g => new SalesTrendDto
                        {
                            Period = $"{g.Key.Year}-W{g.Key.Week}",
                            TotalSales = g.Sum(s => s.TotalAmount),
                            TotalQuantity = g.Sum(s => s.Quantity),
                            OrderCount = g.Count(),
                            AverageOrderValue = g.Average(s => s.TotalAmount)
                        })
                        .OrderBy(t => t.Period)
                        .ToList();
                    break;

                case "MONTHLY":
                    trends = sales.GroupBy(s => new { s.SaleDate.Year, s.SaleDate.Month })
                        .Select(g => new SalesTrendDto
                        {
                            Period = $"{g.Key.Year}-{g.Key.Month:D2}",
                            TotalSales = g.Sum(s => s.TotalAmount),
                            TotalQuantity = g.Sum(s => s.Quantity),
                            OrderCount = g.Count(),
                            AverageOrderValue = g.Average(s => s.TotalAmount)
                        })
                        .OrderBy(t => t.Period)
                        .ToList();
                    break;
            }

            return trends;
        }

        private int GetWeekNumber(DateTime date)
        {
            var day = (int)System.Globalization.CultureInfo.CurrentCulture.Calendar.GetDayOfWeek(date);
            return System.Globalization.CultureInfo.CurrentCulture.Calendar.GetWeekOfYear(
                date, System.Globalization.CalendarWeekRule.FirstFourDayWeek, DayOfWeek.Monday);
        }

        public async Task<List<ProductSalesDto>> GetTopSellingProducts(DateTime startDate, DateTime endDate, int top = 10)
        {
            var productSales = await _context.RiceSales
                .Include(s => s.Product)
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .GroupBy(s => s.ProductId)
                .Select(g => new ProductSalesDto
                {
                    ProductId = g.Key,
                    ProductName = g.First().Product!.ProductName,
                    TotalQuantity = g.Sum(s => s.Quantity),
                    TotalRevenue = g.Sum(s => s.TotalAmount),
                    OrderCount = g.Count(),
                    AveragePrice = g.Average(s => s.Rate)
                })
                .OrderByDescending(p => p.TotalRevenue)
                .Take(top)
                .ToListAsync();

            return productSales;
        }

        public async Task<List<RegionalSalesDto>> GetSalesByRegion(DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Include(s => s.Customer)
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .GroupBy(s => s.Customer!.State ?? "Unknown")
                .Select(g => new RegionalSalesDto
                {
                    Region = g.Key,
                    TotalSales = g.Sum(s => s.TotalAmount),
                    TotalQuantity = g.Sum(s => s.Quantity),
                    CustomerCount = g.Select(s => s.CustomerId).Distinct().Count(),
                    OrderCount = g.Count()
                })
                .OrderByDescending(r => r.TotalSales)
                .ToListAsync();

            return sales;
        }

        public async Task<SalesForecastDto> ForecastSales(int monthsAhead)
        {
            // Get last 12 months of sales data
            var twelveMonthsAgo = DateTime.Today.AddMonths(-12);
            var historicalSales = await _context.RiceSales
                .Where(s => s.SaleDate >= twelveMonthsAgo && s.IsActive)
                .GroupBy(s => new { s.SaleDate.Year, s.SaleDate.Month })
                .Select(g => new
                {
                    Period = new DateTime(g.Key.Year, g.Key.Month, 1),
                    TotalSales = g.Sum(s => s.TotalAmount)
                })
                .OrderBy(s => s.Period)
                .ToListAsync();

            if (!historicalSales.Any())
            {
                return new SalesForecastDto
                {
                    ForecastPeriod = DateTime.Today.AddMonths(monthsAhead),
                    ForecastedAmount = 0,
                    ConfidenceLower = 0,
                    ConfidenceUpper = 0,
                    Method = "Insufficient Data"
                };
            }

            // Simple moving average forecast
            var averageMonthlySales = historicalSales.Average(s => s.TotalSales);
            var stdDev = CalculateStandardDeviation(historicalSales.Select(s => s.TotalSales).ToList());

            return new SalesForecastDto
            {
                ForecastPeriod = DateTime.Today.AddMonths(monthsAhead),
                ForecastedAmount = averageMonthlySales,
                ConfidenceLower = averageMonthlySales - (stdDev * 1.96m),
                ConfidenceUpper = averageMonthlySales + (stdDev * 1.96m),
                Method = "Simple Moving Average"
            };
        }

        private decimal CalculateStandardDeviation(List<decimal> values)
        {
            if (!values.Any()) return 0;
            var avg = values.Average();
            var sumOfSquares = values.Sum(v => Math.Pow((double)(v - avg), 2));
            return (decimal)Math.Sqrt(sumOfSquares / values.Count);
        }
    }

    #endregion

    #region Task 4: Profit Margin Analysis

    public class ProfitMarginAnalysisService : IProfitMarginAnalysisService
    {
        private readonly ApplicationDbContext _context;

        public ProfitMarginAnalysisService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<ProductProfitabilityDto>> GetProductProfitability(DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Include(s => s.Product)
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .ToListAsync();

            var profitability = sales
                .GroupBy(s => new { s.ProductId, s.Product!.ProductName })
                .Select(g => new ProductProfitabilityDto
                {
                    ProductId = g.Key.ProductId,
                    ProductName = g.Key.ProductName,
                    TotalRevenue = g.Sum(s => s.TotalAmount),
                    TotalCost = g.Sum(s => s.Quantity * (g.First().Product?.CostPrice ?? 0)),
                    GrossProfit = g.Sum(s => s.TotalAmount) - g.Sum(s => s.Quantity * (g.First().Product?.CostPrice ?? 0)),
                    ProfitMargin = 0, // Will calculate below
                    UnitsSold = g.Sum(s => s.Quantity)
                })
                .ToList();

            foreach (var item in profitability)
            {
                item.ProfitMargin = item.TotalRevenue > 0 ? (item.GrossProfit / item.TotalRevenue) * 100 : 0;
            }

            return profitability.OrderByDescending(p => p.GrossProfit).ToList();
        }

        public async Task<List<MarginTrendDto>> GetMarginTrends(DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Include(s => s.Product)
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .ToListAsync();

            var trends = sales
                .GroupBy(s => s.SaleDate.Date)
                .Select(g => new MarginTrendDto
                {
                    Date = g.Key,
                    TotalRevenue = g.Sum(s => s.TotalAmount),
                    TotalCost = g.Sum(s => s.Quantity * (s.Product?.CostPrice ?? 0)),
                    GrossMargin = 0 // Will calculate below
                })
                .OrderBy(t => t.Date)
                .ToList();

            foreach (var trend in trends)
            {
                trend.GrossMargin = trend.TotalRevenue > 0
                    ? ((trend.TotalRevenue - trend.TotalCost) / trend.TotalRevenue) * 100
                    : 0;
            }

            return trends;
        }

        public async Task<decimal> CalculateOverallProfitMargin(DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Include(s => s.Product)
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .ToListAsync();

            var totalRevenue = sales.Sum(s => s.TotalAmount);
            var totalCost = sales.Sum(s => s.Quantity * (s.Product?.CostPrice ?? 0));
            var grossProfit = totalRevenue - totalCost;

            return totalRevenue > 0 ? (grossProfit / totalRevenue) * 100 : 0;
        }
    }

    #endregion

    #region Task 5: Customer Behavior Analytics

    public class CustomerBehaviorAnalyticsService : ICustomerBehaviorAnalyticsService
    {
        private readonly ApplicationDbContext _context;

        public CustomerBehaviorAnalyticsService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<CustomerSegmentDto>> GetCustomerSegments()
        {
            var sixMonthsAgo = DateTime.Today.AddMonths(-6);
            var sales = await _context.RiceSales
                .Where(s => s.SaleDate >= sixMonthsAgo && s.IsActive)
                .GroupBy(s => s.CustomerId)
                .Select(g => new
                {
                    CustomerId = g.Key,
                    TotalSpent = g.Sum(s => s.TotalAmount),
                    OrderCount = g.Count(),
                    LastPurchase = g.Max(s => s.SaleDate)
                })
                .ToListAsync();

            // RFM Analysis (Recency, Frequency, Monetary)
            var segments = new List<CustomerSegmentDto>();
            var avgSpent = sales.Any() ? sales.Average(s => s.TotalSpent) : 0;
            var avgOrders = sales.Any() ? sales.Average(s => s.OrderCount) : 0;

            foreach (var sale in sales)
            {
                var recencyDays = (DateTime.Today - sale.LastPurchase).Days;
                string segment;

                if (sale.TotalSpent > avgSpent * 1.5m && recencyDays < 60)
                    segment = "VIP";
                else if (sale.TotalSpent > avgSpent && recencyDays < 90)
                    segment = "High Value";
                else if (sale.OrderCount > avgOrders && recencyDays < 90)
                    segment = "Frequent Buyer";
                else if (recencyDays > 180)
                    segment = "At Risk";
                else
                    segment = "Regular";

                var customer = await _context.Customers.FindAsync(sale.CustomerId);

                segments.Add(new CustomerSegmentDto
                {
                    CustomerId = sale.CustomerId,
                    CustomerName = customer?.CompanyName ?? "Unknown",
                    Segment = segment,
                    TotalSpent = sale.TotalSpent,
                    OrderCount = sale.OrderCount,
                    RecencyDays = recencyDays
                });
            }

            return segments.OrderByDescending(s => s.TotalSpent).ToList();
        }

        public async Task<List<CustomerRetentionDto>> AnalyzeCustomerRetention(DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .GroupBy(s => s.CustomerId)
                .Select(g => new
                {
                    CustomerId = g.Key,
                    FirstPurchase = g.Min(s => s.SaleDate),
                    LastPurchase = g.Max(s => s.SaleDate),
                    OrderCount = g.Count()
                })
                .ToListAsync();

            var retentionData = new List<CustomerRetentionDto>();

            foreach (var sale in sales)
            {
                var daysSinceFirst = (DateTime.Today - sale.FirstPurchase).Days;
                var retention = sale.OrderCount > 1 ? "Retained" : "One-Time";

                var customer = await _context.Customers.FindAsync(sale.CustomerId);

                retentionData.Add(new CustomerRetentionDto
                {
                    CustomerId = sale.CustomerId,
                    CustomerName = customer?.CompanyName ?? "Unknown",
                    FirstPurchaseDate = sale.FirstPurchase,
                    LastPurchaseDate = sale.LastPurchase,
                    TotalOrders = sale.OrderCount,
                    RetentionStatus = retention,
                    DaysSinceFirstPurchase = daysSinceFirst
                });
            }

            return retentionData.OrderByDescending(r => r.TotalOrders).ToList();
        }

        public async Task<decimal> CalculateCustomerLifetimeValue(int customerId)
        {
            var sales = await _context.RiceSales
                .Where(s => s.CustomerId == customerId && s.IsActive)
                .ToListAsync();

            return sales.Sum(s => s.TotalAmount);
        }

        public async Task<List<ChurnRiskDto>> PredictCustomerChurn()
        {
            var ninetyDaysAgo = DateTime.Today.AddDays(-90);
            var oneYearAgo = DateTime.Today.AddDays(-365);

            var recentSales = await _context.RiceSales
                .Where(s => s.SaleDate >= ninetyDaysAgo && s.IsActive)
                .Select(s => s.CustomerId)
                .Distinct()
                .ToListAsync();

            var historicalCustomers = await _context.RiceSales
                .Where(s => s.SaleDate >= oneYearAgo && s.SaleDate < ninetyDaysAgo && s.IsActive)
                .Select(s => s.CustomerId)
                .Distinct()
                .ToListAsync();

            var atRiskCustomers = historicalCustomers.Except(recentSales).ToList();

            var churnRisks = new List<ChurnRiskDto>();

            foreach (var customerId in atRiskCustomers)
            {
                var customer = await _context.Customers.FindAsync(customerId);
                var lastSale = await _context.RiceSales
                    .Where(s => s.CustomerId == customerId && s.IsActive)
                    .OrderByDescending(s => s.SaleDate)
                    .FirstOrDefaultAsync();

                if (lastSale != null)
                {
                    var daysSinceLastPurchase = (DateTime.Today - lastSale.SaleDate).Days;

                    churnRisks.Add(new ChurnRiskDto
                    {
                        CustomerId = customerId,
                        CustomerName = customer?.CompanyName ?? "Unknown",
                        DaysSinceLastPurchase = daysSinceLastPurchase,
                        ChurnRisk = daysSinceLastPurchase > 180 ? "High" : "Medium",
                        LastPurchaseDate = lastSale.SaleDate,
                        LastPurchaseAmount = lastSale.TotalAmount
                    });
                }
            }

            return churnRisks.OrderByDescending(c => c.DaysSinceLastPurchase).ToList();
        }
    }

    #endregion

    #region Task 6: Supplier Performance

    public class SupplierPerformanceService : ISupplierPerformanceService
    {
        private readonly ApplicationDbContext _context;

        public SupplierPerformanceService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<SupplierPerformanceDto>> GetSupplierPerformance(DateTime startDate, DateTime endDate)
        {
            var procurement = await _context.PaddyProcurements
                .Include(p => p.Vendor)
                .Where(p => p.ProcurementDate >= startDate && p.ProcurementDate <= endDate && p.IsActive)
                .GroupBy(p => p.VendorId)
                .Select(g => new SupplierPerformanceDto
                {
                    SupplierId = g.Key,
                    SupplierName = g.First().Vendor!.CompanyName,
                    TotalOrders = g.Count(),
                    TotalValue = g.Sum(p => p.TotalAmount),
                    AverageOrderValue = g.Average(p => p.TotalAmount),
                    OnTimeDeliveries = g.Count(), // Simplified - would need delivery tracking
                    OnTimePercentage = 100, // Simplified
                    QualityScore = 8.5m // Simplified - would need quality tracking
                })
                .OrderByDescending(s => s.TotalValue)
                .ToListAsync();

            return procurement;
        }

        public async Task<List<SupplierReliabilityDto>> AssessSupplierReliability()
        {
            var sixMonthsAgo = DateTime.Today.AddMonths(-6);
            var procurement = await _context.PaddyProcurements
                .Include(p => p.Vendor)
                .Where(p => p.ProcurementDate >= sixMonthsAgo && p.IsActive)
                .GroupBy(p => p.VendorId)
                .Select(g => new SupplierReliabilityDto
                {
                    SupplierId = g.Key,
                    SupplierName = g.First().Vendor!.CompanyName,
                    TotalOrders = g.Count(),
                    SuccessfulDeliveries = g.Count(), // Simplified
                    ReliabilityScore = 95m, // Simplified
                    AverageLeadTime = 7, // Simplified - would need actual tracking
                    DefectRate = 2m // Simplified
                })
                .OrderByDescending(s => s.ReliabilityScore)
                .ToListAsync();

            return procurement;
        }

        public async Task<List<SupplierCostComparisonDto>> CompareSupplierCosts(int productId)
        {
            var sixMonthsAgo = DateTime.Today.AddMonths(-6);

            // Get paddy procurements
            var procurements = await _context.PaddyProcurements
                .Include(p => p.Vendor)
                .Where(p => p.ProcurementDate >= sixMonthsAgo && p.IsActive)
                .GroupBy(p => p.VendorId)
                .Select(g => new SupplierCostComparisonDto
                {
                    SupplierId = g.Key,
                    SupplierName = g.First().Vendor!.CompanyName,
                    AverageUnitCost = g.Average(p => p.RatePerKg),
                    TotalQuantity = g.Sum(p => p.Quantity),
                    TotalSpent = g.Sum(p => p.TotalAmount),
                    OrderCount = g.Count()
                })
                .OrderBy(s => s.AverageUnitCost)
                .ToListAsync();

            return procurements;
        }
    }

    #endregion

    #region Task 11: Cost Analysis

    public class CostAnalysisService : ICostAnalysisService
    {
        private readonly ApplicationDbContext _context;

        public CostAnalysisService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<CostBreakdownDto> GetCostBreakdown(DateTime startDate, DateTime endDate)
        {
            // Material costs (paddy procurement)
            var materialCosts = await _context.PaddyProcurements
                .Where(p => p.ProcurementDate >= startDate && p.ProcurementDate <= endDate && p.IsActive)
                .SumAsync(p => p.TotalAmount);

            // Labor costs (simplified - would need actual payroll data)
            var laborCosts = 0m;

            // Overhead costs (simplified)
            var overheadCosts = 0m;

            // Production costs (from batches)
            var productionCosts = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Where(b => b.BatchDate >= startDate && b.BatchDate <= endDate && b.IsActive)
                .SelectMany(b => b.Inputs)
                .SumAsync(i => i.TotalCost);

            var totalCosts = materialCosts + laborCosts + overheadCosts + productionCosts;

            return new CostBreakdownDto
            {
                MaterialCosts = materialCosts,
                LaborCosts = laborCosts,
                OverheadCosts = overheadCosts,
                ProductionCosts = productionCosts,
                TotalCosts = totalCosts,
                MaterialPercentage = totalCosts > 0 ? (materialCosts / totalCosts) * 100 : 0,
                LaborPercentage = totalCosts > 0 ? (laborCosts / totalCosts) * 100 : 0,
                OverheadPercentage = totalCosts > 0 ? (overheadCosts / totalCosts) * 100 : 0,
                ProductionPercentage = totalCosts > 0 ? (productionCosts / totalCosts) * 100 : 0
            };
        }

        public async Task<List<CostVarianceDto>> AnalyzeCostVariance(DateTime startDate, DateTime endDate)
        {
            var variances = new List<CostVarianceDto>();

            // Compare actual costs vs expected (simplified)
            var actualMaterialCost = await _context.PaddyProcurements
                .Where(p => p.ProcurementDate >= startDate && p.ProcurementDate <= endDate && p.IsActive)
                .SumAsync(p => p.TotalAmount);

            // Expected cost (simplified - would use budget data)
            var expectedMaterialCost = actualMaterialCost * 0.95m;

            variances.Add(new CostVarianceDto
            {
                CostCategory = "Material Costs",
                ExpectedCost = expectedMaterialCost,
                ActualCost = actualMaterialCost,
                Variance = actualMaterialCost - expectedMaterialCost,
                VariancePercentage = expectedMaterialCost > 0
                    ? ((actualMaterialCost - expectedMaterialCost) / expectedMaterialCost) * 100
                    : 0
            });

            return variances;
        }

        public async Task<List<ProductCostDto>> GetProductCostAnalysis()
        {
            var products = await _context.Products
                .Where(p => p.IsActive)
                .Select(p => new ProductCostDto
                {
                    ProductId = p.Id,
                    ProductName = p.ProductName,
                    UnitCost = p.CostPrice,
                    SellingPrice = p.SellingPrice,
                    GrossMargin = p.SellingPrice > 0
                        ? ((p.SellingPrice - p.CostPrice) / p.SellingPrice) * 100
                        : 0
                })
                .OrderByDescending(p => p.GrossMargin)
                .ToListAsync();

            return products;
        }
    }

    #endregion

    #region Task 12: Business Intelligence

    public class BusinessIntelligenceService : IBusinessIntelligenceService
    {
        private readonly ApplicationDbContext _context;

        public BusinessIntelligenceService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<BusinessDashboardDto> GetComprehensiveDashboard()
        {
            var dashboard = new BusinessDashboardDto();

            // Sales metrics
            var today = DateTime.Today;
            var thisMonth = new DateTime(today.Year, today.Month, 1);
            var lastMonth = thisMonth.AddMonths(-1);

            var currentMonthSales = await _context.RiceSales
                .Where(s => s.SaleDate >= thisMonth && s.IsActive)
                .SumAsync(s => s.TotalAmount);

            var lastMonthSales = await _context.RiceSales
                .Where(s => s.SaleDate >= lastMonth && s.SaleDate < thisMonth && s.IsActive)
                .SumAsync(s => s.TotalAmount);

            dashboard.TotalRevenue = currentMonthSales;
            dashboard.RevenueGrowth = lastMonthSales > 0
                ? ((currentMonthSales - lastMonthSales) / lastMonthSales) * 100
                : 0;

            // Inventory value
            dashboard.InventoryValue = await _context.InventoryLedgers
                .Where(i => i.IsActive)
                .SumAsync(i => i.TotalValue);

            // Customer metrics
            dashboard.TotalCustomers = await _context.Customers.CountAsync(c => c.IsActive);
            dashboard.ActiveCustomers = await _context.RiceSales
                .Where(s => s.SaleDate >= thisMonth && s.IsActive)
                .Select(s => s.CustomerId)
                .Distinct()
                .CountAsync();

            // Production metrics
            dashboard.ProductionBatches = await _context.ProductionBatches
                .Where(b => b.BatchDate >= thisMonth && b.IsActive)
                .CountAsync();

            dashboard.AverageEfficiency = await _context.ProductionBatches
                .Where(b => b.BatchDate >= thisMonth
                    && b.IsActive
                    && (b.Status == "Completed" || b.Status == "Verified"))
                .Select(b => b.TotalInputQuantity > 0
                    ? (b.TotalOutputQuantity / b.TotalInputQuantity) * 100
                    : 0)
                .AverageAsync();

            // Pending orders
            dashboard.PendingOrders = await _context.ProductionOrders
                .CountAsync(o => o.Status == "Pending" && o.IsActive);

            return dashboard;
        }

        public async Task<List<KPIDto>> GetKeyPerformanceIndicators(DateTime startDate, DateTime endDate)
        {
            var kpis = new List<KPIDto>();

            // Revenue KPI
            var revenue = await _context.RiceSales
                .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate && s.IsActive)
                .SumAsync(s => s.TotalAmount);

            kpis.Add(new KPIDto
            {
                Name = "Total Revenue",
                Value = revenue,
                Unit = "Currency",
                Target = revenue * 1.1m, // 10% higher target
                Achievement = 91m,
                Trend = "Up"
            });

            // Inventory Turnover KPI
            var avgInventory = await _context.InventoryLedgers
                .Where(i => i.IsActive)
                .AverageAsync(i => i.TotalValue);

            var cogs = await _context.StockMovements
                .Where(m => m.MovementDate >= startDate
                    && m.MovementDate <= endDate
                    && m.MovementType == "OUT"
                    && m.IsActive)
                .SumAsync(m => m.TotalCost);

            var turnover = avgInventory > 0 ? cogs / avgInventory : 0;

            kpis.Add(new KPIDto
            {
                Name = "Inventory Turnover",
                Value = turnover,
                Unit = "Ratio",
                Target = 12m,
                Achievement = turnover > 0 ? (turnover / 12m) * 100 : 0,
                Trend = turnover > 10 ? "Up" : "Down"
            });

            // Production Efficiency KPI
            var efficiency = await _context.ProductionBatches
                .Where(b => b.BatchDate >= startDate
                    && b.BatchDate <= endDate
                    && b.IsActive
                    && (b.Status == "Completed" || b.Status == "Verified"))
                .Select(b => b.TotalInputQuantity > 0
                    ? (b.TotalOutputQuantity / b.TotalInputQuantity) * 100
                    : 0)
                .AverageAsync();

            kpis.Add(new KPIDto
            {
                Name = "Production Efficiency",
                Value = efficiency,
                Unit = "Percentage",
                Target = 95m,
                Achievement = efficiency > 0 ? (efficiency / 95m) * 100 : 0,
                Trend = efficiency > 90 ? "Up" : "Down"
            });

            return kpis;
        }

        public async Task<List<BusinessAlertDto>> GetBusinessAlerts()
        {
            var alerts = new List<BusinessAlertDto>();

            // Low stock alert
            var lowStockCount = await _context.InventoryLedgers
                .CountAsync(i => i.IsActive && i.CurrentStock <= i.MinimumLevel);

            if (lowStockCount > 0)
            {
                alerts.Add(new BusinessAlertDto
                {
                    AlertType = "Low Stock",
                    Severity = "High",
                    Message = $"{lowStockCount} products are below minimum stock level",
                    ActionRequired = "Review and place purchase orders",
                    CreatedDate = DateTime.Now
                });
            }

            // Pending orders alert
            var pendingOrders = await _context.ProductionOrders
                .CountAsync(o => o.Status == "Pending" && o.IsActive);

            if (pendingOrders > 10)
            {
                alerts.Add(new BusinessAlertDto
                {
                    AlertType = "Pending Orders",
                    Severity = "Medium",
                    Message = $"{pendingOrders} production orders are pending",
                    ActionRequired = "Review and schedule production",
                    CreatedDate = DateTime.Now
                });
            }

            return alerts.OrderByDescending(a => a.Severity).ToList();
        }
    }

    #endregion
}
