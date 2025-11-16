using RMMS.Models.Sales;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Interfaces.Sales
{
    public interface ISalesOrderService
    {
        Task<IEnumerable<SalesOrder>> GetAllSalesOrdersAsync();
        Task<SalesOrder?> GetSalesOrderByIdAsync(int id);
        Task<SalesOrder?> GetSalesOrderByNumberAsync(string orderNumber);
        Task<IEnumerable<SalesOrder>> GetSalesOrdersByCustomerAsync(int customerId);
        Task<IEnumerable<SalesOrder>> GetSalesOrdersByQuotationAsync(int quotationId);
        Task<IEnumerable<SalesOrder>> GetSalesOrdersByStatusAsync(string status);
        Task<IEnumerable<SalesOrder>> GetSalesOrdersByDateRangeAsync(DateTime fromDate, DateTime toDate);
        Task<IEnumerable<SalesOrder>> GetPendingSalesOrdersAsync();
        Task<IEnumerable<SalesOrder>> GetOrdersForProductionAsync();
        Task<IEnumerable<SalesOrder>> GetReadyToShipOrdersAsync();
        Task<IEnumerable<SalesOrder>> SearchSalesOrdersAsync(string searchTerm);
        Task<SalesOrder> CreateSalesOrderAsync(SalesOrder salesOrder);
        Task UpdateSalesOrderAsync(SalesOrder salesOrder);
        Task DeleteSalesOrderAsync(int id);
        Task<SalesOrder> AddSalesOrderItemAsync(int salesOrderId, SalesOrderItem item);
        Task RemoveSalesOrderItemAsync(int salesOrderId, int itemId);
        Task RecalculateSalesOrderTotalsAsync(int salesOrderId);
        Task<bool> ConfirmSalesOrderAsync(int salesOrderId, int approvedByEmployeeId);
        Task<bool> UpdateOrderStatusAsync(int salesOrderId, string newStatus);
        Task<bool> ReserveStockAsync(int salesOrderId);
        Task<bool> CancelSalesOrderAsync(int salesOrderId, string cancellationReason);
        Task<Dictionary<string, object>> GetSalesOrderStatisticsAsync();
    }
}
