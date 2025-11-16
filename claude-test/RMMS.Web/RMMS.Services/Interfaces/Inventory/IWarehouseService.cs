using RMMS.Models.Inventory;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Inventory
{
    public interface IWarehouseService
    {
        List<Warehouse> GetAllWarehouses(bool activeOnly = true);
        Warehouse? GetWarehouseById(int id);
        Warehouse? GetWarehouseByCode(string code);
        int CreateWarehouse(Warehouse warehouse, string createdBy);
        bool UpdateWarehouse(Warehouse warehouse, string modifiedBy);
        bool DeleteWarehouse(int id, string deletedBy);
        List<Warehouse> SearchWarehouses(string searchTerm);
        string GenerateWarehouseCode();
    }
}
