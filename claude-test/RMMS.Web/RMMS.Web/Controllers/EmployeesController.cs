using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Linq;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class EmployeesController : Controller
    {
        private readonly IEmployeeService _employeeService;
        private readonly ILogger<EmployeesController> _logger;

        public EmployeesController(IEmployeeService employeeService, ILogger<EmployeesController> logger)
        {
            _employeeService = employeeService;
            _logger = logger;
        }

        // GET: Employees
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "EmployeeName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                List<Employee> employees;

                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    employees = _employeeService.SearchEmployees(searchTerm);
                }
                else
                {
                    employees = _employeeService.GetAllEmployees();
                }

                // Apply sorting
                var employeesQuery = employees.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Employee>.Create(employeesQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading employees");
                TempData["Error"] = "Error loading employees: " + ex.Message;
                return View(new PagedResult<Employee>());
            }
        }

        // GET: Employees/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var employee = _employeeService.GetEmployeeById(id);
                if (employee == null)
                    return NotFound();

                return View(employee);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading employee {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Employees/Create
        public IActionResult Create()
        {
            var employee = new Employee
            {
                EmployeeCode = _employeeService.GenerateEmployeeCode(),
                Status = "Active"
            };
            return View(employee);
        }

        // POST: Employees/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Employee employee)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var employeeId = _employeeService.CreateEmployee(employee, username);
                    TempData["Success"] = $"Employee {employee.EmployeeName} created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(employee);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating employee");
                ModelState.AddModelError("", "Error creating employee: " + ex.Message);
                return View(employee);
            }
        }

        // GET: Employees/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var employee = _employeeService.GetEmployeeById(id);
                if (employee == null)
                    return NotFound();

                return View(employee);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading employee {id} for edit");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Employees/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Employee employee)
        {
            if (id != employee.Id)
                return BadRequest();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var result = _employeeService.UpdateEmployee(employee, username);
                    if (result)
                    {
                        TempData["Success"] = "Employee updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    ModelState.AddModelError("", "Failed to update employee");
                }
                return View(employee);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating employee {id}");
                ModelState.AddModelError("", "Error updating employee: " + ex.Message);
                return View(employee);
            }
        }

        // GET: Employees/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var employee = _employeeService.GetEmployeeById(id);
                if (employee == null)
                    return NotFound();

                return View(employee);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading employee {id} for delete");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Employees/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var result = _employeeService.DeleteEmployee(id, username);
                if (result)
                    TempData["Success"] = "Employee deleted successfully!";
                else
                    TempData["Error"] = "Failed to delete employee";

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting employee {id}");
                TempData["Error"] = "Error deleting employee: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
