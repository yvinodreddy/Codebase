-- Create database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RMMS_Production')
BEGIN
    CREATE DATABASE RMMS_Production;
    PRINT 'Database RMMS_Production created successfully.';
END
ELSE
BEGIN
    PRINT 'Database RMMS_Production already exists.';
END
GO
