using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Production;

namespace RMMS.DataAccess.Repositories.Production
{
    public class ProductionOrderRepository : IProductionOrderRepository
    {
        private readonly ApplicationDbContext _context;

        public ProductionOrderRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        // Basic CRUD
        public ProductionOrder? GetProductionOrderById(int id)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .FirstOrDefault(po => po.Id == id);
        }

        public List<ProductionOrder> GetAllProductionOrders()
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.IsActive)
                .OrderByDescending(po => po.CreatedDate)
                .ToList();
        }

        public bool CreateProductionOrder(ProductionOrder order)
        {
            try
            {
                _context.ProductionOrders.Add(order);
                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool UpdateProductionOrder(ProductionOrder order)
        {
            try
            {
                _context.ProductionOrders.Update(order);
                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool DeleteProductionOrder(int id)
        {
            try
            {
                var order = GetProductionOrderById(id);
                if (order != null)
                {
                    order.IsActive = false;
                    _context.SaveChanges();
                    return true;
                }
                return false;
            }
            catch
            {
                return false;
            }
        }

        // Query Methods
        public ProductionOrder? GetProductionOrderByOrderNumber(string orderNumber)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .FirstOrDefault(po => po.OrderNumber == orderNumber && po.IsActive);
        }

        public List<ProductionOrder> GetProductionOrdersByStatus(string status)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.Status == status && po.IsActive)
                .OrderByDescending(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetProductionOrdersByDateRange(DateTime startDate, DateTime endDate)
        {
            // Use DateTime.Date for date-only comparison
            var startDateOnly = startDate.Date;
            var endDateOnly = endDate.Date;

            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.IsActive)
                .AsEnumerable() // Switch to in-memory evaluation
                .Where(po => po.ScheduledDate.Date >= startDateOnly
                          && po.ScheduledDate.Date <= endDateOnly)
                .OrderBy(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetProductionOrdersByMachine(int machineId)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.AssignedMachineId == machineId && po.IsActive)
                .OrderByDescending(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetProductionOrdersBySupervisor(int supervisorId)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.AssignedSupervisorId == supervisorId && po.IsActive)
                .OrderByDescending(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetProductionOrdersByPriority(string priority)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.Priority == priority && po.IsActive)
                .OrderByDescending(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetScheduledProductionOrders(DateTime date)
        {
            var dateOnly = date.Date;
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.IsActive)
                .AsEnumerable() // Switch to in-memory evaluation
                .Where(po => po.ScheduledDate.Date == dateOnly)
                .OrderBy(po => po.Priority == "Urgent" ? 0 : po.Priority == "High" ? 1 : po.Priority == "Normal" ? 2 : 3)
                .ToList();
        }

        public List<ProductionOrder> GetInProgressProductionOrders()
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.Status == "In Progress" && po.IsActive)
                .OrderBy(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetCompletedProductionOrders(int limit = 50)
        {
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => po.Status == "Completed" && po.IsActive)
                .OrderByDescending(po => po.ActualCompletionDate)
                .Take(limit)
                .ToList();
        }

        public List<ProductionOrder> SearchProductionOrders(string searchTerm)
        {
            searchTerm = searchTerm.ToLower();
            return _context.ProductionOrders
                .Include(po => po.AssignedMachine)
                .Where(po => (po.OrderNumber.ToLower().Contains(searchTerm)
                          || (po.PaddyVariety != null && po.PaddyVariety.ToLower().Contains(searchTerm))
                          || (po.TargetRiceGrade != null && po.TargetRiceGrade.ToLower().Contains(searchTerm))
                          || (po.Status != null && po.Status.ToLower().Contains(searchTerm)))
                          && po.IsActive)
                .OrderByDescending(po => po.CreatedDate)
                .ToList();
        }

        // Statistics
        public int GetTotalProductionOrdersCount()
        {
            return _context.ProductionOrders.Count(po => po.IsActive);
        }

        public int GetProductionOrdersCountByStatus(string status)
        {
            return _context.ProductionOrders.Count(po => po.Status == status && po.IsActive);
        }

        public decimal GetTotalPlannedQuantity()
        {
            return _context.ProductionOrders
                .Where(po => po.IsActive && po.Status != "Cancelled")
                .Sum(po => (decimal?)po.PaddyQuantity) ?? 0;
        }

        public decimal GetTotalProducedQuantity()
        {
            return _context.ProductionOrders
                .Where(po => po.IsActive && po.Status == "Completed")
                .Sum(po => (decimal?)po.ActualQuantityProduced) ?? 0;
        }

        public decimal GetAverageYieldPercent()
        {
            var completedOrders = _context.ProductionOrders
                .Where(po => po.IsActive && po.Status == "Completed" && po.ActualYieldPercent.HasValue)
                .ToList();

            if (!completedOrders.Any())
                return 0;

            return completedOrders.Average(po => po.ActualYieldPercent ?? 0);
        }

        // Code Generation
        public string GenerateOrderNumber()
        {
            var lastOrder = _context.ProductionOrders
                .OrderByDescending(po => po.Id)
                .FirstOrDefault();

            if (lastOrder == null)
                return "PO0001";

            var lastNumber = lastOrder.OrderNumber;
            var numberPart = lastNumber.Substring(2); // Remove "PO"

            if (int.TryParse(numberPart, out int lastNum))
            {
                var newNumber = lastNum + 1;
                return $"PO{newNumber:D4}";
            }

            return "PO0001";
        }

        // Status Management
        public bool UpdateOrderStatus(int orderId, string newStatus, string modifiedBy)
        {
            try
            {
                var order = GetProductionOrderById(orderId);
                if (order == null) return false;

                order.Status = newStatus;
                order.ModifiedBy = modifiedBy;
                order.ModifiedDate = DateTime.Now;

                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool StartProduction(int orderId, string startedBy)
        {
            try
            {
                var order = GetProductionOrderById(orderId);
                if (order == null) return false;

                order.Status = "In Progress";
                order.ActualStartDate = DateTime.Now;
                order.ModifiedBy = startedBy;
                order.ModifiedDate = DateTime.Now;

                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool CompleteProduction(int orderId, decimal actualQuantity, decimal actualYield, string completedBy)
        {
            try
            {
                var order = GetProductionOrderById(orderId);
                if (order == null) return false;

                order.Status = "Completed";
                order.ActualCompletionDate = DateTime.Now;
                order.ActualQuantityProduced = actualQuantity;
                order.ActualYieldPercent = actualYield;
                order.ModifiedBy = completedBy;
                order.ModifiedDate = DateTime.Now;

                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool CancelOrder(int orderId, string cancelledBy, string reason)
        {
            try
            {
                var order = GetProductionOrderById(orderId);
                if (order == null) return false;

                order.Status = "Cancelled";
                order.Remarks = (order.Remarks ?? "") + $"\nCancelled by {cancelledBy}. Reason: {reason}";
                order.ModifiedBy = cancelledBy;
                order.ModifiedDate = DateTime.Now;

                _context.SaveChanges();
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
