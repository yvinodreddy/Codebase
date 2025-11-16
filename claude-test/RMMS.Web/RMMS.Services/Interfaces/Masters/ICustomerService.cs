using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Masters
{
    public interface ICustomerService
    {
        List<Customer> GetAllCustomers(bool activeOnly = true);
        Customer? GetCustomerById(int id);
        Customer? GetCustomerByCode(string code);
        int CreateCustomer(Customer customer, string createdBy);
        bool UpdateCustomer(Customer customer, string modifiedBy);
        bool DeleteCustomer(int id, string deletedBy);
        List<Customer> SearchCustomers(string searchTerm);
        string GenerateCustomerCode();
    }
}
