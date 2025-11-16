using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Masters
{
    public interface IEmployeeRepository
    {
        List<Employee> GetAll(bool activeOnly = true);
        Employee? GetById(int id);
        Employee? GetByCode(string code);
        int Create(Employee employee);
        bool Update(Employee employee);
        bool Delete(int id);
        List<Employee> Search(string searchTerm);
        List<Employee> GetByDepartment(string department);
    }
}
