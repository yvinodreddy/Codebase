using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Services.Integrations
{
    /// <summary>
    /// TASK 4.3.2: Webhook Service Interface
    /// Manages webhook subscriptions and deliveries
    /// </summary>
    public interface IWebhookService
    {
        Task<int> CreateWebhookAsync(string name, string url, string secret, List<string> events);
        Task<bool> DeleteWebhookAsync(int id);
        Task<bool> DeliverWebhookAsync(string eventType, object payload);
        Task RetryFailedDeliveriesAsync();
    }

    public class WebhookDelivery
    {
        public int Id { get; set; }
        public string EventType { get; set; } = string.Empty;
        public string Payload { get; set; } = string.Empty;
        public string Status { get; set; } = "Pending";
        public int AttemptCount { get; set; }
    }
}
