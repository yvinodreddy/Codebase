using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class InventoryController : Controller
    {
        private readonly IInventoryLedgerService _inventoryService;
        private readonly IProductService _productService;
        private readonly IWarehouseService _warehouseService;
        private readonly ILogger<InventoryController> _logger;

        public InventoryController(
            IInventoryLedgerService inventoryService,
            IProductService productService,
            IWarehouseService warehouseService,
            ILogger<InventoryController> logger)
        {
            _inventoryService = inventoryService;
            _productService = productService;
            _warehouseService = warehouseService;
            _logger = logger;
        }

        // GET: Inventory
        public IActionResult Index(string searchTerm, int? warehouseId, string filter, int page = 1, string sortBy = "ProductName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;
                List<InventoryLedger> inventory;

                // Apply filters
                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    inventory = _inventoryService.SearchInventory(searchTerm);
                }
                else if (warehouseId.HasValue)
                {
                    inventory = _inventoryService.GetInventoryByWarehouse(warehouseId.Value);
                }
                else if (!string.IsNullOrWhiteSpace(filter))
                {
                    inventory = filter.ToLower() switch
                    {
                        "low" => _inventoryService.GetLowStockItems(),
                        "over" => _inventoryService.GetOverStockItems(),
                        "reorder" => _inventoryService.GetReorderItems(),
                        _ => _inventoryService.GetAllInventory()
                    };
                }
                else
                {
                    inventory = _inventoryService.GetAllInventory();
                }

                // Apply sorting and pagination
                var inventoryQuery = inventory.AsQueryable().OrderByDynamic(sortBy, sortOrder);
                var pagedResult = PagedResult<InventoryLedger>.Create(inventoryQuery, page, pageSize, sortBy, sortOrder);

                // Get warehouses for dropdown
                var warehouses = _warehouseService.GetAllWarehouses();
                ViewBag.Warehouses = new SelectList(warehouses, "Id", "WarehouseName", warehouseId);
                ViewBag.SearchTerm = searchTerm;
                ViewBag.WarehouseId = warehouseId;
                ViewBag.Filter = filter;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                // Calculate totals
                ViewBag.TotalValue = inventory.Sum(i => i.TotalValue);
                ViewBag.LowStockCount = inventory.Count(i => i.IsLowStock);
                ViewBag.ReorderCount = inventory.Count(i => i.NeedsReorder);

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading inventory");
                TempData["Error"] = "Error loading inventory: " + ex.Message;
                return View(new PagedResult<InventoryLedger>());
            }
        }

        // GET: Inventory/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var inventory = _inventoryService.GetInventoryById(id);
                if (inventory == null)
                    return NotFound();

                return View(inventory);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading inventory {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Inventory/Create
        public IActionResult Create()
        {
            try
            {
                LoadDropdownData();
                var ledger = new InventoryLedger
                {
                    CurrentStock = 0,
                    MinimumLevel = 0,
                    MaximumLevel = 0,
                    ReorderLevel = 0,
                    UnitCost = 0
                };
                return View(ledger);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create form");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inventory/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(InventoryLedger ledger)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    // Check if ledger entry already exists for this product/warehouse/zone combination
                    var existing = _inventoryService.GetInventoryByProductAndWarehouse(
                        ledger.ProductId,
                        ledger.WarehouseId,
                        ledger.ZoneId);

                    if (existing != null)
                    {
                        ModelState.AddModelError("", "Inventory ledger entry already exists for this product/warehouse/zone combination.");
                        LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                        return View(ledger);
                    }

                    var username = User.Identity?.Name ?? "System";
                    var ledgerId = _inventoryService.CreateInventory(ledger, username);
                    TempData["Success"] = "Inventory ledger entry created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                return View(ledger);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating inventory ledger");
                ModelState.AddModelError("", "Error creating inventory: " + ex.Message);
                LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                return View(ledger);
            }
        }

        // GET: Inventory/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var ledger = _inventoryService.GetInventoryById(id);
                if (ledger == null)
                    return NotFound();

                LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                return View(ledger);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading inventory {id} for editing");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inventory/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, InventoryLedger ledger)
        {
            if (id != ledger.Id)
                return NotFound();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var success = _inventoryService.UpdateInventory(ledger, username);
                    if (success)
                    {
                        TempData["Success"] = "Inventory updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to update inventory");
                    }
                }
                LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                return View(ledger);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating inventory {id}");
                ModelState.AddModelError("", "Error updating inventory: " + ex.Message);
                LoadDropdownData(ledger.ProductId, ledger.WarehouseId);
                return View(ledger);
            }
        }

        // GET: Inventory/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var ledger = _inventoryService.GetInventoryById(id);
                if (ledger == null)
                    return NotFound();

                return View(ledger);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading inventory {id} for deletion");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inventory/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _inventoryService.DeleteInventory(id, username);
                if (success)
                {
                    TempData["Success"] = "Inventory entry deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete inventory entry";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting inventory {id}");
                TempData["Error"] = "Error deleting inventory: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // Helper method to load dropdown data
        private void LoadDropdownData(int? selectedProductId = null, int? selectedWarehouseId = null)
        {
            var products = _productService.GetAllProducts();
            var warehouses = _warehouseService.GetAllWarehouses();

            ViewBag.Products = new SelectList(products, "Id", "ProductName", selectedProductId);
            ViewBag.Warehouses = new SelectList(warehouses, "Id", "WarehouseName", selectedWarehouseId);
        }
    }
}
