using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;

namespace RMMS.Services.Services.Analytics.Implementations
{
    public class InventoryAnalyticsService : IInventoryAnalyticsService
    {
        private readonly ApplicationDbContext _context;

        public InventoryAnalyticsService(ApplicationDbContext context)
        {
            _context = context;
        }

        #region Task 2: Real-time Inventory Analytics

        public async Task<InventoryDashboardDto> GetInventoryDashboard()
        {
            var dashboard = new InventoryDashboardDto();

            // Get current stock summary from InventoryLedger (snapshot table)
            var currentStock = await _context.InventoryLedgers
                .Where(i => i.IsActive)
                .GroupBy(i => new { i.ProductId, i.WarehouseId })
                .Select(g => new
                {
                    g.Key.ProductId,
                    g.Key.WarehouseId,
                    CurrentStock = g.Sum(i => i.CurrentStock),
                    Value = g.Sum(i => i.TotalValue)
                })
                .ToListAsync();

            dashboard.TotalInventoryValue = currentStock.Sum(s => s.Value);
            dashboard.TotalSKUs = currentStock.Select(s => s.ProductId).Distinct().Count();

            // Calculate inventory turnover
            var oneYearAgo = DateTime.Today.AddYears(-1);
            dashboard.InventoryTurnoverRatio = await CalculateInventoryTurnoverRatio(oneYearAgo, DateTime.Today);
            dashboard.DaysInventoryOutstanding = await CalculateDaysInventoryOutstanding(oneYearAgo, DateTime.Today);

            // Get reorder alerts
            var reorderPoints = await CalculateReorderPoints();
            dashboard.LowStockItems = reorderPoints.Count(r => r.RequiresReorder && r.UrgencyLevel == "High");
            dashboard.OutOfStockItems = reorderPoints.Count(r => r.CurrentStock <= 0);

            // Get aging analysis
            dashboard.AgingAnalysis = await GetStockAgingAnalysis();
            dashboard.DeadStockItems = dashboard.AgingAnalysis.Count(a => a.DaysInStock > 180);

            // Get ABC classification
            dashboard.ABCAnalysis = await GetABCClassification(oneYearAgo, DateTime.Today);

            // Get top reorder alerts
            dashboard.ReorderAlerts = reorderPoints
                .Where(r => r.RequiresReorder)
                .OrderBy(r => r.DaysUntilStockout)
                .Take(10)
                .ToList();

            return dashboard;
        }

        public async Task<List<StockAgingDto>> GetStockAgingAnalysis()
        {
            var stockAging = new List<StockAgingDto>();

            var inventoryData = await _context.InventoryLedgers
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Where(i => i.IsActive && i.CurrentStock > 0)
                .Select(i => new
                {
                    i.ProductId,
                    i.WarehouseId,
                    ProductName = i.Product!.ProductName,
                    WarehouseName = i.Warehouse!.WarehouseName,
                    i.CurrentStock,
                    LastMovement = i.LastMovementDate ?? i.CreatedDate,
                    i.UnitCost
                })
                .ToListAsync();

            foreach (var item in inventoryData)
            {
                var daysInStock = (DateTime.Today - item.LastMovement).Days;
                var agingBucket = GetAgingBucket(daysInStock);

                stockAging.Add(new StockAgingDto
                {
                    ProductId = item.ProductId,
                    ProductName = item.ProductName ?? "Unknown",
                    WarehouseId = item.WarehouseId,
                    WarehouseName = item.WarehouseName ?? "Unknown",
                    CurrentStock = item.CurrentStock,
                    DaysInStock = daysInStock,
                    AgingBucket = agingBucket,
                    StockValue = item.CurrentStock * item.UnitCost,
                    OldestStockDate = item.LastMovement
                });
            }

            return stockAging.OrderByDescending(s => s.DaysInStock).ToList();
        }

        private string GetAgingBucket(int days)
        {
            if (days <= 30) return "0-30 days";
            if (days <= 60) return "31-60 days";
            if (days <= 90) return "61-90 days";
            if (days <= 120) return "91-120 days";
            if (days <= 180) return "121-180 days";
            return "180+ days";
        }

        public async Task<List<ABCClassificationDto>> GetABCClassification(DateTime startDate, DateTime endDate)
        {
            // Use StockMovement for historical transaction data
            var consumption = await _context.StockMovements
                .Where(m => m.MovementDate >= startDate
                    && m.MovementDate <= endDate
                    && m.MovementType == "OUT"
                    && m.IsActive)
                .GroupBy(m => m.ProductId)
                .Select(g => new
                {
                    ProductId = g.Key,
                    ConsumptionValue = g.Sum(m => m.TotalCost),
                    ConsumptionQuantity = g.Sum(m => m.Quantity)
                })
                .OrderByDescending(x => x.ConsumptionValue)
                .ToListAsync();

            var totalValue = consumption.Sum(c => c.ConsumptionValue);
            var abcList = new List<ABCClassificationDto>();
            decimal cumulativePercentage = 0;

            foreach (var item in consumption)
            {
                var product = await _context.Products.FindAsync(item.ProductId);
                var valuePercentage = totalValue > 0 ? (item.ConsumptionValue / totalValue) * 100 : 0;
                cumulativePercentage += valuePercentage;

                string classification;
                if (cumulativePercentage <= 70) classification = "A";
                else if (cumulativePercentage <= 90) classification = "B";
                else classification = "C";

                abcList.Add(new ABCClassificationDto
                {
                    ProductId = item.ProductId,
                    ProductName = product?.ProductName ?? "Unknown",
                    ConsumptionValue = item.ConsumptionValue,
                    ConsumptionQuantity = item.ConsumptionQuantity,
                    ValuePercentage = valuePercentage,
                    CumulativePercentage = cumulativePercentage,
                    Classification = classification
                });
            }

            return abcList;
        }

        public async Task<List<ReorderPointDto>> CalculateReorderPoints()
        {
            var reorderPoints = new List<ReorderPointDto>();

            var inventoryItems = await _context.InventoryLedgers
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Where(i => i.IsActive)
                .ToListAsync();

            foreach (var item in inventoryItems)
            {
                // Calculate average daily consumption from last 90 days
                var ninetyDaysAgo = DateTime.Today.AddDays(-90);
                var movements = await _context.StockMovements
                    .Where(m => m.ProductId == item.ProductId
                        && m.WarehouseId == item.WarehouseId
                        && m.MovementDate >= ninetyDaysAgo
                        && m.MovementType == "OUT"
                        && m.IsActive)
                    .ToListAsync();

                var totalConsumption = movements.Sum(m => m.Quantity);
                var averageDailyConsumption = movements.Any() ? totalConsumption / 90 : 0;

                var leadTimeDays = 7; // Default lead time
                var safetyStock = averageDailyConsumption * 3; // 3 days safety stock

                var calculatedReorderPoint = (averageDailyConsumption * leadTimeDays) + safetyStock;
                var requiresReorder = item.CurrentStock <= calculatedReorderPoint;
                var daysUntilStockout = averageDailyConsumption > 0
                    ? (int)(item.CurrentStock / averageDailyConsumption)
                    : 999;

                string urgencyLevel;
                if (item.CurrentStock <= 0) urgencyLevel = "Critical";
                else if (daysUntilStockout <= 3) urgencyLevel = "High";
                else if (daysUntilStockout <= 7) urgencyLevel = "Medium";
                else urgencyLevel = "Low";

                reorderPoints.Add(new ReorderPointDto
                {
                    ProductId = item.ProductId,
                    ProductName = item.Product?.ProductName ?? "Unknown",
                    WarehouseId = item.WarehouseId,
                    WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                    CurrentStock = item.CurrentStock,
                    ReorderPoint = calculatedReorderPoint,
                    SafetyStock = safetyStock,
                    LeadTimeDays = leadTimeDays,
                    AverageDailyConsumption = averageDailyConsumption,
                    RequiresReorder = requiresReorder,
                    DaysUntilStockout = daysUntilStockout,
                    UrgencyLevel = urgencyLevel
                });
            }

            return reorderPoints.OrderBy(r => r.DaysUntilStockout).ToList();
        }

        public async Task<List<DemandForecastDto>> ForecastDemand(int months)
        {
            var forecasts = new List<DemandForecastDto>();

            // Get historical data for the last 12 months
            var twelveMonthsAgo = DateTime.Today.AddMonths(-12);
            var movements = await _context.StockMovements
                .Where(m => m.MovementDate >= twelveMonthsAgo
                    && m.MovementType == "OUT"
                    && m.IsActive)
                .GroupBy(m => new { m.ProductId, Month = m.MovementDate.Month, Year = m.MovementDate.Year })
                .Select(g => new
                {
                    g.Key.ProductId,
                    g.Key.Month,
                    g.Key.Year,
                    Quantity = g.Sum(m => m.Quantity)
                })
                .ToListAsync();

            var products = await _context.Products.Where(p => p.IsActive).ToListAsync();

            foreach (var product in products)
            {
                var productMovements = movements.Where(m => m.ProductId == product.Id).ToList();

                if (!productMovements.Any()) continue;

                var averageMonthlyDemand = productMovements.Average(m => m.Quantity);
                var stdDeviation = CalculateStandardDeviation(productMovements.Select(m => m.Quantity).ToList());

                for (int i = 1; i <= months; i++)
                {
                    var forecastDate = DateTime.Today.AddMonths(i);
                    var seasonalityFactor = GetSeasonalityFactor(forecastDate.Month);
                    var forecastedDemand = averageMonthlyDemand * seasonalityFactor;

                    forecasts.Add(new DemandForecastDto
                    {
                        ProductId = product.Id,
                        ProductName = product.ProductName,
                        ForecastMonth = forecastDate,
                        ForecastedDemand = forecastedDemand,
                        ConfidenceLower = forecastedDemand - (stdDeviation * 1.96m),
                        ConfidenceUpper = forecastedDemand + (stdDeviation * 1.96m),
                        Method = "Simple Moving Average with Seasonality"
                    });
                }
            }

            return forecasts;
        }

        private decimal CalculateStandardDeviation(List<decimal> values)
        {
            if (!values.Any()) return 0;

            var avg = values.Average();
            var sumOfSquares = values.Sum(v => Math.Pow((double)(v - avg), 2));
            return (decimal)Math.Sqrt(sumOfSquares / values.Count);
        }

        private decimal GetSeasonalityFactor(int month)
        {
            // Default seasonality factors (can be customized based on business)
            return month switch
            {
                1 => 1.1m,  // January - higher
                2 => 1.0m,
                3 => 1.0m,
                4 => 0.9m,  // April - lower
                5 => 0.9m,
                6 => 0.95m,
                7 => 1.0m,
                8 => 1.0m,
                9 => 1.05m,
                10 => 1.1m, // October - higher
                11 => 1.15m, // November - highest
                12 => 1.2m, // December - highest
                _ => 1.0m
            };
        }

        public async Task<StockValuationDto> GetStockValuation(string method = "FIFO")
        {
            var valuations = await GetStockValuationList(method);

            return new StockValuationDto
            {
                ProductId = 0,
                ProductName = "All Products",
                WarehouseId = 0,
                WarehouseName = "All Warehouses",
                Quantity = valuations.Sum(v => v.Quantity),
                ValuationMethod = method,
                ValuationAmount = valuations.Sum(v => v.ValuationAmount),
                UnitCost = valuations.Sum(v => v.Quantity) > 0
                    ? valuations.Sum(v => v.ValuationAmount) / valuations.Sum(v => v.Quantity)
                    : 0
            };
        }

        private async Task<List<StockValuationDto>> GetStockValuationList(string method)
        {
            var valuations = new List<StockValuationDto>();

            var inventoryItems = await _context.InventoryLedgers
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Where(i => i.IsActive && i.CurrentStock > 0)
                .ToListAsync();

            foreach (var item in inventoryItems)
            {
                decimal valuationAmount = 0;

                switch (method.ToUpper())
                {
                    case "FIFO":
                        valuationAmount = await CalculateFIFOValuation(item.ProductId, item.WarehouseId, item.CurrentStock);
                        break;
                    case "LIFO":
                        valuationAmount = await CalculateLIFOValuation(item.ProductId, item.WarehouseId, item.CurrentStock);
                        break;
                    case "WEIGHTED":
                    default:
                        valuationAmount = item.TotalValue; // Already calculated as weighted average
                        break;
                }

                valuations.Add(new StockValuationDto
                {
                    ProductId = item.ProductId,
                    ProductName = item.Product?.ProductName ?? "Unknown",
                    WarehouseId = item.WarehouseId,
                    WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                    Quantity = item.CurrentStock,
                    ValuationMethod = method,
                    ValuationAmount = valuationAmount,
                    UnitCost = item.CurrentStock > 0 ? valuationAmount / item.CurrentStock : 0
                });
            }

            return valuations;
        }

        private async Task<decimal> CalculateFIFOValuation(int productId, int warehouseId, decimal quantity)
        {
            // Get stock IN movements ordered by date (oldest first)
            var stockIns = await _context.StockMovements
                .Where(m => m.ProductId == productId
                    && m.WarehouseId == warehouseId
                    && m.MovementType == "IN"
                    && m.IsActive)
                .OrderBy(m => m.MovementDate)
                .Select(m => new { m.Quantity, m.UnitCost })
                .ToListAsync();

            decimal remainingQty = quantity;
            decimal totalValue = 0;

            foreach (var stockIn in stockIns)
            {
                if (remainingQty <= 0) break;

                var qtyToValue = Math.Min(remainingQty, stockIn.Quantity);
                totalValue += qtyToValue * stockIn.UnitCost;
                remainingQty -= qtyToValue;
            }

            return totalValue;
        }

        private async Task<decimal> CalculateLIFOValuation(int productId, int warehouseId, decimal quantity)
        {
            // Get stock IN movements ordered by date (newest first)
            var stockIns = await _context.StockMovements
                .Where(m => m.ProductId == productId
                    && m.WarehouseId == warehouseId
                    && m.MovementType == "IN"
                    && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .Select(m => new { m.Quantity, m.UnitCost })
                .ToListAsync();

            decimal remainingQty = quantity;
            decimal totalValue = 0;

            foreach (var stockIn in stockIns)
            {
                if (remainingQty <= 0) break;

                var qtyToValue = Math.Min(remainingQty, stockIn.Quantity);
                totalValue += qtyToValue * stockIn.UnitCost;
                remainingQty -= qtyToValue;
            }

            return totalValue;
        }

        #endregion

        #region Task 10: Inventory Movement Classification & Alerts

        public async Task<List<StockMovementClassificationDto>> ClassifyStockMovements(DateTime startDate, DateTime endDate)
        {
            var movements = await _context.StockMovements
                .Include(m => m.Product)
                .Where(m => m.MovementDate >= startDate && m.MovementDate <= endDate && m.IsActive)
                .GroupBy(m => new { m.MovementType, m.MovementCategory })
                .Select(g => new StockMovementClassificationDto
                {
                    MovementType = g.Key.MovementType,
                    Category = g.Key.MovementCategory,
                    TotalMovements = g.Count(),
                    TotalQuantity = g.Sum(m => m.Quantity),
                    TotalValue = g.Sum(m => m.TotalCost),
                    AverageValue = g.Average(m => m.TotalCost)
                })
                .ToListAsync();

            return movements;
        }

        public async Task<List<StockAlertDto>> GetStockAlerts()
        {
            var alerts = new List<StockAlertDto>();

            var inventoryItems = await _context.InventoryLedgers
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Where(i => i.IsActive)
                .ToListAsync();

            foreach (var item in inventoryItems)
            {
                // Out of stock alert
                if (item.CurrentStock <= 0)
                {
                    alerts.Add(new StockAlertDto
                    {
                        ProductId = item.ProductId,
                        ProductName = item.Product?.ProductName ?? "Unknown",
                        WarehouseId = item.WarehouseId,
                        WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                        AlertType = "Out of Stock",
                        Severity = "Critical",
                        CurrentStock = item.CurrentStock,
                        Threshold = 0,
                        Message = $"{item.Product?.ProductName} is out of stock at {item.Warehouse?.WarehouseName}",
                        AlertDate = DateTime.Now
                    });
                }
                // Low stock alert
                else if (item.CurrentStock <= item.MinimumLevel)
                {
                    alerts.Add(new StockAlertDto
                    {
                        ProductId = item.ProductId,
                        ProductName = item.Product?.ProductName ?? "Unknown",
                        WarehouseId = item.WarehouseId,
                        WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                        AlertType = "Low Stock",
                        Severity = "High",
                        CurrentStock = item.CurrentStock,
                        Threshold = item.MinimumLevel,
                        Message = $"{item.Product?.ProductName} is below minimum level at {item.Warehouse?.WarehouseName}",
                        AlertDate = DateTime.Now
                    });
                }
                // Reorder point alert
                else if (item.CurrentStock <= item.ReorderLevel)
                {
                    alerts.Add(new StockAlertDto
                    {
                        ProductId = item.ProductId,
                        ProductName = item.Product?.ProductName ?? "Unknown",
                        WarehouseId = item.WarehouseId,
                        WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                        AlertType = "Reorder Required",
                        Severity = "Medium",
                        CurrentStock = item.CurrentStock,
                        Threshold = item.ReorderLevel,
                        Message = $"{item.Product?.ProductName} needs reordering at {item.Warehouse?.WarehouseName}",
                        AlertDate = DateTime.Now
                    });
                }
                // Overstock alert
                else if (item.CurrentStock >= item.MaximumLevel)
                {
                    alerts.Add(new StockAlertDto
                    {
                        ProductId = item.ProductId,
                        ProductName = item.Product?.ProductName ?? "Unknown",
                        WarehouseId = item.WarehouseId,
                        WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                        AlertType = "Overstock",
                        Severity = "Low",
                        CurrentStock = item.CurrentStock,
                        Threshold = item.MaximumLevel,
                        Message = $"{item.Product?.ProductName} is overstocked at {item.Warehouse?.WarehouseName}",
                        AlertDate = DateTime.Now
                    });
                }
            }

            return alerts.OrderByDescending(a => a.Severity).ToList();
        }

        public async Task<List<ProductStockoutRiskDto>> PredictStockoutRisk(int daysAhead)
        {
            var riskAnalysis = new List<ProductStockoutRiskDto>();

            var inventoryItems = await _context.InventoryLedgers
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Where(i => i.IsActive && i.CurrentStock > 0)
                .ToListAsync();

            foreach (var item in inventoryItems)
            {
                // Calculate average daily consumption
                var thirtyDaysAgo = DateTime.Today.AddDays(-30);
                var movements = await _context.StockMovements
                    .Where(m => m.ProductId == item.ProductId
                        && m.WarehouseId == item.WarehouseId
                        && m.MovementDate >= thirtyDaysAgo
                        && m.MovementType == "OUT"
                        && m.IsActive)
                    .ToListAsync();

                if (!movements.Any()) continue;

                var averageDailyConsumption = movements.Sum(m => m.Quantity) / 30;
                var projectedStock = item.CurrentStock - (averageDailyConsumption * daysAhead);
                var daysUntilStockout = averageDailyConsumption > 0
                    ? (int)(item.CurrentStock / averageDailyConsumption)
                    : 999;

                string riskLevel;
                if (projectedStock <= 0) riskLevel = "High";
                else if (projectedStock <= item.MinimumLevel) riskLevel = "Medium";
                else riskLevel = "Low";

                riskAnalysis.Add(new ProductStockoutRiskDto
                {
                    ProductId = item.ProductId,
                    ProductName = item.Product?.ProductName ?? "Unknown",
                    WarehouseId = item.WarehouseId,
                    WarehouseName = item.Warehouse?.WarehouseName ?? "Unknown",
                    CurrentStock = item.CurrentStock,
                    AverageDailyConsumption = averageDailyConsumption,
                    ProjectedStock = projectedStock,
                    DaysUntilStockout = daysUntilStockout,
                    RiskLevel = riskLevel,
                    RecommendedOrderQuantity = projectedStock < item.ReorderLevel
                        ? item.MaximumLevel - projectedStock
                        : 0
                });
            }

            return riskAnalysis.OrderBy(r => r.DaysUntilStockout).ToList();
        }

        public async Task<decimal> CalculateInventoryTurnoverRatio(DateTime startDate, DateTime endDate)
        {
            // COGS = Cost of Goods Sold
            var cogs = await _context.StockMovements
                .Where(m => m.MovementDate >= startDate
                    && m.MovementDate <= endDate
                    && m.MovementType == "OUT"
                    && m.MovementCategory == "Sales"
                    && m.IsActive)
                .SumAsync(m => m.TotalCost);

            // Average Inventory = (Beginning Inventory + Ending Inventory) / 2
            var beginningInventory = await _context.InventoryLedgers
                .Where(i => i.IsActive)
                .SumAsync(i => i.TotalValue);

            var endingInventory = beginningInventory; // Simplified - should track historical snapshots

            var averageInventory = (beginningInventory + endingInventory) / 2;

            return averageInventory > 0 ? cogs / averageInventory : 0;
        }

        public async Task<int> CalculateDaysInventoryOutstanding(DateTime startDate, DateTime endDate)
        {
            var turnoverRatio = await CalculateInventoryTurnoverRatio(startDate, endDate);
            return turnoverRatio > 0 ? (int)(365 / turnoverRatio) : 0;
        }

        // Additional methods to satisfy interface
        public async Task<List<StockMovementClassificationDto>> GetStockMovementClassification(DateTime startDate, DateTime endDate)
        {
            return await ClassifyStockMovements(startDate, endDate);
        }

        public async Task<List<DemandForecastDto>> GetDemandForecast(int productId, int months)
        {
            return await ForecastDemand(months);
        }

        public async Task<decimal> CalculateEconomicOrderQuantity(int productId)
        {
            // EOQ = sqrt((2 * Demand * OrderCost) / HoldingCost)
            // Simplified implementation
            var demand = await _context.StockMovements
                .Where(m => m.ProductId == productId && m.MovementType == "OUT" && m.IsActive)
                .SumAsync(m => m.Quantity);

            var orderCost = 100m; // Simplified
            var holdingCost = 10m; // Simplified

            return (decimal)Math.Sqrt((double)((2 * demand * orderCost) / holdingCost));
        }

        public async Task<decimal> CalculateReorderPoint(int productId)
        {
            var reorderPoints = await CalculateReorderPoints();
            return reorderPoints.FirstOrDefault(r => r.ProductId == productId)?.ReorderPoint ?? 0;
        }

        public async Task<List<StockAlertDto>> GenerateAutoReorderSuggestions()
        {
            var reorderPoints = await CalculateReorderPoints();
            return reorderPoints
                .Where(r => r.RequiresReorder)
                .Select(r => new StockAlertDto
                {
                    ProductId = r.ProductId,
                    ProductName = r.ProductName,
                    WarehouseId = r.WarehouseId,
                    WarehouseName = r.WarehouseName,
                    AlertType = "Reorder Required",
                    Severity = r.UrgencyLevel,
                    CurrentStock = r.CurrentStock,
                    Threshold = r.ReorderPoint,
                    Message = $"{r.ProductName} needs reordering - {r.DaysUntilStockout} days until stockout",
                    AlertDate = DateTime.Now
                })
                .ToList();
        }

        #endregion
    }
}
