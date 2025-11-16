using Microsoft.AspNetCore.SignalR;
using Microsoft.AspNetCore.Authorization;

namespace RMMS.Web.Hubs
{
    /// <summary>
    /// SignalR Hub for real-time notifications
    /// Broadcasts alerts, inventory warnings, and system notifications
    /// </summary>
    [Authorize]
    public class NotificationHub : Hub
    {
        private readonly ILogger<NotificationHub> _logger;

        public NotificationHub(ILogger<NotificationHub> logger)
        {
            _logger = logger;
        }

        public override async Task OnConnectedAsync()
        {
            _logger.LogInformation("Client connected to NotificationHub: {ConnectionId}", Context.ConnectionId);
            await Clients.Caller.SendAsync("Connected", new { connectionId = Context.ConnectionId });
            await base.OnConnectedAsync();
        }

        /// <summary>
        /// Send notification to all clients
        /// </summary>
        public async Task SendNotification(string title, string message, string type = "info")
        {
            await Clients.All.SendAsync("ReceiveNotification", new
            {
                title,
                message,
                type,
                timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Send inventory low stock alert
        /// </summary>
        public async Task SendLowStockAlert(int productId, string productName, decimal currentQuantity, decimal reorderLevel)
        {
            await Clients.All.SendAsync("ReceiveLowStockAlert", new
            {
                productId,
                productName,
                currentQuantity,
                reorderLevel,
                timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Subscribe to user-specific notifications
        /// </summary>
        public async Task SubscribeToUserNotifications(string userId)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, $"user_{userId}");
            _logger.LogInformation("Client {ConnectionId} subscribed to user {UserId} notifications", Context.ConnectionId, userId);
        }
    }
}
