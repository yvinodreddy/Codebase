// RMMS.Web/Controllers/PaddyProcurementController.cs
using System;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using RMMS.Models;
using RMMS.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class PaddyProcurementController : Controller
    {
        private readonly IPaddyProcurementService _service;
        private readonly ILogger<PaddyProcurementController> _logger;

        public PaddyProcurementController(IConfiguration configuration, ILogger<PaddyProcurementController> logger)
        {
            _service = new PaddyProcurementService(configuration);
            _logger = logger;
        }

        // GET: PaddyProcurement
        public IActionResult Index(string searchSupplier, string searchVariety, DateTime? startDate, DateTime? endDate, string searchVoucher)
        {
            try
            {
                List<PaddyProcurement> procurements;

                // Check if any search criteria is provided
                bool hasSearchCriteria = !string.IsNullOrEmpty(searchSupplier) ||
                                        !string.IsNullOrEmpty(searchVariety) ||
                                        startDate.HasValue ||
                                        endDate.HasValue ||
                                        !string.IsNullOrEmpty(searchVoucher);

                if (hasSearchCriteria)
                {
                    // Perform search with the provided criteria
                    procurements = _service.SearchProcurements(
                        searchSupplier,
                        searchVariety,
                        startDate,
                        endDate,
                        searchVoucher
                    );
                }
                else
                {
                    // No search criteria - get all active procurements
                    procurements = _service.GetAllProcurements(true);
                }

                // Store search values in ViewBag to maintain them in the form
                ViewBag.SearchSupplier = searchSupplier;
                ViewBag.SearchVariety = searchVariety;
                ViewBag.StartDate = startDate;
                ViewBag.EndDate = endDate;
                ViewBag.SearchVoucher = searchVoucher;

                // Get varieties for dropdown
                ViewBag.PaddyVarieties = GetPaddyVarieties();

                return View(procurements);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in PaddyProcurement Index");
                TempData["Error"] = "Error loading procurement records: " + ex.Message;
                return View(new List<PaddyProcurement>());
            }
        }

        // GET: PaddyProcurement/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var procurement = _service.GetProcurementById(id);
                if (procurement == null)
                {
                    return NotFound();
                }
                return View(procurement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading procurement details for ID {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: PaddyProcurement/Create
        public IActionResult Create()
        {
            var model = new PaddyProcurement
            {
                ReceiptDate = DateTime.Today,
                VoucherNumber = _service.GenerateNewVoucherNumber()
            };

            ViewBag.PaddyVarieties = GetPaddyVarieties();
            return View(model);
        }

        // POST: PaddyProcurement/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(PaddyProcurement model)
        {

            ModelState.Remove("CreatedBy");
            ModelState.Remove("ModifiedBy");
            ModelState.Remove("CreatedDate");
            ModelState.Remove("ModifiedDate");
            ModelState.Remove("IsActive"); 

            if (!ModelState.IsValid)
            {
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }

            try
            {
                string username = User.Identity?.Name ?? "System";
                int newId = _service.CreateProcurement(model, username);

                TempData["Success"] = $"Procurement record created successfully with ID: {newId}";
                return RedirectToAction(nameof(Index));
            }
            catch (ArgumentException ex)
            {
                ModelState.AddModelError("", ex.Message);
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating procurement record");
                ModelState.AddModelError("", "An error occurred while saving the record.");
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }
        }

        // GET: PaddyProcurement/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var procurement = _service.GetProcurementById(id);
                if (procurement == null)
                {
                    return NotFound();
                }

                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(procurement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading procurement for edit, ID {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: PaddyProcurement/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, PaddyProcurement model)
        {
            if (id != model.Id)
            {
                return BadRequest();
            }

            if (!ModelState.IsValid)
            {
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }

            try
            {
                string username = User.Identity?.Name ?? "System";
                bool result = _service.UpdateProcurement(model, username);

                if (result)
                {
                    TempData["Success"] = "Procurement record updated successfully.";
                    return RedirectToAction(nameof(Index));
                }
                else
                {
                    TempData["Error"] = "Failed to update the record.";
                    return RedirectToAction(nameof(Index));
                }
            }
            catch (ArgumentException ex)
            {
                ModelState.AddModelError("", ex.Message);
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating procurement record ID {id}");
                ModelState.AddModelError("", "An error occurred while updating the record.");
                ViewBag.PaddyVarieties = GetPaddyVarieties();
                return View(model);
            }
        }

        // GET: PaddyProcurement/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var procurement = _service.GetProcurementById(id);
                if (procurement == null)
                {
                    return NotFound();
                }
                return View(procurement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading procurement for deletion, ID {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: PaddyProcurement/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                string username = User.Identity?.Name ?? "System";
                bool result = _service.DeleteProcurement(id, username);

                if (result)
                {
                    TempData["Success"] = "Procurement record deleted successfully.";
                }
                else
                {
                    TempData["Error"] = "Failed to delete the record.";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting procurement record ID {id}");
                TempData["Error"] = "An error occurred while deleting the record.";
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: PaddyProcurement/StockSummary
        public IActionResult StockSummary()
        {
            try
            {
                // Get all procurement records for stock summary (view expects List<PaddyProcurement>)
                var procurementRecords = _service.GetAllProcurements(true);
                return View(procurementRecords);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating stock summary");
                TempData["Error"] = "An error occurred while generating the summary.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public IActionResult Search(string supplierName, string variety, DateTime? startDate, DateTime? endDate, string voucherNumber)
        {
            try
            {
                var results = _service.SearchProcurements(supplierName, variety, startDate, endDate, voucherNumber);
                return PartialView("_ProcurementTable", results);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error searching procurement records");
                return Json(new { success = false, message = "Error searching records: " + ex.Message });
            }
        }

        // GET: Quick search for AJAX autocomplete
        [HttpGet]
        public IActionResult QuickSearch(string term)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(term))
                {
                    return Json(new List<PaddyProcurement>());
                }

                var results = _service.GetAllProcurements(true)
                    .Where(p =>
                        (p.SupplierName != null && p.SupplierName.Contains(term, StringComparison.OrdinalIgnoreCase)) ||
                        (p.VoucherNumber != null && p.VoucherNumber.Contains(term, StringComparison.OrdinalIgnoreCase)) ||
                        (p.PaddyVariety != null && p.PaddyVariety.Contains(term, StringComparison.OrdinalIgnoreCase)))
                    .Take(10)
                    .Select(p => new {
                        p.Id,
                        p.VoucherNumber,
                        p.SupplierName,
                        p.PaddyVariety,
                        p.ReceiptDate
                    });

                return Json(results);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in quick search");
                return Json(new { success = false, message = ex.Message });
            }
        }

        // Helper method to get paddy varieties for dropdown
        private List<string> GetPaddyVarieties()
        {
            return new List<string>
            {
                "Basmati",
                "Sonam",
                "Mansuri",
                "Katrni",
                "Sona Masoori",
                "IR-36",
                "IR-64",
                "Other"
            };
        }
    }
}