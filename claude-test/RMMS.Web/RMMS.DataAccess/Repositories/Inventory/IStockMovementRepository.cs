using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public interface IStockMovementRepository
    {
        List<StockMovement> GetAll(bool activeOnly = true);
        StockMovement? GetById(int id);
        StockMovement? GetByCode(string code);
        List<StockMovement> GetByProduct(int productId);
        List<StockMovement> GetByWarehouse(int warehouseId);
        List<StockMovement> GetByDateRange(DateTime startDate, DateTime endDate);
        List<StockMovement> GetByType(string movementType); // IN or OUT
        List<StockMovement> GetByCategory(string category);
        List<StockMovement> GetRecentMovements(int count = 10);
        int Create(StockMovement movement);
        bool Update(StockMovement movement);
        bool Delete(int id);
        List<StockMovement> Search(string searchTerm);
        string GenerateMovementCode();
    }
}
