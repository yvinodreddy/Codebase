using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Masters
{
    public class CustomerRepository : ICustomerRepository
    {
        private readonly ApplicationDbContext _context;

        public CustomerRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Customer> GetAll(bool activeOnly = true)
        {
            var query = _context.Customers
                .Include(c => c.Contacts)
                .Include(c => c.Addresses)
                .AsQueryable();

            if (activeOnly)
                query = query.Where(c => c.IsActive);

            return query.OrderByDescending(c => c.CreatedDate).ToList();
        }

        public Customer? GetById(int id)
        {
            return _context.Customers
                .Include(c => c.Contacts)
                .Include(c => c.Addresses)
                .FirstOrDefault(c => c.Id == id);
        }

        public Customer? GetByCode(string code)
        {
            return _context.Customers
                .Include(c => c.Contacts)
                .Include(c => c.Addresses)
                .FirstOrDefault(c => c.CustomerCode == code);
        }

        public int Create(Customer customer)
        {
            _context.Customers.Add(customer);
            _context.SaveChanges();
            return customer.Id;
        }

        public bool Update(Customer customer)
        {
            _context.Customers.Update(customer);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var customer = _context.Customers.Find(id);
            if (customer != null)
            {
                customer.IsActive = false;
                customer.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<Customer> Search(string searchTerm)
        {
            return _context.Customers
                .Include(c => c.Contacts)
                .Include(c => c.Addresses)
                .Where(c => c.IsActive &&
                    (c.CustomerName.Contains(searchTerm) ||
                     c.CustomerCode.Contains(searchTerm) ||
                     (c.GSTIN != null && c.GSTIN.Contains(searchTerm))))
                .OrderBy(c => c.CustomerName)
                .ToList();
        }
    }
}
