using System.Security.Claims;

namespace RMMS.Services.Services.Authentication
{
    /// <summary>
    /// Interface for JWT token generation and validation
    /// </summary>
    public interface IJwtService
    {
        /// <summary>
        /// Generates a JWT access token for the specified user
        /// </summary>
        /// <param name="userId">User ID</param>
        /// <param name="username">Username</param>
        /// <param name="roles">List of user roles</param>
        /// <returns>JWT access token</returns>
        string GenerateAccessToken(string userId, string username, List<string> roles);

        /// <summary>
        /// Generates a cryptographically secure refresh token
        /// </summary>
        /// <returns>Refresh token</returns>
        string GenerateRefreshToken();

        /// <summary>
        /// Validates a JWT token
        /// </summary>
        /// <param name="token">Token to validate</param>
        /// <returns>Claims principal if valid, null otherwise</returns>
        ClaimsPrincipal? ValidateToken(string token);

        /// <summary>
        /// Extracts claims from an expired token (for refresh token flow)
        /// </summary>
        /// <param name="token">Expired token</param>
        /// <returns>Claims principal from expired token</returns>
        ClaimsPrincipal? GetPrincipalFromExpiredToken(string token);
    }
}
