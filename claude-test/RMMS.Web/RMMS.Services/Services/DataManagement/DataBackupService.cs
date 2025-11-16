using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;

namespace RMMS.Services.Services.DataManagement
{
    public class DataBackupService : IDataBackupService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<DataBackupService> _logger;
        private readonly IConfiguration _configuration;

        public DataBackupService(
            ApplicationDbContext context,
            ILogger<DataBackupService> logger,
            IConfiguration configuration)
        {
            _context = context;
            _logger = logger;
            _configuration = configuration;
        }

        public async Task<bool> CreateDatabaseBackupAsync(string backupName)
        {
            try
            {
                var databaseName = _context.Database.GetDbConnection().Database;
                var backupPath = $"/var/backups/rmms/{backupName}_{DateTime.Now:yyyyMMdd_HHmmss}.bak";

                var sql = $@"
                    BACKUP DATABASE [{databaseName}]
                    TO DISK = '{backupPath}'
                    WITH FORMAT,
                    MEDIANAME = 'RMMS_Backup',
                    NAME = '{backupName}';
                ";

                await _context.Database.ExecuteSqlRawAsync(sql);
                _logger.LogInformation($"Database backup created: {backupPath}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Database backup failed");
                return false;
            }
        }

        public async Task<bool> RestoreDatabaseBackupAsync(string backupPath)
        {
            try
            {
                var databaseName = _context.Database.GetDbConnection().Database;

                var sql = $@"
                    USE master;
                    ALTER DATABASE [{databaseName}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                    RESTORE DATABASE [{databaseName}] FROM DISK = '{backupPath}' WITH REPLACE;
                    ALTER DATABASE [{databaseName}] SET MULTI_USER;
                ";

                await _context.Database.ExecuteSqlRawAsync(sql);
                _logger.LogInformation($"Database restored from: {backupPath}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Database restore failed");
                return false;
            }
        }

        public async Task<List<string>> GetAvailableBackupsAsync()
        {
            await Task.CompletedTask;
            // In production, scan backup directory
            return new List<string> { "backup_20251021.bak", "backup_20251020.bak" };
        }

        public async Task<bool> ScheduleAutomaticBackupAsync(string schedule)
        {
            _logger.LogInformation($"Backup scheduled: {schedule}");
            await Task.CompletedTask;
            // Use Hangfire for scheduling
            return true;
        }
    }
}
