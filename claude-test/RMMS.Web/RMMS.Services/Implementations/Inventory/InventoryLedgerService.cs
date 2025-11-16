using RMMS.DataAccess.Repositories.Inventory;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Implementations.Inventory
{
    public class InventoryLedgerService : IInventoryLedgerService
    {
        private readonly IInventoryLedgerRepository _repository;

        public InventoryLedgerService(IInventoryLedgerRepository repository)
        {
            _repository = repository;
        }

        public List<InventoryLedger> GetAllInventory(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public InventoryLedger? GetInventoryById(int id)
        {
            return _repository.GetById(id);
        }

        public InventoryLedger? GetInventoryByProductAndWarehouse(int productId, int warehouseId, int? zoneId = null)
        {
            return _repository.GetByProductAndWarehouse(productId, warehouseId, zoneId);
        }

        public List<InventoryLedger> GetInventoryByProduct(int productId)
        {
            return _repository.GetByProduct(productId);
        }

        public List<InventoryLedger> GetInventoryByWarehouse(int warehouseId)
        {
            return _repository.GetByWarehouse(warehouseId);
        }

        public List<InventoryLedger> GetLowStockItems()
        {
            return _repository.GetLowStockItems();
        }

        public List<InventoryLedger> GetOverStockItems()
        {
            return _repository.GetOverStockItems();
        }

        public List<InventoryLedger> GetReorderItems()
        {
            return _repository.GetReorderItems();
        }

        public int CreateInventory(InventoryLedger ledger, string createdBy)
        {
            ledger.CreatedDate = DateTime.Now;
            ledger.CreatedBy = createdBy;
            ledger.IsActive = true;
            ledger.LastUpdated = DateTime.Now;

            // Calculate total value
            ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;

            // If no movement date set, use creation date
            if (!ledger.LastMovementDate.HasValue)
            {
                ledger.LastMovementDate = DateTime.Now;
            }

            return _repository.Create(ledger);
        }

        public bool UpdateInventory(InventoryLedger ledger, string modifiedBy)
        {
            ledger.ModifiedDate = DateTime.Now;
            ledger.ModifiedBy = modifiedBy;
            ledger.LastUpdated = DateTime.Now;

            // Recalculate total value
            ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;

            return _repository.Update(ledger);
        }

        public bool DeleteInventory(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public bool AdjustStock(int productId, int warehouseId, decimal quantity, int? zoneId = null, string modifiedBy = "System")
        {
            // This method updates stock quantity for existing ledger entry
            return _repository.UpdateStock(productId, warehouseId, quantity, zoneId);
        }

        public List<InventoryLedger> SearchInventory(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllInventory();

            return _repository.Search(searchTerm);
        }

        public decimal GetTotalInventoryValue()
        {
            return _repository.GetTotalInventoryValue();
        }

        public decimal GetWarehouseInventoryValue(int warehouseId)
        {
            return _repository.GetInventoryValueByWarehouse(warehouseId);
        }
    }
}
