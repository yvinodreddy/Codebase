using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class SalesOrdersController : Controller
    {
        private readonly ISalesOrderService _salesOrderService;
        private readonly ICustomerService _customerService;
        private readonly IProductService _productService;
        private readonly IQuotationService _quotationService;

        public SalesOrdersController(
            ISalesOrderService salesOrderService,
            ICustomerService customerService,
            IProductService productService,
            IQuotationService quotationService)
        {
            _salesOrderService = salesOrderService;
            _customerService = customerService;
            _productService = productService;
            _quotationService = quotationService;
        }

        // GET: SalesOrders
        public async Task<IActionResult> Index(string searchTerm, string status, int page = 1)
        {
            try
            {
                const int pageSize = 16;
                IEnumerable<SalesOrder> salesOrders;

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    salesOrders = await _salesOrderService.SearchSalesOrdersAsync(searchTerm);
                }
                else if (!string.IsNullOrEmpty(status))
                {
                    salesOrders = await _salesOrderService.GetSalesOrdersByStatusAsync(status);
                }
                else
                {
                    salesOrders = await _salesOrderService.GetAllSalesOrdersAsync();
                }

                var stats = await _salesOrderService.GetSalesOrderStatisticsAsync();
                ViewBag.Statistics = stats;
                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = status;

                // Apply pagination
                var totalRecords = salesOrders.Count();
                var totalPages = (int)Math.Ceiling(totalRecords / (double)pageSize);
                var pagedSalesOrders = salesOrders.Skip((page - 1) * pageSize).Take(pageSize).ToList();

                ViewBag.CurrentPage = page;
                ViewBag.TotalPages = totalPages;
                ViewBag.TotalRecords = totalRecords;

                return View(pagedSalesOrders);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading sales orders: {ex.Message}";
                return View(new List<SalesOrder>());
            }
        }

        // GET: SalesOrders/Details/5
        public async Task<IActionResult> Details(int id)
        {
            try
            {
                var salesOrder = await _salesOrderService.GetSalesOrderByIdAsync(id);
                if (salesOrder == null)
                {
                    TempData["Error"] = "Sales order not found.";
                    return RedirectToAction(nameof(Index));
                }

                // Populate products for adding items
                ViewBag.Products = _productService.GetAllProducts();

                return View(salesOrder);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading sales order: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: SalesOrders/Create
        public async Task<IActionResult> Create(int? quotationId)
        {
            await PopulateDropdowns();

            var salesOrder = new SalesOrder
            {
                OrderDate = DateTime.Now,
                DeliveryDate = DateTime.Now.AddDays(15)
            };

            if (quotationId.HasValue)
            {
                var quotation = await _quotationService.GetQuotationByIdAsync(quotationId.Value);
                if (quotation != null && quotation.Status == "Accepted")
                {
                    salesOrder.QuotationId = quotationId.Value;
                    salesOrder.CustomerId = quotation.CustomerId;
                    salesOrder.PaymentTerms = quotation.PaymentTerms;
                    salesOrder.DeliveryTerms = quotation.DeliveryTerms;
                    ViewBag.FromQuotation = true;
                }
            }

            return View(salesOrder);
        }

        // POST: SalesOrders/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(SalesOrder salesOrder)
        {
            try
            {
                salesOrder.CreatedBy = User.Identity?.Name ?? "System";
                salesOrder.CreatedDate = DateTime.Now;

                await _salesOrderService.CreateSalesOrderAsync(salesOrder);
                TempData["Success"] = "Sales order created successfully.";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error creating sales order: {ex.Message}";
                await PopulateDropdowns();
                return View(salesOrder);
            }
        }

        // GET: SalesOrders/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var salesOrder = await _salesOrderService.GetSalesOrderByIdAsync(id);
                if (salesOrder == null)
                {
                    TempData["Error"] = "Sales order not found.";
                    return RedirectToAction(nameof(Index));
                }

                await PopulateDropdowns();
                return View(salesOrder);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading sales order: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: SalesOrders/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, SalesOrder salesOrder)
        {
            if (id != salesOrder.Id)
            {
                return NotFound();
            }

            try
            {
                salesOrder.ModifiedBy = User.Identity?.Name ?? "System";
                salesOrder.ModifiedDate = DateTime.Now;

                await _salesOrderService.UpdateSalesOrderAsync(salesOrder);
                TempData["Success"] = "Sales order updated successfully.";
                return RedirectToAction(nameof(Details), new { id = salesOrder.Id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error updating sales order: {ex.Message}";
                await PopulateDropdowns();
                return View(salesOrder);
            }
        }

        // GET: SalesOrders/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var salesOrder = await _salesOrderService.GetSalesOrderByIdAsync(id);
                if (salesOrder == null)
                {
                    TempData["Error"] = "Sales order not found.";
                    return RedirectToAction(nameof(Index));
                }

                return View(salesOrder);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading sales order: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: SalesOrders/DeleteConfirmed
        [HttpPost, ActionName("DeleteConfirmed")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            try
            {
                await _salesOrderService.DeleteSalesOrderAsync(id);
                TempData["Success"] = "Sales order deleted successfully.";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error deleting sales order: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: SalesOrders/Confirm/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Confirm(int id, int approvedByEmployeeId)
        {
            try
            {
                var result = await _salesOrderService.ConfirmSalesOrderAsync(id, approvedByEmployeeId);
                if (result)
                {
                    TempData["Success"] = "Sales order confirmed successfully.";
                }
                else
                {
                    TempData["Error"] = "Unable to confirm sales order. Check status.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error confirming sales order: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: SalesOrders/UpdateStatus
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> UpdateStatus(int id, string newStatus)
        {
            try
            {
                var result = await _salesOrderService.UpdateOrderStatusAsync(id, newStatus);
                if (result)
                {
                    TempData["Success"] = $"Order status updated to {newStatus}.";
                }
                else
                {
                    TempData["Error"] = "Unable to update status.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error updating status: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: SalesOrders/ReserveStock
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ReserveStock(int id)
        {
            try
            {
                var result = await _salesOrderService.ReserveStockAsync(id);
                if (result)
                {
                    TempData["Success"] = "Stock reserved successfully.";
                }
                else
                {
                    TempData["Error"] = "Unable to reserve stock.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error reserving stock: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: SalesOrders/Cancel
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Cancel(int id, string cancellationReason)
        {
            try
            {
                var result = await _salesOrderService.CancelSalesOrderAsync(id, cancellationReason);
                if (result)
                {
                    TempData["Success"] = "Sales order cancelled.";
                }
                else
                {
                    TempData["Error"] = "Unable to cancel sales order.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error cancelling sales order: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: SalesOrders/AddItem
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AddItem(int salesOrderId, SalesOrderItem item)
        {
            try
            {
                item.SalesOrderId = salesOrderId;

                // Calculate line totals
                var subtotal = item.Quantity * item.UnitPrice;
                item.DiscountAmount = item.DiscountAmount ?? 0;
                item.TaxAmount = item.TaxAmount ?? 0;
                item.TotalAmount = subtotal - (item.DiscountAmount ?? 0) + (item.TaxAmount ?? 0);

                await _salesOrderService.AddSalesOrderItemAsync(salesOrderId, item);
                TempData["Success"] = "Item added successfully.";
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error adding item: {ex.Message}";
            }

            return RedirectToAction(nameof(Details), new { id = salesOrderId });
        }

        // POST: SalesOrders/RemoveItem
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RemoveItem(int salesOrderId, int itemId)
        {
            try
            {
                await _salesOrderService.RemoveSalesOrderItemAsync(salesOrderId, itemId);
                TempData["Success"] = "Item removed successfully.";
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error removing item: {ex.Message}";
            }

            return RedirectToAction(nameof(Details), new { id = salesOrderId });
        }

        private async Task PopulateDropdowns()
        {
            var customers = _customerService.GetAllCustomers();
            var products = _productService.GetAllProducts();
            var quotations = await _quotationService.GetAllQuotationsAsync();

            ViewBag.Customers = customers;
            ViewBag.Products = products;
            ViewBag.Quotations = quotations.Where(q => q.Status == "Accepted");
        }
    }
}
