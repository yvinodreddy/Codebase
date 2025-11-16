using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace RMMS.Services.Services
{
    /// <summary>
    /// Background service that runs daily to check and update expired quotations
    /// </summary>
    public class QuoteExpirationBackgroundService : BackgroundService
    {
        private readonly IServiceProvider _serviceProvider;
        private readonly ILogger<QuoteExpirationBackgroundService> _logger;
        private readonly TimeSpan _checkInterval = TimeSpan.FromHours(6); // Check every 6 hours

        public QuoteExpirationBackgroundService(
            IServiceProvider serviceProvider,
            ILogger<QuoteExpirationBackgroundService> logger)
        {
            _serviceProvider = serviceProvider;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Quote Expiration Background Service started");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    await ProcessExpiringQuotes();
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing expiring quotes");
                }

                // Wait for next execution
                await Task.Delay(_checkInterval, stoppingToken);
            }

            _logger.LogInformation("Quote Expiration Background Service stopped");
        }

        private async Task ProcessExpiringQuotes()
        {
            using var scope = _serviceProvider.CreateScope();
            var quoteExpirationService = scope.ServiceProvider
                .GetRequiredService<IQuoteExpirationService>();

            _logger.LogInformation("Starting quote expiration check...");

            // 1. Update expired quotes status
            var expiredCount = await quoteExpirationService.UpdateExpiredQuotesStatus();
            if (expiredCount > 0)
            {
                _logger.LogInformation($"Updated {expiredCount} expired quotations");
            }

            // 2. Send alerts for quotes expiring in 3 days
            var expiringQuotes = await quoteExpirationService.GetExpiringQuotes(3);
            foreach (var quote in expiringQuotes)
            {
                try
                {
                    await quoteExpirationService.SendExpirationAlert(quote.Id);
                    _logger.LogInformation($"Sent expiration alert for quote {quote.QuotationNumber}");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Failed to send alert for quote {quote.QuotationNumber}");
                }
            }

            _logger.LogInformation("Quote expiration check completed");
        }
    }
}
