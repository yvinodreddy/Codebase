using RMMS.DataAccess.Repositories.Sales;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace RMMS.Services.Implementations.Sales
{
    public class SalesOrderService : ISalesOrderService
    {
        private readonly ISalesOrderRepository _salesOrderRepository;
        private readonly IQuotationRepository _quotationRepository;
        private readonly IInventoryLedgerService _inventoryService;
        private readonly ILogger<SalesOrderService> _logger;

        public SalesOrderService(
            ISalesOrderRepository salesOrderRepository,
            IQuotationRepository quotationRepository,
            IInventoryLedgerService inventoryService,
            ILogger<SalesOrderService> logger)
        {
            _salesOrderRepository = salesOrderRepository;
            _quotationRepository = quotationRepository;
            _inventoryService = inventoryService;
            _logger = logger;
        }

        public async Task<IEnumerable<SalesOrder>> GetAllSalesOrdersAsync()
        {
            return await _salesOrderRepository.GetAllAsync();
        }

        public async Task<SalesOrder?> GetSalesOrderByIdAsync(int id)
        {
            return await _salesOrderRepository.GetByIdAsync(id);
        }

        public async Task<SalesOrder?> GetSalesOrderByNumberAsync(string orderNumber)
        {
            return await _salesOrderRepository.GetByOrderNumberAsync(orderNumber);
        }

        public async Task<IEnumerable<SalesOrder>> GetSalesOrdersByCustomerAsync(int customerId)
        {
            return await _salesOrderRepository.GetByCustomerIdAsync(customerId);
        }

        public async Task<IEnumerable<SalesOrder>> GetSalesOrdersByQuotationAsync(int quotationId)
        {
            return await _salesOrderRepository.GetByQuotationIdAsync(quotationId);
        }

        public async Task<IEnumerable<SalesOrder>> GetSalesOrdersByStatusAsync(string status)
        {
            return await _salesOrderRepository.GetByStatusAsync(status);
        }

        public async Task<IEnumerable<SalesOrder>> GetSalesOrdersByDateRangeAsync(DateTime fromDate, DateTime toDate)
        {
            return await _salesOrderRepository.GetByDateRangeAsync(fromDate, toDate);
        }

        public async Task<IEnumerable<SalesOrder>> GetPendingSalesOrdersAsync()
        {
            return await _salesOrderRepository.GetPendingOrdersAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetOrdersForProductionAsync()
        {
            return await _salesOrderRepository.GetOrdersForProductionAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetReadyToShipOrdersAsync()
        {
            return await _salesOrderRepository.GetReadyToShipOrdersAsync();
        }

        public async Task<IEnumerable<SalesOrder>> SearchSalesOrdersAsync(string searchTerm)
        {
            var allOrders = await _salesOrderRepository.GetAllAsync();

            if (string.IsNullOrWhiteSpace(searchTerm))
                return allOrders;

            searchTerm = searchTerm.ToLower();
            return allOrders.Where(so =>
                so.OrderNumber.ToLower().Contains(searchTerm) ||
                (so.Customer != null && so.Customer.CustomerName.ToLower().Contains(searchTerm)) ||
                (so.Customer != null && so.Customer.CustomerCode.ToLower().Contains(searchTerm)) ||
                (so.Remarks != null && so.Remarks.ToLower().Contains(searchTerm))
            );
        }

        public async Task<SalesOrder> CreateSalesOrderAsync(SalesOrder salesOrder)
        {
            // Set default values
            salesOrder.Status = "Pending";
            salesOrder.CreatedDate = DateTime.Now;
            salesOrder.StockReserved = false;

            // If created from quotation, update quotation status
            if (salesOrder.QuotationId.HasValue)
            {
                var quotation = await _quotationRepository.GetByIdAsync(salesOrder.QuotationId.Value);
                if (quotation != null)
                {
                    quotation.Status = "Converted";
                    quotation.ModifiedDate = DateTime.Now;
                    await _quotationRepository.UpdateAsync(quotation);
                }
            }

            return await _salesOrderRepository.AddAsync(salesOrder);
        }

        public async Task UpdateSalesOrderAsync(SalesOrder salesOrder)
        {
            salesOrder.ModifiedDate = DateTime.Now;
            await _salesOrderRepository.UpdateAsync(salesOrder);
        }

        public async Task DeleteSalesOrderAsync(int id)
        {
            await _salesOrderRepository.DeleteAsync(id);
        }

        public async Task<SalesOrder> AddSalesOrderItemAsync(int salesOrderId, SalesOrderItem item)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                throw new Exception("Sales order not found");

            salesOrder.SalesOrderItems.Add(item);
            await RecalculateSalesOrderTotalsAsync(salesOrderId);

            return salesOrder;
        }

        public async Task RemoveSalesOrderItemAsync(int salesOrderId, int itemId)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                throw new Exception("Sales order not found");

            var item = salesOrder.SalesOrderItems.FirstOrDefault(i => i.Id == itemId);
            if (item != null)
            {
                salesOrder.SalesOrderItems.Remove(item);
                await RecalculateSalesOrderTotalsAsync(salesOrderId);
            }
        }

        public async Task RecalculateSalesOrderTotalsAsync(int salesOrderId)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                return;

            // Calculate subtotal from items
            salesOrder.SubtotalAmount = salesOrder.SalesOrderItems.Sum(i => i.LineTotal);

            // Apply discount
            var amountAfterDiscount = salesOrder.SubtotalAmount - (salesOrder.DiscountAmount ?? 0);

            // Calculate total (subtotal - discount + tax + freight + other charges)
            salesOrder.TotalAmount = amountAfterDiscount
                + salesOrder.TaxAmount
                + (salesOrder.FreightCharges ?? 0)
                + (salesOrder.OtherCharges ?? 0);

            await _salesOrderRepository.UpdateAsync(salesOrder);
        }

        public async Task<bool> ConfirmSalesOrderAsync(int salesOrderId, int approvedByEmployeeId)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                return false;

            if (salesOrder.Status != "Pending")
                return false;

            salesOrder.ApprovedByEmployeeId = approvedByEmployeeId;
            salesOrder.ApprovalDate = DateTime.Now;
            salesOrder.Status = "Confirmed";
            salesOrder.ModifiedDate = DateTime.Now;

            await _salesOrderRepository.UpdateAsync(salesOrder);
            return true;
        }

        public async Task<bool> UpdateOrderStatusAsync(int salesOrderId, string newStatus)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                return false;

            // Validate status transition
            var validStatuses = new[] { "Pending", "Confirmed", "In Production", "Ready to Ship", "Shipped", "Delivered", "Cancelled" };
            if (!validStatuses.Contains(newStatus))
                return false;

            salesOrder.Status = newStatus;
            salesOrder.ModifiedDate = DateTime.Now;

            await _salesOrderRepository.UpdateAsync(salesOrder);
            return true;
        }

        public async Task<bool> ReserveStockAsync(int salesOrderId)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
            {
                _logger.LogWarning($"Sales order {salesOrderId} not found for stock reservation");
                return false;
            }

            if (salesOrder.StockReserved)
            {
                _logger.LogInformation($"Stock already reserved for sales order {salesOrderId}");
                return false; // Already reserved
            }

            if (salesOrder.SalesOrderItems == null || !salesOrder.SalesOrderItems.Any())
            {
                _logger.LogWarning($"Sales order {salesOrderId} has no items to reserve");
                return false;
            }

            try
            {
                // Reserve stock for each line item
                foreach (var item in salesOrder.SalesOrderItems)
                {
                    if (!item.WarehouseId.HasValue)
                    {
                        _logger.LogWarning($"Sales order item {item.Id} has no warehouse specified, using default warehouse 1");
                        item.WarehouseId = 1; // Default warehouse
                    }

                    // Get current inventory for this product in the specified warehouse
                    var inventory = _inventoryService.GetInventoryByProductAndWarehouse(
                        item.ProductId,
                        item.WarehouseId.Value);

                    if (inventory == null)
                    {
                        _logger.LogError($"No inventory record found for Product {item.ProductId} in Warehouse {item.WarehouseId}");
                        return false;
                    }

                    // Check if sufficient stock is available
                    if (inventory.CurrentStock < item.Quantity)
                    {
                        _logger.LogError($"Insufficient stock for Product {item.ProductId}. Available: {inventory.CurrentStock}, Required: {item.Quantity}");
                        return false;
                    }

                    // Reserve stock by reducing available quantity
                    bool stockAdjusted = _inventoryService.AdjustStock(
                        item.ProductId,
                        item.WarehouseId.Value,
                        inventory.CurrentStock - item.Quantity, // Reduce by order quantity
                        null,
                        "StockReservation"
                    );

                    if (!stockAdjusted)
                    {
                        _logger.LogError($"Failed to adjust stock for Product {item.ProductId}");
                        return false;
                    }

                    // Track allocated quantity
                    item.AllocatedQuantity = item.Quantity;
                    _logger.LogInformation($"Reserved {item.Quantity} units of Product {item.ProductId} from Warehouse {item.WarehouseId}");
                }

                // Mark order as stock reserved
                salesOrder.StockReserved = true;
                salesOrder.StockReservedDate = DateTime.Now;
                salesOrder.ModifiedDate = DateTime.Now;

                await _salesOrderRepository.UpdateAsync(salesOrder);

                _logger.LogInformation($"Stock successfully reserved for sales order {salesOrderId}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error reserving stock for sales order {salesOrderId}");
                return false;
            }
        }

        public async Task<bool> CancelSalesOrderAsync(int salesOrderId, string cancellationReason)
        {
            var salesOrder = await _salesOrderRepository.GetByIdAsync(salesOrderId);
            if (salesOrder == null)
                return false;

            // Cannot cancel if already shipped or delivered
            if (salesOrder.Status == "Shipped" || salesOrder.Status == "Delivered")
                return false;

            salesOrder.Status = "Cancelled";
            salesOrder.Remarks = (salesOrder.Remarks ?? "") + $"\nCancelled: {cancellationReason}";
            salesOrder.ModifiedDate = DateTime.Now;

            // Release stock if it was reserved
            if (salesOrder.StockReserved)
            {
                try
                {
                    // Release reserved stock back to inventory
                    foreach (var item in salesOrder.SalesOrderItems)
                    {
                        if (item.AllocatedQuantity.HasValue && item.AllocatedQuantity.Value > 0 && item.WarehouseId.HasValue)
                        {
                            var inventory = _inventoryService.GetInventoryByProductAndWarehouse(
                                item.ProductId,
                                item.WarehouseId.Value);

                            if (inventory != null)
                            {
                                // Return the allocated quantity back to inventory
                                _inventoryService.AdjustStock(
                                    item.ProductId,
                                    item.WarehouseId.Value,
                                    inventory.CurrentStock + item.AllocatedQuantity.Value,
                                    null,
                                    "StockRelease-Cancellation"
                                );

                                item.AllocatedQuantity = 0;
                                _logger.LogInformation($"Released {item.AllocatedQuantity.Value} units of Product {item.ProductId} back to Warehouse {item.WarehouseId}");
                            }
                        }
                    }

                    salesOrder.StockReserved = false;
                    salesOrder.StockReservedDate = null;
                    _logger.LogInformation($"Stock released for cancelled sales order {salesOrderId}");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error releasing stock for cancelled sales order {salesOrderId}");
                }
            }

            await _salesOrderRepository.UpdateAsync(salesOrder);
            return true;
        }

        public async Task<Dictionary<string, object>> GetSalesOrderStatisticsAsync()
        {
            var allOrders = await _salesOrderRepository.GetAllAsync();

            return new Dictionary<string, object>
            {
                { "TotalOrders", allOrders.Count() },
                { "PendingCount", allOrders.Count(so => so.Status == "Pending") },
                { "ConfirmedCount", allOrders.Count(so => so.Status == "Confirmed") },
                { "InProductionCount", allOrders.Count(so => so.Status == "In Production") },
                { "ReadyToShipCount", allOrders.Count(so => so.Status == "Ready to Ship") },
                { "ShippedCount", allOrders.Count(so => so.Status == "Shipped") },
                { "DeliveredCount", allOrders.Count(so => so.Status == "Delivered") },
                { "CancelledCount", allOrders.Count(so => so.Status == "Cancelled") },
                { "TotalValue", allOrders.Where(so => so.Status != "Cancelled").Sum(so => so.TotalAmount) },
                { "AverageValue", allOrders.Any() ? allOrders.Where(so => so.Status != "Cancelled").Average(so => so.TotalAmount) : 0 }
            };
        }
    }
}
