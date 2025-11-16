using Microsoft.AspNetCore.SignalR;
using Microsoft.AspNetCore.Authorization;

namespace RMMS.Web.Hubs
{
    /// <summary>
    /// SignalR Hub for real-time production updates
    /// Broadcasts production status, batch completions, and machine status changes
    /// </summary>
    [Authorize]
    public class ProductionHub : Hub
    {
        private readonly ILogger<ProductionHub> _logger;

        public ProductionHub(ILogger<ProductionHub> logger)
        {
            _logger = logger;
        }

        public override async Task OnConnectedAsync()
        {
            _logger.LogInformation("Client connected: {ConnectionId}", Context.ConnectionId);
            await Clients.Caller.SendAsync("Connected", new { connectionId = Context.ConnectionId, message = "Connected to ProductionHub" });
            await base.OnConnectedAsync();
        }

        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            _logger.LogInformation("Client disconnected: {ConnectionId}", Context.ConnectionId);
            await base.OnDisconnectedAsync(exception);
        }

        /// <summary>
        /// Broadcast production batch update to all connected clients
        /// </summary>
        public async Task SendProductionUpdate(object update)
        {
            await Clients.All.SendAsync("ReceiveProductionUpdate", update);
        }

        /// <summary>
        /// Broadcast machine status change
        /// </summary>
        public async Task SendMachineStatusUpdate(int machineId, string status)
        {
            await Clients.All.SendAsync("ReceiveMachineStatus", new { machineId, status, timestamp = DateTime.UtcNow });
        }

        /// <summary>
        /// Subscribe to specific machine updates
        /// </summary>
        public async Task SubscribeToMachine(int machineId)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, $"machine_{machineId}");
            _logger.LogInformation("Client {ConnectionId} subscribed to machine {MachineId}", Context.ConnectionId, machineId);
        }

        /// <summary>
        /// Unsubscribe from machine updates
        /// </summary>
        public async Task UnsubscribeFromMachine(int machineId)
        {
            await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"machine_{machineId}");
            _logger.LogInformation("Client {ConnectionId} unsubscribed from machine {MachineId}", Context.ConnectionId, machineId);
        }
    }
}
