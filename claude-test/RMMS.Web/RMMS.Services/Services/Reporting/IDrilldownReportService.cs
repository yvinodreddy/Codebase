using System.Collections.Generic;
using System.Threading.Tasks;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for drill-down hierarchical reports
    /// </summary>
    public interface IDrilldownReportService
    {
        /// <summary>
        /// Get sales drilldown report (Year > Quarter > Month > Customer > Product)
        /// </summary>
        Task<DrilldownResult> GetSalesDrilldownAsync(Dictionary<string, string> filters, int currentLevel);

        /// <summary>
        /// Get inventory drilldown report (Warehouse > Category > Product)
        /// </summary>
        Task<DrilldownResult> GetInventoryDrilldownAsync(Dictionary<string, string> filters, int currentLevel);

        /// <summary>
        /// Get production drilldown report (Year > Month > Batch > Machine)
        /// </summary>
        Task<DrilldownResult> GetProductionDrilldownAsync(Dictionary<string, string> filters, int currentLevel);

        /// <summary>
        /// Navigate up in hierarchy
        /// </summary>
        Task<DrilldownResult> NavigateUpAsync(string reportType, Dictionary<string, string> filters, int currentLevel);

        /// <summary>
        /// Get available drilldown report definitions
        /// </summary>
        Task<List<DrilldownReportDefinition>> GetAvailableReportsAsync();
    }
}
