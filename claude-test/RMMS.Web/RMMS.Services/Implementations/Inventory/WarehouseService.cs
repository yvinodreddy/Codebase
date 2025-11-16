using RMMS.DataAccess.Repositories.Inventory;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Implementations.Inventory
{
    public class WarehouseService : IWarehouseService
    {
        private readonly IWarehouseRepository _repository;

        public WarehouseService(IWarehouseRepository repository)
        {
            _repository = repository;
        }

        public List<Warehouse> GetAllWarehouses(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public Warehouse? GetWarehouseById(int id)
        {
            return _repository.GetById(id);
        }

        public Warehouse? GetWarehouseByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        public int CreateWarehouse(Warehouse warehouse, string createdBy)
        {
            warehouse.CreatedDate = DateTime.Now;
            warehouse.CreatedBy = createdBy;
            warehouse.IsActive = true;

            if (string.IsNullOrEmpty(warehouse.WarehouseCode))
            {
                warehouse.WarehouseCode = GenerateWarehouseCode();
            }

            // Calculate available capacity
            warehouse.AvailableCapacity = warehouse.TotalCapacity - warehouse.UsedCapacity;

            return _repository.Create(warehouse);
        }

        public bool UpdateWarehouse(Warehouse warehouse, string modifiedBy)
        {
            warehouse.ModifiedDate = DateTime.Now;
            warehouse.ModifiedBy = modifiedBy;

            // Recalculate available capacity
            warehouse.AvailableCapacity = warehouse.TotalCapacity - warehouse.UsedCapacity;

            return _repository.Update(warehouse);
        }

        public bool DeleteWarehouse(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public List<Warehouse> SearchWarehouses(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllWarehouses();

            return _repository.Search(searchTerm);
        }

        public string GenerateWarehouseCode()
        {
            return _repository.GenerateWarehouseCode();
        }
    }
}
