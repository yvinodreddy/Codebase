using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IAuditTrailService
    {
        Task LogChangeAsync(string entityType, int entityId, string action, string changes, string userId);
        Task<List<object>> GetEntityAuditHistoryAsync(string entityType, int entityId);
        Task<List<object>> GetUserActivityAsync(string userId, DateTime from, DateTime to);
        Task<bool> EnableAuditingAsync(string entityType);
    }
}
