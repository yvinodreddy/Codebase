using BCrypt.Net;
using FHIRHealthcareAPI.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Manages user authentication and authorization
    /// </summary>
    public class UserService
    {
        private readonly IConfiguration _configuration;
        private readonly JwtSettings _jwtSettings;

        // In production, this would be a database. For now, we'll use in-memory storage
        private static readonly List<User> _users = new();
        private static int _nextId = 1;

        public UserService(IConfiguration configuration)
        {
            _configuration = configuration;
            _jwtSettings = configuration.GetSection("JwtSettings").Get<JwtSettings>();

            // Add debugging here too
            Console.WriteLine($"📋 UserService Init - SecretKey: {_jwtSettings?.SecretKey}");
            Console.WriteLine($"📋 UserService Init - Issuer: {_jwtSettings?.Issuer}");

            // Seed with test users if empty
            if (!_users.Any())
            {
                SeedTestUsers();
            }
        }

        /// <summary>
        /// Creates initial test users for development
        /// </summary>
        private void SeedTestUsers()
        {
            // Create a test doctor
            _users.Add(new User
            {
                Id = _nextId++,
                Username = "dr.smith",
                Email = "smith@hospital.com",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword("Doctor123!"),
                FirstName = "John",
                LastName = "Smith",
                Role = UserRoles.Doctor,
                LicenseNumber = "MD12345",
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            });

            // Create a test nurse
            _users.Add(new User
            {
                Id = _nextId++,
                Username = "nurse.johnson",
                Email = "johnson@hospital.com",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword("Nurse123!"),
                FirstName = "Mary",
                LastName = "Johnson",
                Role = UserRoles.Nurse,
                LicenseNumber = "RN67890",
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            });

            // Create a test patient
            _users.Add(new User
            {
                Id = _nextId++,
                Username = "patient.williams",
                Email = "williams@email.com",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword("Patient123!"),
                FirstName = "Robert",
                LastName = "Williams",
                Role = UserRoles.Patient,
                FhirPatientId = "1",  // Links to FHIR Patient resource
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            });

            // Create an admin
            _users.Add(new User
            {
                Id = _nextId++,
                Username = "admin",
                Email = "admin@hospital.com",
                PasswordHash = BCrypt.Net.BCrypt.HashPassword("Admin123!"),
                FirstName = "System",
                LastName = "Administrator",
                Role = UserRoles.Admin,
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            });
        }

        /// <summary>
        /// Authenticates a user and returns a JWT token if successful
        /// </summary>
        public async Task<(bool Success, string Token, string Message, User User)> AuthenticateAsync(
            string username, string password)
        {
            // Find user by username
            var user = _users.FirstOrDefault(u =>
                u.Username.Equals(username, StringComparison.OrdinalIgnoreCase));

            if (user == null)
            {
                // Don't reveal whether username exists (security best practice)
                return (false, null, "Invalid username or password", null);
            }

            // Check if account is locked
            if (user.LockedUntil.HasValue && user.LockedUntil > DateTime.UtcNow)
            {
                var remainingTime = (user.LockedUntil.Value - DateTime.UtcNow).TotalMinutes;
                return (false, null, $"Account locked. Try again in {Math.Ceiling(remainingTime)} minutes", null);
            }

            // Check if account is active
            if (!user.IsActive)
            {
                return (false, null, "Account is disabled. Contact administrator", null);
            }

            // Verify password
            if (!BCrypt.Net.BCrypt.Verify(password, user.PasswordHash))
            {
                // Track failed attempts
                user.FailedLoginAttempts++;

                // Lock account after 5 failed attempts
                if (user.FailedLoginAttempts >= 5)
                {
                    user.LockedUntil = DateTime.UtcNow.AddMinutes(30);
                    return (false, null, "Account locked due to multiple failed attempts", null);
                }

                return (false, null, "Invalid username or password", null);
            }

            // Reset failed attempts on successful login
            user.FailedLoginAttempts = 0;
            user.LockedUntil = null;
            user.LastLogin = DateTime.UtcNow;

            // Generate JWT token
            var token = GenerateJwtToken(user);

            return (true, token, "Authentication successful", user);
        }

        /// <summary>
        /// Generates a JWT token for an authenticated user
        /// </summary>
        private string GenerateJwtToken(User user)
        {
            var tokenHandler = new JwtSecurityTokenHandler();
            //var key = Encoding.ASCII.GetBytes(_jwtSettings.SecretKey); 
            Console.WriteLine($"🔑 UserService - SecretKey: {_jwtSettings.SecretKey}");
            Console.WriteLine($"🔑 UserService - Issuer: {_jwtSettings.Issuer}");
            Console.WriteLine($"🔑 UserService - Audience: {_jwtSettings.Audience}");
            var key = Encoding.UTF8.GetBytes(_jwtSettings.SecretKey); // Should be UTF8, not ASCII

            Console.WriteLine($"🔑 UserService - Key Length: {key.Length} bytes");

            // Define claims (user information embedded in token)
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Email, user.Email),
                new Claim(ClaimTypes.Role, user.Role),
                new Claim("FullName", $"{user.FirstName} {user.LastName}"),
                new Claim("IsActive", user.IsActive.ToString())
            };

            // Add license number for medical professionals
            if (!string.IsNullOrEmpty(user.LicenseNumber))
            {
                claims.Add(new Claim("LicenseNumber", user.LicenseNumber));
            }

            // Add FHIR Patient ID for patients
            if (!string.IsNullOrEmpty(user.FhirPatientId))
            {
                claims.Add(new Claim("FhirPatientId", user.FhirPatientId));
            }

            // Add permissions based on role
            var permissions = UserRoles.RolePermissions[user.Role];
            foreach (var permission in permissions)
            {
                claims.Add(new Claim("Permission", permission));
            }

            // Create token descriptor
            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Subject = new ClaimsIdentity(claims),
                Expires = DateTime.UtcNow.AddMinutes(_jwtSettings.ExpirationMinutes),
                Issuer = _jwtSettings.Issuer,
                Audience = _jwtSettings.Audience,
                SigningCredentials = new SigningCredentials(
                    new SymmetricSecurityKey(key),
                    SecurityAlgorithms.HmacSha256Signature)
            };

            // Create and return token
            var token = tokenHandler.CreateToken(tokenDescriptor);
            return tokenHandler.WriteToken(token);
        }

        /// <summary>
        /// Registers a new user in the system
        /// </summary>
        public async Task<(bool Success, string Message, User User)> RegisterAsync(
            string username, string email, string password, string firstName,
            string lastName, string role, string licenseNumber = null)
        {
            // Validate username is unique
            if (_users.Any(u => u.Username.Equals(username, StringComparison.OrdinalIgnoreCase)))
            {
                return (false, "Username already exists", null);
            }

            // Validate email is unique
            if (_users.Any(u => u.Email.Equals(email, StringComparison.OrdinalIgnoreCase)))
            {
                return (false, "Email already registered", null);
            }

            // Validate password strength
            if (password.Length < 8 || !password.Any(char.IsDigit) || !password.Any(char.IsUpper))
            {
                return (false, "Password must be at least 8 characters with numbers and uppercase", null);
            }

            // Validate role
            if (!new[] { UserRoles.Doctor, UserRoles.Nurse, UserRoles.Patient }.Contains(role))
            {
                return (false, "Invalid role specified", null);
            }

            // Create new user
            var user = new User
            {
                Id = _nextId++,
                Username = username,
                Email = email,
                PasswordHash = BCrypt.Net.BCrypt.HashPassword(password),
                FirstName = firstName,
                LastName = lastName,
                Role = role,
                LicenseNumber = licenseNumber,
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            };

            _users.Add(user);

            return (true, "User registered successfully", user);
        }

        /// <summary>
        /// Gets a user by their ID
        /// </summary>
        public async Task<User> GetUserByIdAsync(int userId)
        {
            return _users.FirstOrDefault(u => u.Id == userId);
        }
    }
}