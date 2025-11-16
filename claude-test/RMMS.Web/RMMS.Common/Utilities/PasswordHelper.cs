// RMMS.Common/Utilities/PasswordHelper.cs
using System;
using System.Security.Cryptography;
using System.Text;

namespace RMMS.Common.Utilities
{
    public static class PasswordHelper
    {
        // Using BCrypt.Net-Next NuGet package is recommended for production
        // Install-Package BCrypt.Net-Next

        public static string HashPassword(string password)
        {
            return BCrypt.Net.BCrypt.HashPassword(password, 11);
        }

        public static bool VerifyPassword(string password, string hashedPassword)
        {
            return BCrypt.Net.BCrypt.Verify(password, hashedPassword);
        }

        // Alternative: Simple SHA256 (not recommended for production)
        public static string HashPasswordSHA256(string password)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] hashedBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(hashedBytes);
            }
        }
    }
}