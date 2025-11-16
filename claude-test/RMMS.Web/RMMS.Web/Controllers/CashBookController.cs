using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class CashBookController : Controller
    {
        private readonly ILogger<CashBookController> _logger;
        private readonly ICashBookService _cashBookService;

        public CashBookController(
            ILogger<CashBookController> logger,
            ICashBookService cashBookService)
        {
            _logger = logger;
            _cashBookService = cashBookService;
        }

        public IActionResult Index()
        {
            try
            {
                var model = _cashBookService.GetAll();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving cash book entries");
                TempData["Error"] = "Error loading cash book entries";
                return View(new List<CashBook>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var entry = _cashBookService.GetById(id);
                if (entry == null)
                {
                    TempData["Error"] = "Cash book entry not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(entry);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving cash book entry details");
                TempData["Error"] = "Error loading entry details";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            return View(new CashBook { TransactionDate = DateTime.Today });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(CashBook model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    _cashBookService.Create(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Cash book entry created successfully");
                    TempData["Success"] = "Cash transaction recorded successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating cash book entry");
                TempData["Error"] = "Error creating cash book entry. Please try again.";
                return View(model);
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var entry = _cashBookService.GetById(id);
                if (entry == null)
                {
                    TempData["Error"] = "Cash book entry not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(entry);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving cash book entry for editing");
                TempData["Error"] = "Error loading entry for editing";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, CashBook model)
        {
            try
            {
                if (id != model.Id)
                {
                    TempData["Error"] = "Invalid entry ID";
                    return RedirectToAction(nameof(Index));
                }

                if (ModelState.IsValid)
                {
                    _cashBookService.Update(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Cash book entry updated successfully");
                    TempData["Success"] = "Cash transaction updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating cash book entry");
                TempData["Error"] = "Error updating cash book entry. Please try again.";
                return View(model);
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                var entry = _cashBookService.GetById(id);
                if (entry == null)
                {
                    TempData["Error"] = "Cash book entry not found";
                    return RedirectToAction(nameof(Index));
                }

                _cashBookService.Delete(id, User.Identity?.Name ?? "System");
                _logger.LogInformation("Cash book entry deleted successfully");
                TempData["Success"] = "Cash transaction deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting cash book entry");
                TempData["Error"] = "Error deleting cash book entry. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}