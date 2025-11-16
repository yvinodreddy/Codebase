using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for getting real-time dashboard data (broadcasting handled by controllers/hubs)
    /// </summary>
    public interface IRealtimeDashboardService
    {
        Task<Dictionary<string, object>> GetSalesDashboardDataAsync();
        Task<Dictionary<string, object>> GetProductionDashboardDataAsync();
        Task<Dictionary<string, object>> GetInventoryDashboardDataAsync();
        Task<Dictionary<string, object>> GetFinancialDashboardDataAsync();
    }
}
