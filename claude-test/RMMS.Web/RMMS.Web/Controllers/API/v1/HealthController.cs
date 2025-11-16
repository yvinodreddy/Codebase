using Microsoft.AspNetCore.Mvc;

namespace RMMS.Web.Controllers.API.v1
{
    /// <summary>
    /// Health check endpoint for API monitoring
    /// </summary>
    [Route("api/v1/[controller]")]
    public class HealthController : BaseApiController
    {
        /// <summary>
        /// Basic health check endpoint
        /// </summary>
        /// <returns>API health status</returns>
        [HttpGet]
        public IActionResult Get()
        {
            return Success(new
            {
                status = "healthy",
                timestamp = DateTime.UtcNow,
                version = "1.0.0",
                environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"
            }, "API is healthy");
        }

        /// <summary>
        /// Detailed health check with database connectivity
        /// </summary>
        [HttpGet("detailed")]
        public IActionResult GetDetailed()
        {
            // TODO: Add database connectivity check
            return Success(new
            {
                status = "healthy",
                timestamp = DateTime.UtcNow,
                version = "1.0.0",
                environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production",
                checks = new
                {
                    api = "healthy",
                    database = "pending", // Will implement in Task 4.1.7
                    memory = "healthy"
                }
            }, "API is healthy");
        }

        /// <summary>
        /// Ping endpoint for quick connectivity test
        /// </summary>
        [HttpGet("ping")]
        public IActionResult Ping()
        {
            return Success(new { message = "pong" });
        }
    }
}
