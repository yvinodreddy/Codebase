using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Mobile.DTOs
{
    /// <summary>
    /// DTO for registering a mobile device
    /// </summary>
    public class DeviceRegistrationDto
    {
        [Required]
        [MaxLength(200)]
        public string DeviceId { get; set; } = string.Empty;

        [Required]
        [MaxLength(20)]
        public string Platform { get; set; } = string.Empty; // "Android" or "iOS"

        [MaxLength(100)]
        public string? DeviceModel { get; set; }

        [MaxLength(50)]
        public string? OSVersion { get; set; }

        [Required]
        [MaxLength(20)]
        public string AppVersion { get; set; } = string.Empty;

        [Required]
        [MaxLength(500)]
        public string PushToken { get; set; } = string.Empty;

        [MaxLength(10)]
        public string? Language { get; set; }

        public bool NotificationsEnabled { get; set; } = true;

        public bool BiometricEnabled { get; set; } = false;
    }

    /// <summary>
    /// Response DTO for device registration
    /// </summary>
    public class DeviceRegistrationResponseDto
    {
        public int DeviceId { get; set; }
        public bool IsNewDevice { get; set; }
        public MobileAppConfigDto? AppConfig { get; set; }
    }
}
