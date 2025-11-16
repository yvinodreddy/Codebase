using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using RMMS.Services.Services;
using RMMS.DataAccess.Data;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Web.Controllers
{
    [Authorize]
    public class QuoteExpirationController : Controller
    {
        private readonly IQuoteExpirationService _expirationService;
        private readonly ApplicationDbContext _context;

        public QuoteExpirationController(
            IQuoteExpirationService expirationService,
            ApplicationDbContext context)
        {
            _expirationService = expirationService;
            _context = context;
        }

        // GET: QuoteExpiration/Dashboard
        public async Task<IActionResult> Dashboard()
        {
            var summary = await _expirationService.GetExpirationSummary();
            ViewBag.Summary = summary;

            var expiringQuotes = await _expirationService.GetExpiringQuotes(7);
            return View(expiringQuotes);
        }

        // GET: QuoteExpiration/ExpiringQuotes
        public async Task<IActionResult> ExpiringQuotes(int days = 7)
        {
            ViewBag.Days = days;
            var quotes = await _expirationService.GetExpiringQuotes(days);
            return View(quotes);
        }

        // GET: QuoteExpiration/ExpiredQuotes
        public async Task<IActionResult> ExpiredQuotes()
        {
            var quotes = await _expirationService.GetExpiredQuotes();
            return View(quotes);
        }

        // POST: QuoteExpiration/ExtendValidity
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ExtendValidity(int id, int additionalDays)
        {
            if (additionalDays <= 0 || additionalDays > 90)
            {
                TempData["ErrorMessage"] = "Additional days must be between 1 and 90.";
                return RedirectToAction(nameof(Dashboard));
            }

            var success = await _expirationService.ExtendQuoteValidity(id, additionalDays);

            if (success)
            {
                TempData["SuccessMessage"] = $"Quotation validity extended by {additionalDays} days.";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to extend quotation validity.";
            }

            return RedirectToAction(nameof(Dashboard));
        }

        // POST: QuoteExpiration/SendAlert
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SendAlert(int id)
        {
            var success = await _expirationService.SendExpirationAlert(id);

            if (success)
            {
                TempData["SuccessMessage"] = "Expiration alert sent successfully.";
            }
            else
            {
                TempData["ErrorMessage"] = "Failed to send expiration alert.";
            }

            return RedirectToAction(nameof(Dashboard));
        }

        // POST: QuoteExpiration/UpdateExpiredStatus
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> UpdateExpiredStatus()
        {
            var count = await _expirationService.UpdateExpiredQuotesStatus();
            TempData["SuccessMessage"] = $"Updated {count} expired quotations.";
            return RedirectToAction(nameof(Dashboard));
        }

        // GET: QuoteExpiration/Widget (for dashboard widget)
        public async Task<IActionResult> Widget()
        {
            var summary = await _expirationService.GetExpirationSummary();
            return PartialView("_ExpirationWidget", summary);
        }
    }
}
