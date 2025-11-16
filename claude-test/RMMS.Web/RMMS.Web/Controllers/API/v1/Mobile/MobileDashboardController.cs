using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Production;
using RMMS.Services.Interfaces.Inventory;
using RMMS.Services.Interfaces.Sales;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers.API.v1.Mobile
{
    /// <summary>
    /// API controller for mobile dashboard (lightweight data)
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    public class MobileDashboardController : BaseApiController
    {
        private readonly IProductionBatchService _productionService;
        private readonly IInventoryLedgerService _inventoryService;
        private readonly ISalesOrderService _salesService;

        public MobileDashboardController(
            IProductionBatchService productionService,
            IInventoryLedgerService inventoryService,
            ISalesOrderService salesService)
        {
            _productionService = productionService;
            _inventoryService = inventoryService;
            _salesService = salesService;
        }

        /// <summary>
        /// Get mobile dashboard summary
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetDashboard()
        {
            try
            {
                var dashboard = new MobileDashboardDto
                {
                    Timestamp = DateTime.UtcNow,
                    Production = await GetProductionSummaryAsync(),
                    Inventory = await GetInventorySummaryAsync(),
                    Sales = await GetSalesSummaryAsync(),
                    RecentAlerts = GetRecentAlerts()
                };

                return Success(dashboard);
            }
            catch (Exception ex)
            {
                return Error($"Error loading dashboard: {ex.Message}");
            }
        }

        private async Task<ProductionSummaryDto> GetProductionSummaryAsync()
        {
            // Simplified version returning summary data
            // TODO: Implement proper data fetching once service methods are available
            await Task.CompletedTask;

            return new ProductionSummaryDto
            {
                ActiveBatches = 5,
                TodayOutput = 1250.5m,
                AverageYield = 92.5m,
                MachinesActive = 3,
                MachinesIdle = 2
            };
        }

        private async Task<InventorySummaryDto> GetInventorySummaryAsync()
        {
            // Simplified version returning summary data
            // TODO: Implement proper data fetching once service methods are available
            await Task.CompletedTask;

            return new InventorySummaryDto
            {
                TotalStockValue = 125000.50m,
                LowStockItems = 3,
                OutOfStockItems = 1,
                TopItems = new List<TopStockItemDto>
                {
                    new TopStockItemDto { ProductId = 1, ProductName = "Basmati Rice", Quantity = 5000, Unit = "Kg" },
                    new TopStockItemDto { ProductId = 2, ProductName = "Sona Masoori", Quantity = 3500, Unit = "Kg" },
                    new TopStockItemDto { ProductId = 3, ProductName = "Broken Rice", Quantity = 2000, Unit = "Kg" }
                }
            };
        }

        private async Task<SalesSummaryDto> GetSalesSummaryAsync()
        {
            // Simplified version returning summary data
            // TODO: Implement proper data fetching once service methods are available
            await Task.CompletedTask;

            return new SalesSummaryDto
            {
                TodaySales = 15750.25m,
                WeekSales = 87230.50m,
                MonthSales = 345678.90m,
                PendingOrders = 12
            };
        }

        private List<AlertDto> GetRecentAlerts()
        {
            // In production, this would query from a proper alerts/notifications system
            return new List<AlertDto>
            {
                new AlertDto
                {
                    Type = "inventory",
                    Message = "Low stock alert: Some items below minimum level",
                    Timestamp = DateTime.UtcNow.AddHours(-2),
                    Severity = "warning"
                }
            };
        }
    }
}
