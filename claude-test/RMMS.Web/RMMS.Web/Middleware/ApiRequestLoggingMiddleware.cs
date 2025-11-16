using System.Diagnostics;
using System.Text;

namespace RMMS.Web.Middleware
{
    /// <summary>
    /// Middleware for detailed API request/response logging
    /// Logs request details, response times, and status codes
    /// </summary>
    public class ApiRequestLoggingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ApiRequestLoggingMiddleware> _logger;

        public ApiRequestLoggingMiddleware(
            RequestDelegate next,
            ILogger<ApiRequestLoggingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            // Only log API requests (skip static files, MVC pages, etc.)
            if (!context.Request.Path.StartsWithSegments("/api"))
            {
                await _next(context);
                return;
            }

            // Generate unique request ID
            var requestId = Guid.NewGuid().ToString("N").Substring(0, 8);
            context.Items["RequestId"] = requestId;

            var stopwatch = Stopwatch.StartNew();

            try
            {
                // Log request details
                await LogRequest(context, requestId);

                // Capture original response body stream
                var originalBodyStream = context.Response.Body;

                using var responseBody = new MemoryStream();
                context.Response.Body = responseBody;

                // Execute the next middleware
                await _next(context);

                stopwatch.Stop();

                // Log response details
                await LogResponse(context, requestId, stopwatch.ElapsedMilliseconds);

                // Copy response body back to original stream
                await responseBody.CopyToAsync(originalBodyStream);
            }
            catch (Exception ex)
            {
                stopwatch.Stop();
                _logger.LogError(ex, "[{RequestId}] Request failed after {ElapsedMs}ms: {Method} {Path}",
                    requestId, stopwatch.ElapsedMilliseconds, context.Request.Method, context.Request.Path);
                throw;
            }
        }

        private async Task LogRequest(HttpContext context, string requestId)
        {
            var request = context.Request;

            // Build request details
            var requestDetails = new StringBuilder();
            requestDetails.AppendLine($"[{requestId}] API Request:");
            requestDetails.AppendLine($"  Method: {request.Method}");
            requestDetails.AppendLine($"  Path: {request.Path}{request.QueryString}");
            requestDetails.AppendLine($"  Client IP: {context.Connection.RemoteIpAddress}");
            requestDetails.AppendLine($"  User-Agent: {request.Headers["User-Agent"]}");

            // Log authorization header (without exposing the token)
            if (request.Headers.ContainsKey("Authorization"))
            {
                var authHeader = request.Headers["Authorization"].ToString();
                var tokenPreview = authHeader.Length > 20
                    ? $"{authHeader.Substring(0, 20)}... (truncated)"
                    : authHeader;
                requestDetails.AppendLine($"  Authorization: {tokenPreview}");
            }

            // Log API version if present
            if (request.Headers.ContainsKey("X-Api-Version"))
            {
                requestDetails.AppendLine($"  API Version: {request.Headers["X-Api-Version"]}");
            }

            // Log request body for POST/PUT/PATCH (only in development or for debugging)
            if ((request.Method == "POST" || request.Method == "PUT" || request.Method == "PATCH")
                && request.ContentLength > 0
                && request.ContentLength < 10000) // Only log small payloads
            {
                request.EnableBuffering();
                var buffer = new byte[Convert.ToInt32(request.ContentLength)];
                await request.Body.ReadAsync(buffer, 0, buffer.Length);
                var bodyAsText = Encoding.UTF8.GetString(buffer);
                request.Body.Position = 0; // Reset position for next middleware

                // Sanitize sensitive data
                bodyAsText = SanitizeSensitiveData(bodyAsText);
                requestDetails.AppendLine($"  Body: {bodyAsText}");
            }

            _logger.LogInformation(requestDetails.ToString());
        }

        private Task LogResponse(HttpContext context, string requestId, long elapsedMs)
        {
            var response = context.Response;

            // Determine log level based on status code
            var logLevel = response.StatusCode switch
            {
                >= 500 => LogLevel.Error,
                >= 400 => LogLevel.Warning,
                _ => LogLevel.Information
            };

            // Log response summary
            _logger.Log(logLevel,
                "[{RequestId}] API Response: {Method} {Path} - Status: {StatusCode} - Duration: {ElapsedMs}ms",
                requestId, context.Request.Method, context.Request.Path, response.StatusCode, elapsedMs);

            // Log warning for slow requests
            if (elapsedMs > 3000)
            {
                _logger.LogWarning(
                    "[{RequestId}] SLOW REQUEST: {Method} {Path} took {ElapsedMs}ms",
                    requestId, context.Request.Method, context.Request.Path, elapsedMs);
            }

            return Task.CompletedTask;
        }

        private string SanitizeSensitiveData(string input)
        {
            // Remove or mask sensitive fields like passwords, tokens, etc.
            var sensitiveFields = new[] { "password", "token", "secret", "apiKey", "creditCard" };

            foreach (var field in sensitiveFields)
            {
                // Simple regex to mask sensitive data (can be enhanced)
                input = System.Text.RegularExpressions.Regex.Replace(
                    input,
                    $"\"{field}\"\\s*:\\s*\"([^\"]+)\"",
                    $"\"{field}\":\"***REDACTED***\"",
                    System.Text.RegularExpressions.RegexOptions.IgnoreCase);
            }

            return input;
        }
    }

    /// <summary>
    /// Extension method to register the request logging middleware
    /// </summary>
    public static class ApiRequestLoggingMiddlewareExtensions
    {
        public static IApplicationBuilder UseApiRequestLogging(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<ApiRequestLoggingMiddleware>();
        }
    }
}
