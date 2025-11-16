using RMMS.Models.Production;

namespace RMMS.Services.Interfaces.Production
{
    public interface IProductionOrderService
    {
        // Basic CRUD
        ProductionOrder? GetProductionOrderById(int id);
        List<ProductionOrder> GetAllProductionOrders();
        bool CreateProductionOrder(ProductionOrder order, string createdBy);
        bool UpdateProductionOrder(ProductionOrder order, string modifiedBy);
        bool DeleteProductionOrder(int id);

        // Query Methods
        ProductionOrder? GetProductionOrderByOrderNumber(string orderNumber);
        List<ProductionOrder> GetProductionOrdersByStatus(string status);
        List<ProductionOrder> GetProductionOrdersByDateRange(DateTime startDate, DateTime endDate);
        List<ProductionOrder> GetProductionOrdersByMachine(int machineId);
        List<ProductionOrder> GetProductionOrdersBySupervisor(int supervisorId);
        List<ProductionOrder> GetProductionOrdersByPriority(string priority);
        List<ProductionOrder> GetScheduledProductionOrders(DateTime date);
        List<ProductionOrder> GetTodayScheduledOrders();
        List<ProductionOrder> GetInProgressProductionOrders();
        List<ProductionOrder> GetCompletedProductionOrders(int limit = 50);
        List<ProductionOrder> SearchProductionOrders(string searchTerm);

        // Statistics
        int GetTotalProductionOrdersCount();
        int GetDraftOrdersCount();
        int GetScheduledOrdersCount();
        int GetInProgressOrdersCount();
        int GetCompletedOrdersCount();
        decimal GetTotalPlannedQuantity();
        decimal GetTotalProducedQuantity();
        decimal GetAverageYieldPercent();

        // Business Logic
        string GenerateOrderNumber();
        bool ValidateOrderNumber(string orderNumber);
        bool CanStartProduction(int orderId);
        bool CanCompleteProduction(int orderId);
        bool CanCancelOrder(int orderId);

        // Workflow Methods
        bool ScheduleOrder(int orderId, DateTime scheduledDate, int? machineId, int? supervisorId, string modifiedBy);
        bool StartProduction(int orderId, string startedBy);
        bool CompleteProduction(int orderId, decimal actualQuantity, decimal actualYield, string completedBy);
        bool CancelOrder(int orderId, string cancelledBy, string reason);
        bool CloseOrder(int orderId, string closedBy);

        // Dashboard/Reporting
        Dictionary<string, int> GetOrderCountByStatus();
        List<ProductionOrder> GetUpcomingOrders(int days = 7);
        List<ProductionOrder> GetOverdueOrders();
        decimal GetProductionEfficiency();
    }
}
