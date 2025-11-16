-- ============================================================
-- PHASE 4: JWT AUTHENTICATION - REFRESH TOKENS TABLE
-- ============================================================
-- This script creates the RefreshTokens table for JWT authentication
-- Execute this script on the RMMS_Production database

USE RMMS_Production;
GO

-- Check if table already exists
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RefreshTokens')
BEGIN
    CREATE TABLE RefreshTokens (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Token NVARCHAR(500) NOT NULL,
        UserId NVARCHAR(100) NOT NULL,
        ExpiresAt DATETIME2 NOT NULL,
        CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
        RevokedAt DATETIME2 NULL,
        IsRevoked BIT NOT NULL DEFAULT 0
    );

    -- Create indexes for performance
    CREATE INDEX IX_RefreshTokens_Token ON RefreshTokens(Token);
    CREATE INDEX IX_RefreshTokens_UserId ON RefreshTokens(UserId);
    CREATE INDEX IX_RefreshTokens_ExpiresAt ON RefreshTokens(ExpiresAt);

    PRINT 'RefreshTokens table created successfully';
END
ELSE
BEGIN
    PRINT 'RefreshTokens table already exists';
END
GO

-- Verify table creation
SELECT
    t.name AS TableName,
    c.name AS ColumnName,
    ty.name AS DataType,
    c.max_length,
    c.is_nullable
FROM sys.tables t
INNER JOIN sys.columns c ON t.object_id = c.object_id
INNER JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE t.name = 'RefreshTokens'
ORDER BY c.column_id;
GO

-- Display indexes
SELECT
    i.name AS IndexName,
    i.type_desc AS IndexType,
    COL_NAME(ic.object_id, ic.column_id) AS ColumnName
FROM sys.indexes i
INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
WHERE i.object_id = OBJECT_ID('RefreshTokens')
ORDER BY i.name, ic.key_ordinal;
GO

PRINT 'Phase 4: RefreshTokens table setup complete';
