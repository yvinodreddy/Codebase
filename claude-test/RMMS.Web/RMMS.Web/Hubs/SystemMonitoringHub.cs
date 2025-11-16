using Microsoft.AspNetCore.SignalR;
using Microsoft.AspNetCore.Authorization;

namespace RMMS.Web.Hubs
{
    /// <summary>
    /// SignalR Hub for real-time system monitoring
    /// Broadcasts system metrics, performance data, and monitoring alerts
    /// </summary>
    [Authorize]
    public class SystemMonitoringHub : Hub
    {
        private readonly ILogger<SystemMonitoringHub> _logger;

        public SystemMonitoringHub(ILogger<SystemMonitoringHub> logger)
        {
            _logger = logger;
        }

        public override async Task OnConnectedAsync()
        {
            _logger.LogInformation("Client connected to SystemMonitoringHub: {ConnectionId}", Context.ConnectionId);
            await Clients.Caller.SendAsync("Connected", new { connectionId = Context.ConnectionId, timestamp = DateTime.UtcNow });
            await base.OnConnectedAsync();
        }

        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            _logger.LogInformation("Client disconnected from SystemMonitoringHub: {ConnectionId}", Context.ConnectionId);
            await base.OnDisconnectedAsync(exception);
        }

        /// <summary>
        /// Broadcast system performance metrics to all connected clients
        /// </summary>
        public async Task BroadcastSystemMetrics(object metrics)
        {
            await Clients.All.SendAsync("ReceiveSystemMetrics", metrics);
        }

        /// <summary>
        /// Send real-time database statistics
        /// </summary>
        public async Task BroadcastDatabaseStats(int activeConnections, int totalQueries, decimal averageResponseTime)
        {
            await Clients.All.SendAsync("ReceiveDatabaseStats", new
            {
                activeConnections,
                totalQueries,
                averageResponseTime,
                timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Send real-time application metrics
        /// </summary>
        public async Task BroadcastApplicationMetrics(double cpuUsage, long memoryUsageMB, int requestsPerSecond)
        {
            await Clients.All.SendAsync("ReceiveApplicationMetrics", new
            {
                cpuUsage,
                memoryUsageMB,
                requestsPerSecond,
                timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Send system alert to all monitoring clients
        /// </summary>
        public async Task SendSystemAlert(string severity, string message, string source)
        {
            await Clients.All.SendAsync("ReceiveSystemAlert", new
            {
                severity,
                message,
                source,
                timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Join a specific monitoring group (e.g., "database", "api", "production")
        /// </summary>
        public async Task JoinMonitoringGroup(string groupName)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, groupName);
            _logger.LogInformation("Client {ConnectionId} joined monitoring group: {GroupName}", Context.ConnectionId, groupName);
        }

        /// <summary>
        /// Leave a specific monitoring group
        /// </summary>
        public async Task LeaveMonitoringGroup(string groupName)
        {
            await Groups.RemoveFromGroupAsync(Context.ConnectionId, groupName);
            _logger.LogInformation("Client {ConnectionId} left monitoring group: {GroupName}", Context.ConnectionId, groupName);
        }

        /// <summary>
        /// Send metrics to a specific monitoring group
        /// </summary>
        public async Task BroadcastToGroup(string groupName, object data)
        {
            await Clients.Group(groupName).SendAsync("ReceiveGroupMetrics", data);
        }

        // ============================================================
        // SIGNALR CONSOLE COMPATIBILITY METHODS
        // ============================================================

        /// <summary>
        /// Send a message to all connected clients (Console compatibility)
        /// </summary>
        public async Task SendMessage(string user, string message)
        {
            await Clients.All.SendAsync("ReceiveMessage", user, message);
            _logger.LogInformation("Message sent from {User}: {Message}", user, message);
        }

        /// <summary>
        /// Join a group (Console compatibility - alias for JoinMonitoringGroup)
        /// </summary>
        public async Task JoinGroup(string groupName)
        {
            await JoinMonitoringGroup(groupName);
        }

        /// <summary>
        /// Broadcast current system metrics (Console compatibility)
        /// </summary>
        public async Task BroadcastMetrics()
        {
            var metrics = new
            {
                timestamp = DateTime.UtcNow,
                cpuUsage = Environment.ProcessorCount,
                memoryUsage = GC.GetTotalMemory(false) / 1024 / 1024, // MB
                activeConnections = 1,
                status = "Healthy"
            };

            await Clients.All.SendAsync("MetricsUpdate", metrics);
            _logger.LogInformation("Broadcasting metrics to all clients");
        }
    }
}
