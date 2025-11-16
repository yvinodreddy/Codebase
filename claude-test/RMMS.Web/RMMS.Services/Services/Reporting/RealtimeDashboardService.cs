using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Dashboard service for real-time data aggregation
    /// </summary>
    public class RealtimeDashboardService : IRealtimeDashboardService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<RealtimeDashboardService> _logger;

        public RealtimeDashboardService(
            ApplicationDbContext context,
            ILogger<RealtimeDashboardService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<Dictionary<string, object>> GetSalesDashboardDataAsync()
        {
            var today = DateTime.Today;
            var thisMonth = new DateTime(today.Year, today.Month, 1);

            var todaySales = await _context.RiceSales
                .Where(s => s.SaleDate >= today)
                .SumAsync(s => (decimal?)s.TotalInvoiceValue) ?? 0;

            var monthSales = await _context.RiceSales
                .Where(s => s.SaleDate >= thisMonth)
                .SumAsync(s => (decimal?)s.TotalInvoiceValue) ?? 0;

            var salesCount = await _context.RiceSales
                .Where(s => s.SaleDate >= today)
                .CountAsync();

            var topCustomers = await _context.RiceSales
                .Where(s => s.SaleDate >= thisMonth)
                .GroupBy(s => s.BuyerName)
                .Select(g => new
                {
                    Customer = g.Key,
                    Total = g.Sum(s => s.TotalInvoiceValue)
                })
                .OrderByDescending(x => x.Total)
                .Take(5)
                .ToListAsync();

            return new Dictionary<string, object>
            {
                ["todaySales"] = todaySales,
                ["monthSales"] = monthSales,
                ["salesCount"] = salesCount,
                ["topCustomers"] = topCustomers,
                ["lastUpdated"] = DateTime.Now
            };
        }

        public async Task<Dictionary<string, object>> GetProductionDashboardDataAsync()
        {
            var today = DateTime.Today;

            var activeBatches = await _context.ProductionBatches
                .Where(b => b.Status == "In Progress")
                .CountAsync();

            var completedToday = await _context.ProductionBatches
                .Where(b => b.BatchDate >= today && b.Status == "Completed")
                .CountAsync();

            var avgQuality = await _context.ProductionBatches
                .Where(b => b.BatchDate >= today && b.QualityScore.HasValue)
                .AverageAsync(b => (decimal?)b.QualityScore) ?? 0;

            var batchStatus = await _context.ProductionBatches
                .Where(b => b.BatchDate >= today.AddDays(-7))
                .GroupBy(b => b.Status)
                .Select(g => new
                {
                    Status = g.Key,
                    Count = g.Count()
                })
                .ToListAsync();

            return new Dictionary<string, object>
            {
                ["activeBatches"] = activeBatches,
                ["completedToday"] = completedToday,
                ["avgQuality"] = avgQuality,
                ["batchStatus"] = batchStatus,
                ["lastUpdated"] = DateTime.Now
            };
        }

        public async Task<Dictionary<string, object>> GetInventoryDashboardDataAsync()
        {
            var lowStockCount = await _context.Products
                .Where(p => p.IsActive && p.MinimumStockLevel.HasValue)
                .CountAsync();

            var totalProducts = await _context.Products
                .Where(p => p.IsActive)
                .CountAsync();

            var recentMovements = await _context.StockMovements
                .Where(m => m.MovementDate >= DateTime.Today.AddDays(-1))
                .CountAsync();

            var warehouseUtilization = await _context.Warehouses
                .Where(w => w.IsActive)
                .Select(w => new
                {
                    w.WarehouseName,
                    w.WarehouseCode
                })
                .ToListAsync();

            return new Dictionary<string, object>
            {
                ["lowStockCount"] = lowStockCount,
                ["totalProducts"] = totalProducts,
                ["recentMovements"] = recentMovements,
                ["warehouses"] = warehouseUtilization,
                ["lastUpdated"] = DateTime.Now
            };
        }

        public async Task<Dictionary<string, object>> GetFinancialDashboardDataAsync()
        {
            var today = DateTime.Today;
            var thisMonth = new DateTime(today.Year, today.Month, 1);

            var monthRevenue = await _context.RiceSales
                .Where(s => s.SaleDate >= thisMonth)
                .SumAsync(s => (decimal?)s.GrossInvoiceAmount) ?? 0;

            var receipts = await _context.CashBooks
                .Where(c => c.TransactionDate >= thisMonth)
                .SumAsync(c => (decimal?)c.Receipts) ?? 0;

            var payments = await _context.CashBooks
                .Where(c => c.TransactionDate >= thisMonth)
                .SumAsync(c => (decimal?)c.Payments) ?? 0;

            var netCashFlow = receipts - payments;

            return new Dictionary<string, object>
            {
                ["monthRevenue"] = monthRevenue,
                ["receipts"] = receipts,
                ["payments"] = payments,
                ["netCashFlow"] = netCashFlow,
                ["lastUpdated"] = DateTime.Now
            };
        }
    }
}
