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
    public class StockMovementsController : Controller
    {
        private readonly IStockMovementService _movementService;
        private readonly IProductService _productService;
        private readonly IWarehouseService _warehouseService;
        private readonly ILogger<StockMovementsController> _logger;

        public StockMovementsController(
            IStockMovementService movementService,
            IProductService productService,
            IWarehouseService warehouseService,
            ILogger<StockMovementsController> logger)
        {
            _movementService = movementService;
            _productService = productService;
            _warehouseService = warehouseService;
            _logger = logger;
        }

        // GET: StockMovements
        public IActionResult Index(string searchTerm, string movementType, int page = 1, string sortBy = "MovementDate", string sortOrder = "desc")
        {
            try
            {
                const int pageSize = 16;
                List<StockMovement> movements;

                // Apply filters
                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    movements = _movementService.SearchMovements(searchTerm);
                }
                else if (!string.IsNullOrWhiteSpace(movementType))
                {
                    movements = _movementService.GetMovementsByType(movementType);
                }
                else
                {
                    movements = _movementService.GetAllMovements();
                }

                // Apply server-side sorting and paging
                var movementsQuery = movements.AsQueryable().OrderByDynamic(sortBy, sortOrder);
                var pagedResult = PagedResult<StockMovement>.Create(movementsQuery, page, pageSize, sortBy, sortOrder);

                // Get warehouses for dropdown
                var warehouses = _warehouseService.GetAllWarehouses();
                ViewBag.Warehouses = new SelectList(warehouses, "Id", "WarehouseName");
                ViewBag.SearchTerm = searchTerm;
                ViewBag.MovementType = movementType;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                // Calculate statistics
                ViewBag.TotalMovements = movements.Count;
                ViewBag.InMovements = movements.Count(m => m.MovementType == "IN");
                ViewBag.OutMovements = movements.Count(m => m.MovementType == "OUT");
                ViewBag.TotalValue = movements.Sum(m => m.TotalCost);

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading stock movements");
                TempData["Error"] = "Error loading stock movements: " + ex.Message;
                return View(new PagedResult<StockMovement>());
            }
        }

        // GET: StockMovements/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var movement = _movementService.GetMovementById(id);
                if (movement == null)
                    return NotFound();

                return View(movement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock movement {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: StockMovements/Create
        public IActionResult Create(string type = "IN")
        {
            try
            {
                LoadDropdownData();

                var movement = new StockMovement
                {
                    MovementCode = _movementService.GenerateMovementCode(),
                    MovementType = type,
                    MovementDate = DateTime.Now,
                    MovementCategory = type == "IN" ? "Procurement" : "Sales",
                    Quantity = 0,
                    UnitCost = 0,
                    IsApproved = true
                };

                ViewBag.MovementType = type;
                return View(movement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create form");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockMovements/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(StockMovement movement)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    // Validate movement
                    var validation = _movementService.ValidateMovement(movement);
                    if (!validation.success)
                    {
                        ModelState.AddModelError("", validation.message);
                        LoadDropdownData(movement.ProductId, movement.WarehouseId);
                        ViewBag.MovementType = movement.MovementType;
                        return View(movement);
                    }

                    var username = User.Identity?.Name ?? "System";
                    var movementId = _movementService.CreateMovement(movement, username);

                    TempData["Success"] = $"Stock movement {movement.MovementCode} created successfully! Inventory ledger updated.";
                    return RedirectToAction(nameof(Index));
                }

                LoadDropdownData(movement.ProductId, movement.WarehouseId);
                ViewBag.MovementType = movement.MovementType;
                return View(movement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating stock movement");
                ModelState.AddModelError("", "Error creating stock movement: " + ex.Message);
                LoadDropdownData(movement.ProductId, movement.WarehouseId);
                ViewBag.MovementType = movement.MovementType;
                return View(movement);
            }
        }

        // GET: StockMovements/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var movement = _movementService.GetMovementById(id);
                if (movement == null)
                    return NotFound();

                return View(movement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock movement {id} for deletion");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockMovements/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _movementService.DeleteMovement(id, username);
                if (success)
                {
                    TempData["Success"] = "Stock movement deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete stock movement";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting stock movement {id}");
                TempData["Error"] = "Error deleting stock movement: " + ex.Message;
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

            // Movement types
            ViewBag.MovementTypes = new List<SelectListItem>
            {
                new SelectListItem { Value = "IN", Text = "Stock IN (Receive)" },
                new SelectListItem { Value = "OUT", Text = "Stock OUT (Issue)" }
            };

            // Movement categories
            ViewBag.MovementCategories = new List<SelectListItem>
            {
                new SelectListItem { Value = "Procurement", Text = "Procurement" },
                new SelectListItem { Value = "Sales", Text = "Sales" },
                new SelectListItem { Value = "Production", Text = "Production" },
                new SelectListItem { Value = "Transfer", Text = "Transfer" },
                new SelectListItem { Value = "Adjustment", Text = "Adjustment" },
                new SelectListItem { Value = "Return", Text = "Return" }
            };
        }
    }
}
