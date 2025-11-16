using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IMasterDataService
    {
        Task<object> GetGoldenRecordAsync(string entityType, int entityId);
        Task<bool> PromoteToGoldenRecordAsync(string entityType, int entityId);
        Task<List<object>> GetDataQualityScoresAsync(string entityType);
        Task<bool> SyncMasterDataAsync(string entityType);
    }
}
