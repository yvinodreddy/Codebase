using System;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IDataArchivalService
    {
        Task<int> ArchiveOldSalesAsync(DateTime beforeDate);
        Task<int> ArchiveOldBatchesAsync(DateTime beforeDate);
        Task<bool> CompressArchivedDataAsync();
        Task<int> DeleteArchivedDataAsync(DateTime beforeDate);
    }
}
