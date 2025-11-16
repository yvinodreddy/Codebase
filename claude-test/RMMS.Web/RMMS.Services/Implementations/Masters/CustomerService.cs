using RMMS.DataAccess.Repositories.Masters;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Masters
{
    public class CustomerService : ICustomerService
    {
        private readonly ICustomerRepository _repository;

        public CustomerService(ICustomerRepository repository)
        {
            _repository = repository;
        }

        public List<Customer> GetAllCustomers(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public Customer? GetCustomerById(int id)
        {
            return _repository.GetById(id);
        }

        public Customer? GetCustomerByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        public int CreateCustomer(Customer customer, string createdBy)
        {
            customer.CreatedDate = DateTime.Now;
            customer.CreatedBy = createdBy;
            customer.IsActive = true;

            if (string.IsNullOrEmpty(customer.CustomerCode))
            {
                customer.CustomerCode = GenerateCustomerCode();
            }

            return _repository.Create(customer);
        }

        public bool UpdateCustomer(Customer customer, string modifiedBy)
        {
            customer.ModifiedDate = DateTime.Now;
            customer.ModifiedBy = modifiedBy;
            return _repository.Update(customer);
        }

        public bool DeleteCustomer(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public List<Customer> SearchCustomers(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllCustomers();

            return _repository.Search(searchTerm);
        }

        public string GenerateCustomerCode()
        {
            var customers = _repository.GetAll(false);
            if (customers.Any())
            {
                var maxCode = customers
                    .Select(c => c.CustomerCode)
                    .Where(code => code.StartsWith("CUST"))
                    .Select(code => int.TryParse(code.Substring(4), out int num) ? num : 0)
                    .DefaultIfEmpty(0)
                    .Max();
                return $"CUST{(maxCode + 1):D4}";
            }
            return "CUST0001";
        }
    }
}
