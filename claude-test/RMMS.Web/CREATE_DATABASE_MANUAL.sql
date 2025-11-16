-- ============================================
-- Manual Database Creation Script
-- ============================================
-- This script must be run by a user with CREATE DATABASE permissions (like 'sa')
-- Run this in SQL Server Management Studio or using sqlcmd as administrator

USE master;
GO

-- Create the database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RMMS_Production')
BEGIN
    CREATE DATABASE RMMS_Production;
    PRINT 'Database RMMS_Production created successfully';
END
ELSE
BEGIN
    PRINT 'Database RMMS_Production already exists';
END
GO

-- Grant access to rmms_user
USE RMMS_Production;
GO

-- Create user if doesn't exist and grant permissions
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'rmms_user')
BEGIN
    CREATE USER [rmms_user] FOR LOGIN [rmms_user];
    PRINT 'User rmms_user created';
END
GO

-- Grant necessary permissions
ALTER ROLE db_owner ADD MEMBER [rmms_user];
GO

PRINT 'Database setup complete. rmms_user now has full access to RMMS_Production';
GO
