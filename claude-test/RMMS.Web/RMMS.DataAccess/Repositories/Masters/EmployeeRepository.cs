using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Masters
{
    public class EmployeeRepository : IEmployeeRepository
    {
        private readonly ApplicationDbContext _context;

        public EmployeeRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Employee> GetAll(bool activeOnly = true)
        {
            var query = _context.Employees.AsQueryable();

            if (activeOnly)
                query = query.Where(e => e.IsActive);

            return query.OrderByDescending(e => e.CreatedDate).ToList();
        }

        public Employee? GetById(int id)
        {
            return _context.Employees.FirstOrDefault(e => e.Id == id);
        }

        public Employee? GetByCode(string code)
        {
            return _context.Employees.FirstOrDefault(e => e.EmployeeCode == code);
        }

        public int Create(Employee employee)
        {
            _context.Employees.Add(employee);
            _context.SaveChanges();
            return employee.Id;
        }

        public bool Update(Employee employee)
        {
            _context.Employees.Update(employee);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var employee = _context.Employees.Find(id);
            if (employee != null)
            {
                employee.IsActive = false;
                employee.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<Employee> Search(string searchTerm)
        {
            return _context.Employees
                .Where(e => e.IsActive &&
                    (e.EmployeeName.Contains(searchTerm) ||
                     e.EmployeeCode.Contains(searchTerm) ||
                     (e.Mobile != null && e.Mobile.Contains(searchTerm)) ||
                     (e.Department != null && e.Department.Contains(searchTerm))))
                .OrderBy(e => e.EmployeeName)
                .ToList();
        }

        public List<Employee> GetByDepartment(string department)
        {
            return _context.Employees
                .Where(e => e.IsActive && e.Department == department)
                .OrderBy(e => e.EmployeeName)
                .ToList();
        }
    }
}
