// =====================================================
// DASHBOARD SERVICE
// =====================================================

// RMMS.Services/DashboardService.cs
using System;
using System.Data;
using System.Collections.Generic;
using System.Linq;
using RMMS.DataAccess.Helpers;
using Microsoft.Extensions.Configuration;
using Microsoft.Data.SqlClient;
using RMMS.Services.Interfaces.Inventory;
using RMMS.Services.Interfaces.Masters;
using RMMS.Services.Interfaces.Production;

namespace RMMS.Services
{
    public interface IDashboardService
    {
        DashboardViewModel GetDashboardData(string username);
        List<ChartData> GetMonthlySalesChart(int year);
        List<ChartData> GetStockByVarietyChart();
        decimal GetTotalReceivables();
        decimal GetTotalPayables();
    }

    public class DashboardService : IDashboardService
    {
        private readonly DatabaseHelper _dbHelper;
        private readonly IWarehouseService? _warehouseService;
        private readonly IInventoryLedgerService? _inventoryLedgerService;
        private readonly IStockMovementService? _stockMovementService;
        private readonly IStockAdjustmentService? _stockAdjustmentService;
        private readonly IProductService? _productService;
        private readonly IMachineService? _machineService;
        private readonly IProductionOrderService? _productionOrderService;
        private readonly IProductionBatchService? _productionBatchService;

        public DashboardService(
            IConfiguration configuration,
            IWarehouseService? warehouseService = null,
            IInventoryLedgerService? inventoryLedgerService = null,
            IStockMovementService? stockMovementService = null,
            IStockAdjustmentService? stockAdjustmentService = null,
            IProductService? productService = null,
            IMachineService? machineService = null,
            IProductionOrderService? productionOrderService = null,
            IProductionBatchService? productionBatchService = null)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
            _warehouseService = warehouseService;
            _inventoryLedgerService = inventoryLedgerService;
            _stockMovementService = stockMovementService;
            _stockAdjustmentService = stockAdjustmentService;
            _productService = productService;
            _machineService = machineService;
            _productionOrderService = productionOrderService;
            _productionBatchService = productionBatchService;
        }

        public DashboardViewModel GetDashboardData(string username)
        {
            try
            {
                var dashboard = new DashboardViewModel();

                // Get summary statistics using stored procedures
                dashboard.TotalPaddyStock = _dbHelper.ExecuteScalar<decimal>("sp_Dashboard_GetTotalPaddyStock");
                dashboard.TotalRiceStock = _dbHelper.ExecuteScalar<decimal>("sp_Dashboard_GetTotalRiceStock");
                dashboard.MonthlyRevenue = _dbHelper.ExecuteScalar<decimal>("sp_Dashboard_GetMonthlyRevenue");
                dashboard.PendingPayments = _dbHelper.ExecuteScalar<int>("sp_Dashboard_GetPendingPaymentsCount");
                dashboard.TotalCustomers = _dbHelper.ExecuteScalar<int>("sp_Dashboard_GetTotalCustomers");
                dashboard.TotalSuppliers = _dbHelper.ExecuteScalar<int>("sp_Dashboard_GetTotalSuppliers");

                // Get recent transactions
                dashboard.RecentTransactions = GetRecentTransactions(5);

                // Get alerts
                dashboard.Alerts = GetSystemAlerts();

                // Get inventory statistics (if services are available)
                if (_warehouseService != null)
                {
                    var warehouses = _warehouseService.GetAllWarehouses();
                    dashboard.TotalWarehouses = warehouses.Count;

                    if (_inventoryLedgerService != null)
                    {
                        dashboard.InventoryByWarehouse = warehouses.Select(w => new InventoryByWarehouse
                        {
                            WarehouseName = w.WarehouseName,
                            TotalValue = _inventoryLedgerService.GetWarehouseInventoryValue(w.Id),
                            Capacity = w.TotalCapacity,
                            UtilizationPercent = w.TotalCapacity > 0 ? (w.UsedCapacity / w.TotalCapacity) * 100 : 0,
                            ProductCount = _inventoryLedgerService.GetInventoryByWarehouse(w.Id).Count
                        }).ToList();
                    }
                }

                if (_inventoryLedgerService != null)
                {
                    dashboard.TotalInventoryValue = _inventoryLedgerService.GetTotalInventoryValue();

                    var lowStockItems = _inventoryLedgerService.GetLowStockItems();
                    dashboard.LowStockItemsCount = lowStockItems.Count;
                    dashboard.LowStockItems = lowStockItems.Take(5).Select(item => new LowStockItem
                    {
                        ProductCode = item.Product?.ProductCode,
                        ProductName = item.Product?.ProductName,
                        WarehouseName = item.Warehouse?.WarehouseName,
                        CurrentStock = item.CurrentStock,
                        MinimumLevel = item.MinimumLevel,
                        ReorderLevel = item.ReorderLevel,
                        ShortageQuantity = item.MinimumLevel - item.CurrentStock
                    }).ToList();

                    dashboard.OverStockItemsCount = _inventoryLedgerService.GetOverStockItems().Count;
                    dashboard.ReorderItemsCount = _inventoryLedgerService.GetReorderItems().Count;
                }

                if (_productService != null)
                {
                    dashboard.TotalProducts = _productService.GetAllProducts().Count;
                }

                if (_stockAdjustmentService != null)
                {
                    dashboard.PendingAdjustmentsCount = _stockAdjustmentService.GetPendingApprovals().Count;
                }

                if (_stockMovementService != null)
                {
                    var recentMovements = _stockMovementService.GetAllMovements().OrderByDescending(m => m.MovementDate).Take(5);
                    dashboard.RecentStockMovements = recentMovements.Select(m => new StockMovementSummary
                    {
                        MovementDate = m.MovementDate,
                        MovementCode = m.MovementCode,
                        MovementType = m.MovementType,
                        ProductName = m.Product?.ProductName,
                        WarehouseName = m.Warehouse?.WarehouseName,
                        Quantity = m.Quantity,
                        Category = m.MovementCategory
                    }).ToList();
                }

                // Add inventory alerts
                if (dashboard.LowStockItemsCount > 0)
                {
                    dashboard.Alerts.Insert(0, new SystemAlert
                    {
                        Type = "Warning",
                        Message = $"{dashboard.LowStockItemsCount} product(s) are below minimum stock level",
                        Severity = "Medium"
                    });
                }

                if (dashboard.PendingAdjustmentsCount > 0)
                {
                    dashboard.Alerts.Insert(0, new SystemAlert
                    {
                        Type = "Info",
                        Message = $"{dashboard.PendingAdjustmentsCount} stock adjustment(s) pending approval",
                        Severity = "Low"
                    });
                }

                // Get production statistics
                if (_machineService != null)
                {
                    var machines = _machineService.GetAllMachines();
                    dashboard.TotalMachines = machines.Count;
                    dashboard.OperationalMachines = machines.Count(m => m.Status == "Operational");
                    dashboard.MaintenanceDueMachines = machines.Count(m => m.NextMaintenanceDue.HasValue && m.NextMaintenanceDue.Value <= DateTime.Now.AddDays(7));
                }

                if (_productionBatchService != null)
                {
                    var today = DateTime.Today;
                    var batches = _productionBatchService.GetAllBatches();

                    dashboard.TodaysBatches = batches.Count(b => b.BatchDate.Date == today);
                    dashboard.ActiveBatches = batches.Count(b => b.Status == "In Progress");
                    dashboard.CompletedBatchesToday = batches.Count(b => b.BatchDate.Date == today && b.Status == "Completed");

                    // Get today's production quantity
                    var todaysBatches = batches.Where(b => b.BatchDate.Date == today && b.Status == "Completed");
                    dashboard.TodaysProductionQuantity = todaysBatches.Sum(b => b.TotalOutputQuantity);

                    // Recent batches
                    dashboard.RecentBatches = batches
                        .OrderByDescending(b => b.BatchDate)
                        .Take(5)
                        .Select(b => new ProductionBatchSummary
                        {
                            BatchNumber = b.BatchNumber,
                            BatchDate = b.BatchDate,
                            Status = b.Status,
                            InputQuantity = b.TotalInputQuantity,
                            OutputQuantity = b.TotalOutputQuantity,
                            YieldPercent = b.YieldRecord?.TotalYieldPercent ?? 0,
                            OperatorName = b.Operator?.EmployeeName ?? "N/A"
                        }).ToList();

                    // Yield analysis for alerts
                    var recentCompletedBatches = batches
                        .Where(b => b.Status == "Completed" && b.YieldRecord != null && b.YieldRecord.TotalYieldPercent > 0)
                        .OrderByDescending(b => b.BatchDate)
                        .Take(10)
                        .ToList();

                    if (recentCompletedBatches.Any())
                    {
                        var avgYield = recentCompletedBatches.Average(b => b.YieldRecord!.TotalYieldPercent);
                        var lowYieldBatches = recentCompletedBatches.Where(b => b.YieldRecord!.TotalYieldPercent < avgYield * 0.9m).ToList();

                        if (lowYieldBatches.Any())
                        {
                            dashboard.Alerts.Insert(0, new SystemAlert
                            {
                                Type = "Warning",
                                Message = $"{lowYieldBatches.Count} recent batch(es) with below-average yield (< {avgYield:F1}%)",
                                Severity = "Medium"
                            });
                        }
                    }
                }

                if (_productionOrderService != null)
                {
                    var orders = _productionOrderService.GetAllProductionOrders();
                    dashboard.PendingProductionOrders = orders.Count(o => o.Status == "Scheduled" || o.Status == "In Progress");
                }

                // Machine maintenance alerts
                if (dashboard.MaintenanceDueMachines > 0)
                {
                    dashboard.Alerts.Insert(0, new SystemAlert
                    {
                        Type = "Warning",
                        Message = $"{dashboard.MaintenanceDueMachines} machine(s) due for maintenance within 7 days",
                        Severity = "High"
                    });
                }

                return dashboard;
            }
            catch (SqlException ex)
            {
                // Return safe default values for dashboard on database error
                return new DashboardViewModel
                {
                    TotalPaddyStock = 0,
                    TotalRiceStock = 0,
                    MonthlyRevenue = 0,
                    PendingPayments = 0,
                    TotalCustomers = 0,
                    TotalSuppliers = 0,
                    RecentTransactions = new List<TransactionSummary>(),
                    Alerts = new List<SystemAlert>
                    {
                        new SystemAlert
                        {
                            Type = "Error",
                            Message = $"Database error loading dashboard: {ex.Message}",
                            Severity = "High"
                        }
                    }
                };
            }
            catch (Exception ex)
            {
                // Return safe default values for dashboard on general error
                return new DashboardViewModel
                {
                    TotalPaddyStock = 0,
                    TotalRiceStock = 0,
                    MonthlyRevenue = 0,
                    PendingPayments = 0,
                    TotalCustomers = 0,
                    TotalSuppliers = 0,
                    RecentTransactions = new List<TransactionSummary>(),
                    Alerts = new List<SystemAlert>
                    {
                        new SystemAlert
                        {
                            Type = "Error",
                            Message = $"Error loading dashboard: {ex.Message}",
                            Severity = "High"
                        }
                    }
                };
            }
        }

        public List<ChartData> GetMonthlySalesChart(int year)
        {
            try
            {
                var chartData = new List<ChartData>();

                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Year", year)
                };

                DataTable dt = _dbHelper.ExecuteDataTable("sp_Dashboard_GetMonthlySales", parameters);

                foreach (DataRow row in dt.Rows)
                {
                    chartData.Add(new ChartData
                    {
                        Label = row["MonthName"] != DBNull.Value ? row["MonthName"].ToString() ?? "Unknown" : "Unknown",
                        Value = row["TotalSales"] != DBNull.Value ? Convert.ToDecimal(row["TotalSales"]) : 0m
                    });
                }

                return chartData;
            }
            catch (SqlException)
            {
                // Return empty chart data on database error
                return new List<ChartData>();
            }
            catch (Exception)
            {
                // Return empty chart data on general error
                return new List<ChartData>();
            }
        }

        public List<ChartData> GetStockByVarietyChart()
        {
            try
            {
                var chartData = new List<ChartData>();

                DataTable dt = _dbHelper.ExecuteDataTable("sp_Dashboard_GetStockByVariety");

                foreach (DataRow row in dt.Rows)
                {
                    chartData.Add(new ChartData
                    {
                        Label = row["Variety"] != DBNull.Value ? row["Variety"].ToString() ?? "Unknown" : "Unknown",
                        Value = row["Stock"] != DBNull.Value ? Convert.ToDecimal(row["Stock"]) : 0m
                    });
                }

                return chartData;
            }
            catch (SqlException)
            {
                // Return empty chart data on database error
                return new List<ChartData>();
            }
            catch (Exception)
            {
                // Return empty chart data on general error
                return new List<ChartData>();
            }
        }

        public decimal GetTotalReceivables()
        {
            try
            {
                return _dbHelper.ExecuteScalar<decimal>("sp_Dashboard_GetTotalReceivables");
            }
            catch (SqlException)
            {
                // Return safe default value on database error
                return 0m;
            }
            catch (Exception)
            {
                // Return safe default value on general error
                return 0m;
            }
        }

        public decimal GetTotalPayables()
        {
            try
            {
                return _dbHelper.ExecuteScalar<decimal>("sp_Dashboard_GetTotalPayables");
            }
            catch (SqlException)
            {
                // Return safe default value on database error
                return 0m;
            }
            catch (Exception)
            {
                // Return safe default value on general error
                return 0m;
            }
        }

        private List<TransactionSummary> GetRecentTransactions(int count)
        {
            try
            {
                var transactions = new List<TransactionSummary>();

                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Count", count)
                };

                DataTable dt = _dbHelper.ExecuteDataTable("sp_Dashboard_GetRecentTransactions", parameters);

                foreach (DataRow row in dt.Rows)
                {
                    transactions.Add(new TransactionSummary
                    {
                        Date = row["TransactionDate"] != DBNull.Value ? Convert.ToDateTime(row["TransactionDate"]) : DateTime.Now,
                        Type = row["TransactionType"] != DBNull.Value ? row["TransactionType"].ToString() ?? "" : "",
                        Description = row["Description"] != DBNull.Value ? row["Description"].ToString() ?? "" : "",
                        Amount = row["Amount"] != DBNull.Value ? Convert.ToDecimal(row["Amount"]) : 0m
                    });
                }

                return transactions;
            }
            catch (SqlException)
            {
                // Return empty list on database error
                return new List<TransactionSummary>();
            }
            catch (Exception)
            {
                // Return empty list on general error
                return new List<TransactionSummary>();
            }
        }

        private List<SystemAlert> GetSystemAlerts()
        {
            try
            {
                var alerts = new List<SystemAlert>();

                DataTable dt = _dbHelper.ExecuteDataTable("sp_Dashboard_GetAlerts");

                foreach (DataRow row in dt.Rows)
                {
                    alerts.Add(new SystemAlert
                    {
                        Type = row["AlertType"] != DBNull.Value ? row["AlertType"].ToString() ?? "" : "",
                        Message = row["Message"] != DBNull.Value ? row["Message"].ToString() ?? "" : "",
                        Severity = row["Severity"] != DBNull.Value ? row["Severity"].ToString() ?? "" : ""
                    });
                }

                return alerts;
            }
            catch (SqlException)
            {
                // Return empty list on database error
                return new List<SystemAlert>();
            }
            catch (Exception)
            {
                // Return empty list on general error
                return new List<SystemAlert>();
            }
        }
    }

    // View Models
    public class DashboardViewModel
    {
        public decimal TotalPaddyStock { get; set; }
        public decimal TotalRiceStock { get; set; }
        public decimal MonthlyRevenue { get; set; }
        public int PendingPayments { get; set; }
        public int TotalCustomers { get; set; }
        public int TotalSuppliers { get; set; }
        public List<TransactionSummary> RecentTransactions { get; set; } = new List<TransactionSummary>();
        public List<SystemAlert> Alerts { get; set; } = new List<SystemAlert>();

        // Inventory Statistics
        public int TotalWarehouses { get; set; }
        public decimal TotalInventoryValue { get; set; }
        public int LowStockItemsCount { get; set; }
        public int OverStockItemsCount { get; set; }
        public int ReorderItemsCount { get; set; }
        public int TotalProducts { get; set; }
        public int PendingAdjustmentsCount { get; set; }
        public List<StockMovementSummary> RecentStockMovements { get; set; } = new List<StockMovementSummary>();
        public List<LowStockItem> LowStockItems { get; set; } = new List<LowStockItem>();
        public List<InventoryByWarehouse> InventoryByWarehouse { get; set; } = new List<InventoryByWarehouse>();

        // Production Statistics
        public int TotalMachines { get; set; }
        public int OperationalMachines { get; set; }
        public int MaintenanceDueMachines { get; set; }
        public int TodaysBatches { get; set; }
        public int ActiveBatches { get; set; }
        public int CompletedBatchesToday { get; set; }
        public decimal TodaysProductionQuantity { get; set; }
        public int PendingProductionOrders { get; set; }
        public List<ProductionBatchSummary> RecentBatches { get; set; } = new List<ProductionBatchSummary>();
    }

    public class StockMovementSummary
    {
        public DateTime MovementDate { get; set; }
        public string? MovementCode { get; set; }
        public string? MovementType { get; set; }
        public string? ProductName { get; set; }
        public string? WarehouseName { get; set; }
        public decimal Quantity { get; set; }
        public string? Category { get; set; }
    }

    public class LowStockItem
    {
        public string? ProductCode { get; set; }
        public string? ProductName { get; set; }
        public string? WarehouseName { get; set; }
        public decimal CurrentStock { get; set; }
        public decimal MinimumLevel { get; set; }
        public decimal ReorderLevel { get; set; }
        public decimal ShortageQuantity { get; set; }
    }

    public class InventoryByWarehouse
    {
        public string? WarehouseName { get; set; }
        public int ProductCount { get; set; }
        public decimal TotalValue { get; set; }
        public decimal Capacity { get; set; }
        public decimal UtilizationPercent { get; set; }
    }

    public class ChartData
    {
        public string? Label { get; set; }
        public decimal Value { get; set; }
    }

    public class TransactionSummary
    {
        public DateTime Date { get; set; }
        public string? Type { get; set; }
        public string? Description { get; set; }
        public decimal Amount { get; set; }
    }

    public class SystemAlert
    {
        public string? Type { get; set; }
        public string? Message { get; set; }
        public string? Severity { get; set; }
    }

    public class ProductionBatchSummary
    {
        public string? BatchNumber { get; set; }
        public DateTime BatchDate { get; set; }
        public string? Status { get; set; }
        public decimal InputQuantity { get; set; }
        public decimal OutputQuantity { get; set; }
        public decimal YieldPercent { get; set; }
        public string? OperatorName { get; set; }
    }
}