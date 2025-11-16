using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/test/graphdb")]
    [AllowAnonymous] // For testing purposes
    public class GraphDBTestController : ControllerBase
    {
        private readonly ILogger<GraphDBTestController> _logger;

        public GraphDBTestController(ILogger<GraphDBTestController> logger)
        {
            _logger = logger;
        }

        [HttpGet("health")]
        public async Task<IActionResult> CheckHealth()
        {
            try
            {
                // Simple GraphDB connection test
                using var httpClient = new HttpClient();
                var response = await httpClient.GetAsync("http://localhost:7200/rest/repositories");

                var isHealthy = response.IsSuccessStatusCode;

                return Ok(new
                {
                    healthy = isHealthy,
                    graphDbUrl = "http://localhost:7200",
                    status = response.StatusCode.ToString(),
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "GraphDB health check failed");
                return Ok(new
                {
                    healthy = false,
                    error = ex.Message,
                    timestamp = DateTime.UtcNow
                });
            }
        }

        [HttpGet("test-connection")]
        public async Task<IActionResult> TestConnection()
        {
            try
            {
                using var httpClient = new HttpClient();
                var response = await httpClient.GetAsync("http://localhost:7200/repositories/healthcare/size");
                var content = await response.Content.ReadAsStringAsync();

                return Ok(new
                {
                    success = response.IsSuccessStatusCode,
                    repositorySize = content,
                    message = "GraphDB repository connection test"
                });
            }
            catch (Exception ex)
            {
                return Ok(new
                {
                    success = false,
                    error = ex.Message
                });
            }
        }
    }
}