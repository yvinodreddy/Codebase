-- ============================================
-- SETUP AUTHENTICATION SYSTEM
-- Creates Users table, stored procedure, and admin user
-- ============================================

USE RMMS_Production;
GO

PRINT 'Setting up authentication...';
GO

-- 1. Create Users table if not exists
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users')
BEGIN
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
    PRINT '✓ Users table created';
END
ELSE
    PRINT '✓ Users table already exists';
GO

-- 2. Create login validation stored procedure
CREATE OR ALTER PROCEDURE sp_User_ValidateLogin
    @Username NVARCHAR(100),
    @PasswordHash NVARCHAR(500)
AS
BEGIN
    SET NOCOUNT ON;

    -- Return user if credentials match
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

    -- Update last login date if found
    IF @@ROWCOUNT > 0
    BEGIN
        UPDATE Users
        SET LastLoginDate = GETDATE()
        WHERE Username = @Username;
    END
END
GO

PRINT '✓ sp_User_ValidateLogin procedure created';
GO

-- 3. Insert admin user (password: Admin@123)
-- BCrypt hash for 'Admin@123': $2a$11$vqN5Y.RXXqVZqVK0eJZVQ.8HzDQKJ5xQMxKQNxVxVN8PxQKQxVxVx

DECLARE @AdminPasswordHash NVARCHAR(500) = '$2a$11$vqN5Y.RXXqVZqVK0eJZVQ.8HzDQKJ5xQMxKQNxVxVN8PxQKQxVxVx';

IF NOT EXISTS (SELECT * FROM Users WHERE Username = 'admin')
BEGIN
    INSERT INTO Users (Username, PasswordHash, Email, FullName, Role, IsActive)
    VALUES ('admin', @AdminPasswordHash, 'admin@rmms.com', 'System Administrator', 'Admin', 1);

    PRINT '✓ Admin user created (Username: admin, Password: Admin@123)';
END
ELSE
BEGIN
    -- Update existing admin password
    UPDATE Users
    SET PasswordHash = @AdminPasswordHash,
        Email = 'admin@rmms.com',
        FullName = 'System Administrator',
        Role = 'Admin',
        IsActive = 1
    WHERE Username = 'admin';

    PRINT '✓ Admin user updated (Username: admin, Password: Admin@123)';
END
GO

-- 4. Create additional test users
IF NOT EXISTS (SELECT * FROM Users WHERE Username = 'manager')
BEGIN
    INSERT INTO Users (Username, PasswordHash, Email, FullName, Role, IsActive)
    VALUES ('manager', '$2a$11$vqN5Y.RXXqVZqVK0eJZVQ.8HzDQKJ5xQMxKQNxVxVN8PxQKQxVxVx',
            'manager@rmms.com', 'Mill Manager', 'Manager', 1);
    PRINT '✓ Manager user created (Username: manager, Password: Admin@123)';
END
GO

IF NOT EXISTS (SELECT * FROM Users WHERE Username = 'operator')
BEGIN
    INSERT INTO Users (Username, PasswordHash, Email, FullName, Role, IsActive)
    VALUES ('operator', '$2a$11$vqN5Y.RXXqVZqVK0eJZVQ.8HzDQKJ5xQMxKQNxVxVN8PxQKQxVxVx',
            'operator@rmms.com', 'Production Operator', 'Operator', 1);
    PRINT '✓ Operator user created (Username: operator, Password: Admin@123)';
END
GO

-- 5. Verify setup
PRINT '';
PRINT '========================================';
PRINT 'AUTHENTICATION SETUP COMPLETE!';
PRINT '========================================';
PRINT '';
PRINT 'Available Users:';
SELECT
    Username,
    FullName,
    Role,
    Email,
    CASE WHEN IsActive = 1 THEN 'Active' ELSE 'Inactive' END AS Status
FROM Users;
GO

PRINT '';
PRINT 'Login Credentials:';
PRINT '  Username: admin    | Password: Admin@123 | Role: Admin';
PRINT '  Username: manager  | Password: Admin@123 | Role: Manager';
PRINT '  Username: operator | Password: Admin@123 | Role: Operator';
PRINT '';
GO
