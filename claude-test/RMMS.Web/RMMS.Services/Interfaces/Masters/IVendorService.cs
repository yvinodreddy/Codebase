using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Masters
{
    public interface IVendorService
    {
        List<Vendor> GetAllVendors(bool activeOnly = true);
        Vendor? GetVendorById(int id);
        Vendor? GetVendorByCode(string code);
        int CreateVendor(Vendor vendor, string createdBy);
        bool UpdateVendor(Vendor vendor, string modifiedBy);
        bool DeleteVendor(int id, string deletedBy);
        List<Vendor> SearchVendors(string searchTerm);
        string GenerateVendorCode();
    }
}
