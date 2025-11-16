using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.Monitoring
{
    public class SignalRLog
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(200)]
        public string ConnectionId { get; set; } = string.Empty;

        [StringLength(100)]
        public string HubName { get; set; } = string.Empty;

        [StringLength(100)]
        public string MethodName { get; set; } = string.Empty;

        [StringLength(50)]
        public string EventType { get; set; } = string.Empty;

        public string Payload { get; set; } = string.Empty;

        [StringLength(450)]
        public string UserId { get; set; } = string.Empty;

        [StringLength(50)]
        public string IpAddress { get; set; } = string.Empty;

        public DateTime Timestamp { get; set; } = DateTime.Now;

        public bool IsActive { get; set; } = true;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
