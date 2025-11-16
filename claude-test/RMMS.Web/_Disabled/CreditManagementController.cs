using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using RMMS.Services.Services;
using RMMS.DataAccess.Data;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Web.Controllers
{
    [Authorize]
    public class CreditManagementController : Controller
    {
        private readonly ICreditManagementService _creditService;
        private readonly ApplicationDbContext _context;

        public CreditManagementController(
            ICreditManagementService creditService,
            ApplicationDbContext context)
        {
            _creditService = creditService;
            _context = context;
        }

        // GET: CreditManagement
        public async Task<IActionResult> Index()
        {
            var customersWithCredit = await _context.Customers
                .Where(c => c.IsActive && c.CreditLimit != null && c.CreditLimit > 0)
                .OrderBy(c => c.CustomerName)
                .ToListAsync();

            var creditStatuses = new List<CreditStatus>();

            foreach (var customer in customersWithCredit)
            {
                var status = await _creditService.GetCustomerCreditStatus(customer.Id);
                creditStatuses.Add(status);
            }

            // Sort by utilization percentage (highest first)
            creditStatuses = creditStatuses
                .OrderByDescending(c => c.UtilizationPercentage)
                .ToList();

            ViewBag.TotalCustomers = customersWithCredit.Count;
            ViewBag.ExceededCount = creditStatuses.Count(c => c.Status == "Exceeded");
            ViewBag.CriticalCount = creditStatuses.Count(c => c.Status == "Critical");
            ViewBag.WarningCount = creditStatuses.Count(c => c.Status == "Warning");
            ViewBag.GoodCount = creditStatuses.Count(c => c.Status == "Good");

            return View(creditStatuses);
        }

        // GET: CreditManagement/CustomerStatus/5
        public async Task<IActionResult> CustomerStatus(int id)
        {
            var status = await _creditService.GetCustomerCreditStatus(id);

            if (status.CustomerName == "Unknown")
            {
                TempData["ErrorMessage"] = "Customer not found.";
                return RedirectToAction(nameof(Index));
            }

            // Get transaction history
            var riceSales = await _context.RiceSales
                .Where(r => r.CustomerId == id && r.IsActive)
                .OrderByDescending(r => r.SaleDate)
                .Take(10)
                .ToListAsync();

            var byProductSales = await _context.ByProductSales
                .Where(b => b.CustomerId == id && b.IsActive)
                .OrderByDescending(b => b.SaleDate)
                .Take(10)
                .ToListAsync();

            ViewBag.RiceSales = riceSales;
            ViewBag.ByProductSales = byProductSales;
            ViewBag.Alert = await _creditService.GenerateCreditAlert(id);

            return View(status);
        }

        // GET: CreditManagement/Alerts
        public async Task<IActionResult> Alerts()
        {
            var customersWithCredit = await _context.Customers
                .Where(c => c.IsActive && c.CreditLimit != null && c.CreditLimit > 0)
                .ToListAsync();

            var alerts = new List<CreditLimitAlert>();

            foreach (var customer in customersWithCredit)
            {
                var status = await _creditService.GetCustomerCreditStatus(customer.Id);

                // Only include alerts that require attention
                if (status.Status == "Exceeded" || status.Status == "Critical" || status.Status == "Warning")
                {
                    var alert = await _creditService.GenerateCreditAlert(customer.Id);
                    alerts.Add(alert);
                }
            }

            // Sort by severity
            alerts = alerts.OrderByDescending(a => a.RequiresAction)
                          .ThenByDescending(a => a.UtilizationPercentage)
                          .ToList();

            ViewBag.CriticalAlerts = alerts.Count(a => a.AlertType == "Limit Exceeded");
            ViewBag.WarningAlerts = alerts.Count(a => a.AlertType == "Near Limit");

            return View(alerts);
        }

        // GET: CreditManagement/ExceedingLimit
        public async Task<IActionResult> ExceedingLimit()
        {
            var exceedingCustomers = await _creditService.GetCustomersExceedingCreditLimit();

            var statuses = new List<CreditStatus>();
            foreach (var customer in exceedingCustomers)
            {
                var status = await _creditService.GetCustomerCreditStatus(customer.Id);
                statuses.Add(status);
            }

            statuses = statuses.OrderByDescending(s => s.CreditUtilized - s.CreditLimit).ToList();

            return View(statuses);
        }

        // POST: CreditManagement/BlockCustomer/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> BlockCustomer(int id)
        {
            var customer = await _context.Customers.FindAsync(id);

            if (customer == null)
            {
                TempData["ErrorMessage"] = "Customer not found.";
                return RedirectToAction(nameof(Index));
            }

            customer.Status = "Blocked";
            customer.ModifiedDate = DateTime.Now;
            customer.ModifiedBy = User.Identity?.Name;

            await _context.SaveChangesAsync();

            TempData["SuccessMessage"] = $"Customer {customer.CustomerName} has been blocked due to credit limit exceeded.";
            return RedirectToAction(nameof(CustomerStatus), new { id = id });
        }

        // POST: CreditManagement/UnblockCustomer/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> UnblockCustomer(int id)
        {
            var customer = await _context.Customers.FindAsync(id);

            if (customer == null)
            {
                TempData["ErrorMessage"] = "Customer not found.";
                return RedirectToAction(nameof(Index));
            }

            customer.Status = "Active";
            customer.ModifiedDate = DateTime.Now;
            customer.ModifiedBy = User.Identity?.Name;

            await _context.SaveChangesAsync();

            TempData["SuccessMessage"] = $"Customer {customer.CustomerName} has been unblocked.";
            return RedirectToAction(nameof(CustomerStatus), new { id = id });
        }

        // API: CreditManagement/ValidateCredit
        [HttpPost]
        public async Task<JsonResult> ValidateCredit(int customerId, decimal orderAmount)
        {
            var isValid = await _creditService.ValidateOrderAgainstCreditLimit(customerId, orderAmount);
            var status = await _creditService.GetCustomerCreditStatus(customerId);

            return Json(new
            {
                isValid = isValid,
                creditLimit = status.CreditLimit,
                creditUtilized = status.CreditUtilized,
                availableCredit = status.AvailableCredit,
                utilizationPercentage = status.UtilizationPercentage,
                message = isValid
                    ? "Credit limit validation passed."
                    : "Order amount exceeds available credit limit."
            });
        }

        // GET: CreditManagement/Dashboard
        public async Task<IActionResult> Dashboard()
        {
            var customersWithCredit = await _context.Customers
                .Where(c => c.IsActive && c.CreditLimit != null && c.CreditLimit > 0)
                .ToListAsync();

            var statuses = new List<CreditStatus>();
            foreach (var customer in customersWithCredit)
            {
                var status = await _creditService.GetCustomerCreditStatus(customer.Id);
                statuses.Add(status);
            }

            ViewBag.TotalCustomers = customersWithCredit.Count;
            ViewBag.TotalCreditLimit = customersWithCredit.Sum(c => c.CreditLimit ?? 0);
            ViewBag.TotalUtilized = statuses.Sum(s => s.CreditUtilized);
            ViewBag.TotalAvailable = statuses.Sum(s => s.AvailableCredit);
            ViewBag.AverageUtilization = statuses.Any() ? statuses.Average(s => s.UtilizationPercentage) : 0;

            ViewBag.ExceededCount = statuses.Count(c => c.Status == "Exceeded");
            ViewBag.CriticalCount = statuses.Count(c => c.Status == "Critical");
            ViewBag.WarningCount = statuses.Count(c => c.Status == "Warning");
            ViewBag.GoodCount = statuses.Count(c => c.Status == "Good");

            // Top 10 customers by utilization
            ViewBag.TopUtilizers = statuses.OrderByDescending(s => s.UtilizationPercentage).Take(10).ToList();

            return View();
        }
    }
}
