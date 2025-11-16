using RMMS.Models.Mobile.DTOs;
using System.Threading.Tasks;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for mobile data synchronization with conflict resolution
    /// </summary>
    public interface IMobileSyncService
    {
        /// <summary>
        /// Sync data for a specific entity type
        /// </summary>
        Task<SyncResponseDto<T>> SyncDataAsync<T>(string userId, int deviceId, SyncRequestDto request) where T : class;

        /// <summary>
        /// Batch sync multiple entity types
        /// </summary>
        Task<BatchSyncResponseDto> BatchSyncAsync(string userId, int deviceId, BatchSyncRequestDto request);

        /// <summary>
        /// Pull changes from server (download)
        /// </summary>
        Task<SyncResponseDto<T>> PullChangesAsync<T>(string userId, SyncRequestDto request) where T : class;

        /// <summary>
        /// Push changes to server (upload)
        /// </summary>
        Task<bool> PushChangesAsync<T>(string userId, int deviceId, T[] changes) where T : class;

        /// <summary>
        /// Get sync status for a device
        /// </summary>
        Task<object> GetSyncStatusAsync(int deviceId);

        /// <summary>
        /// Resolve sync conflicts
        /// </summary>
        Task<bool> ResolveConflictAsync(int deviceId, string entityType, string entityId, string resolution);
    }
}
