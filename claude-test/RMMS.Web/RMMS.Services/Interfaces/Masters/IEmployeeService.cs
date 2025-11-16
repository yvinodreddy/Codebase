using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Masters
{
    public interface IEmployeeService
    {
        List<Employee> GetAllEmployees(bool activeOnly = true);
        Employee? GetEmployeeById(int id);
        Employee? GetEmployeeByCode(string code);
        int CreateEmployee(Employee employee, string createdBy);
        bool UpdateEmployee(Employee employee, string modifiedBy);
        bool DeleteEmployee(int id, string deletedBy);
        List<Employee> SearchEmployees(string searchTerm);
        List<Employee> GetEmployeesByDepartment(string department);
        string GenerateEmployeeCode();
    }
}
