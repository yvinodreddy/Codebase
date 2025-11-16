USE RMMS_Production;
GO

PRINT '🚀 Starting COMPREHENSIVE Phase 4 data seeding...';
PRINT 'Target: 40+ records per table for complete testing';
PRINT '';

-- ============================================================
-- 1. SEED API KEYS (50 records)
-- ============================================================
PRINT '📊 Seeding API Keys (50 records)...';

DELETE FROM ApiKeys;

DECLARE @i INT = 1;
DECLARE @now DATETIME = GETDATE();

WHILE @i <= 50
BEGIN
    INSERT INTO ApiKeys (
        Name, Description, KeyValue, UserId, 
        ExpiresAt, IsActive, RequestCount, RateLimit, 
        LastUsed, Permissions, CreatedBy, CreatedDate
    )
    VALUES (
        'API Key ' + CAST(@i AS VARCHAR),
        'Test API key #' + CAST(@i AS VARCHAR) + ' for development and testing',
        'key_' + CAST(NEWID() AS VARCHAR(50)),
        'user_' + CAST(@i AS VARCHAR),
        CASE 
            WHEN @i % 10 = 0 THEN DATEADD(day, -5, @now)
            WHEN @i % 5 = 0 THEN DATEADD(month, 1, @now)
            ELSE DATEADD(year, 1, @now)
        END,
        CASE WHEN @i % 7 = 0 THEN 0 ELSE 1 END,
        CAST(RAND(CHECKSUM(NEWID())) * 10000 AS INT),
        CASE 
            WHEN @i % 3 = 0 THEN 1000
            WHEN @i % 3 = 1 THEN 5000
            ELSE 10000
        END,
        CASE 
            WHEN @i % 4 = 0 THEN NULL
            ELSE DATEADD(minute, -CAST(RAND(CHECKSUM(NEWID())) * 1440 AS INT), @now)
        END,
        CASE 
            WHEN @i % 4 = 0 THEN 'read'
            WHEN @i % 4 = 1 THEN 'read,write'
            WHEN @i % 4 = 2 THEN 'read,write,delete'
            ELSE 'admin'
        END,
        'admin',
        DATEADD(day, -@i, @now)
    );
    
    SET @i = @i + 1;
END

PRINT '   ✓ Seeded 50 API Keys';
PRINT '';

-- ============================================================
-- 2. SEED API ANALYTICS (1000 records)
-- ============================================================
PRINT '📊 Seeding API Analytics (1000 records)...';

DELETE FROM ApiAnalytics;

DECLARE @j INT = 1;
DECLARE @now2 DATETIME = GETDATE();

WHILE @j <= 1000
BEGIN
    DECLARE @endpoint VARCHAR(100) = CASE (@j % 10)
        WHEN 0 THEN '/api/products'
        WHEN 1 THEN '/api/customers'
        WHEN 2 THEN '/api/orders'
        WHEN 3 THEN '/api/inventory'
        WHEN 4 THEN '/api/reports/sales'
        WHEN 5 THEN '/api/reports/production'
        WHEN 6 THEN '/api/auth/login'
        WHEN 7 THEN '/api/users'
        WHEN 8 THEN '/api/analytics'
        ELSE '/api/dashboard'
    END;
    
    DECLARE @statusCode INT = CASE 
        WHEN (@j % 10) = 0 THEN 404
        WHEN (@j % 20) = 0 THEN 500
        WHEN (@j % 15) = 0 THEN 400
        ELSE 200
    END;
    
    DECLARE @responseTime INT = CASE
        WHEN @endpoint LIKE '%reports%' THEN 300 + (@j % 500)
        WHEN @endpoint LIKE '%dashboard%' THEN 100 + (@j % 200)
        ELSE 50 + (@j % 150)
    END;
    
    INSERT INTO ApiAnalytics (
        Endpoint, Method, StatusCode, ResponseTime,
        IpAddress, UserAgent, RequestedAt, ErrorMessage,
        CreatedDate, IsActive
    )
    VALUES (
        @endpoint,
        CASE (@j % 4)
            WHEN 0 THEN 'GET'
            WHEN 1 THEN 'POST'
            WHEN 2 THEN 'PUT'
            ELSE 'DELETE'
        END,
        @statusCode,
        @responseTime,
        '192.168.' + CAST((@j % 255) AS VARCHAR) + '.' + CAST(((@j * 17) % 255) AS VARCHAR),
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        DATEADD(minute, -(@j * 2), @now2),
        CASE WHEN @statusCode >= 400 THEN 'Error message for status ' + CAST(@statusCode AS VARCHAR) ELSE NULL END,
        DATEADD(minute, -(@j * 2), @now2),
        1
    );
    
    SET @j = @j + 1;
END

PRINT '   ✓ Seeded 1000 API Analytics records';
PRINT '';

PRINT '============================================================';
PRINT '✅ SEEDING PHASE 1 COMPLETE (API Keys + Analytics)';
PRINT '============================================================';
PRINT '';
PRINT 'Continuing with Webhooks, Integrations, and Mobile data...';

GO
