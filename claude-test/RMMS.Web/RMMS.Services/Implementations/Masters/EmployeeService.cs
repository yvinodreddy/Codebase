using RMMS.DataAccess.Repositories.Masters;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Masters
{
    public class EmployeeService : IEmployeeService
    {
        private readonly IEmployeeRepository _repository;

        public EmployeeService(IEmployeeRepository repository)
        {
            _repository = repository;
        }

        public List<Employee> GetAllEmployees(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public Employee? GetEmployeeById(int id)
        {
            return _repository.GetById(id);
        }

        public Employee? GetEmployeeByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        public int CreateEmployee(Employee employee, string createdBy)
        {
            employee.CreatedDate = DateTime.Now;
            employee.CreatedBy = createdBy;
            employee.IsActive = true;

            if (string.IsNullOrEmpty(employee.EmployeeCode))
            {
                employee.EmployeeCode = GenerateEmployeeCode();
            }

            return _repository.Create(employee);
        }

        public bool UpdateEmployee(Employee employee, string modifiedBy)
        {
            employee.ModifiedDate = DateTime.Now;
            employee.ModifiedBy = modifiedBy;
            return _repository.Update(employee);
        }

        public bool DeleteEmployee(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public List<Employee> SearchEmployees(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllEmployees();

            return _repository.Search(searchTerm);
        }

        public List<Employee> GetEmployeesByDepartment(string department)
        {
            return _repository.GetByDepartment(department);
        }

        public string GenerateEmployeeCode()
        {
            var employees = _repository.GetAll(false);
            if (employees.Any())
            {
                var maxCode = employees
                    .Select(e => e.EmployeeCode)
                    .Where(code => code.StartsWith("EMP"))
                    .Select(code => int.TryParse(code.Substring(3), out int num) ? num : 0)
                    .DefaultIfEmpty(0)
                    .Max();
                return $"EMP{(maxCode + 1):D4}";
            }
            return "EMP0001";
        }
    }
}
