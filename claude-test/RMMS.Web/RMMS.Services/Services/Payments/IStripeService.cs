using System.Threading.Tasks;

namespace RMMS.Services.Services.Payments
{
    /// <summary>
    /// TASK 4.3.5: Stripe Payment Gateway Service
    /// Handles payment processing via Stripe
    /// </summary>
    public interface IStripeService
    {
        Task<PaymentResult> CreatePaymentIntentAsync(decimal amount, string currency, string customerEmail, string orderId);
        Task<PaymentResult> CapturePaymentAsync(string paymentIntentId);
        Task<PaymentResult> RefundPaymentAsync(string transactionId, decimal? amount = null);
        Task<PaymentStatus> GetPaymentStatusAsync(string transactionId);
    }

    public class PaymentResult
    {
        public bool Success { get; set; }
        public string TransactionId { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public string ClientSecret { get; set; } = string.Empty;
    }

    public class PaymentStatus
    {
        public string Status { get; set; } = string.Empty;
        public decimal Amount { get; set; }
        public string Currency { get; set; } = "INR";
        public bool IsRefunded { get; set; }
    }
}
