using System.Net;
using System.Text.Json;
using RMMS.Web.Controllers.API;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Web.Middleware
{
    /// <summary>
    /// Global exception handling middleware for API endpoints
    /// Catches unhandled exceptions and returns standardized error responses
    /// </summary>
    public class ApiExceptionMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ApiExceptionMiddleware> _logger;
        private readonly IWebHostEnvironment _env;

        public ApiExceptionMiddleware(
            RequestDelegate next,
            ILogger<ApiExceptionMiddleware> logger,
            IWebHostEnvironment env)
        {
            _next = next;
            _logger = logger;
            _env = env;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                await HandleExceptionAsync(context, ex);
            }
        }

        private async Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            // Log the exception
            _logger.LogError(exception, "An unhandled exception occurred while processing the request");

            // Determine status code and error message based on exception type
            var (statusCode, message, errors) = GetErrorDetails(exception);

            // Create standardized error response
            var response = new ApiResponse<object>
            {
                Success = false,
                Message = message,
                Data = null,
                Errors = errors,
                Timestamp = DateTime.UtcNow
            };

            // Include stack trace in development environment
            if (_env.IsDevelopment())
            {
                response.Errors.Add($"Exception: {exception.GetType().Name}");
                response.Errors.Add($"Stack Trace: {exception.StackTrace}");

                if (exception.InnerException != null)
                {
                    response.Errors.Add($"Inner Exception: {exception.InnerException.Message}");
                }
            }

            // Set response details
            context.Response.StatusCode = (int)statusCode;
            context.Response.ContentType = "application/json";

            // Serialize and write response
            var jsonOptions = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                WriteIndented = _env.IsDevelopment()
            };

            var jsonResponse = JsonSerializer.Serialize(response, jsonOptions);
            await context.Response.WriteAsync(jsonResponse);
        }

        private (HttpStatusCode statusCode, string message, List<string> errors) GetErrorDetails(Exception exception)
        {
            return exception switch
            {
                // Validation exceptions
                ArgumentNullException _ => (
                    HttpStatusCode.BadRequest,
                    "A required parameter was not provided",
                    new List<string> { exception.Message }
                ),
                ArgumentException _ => (
                    HttpStatusCode.BadRequest,
                    "Invalid argument provided",
                    new List<string> { exception.Message }
                ),

                // Database exceptions (more specific first)
                DbUpdateConcurrencyException _ => (
                    HttpStatusCode.Conflict,
                    "The record has been modified by another user",
                    new List<string> { exception.Message }
                ),
                DbUpdateException dbEx => (
                    HttpStatusCode.Conflict,
                    "A database error occurred while saving changes",
                    new List<string> { dbEx.InnerException?.Message ?? dbEx.Message }
                ),

                // Not found exceptions
                KeyNotFoundException _ => (
                    HttpStatusCode.NotFound,
                    "The requested resource was not found",
                    new List<string> { exception.Message }
                ),
                FileNotFoundException _ => (
                    HttpStatusCode.NotFound,
                    "The requested file was not found",
                    new List<string> { exception.Message }
                ),

                // Authorization exceptions
                UnauthorizedAccessException _ => (
                    HttpStatusCode.Forbidden,
                    "You do not have permission to access this resource",
                    new List<string> { exception.Message }
                ),

                // Validation exceptions
                InvalidOperationException _ => (
                    HttpStatusCode.UnprocessableEntity,
                    "The operation is invalid in the current state",
                    new List<string> { exception.Message }
                ),

                // Timeout exceptions
                TimeoutException _ => (
                    HttpStatusCode.RequestTimeout,
                    "The request timed out",
                    new List<string> { exception.Message }
                ),

                // Default: Internal Server Error
                _ => (
                    HttpStatusCode.InternalServerError,
                    "An unexpected error occurred while processing your request",
                    new List<string> { _env.IsDevelopment() ? exception.Message : "Please contact support if the problem persists" }
                )
            };
        }
    }

    /// <summary>
    /// Extension method to register the exception middleware
    /// </summary>
    public static class ApiExceptionMiddlewareExtensions
    {
        public static IApplicationBuilder UseApiExceptionHandler(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<ApiExceptionMiddleware>();
        }
    }
}
