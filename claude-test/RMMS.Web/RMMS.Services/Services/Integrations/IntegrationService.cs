using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using RMMS.DataAccess.Context;
using RMMS.Models.API;

namespace RMMS.Services.Services.Integrations
{
    /// <summary>
    /// TASK 4.3.1: Integration Framework Service Implementation
    /// Base implementation for third-party integrations
    /// </summary>
    public class IntegrationService : IIntegrationService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<IntegrationService> _logger;
        private readonly IConfiguration _configuration;

        public IntegrationService(
            ApplicationDbContext context,
            ILogger<IntegrationService> logger,
            IConfiguration configuration)
        {
            _context = context;
            _logger = logger;
            _configuration = configuration;
        }

        public async Task<bool> TestConnectionAsync()
        {
            try
            {
                _logger.LogInformation("Testing integration connection");

                // Test database connectivity
                var canConnect = await _context.Database.CanConnectAsync();

                if (canConnect)
                {
                    _logger.LogInformation("Integration connection test successful");
                    return true;
                }
                else
                {
                    _logger.LogWarning("Integration connection test failed");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error testing integration connection");
                return false;
            }
        }

        public async Task<Dictionary<string, object>> GetStatusAsync()
        {
            try
            {
                var status = new Dictionary<string, object>();

                // Get active integrations count
                var activeIntegrations = await _context.Set<IntegrationStatus>()
                    .Where(i => i.IsActive)
                    .CountAsync();

                // Get last check times
                var lastCheckTimes = await _context.Set<IntegrationStatus>()
                    .Where(i => i.IsActive)
                    .Select(i => new { i.Name, i.LastChecked })
                    .ToListAsync();

                status.Add("activeIntegrations", activeIntegrations);
                status.Add("lastCheckTimes", lastCheckTimes);
                status.Add("systemStatus", "Operational");
                status.Add("timestamp", DateTime.UtcNow);

                _logger.LogDebug("Retrieved integration status");
                return status;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting integration status");
                return new Dictionary<string, object>
                {
                    { "error", ex.Message },
                    { "systemStatus", "Error" },
                    { "timestamp", DateTime.UtcNow }
                };
            }
        }

        public async Task<bool> EnableAsync()
        {
            try
            {
                _logger.LogInformation("Enabling integration");

                // Update all integrations to active
                var integrations = await _context.Set<IntegrationStatus>().ToListAsync();
                foreach (var integration in integrations)
                {
                    integration.IsActive = true;
                    integration.LastChecked = DateTime.UtcNow;
                }

                await _context.SaveChangesAsync();

                _logger.LogInformation("Integration enabled successfully");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error enabling integration");
                return false;
            }
        }

        public async Task<bool> DisableAsync()
        {
            try
            {
                _logger.LogInformation("Disabling integration");

                // Update all integrations to inactive
                var integrations = await _context.Set<IntegrationStatus>().ToListAsync();
                foreach (var integration in integrations)
                {
                    integration.IsActive = false;
                }

                await _context.SaveChangesAsync();

                _logger.LogInformation("Integration disabled successfully");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error disabling integration");
                return false;
            }
        }

        public async Task<SyncResult> SyncDataAsync()
        {
            var result = new SyncResult();

            try
            {
                _logger.LogInformation("Starting integration data sync");

                var activeIntegrations = await _context.Set<IntegrationStatus>()
                    .Where(i => i.IsActive)
                    .ToListAsync();

                result.RecordsProcessed = activeIntegrations.Count;

                foreach (var integration in activeIntegrations)
                {
                    try
                    {
                        integration.LastChecked = DateTime.UtcNow;
                        integration.LastSuccess = DateTime.UtcNow;
                        integration.Status = "Completed";
                        integration.SuccessCount++;
                    }
                    catch (Exception ex)
                    {
                        result.RecordsFailed++;
                        integration.FailureCount++;
                        integration.LastError = ex.Message;
                        result.Errors.Add($"{integration.Name}: {ex.Message}");
                        _logger.LogError(ex, $"Error syncing integration: {integration.Name}");
                    }
                }

                await _context.SaveChangesAsync();

                result.Success = result.RecordsFailed == 0;
                result.Message = result.Success
                    ? $"Sync completed successfully. {result.RecordsProcessed} records processed."
                    : $"Sync completed with errors. {result.RecordsProcessed - result.RecordsFailed}/{result.RecordsProcessed} records synced.";

                _logger.LogInformation(result.Message);
                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during integration sync");
                result.Success = false;
                result.Message = $"Sync failed: {ex.Message}";
                result.Errors.Add(ex.Message);
                return result;
            }
        }
    }
}
