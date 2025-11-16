using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public class InventoryLedgerRepository : IInventoryLedgerRepository
    {
        private readonly ApplicationDbContext _context;

        public InventoryLedgerRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<InventoryLedger> GetAll(bool activeOnly = true)
        {
            var query = _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(i => i.IsActive);

            return query.OrderByDescending(i => i.CreatedDate).ToList();
        }

        public InventoryLedger? GetById(int id)
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .FirstOrDefault(i => i.Id == id);
        }

        public InventoryLedger? GetByProductAndWarehouse(int productId, int warehouseId, int? zoneId = null)
        {
            var query = _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.ProductId == productId && i.WarehouseId == warehouseId && i.IsActive);

            if (zoneId.HasValue)
                query = query.Where(i => i.ZoneId == zoneId.Value);

            return query.FirstOrDefault();
        }

        public List<InventoryLedger> GetByProduct(int productId)
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.ProductId == productId && i.IsActive)
                .OrderBy(i => i.Warehouse!.WarehouseName)
                .ToList();
        }

        public List<InventoryLedger> GetByWarehouse(int warehouseId)
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.WarehouseId == warehouseId && i.IsActive)
                .OrderBy(i => i.Product!.ProductName)
                .ToList();
        }

        public List<InventoryLedger> GetLowStockItems()
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.IsActive && i.CurrentStock <= i.MinimumLevel)
                .OrderBy(i => i.CurrentStock)
                .ToList();
        }

        public List<InventoryLedger> GetOverStockItems()
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.IsActive && i.CurrentStock >= i.MaximumLevel)
                .OrderByDescending(i => i.CurrentStock)
                .ToList();
        }

        public List<InventoryLedger> GetReorderItems()
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.IsActive && i.CurrentStock <= i.ReorderLevel && i.CurrentStock > i.MinimumLevel)
                .OrderBy(i => i.CurrentStock)
                .ToList();
        }

        public int Create(InventoryLedger ledger)
        {
            ledger.CreatedDate = DateTime.Now;
            ledger.LastUpdated = DateTime.Now;
            ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;

            _context.InventoryLedger.Add(ledger);
            _context.SaveChanges();
            return ledger.Id;
        }

        public bool Update(InventoryLedger ledger)
        {
            ledger.ModifiedDate = DateTime.Now;
            ledger.LastUpdated = DateTime.Now;
            ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;

            _context.InventoryLedger.Update(ledger);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var ledger = _context.InventoryLedger.Find(id);
            if (ledger != null)
            {
                ledger.IsActive = false;
                ledger.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public bool UpdateStock(int productId, int warehouseId, decimal quantity, int? zoneId = null)
        {
            var ledger = GetByProductAndWarehouse(productId, warehouseId, zoneId);
            if (ledger != null)
            {
                ledger.CurrentStock = quantity;
                ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;
                ledger.LastMovementDate = DateTime.Now;
                ledger.LastUpdated = DateTime.Now;
                ledger.ModifiedDate = DateTime.Now;

                _context.InventoryLedger.Update(ledger);
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<InventoryLedger> Search(string searchTerm)
        {
            return _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Include(i => i.Zone)
                .Where(i => i.IsActive &&
                    (i.Product!.ProductName.Contains(searchTerm) ||
                     i.Product!.ProductCode.Contains(searchTerm) ||
                     i.Warehouse!.WarehouseName.Contains(searchTerm) ||
                     i.Warehouse!.WarehouseCode.Contains(searchTerm)))
                .OrderByDescending(i => i.CreatedDate)
                .ToList();
        }

        public decimal GetTotalInventoryValue()
        {
            return _context.InventoryLedger
                .Where(i => i.IsActive)
                .Sum(i => i.TotalValue);
        }

        public decimal GetInventoryValueByWarehouse(int warehouseId)
        {
            return _context.InventoryLedger
                .Where(i => i.IsActive && i.WarehouseId == warehouseId)
                .Sum(i => i.TotalValue);
        }
    }
}
