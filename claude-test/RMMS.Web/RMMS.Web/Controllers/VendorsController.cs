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
    public class VendorsController : Controller
    {
        private readonly IVendorService _vendorService;
        private readonly ILogger<VendorsController> _logger;

        public VendorsController(IVendorService vendorService, ILogger<VendorsController> logger)
        {
            _vendorService = vendorService;
            _logger = logger;
        }

        // GET: Vendors
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "VendorName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                var vendors = string.IsNullOrWhiteSpace(searchTerm)
                    ? _vendorService.GetAllVendors()
                    : _vendorService.SearchVendors(searchTerm);

                // Apply sorting
                var vendorsQuery = vendors.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Vendor>.Create(vendorsQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading vendors");
                TempData["Error"] = "Error loading vendors: " + ex.Message;
                return View(new PagedResult<Vendor>());
            }
        }

        // GET: Vendors/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var vendor = _vendorService.GetVendorById(id);
                if (vendor == null)
                    return NotFound();

                return View(vendor);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading vendor {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Vendors/Create
        public IActionResult Create()
        {
            var vendor = new Vendor
            {
                VendorCode = _vendorService.GenerateVendorCode(),
                Status = "Active"
            };
            return View(vendor);
        }

        // POST: Vendors/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Vendor vendor)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var vendorId = _vendorService.CreateVendor(vendor, username);
                    TempData["Success"] = $"Vendor {vendor.VendorName} created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(vendor);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating vendor");
                ModelState.AddModelError("", "Error creating vendor: " + ex.Message);
                return View(vendor);
            }
        }

        // GET: Vendors/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var vendor = _vendorService.GetVendorById(id);
                if (vendor == null)
                    return NotFound();

                return View(vendor);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading vendor {id} for edit");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Vendors/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Vendor vendor)
        {
            if (id != vendor.Id)
                return BadRequest();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var result = _vendorService.UpdateVendor(vendor, username);
                    if (result)
                    {
                        TempData["Success"] = "Vendor updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    ModelState.AddModelError("", "Failed to update vendor");
                }
                return View(vendor);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating vendor {id}");
                ModelState.AddModelError("", "Error updating vendor: " + ex.Message);
                return View(vendor);
            }
        }

        // GET: Vendors/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var vendor = _vendorService.GetVendorById(id);
                if (vendor == null)
                    return NotFound();

                return View(vendor);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading vendor {id} for delete");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Vendors/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var result = _vendorService.DeleteVendor(id, username);
                if (result)
                    TempData["Success"] = "Vendor deleted successfully!";
                else
                    TempData["Error"] = "Failed to delete vendor";

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting vendor {id}");
                TempData["Error"] = "Error deleting vendor: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
