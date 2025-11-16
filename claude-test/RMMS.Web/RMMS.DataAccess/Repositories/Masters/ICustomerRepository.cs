using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Masters
{
    public interface ICustomerRepository
    {
        List<Customer> GetAll(bool activeOnly = true);
        Customer? GetById(int id);
        Customer? GetByCode(string code);
        int Create(Customer customer);
        bool Update(Customer customer);
        bool Delete(int id);
        List<Customer> Search(string searchTerm);
    }
}
