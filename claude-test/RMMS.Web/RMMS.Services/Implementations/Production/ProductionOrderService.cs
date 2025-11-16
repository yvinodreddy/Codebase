using RMMS.DataAccess.Repositories.Production;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;

namespace RMMS.Services.Implementations.Production
{
    public class ProductionOrderService : IProductionOrderService
    {
        private readonly IProductionOrderRepository _productionOrderRepository;

        public ProductionOrderService(IProductionOrderRepository productionOrderRepository)
        {
            _productionOrderRepository = productionOrderRepository;
        }

        // Basic CRUD
        public ProductionOrder? GetProductionOrderById(int id)
        {
            return _productionOrderRepository.GetProductionOrderById(id);
        }

        public List<ProductionOrder> GetAllProductionOrders()
        {
            return _productionOrderRepository.GetAllProductionOrders();
        }

        public bool CreateProductionOrder(ProductionOrder order, string createdBy)
        {
            // Generate order number if not provided
            if (string.IsNullOrWhiteSpace(order.OrderNumber))
            {
                order.OrderNumber = GenerateOrderNumber();
            }

            // Set audit fields
            order.CreatedBy = createdBy;
            order.CreatedDate = DateTime.Now;
            order.IsActive = true;

            // Set defaults
            if (order.OrderDate == default)
            {
                order.OrderDate = DateTime.Now;
            }

            if (string.IsNullOrWhiteSpace(order.Status))
            {
                order.Status = "Draft";
            }

            if (string.IsNullOrWhiteSpace(order.Priority))
            {
                order.Priority = "Normal";
            }

            if (!order.ExpectedYieldPercent.HasValue)
            {
                order.ExpectedYieldPercent = 65.00m;
            }

            return _productionOrderRepository.CreateProductionOrder(order);
        }

        public bool UpdateProductionOrder(ProductionOrder order, string modifiedBy)
        {
            order.ModifiedBy = modifiedBy;
            order.ModifiedDate = DateTime.Now;

            return _productionOrderRepository.UpdateProductionOrder(order);
        }

        public bool DeleteProductionOrder(int id)
        {
            return _productionOrderRepository.DeleteProductionOrder(id);
        }

        // Query Methods
        public ProductionOrder? GetProductionOrderByOrderNumber(string orderNumber)
        {
            return _productionOrderRepository.GetProductionOrderByOrderNumber(orderNumber);
        }

        public List<ProductionOrder> GetProductionOrdersByStatus(string status)
        {
            return _productionOrderRepository.GetProductionOrdersByStatus(status);
        }

        public List<ProductionOrder> GetProductionOrdersByDateRange(DateTime startDate, DateTime endDate)
        {
            return _productionOrderRepository.GetProductionOrdersByDateRange(startDate, endDate);
        }

        public List<ProductionOrder> GetProductionOrdersByMachine(int machineId)
        {
            return _productionOrderRepository.GetProductionOrdersByMachine(machineId);
        }

        public List<ProductionOrder> GetProductionOrdersBySupervisor(int supervisorId)
        {
            return _productionOrderRepository.GetProductionOrdersBySupervisor(supervisorId);
        }

        public List<ProductionOrder> GetProductionOrdersByPriority(string priority)
        {
            return _productionOrderRepository.GetProductionOrdersByPriority(priority);
        }

        public List<ProductionOrder> GetScheduledProductionOrders(DateTime date)
        {
            return _productionOrderRepository.GetScheduledProductionOrders(date);
        }

        public List<ProductionOrder> GetTodayScheduledOrders()
        {
            return _productionOrderRepository.GetScheduledProductionOrders(DateTime.Today);
        }

        public List<ProductionOrder> GetInProgressProductionOrders()
        {
            return _productionOrderRepository.GetInProgressProductionOrders();
        }

        public List<ProductionOrder> GetCompletedProductionOrders(int limit = 50)
        {
            return _productionOrderRepository.GetCompletedProductionOrders(limit);
        }

        public List<ProductionOrder> SearchProductionOrders(string searchTerm)
        {
            return _productionOrderRepository.SearchProductionOrders(searchTerm);
        }

        // Statistics
        public int GetTotalProductionOrdersCount()
        {
            return _productionOrderRepository.GetTotalProductionOrdersCount();
        }

        public int GetDraftOrdersCount()
        {
            return _productionOrderRepository.GetProductionOrdersCountByStatus("Draft");
        }

        public int GetScheduledOrdersCount()
        {
            return _productionOrderRepository.GetProductionOrdersCountByStatus("Scheduled");
        }

        public int GetInProgressOrdersCount()
        {
            return _productionOrderRepository.GetProductionOrdersCountByStatus("In Progress");
        }

        public int GetCompletedOrdersCount()
        {
            return _productionOrderRepository.GetProductionOrdersCountByStatus("Completed");
        }

        public decimal GetTotalPlannedQuantity()
        {
            return _productionOrderRepository.GetTotalPlannedQuantity();
        }

        public decimal GetTotalProducedQuantity()
        {
            return _productionOrderRepository.GetTotalProducedQuantity();
        }

        public decimal GetAverageYieldPercent()
        {
            return _productionOrderRepository.GetAverageYieldPercent();
        }

        // Business Logic
        public string GenerateOrderNumber()
        {
            return _productionOrderRepository.GenerateOrderNumber();
        }

        public bool ValidateOrderNumber(string orderNumber)
        {
            if (string.IsNullOrWhiteSpace(orderNumber))
                return false;

            // Check format: PO####
            if (!orderNumber.StartsWith("PO") || orderNumber.Length != 6)
                return false;

            // Check if numeric part
            var numericPart = orderNumber.Substring(2);
            return int.TryParse(numericPart, out _);
        }

        public bool CanStartProduction(int orderId)
        {
            var order = GetProductionOrderById(orderId);
            if (order == null) return false;

            // Can only start from Scheduled status
            return order.Status == "Scheduled" && order.AssignedMachineId.HasValue;
        }

        public bool CanCompleteProduction(int orderId)
        {
            var order = GetProductionOrderById(orderId);
            if (order == null) return false;

            // Can only complete from In Progress status
            return order.Status == "In Progress";
        }

        public bool CanCancelOrder(int orderId)
        {
            var order = GetProductionOrderById(orderId);
            if (order == null) return false;

            // Cannot cancel completed or closed orders
            return order.Status != "Completed" && order.Status != "Closed";
        }

        // Workflow Methods
        public bool ScheduleOrder(int orderId, DateTime scheduledDate, int? machineId, int? supervisorId, string modifiedBy)
        {
            var order = GetProductionOrderById(orderId);
            if (order == null) return false;

            order.ScheduledDate = scheduledDate;
            order.AssignedMachineId = machineId;
            order.AssignedSupervisorId = supervisorId;
            order.Status = "Scheduled";
            order.ModifiedBy = modifiedBy;
            order.ModifiedDate = DateTime.Now;

            return _productionOrderRepository.UpdateProductionOrder(order);
        }

        public bool StartProduction(int orderId, string startedBy)
        {
            if (!CanStartProduction(orderId))
                return false;

            return _productionOrderRepository.StartProduction(orderId, startedBy);
        }

        public bool CompleteProduction(int orderId, decimal actualQuantity, decimal actualYield, string completedBy)
        {
            if (!CanCompleteProduction(orderId))
                return false;

            return _productionOrderRepository.CompleteProduction(orderId, actualQuantity, actualYield, completedBy);
        }

        public bool CancelOrder(int orderId, string cancelledBy, string reason)
        {
            if (!CanCancelOrder(orderId))
                return false;

            return _productionOrderRepository.CancelOrder(orderId, cancelledBy, reason);
        }

        public bool CloseOrder(int orderId, string closedBy)
        {
            var order = GetProductionOrderById(orderId);
            if (order == null || order.Status != "Completed")
                return false;

            return _productionOrderRepository.UpdateOrderStatus(orderId, "Closed", closedBy);
        }

        // Dashboard/Reporting
        public Dictionary<string, int> GetOrderCountByStatus()
        {
            return new Dictionary<string, int>
            {
                { "Draft", GetDraftOrdersCount() },
                { "Scheduled", GetScheduledOrdersCount() },
                { "In Progress", GetInProgressOrdersCount() },
                { "Completed", GetCompletedOrdersCount() }
            };
        }

        public List<ProductionOrder> GetUpcomingOrders(int days = 7)
        {
            var today = DateTime.Today;
            var futureDate = today.AddDays(days);
            return GetProductionOrdersByDateRange(today, futureDate)
                .Where(po => po.Status == "Scheduled" || po.Status == "Draft")
                .OrderBy(po => po.ScheduledDate)
                .ToList();
        }

        public List<ProductionOrder> GetOverdueOrders()
        {
            var today = DateTime.Today.Date;
            return GetAllProductionOrders()
                .Where(po => po.ScheduledDate.Date < today
                          && (po.Status == "Scheduled" || po.Status == "In Progress"))
                .OrderBy(po => po.ScheduledDate)
                .ToList();
        }

        public decimal GetProductionEfficiency()
        {
            var totalPlanned = GetTotalPlannedQuantity();
            var totalProduced = GetTotalProducedQuantity();

            if (totalPlanned == 0) return 0;

            return Math.Round((totalProduced / totalPlanned) * 100, 2);
        }
    }
}
