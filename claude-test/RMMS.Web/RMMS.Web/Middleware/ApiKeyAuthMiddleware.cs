using Microsoft.Extensions.Primitives;

namespace RMMS.Web.Middleware
{
    /// <summary>
    /// Middleware for API Key authentication
    /// Checks for X-API-Key header and validates against configured keys
    /// </summary>
    public class ApiKeyAuthMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly IConfiguration _configuration;
        private readonly ILogger<ApiKeyAuthMiddleware> _logger;
        private const string API_KEY_HEADER = "X-API-Key";

        public ApiKeyAuthMiddleware(
            RequestDelegate next,
            IConfiguration configuration,
            ILogger<ApiKeyAuthMiddleware> logger)
        {
            _next = next;
            _configuration = configuration;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            // Skip API key check for non-API routes
            if (!context.Request.Path.StartsWithSegments("/api"))
            {
                await _next(context);
                return;
            }

            // Skip API key check for authentication endpoints
            if (context.Request.Path.Value?.Contains("/api/v1/Auth", StringComparison.OrdinalIgnoreCase) == true ||
                context.Request.Path.Value?.Contains("/health", StringComparison.OrdinalIgnoreCase) == true ||
                context.Request.Path.Value?.Contains("/swagger", StringComparison.OrdinalIgnoreCase) == true)
            {
                await _next(context);
                return;
            }

            // Check if Bearer token is present (JWT authentication takes precedence)
            if (context.Request.Headers.ContainsKey("Authorization"))
            {
                var authHeader = context.Request.Headers["Authorization"].ToString();
                if (authHeader.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase))
                {
                    await _next(context);
                    return;
                }
            }

            // Check for API Key
            if (!context.Request.Headers.TryGetValue(API_KEY_HEADER, out StringValues apiKeyValues))
            {
                _logger.LogWarning("API Key missing for request: {Path}", context.Request.Path);
                context.Response.StatusCode = 401;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync("{\"error\":\"API Key is missing\",\"message\":\"Please provide a valid API Key in the X-API-Key header\"}");
                return;
            }

            var providedApiKey = apiKeyValues.ToString();

            // Validate API Key
            if (!IsValidApiKey(providedApiKey))
            {
                _logger.LogWarning("Invalid API Key attempt from IP: {IP}, Path: {Path}",
                    context.Connection.RemoteIpAddress, context.Request.Path);
                context.Response.StatusCode = 401;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync("{\"error\":\"Invalid API Key\",\"message\":\"The provided API Key is not valid\"}");
                return;
            }

            // Log successful API Key authentication
            _logger.LogInformation("API Key authentication successful for: {Path}", context.Request.Path);

            await _next(context);
        }

        private bool IsValidApiKey(string providedKey)
        {
            // Get valid API keys from configuration
            var validKeys = _configuration.GetSection("ApiKeys:ValidKeys").Get<string[]>();

            if (validKeys == null || validKeys.Length == 0)
            {
                _logger.LogWarning("No API Keys configured in appsettings.json");
                // If no keys configured, allow access (for backward compatibility)
                return true;
            }

            return validKeys.Contains(providedKey);
        }
    }

    /// <summary>
    /// Extension method to register API Key authentication middleware
    /// </summary>
    public static class ApiKeyAuthMiddlewareExtensions
    {
        public static IApplicationBuilder UseApiKeyAuthentication(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<ApiKeyAuthMiddleware>();
        }
    }
}
