using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Mobile
{
    public class MobileSyncService : IMobileSyncService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MobileSyncService> _logger;

        public MobileSyncService(
            ApplicationDbContext context,
            ILogger<MobileSyncService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<SyncResponseDto<T>> SyncDataAsync<T>(string userId, int deviceId, SyncRequestDto request) where T : class
        {
            var stopwatch = Stopwatch.StartNew();

            try
            {
                var response = await PullChangesAsync<T>(userId, request);

                // Log sync operation
                await LogSyncAsync(deviceId, userId, request.EntityType, "pull",
                    response.Data.Count, 0, stopwatch.ElapsedMilliseconds);

                return response;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error syncing {request.EntityType} for user {userId}");

                // Log failed sync
                await LogSyncAsync(deviceId, userId, request.EntityType, "pull",
                    0, 0, stopwatch.ElapsedMilliseconds, "failed", ex.Message);

                throw;
            }
        }

        public async Task<BatchSyncResponseDto> BatchSyncAsync(string userId, int deviceId, BatchSyncRequestDto request)
        {
            var stopwatch = Stopwatch.StartNew();
            var response = new BatchSyncResponseDto
            {
                ServerTimestamp = DateTime.UtcNow,
                Results = new Dictionary<string, object>()
            };

            int totalRecords = 0;
            int successCount = 0;
            int errorCount = 0;
            var errors = new List<string>();

            foreach (var syncRequest in request.Requests)
            {
                try
                {
                    // NOTE: In a real implementation, you would dynamically determine
                    // the type based on EntityType and call the appropriate repository
                    // For now, this is a placeholder showing the structure

                    _logger.LogInformation($"Syncing entity type: {syncRequest.EntityType}");

                    // Placeholder - in production, route to appropriate service/repository
                    var entityData = new List<object>();

                    response.Results[syncRequest.EntityType] = new SyncResponseDto<object>
                    {
                        Data = entityData,
                        ServerTimestamp = DateTime.UtcNow,
                        TotalRecords = entityData.Count,
                        PageNumber = syncRequest.PageNumber,
                        PageSize = syncRequest.PageSize,
                        HasMore = false
                    };

                    totalRecords += entityData.Count;
                    successCount++;
                }
                catch (Exception ex)
                {
                    errorCount++;
                    errors.Add($"{syncRequest.EntityType}: {ex.Message}");
                    _logger.LogError(ex, $"Error syncing {syncRequest.EntityType}");
                }
            }

            response.TotalRecords = totalRecords;
            response.SuccessCount = successCount;
            response.ErrorCount = errorCount;
            response.Errors = errors.Any() ? errors : null;

            // Log batch sync
            await LogSyncAsync(deviceId, userId, "batch", "pull",
                totalRecords, 0, stopwatch.ElapsedMilliseconds,
                errorCount > 0 ? "partial" : "success");

            return response;
        }

        public Task<SyncResponseDto<T>> PullChangesAsync<T>(string userId, SyncRequestDto request) where T : class
        {
            try
            {
                // NOTE: This is a simplified implementation
                // In production, you would query the appropriate DbSet based on EntityType
                // and apply appropriate filters based on lastSyncTimestamp

                var response = new SyncResponseDto<T>
                {
                    Data = new List<T>(),
                    ServerTimestamp = DateTime.UtcNow,
                    TotalRecords = 0,
                    PageNumber = request.PageNumber,
                    PageSize = request.PageSize,
                    HasMore = false,
                    Metadata = new SyncMetadata
                    {
                        ConflictCount = 0,
                        NextSyncRecommended = DateTime.UtcNow.AddMinutes(15)
                    }
                };

                _logger.LogInformation($"Pulling changes for {request.EntityType}, last sync: {request.LastSyncTimestamp}");

                return Task.FromResult(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error pulling changes for {request.EntityType}");
                throw;
            }
        }

        public async Task<bool> PushChangesAsync<T>(string userId, int deviceId, T[] changes) where T : class
        {
            var stopwatch = Stopwatch.StartNew();

            try
            {
                _logger.LogInformation($"Pushing {changes.Length} changes from device {deviceId}");

                // NOTE: In production, implement actual data merge logic with conflict detection
                // This is a placeholder showing the structure

                // Log sync operation
                await LogSyncAsync(deviceId, userId, typeof(T).Name, "push",
                    changes.Length, 0, stopwatch.ElapsedMilliseconds);

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error pushing changes for user {userId}");

                // Log failed sync
                await LogSyncAsync(deviceId, userId, typeof(T).Name, "push",
                    0, 0, stopwatch.ElapsedMilliseconds, "failed", ex.Message);

                return false;
            }
        }

        public async Task<object> GetSyncStatusAsync(int deviceId)
        {
            try
            {
                var recentSyncs = await _context.SyncLogs
                    .Where(s => s.DeviceId == deviceId)
                    .OrderByDescending(s => s.ServerTimestamp)
                    .Take(10)
                    .ToListAsync();

                var lastSuccessfulSync = recentSyncs
                    .Where(s => s.Status == "success")
                    .OrderByDescending(s => s.ServerTimestamp)
                    .FirstOrDefault();

                return new
                {
                    LastSyncTime = lastSuccessfulSync?.ServerTimestamp,
                    PendingConflicts = recentSyncs.Sum(s => s.ConflictCount),
                    RecentSyncs = recentSyncs.Select(s => new
                    {
                        s.EntityType,
                        s.Operation,
                        s.RecordCount,
                        s.Status,
                        s.ServerTimestamp
                    })
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting sync status for device {deviceId}");
                throw;
            }
        }

        public Task<bool> ResolveConflictAsync(int deviceId, string entityType, string entityId, string resolution)
        {
            try
            {
                _logger.LogInformation($"Resolving conflict for {entityType}:{entityId} on device {deviceId}, resolution: {resolution}");

                // NOTE: In production, implement actual conflict resolution logic
                // This would typically involve:
                // 1. Loading both versions (server and client)
                // 2. Applying the resolution strategy (server-wins, client-wins, merge, etc.)
                // 3. Updating the database
                // 4. Returning the resolved entity to the client

                return Task.FromResult(true);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error resolving conflict");
                return Task.FromResult(false);
            }
        }

        private async Task LogSyncAsync(int deviceId, string userId, string entityType, string operation,
            int recordCount, int conflictCount, long durationMs, string status = "success", string? errorMessage = null)
        {
            try
            {
                var syncLog = new SyncLog
                {
                    DeviceId = deviceId,
                    UserId = userId,
                    EntityType = entityType,
                    Operation = operation,
                    RecordCount = recordCount,
                    ClientTimestamp = DateTime.UtcNow, // Would be provided by client in real scenario
                    ServerTimestamp = DateTime.UtcNow,
                    Status = status,
                    ErrorMessage = errorMessage,
                    ConflictCount = conflictCount,
                    DataSizeBytes = 0, // Would calculate actual size in production
                    DurationMs = (int)durationMs
                };

                _context.SyncLogs.Add(syncLog);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error logging sync operation");
                // Don't throw - logging failure shouldn't break sync
            }
        }
    }
}
