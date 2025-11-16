using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Mobile
{
    public class MobileDeviceService : IMobileDeviceService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MobileDeviceService> _logger;
        private readonly IMobileConfigService _configService;

        public MobileDeviceService(
            ApplicationDbContext context,
            ILogger<MobileDeviceService> logger,
            IMobileConfigService configService)
        {
            _context = context;
            _logger = logger;
            _configService = configService;
        }

        public async Task<DeviceRegistrationResponseDto> RegisterDeviceAsync(string userId, DeviceRegistrationDto dto)
        {
            try
            {
                // Check if device already exists
                var existingDevice = await _context.MobileDevices
                    .FirstOrDefaultAsync(d => d.DeviceId == dto.DeviceId && d.UserId == userId);

                bool isNewDevice = existingDevice == null;

                if (existingDevice != null)
                {
                    // Update existing device
                    existingDevice.Platform = dto.Platform;
                    existingDevice.DeviceModel = dto.DeviceModel;
                    existingDevice.OSVersion = dto.OSVersion;
                    existingDevice.AppVersion = dto.AppVersion;
                    existingDevice.PushToken = dto.PushToken;
                    existingDevice.Language = dto.Language;
                    existingDevice.NotificationsEnabled = dto.NotificationsEnabled;
                    existingDevice.BiometricEnabled = dto.BiometricEnabled;
                    existingDevice.LastActiveAt = DateTime.UtcNow;
                    existingDevice.IsActive = true;

                    _context.MobileDevices.Update(existingDevice);
                }
                else
                {
                    // Create new device
                    var newDevice = new MobileDevice
                    {
                        UserId = userId,
                        DeviceId = dto.DeviceId,
                        Platform = dto.Platform,
                        DeviceModel = dto.DeviceModel,
                        OSVersion = dto.OSVersion,
                        AppVersion = dto.AppVersion,
                        PushToken = dto.PushToken,
                        Language = dto.Language,
                        NotificationsEnabled = dto.NotificationsEnabled,
                        BiometricEnabled = dto.BiometricEnabled,
                        RegisteredAt = DateTime.UtcNow,
                        LastActiveAt = DateTime.UtcNow,
                        IsActive = true
                    };

                    _context.MobileDevices.Add(newDevice);
                    existingDevice = newDevice;
                }

                await _context.SaveChangesAsync();

                // Get app configuration
                var appConfig = await _configService.GetConfigAsync(dto.Platform, dto.AppVersion);

                _logger.LogInformation($"Device registered: {dto.DeviceId} for user {userId}, IsNew: {isNewDevice}");

                return new DeviceRegistrationResponseDto
                {
                    DeviceId = existingDevice.Id,
                    IsNewDevice = isNewDevice,
                    AppConfig = appConfig
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error registering device {dto.DeviceId} for user {userId}");
                throw;
            }
        }

        public async Task<MobileDevice?> GetDeviceByIdAsync(int deviceId)
        {
            return await _context.MobileDevices
                .FirstOrDefaultAsync(d => d.Id == deviceId);
        }

        public async Task<List<MobileDevice>> GetUserDevicesAsync(string userId)
        {
            return await _context.MobileDevices
                .Where(d => d.UserId == userId && d.IsActive)
                .OrderByDescending(d => d.LastActiveAt)
                .ToListAsync();
        }

        public async Task<bool> UpdatePushTokenAsync(int deviceId, string pushToken)
        {
            try
            {
                var device = await GetDeviceByIdAsync(deviceId);
                if (device == null) return false;

                device.PushToken = pushToken;
                device.LastActiveAt = DateTime.UtcNow;

                _context.MobileDevices.Update(device);
                await _context.SaveChangesAsync();

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating push token for device {deviceId}");
                return false;
            }
        }

        public async Task<bool> UpdateLastActiveAsync(int deviceId)
        {
            try
            {
                var device = await GetDeviceByIdAsync(deviceId);
                if (device == null) return false;

                device.LastActiveAt = DateTime.UtcNow;

                _context.MobileDevices.Update(device);
                await _context.SaveChangesAsync();

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating last active for device {deviceId}");
                return false;
            }
        }

        public async Task<bool> DeactivateDeviceAsync(int deviceId)
        {
            try
            {
                var device = await GetDeviceByIdAsync(deviceId);
                if (device == null) return false;

                device.IsActive = false;

                _context.MobileDevices.Update(device);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device deactivated: {deviceId}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deactivating device {deviceId}");
                return false;
            }
        }

        public async Task<bool> DeleteDeviceAsync(int deviceId)
        {
            try
            {
                var device = await GetDeviceByIdAsync(deviceId);
                if (device == null) return false;

                _context.MobileDevices.Remove(device);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Device deleted: {deviceId}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting device {deviceId}");
                return false;
            }
        }

        public async Task<int> GetActiveDeviceCountAsync(string userId)
        {
            return await _context.MobileDevices
                .CountAsync(d => d.UserId == userId && d.IsActive);
        }
    }
}
