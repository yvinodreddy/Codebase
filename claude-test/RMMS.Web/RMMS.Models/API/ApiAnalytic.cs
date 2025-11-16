using System;
using System.ComponentModel.DataAnnotations;

namespace RMMS.Models.API
{
    public class ApiAnalytic
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string Name { get; set; } = string.Empty;

        [StringLength(1000)]
        public string Description { get; set; } = string.Empty;

        [StringLength(200)]
        public string Endpoint { get; set; } = string.Empty;

        [StringLength(10)]
        public string Method { get; set; } = "GET";

        public int ResponseTime { get; set; } = 0;

        public int StatusCode { get; set; } = 200;

        [StringLength(450)]
        public string UserId { get; set; } = string.Empty;

        [StringLength(50)]
        public string IpAddress { get; set; } = string.Empty;

        public string RequestBody { get; set; } = string.Empty;

        public string ResponseBody { get; set; } = string.Empty;

        [StringLength(500)]
        public string ErrorMessage { get; set; } = string.Empty;

        public bool IsActive { get; set; } = true;

        public DateTime CreatedDate { get; set; } = DateTime.Now;

        [StringLength(450)]
        public string? ModifiedBy { get; set; }

        public DateTime? ModifiedDate { get; set; }
    }
}
