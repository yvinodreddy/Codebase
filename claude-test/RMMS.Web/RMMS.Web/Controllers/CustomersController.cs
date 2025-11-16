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
    public class CustomersController : Controller
    {
        private readonly ICustomerService _customerService;
        private readonly ILogger<CustomersController> _logger;

        public CustomersController(ICustomerService customerService, ILogger<CustomersController> logger)
        {
            _customerService = customerService;
            _logger = logger;
        }

        // GET: Customers
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "CustomerName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                var customers = string.IsNullOrWhiteSpace(searchTerm)
                    ? _customerService.GetAllCustomers()
                    : _customerService.SearchCustomers(searchTerm);

                // Apply sorting
                var customersQuery = customers.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Customer>.Create(customersQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading customers");
                TempData["Error"] = "Error loading customers: " + ex.Message;
                return View(new PagedResult<Customer>());
            }
        }

        // GET: Customers/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var customer = _customerService.GetCustomerById(id);
                if (customer == null)
                    return NotFound();

                return View(customer);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading customer {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Customers/Create
        public IActionResult Create()
        {
            var customer = new Customer
            {
                CustomerCode = _customerService.GenerateCustomerCode(),
                Status = "Active"
            };
            return View(customer);
        }

        // POST: Customers/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Customer customer)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var customerId = _customerService.CreateCustomer(customer, username);
                    TempData["Success"] = $"Customer {customer.CustomerName} created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(customer);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating customer");
                ModelState.AddModelError("", "Error creating customer: " + ex.Message);
                return View(customer);
            }
        }

        // GET: Customers/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var customer = _customerService.GetCustomerById(id);
                if (customer == null)
                    return NotFound();

                return View(customer);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading customer {id} for edit");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Customers/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Customer customer)
        {
            if (id != customer.Id)
                return BadRequest();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var result = _customerService.UpdateCustomer(customer, username);
                    if (result)
                    {
                        TempData["Success"] = "Customer updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    ModelState.AddModelError("", "Failed to update customer");
                }
                return View(customer);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating customer {id}");
                ModelState.AddModelError("", "Error updating customer: " + ex.Message);
                return View(customer);
            }
        }

        // GET: Customers/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var customer = _customerService.GetCustomerById(id);
                if (customer == null)
                    return NotFound();

                return View(customer);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading customer {id} for delete");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Customers/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var result = _customerService.DeleteCustomer(id, username);
                if (result)
                    TempData["Success"] = "Customer deleted successfully!";
                else
                    TempData["Error"] = "Failed to delete customer";

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting customer {id}");
                TempData["Error"] = "Error deleting customer: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
