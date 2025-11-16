using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;

namespace RMMS.Web.Hubs
{
    public class DashboardHub : Hub
    {
        public async Task SendDashboardUpdate(string updateType, object data)
        {
            await Clients.All.SendAsync("ReceiveDashboardUpdate", updateType, data);
        }

        public async Task JoinDashboardGroup(string dashboardType)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, dashboardType);
        }

        public async Task LeaveDashboardGroup(string dashboardType)
        {
            await Groups.RemoveFromGroupAsync(Context.ConnectionId, dashboardType);
        }

        public override async Task OnConnectedAsync()
        {
            await Clients.Caller.SendAsync("Connected", Context.ConnectionId);
            await base.OnConnectedAsync();
        }

        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            await base.OnDisconnectedAsync(exception);
        }
    }
}
