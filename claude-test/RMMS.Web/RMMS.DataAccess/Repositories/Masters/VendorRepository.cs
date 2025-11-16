using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Masters
{
    public class VendorRepository : IVendorRepository
    {
        private readonly ApplicationDbContext _context;

        public VendorRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Vendor> GetAll(bool activeOnly = true)
        {
            var query = _context.Vendors
                .Include(v => v.Contacts)
                .Include(v => v.Addresses)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(v => v.IsActive);

            return query.OrderByDescending(v => v.CreatedDate).ToList();
        }

        public Vendor? GetById(int id)
        {
            return _context.Vendors
                .Include(v => v.Contacts)
                .Include(v => v.Addresses)
                .FirstOrDefault(v => v.Id == id);
        }

        public Vendor? GetByCode(string code)
        {
            return _context.Vendors
                .Include(v => v.Contacts)
                .Include(v => v.Addresses)
                .FirstOrDefault(v => v.VendorCode == code);
        }

        public int Create(Vendor vendor)
        {
            _context.Vendors.Add(vendor);
            _context.SaveChanges();
            return vendor.Id;
        }

        public bool Update(Vendor vendor)
        {
            _context.Vendors.Update(vendor);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var vendor = _context.Vendors.Find(id);
            if (vendor != null)
            {
                vendor.IsActive = false;
                vendor.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<Vendor> Search(string searchTerm)
        {
            return _context.Vendors
                .Include(v => v.Contacts)
                .Include(v => v.Addresses)
                .Where(v => v.IsActive &&
                    (v.VendorName.Contains(searchTerm) ||
                     v.VendorCode.Contains(searchTerm) ||
                     (v.GSTIN != null && v.GSTIN.Contains(searchTerm))))
                .OrderBy(v => v.VendorName)
                .ToList();
        }
    }
}
