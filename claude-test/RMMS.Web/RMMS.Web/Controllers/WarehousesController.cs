using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class WarehousesController : Controller
    {
        private readonly IWarehouseService _warehouseService;
        private readonly ILogger<WarehousesController> _logger;

        public WarehousesController(IWarehouseService warehouseService, ILogger<WarehousesController> logger)
        {
            _warehouseService = warehouseService;
            _logger = logger;
        }

        // GET: Warehouses
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "WarehouseName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                var warehouses = string.IsNullOrWhiteSpace(searchTerm)
                    ? _warehouseService.GetAllWarehouses()
                    : _warehouseService.SearchWarehouses(searchTerm);

                // Apply sorting
                var warehousesQuery = warehouses.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Warehouse>.Create(warehousesQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading warehouses");
                TempData["Error"] = "Error loading warehouses: " + ex.Message;
                return View(new PagedResult<Warehouse>());
            }
        }

        // GET: Warehouses/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var warehouse = _warehouseService.GetWarehouseById(id);
                if (warehouse == null)
                    return NotFound();

                return View(warehouse);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading warehouse {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Warehouses/Create
        public IActionResult Create()
        {
            var warehouse = new Warehouse
            {
                WarehouseCode = _warehouseService.GenerateWarehouseCode(),
                Status = "Active",
                IsTemperatureControlled = false
            };
            return View(warehouse);
        }

        // POST: Warehouses/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Warehouse warehouse)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var warehouseId = _warehouseService.CreateWarehouse(warehouse, username);
                    TempData["Success"] = $"Warehouse {warehouse.WarehouseName} created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(warehouse);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating warehouse");
                ModelState.AddModelError("", "Error creating warehouse: " + ex.Message);
                return View(warehouse);
            }
        }

        // GET: Warehouses/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var warehouse = _warehouseService.GetWarehouseById(id);
                if (warehouse == null)
                    return NotFound();

                return View(warehouse);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading warehouse {id} for editing");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Warehouses/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Warehouse warehouse)
        {
            if (id != warehouse.Id)
                return NotFound();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var success = _warehouseService.UpdateWarehouse(warehouse, username);
                    if (success)
                    {
                        TempData["Success"] = $"Warehouse {warehouse.WarehouseName} updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to update warehouse");
                    }
                }
                return View(warehouse);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating warehouse {id}");
                ModelState.AddModelError("", "Error updating warehouse: " + ex.Message);
                return View(warehouse);
            }
        }

        // GET: Warehouses/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var warehouse = _warehouseService.GetWarehouseById(id);
                if (warehouse == null)
                    return NotFound();

                return View(warehouse);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading warehouse {id} for deletion");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Warehouses/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var warehouse = _warehouseService.GetWarehouseById(id);
                if (warehouse == null)
                    return NotFound();

                var username = User.Identity?.Name ?? "System";
                var success = _warehouseService.DeleteWarehouse(id, username);
                if (success)
                {
                    TempData["Success"] = $"Warehouse {warehouse.WarehouseName} deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete warehouse";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting warehouse {id}");
                TempData["Error"] = "Error deleting warehouse: " + ex.Message;
            }

            return RedirectToAction(nameof(Index));
        }
    }
}
