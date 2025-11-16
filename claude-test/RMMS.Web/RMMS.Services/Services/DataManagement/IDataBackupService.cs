using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IDataBackupService
    {
        Task<bool> CreateDatabaseBackupAsync(string backupName);
        Task<bool> RestoreDatabaseBackupAsync(string backupPath);
        Task<List<string>> GetAvailableBackupsAsync();
        Task<bool> ScheduleAutomaticBackupAsync(string schedule);
    }
}
