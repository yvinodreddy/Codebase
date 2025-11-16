// RMMS.Web/Controllers/RiceSalesController.cs
using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;
using System.Security.Claims;  // Add this for getting the username

namespace RMMS.Web.Controllers
{
    public class RiceSalesController : Controller
    {
        private readonly IRiceSalesService _riceSalesService;
        private readonly ILogger<RiceSalesController> _logger;

        public RiceSalesController(IRiceSalesService riceSalesService, ILogger<RiceSalesController> logger)
        {
            _riceSalesService = riceSalesService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var sales = _riceSalesService.GetAllSales();
                return View(sales);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading rice sales");
                // Return an empty list if service isn't configured yet
                return View(new List<RiceSales>());
            }
        }

        public IActionResult Create()
        {
            try
            {
                var model = new RiceSales
                {
                    SaleDate = DateTime.Today,
                    InvoiceNumber = GenerateInvoiceNumber(),
                    // Initialize other required properties to prevent null issues
                    PaymentStatus = "Pending",
                    PaymentMode = "Cash",
                    Discount = 0,
                    FreightCharges = 0,
                    OtherCharges = 0
                };
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating new rice sale form");
                TempData["Error"] = "Error loading form: " + ex.Message;
                return RedirectToAction("Index");
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(RiceSales model)
        {
            // Remove system fields from validation
            ModelState.Remove("CreatedBy");
            ModelState.Remove("ModifiedBy");
            ModelState.Remove("BuyerGSTIN");  // Remove if optional

            if (ModelState.IsValid)
            {
                try
                {
                    string currentUsername = User.Identity?.Name ?? "System";
                    _riceSalesService.CreateSale(model, currentUsername);
                    TempData["Success"] = "Rice sale record created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating rice sale: {Message}", ex.Message);
                    ModelState.AddModelError("", "Error: " + ex.Message);
                }
            }

            // Re-generate invoice number if returning to view
            model.InvoiceNumber = GenerateInvoiceNumber();
            return View(model);
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var sale = _riceSalesService.GetSaleById(id);
                if (sale == null)
                {
                    return NotFound();
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading rice sale for edit");
                TempData["Error"] = "Error loading sale record: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, RiceSales model)
        {
            if (id != model.Id)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    // For update operations, we also need to track who modified it
                    string currentUsername = User.Identity?.Name ?? "System";

                    // Pass the username for the update operation too
                    _riceSalesService.UpdateSale(model, currentUsername);

                    TempData["Success"] = "Rice sale record updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error updating rice sale");
                    ModelState.AddModelError("", "An error occurred while updating the record.");
                }
            }
            return View(model);
        }

        public IActionResult Details(int id)
        {
            try
            {
                var sale = _riceSalesService.GetSaleById(id);
                if (sale == null)
                {
                    return NotFound();
                }
                return View(sale);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading rice sale details");
                TempData["Error"] = "Error loading sale details: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        private string GenerateInvoiceNumber()
        {
            // This creates a unique invoice number using the current date and a random number
            // Format: INV-20240315-1234
            return $"INV-{DateTime.Now:yyyyMMdd}-{new Random().Next(1000, 9999)}";
        }
    }
}