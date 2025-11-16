#!/usr/bin/env dotnet-script
#r "nuget: BCrypt.Net-Next, 4.0.3"
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using System;
using System.Data;
using Microsoft.Data.SqlClient;
using BCrypt.Net;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

Console.WriteLine("========================================");
Console.WriteLine("CREATING USERS WITH PROPER BCRYPT HASHES");
Console.WriteLine("========================================\n");

// Password to hash
var password = "Admin@123";

// Generate BCrypt hash for the password
Console.WriteLine($"Generating BCrypt hash for password: {password}");
var passwordHash = BCrypt.Net.BCrypt.HashPassword(password);
Console.WriteLine($"Generated hash: {passwordHash}\n");

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("✓ Connected to database\n");

    // Check if Users table exists
    var checkTableCmd = new SqlCommand(@"
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = 'Users'
    ", connection);

    var tableExists = (int)checkTableCmd.ExecuteScalar() > 0;

    if (!tableExists)
    {
        Console.WriteLine("Creating Users table...");
        var createTableCmd = new SqlCommand(@"
            CREATE TABLE Users (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                Username NVARCHAR(100) NOT NULL UNIQUE,
                PasswordHash NVARCHAR(500) NOT NULL,
                Email NVARCHAR(200),
                FullName NVARCHAR(200),
                Role NVARCHAR(50) NOT NULL DEFAULT 'User',
                IsActive BIT NOT NULL DEFAULT 1,
                CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
                LastLoginDate DATETIME2 NULL
            );
        ", connection);
        createTableCmd.ExecuteNonQuery();
        Console.WriteLine("✓ Users table created\n");
    }

    // Create or update stored procedure
    Console.WriteLine("Creating/updating sp_User_ValidateLogin...");
    var createProcCmd = new SqlCommand(@"
        IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_User_ValidateLogin')
            DROP PROCEDURE sp_User_ValidateLogin;
    ", connection);
    createProcCmd.ExecuteNonQuery();

    createProcCmd = new SqlCommand(@"
        CREATE PROCEDURE sp_User_ValidateLogin
            @Username NVARCHAR(100),
            @PasswordHash NVARCHAR(500)
        AS
        BEGIN
            SET NOCOUNT ON;

            SELECT
                Id,
                Username,
                Email,
                FullName,
                Role
            FROM Users
            WHERE Username = @Username
                AND PasswordHash = @PasswordHash
                AND IsActive = 1;

            IF @@ROWCOUNT > 0
            BEGIN
                UPDATE Users
                SET LastLoginDate = GETDATE()
                WHERE Username = @Username;
            END
        END
    ", connection);
    createProcCmd.ExecuteNonQuery();
    Console.WriteLine("✓ sp_User_ValidateLogin created\n");

    // Define users to create
    var users = new[]
    {
        new { Username = "admin", Email = "admin@rmms.com", FullName = "System Administrator", Role = "Admin" },
        new { Username = "manager", Email = "manager@rmms.com", FullName = "Mill Manager", Role = "Manager" },
        new { Username = "operator", Email = "operator@rmms.com", FullName = "Production Operator", Role = "Operator" }
    };

    Console.WriteLine("Creating/updating users...\n");

    foreach (var user in users)
    {
        // Check if user exists
        var checkCmd = new SqlCommand(
            "SELECT COUNT(*) FROM Users WHERE Username = @Username",
            connection
        );
        checkCmd.Parameters.AddWithValue("@Username", user.Username);

        var userExists = (int)checkCmd.ExecuteScalar() > 0;

        if (userExists)
        {
            // Update existing user
            var updateCmd = new SqlCommand(@"
                UPDATE Users
                SET PasswordHash = @PasswordHash,
                    Email = @Email,
                    FullName = @FullName,
                    Role = @Role,
                    IsActive = 1
                WHERE Username = @Username
            ", connection);

            updateCmd.Parameters.AddWithValue("@Username", user.Username);
            updateCmd.Parameters.AddWithValue("@PasswordHash", passwordHash);
            updateCmd.Parameters.AddWithValue("@Email", user.Email);
            updateCmd.Parameters.AddWithValue("@FullName", user.FullName);
            updateCmd.Parameters.AddWithValue("@Role", user.Role);

            updateCmd.ExecuteNonQuery();
            Console.WriteLine($"✓ Updated user: {user.Username,-12} | {user.FullName,-30} | Role: {user.Role}");
        }
        else
        {
            // Insert new user
            var insertCmd = new SqlCommand(@"
                INSERT INTO Users (Username, PasswordHash, Email, FullName, Role, IsActive)
                VALUES (@Username, @PasswordHash, @Email, @FullName, @Role, 1)
            ", connection);

            insertCmd.Parameters.AddWithValue("@Username", user.Username);
            insertCmd.Parameters.AddWithValue("@PasswordHash", passwordHash);
            insertCmd.Parameters.AddWithValue("@Email", user.Email);
            insertCmd.Parameters.AddWithValue("@FullName", user.FullName);
            insertCmd.Parameters.AddWithValue("@Role", user.Role);

            insertCmd.ExecuteNonQuery();
            Console.WriteLine($"✓ Created user: {user.Username,-12} | {user.FullName,-30} | Role: {user.Role}");
        }
    }

    Console.WriteLine("\n========================================");
    Console.WriteLine("USERS CREATED SUCCESSFULLY!");
    Console.WriteLine("========================================\n");

    // Verify users
    Console.WriteLine("Verifying users in database:\n");
    var verifyCmd = new SqlCommand(@"
        SELECT Username, FullName, Role, Email,
               CASE WHEN IsActive = 1 THEN 'Active' ELSE 'Inactive' END AS Status,
               LEFT(PasswordHash, 30) + '...' AS PasswordHashPreview
        FROM Users
        ORDER BY Id
    ", connection);

    using (var reader = verifyCmd.ExecuteReader())
    {
        Console.WriteLine("Username     | Full Name                      | Role        | Email                  | Status  | Password Hash Preview");
        Console.WriteLine("------------------------------------------------------------------------------------------------------------------------");

        while (reader.Read())
        {
            Console.WriteLine(
                $"{reader["Username"],-12} | " +
                $"{reader["FullName"],-30} | " +
                $"{reader["Role"],-11} | " +
                $"{reader["Email"],-22} | " +
                $"{reader["Status"],-7} | " +
                $"{reader["PasswordHashPreview"]}"
            );
        }
    }

    Console.WriteLine("\n========================================");
    Console.WriteLine("LOGIN CREDENTIALS:");
    Console.WriteLine("========================================");
    Console.WriteLine("  Username: admin    | Password: Admin@123 | Role: Admin");
    Console.WriteLine("  Username: manager  | Password: Admin@123 | Role: Manager");
    Console.WriteLine("  Username: operator | Password: Admin@123 | Role: Operator");
    Console.WriteLine("========================================\n");

    Console.WriteLine("✓ All users configured with BCrypt hashed passwords!");
    Console.WriteLine("✓ You can now login at: http://localhost:5090/Account/Login\n");
}
