using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Services.Integrations
{
    /// <summary>
    /// TASK 4.3.1: Integration Framework Service Interface
    /// Base interface for all third-party integrations
    /// </summary>
    public interface IIntegrationService
    {
        Task<bool> TestConnectionAsync();
        Task<Dictionary<string, object>> GetStatusAsync();
        Task<bool> EnableAsync();
        Task<bool> DisableAsync();
        Task<SyncResult> SyncDataAsync();
    }

    public class SyncResult
    {
        public bool Success { get; set; }
        public int RecordsProcessed { get; set; }
        public int RecordsFailed { get; set; }
        public List<string> Errors { get; set; } = new List<string>();
        public string Message { get; set; } = string.Empty;
    }
}
