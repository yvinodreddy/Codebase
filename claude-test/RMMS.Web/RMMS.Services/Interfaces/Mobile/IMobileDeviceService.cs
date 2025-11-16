using RMMS.Models.Mobile;
using RMMS.Models.Mobile.DTOs;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for managing mobile device registrations and tracking
    /// </summary>
    public interface IMobileDeviceService
    {
        /// <summary>
        /// Register or update a mobile device
        /// </summary>
        Task<DeviceRegistrationResponseDto> RegisterDeviceAsync(string userId, DeviceRegistrationDto dto);

        /// <summary>
        /// Get device by ID
        /// </summary>
        Task<MobileDevice?> GetDeviceByIdAsync(int deviceId);

        /// <summary>
        /// Get all devices for a user
        /// </summary>
        Task<List<MobileDevice>> GetUserDevicesAsync(string userId);

        /// <summary>
        /// Update device push token
        /// </summary>
        Task<bool> UpdatePushTokenAsync(int deviceId, string pushToken);

        /// <summary>
        /// Update device last active timestamp
        /// </summary>
        Task<bool> UpdateLastActiveAsync(int deviceId);

        /// <summary>
        /// Deactivate a device
        /// </summary>
        Task<bool> DeactivateDeviceAsync(int deviceId);

        /// <summary>
        /// Delete a device
        /// </summary>
        Task<bool> DeleteDeviceAsync(int deviceId);

        /// <summary>
        /// Get active device count for a user
        /// </summary>
        Task<int> GetActiveDeviceCountAsync(string userId);
    }
}
