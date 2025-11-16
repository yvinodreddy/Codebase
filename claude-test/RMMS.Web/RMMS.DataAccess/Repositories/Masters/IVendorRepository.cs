using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Masters
{
    public interface IVendorRepository
    {
        List<Vendor> GetAll(bool activeOnly = true);
        Vendor? GetById(int id);
        Vendor? GetByCode(string code);
        int Create(Vendor vendor);
        bool Update(Vendor vendor);
        bool Delete(int id);
        List<Vendor> Search(string searchTerm);
    }
}
