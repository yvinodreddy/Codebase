using RMMS.Models.Inventory;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Inventory
{
    public interface IInventoryLedgerService
    {
        List<InventoryLedger> GetAllInventory(bool activeOnly = true);
        InventoryLedger? GetInventoryById(int id);
        InventoryLedger? GetInventoryByProductAndWarehouse(int productId, int warehouseId, int? zoneId = null);
        List<InventoryLedger> GetInventoryByProduct(int productId);
        List<InventoryLedger> GetInventoryByWarehouse(int warehouseId);
        List<InventoryLedger> GetLowStockItems();
        List<InventoryLedger> GetOverStockItems();
        List<InventoryLedger> GetReorderItems();
        int CreateInventory(InventoryLedger ledger, string createdBy);
        bool UpdateInventory(InventoryLedger ledger, string modifiedBy);
        bool DeleteInventory(int id, string deletedBy);
        bool AdjustStock(int productId, int warehouseId, decimal quantity, int? zoneId = null, string modifiedBy = "System");
        List<InventoryLedger> SearchInventory(string searchTerm);
        decimal GetTotalInventoryValue();
        decimal GetWarehouseInventoryValue(int warehouseId);
    }
}
