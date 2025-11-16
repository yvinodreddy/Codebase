using RMMS.Models.Inventory;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public interface IInventoryLedgerRepository
    {
        List<InventoryLedger> GetAll(bool activeOnly = true);
        InventoryLedger? GetById(int id);
        InventoryLedger? GetByProductAndWarehouse(int productId, int warehouseId, int? zoneId = null);
        List<InventoryLedger> GetByProduct(int productId);
        List<InventoryLedger> GetByWarehouse(int warehouseId);
        List<InventoryLedger> GetLowStockItems();
        List<InventoryLedger> GetOverStockItems();
        List<InventoryLedger> GetReorderItems();
        int Create(InventoryLedger ledger);
        bool Update(InventoryLedger ledger);
        bool Delete(int id);
        bool UpdateStock(int productId, int warehouseId, decimal quantity, int? zoneId = null);
        List<InventoryLedger> Search(string searchTerm);
        decimal GetTotalInventoryValue();
        decimal GetInventoryValueByWarehouse(int warehouseId);
    }
}
