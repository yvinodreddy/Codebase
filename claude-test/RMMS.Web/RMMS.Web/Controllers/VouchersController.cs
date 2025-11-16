using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class VouchersController : Controller
    {
        private readonly ILogger<VouchersController> _logger;
        private readonly IVoucherService _voucherService;

        public VouchersController(
            ILogger<VouchersController> logger,
            IVoucherService voucherService)
        {
            _logger = logger;
            _voucherService = voucherService;
        }

        public IActionResult Index()
        {
            try
            {
                var model = _voucherService.GetAll();
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving vouchers");
                TempData["Error"] = "Error loading vouchers";
                return View(new List<Voucher>());
            }
        }

        public IActionResult Details(int id)
        {
            try
            {
                var voucher = _voucherService.GetById(id);
                if (voucher == null)
                {
                    TempData["Error"] = "Voucher not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(voucher);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving voucher details");
                TempData["Error"] = "Error loading voucher details";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult Create()
        {
            return View(new Voucher { VoucherDate = DateTime.Today });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Voucher model)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    _voucherService.Create(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Voucher created successfully");
                    TempData["Success"] = "Voucher created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating voucher");
                TempData["Error"] = "Error creating voucher. Please try again.";
                return View(model);
            }
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var voucher = _voucherService.GetById(id);
                if (voucher == null)
                {
                    TempData["Error"] = "Voucher not found";
                    return RedirectToAction(nameof(Index));
                }
                return View(voucher);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving voucher for editing");
                TempData["Error"] = "Error loading voucher for editing";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Voucher model)
        {
            try
            {
                if (id != model.Id)
                {
                    TempData["Error"] = "Invalid voucher ID";
                    return RedirectToAction(nameof(Index));
                }

                if (ModelState.IsValid)
                {
                    _voucherService.Update(model, User.Identity?.Name ?? "System");
                    _logger.LogInformation("Voucher updated successfully");
                    TempData["Success"] = "Voucher updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating voucher");
                TempData["Error"] = "Error updating voucher. Please try again.";
                return View(model);
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                var voucher = _voucherService.GetById(id);
                if (voucher == null)
                {
                    TempData["Error"] = "Voucher not found";
                    return RedirectToAction(nameof(Index));
                }

                _voucherService.Delete(id, User.Identity?.Name ?? "System");
                _logger.LogInformation("Voucher deleted successfully");
                TempData["Success"] = "Voucher deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting voucher");
                TempData["Error"] = "Error deleting voucher. Please try again.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}