using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;
using System;

namespace RMMS.Web.Controllers
{
    public class ByProductSalesController : Controller
    {
        private readonly IByProductSalesService _service;
        private readonly ILogger<ByProductSalesController> _logger;

        public ByProductSalesController(IByProductSalesService service, ILogger<ByProductSalesController> logger)
        {
            _service = service;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var sales = _service.GetAllSales();
                return View(sales);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading by-product sales");
                TempData["Error"] = "Unable to load sales records.";
                return View(new List<ByProductSales>());
            }
        }

        public IActionResult Create()
        {
            var model = new ByProductSales
            {
                SaleDate = DateTime.Today,
                PaymentMode = "Cash"  // Set a default
            };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(ByProductSales model)
        {
            if (ModelState.IsValid)
            {
                try
                {
                    string username = User.Identity?.Name ?? "System";

                    // CreateSale returns an int (the new ID)
                    int newId = _service.CreateSale(model, username);

                    if (newId > 0)
                    {
                        TempData["Success"] = $"By-product sale recorded successfully with ID: {newId}";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to create sale record.");
                    }
                }
                catch (ArgumentException ex)
                {
                    // These are validation errors from the service
                    ModelState.AddModelError("", ex.Message);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating by-product sale");
                    ModelState.AddModelError("", "An unexpected error occurred. Please try again.");
                }
            }

            return View(model);
        }

        public IActionResult Details(int id)
        {
            try
            {
                var sale = _service.GetSaleById(id);
                if (sale == null)
                {
                    TempData["Error"] = "Sale record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading sale details with ID {id}");
                TempData["Error"] = "Unable to load sale record.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var sale = _service.GetSaleById(id);
                if (sale == null)
                {
                    TempData["Error"] = "Sale record not found.";
                    return RedirectToAction(nameof(Index));
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading sale with ID {id}");
                TempData["Error"] = "Unable to load sale record.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, ByProductSales model)
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

                    // UpdateSale returns a bool
                    bool success = _service.UpdateSale(model, username);

                    if (success)
                    {
                        TempData["Success"] = "By-product sale updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to update sale record.");
                    }
                }
                catch (ArgumentException ex)
                {
                    ModelState.AddModelError("", ex.Message);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error updating sale with ID {id}");
                    ModelState.AddModelError("", "An unexpected error occurred.");
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

                // DeleteSale returns a bool
                bool success = _service.DeleteSale(id, username);

                if (success)
                {
                    TempData["Success"] = "Sale record deleted successfully.";
                }
                else
                {
                    TempData["Error"] = "Unable to delete sale record.";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting sale with ID {id}");
                TempData["Error"] = "An error occurred while deleting.";
            }

            return RedirectToAction(nameof(Index));
        }
    }
}