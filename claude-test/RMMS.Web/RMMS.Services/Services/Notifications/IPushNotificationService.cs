using System.Threading.Tasks;

namespace RMMS.Services.Services.Notifications
{
    /// <summary>
    /// TASK 4.4.4: Push Notification Service (Firebase)
    /// Sends push notifications to mobile devices
    /// </summary>
    public interface IPushNotificationService
    {
        Task<bool> SendNotificationAsync(string userId, string title, string body, object? data = null);
        Task<bool> SendToTokenAsync(string deviceToken, string title, string body, object? data = null);
        Task<bool> SendToTopicAsync(string topic, string title, string body, object? data = null);
        Task<bool> RegisterDeviceTokenAsync(string userId, string deviceToken, string platform);
        Task<bool> UnregisterDeviceTokenAsync(string deviceToken);
    }
}
