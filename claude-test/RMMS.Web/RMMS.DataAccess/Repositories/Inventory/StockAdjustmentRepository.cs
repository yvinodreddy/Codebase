using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public class StockAdjustmentRepository : IStockAdjustmentRepository
    {
        private readonly ApplicationDbContext _context;

        public StockAdjustmentRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<StockAdjustment> GetAll(bool activeOnly = true)
        {
            var query = _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(a => a.IsActive);

            return query.OrderByDescending(a => a.AdjustmentDate).ToList();
        }

        public StockAdjustment? GetById(int id)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .FirstOrDefault(a => a.Id == id);
        }

        public StockAdjustment? GetByCode(string code)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .FirstOrDefault(a => a.AdjustmentCode == code);
        }

        public List<StockAdjustment> GetByProduct(int productId)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.ProductId == productId && a.IsActive)
                .OrderByDescending(a => a.AdjustmentDate)
                .ToList();
        }

        public List<StockAdjustment> GetByWarehouse(int warehouseId)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.WarehouseId == warehouseId && a.IsActive)
                .OrderByDescending(a => a.AdjustmentDate)
                .ToList();
        }

        public List<StockAdjustment> GetPendingApprovals()
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.IsActive && a.RequiresApproval && !a.IsApproved && !a.IsRejected)
                .OrderBy(a => a.AdjustmentDate)
                .ToList();
        }

        public List<StockAdjustment> GetApproved()
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.IsActive && a.IsApproved)
                .OrderByDescending(a => a.ApprovalDate)
                .ToList();
        }

        public List<StockAdjustment> GetRejected()
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.IsActive && a.IsRejected)
                .OrderByDescending(a => a.ModifiedDate)
                .ToList();
        }

        public List<StockAdjustment> GetByDateRange(DateTime startDate, DateTime endDate)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.AdjustmentDate >= startDate && a.AdjustmentDate <= endDate && a.IsActive)
                .OrderByDescending(a => a.AdjustmentDate)
                .ToList();
        }

        public int Create(StockAdjustment adjustment)
        {
            adjustment.CreatedDate = DateTime.Now;
            _context.StockAdjustments.Add(adjustment);
            _context.SaveChanges();
            return adjustment.Id;
        }

        public bool Update(StockAdjustment adjustment)
        {
            adjustment.ModifiedDate = DateTime.Now;
            _context.StockAdjustments.Update(adjustment);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var adjustment = _context.StockAdjustments.Find(id);
            if (adjustment != null)
            {
                adjustment.IsActive = false;
                adjustment.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<StockAdjustment> Search(string searchTerm)
        {
            return _context.StockAdjustments
                .Include(a => a.Product)
                .Include(a => a.Warehouse)
                .Include(a => a.Zone)
                .Where(a => a.IsActive &&
                    (a.AdjustmentCode.Contains(searchTerm) ||
                     a.Product!.ProductName.Contains(searchTerm) ||
                     a.Product!.ProductCode.Contains(searchTerm) ||
                     a.Warehouse!.WarehouseName.Contains(searchTerm) ||
                     a.Reason.Contains(searchTerm)))
                .OrderByDescending(a => a.AdjustmentDate)
                .ToList();
        }

        public string GenerateAdjustmentCode()
        {
            var lastAdjustment = _context.StockAdjustments
                .OrderByDescending(a => a.Id)
                .FirstOrDefault();

            if (lastAdjustment == null)
                return "ADJ0001";

            // Extract numeric part from last code (e.g., ADJ0001 -> 1)
            var lastNumber = int.Parse(lastAdjustment.AdjustmentCode.Substring(3));
            var newNumber = lastNumber + 1;

            return $"ADJ{newNumber:D4}"; // Format as ADJ0001, ADJ0002, etc.
        }
    }
}
