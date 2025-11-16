using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public class SalesOrderRepository : ISalesOrderRepository
    {
        private readonly ApplicationDbContext _context;

        public SalesOrderRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<SalesOrder>> GetAllAsync()
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.Quotation)
                .Include(so => so.ApprovedByEmployee)
                .Include(so => so.SalesOrderItems)
                    .ThenInclude(item => item.Product)
                .Include(so => so.SalesOrderItems)
                    .ThenInclude(item => item.Warehouse)
                .Where(so => so.IsActive)
                .OrderByDescending(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<SalesOrder?> GetByIdAsync(int id)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.Quotation)
                .Include(so => so.ApprovedByEmployee)
                .Include(so => so.SalesOrderItems)
                    .ThenInclude(item => item.Product)
                .Include(so => so.SalesOrderItems)
                    .ThenInclude(item => item.Warehouse)
                .FirstOrDefaultAsync(so => so.Id == id && so.IsActive);
        }

        public async Task<SalesOrder?> GetByOrderNumberAsync(string orderNumber)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.Quotation)
                .Include(so => so.SalesOrderItems)
                .FirstOrDefaultAsync(so => so.OrderNumber == orderNumber && so.IsActive);
        }

        public async Task<IEnumerable<SalesOrder>> GetByCustomerIdAsync(int customerId)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.CustomerId == customerId && so.IsActive)
                .OrderByDescending(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetByQuotationIdAsync(int quotationId)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.Quotation)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.QuotationId == quotationId && so.IsActive)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetByStatusAsync(string status)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.Status == status && so.IsActive)
                .OrderByDescending(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetByDateRangeAsync(DateTime fromDate, DateTime toDate)
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.OrderDate >= fromDate && so.OrderDate <= toDate && so.IsActive)
                .OrderByDescending(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetPendingOrdersAsync()
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => (so.Status == "Pending" || so.Status == "Confirmed") && so.IsActive)
                .OrderByDescending(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetOrdersForProductionAsync()
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                    .ThenInclude(item => item.Product)
                .Where(so => (so.Status == "Confirmed" || so.Status == "In Production") && so.IsActive)
                .OrderBy(so => so.DeliveryDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<SalesOrder>> GetReadyToShipOrdersAsync()
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.Status == "Ready to Ship" && so.IsActive)
                .OrderBy(so => so.DeliveryDate)
                .ToListAsync();
        }

        public async Task<string> GenerateOrderNumberAsync()
        {
            var now = DateTime.Now;
            var prefix = $"SO{now:yyyyMM}";

            var lastOrder = await _context.SalesOrders
                .Where(so => so.OrderNumber.StartsWith(prefix))
                .OrderByDescending(so => so.OrderNumber)
                .FirstOrDefaultAsync();

            if (lastOrder == null)
            {
                return $"{prefix}0001";
            }

            var lastNumber = int.Parse(lastOrder.OrderNumber.Substring(prefix.Length));
            var newNumber = lastNumber + 1;

            return $"{prefix}{newNumber:D4}";
        }

        public async Task<SalesOrder> AddAsync(SalesOrder salesOrder)
        {
            if (string.IsNullOrEmpty(salesOrder.OrderNumber))
            {
                salesOrder.OrderNumber = await GenerateOrderNumberAsync();
            }

            _context.SalesOrders.Add(salesOrder);
            await _context.SaveChangesAsync();
            return salesOrder;
        }

        public async Task UpdateAsync(SalesOrder salesOrder)
        {
            _context.SalesOrders.Update(salesOrder);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(int id)
        {
            var salesOrder = await _context.SalesOrders.FindAsync(id);
            if (salesOrder != null)
            {
                salesOrder.IsActive = false;
                salesOrder.ModifiedDate = DateTime.Now;
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.SalesOrders.AnyAsync(so => so.Id == id && so.IsActive);
        }
    }
}
