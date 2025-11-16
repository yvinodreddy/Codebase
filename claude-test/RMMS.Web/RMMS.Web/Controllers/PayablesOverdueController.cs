using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class PayablesOverdueController : Controller
    {
        private readonly ILogger<PayablesOverdueController> _logger;
        private readonly IPayableOverdueService _payableOverdueService;

        public PayablesOverdueController(
            ILogger<PayablesOverdueController> logger,
            IPayableOverdueService payableOverdueService)
        {
            _logger = logger;
            _payableOverdueService = payableOverdueService;
        }

        public IActionResult Index()
        {
            try
            {
                var model = _payableOverdueService.GetAll();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving payables");
                TempData["Error"] = "Error loading payables";
                return View(new List<PayableOverdue>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var payable = _payableOverdueService.GetById(id);
                if (payable == null)
                {
                    TempData["Error"] = "Payable record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(payable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error retrieving payable with ID {id}");
                TempData["Error"] = "Error loading payable details";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(PayableOverdue model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    string username = User.Identity?.Name ?? "System";
                    _payableOverdueService.Create(model, username);
                    TempData["Success"] = "Payable record created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating payable record");
                TempData["Error"] = "An error occurred while creating the payable record.";
                return View(model);
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var payable = _payableOverdueService.GetById(id);
                if (payable == null)
                {
                    TempData["Error"] = "Payable record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(payable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading payable with ID {id}");
                TempData["Error"] = "Error loading payable record";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(PayableOverdue model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    string username = User.Identity?.Name ?? "System";
                    _payableOverdueService.Update(model, username);
                    TempData["Success"] = "Payable record updated successfully!";
                    return RedirectToAction(nameof(Details), new { id = model.Id });
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating payable with ID {model.Id}");
                TempData["Error"] = "An error occurred while updating the payable record.";
                return View(model);
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                _payableOverdueService.Delete(id, username);
                TempData["Success"] = "Payable record deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting payable with ID {id}");
                TempData["Error"] = "An error occurred while deleting the payable record.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult RecordPayment(int id)
        {
            try
            {
                var payable = _payableOverdueService.GetById(id);
                if (payable == null)
                {
                    TempData["Error"] = "Payable record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(payable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading payable with ID {id}");
                TempData["Error"] = "Unable to load payable record";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult RecordPayment(int id, decimal paymentAmount)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                _payableOverdueService.RecordPayment(id, paymentAmount, username);
                TempData["Success"] = "Payment recorded successfully!";
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error recording payment for payable ID {id}");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult SendReminder(int id)
        {
            try
            {
                var payable = _payableOverdueService.GetById(id);
                if (payable == null)
                {
                    TempData["Error"] = "Payable record not found";
                    return RedirectToAction(nameof(Index));
                }

                // Log the reminder action
                _logger.LogInformation($"Payment reminder sent for payable ID: {id}, Supplier: {payable.SupplierName}, Amount: {payable.BalancePayable}");

                TempData["Success"] = $"Payment reminder sent successfully to {payable.SupplierName}!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending payment reminder");
                TempData["Error"] = "Error sending payment reminder. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult SendBulkReminders()
        {
            try
            {
                var allPayables = _payableOverdueService.GetAll();
                var overduePayables = allPayables.Where(p => p.DaysOverdue > 0).ToList();

                if (!overduePayables.Any())
                {
                    TempData["Warning"] = "No overdue payables found to send reminders.";
                    return RedirectToAction(nameof(Index));
                }

                int remindersSent = 0;
                foreach (var payable in overduePayables)
                {
                    // Log each reminder sent
                    _logger.LogInformation($"Bulk reminder sent for payable ID: {payable.Id}, Supplier: {payable.SupplierName}, Amount: {payable.BalancePayable}, Days Overdue: {payable.DaysOverdue}");
                    remindersSent++;
                }

                TempData["Success"] = $"Successfully sent {remindersSent} payment reminder(s) to overdue suppliers!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending bulk payment reminders");
                TempData["Error"] = "Error sending bulk reminders. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
