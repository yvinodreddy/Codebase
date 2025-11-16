using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class LoansAdvancesController : Controller
    {
        private readonly ILoansAdvancesService _service;
        private readonly ILogger<LoansAdvancesController> _logger;

        public LoansAdvancesController(ILoansAdvancesService service, ILogger<LoansAdvancesController> logger)
        {
            _service = service;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var loans = _service.GetAll();
                return View(loans);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading loans and advances");
                return View(new List<LoanAdvance>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var loan = _service.GetById(id);
                if (loan == null)
                {
                    TempData["Error"] = "Loan/Advance record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(loan);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading loan with ID {id}");
                TempData["Error"] = "Unable to load loan/advance record.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            var model = new LoanAdvance
            {
                Date = DateTime.Today
            };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(LoanAdvance model)
        {
            if (ModelState.IsValid)
            {
                try
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Create(model, username);
                    TempData["Success"] = "Loan/Advance record created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating loan/advance");
                    ModelState.AddModelError("", "An error occurred while creating the record.");
                }
            }
            return View(model);
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var loan = _service.GetById(id);
                if (loan == null)
                {
                    TempData["Error"] = "Loan/Advance record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(loan);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading loan with ID {id}");
                TempData["Error"] = "Unable to load loan/advance record.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, LoanAdvance model)
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
                    TempData["Success"] = "Loan/Advance record updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error updating loan with ID {id}");
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
                TempData["Success"] = "Loan/Advance record deleted successfully.";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting loan with ID {id}");
                TempData["Error"] = "An error occurred while deleting.";
            }
            return RedirectToAction(nameof(Index));
        }

        public IActionResult RecordRepayment(int id)
        {
            try
            {
                var loan = _service.GetById(id);
                if (loan == null)
                {
                    TempData["Error"] = "Loan/Advance record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(loan);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading loan with ID {id}");
                TempData["Error"] = "Unable to load loan/advance record.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult RecordRepayment(int id, decimal repaymentAmount, DateTime repaymentDate)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                _service.RecordRepayment(id, repaymentAmount, repaymentDate, username);
                TempData["Success"] = "Repayment recorded successfully!";
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error recording repayment for loan ID {id}");
                TempData["Error"] = "An error occurred while recording repayment.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
