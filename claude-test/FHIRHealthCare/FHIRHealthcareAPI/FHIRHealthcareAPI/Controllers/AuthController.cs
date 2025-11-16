using FHIRHealthcareAPI.Models;
using FHIRHealthcareAPI.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly UserService _userService;

        public AuthController(UserService userService)
        {
            _userService = userService;
        }

        /// <summary>
        /// POST: api/auth/login
        /// Authenticates a user and returns a JWT token
        /// </summary>
        [HttpPost("login")]
        [AllowAnonymous]  // This endpoint doesn't require authentication
        public async Task<IActionResult> Login([FromBody] LoginRequest request)
        {
            if (string.IsNullOrEmpty(request.Username) || string.IsNullOrEmpty(request.Password))
            {
                return BadRequest(new { error = "Username and password are required" });
            }

            var (success, token, message, user) = await _userService.AuthenticateAsync(
                request.Username, request.Password);

            if (!success)
            {
                return Unauthorized(new { error = message });
            }

            // Return token and user information
            return Ok(new
            {
                token = token,
                expiresIn = 3600,  // seconds
                tokenType = "Bearer",
                user = new
                {
                    id = user.Id,
                    username = user.Username,
                    email = user.Email,
                    fullName = $"{user.FirstName} {user.LastName}",
                    role = user.Role
                }
            });
        }

        /// <summary>
        /// POST: api/auth/register
        /// Registers a new user (admin only)
        /// </summary>
        [HttpPost("register")]
        [Authorize(Roles = "Admin")]  // Only admins can create new users
        public async Task<IActionResult> Register([FromBody] RegisterRequest request)
        {
            var (success, message, user) = await _userService.RegisterAsync(
                request.Username,
                request.Email,
                request.Password,
                request.FirstName,
                request.LastName,
                request.Role,
                request.LicenseNumber);

            if (!success)
            {
                return BadRequest(new { error = message });
            }

            return Created($"api/auth/user/{user.Id}", new
            {
                id = user.Id,
                username = user.Username,
                email = user.Email,
                role = user.Role
            });
        }

        [HttpGet("debug-headers")]
        [AllowAnonymous]
        public IActionResult DebugHeaders()
        {
            var authHeader = Request.Headers["Authorization"].FirstOrDefault();
            var allHeaders = Request.Headers.Select(h => $"{h.Key}: {h.Value}").ToList();

            return Ok(new
            {
                hasAuthHeader = !string.IsNullOrEmpty(authHeader),
                authHeaderValue = authHeader ?? "NONE",
                authHeaderLength = authHeader?.Length ?? 0,
                startsWithBearer = authHeader?.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase),
                allHeaders = allHeaders
            });
        }

        [HttpGet("test-no-auth")]
        [AllowAnonymous]
        public IActionResult TestNoAuth()
        {
            var authHeader = Request.Headers["Authorization"].FirstOrDefault();
            return Ok(new
            {
                message = "Endpoint reached",
                hasAuthHeader = !string.IsNullOrEmpty(authHeader),
                authHeaderValue = authHeader ?? "None"
            });
        }

        [HttpGet("simple-test")]
        [Authorize] // Just requires authentication, no specific role
        public IActionResult SimpleTest()
        {
            return Ok(new
            {
                message = "JWT is working!",
                user = User.Identity.Name,
                isAuthenticated = User.Identity.IsAuthenticated
            });
        }

        [HttpGet("test-auth")]
        [Authorize] // Just require authentication, no specific role
        public IActionResult TestAuth()
        {
            return Ok(new
            {
                authenticated = User.Identity.IsAuthenticated,
                username = User.Identity.Name,
                claims = User.Claims.Select(c => new { type = c.Type, value = c.Value }).ToList()
            });
        } 

        /// <summary>
        /// GET: api/auth/me
        /// Returns current user information
        /// </summary>
        [HttpGet("me")]
        [Authorize]  // Requires authentication
        public async Task<IActionResult> GetCurrentUser()
        {
            // Get user ID from JWT claims
            var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (string.IsNullOrEmpty(userIdClaim))
            {
                return Unauthorized(new { error = "Invalid token" });
            }

            var user = await _userService.GetUserByIdAsync(int.Parse(userIdClaim));
            if (user == null)
            {
                return NotFound(new { error = "User not found" });
            }

            return Ok(new
            {
                id = user.Id,
                username = user.Username,
                email = user.Email,
                fullName = $"{user.FirstName} {user.LastName}",
                role = user.Role,
                permissions = UserRoles.RolePermissions[user.Role]
            });
        }
    }

    // Request models
    public class LoginRequest
    {
        public string Username { get; set; }
        public string Password { get; set; }
    }

    public class RegisterRequest
    {
        public string Username { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Role { get; set; }
        public string LicenseNumber { get; set; }
    }
}