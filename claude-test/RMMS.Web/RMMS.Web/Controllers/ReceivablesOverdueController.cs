using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class ReceivablesOverdueController : Controller
    {
        private readonly IReceivableOverdueService _service;
        private readonly ILogger<ReceivablesOverdueController> _logger;

        public ReceivablesOverdueController(IReceivableOverdueService service, ILogger<ReceivablesOverdueController> logger)
        {
            _service = service;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var receivables = _service.GetAll();
                return View(receivables);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading receivables");
                return View(new List<ReceivableOverdue>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var receivable = _service.GetById(id);
                if (receivable == null)
                {
                    TempData["Error"] = "Receivable record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(receivable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading receivable with ID {id}");
                TempData["Error"] = "Unable to load receivable record.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            var model = new ReceivableOverdue
            {
                InvoiceDate = DateTime.Today,
                DueDate = DateTime.Today.AddDays(30)
            };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(ReceivableOverdue model)
        {
            if (ModelState.IsValid)
            {
                try
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Create(model, username);
                    TempData["Success"] = "Receivable record created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating receivable");
                    ModelState.AddModelError("", "An error occurred while creating the record.");
                }
            }
            return View(model);
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var receivable = _service.GetById(id);
                if (receivable == null)
                {
                    TempData["Error"] = "Receivable record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(receivable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading receivable with ID {id}");
                TempData["Error"] = "Unable to load receivable record.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, ReceivableOverdue model)
        {
            if (id != model.Id)
            {
                return BadRequest();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Update(model, username);
                    TempData["Success"] = "Receivable record updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error updating receivable with ID {id}");
                    ModelState.AddModelError("", "An error occurred while updating the record.");
                }
            }
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                _service.Delete(id, username);
                TempData["Success"] = "Receivable record deleted successfully.";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting receivable with ID {id}");
                TempData["Error"] = "An error occurred while deleting.";
            }
            return RedirectToAction(nameof(Index));
        }

        // Support both GET and POST for SendReminder (removed [HttpPost] restriction)
        public IActionResult SendReminder(int id)
        {
            try
            {
                var receivable = _service.GetById(id);
                if (receivable == null)
                {
                    TempData["Error"] = "Receivable record not found";
                    return RedirectToAction(nameof(Index));
                }

                // Log the reminder action
                _logger.LogInformation($"Payment reminder sent for receivable ID: {id}, Customer: {receivable.CustomerName}, Amount: {receivable.BalanceDue}");

                TempData["Success"] = $"Payment reminder sent successfully to {receivable.CustomerName}!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending payment reminder");
                TempData["Error"] = "Error sending payment reminder. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult RecordPayment(int id)
        {
            try
            {
                var receivable = _service.GetById(id);
                if (receivable == null)
                {
                    TempData["Error"] = "Receivable record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(receivable);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading receivable with ID {id}");
                TempData["Error"] = "Unable to load receivable record";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult RecordPayment(int id, decimal receiptAmount)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                _service.RecordReceipt(id, receiptAmount, username);
                TempData["Success"] = "Payment recorded successfully!";
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error recording payment for receivable ID {id}");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult SendBulkReminders()
        {
            try
            {
                var allReceivables = _service.GetAll();
                var overdueReceivables = allReceivables.Where(r => r.DaysOverdue > 0).ToList();

                if (!overdueReceivables.Any())
                {
                    TempData["Warning"] = "No overdue receivables found to send reminders.";
                    return RedirectToAction(nameof(Index));
                }

                int remindersSent = 0;
                foreach (var receivable in overdueReceivables)
                {
                    // Log each reminder sent
                    _logger.LogInformation($"Bulk reminder sent for receivable ID: {receivable.Id}, Customer: {receivable.CustomerName}, Amount: {receivable.BalanceDue}, Days Overdue: {receivable.DaysOverdue}");
                    remindersSent++;
                }

                TempData["Success"] = $"Successfully sent {remindersSent} payment reminder(s) to overdue customers!";
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
