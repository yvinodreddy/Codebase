using RMMS.DataAccess.Repositories.Masters;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Masters
{
    public class VendorService : IVendorService
    {
        private readonly IVendorRepository _repository;

        public VendorService(IVendorRepository repository)
        {
            _repository = repository;
        }

        public List<Vendor> GetAllVendors(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public Vendor? GetVendorById(int id)
        {
            return _repository.GetById(id);
        }

        public Vendor? GetVendorByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        public int CreateVendor(Vendor vendor, string createdBy)
        {
            vendor.CreatedDate = DateTime.Now;
            vendor.CreatedBy = createdBy;
            vendor.IsActive = true;

            if (string.IsNullOrEmpty(vendor.VendorCode))
            {
                vendor.VendorCode = GenerateVendorCode();
            }

            return _repository.Create(vendor);
        }

        public bool UpdateVendor(Vendor vendor, string modifiedBy)
        {
            vendor.ModifiedDate = DateTime.Now;
            vendor.ModifiedBy = modifiedBy;
            return _repository.Update(vendor);
        }

        public bool DeleteVendor(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public List<Vendor> SearchVendors(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllVendors();

            return _repository.Search(searchTerm);
        }

        public string GenerateVendorCode()
        {
            var vendors = _repository.GetAll(false);
            if (vendors.Any())
            {
                var maxCode = vendors
                    .Select(v => v.VendorCode)
                    .Where(code => code.StartsWith("VEND"))
                    .Select(code => int.TryParse(code.Substring(4), out int num) ? num : 0)
                    .DefaultIfEmpty(0)
                    .Max();
                return $"VEND{(maxCode + 1):D4}";
            }
            return "VEND0001";
        }
    }
}
