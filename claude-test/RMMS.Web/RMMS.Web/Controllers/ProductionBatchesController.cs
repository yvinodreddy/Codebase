using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class ProductionBatchesController : Controller
    {
        private readonly IProductionBatchService _batchService;
        private readonly IProductionOrderService _orderService;
        private readonly IEmployeeService _employeeService;
        private readonly ILogger<ProductionBatchesController> _logger;

        public ProductionBatchesController(
            IProductionBatchService batchService,
            IProductionOrderService orderService,
            IEmployeeService employeeService,
            ILogger<ProductionBatchesController> logger)
        {
            _batchService = batchService;
            _orderService = orderService;
            _employeeService = employeeService;
            _logger = logger;
        }

        // GET: ProductionBatches
        public IActionResult Index(string searchTerm, string status, int page = 1, string sortBy = "BatchNumber", string sortOrder = "desc")
        {
            try
            {
                const int pageSize = 16;
                List<ProductionBatch> batches;

                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    batches = _batchService.SearchBatches(searchTerm);
                }
                else if (!string.IsNullOrWhiteSpace(status))
                {
                    batches = _batchService.GetBatchesByStatus(status);
                }
                else
                {
                    batches = _batchService.GetAllBatches();
                }

                var batchesQuery = batches.AsQueryable().OrderByDynamic(sortBy, sortOrder);
                var pagedResult = PagedResult<ProductionBatch>.Create(batchesQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.Status = status;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                // Statistics
                ViewBag.TotalBatches = batches.Count;
                ViewBag.InProgressCount = _batchService.GetInProgressBatchesCount();
                ViewBag.CompletedCount = _batchService.GetCompletedBatchesCount();
                ViewBag.TodayCount = _batchService.GetTodayBatchesCount();
                ViewBag.PendingVerificationCount = _batchService.GetPendingVerificationBatches().Count;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading production batches");
                TempData["Error"] = "Error loading production batches: " + ex.Message;
                return View(new PagedResult<ProductionBatch>());
            }
        }

        // GET: ProductionBatches/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var batch = _batchService.GetBatchWithDetails(id);
                if (batch == null)
                    return NotFound();

                // Calculate statistics
                ViewBag.TotalInputQuantity = _batchService.GetTotalInputQuantity(id);
                ViewBag.TotalOutputQuantity = _batchService.GetTotalOutputQuantity(id);
                ViewBag.Efficiency = _batchService.GetBatchEfficiency(id);

                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading batch details for ID: {Id}", id);
                TempData["Error"] = "Error loading batch details: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: ProductionBatches/Create
        public IActionResult Create()
        {
            try
            {
                LoadDropdownData();

                var batch = new ProductionBatch
                {
                    BatchNumber = _batchService.GenerateBatchNumber(),
                    BatchDate = DateTime.Today,
                    ShiftType = "Morning",
                    Status = "Planned"
                };

                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create batch form");
                TempData["Error"] = "Error loading form: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: ProductionBatches/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(ProductionBatch batch)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var currentUser = User.Identity?.Name ?? "System";
                    var batchId = _batchService.CreateBatch(batch, currentUser);

                    TempData["Success"] = $"Production batch {batch.BatchNumber} created successfully!";
                    return RedirectToAction(nameof(Details), new { id = batchId });
                }

                LoadDropdownData();
                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating batch");
                TempData["Error"] = "Error creating batch: " + ex.Message;
                LoadDropdownData();
                return View(batch);
            }
        }

        // GET: ProductionBatches/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var batch = _batchService.GetBatchById(id);
                if (batch == null)
                    return NotFound();

                // Only allow editing if batch is Planned or In Progress
                if (batch.Status != "Planned" && batch.Status != "In Progress")
                {
                    TempData["Warning"] = $"Cannot edit batch with status: {batch.Status}";
                    return RedirectToAction(nameof(Details), new { id });
                }

                LoadDropdownData();
                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading batch for edit: {Id}", id);
                TempData["Error"] = "Error loading batch: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: ProductionBatches/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, ProductionBatch batch)
        {
            try
            {
                if (id != batch.Id)
                    return NotFound();

                if (ModelState.IsValid)
                {
                    var currentUser = User.Identity?.Name ?? "System";
                    var success = _batchService.UpdateBatch(batch, currentUser);

                    if (success)
                    {
                        TempData["Success"] = $"Batch {batch.BatchNumber} updated successfully!";
                        return RedirectToAction(nameof(Details), new { id });
                    }
                    else
                    {
                        TempData["Error"] = "Failed to update batch.";
                    }
                }

                LoadDropdownData();
                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating batch ID: {Id}", id);
                TempData["Error"] = "Error updating batch: " + ex.Message;
                LoadDropdownData();
                return View(batch);
            }
        }

        // GET: ProductionBatches/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var batch = _batchService.GetBatchById(id);
                if (batch == null)
                    return NotFound();

                // Only allow deletion if batch is Planned
                if (batch.Status != "Planned")
                {
                    TempData["Warning"] = $"Cannot delete batch with status: {batch.Status}";
                    return RedirectToAction(nameof(Details), new { id });
                }

                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading batch for delete: {Id}", id);
                TempData["Error"] = "Error loading batch: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: ProductionBatches/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.DeleteBatch(id, currentUser);

                if (success)
                {
                    TempData["Success"] = "Batch deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete batch. Only Planned batches can be deleted.";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting batch ID: {Id}", id);
                TempData["Error"] = "Error deleting batch: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: ProductionBatches/Start/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Start(int id)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.StartBatch(id, currentUser);

                if (success)
                {
                    TempData["Success"] = "Batch started successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to start batch. Only Planned batches can be started.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error starting batch ID: {Id}", id);
                TempData["Error"] = "Error starting batch: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // GET: ProductionBatches/Complete/5
        public IActionResult Complete(int id)
        {
            try
            {
                var batch = _batchService.GetBatchById(id);
                if (batch == null)
                    return NotFound();

                // Only allow completion if batch is In Progress
                if (batch.Status != "In Progress")
                {
                    TempData["Warning"] = $"Cannot complete batch with status: {batch.Status}";
                    return RedirectToAction(nameof(Details), new { id });
                }

                return View(batch);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading complete form for batch ID: {Id}", id);
                TempData["Error"] = "Error loading form: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: ProductionBatches/Complete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Complete(int id, decimal qualityScore, string? qualityRemarks)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.CompleteBatch(id, qualityScore, qualityRemarks, currentUser);

                if (success)
                {
                    TempData["Success"] = "Batch completed successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to complete batch.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error completing batch ID: {Id}", id);
                TempData["Error"] = "Error completing batch: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: ProductionBatches/Verify/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Verify(int id)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.VerifyBatch(id, currentUser);

                if (success)
                {
                    TempData["Success"] = "Batch verified successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to verify batch. Ensure yield is calculated and verified.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error verifying batch ID: {Id}", id);
                TempData["Error"] = "Error verifying batch: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: ProductionBatches/Cancel/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Cancel(int id, string reason)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.CancelBatch(id, reason, currentUser);

                if (success)
                {
                    TempData["Success"] = "Batch cancelled successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to cancel batch.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cancelling batch ID: {Id}", id);
                TempData["Error"] = "Error cancelling batch: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: ProductionBatches/CalculateYield/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult CalculateYield(int id)
        {
            try
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _batchService.CalculateYield(id, currentUser);

                if (success)
                {
                    TempData["Success"] = "Yield calculated successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to calculate yield. Ensure batch is completed with inputs and outputs.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error calculating yield for batch ID: {Id}", id);
                TempData["Error"] = "Error calculating yield: " + ex.Message;
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        private void LoadDropdownData()
        {
            try
            {
                // Load production orders (only In Progress or Scheduled)
                var orders = _orderService.GetAllProductionOrders()
                    .Where(o => o.Status == "Scheduled" || o.Status == "In Progress")
                    .OrderBy(o => o.OrderNumber)
                    .ToList();

                ViewBag.ProductionOrders = new SelectList(orders, "Id", "OrderNumber");

                // Load employees for operators and supervisors
                var employees = _employeeService.GetAllEmployees()
                    .OrderBy(e => e.EmployeeName)
                    .ToList();

                ViewBag.Operators = new SelectList(employees, "Id", "EmployeeName");
                ViewBag.Supervisors = new SelectList(employees, "Id", "EmployeeName");

                // Shift types
                ViewBag.ShiftTypes = new SelectList(new[] { "Morning", "Evening", "Night" });

                // Status options
                ViewBag.StatusOptions = new SelectList(new[] { "Planned", "In Progress", "Completed", "Verified", "Cancelled" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading dropdown data");
                ViewBag.ProductionOrders = new SelectList(new List<ProductionOrder>(), "Id", "OrderNumber");
                ViewBag.Operators = new SelectList(new List<RMMS.Models.Masters.Employee>(), "Id", "EmployeeName");
                ViewBag.Supervisors = new SelectList(new List<RMMS.Models.Masters.Employee>(), "Id", "EmployeeName");
                ViewBag.ShiftTypes = new SelectList(new[] { "Morning", "Evening", "Night" });
                ViewBag.StatusOptions = new SelectList(new[] { "Planned", "In Progress", "Completed", "Verified", "Cancelled" });
            }
        }
    }
}
