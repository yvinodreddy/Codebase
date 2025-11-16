using RMMS.Models.Inventory;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public interface IWarehouseRepository
    {
        List<Warehouse> GetAll(bool activeOnly = true);
        Warehouse? GetById(int id);
        Warehouse? GetByCode(string code);
        int Create(Warehouse warehouse);
        bool Update(Warehouse warehouse);
        bool Delete(int id);
        List<Warehouse> Search(string searchTerm);
        string GenerateWarehouseCode();
    }
}
