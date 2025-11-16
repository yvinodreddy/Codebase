using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public class StockMovementRepository : IStockMovementRepository
    {
        private readonly ApplicationDbContext _context;

        public StockMovementRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<StockMovement> GetAll(bool activeOnly = true)
        {
            var query = _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(m => m.IsActive);

            return query.OrderByDescending(m => m.MovementDate).ToList();
        }

        public StockMovement? GetById(int id)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .FirstOrDefault(m => m.Id == id);
        }

        public StockMovement? GetByCode(string code)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .FirstOrDefault(m => m.MovementCode == code);
        }

        public List<StockMovement> GetByProduct(int productId)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.ProductId == productId && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public List<StockMovement> GetByWarehouse(int warehouseId)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.WarehouseId == warehouseId && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public List<StockMovement> GetByDateRange(DateTime startDate, DateTime endDate)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.MovementDate >= startDate && m.MovementDate <= endDate && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public List<StockMovement> GetByType(string movementType)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.MovementType == movementType && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public List<StockMovement> GetByCategory(string category)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.MovementCategory == category && m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public List<StockMovement> GetRecentMovements(int count = 10)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.IsActive)
                .OrderByDescending(m => m.MovementDate)
                .Take(count)
                .ToList();
        }

        public int Create(StockMovement movement)
        {
            movement.CreatedDate = DateTime.Now;
            movement.TotalCost = movement.Quantity * movement.UnitCost;

            _context.StockMovements.Add(movement);
            _context.SaveChanges();
            return movement.Id;
        }

        public bool Update(StockMovement movement)
        {
            movement.ModifiedDate = DateTime.Now;
            movement.TotalCost = movement.Quantity * movement.UnitCost;

            _context.StockMovements.Update(movement);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var movement = _context.StockMovements.Find(id);
            if (movement != null)
            {
                movement.IsActive = false;
                movement.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<StockMovement> Search(string searchTerm)
        {
            return _context.StockMovements
                .Include(m => m.Product)
                .Include(m => m.Warehouse)
                .Include(m => m.Zone)
                .Where(m => m.IsActive &&
                    (m.MovementCode.Contains(searchTerm) ||
                     m.Product!.ProductName.Contains(searchTerm) ||
                     m.Product!.ProductCode.Contains(searchTerm) ||
                     m.Warehouse!.WarehouseName.Contains(searchTerm) ||
                     (m.ReferenceNumber != null && m.ReferenceNumber.Contains(searchTerm))))
                .OrderByDescending(m => m.MovementDate)
                .ToList();
        }

        public string GenerateMovementCode()
        {
            var lastMovement = _context.StockMovements
                .OrderByDescending(m => m.Id)
                .FirstOrDefault();

            if (lastMovement == null)
                return "STM0001";

            // Extract numeric part from last code (e.g., STM0001 -> 1)
            var lastNumber = int.Parse(lastMovement.MovementCode.Substring(3));
            var newNumber = lastNumber + 1;

            return $"STM{newNumber:D4}"; // Format as STM0001, STM0002, etc.
        }
    }
}
