using System;
using System.Collections.Generic;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// Lightweight dashboard DTO optimized for mobile
    /// </summary>
    public class MobileDashboardDto
    {
        public DateTime Timestamp { get; set; }

        // Production Summary
        public ProductionSummaryDto? Production { get; set; }

        // Inventory Summary
        public InventorySummaryDto? Inventory { get; set; }

        // Sales Summary
        public SalesSummaryDto? Sales { get; set; }

        // Recent Alerts
        public List<AlertDto>? RecentAlerts { get; set; }
    }

    public class ProductionSummaryDto
    {
        public int ActiveBatches { get; set; }
        public decimal TodayOutput { get; set; }
        public decimal AverageYield { get; set; }
        public int MachinesActive { get; set; }
        public int MachinesIdle { get; set; }
    }

    public class InventorySummaryDto
    {
        public decimal TotalStockValue { get; set; }
        public int LowStockItems { get; set; }
        public int OutOfStockItems { get; set; }
        public List<TopStockItemDto>? TopItems { get; set; }
    }

    public class TopStockItemDto
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; } = string.Empty;
        public decimal Quantity { get; set; }
        public string Unit { get; set; } = string.Empty;
    }

    public class SalesSummaryDto
    {
        public decimal TodaySales { get; set; }
        public decimal WeekSales { get; set; }
        public decimal MonthSales { get; set; }
        public int PendingOrders { get; set; }
    }

    public class AlertDto
    {
        public string Type { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public string Severity { get; set; } = "info"; // info, warning, error
    }
}
