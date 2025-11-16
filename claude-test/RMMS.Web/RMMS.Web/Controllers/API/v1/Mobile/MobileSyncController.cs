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
    /// API controller for mobile data synchronization
    /// </summary>
    [Route("api/v1/mobile/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    public class MobileSyncController : BaseApiController
    {
        private readonly IMobileSyncService _syncService;

        public MobileSyncController(IMobileSyncService syncService)
        {
            _syncService = syncService;
        }

        /// <summary>
        /// Batch sync multiple entity types
        /// </summary>
        [HttpPost("batch")]
        public async Task<IActionResult> BatchSync([FromBody] BatchSyncRequestDto request, [FromQuery] int deviceId)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            var response = await _syncService.BatchSyncAsync(userId, deviceId, request);
            return Success(response);
        }

        /// <summary>
        /// Pull changes from server for a specific entity type
        /// </summary>
        [HttpPost("pull")]
        public async Task<IActionResult> Pull([FromBody] SyncRequestDto request)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userId))
                return Error("User ID not found", null, 401);

            // NOTE: In production, you would route to the appropriate typed method
            // based on request.EntityType
            var response = await _syncService.PullChangesAsync<object>(userId, request);
            return Success(response);
        }

        /// <summary>
        /// Get sync status for a device
        /// </summary>
        [HttpGet("status")]
        public async Task<IActionResult> GetSyncStatus([FromQuery] int deviceId)
        {
            var status = await _syncService.GetSyncStatusAsync(deviceId);
            return Success(status);
        }

        /// <summary>
        /// Resolve a sync conflict
        /// </summary>
        [HttpPost("resolve-conflict")]
        public async Task<IActionResult> ResolveConflict([FromBody] ResolveConflictDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            var success = await _syncService.ResolveConflictAsync(
                dto.DeviceId,
                dto.EntityType,
                dto.EntityId,
                dto.Resolution
            );

            return success
                ? Success("Conflict resolved successfully")
                : Error("Failed to resolve conflict");
        }
    }

    public class ResolveConflictDto
    {
        public int DeviceId { get; set; }
        public string EntityType { get; set; } = string.Empty;
        public string EntityId { get; set; } = string.Empty;
        public string Resolution { get; set; } = "server-wins"; // server-wins, client-wins, merge
    }
}
