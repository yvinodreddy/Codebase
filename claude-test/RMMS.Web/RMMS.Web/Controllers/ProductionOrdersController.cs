using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;

namespace RMMS.Web.Controllers
{
    public class ProductionOrdersController : Controller
    {
        private readonly IProductionOrderService _productionOrderService;
        private readonly IMachineService _machineService;

        public ProductionOrdersController(
            IProductionOrderService productionOrderService,
            IMachineService machineService)
        {
            _productionOrderService = productionOrderService;
            _machineService = machineService;
        }

        // GET: ProductionOrders
        public IActionResult Index(string searchTerm, string orderStatus, int page = 1, string sortBy = "OrderDate", string sortOrder = "desc")
        {
            try
            {
                const int pageSize = 16;

                List<ProductionOrder> orders;

                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    orders = _productionOrderService.SearchProductionOrders(searchTerm);
                }
                else if (!string.IsNullOrWhiteSpace(orderStatus))
                {
                    orders = _productionOrderService.GetProductionOrdersByStatus(orderStatus);
                }
                else
                {
                    orders = _productionOrderService.GetAllProductionOrders();
                }

                // Apply sorting
                var ordersQuery = orders.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<ProductionOrder>.Create(ordersQuery, page, pageSize, sortBy, sortOrder);

                // Set statistics in ViewBag
                ViewBag.TotalOrders = _productionOrderService.GetTotalProductionOrdersCount();
                ViewBag.DraftCount = _productionOrderService.GetDraftOrdersCount();
                ViewBag.ScheduledCount = _productionOrderService.GetScheduledOrdersCount();
                ViewBag.InProgressCount = _productionOrderService.GetInProgressOrdersCount();
                ViewBag.CompletedCount = _productionOrderService.GetCompletedOrdersCount();
                ViewBag.TotalPlannedQty = _productionOrderService.GetTotalPlannedQuantity();
                ViewBag.TotalProducedQty = _productionOrderService.GetTotalProducedQuantity();
                ViewBag.AverageYield = _productionOrderService.GetAverageYieldPercent();
                ViewBag.OverdueCount = _productionOrderService.GetOverdueOrders().Count;

                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = orderStatus;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch
            {
                return View(new PagedResult<ProductionOrder>());
            }
        }

        // GET: ProductionOrders/Details/5
        public IActionResult Details(int id)
        {
            var order = _productionOrderService.GetProductionOrderById(id);
            if (order == null)
            {
                return NotFound();
            }

            return View(order);
        }

        // GET: ProductionOrders/Create
        public IActionResult Create()
        {
            // Populate dropdowns
            ViewBag.Machines = new SelectList(_machineService.GetOperationalMachines(), "Id", "MachineName");
            ViewBag.OrderNumber = _productionOrderService.GenerateOrderNumber();

            return View();
        }

        // POST: ProductionOrders/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(ProductionOrder order)
        {
            if (ModelState.IsValid)
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _productionOrderService.CreateProductionOrder(order, currentUser);
                if (success)
                {
                    TempData["SuccessMessage"] = "Production order created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                else
                {
                    ModelState.AddModelError("", "Failed to create production order.");
                }
            }

            // Repopulate dropdowns on error
            ViewBag.Machines = new SelectList(_machineService.GetOperationalMachines(), "Id", "MachineName");
            ViewBag.OrderNumber = order.OrderNumber;

            return View(order);
        }

        // GET: ProductionOrders/Edit/5
        public IActionResult Edit(int id)
        {
            var order = _productionOrderService.GetProductionOrderById(id);
            if (order == null)
            {
                return NotFound();
            }

            // Only allow editing of Draft and Scheduled orders
            if (order.Status != "Draft" && order.Status != "Scheduled")
            {
                TempData["ErrorMessage"] = "Cannot edit orders that are in progress or completed.";
                return RedirectToAction(nameof(Details), new { id });
            }

            // Populate dropdowns
            ViewBag.Machines = new SelectList(_machineService.GetOperationalMachines(), "Id", "MachineName", order.AssignedMachineId);

            return View(order);
        }

        // POST: ProductionOrders/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, ProductionOrder order)
        {
            if (id != order.Id)
            {
                return BadRequest();
            }

            if (ModelState.IsValid)
            {
                var currentUser = User.Identity?.Name ?? "System";
                var success = _productionOrderService.UpdateProductionOrder(order, currentUser);
                if (success)
                {
                    TempData["SuccessMessage"] = "Production order updated successfully!";
                    return RedirectToAction(nameof(Details), new { id });
                }
                else
                {
                    ModelState.AddModelError("", "Failed to update production order.");
                }
            }

            // Repopulate dropdowns on error
            ViewBag.Machines = new SelectList(_machineService.GetOperationalMachines(), "Id", "MachineName", order.AssignedMachineId);

            return View(order);
        }

        // GET: ProductionOrders/Delete/5
        public IActionResult Delete(int id)
        {
            var order = _productionOrderService.GetProductionOrderById(id);
            if (order == null)
            {
                return NotFound();
            }

            // Only allow deleting Draft orders
            if (order.Status != "Draft")
            {
                TempData["ErrorMessage"] = "Only draft orders can be deleted. Use Cancel instead.";
                return RedirectToAction(nameof(Details), new { id });
            }

            return View(order);
        }

        // POST: ProductionOrders/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            var success = _productionOrderService.DeleteProductionOrder(id);
            if (success)
            {
                TempData["SuccessMessage"] = "Production order deleted successfully!";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to delete production order.";
            }

            return RedirectToAction(nameof(Index));
        }

        // POST: ProductionOrders/Schedule/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Schedule(int id, DateTime scheduledDate, int? machineId, int? supervisorId)
        {
            var success = _productionOrderService.ScheduleOrder(id, scheduledDate, machineId, supervisorId, "System");
            if (success)
            {
                TempData["SuccessMessage"] = "Production order scheduled successfully!";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to schedule production order.";
            }

            return RedirectToAction(nameof(Details), new { id });
        }

        // POST: ProductionOrders/Start/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Start(int id)
        {
            var success = _productionOrderService.StartProduction(id, "System");
            if (success)
            {
                TempData["SuccessMessage"] = "Production started successfully!";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to start production. Order must be scheduled and have a machine assigned.";
            }

            return RedirectToAction(nameof(Details), new { id });
        }

        // GET: ProductionOrders/Complete/5
        public IActionResult Complete(int id)
        {
            var order = _productionOrderService.GetProductionOrderById(id);
            if (order == null)
            {
                return NotFound();
            }

            if (order.Status != "In Progress")
            {
                TempData["ErrorMessage"] = "Only orders in progress can be completed.";
                return RedirectToAction(nameof(Details), new { id });
            }

            return View(order);
        }

        // POST: ProductionOrders/Complete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Complete(int id, decimal actualQuantity, decimal actualYield)
        {
            var success = _productionOrderService.CompleteProduction(id, actualQuantity, actualYield, "System");
            if (success)
            {
                TempData["SuccessMessage"] = "Production completed successfully!";
                return RedirectToAction(nameof(Details), new { id });
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to complete production.";
                return RedirectToAction(nameof(Complete), new { id });
            }
        }

        // GET: ProductionOrders/Cancel/5
        public IActionResult Cancel(int id)
        {
            var order = _productionOrderService.GetProductionOrderById(id);
            if (order == null)
            {
                return NotFound();
            }

            if (!_productionOrderService.CanCancelOrder(id))
            {
                TempData["ErrorMessage"] = "This order cannot be cancelled.";
                return RedirectToAction(nameof(Details), new { id });
            }

            return View(order);
        }

        // POST: ProductionOrders/Cancel/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Cancel(int id, string reason)
        {
            if (string.IsNullOrWhiteSpace(reason))
            {
                TempData["ErrorMessage"] = "Cancellation reason is required.";
                return RedirectToAction(nameof(Cancel), new { id });
            }

            var success = _productionOrderService.CancelOrder(id, "System", reason);
            if (success)
            {
                TempData["SuccessMessage"] = "Production order cancelled successfully!";
                return RedirectToAction(nameof(Details), new { id });
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to cancel production order.";
                return RedirectToAction(nameof(Cancel), new { id });
            }
        }
    }
}
