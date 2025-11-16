using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class BankTransactionsController : Controller
    {
        private readonly ILogger<BankTransactionsController> _logger;
        private readonly IBankTransactionService _bankTransactionService;

        public BankTransactionsController(
            ILogger<BankTransactionsController> logger,
            IBankTransactionService bankTransactionService)
        {
            _logger = logger;
            _bankTransactionService = bankTransactionService;
        }

        public IActionResult Index()
        {
            try
            {
                var model = _bankTransactionService.GetAll();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank transactions");
                TempData["Error"] = "Error loading bank transactions";
                return View(new List<BankTransaction>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var transaction = _bankTransactionService.GetById(id);
                if (transaction == null)
                {
                    TempData["Error"] = "Bank transaction not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(transaction);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank transaction details");
                TempData["Error"] = "Error loading transaction details";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            return View(new BankTransaction { TransactionDate = DateTime.Today });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(BankTransaction model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    _bankTransactionService.Create(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Bank transaction created successfully");
                    TempData["Success"] = "Bank transaction recorded successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating bank transaction");
                TempData["Error"] = "Error creating bank transaction. Please try again.";
                return View(model);
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var transaction = _bankTransactionService.GetById(id);
                if (transaction == null)
                {
                    TempData["Error"] = "Bank transaction not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(transaction);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank transaction for editing");
                TempData["Error"] = "Error loading transaction for editing";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, BankTransaction model)
        {
            try
            {
                if (id != model.Id)
                {
                    TempData["Error"] = "Invalid transaction ID";
                    return RedirectToAction(nameof(Index));
                }

                if (ModelState.IsValid)
                {
                    _bankTransactionService.Update(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Bank transaction updated successfully");
                    TempData["Success"] = "Bank transaction updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating bank transaction");
                TempData["Error"] = "Error updating bank transaction. Please try again.";
                return View(model);
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                var transaction = _bankTransactionService.GetById(id);
                if (transaction == null)
                {
                    TempData["Error"] = "Bank transaction not found";
                    return RedirectToAction(nameof(Index));
                }

                _bankTransactionService.Delete(id, User.Identity?.Name ?? "System");
                _logger.LogInformation("Bank transaction deleted successfully");
                TempData["Success"] = "Bank transaction deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting bank transaction");
                TempData["Error"] = "Error deleting bank transaction. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}