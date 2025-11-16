using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Mvc;
using RMMS.Models.Mobile.DTOs;
using RMMS.Services.Interfaces.Mobile;
using System.Security.Claims;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers.API.v1.Mobile
{
    /// <summary>
    /// API controller for mobile device management
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    public class MobileDeviceController : BaseApiController
    {
        private readonly IMobileDeviceService _deviceService;

        public MobileDeviceController(IMobileDeviceService deviceService)
        {
            _deviceService = deviceService;
        }

        /// <summary>
        /// Register or update a mobile device
        /// </summary>
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] DeviceRegistrationDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var response = await _deviceService.RegisterDeviceAsync(userId, dto);
            return Success(response, "Device registered successfully");
        }

        /// <summary>
        /// Get all devices for current user
        /// </summary>
        [HttpGet("my-devices")]
        public async Task<IActionResult> GetMyDevices()
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var devices = await _deviceService.GetUserDevicesAsync(userId);
            return Success(devices);
        }

        /// <summary>
        /// Update push token for a device
        /// </summary>
        [HttpPut("{deviceId}/push-token")]
        public async Task<IActionResult> UpdatePushToken(int deviceId, [FromBody] UpdatePushTokenDto dto)
        {
            if (string.IsNullOrEmpty(dto.PushToken))
                return ValidationError("Push token is required");

            var success = await _deviceService.UpdatePushTokenAsync(deviceId, dto.PushToken);
            return success
                ? Success("Push token updated successfully")
                : Error("Failed to update push token");
        }

        /// <summary>
        /// Update device last active timestamp (heartbeat)
        /// </summary>
        [HttpPost("{deviceId}/heartbeat")]
        public async Task<IActionResult> Heartbeat(int deviceId)
        {
            var success = await _deviceService.UpdateLastActiveAsync(deviceId);
            return success
                ? Success("Heartbeat recorded")
                : Error("Device not found", null, 404);
        }

        /// <summary>
        /// Deactivate a device
        /// </summary>
        [HttpPost("{deviceId}/deactivate")]
        public async Task<IActionResult> Deactivate(int deviceId)
        {
            var success = await _deviceService.DeactivateDeviceAsync(deviceId);
            return success
                ? Success("Device deactivated successfully")
                : Error("Failed to deactivate device");
        }

        /// <summary>
        /// Delete a device
        /// </summary>
        [HttpDelete("{deviceId}")]
        public async Task<IActionResult> Delete(int deviceId)
        {
            var success = await _deviceService.DeleteDeviceAsync(deviceId);
            return success
                ? Success("Device deleted successfully")
                : Error("Failed to delete device");
        }
    }

    public class UpdatePushTokenDto
    {
        public string PushToken { get; set; } = string.Empty;
    }
}
