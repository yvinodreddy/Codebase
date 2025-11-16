using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Inventory
{
    public interface IStockMovementService
    {
        List<StockMovement> GetAllMovements(bool activeOnly = true);
        StockMovement? GetMovementById(int id);
        StockMovement? GetMovementByCode(string code);
        List<StockMovement> GetMovementsByProduct(int productId);
        List<StockMovement> GetMovementsByWarehouse(int warehouseId);
        List<StockMovement> GetMovementsByDateRange(DateTime startDate, DateTime endDate);
        List<StockMovement> GetMovementsByType(string movementType);
        List<StockMovement> GetMovementsByCategory(string category);
        List<StockMovement> GetRecentMovements(int count = 10);
        int CreateMovement(StockMovement movement, string createdBy);
        bool UpdateMovement(StockMovement movement, string modifiedBy);
        bool DeleteMovement(int id, string deletedBy);
        List<StockMovement> SearchMovements(string searchTerm);
        string GenerateMovementCode();
        (bool success, string message) ValidateMovement(StockMovement movement);
    }
}
