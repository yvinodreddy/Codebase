using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace RMMS.Services.Services
{
    public interface IQuoteExpirationService
    {
        Task<List<Quotation>> GetExpiringQuotes(int daysBeforeExpiry = 3);
        Task<List<Quotation>> GetExpiredQuotes();
        Task<int> UpdateExpiredQuotesStatus();
        Task<bool> SendExpirationAlert(int quotationId);
        Task<QuoteExpirationSummary> GetExpirationSummary();
        Task<bool> ExtendQuoteValidity(int quotationId, int additionalDays);
    }

    public class QuoteExpirationService : IQuoteExpirationService
    {
        private readonly ApplicationDbContext _context;
        private readonly IEmailNotificationService _emailService;
        private readonly ILogger<QuoteExpirationService> _logger;

        public QuoteExpirationService(
            ApplicationDbContext context,
            IEmailNotificationService emailService,
            ILogger<QuoteExpirationService> logger)
        {
            _context = context;
            _emailService = emailService;
            _logger = logger;
        }

        /// <summary>
        /// Get quotes that are expiring within specified days
        /// </summary>
        public async Task<List<Quotation>> GetExpiringQuotes(int daysBeforeExpiry = 3)
        {
            var today = DateTime.Today;
            var expiryThreshold = today.AddDays(daysBeforeExpiry);

            var expiringQuotes = await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.QuotationItems)
                .Where(q => q.IsActive &&
                           q.Status != "Expired" &&
                           q.Status != "Converted" &&
                           q.Status != "Rejected" &&
                           q.ValidUntil > today &&
                           q.ValidUntil <= expiryThreshold)
                .OrderBy(q => q.ValidUntil)
                .ToListAsync();

            return expiringQuotes;
        }

        /// <summary>
        /// Get all quotes that have expired but status not updated
        /// </summary>
        public async Task<List<Quotation>> GetExpiredQuotes()
        {
            var today = DateTime.Today;

            var expiredQuotes = await _context.Quotations
                .Include(q => q.Customer)
                .Where(q => q.IsActive &&
                           q.Status != "Expired" &&
                           q.Status != "Converted" &&
                           q.Status != "Rejected" &&
                           q.ValidUntil < today)
                .OrderBy(q => q.ValidUntil)
                .ToListAsync();

            return expiredQuotes;
        }

        /// <summary>
        /// Update status of all expired quotations
        /// </summary>
        public async Task<int> UpdateExpiredQuotesStatus()
        {
            var expiredQuotes = await GetExpiredQuotes();

            foreach (var quote in expiredQuotes)
            {
                quote.Status = "Expired";
                quote.ModifiedDate = DateTime.Now;
                quote.ModifiedBy = "System";

                _logger.LogInformation($"Quote {quote.QuotationNumber} marked as expired");
            }

            await _context.SaveChangesAsync();

            return expiredQuotes.Count;
        }

        /// <summary>
        /// Send expiration alert email for a specific quotation
        /// </summary>
        public async Task<bool> SendExpirationAlert(int quotationId)
        {
            var quote = await _context.Quotations
                .Include(q => q.Customer)
                    .ThenInclude(c => c!.Contacts)
                .FirstOrDefaultAsync(q => q.Id == quotationId);

            if (quote == null)
                return false;

            var daysUntilExpiry = (quote.ValidUntil - DateTime.Today).Days;

            var subject = $"Quotation Expiring Soon - {quote.QuotationNumber}";
            var body = $@"
                <html>
                <body style='font-family: Arial, sans-serif;'>
                    <div style='max-width: 600px; margin: 0 auto; padding: 20px;'>
                        <h2 style='color: #e74c3c;'>Quotation Expiring Soon</h2>

                        <div style='background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;'>
                            <strong>⚠️ This quotation will expire in {daysUntilExpiry} days</strong>
                        </div>

                        <h3>Quotation Details:</h3>
                        <table style='width: 100%; border-collapse: collapse;'>
                            <tr>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'><strong>Quotation #:</strong></td>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'>{quote.QuotationNumber}</td>
                            </tr>
                            <tr>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'><strong>Date:</strong></td>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'>{quote.QuotationDate:dd-MMM-yyyy}</td>
                            </tr>
                            <tr>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'><strong>Valid Until:</strong></td>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd; color: #e74c3c;'><strong>{quote.ValidUntil:dd-MMM-yyyy}</strong></td>
                            </tr>
                            <tr>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'><strong>Total Amount:</strong></td>
                                <td style='padding: 8px; border-bottom: 1px solid #ddd;'><strong>₹{quote.TotalAmount:N2}</strong></td>
                            </tr>
                        </table>

                        <p style='margin-top: 20px;'>
                            Please review this quotation and take necessary action before it expires.
                            If you need an extension, please contact us immediately.
                        </p>

                        <div style='background-color: #f8f9fa; padding: 15px; margin-top: 20px; border-radius: 5px;'>
                            <p style='margin: 0;'><strong>Need to extend the validity?</strong></p>
                            <p style='margin: 5px 0 0 0;'>Contact our sales team: sales@rmms.com | +91-XXXXXXXXXX</p>
                        </div>

                        <br/>
                        <p>Best Regards,<br/>
                        <strong>RMMS Sales Team</strong></p>
                    </div>
                </body>
                </html>
            ";

            // Get customer's primary contact email
            var customerEmail = quote.Customer?.Contacts?
                .Where(c => c != null && c.IsPrimary)
                .Select(c => c.Email)
                .FirstOrDefault()
                ?? "customer@example.com";

            return await _emailService.SendCustomEmail(customerEmail, subject, body);
        }

        /// <summary>
        /// Get comprehensive expiration summary
        /// </summary>
        public async Task<QuoteExpirationSummary> GetExpirationSummary()
        {
            var today = DateTime.Today;

            var summary = new QuoteExpirationSummary
            {
                ExpiringToday = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.ValidUntil == today),

                ExpiringTomorrow = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.ValidUntil == today.AddDays(1)),

                ExpiringIn3Days = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.ValidUntil > today &&
                    q.ValidUntil <= today.AddDays(3)),

                ExpiringIn7Days = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.ValidUntil > today &&
                    q.ValidUntil <= today.AddDays(7)),

                ExpiredNotUpdated = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.ValidUntil < today),

                TotalActiveQuotes = await _context.Quotations.CountAsync(q =>
                    q.IsActive &&
                    q.Status != "Expired" &&
                    q.Status != "Converted" &&
                    q.Status != "Rejected")
            };

            // Calculate total value at risk
            var expiringQuotes = await GetExpiringQuotes(7);
            summary.TotalValueAtRisk = expiringQuotes.Sum(q => q.TotalAmount);

            return summary;
        }

        /// <summary>
        /// Extend quote validity by specified days
        /// </summary>
        public async Task<bool> ExtendQuoteValidity(int quotationId, int additionalDays)
        {
            var quote = await _context.Quotations.FindAsync(quotationId);

            if (quote == null || quote.Status == "Expired" || quote.Status == "Converted")
                return false;

            quote.ValidUntil = quote.ValidUntil.AddDays(additionalDays);
            quote.ModifiedDate = DateTime.Now;
            quote.ModifiedBy = "System";

            await _context.SaveChangesAsync();

            _logger.LogInformation($"Quote {quote.QuotationNumber} validity extended by {additionalDays} days");

            return true;
        }
    }

    // Supporting class
    public class QuoteExpirationSummary
    {
        public int ExpiringToday { get; set; }
        public int ExpiringTomorrow { get; set; }
        public int ExpiringIn3Days { get; set; }
        public int ExpiringIn7Days { get; set; }
        public int ExpiredNotUpdated { get; set; }
        public int TotalActiveQuotes { get; set; }
        public decimal TotalValueAtRisk { get; set; }

        public int TotalCritical => ExpiringToday + ExpiringTomorrow;
        public int TotalWarning => ExpiringIn3Days;
        public double CriticalPercentage => TotalActiveQuotes > 0
            ? (TotalCritical * 100.0 / TotalActiveQuotes)
            : 0;
    }
}
