using RMMS.Models.Production;

namespace RMMS.DataAccess.Repositories.Production
{
    public interface IProductionOrderRepository
    {
        // Basic CRUD
        ProductionOrder? GetProductionOrderById(int id);
        List<ProductionOrder> GetAllProductionOrders();
        bool CreateProductionOrder(ProductionOrder order);
        bool UpdateProductionOrder(ProductionOrder order);
        bool DeleteProductionOrder(int id);

        // Query Methods
        ProductionOrder? GetProductionOrderByOrderNumber(string orderNumber);
        List<ProductionOrder> GetProductionOrdersByStatus(string status);
        List<ProductionOrder> GetProductionOrdersByDateRange(DateTime startDate, DateTime endDate);
        List<ProductionOrder> GetProductionOrdersByMachine(int machineId);
        List<ProductionOrder> GetProductionOrdersBySupervisor(int supervisorId);
        List<ProductionOrder> GetProductionOrdersByPriority(string priority);
        List<ProductionOrder> GetScheduledProductionOrders(DateTime date);
        List<ProductionOrder> GetInProgressProductionOrders();
        List<ProductionOrder> GetCompletedProductionOrders(int limit = 50);
        List<ProductionOrder> SearchProductionOrders(string searchTerm);

        // Statistics
        int GetTotalProductionOrdersCount();
        int GetProductionOrdersCountByStatus(string status);
        decimal GetTotalPlannedQuantity();
        decimal GetTotalProducedQuantity();
        decimal GetAverageYieldPercent();

        // Code Generation
        string GenerateOrderNumber();

        // Status Management
        bool UpdateOrderStatus(int orderId, string newStatus, string modifiedBy);
        bool StartProduction(int orderId, string startedBy);
        bool CompleteProduction(int orderId, decimal actualQuantity, decimal actualYield, string completedBy);
        bool CancelOrder(int orderId, string cancelledBy, string reason);
    }
}
