using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Web.Controllers
{
    public class RiceProcurementExternalController : Controller
    {
        private readonly ILogger<RiceProcurementExternalController> _logger;
        private readonly IRiceProcurementExternalService _service;

        public RiceProcurementExternalController(
            ILogger<RiceProcurementExternalController> logger,
            IRiceProcurementExternalService service)
        {
            _logger = logger;
            _service = service;
        }

        public IActionResult Index()
        {
            var data = _service.GetAll();
            return View(data);
        }

        public IActionResult Create()
        {
            var model = new RiceProcurementExternal
            {
                Date = DateTime.Today,
                PaymentStatus = "Pending"
            };

            PopulateDropdowns();
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(RiceProcurementExternal model)
        {
            if (ModelState.IsValid)
            {
                try
                {
                    string username = User.Identity?.Name ?? "System";
                    _service.Create(model, username);
                    TempData["Success"] = "External rice procurement record created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating rice procurement external record");
                    ModelState.AddModelError("", "An error occurred while creating the record. Please try again.");
                }
            }

            PopulateDropdowns();
            return View(model);
        }

        private void PopulateDropdowns()
        {
            ViewBag.ItemDescriptions = new List<string>
            {
                "Mansuri",
                "Katrni",
                "Sonam",
                "Basmati",
                "Sona Masoori",
                "IR-64"
            };

            ViewBag.PaymentModes = new List<string>
            {
                "Cash",
                "Online",
                "Cheque",
                "Credit"
            };
        }
    }
}