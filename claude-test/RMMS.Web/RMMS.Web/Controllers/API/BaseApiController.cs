using Microsoft.AspNetCore.Mvc;
using Asp.Versioning;

namespace RMMS.Web.Controllers.API
{
    /// <summary>
    /// Base controller for all API endpoints
    /// Provides standard response format and common functionality
    /// </summary>
    [ApiController]
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    [Produces("application/json")]
    public abstract class BaseApiController : ControllerBase
    {
        /// <summary>
        /// Returns a successful API response
        /// </summary>
        protected IActionResult Success<T>(T data, string message = "Success")
        {
            return Ok(new ApiResponse<T>
            {
                Success = true,
                Message = message,
                Data = data,
                Errors = new List<string>(),
                Timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Returns a successful API response with no data
        /// </summary>
        protected IActionResult Success(string message = "Success")
        {
            return Ok(new ApiResponse<object>
            {
                Success = true,
                Message = message,
                Data = null,
                Errors = new List<string>(),
                Timestamp = DateTime.UtcNow
            });
        }

        /// <summary>
        /// Returns an error API response
        /// </summary>
        protected IActionResult Error(string message, List<string>? errors = null, int statusCode = 400)
        {
            var response = new ApiResponse<object>
            {
                Success = false,
                Message = message,
                Data = null,
                Errors = errors ?? new List<string>(),
                Timestamp = DateTime.UtcNow
            };

            return statusCode switch
            {
                400 => BadRequest(response),
                401 => Unauthorized(response),
                403 => StatusCode(403, response),
                404 => NotFound(response),
                409 => Conflict(response),
                422 => UnprocessableEntity(response),
                500 => StatusCode(500, response),
                _ => StatusCode(statusCode, response)
            };
        }

        /// <summary>
        /// Returns a validation error response
        /// </summary>
        protected IActionResult ValidationError(string message = "Validation failed")
        {
            var errors = ModelState.Values
                .SelectMany(v => v.Errors)
                .Select(e => e.ErrorMessage)
                .ToList();

            return Error(message, errors, 422);
        }

        /// <summary>
        /// Returns a not found error response
        /// </summary>
        protected IActionResult NotFoundError(string message = "Resource not found")
        {
            return Error(message, errors: null, statusCode: 404);
        }

        /// <summary>
        /// Returns an unauthorized error response
        /// </summary>
        protected IActionResult UnauthorizedError(string message = "Unauthorized access")
        {
            return Error(message, errors: null, statusCode: 401);
        }
    }

    /// <summary>
    /// Standard API response format
    /// </summary>
    /// <typeparam name="T">Type of data being returned</typeparam>
    public class ApiResponse<T>
    {
        /// <summary>
        /// Indicates if the request was successful
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Human-readable message about the response
        /// </summary>
        public string Message { get; set; } = string.Empty;

        /// <summary>
        /// The actual data being returned
        /// </summary>
        public T? Data { get; set; }

        /// <summary>
        /// List of error messages (if any)
        /// </summary>
        public List<string> Errors { get; set; } = new List<string>();

        /// <summary>
        /// Timestamp when the response was generated (UTC)
        /// </summary>
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Pagination metadata (optional)
        /// </summary>
        public PaginationMetadata? Pagination { get; set; }
    }

    /// <summary>
    /// Pagination metadata for list responses
    /// </summary>
    public class PaginationMetadata
    {
        public int CurrentPage { get; set; }
        public int PageSize { get; set; }
        public int TotalPages { get; set; }
        public int TotalCount { get; set; }
        public bool HasPrevious => CurrentPage > 1;
        public bool HasNext => CurrentPage < TotalPages;
    }
}
