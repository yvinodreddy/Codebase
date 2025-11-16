using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class QuotationsController : Controller
    {
        private readonly IQuotationService _quotationService;
        private readonly ICustomerService _customerService;
        private readonly IProductService _productService;
        private readonly IInquiryService _inquiryService;
        private readonly ISalesOrderService _salesOrderService;

        public QuotationsController(
            IQuotationService quotationService,
            ICustomerService customerService,
            IProductService productService,
            IInquiryService inquiryService,
            ISalesOrderService salesOrderService)
        {
            _quotationService = quotationService;
            _customerService = customerService;
            _productService = productService;
            _inquiryService = inquiryService;
            _salesOrderService = salesOrderService;
        }

        // GET: Quotations
        public async Task<IActionResult> Index(string searchTerm, string status, int page = 1)
        {
            try
            {
                const int pageSize = 16;
                IEnumerable<Quotation> quotations;

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    quotations = await _quotationService.SearchQuotationsAsync(searchTerm);
                }
                else if (!string.IsNullOrEmpty(status))
                {
                    quotations = await _quotationService.GetQuotationsByStatusAsync(status);
                }
                else
                {
                    quotations = await _quotationService.GetAllQuotationsAsync();
                }

                var stats = await _quotationService.GetQuotationStatisticsAsync();
                ViewBag.Statistics = stats;
                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = status;

                // Apply pagination
                var totalRecords = quotations.Count();
                var totalPages = (int)Math.Ceiling(totalRecords / (double)pageSize);
                var pagedQuotations = quotations.Skip((page - 1) * pageSize).Take(pageSize).ToList();

                ViewBag.CurrentPage = page;
                ViewBag.TotalPages = totalPages;
                ViewBag.TotalRecords = totalRecords;

                return View(pagedQuotations);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading quotations: {ex.Message}";
                return View(new List<Quotation>());
            }
        }

        // GET: Quotations/Details/5
        public async Task<IActionResult> Details(int id)
        {
            try
            {
                var quotation = await _quotationService.GetQuotationByIdAsync(id);
                if (quotation == null)
                {
                    TempData["Error"] = "Quotation not found.";
                    return RedirectToAction(nameof(Index));
                }

                // Populate products for adding items
                ViewBag.Products = _productService.GetAllProducts();

                return View(quotation);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading quotation: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Quotations/Create
        public async Task<IActionResult> Create(int? inquiryId)
        {
            await PopulateDropdowns();

            var quotation = new Quotation
            {
                QuotationDate = DateTime.Now,
                ValidUntil = DateTime.Now.AddDays(30)
            };

            if (inquiryId.HasValue)
            {
                var inquiry = await _inquiryService.GetInquiryByIdAsync(inquiryId.Value);
                if (inquiry != null)
                {
                    quotation.InquiryId = inquiryId.Value;
                    quotation.CustomerId = inquiry.CustomerId;
                }
            }

            return View(quotation);
        }

        // POST: Quotations/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Quotation quotation)
        {
            try
            {
                quotation.CreatedBy = User.Identity?.Name ?? "System";
                quotation.CreatedDate = DateTime.Now;

                await _quotationService.CreateQuotationAsync(quotation);
                TempData["Success"] = "Quotation created successfully.";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error creating quotation: {ex.Message}";
                await PopulateDropdowns();
                return View(quotation);
            }
        }

        // GET: Quotations/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var quotation = await _quotationService.GetQuotationByIdAsync(id);
                if (quotation == null)
                {
                    TempData["Error"] = "Quotation not found.";
                    return RedirectToAction(nameof(Index));
                }

                await PopulateDropdowns();
                return View(quotation);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading quotation: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Quotations/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Quotation quotation)
        {
            if (id != quotation.Id)
            {
                return NotFound();
            }

            try
            {
                quotation.ModifiedBy = User.Identity?.Name ?? "System";
                quotation.ModifiedDate = DateTime.Now;

                await _quotationService.UpdateQuotationAsync(quotation);
                TempData["Success"] = "Quotation updated successfully.";
                return RedirectToAction(nameof(Details), new { id = quotation.Id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error updating quotation: {ex.Message}";
                await PopulateDropdowns();
                return View(quotation);
            }
        }

        // GET: Quotations/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var quotation = await _quotationService.GetQuotationByIdAsync(id);
                if (quotation == null)
                {
                    TempData["Error"] = "Quotation not found.";
                    return RedirectToAction(nameof(Index));
                }

                return View(quotation);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading quotation: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Quotations/DeleteConfirmed
        [HttpPost, ActionName("DeleteConfirmed")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            try
            {
                await _quotationService.DeleteQuotationAsync(id);
                TempData["Success"] = "Quotation deleted successfully.";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error deleting quotation: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Quotations/Approve/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Approve(int id, int approvedByEmployeeId)
        {
            try
            {
                var result = await _quotationService.ApproveQuotationAsync(id, approvedByEmployeeId);
                if (result)
                {
                    TempData["Success"] = "Quotation approved and sent successfully.";
                }
                else
                {
                    TempData["Error"] = "Unable to approve quotation. Check status.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error approving quotation: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: Quotations/Send/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Send(int id)
        {
            try
            {
                var result = await _quotationService.SendQuotationAsync(id);
                if (result)
                {
                    TempData["Success"] = "Quotation sent to customer successfully.";
                }
                else
                {
                    TempData["Error"] = "Unable to send quotation. Check status.";
                }
                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error sending quotation: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: Quotations/ConvertToSalesOrder/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ConvertToSalesOrder(int id)
        {
            try
            {
                var quotation = await _quotationService.GetQuotationByIdAsync(id);
                if (quotation == null)
                {
                    TempData["Error"] = "Quotation not found.";
                    return RedirectToAction(nameof(Index));
                }

                if (quotation.Status != "Accepted")
                {
                    TempData["Error"] = "Only accepted quotations can be converted to sales orders.";
                    return RedirectToAction(nameof(Details), new { id });
                }

                // Create sales order from quotation
                var salesOrder = new SalesOrder
                {
                    QuotationId = quotation.Id,
                    CustomerId = quotation.CustomerId,
                    OrderDate = DateTime.Now,
                    DeliveryDate = DateTime.Now.AddDays(15),
                    PaymentTerms = quotation.PaymentTerms,
                    DeliveryTerms = quotation.DeliveryTerms,
                    SubtotalAmount = quotation.SubtotalAmount,
                    DiscountAmount = quotation.DiscountAmount,
                    TaxAmount = quotation.TaxAmount,
                    TotalAmount = quotation.TotalAmount,
                    Status = "Pending",
                    Priority = "Normal",
                    Remarks = $"Created from Quotation: {quotation.QuotationNumber}",
                    CreatedBy = User.Identity?.Name ?? "System",
                    CreatedDate = DateTime.Now
                };

                // Copy quotation items to sales order items
                foreach (var qItem in quotation.QuotationItems)
                {
                    salesOrder.SalesOrderItems.Add(new SalesOrderItem
                    {
                        ProductId = qItem.ProductId,
                        ProductDescription = qItem.ProductDescription,
                        Quantity = qItem.Quantity,
                        UnitOfMeasure = qItem.UnitOfMeasure,
                        UnitPrice = qItem.UnitPrice,
                        DiscountAmount = qItem.DiscountAmount,
                        TaxAmount = qItem.TaxAmount,
                        TotalAmount = qItem.TotalAmount,
                        Remarks = qItem.Remarks
                    });
                }

                await _salesOrderService.CreateSalesOrderAsync(salesOrder);

                TempData["Success"] = $"Sales order created successfully from quotation {quotation.QuotationNumber}.";
                return RedirectToAction("Details", "SalesOrders", new { id = salesOrder.Id });
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error converting quotation: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: Quotations/AddItem
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AddItem(int quotationId, QuotationItem item)
        {
            try
            {
                item.QuotationId = quotationId;

                // Calculate line totals
                var subtotal = item.Quantity * item.UnitPrice;
                item.DiscountAmount = item.DiscountPercent.HasValue
                    ? subtotal * (item.DiscountPercent.Value / 100)
                    : 0;
                item.TaxAmount = item.TaxPercent.HasValue
                    ? (subtotal - (item.DiscountAmount ?? 0)) * (item.TaxPercent.Value / 100)
                    : 0;
                item.TotalAmount = subtotal - (item.DiscountAmount ?? 0) + (item.TaxAmount ?? 0);

                await _quotationService.AddQuotationItemAsync(quotationId, item);
                TempData["Success"] = "Item added successfully.";
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error adding item: {ex.Message}";
            }

            return RedirectToAction(nameof(Details), new { id = quotationId });
        }

        // POST: Quotations/RemoveItem
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RemoveItem(int quotationId, int itemId)
        {
            try
            {
                await _quotationService.RemoveQuotationItemAsync(quotationId, itemId);
                TempData["Success"] = "Item removed successfully.";
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error removing item: {ex.Message}";
            }

            return RedirectToAction(nameof(Details), new { id = quotationId });
        }

        private async Task PopulateDropdowns()
        {
            var customers = _customerService.GetAllCustomers();
            var products = _productService.GetAllProducts();
            var inquiries = await _inquiryService.GetAllInquiriesAsync();

            ViewBag.Customers = customers;
            ViewBag.Products = products;
            ViewBag.Inquiries = inquiries.Where(i => i.Status != "Converted" && i.Status != "Lost");
        }
    }
}
