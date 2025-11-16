using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IDataCleansingService
    {
        Task<List<object>> FindDuplicateRecordsAsync(string entityType);
        Task<bool> MergeDuplicatesAsync(string entityType, List<int> duplicateIds, int masterRecordId);
        Task<int> StandardizeDataAsync(string entityType, string field);
        Task<int> CleanInvalidDataAsync(string entityType);
    }
}
