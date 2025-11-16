using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class ExternalRiceSalesController : Controller
    {
        private readonly IExternalRiceSaleService _service;
        private readonly ILogger<ExternalRiceSalesController> _logger;

        public ExternalRiceSalesController(IExternalRiceSaleService service, ILogger<ExternalRiceSalesController> logger)
        {
            _service = service;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var sales = _service.GetAll();
                return View(sales);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading external rice sales");
                return View(new List<ExternalRiceSale>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var sale = _service.GetById(id);
                if (sale == null)
                {
                    TempData["Error"] = "Sale record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading sale with ID {id}");
                TempData["Error"] = "Unable to load sale record";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            var model = new ExternalRiceSale { Date = DateTime.Today };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(ExternalRiceSale model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Create(model, username);
                    TempData["Success"] = "External rice sale created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating external rice sale");
                TempData["Error"] = "An error occurred while creating the sale";
                return View(model);
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var sale = _service.GetById(id);
                if (sale == null)
                {
                    TempData["Error"] = "Sale record not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading sale with ID {id}");
                TempData["Error"] = "Unable to load sale record";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(ExternalRiceSale model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Update(model, username);
                    TempData["Success"] = "External rice sale updated successfully!";
                    return RedirectToAction(nameof(Details), new { id = model.Id });
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating sale with ID {model.Id}");
                TempData["Error"] = "An error occurred while updating the sale";
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
                _service.Delete(id, username);
                TempData["Success"] = "External rice sale deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting sale with ID {id}");
                TempData["Error"] = "An error occurred while deleting the sale";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
