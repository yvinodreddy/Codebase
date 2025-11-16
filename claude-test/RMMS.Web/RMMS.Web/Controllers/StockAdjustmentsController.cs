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
    public class StockAdjustmentsController : Controller
    {
        private readonly IStockAdjustmentService _adjustmentService;
        private readonly IProductService _productService;
        private readonly IWarehouseService _warehouseService;
        private readonly ILogger<StockAdjustmentsController> _logger;

        public StockAdjustmentsController(
            IStockAdjustmentService adjustmentService,
            IProductService productService,
            IWarehouseService warehouseService,
            ILogger<StockAdjustmentsController> logger)
        {
            _adjustmentService = adjustmentService;
            _productService = productService;
            _warehouseService = warehouseService;
            _logger = logger;
        }

        // GET: StockAdjustments
        public IActionResult Index(string searchTerm, string approvalStatus, int page = 1, string sortBy = "AdjustmentDate", string sortOrder = "desc")
        {
            try
            {
                const int pageSize = 16;
                List<StockAdjustment> adjustments;

                // Apply filters
                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    adjustments = _adjustmentService.SearchAdjustments(searchTerm);
                }
                else if (approvalStatus == "Pending")
                {
                    adjustments = _adjustmentService.GetPendingApprovals();
                }
                else if (approvalStatus == "Approved")
                {
                    adjustments = _adjustmentService.GetApprovedAdjustments();
                }
                else if (approvalStatus == "Rejected")
                {
                    adjustments = _adjustmentService.GetRejectedAdjustments();
                }
                else
                {
                    adjustments = _adjustmentService.GetAllAdjustments();
                }

                // Apply sorting and paging
                var adjustmentsQuery = adjustments.AsQueryable().OrderByDynamic(sortBy, sortOrder);
                var pagedResult = PagedResult<StockAdjustment>.Create(adjustmentsQuery, page, pageSize, sortBy, sortOrder);

                // Get warehouses for dropdown
                var warehouses = _warehouseService.GetAllWarehouses();
                ViewBag.Warehouses = new SelectList(warehouses, "Id", "WarehouseName");
                ViewBag.SearchTerm = searchTerm;
                ViewBag.ApprovalStatus = approvalStatus;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                // Calculate statistics
                ViewBag.TotalAdjustments = adjustments.Count;
                ViewBag.PendingCount = adjustments.Count(a => a.RequiresApproval && !a.IsApproved && !a.IsRejected);
                ViewBag.ApprovedCount = adjustments.Count(a => a.IsApproved);
                ViewBag.RejectedCount = adjustments.Count(a => a.IsRejected);
                ViewBag.IncreaseCount = adjustments.Count(a => a.AdjustmentType == "Increase");
                ViewBag.DecreaseCount = adjustments.Count(a => a.AdjustmentType == "Decrease");

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading stock adjustments");
                TempData["Error"] = "Error loading stock adjustments: " + ex.Message;
                return View(new PagedResult<StockAdjustment>());
            }
        }

        // GET: StockAdjustments/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var adjustment = _adjustmentService.GetAdjustmentById(id);
                if (adjustment == null)
                    return NotFound();

                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock adjustment {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: StockAdjustments/Create
        public IActionResult Create(string type = "Increase")
        {
            try
            {
                LoadDropdownData();

                var adjustment = new StockAdjustment
                {
                    AdjustmentCode = _adjustmentService.GenerateAdjustmentCode(),
                    AdjustmentType = type,
                    AdjustmentDate = DateTime.Now,
                    Quantity = 0,
                    RequiresApproval = true,
                    IsApproved = false
                };

                ViewBag.AdjustmentType = type;
                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create form");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockAdjustments/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(StockAdjustment adjustment)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var adjustmentId = _adjustmentService.CreateAdjustment(adjustment, username);

                    if (adjustment.RequiresApproval)
                    {
                        TempData["Success"] = $"Stock adjustment {adjustment.AdjustmentCode} created successfully! Pending approval.";
                    }
                    else
                    {
                        TempData["Success"] = $"Stock adjustment {adjustment.AdjustmentCode} created and applied successfully!";
                    }

                    return RedirectToAction(nameof(Index));
                }

                LoadDropdownData(adjustment.ProductId, adjustment.WarehouseId);
                ViewBag.AdjustmentType = adjustment.AdjustmentType;
                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating stock adjustment");
                ModelState.AddModelError("", "Error creating stock adjustment: " + ex.Message);
                LoadDropdownData(adjustment.ProductId, adjustment.WarehouseId);
                ViewBag.AdjustmentType = adjustment.AdjustmentType;
                return View(adjustment);
            }
        }

        // GET: StockAdjustments/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var adjustment = _adjustmentService.GetAdjustmentById(id);
                if (adjustment == null)
                    return NotFound();

                // Don't allow editing of approved adjustments
                if (adjustment.IsApproved)
                {
                    TempData["Error"] = "Cannot edit an approved adjustment";
                    return RedirectToAction(nameof(Index));
                }

                LoadDropdownData(adjustment.ProductId, adjustment.WarehouseId);
                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock adjustment {id} for editing");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockAdjustments/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, StockAdjustment adjustment)
        {
            if (id != adjustment.Id)
                return NotFound();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var success = _adjustmentService.UpdateAdjustment(adjustment, username);

                    if (success)
                    {
                        TempData["Success"] = "Stock adjustment updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to update stock adjustment");
                    }
                }

                LoadDropdownData(adjustment.ProductId, adjustment.WarehouseId);
                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating stock adjustment {id}");
                ModelState.AddModelError("", "Error updating stock adjustment: " + ex.Message);
                LoadDropdownData(adjustment.ProductId, adjustment.WarehouseId);
                return View(adjustment);
            }
        }

        // GET: StockAdjustments/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var adjustment = _adjustmentService.GetAdjustmentById(id);
                if (adjustment == null)
                    return NotFound();

                // Don't allow deletion of approved adjustments
                if (adjustment.IsApproved)
                {
                    TempData["Error"] = "Cannot delete an approved adjustment";
                    return RedirectToAction(nameof(Index));
                }

                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock adjustment {id} for deletion");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockAdjustments/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _adjustmentService.DeleteAdjustment(id, username);
                if (success)
                {
                    TempData["Success"] = "Stock adjustment deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete stock adjustment";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting stock adjustment {id}");
                TempData["Error"] = "Error deleting stock adjustment: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: StockAdjustments/Approve/5
        public IActionResult Approve(int id)
        {
            try
            {
                var adjustment = _adjustmentService.GetAdjustmentById(id);
                if (adjustment == null)
                    return NotFound();

                if (!adjustment.RequiresApproval || adjustment.IsApproved)
                {
                    TempData["Error"] = "This adjustment does not require approval or is already approved";
                    return RedirectToAction(nameof(Index));
                }

                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock adjustment {id} for approval");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockAdjustments/Approve/5
        [HttpPost, ActionName("Approve")]
        [ValidateAntiForgeryToken]
        public IActionResult ApproveConfirmed(int id, string? remarks)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _adjustmentService.ApproveAdjustment(id, username, remarks);

                if (success)
                {
                    TempData["Success"] = "Stock adjustment approved successfully! Inventory ledger updated.";
                }
                else
                {
                    TempData["Error"] = "Failed to approve stock adjustment";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error approving stock adjustment {id}");
                TempData["Error"] = "Error approving stock adjustment: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: StockAdjustments/Reject/5
        public IActionResult Reject(int id)
        {
            try
            {
                var adjustment = _adjustmentService.GetAdjustmentById(id);
                if (adjustment == null)
                    return NotFound();

                if (!adjustment.RequiresApproval || adjustment.IsApproved || adjustment.IsRejected)
                {
                    TempData["Error"] = "This adjustment cannot be rejected";
                    return RedirectToAction(nameof(Index));
                }

                return View(adjustment);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading stock adjustment {id} for rejection");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: StockAdjustments/Reject/5
        [HttpPost, ActionName("Reject")]
        [ValidateAntiForgeryToken]
        public IActionResult RejectConfirmed(int id, string reason)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(reason))
                {
                    TempData["Error"] = "Rejection reason is required";
                    return RedirectToAction(nameof(Reject), new { id });
                }

                var username = User.Identity?.Name ?? "System";
                var success = _adjustmentService.RejectAdjustment(id, username, reason);

                if (success)
                {
                    TempData["Success"] = "Stock adjustment rejected successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to reject stock adjustment";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error rejecting stock adjustment {id}");
                TempData["Error"] = "Error rejecting stock adjustment: " + ex.Message;
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

            // Adjustment types
            ViewBag.AdjustmentTypes = new List<SelectListItem>
            {
                new SelectListItem { Value = "Increase", Text = "Stock Increase" },
                new SelectListItem { Value = "Decrease", Text = "Stock Decrease" },
                new SelectListItem { Value = "Transfer", Text = "Stock Transfer" }
            };

            // Adjustment reasons
            ViewBag.Reasons = new List<SelectListItem>
            {
                new SelectListItem { Value = "Damage", Text = "Damage" },
                new SelectListItem { Value = "Theft", Text = "Theft" },
                new SelectListItem { Value = "Spoilage", Text = "Spoilage" },
                new SelectListItem { Value = "Counting Error", Text = "Counting Error" },
                new SelectListItem { Value = "Physical Verification", Text = "Physical Verification" },
                new SelectListItem { Value = "Moisture Loss", Text = "Moisture Loss" },
                new SelectListItem { Value = "Revaluation", Text = "Revaluation" },
                new SelectListItem { Value = "Other", Text = "Other" }
            };
        }
    }
}
