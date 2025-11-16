-- RMMS Implementation Tracking Tables
-- Run this script first to enable progress tracking
-- Database: RMMS_Production

USE RMMS_Production;
GO

-- Check if tables exist and create if not
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ImplementationProgress')
BEGIN
    CREATE TABLE ImplementationProgress (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        StepNumber VARCHAR(20) NOT NULL,
        StepName VARCHAR(200) NOT NULL,
        Status VARCHAR(20) NOT NULL, -- NotStarted, InProgress, Completed, Blocked
        StartedDate DATETIME,
        CompletedDate DATETIME,
        CompletedBy VARCHAR(100),
        Notes VARCHAR(MAX),
        GitCommitHash VARCHAR(50),
        CreatedDate DATETIME DEFAULT GETDATE()
    );

    PRINT 'Table ImplementationProgress created successfully.';
END
ELSE
BEGIN
    PRINT 'Table ImplementationProgress already exists.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SessionLog')
BEGIN
    CREATE TABLE SessionLog (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        SessionDate DATE NOT NULL,
        StartTime DATETIME NOT NULL,
        EndTime DATETIME,
        WorkCompleted VARCHAR(MAX),
        NextSteps VARCHAR(MAX),
        BlockersIssues VARCHAR(MAX),
        CreatedBy VARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE()
    );

    PRINT 'Table SessionLog created successfully.';
END
ELSE
BEGIN
    PRINT 'Table SessionLog already exists.';
END
GO

-- Insert initial tracking entry
IF NOT EXISTS (SELECT * FROM ImplementationProgress WHERE StepNumber = 'INIT')
BEGIN
    INSERT INTO ImplementationProgress (StepNumber, StepName, Status, StartedDate, CompletedDate, CompletedBy, Notes)
    VALUES ('INIT', 'Implementation System Initialized', 'Completed', GETDATE(), GETDATE(), SYSTEM_USER, 'Tracking tables created and ready');

    PRINT 'Initial tracking entry created.';
END
GO

-- Insert first session log
INSERT INTO SessionLog (SessionDate, StartTime, CreatedBy, WorkCompleted, NextSteps)
VALUES (
    CAST(GETDATE() AS DATE),
    GETDATE(),
    SYSTEM_USER,
    'Created tracking tables for implementation progress',
    'Begin Phase 1 Sprint 1: Master Data Implementation'
);
GO

-- Verify tables created
SELECT 'ImplementationProgress Table' AS TableName, COUNT(*) AS RecordCount FROM ImplementationProgress
UNION ALL
SELECT 'SessionLog Table', COUNT(*) FROM SessionLog;
GO

PRINT 'Database tracking setup completed successfully!';
PRINT 'You can now track implementation progress in these tables.';
GO
