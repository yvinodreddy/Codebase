using System.Collections.Generic;
using System.Threading.Tasks;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    public interface ICustomReportBuilderService
    {
        Task<int> SaveReportDefinitionAsync(CustomReportDefinition report);
        Task<CustomReportDefinition> GetReportDefinitionAsync(int reportId);
        Task<List<CustomReportDefinition>> GetUserReportsAsync(string userId);
        Task<CustomReportResult> ExecuteReportAsync(int reportId, Dictionary<string, string> parameters);
        Task<CustomReportResult> ExecuteCustomSQLAsync(string sql);
        Task<bool> DeleteReportAsync(int reportId);
        Task<List<string>> GetAvailableDataSourcesAsync();
        Task<List<string>> GetDataSourceColumnsAsync(string dataSource);
    }
}
