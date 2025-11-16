using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Services.Authentication;
using RMMS.DataAccess.Context;
using RMMS.Models.Authentication;
using System.Security.Claims;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Web.Controllers.API.v1
{
    /// <summary>
    /// Authentication controller for JWT token management
    /// </summary>
    [Route("api/v1/[controller]")]
    public class AuthController : BaseApiController
    {
        private readonly IJwtService _jwtService;
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        public AuthController(
            IJwtService jwtService,
            ApplicationDbContext context,
            IConfiguration configuration)
        {
            _jwtService = jwtService;
            _context = context;
            _configuration = configuration;
        }

        /// <summary>
        /// Login endpoint - returns JWT access token and refresh token
        /// </summary>
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginRequest request)
        {
            if (!ModelState.IsValid)
                return ValidationError();

            // TODO: Replace with actual authentication against Users table
            // For now, using simple demo authentication
            if (request.Username == "admin" && request.Password == "admin123")
            {
                var userId = "1";
                var username = request.Username;
                var roles = new List<string> { "Admin", "User" };

                // Generate tokens
                var accessToken = _jwtService.GenerateAccessToken(userId, username, roles);
                var refreshToken = _jwtService.GenerateRefreshToken();

                // Store refresh token in database
                var refreshTokenExpiryDays = int.Parse(_configuration["JwtSettings:RefreshTokenExpirationDays"] ?? "7");
                var refreshTokenEntity = new RefreshToken
                {
                    Token = refreshToken,
                    UserId = userId,
                    ExpiresAt = DateTime.UtcNow.AddDays(refreshTokenExpiryDays),
                    CreatedAt = DateTime.UtcNow,
                    IsRevoked = false
                };

                _context.RefreshTokens.Add(refreshTokenEntity);
                await _context.SaveChangesAsync();

                return Success(new
                {
                    accessToken,
                    refreshToken,
                    expiresIn = int.Parse(_configuration["JwtSettings:TokenExpirationMinutes"] ?? "60") * 60, // seconds
                    tokenType = "Bearer",
                    user = new
                    {
                        id = userId,
                        username,
                        roles
                    }
                }, "Login successful");
            }

            return Error("Invalid username or password", null, 401);
        }

        /// <summary>
        /// Refresh token endpoint - returns new access token using refresh token
        /// </summary>
        [HttpPost("refresh")]
        public async Task<IActionResult> Refresh([FromBody] RefreshTokenRequest request)
        {
            if (string.IsNullOrEmpty(request.RefreshToken))
                return ValidationError("Refresh token is required");

            // Validate the refresh token
            var storedToken = await _context.RefreshTokens
                .FirstOrDefaultAsync(rt => rt.Token == request.RefreshToken && rt.IsRevoked == false);

            if (storedToken == null)
                return Error("Invalid refresh token", null, 401);

            if (storedToken.IsExpired)
                return Error("Refresh token has expired", null, 401);

            // Extract claims from the expired access token
            var principal = _jwtService.GetPrincipalFromExpiredToken(request.AccessToken);
            if (principal == null)
                return Error("Invalid access token", null, 401);

            var userId = principal.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            var username = principal.FindFirst(ClaimTypes.Name)?.Value;
            var roles = principal.FindAll(ClaimTypes.Role).Select(c => c.Value).ToList();

            if (userId != storedToken.UserId)
                return Error("Token mismatch", null, 401);

            // Generate new tokens
            var newAccessToken = _jwtService.GenerateAccessToken(userId, username ?? "", roles);
            var newRefreshToken = _jwtService.GenerateRefreshToken();

            // Revoke old refresh token
            storedToken.IsRevoked = true;
            storedToken.RevokedAt = DateTime.UtcNow;

            // Store new refresh token
            var refreshTokenExpiryDays = int.Parse(_configuration["JwtSettings:RefreshTokenExpirationDays"] ?? "7");
            var newRefreshTokenEntity = new RefreshToken
            {
                Token = newRefreshToken,
                UserId = userId ?? "",
                ExpiresAt = DateTime.UtcNow.AddDays(refreshTokenExpiryDays),
                CreatedAt = DateTime.UtcNow,
                IsRevoked = false
            };

            _context.RefreshTokens.Add(newRefreshTokenEntity);
            await _context.SaveChangesAsync();

            return Success(new
            {
                accessToken = newAccessToken,
                refreshToken = newRefreshToken,
                expiresIn = int.Parse(_configuration["JwtSettings:TokenExpirationMinutes"] ?? "60") * 60,
                tokenType = "Bearer"
            }, "Token refreshed successfully");
        }

        /// <summary>
        /// Logout endpoint - revokes refresh token
        /// </summary>
        [HttpPost("logout")]
        [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
        public async Task<IActionResult> Logout([FromBody] LogoutRequest request)
        {
            if (string.IsNullOrEmpty(request.RefreshToken))
                return ValidationError("Refresh token is required");

            var storedToken = await _context.RefreshTokens
                .FirstOrDefaultAsync(rt => rt.Token == request.RefreshToken);

            if (storedToken != null && !storedToken.IsRevoked)
            {
                storedToken.IsRevoked = true;
                storedToken.RevokedAt = DateTime.UtcNow;
                await _context.SaveChangesAsync();
            }

            return Success("Logged out successfully");
        }

        /// <summary>
        /// Get current user info from JWT token
        /// </summary>
        [HttpGet("me")]
        [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
        public IActionResult GetCurrentUser()
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            var username = User.FindFirst(ClaimTypes.Name)?.Value;
            var roles = User.FindAll(ClaimTypes.Role).Select(c => c.Value).ToList();

            return Success(new
            {
                id = userId,
                username,
                roles
            });
        }
    }

    // DTOs for authentication requests
    public class LoginRequest
    {
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }

    public class RefreshTokenRequest
    {
        public string AccessToken { get; set; } = string.Empty;
        public string RefreshToken { get; set; } = string.Empty;
    }

    public class LogoutRequest
    {
        public string RefreshToken { get; set; } = string.Empty;
    }
}
