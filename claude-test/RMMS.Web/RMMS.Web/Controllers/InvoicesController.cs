using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using RMMS.Services;
using RMMS.Models;

namespace RMMS.Web.Controllers
{
    public class InvoicesController : Controller
    {
        private readonly ILogger<InvoicesController> _logger;
        private readonly IRiceSalesService _riceSalesService;

        public InvoicesController(
            ILogger<InvoicesController> logger,
            IRiceSalesService riceSalesService)
        {
            _logger = logger;
            _riceSalesService = riceSalesService;
        }

        /// <summary>
        /// Invoice Template Selector Page
        /// </summary>
        public IActionResult Index()
        {
            _logger.LogInformation("Invoice templates page accessed");
            return View();
        }

        /// <summary>
        /// Professional Invoice Template 1 - Modern Blue Design
        /// </summary>
        public IActionResult Template1(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 1 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                // If no saleId provided, get the most recent sale as an example
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Professional Invoice Template 2 - Minimalist Black & White
        /// </summary>
        public IActionResult Template2(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 2 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Professional Invoice Template 3 - Colorful Modern Design
        /// </summary>
        public IActionResult Template3(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 3 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Professional Invoice Template 4 - Classic Traditional
        /// </summary>
        public IActionResult Template4(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 4 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Professional Invoice Template 5 - International Format
        /// </summary>
        public IActionResult Template5(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 5 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Professional Invoice Template 6 - Detailed GST Format
        /// </summary>
        public IActionResult Template6(int? saleId)
        {
            _logger.LogInformation($"Invoice Template 6 accessed for sale: {saleId}");

            RiceSales? saleData = null;
            if (saleId.HasValue)
            {
                saleData = _riceSalesService.GetSaleById(saleId.Value);
                if (saleData == null)
                {
                    _logger.LogWarning($"Sale with ID {saleId} not found");
                    TempData["ErrorMessage"] = $"Invoice not found for Sale ID: {saleId}";
                    return RedirectToAction("Index");
                }
            }
            else
            {
                var allSales = _riceSalesService.GetAllSales(true);
                saleData = allSales.OrderByDescending(s => s.SaleDate).FirstOrDefault();

                if (saleData == null)
                {
                    _logger.LogWarning("No sales data found in database");
                    TempData["ErrorMessage"] = "No sales data available. Please create a sale first.";
                    return RedirectToAction("Index");
                }
            }

            return View(saleData);
        }

        /// <summary>
        /// Generate PDF for invoice
        /// </summary>
        [HttpPost]
        public IActionResult GeneratePDF(int saleId, int templateNumber = 1)
        {
            _logger.LogInformation($"Generating PDF for sale {saleId} using template {templateNumber}");

            // TODO: Implement PDF generation using a library like SelectPdf or IronPDF
            // For now, client-side PDF generation is used via jsPDF

            return Json(new { success = true, message = "PDF generation handled client-side" });
        }

        /// <summary>
        /// Email invoice to customer
        /// </summary>
        [HttpPost]
        public IActionResult EmailInvoice(int saleId, string email, int templateNumber = 1)
        {
            _logger.LogInformation($"Emailing invoice for sale {saleId} to {email}");

            // TODO: Implement email sending functionality

            return Json(new { success = true, message = "Email functionality coming in Phase 2.2" });
        }
    }
}
