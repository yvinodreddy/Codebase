using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public class WarehouseRepository : IWarehouseRepository
    {
        private readonly ApplicationDbContext _context;

        public WarehouseRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Warehouse> GetAll(bool activeOnly = true)
        {
            var query = _context.Warehouses
                .Include(w => w.Zones)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(w => w.IsActive);

            return query.OrderByDescending(w => w.CreatedDate).ToList();
        }

        public Warehouse? GetById(int id)
        {
            return _context.Warehouses
                .Include(w => w.Zones)
                .FirstOrDefault(w => w.Id == id);
        }

        public Warehouse? GetByCode(string code)
        {
            return _context.Warehouses
                .Include(w => w.Zones)
                .FirstOrDefault(w => w.WarehouseCode == code);
        }

        public int Create(Warehouse warehouse)
        {
            warehouse.CreatedDate = DateTime.Now;
            warehouse.AvailableCapacity = warehouse.TotalCapacity - warehouse.UsedCapacity;

            _context.Warehouses.Add(warehouse);
            _context.SaveChanges();
            return warehouse.Id;
        }

        public bool Update(Warehouse warehouse)
        {
            warehouse.ModifiedDate = DateTime.Now;
            warehouse.AvailableCapacity = warehouse.TotalCapacity - warehouse.UsedCapacity;

            _context.Warehouses.Update(warehouse);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var warehouse = _context.Warehouses.Find(id);
            if (warehouse != null)
            {
                warehouse.IsActive = false;
                warehouse.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<Warehouse> Search(string searchTerm)
        {
            return _context.Warehouses
                .Include(w => w.Zones)
                .Where(w => w.IsActive &&
                    (w.WarehouseName.Contains(searchTerm) ||
                     w.WarehouseCode.Contains(searchTerm) ||
                     (w.Location != null && w.Location.Contains(searchTerm)) ||
                     (w.City != null && w.City.Contains(searchTerm))))
                .OrderByDescending(w => w.CreatedDate)
                .ToList();
        }

        public string GenerateWarehouseCode()
        {
            var lastWarehouse = _context.Warehouses
                .OrderByDescending(w => w.Id)
                .FirstOrDefault();

            if (lastWarehouse == null)
                return "WRHS0001";

            // Extract numeric part from last code (e.g., WRHS0001 -> 1)
            var lastNumber = int.Parse(lastWarehouse.WarehouseCode.Substring(4));
            var newNumber = lastNumber + 1;

            return $"WRHS{newNumber:D4}"; // Format as WRHS0001, WRHS0002, etc.
        }
    }
}
