using RMMS.Models.Sales;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public interface ISalesOrderRepository
    {
        Task<IEnumerable<SalesOrder>> GetAllAsync();
        Task<SalesOrder?> GetByIdAsync(int id);
        Task<SalesOrder?> GetByOrderNumberAsync(string orderNumber);
        Task<IEnumerable<SalesOrder>> GetByCustomerIdAsync(int customerId);
        Task<IEnumerable<SalesOrder>> GetByQuotationIdAsync(int quotationId);
        Task<IEnumerable<SalesOrder>> GetByStatusAsync(string status);
        Task<IEnumerable<SalesOrder>> GetByDateRangeAsync(DateTime fromDate, DateTime toDate);
        Task<IEnumerable<SalesOrder>> GetPendingOrdersAsync();
        Task<IEnumerable<SalesOrder>> GetOrdersForProductionAsync(); // Confirmed + In Production
        Task<IEnumerable<SalesOrder>> GetReadyToShipOrdersAsync();
        Task<string> GenerateOrderNumberAsync();
        Task<SalesOrder> AddAsync(SalesOrder salesOrder);
        Task UpdateAsync(SalesOrder salesOrder);
        Task DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
    }
}
