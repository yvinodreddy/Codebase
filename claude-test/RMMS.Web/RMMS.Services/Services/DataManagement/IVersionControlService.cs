using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IVersionControlService
    {
        Task<int> CreateSnapshotAsync(string entityType, int entityId, object currentState);
        Task<bool> RollbackToVersionAsync(string entityType, int entityId, int versionId);
        Task<List<object>> GetVersionHistoryAsync(string entityType, int entityId);
        Task<object> CompareVersionsAsync(int version1Id, int version2Id);
    }
}
