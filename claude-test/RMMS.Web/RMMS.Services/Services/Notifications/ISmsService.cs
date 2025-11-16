using System.Threading.Tasks;

namespace RMMS.Services.Services.Notifications
{
    /// <summary>
    /// TASK 4.3.6: SMS Service Interface (Twilio)
    /// Sends SMS notifications
    /// </summary>
    public interface ISmsService
    {
        Task<bool> SendSmsAsync(string phoneNumber, string message);
        Task<bool> SendBulkSmsAsync(string[] phoneNumbers, string message);
        Task<SmsStatus> GetSmsStatusAsync(string messageId);
    }

    public class SmsStatus
    {
        public string MessageId { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public string ErrorMessage { get; set; } = string.Empty;
    }
}
