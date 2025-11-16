-- ============================================================================
-- COMPREHENSIVE SEED DATA FOR PHASE 3 & PHASE 4 TABLES
-- This script populates all tables with realistic test data
-- ============================================================================

USE RMMS_Production;
GO

PRINT 'Starting comprehensive data seeding for Phase 3 & 4...';

-- ============================================================================
-- PHASE 4: API KEYS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM ApiKeys WHERE Name = 'Production API Key')
BEGIN
    INSERT INTO ApiKeys (Name, Description, KeyValue, UserId, ExpiresAt, IsActive, RequestCount, RateLimit, LastUsed, Permissions, CreatedBy, CreatedDate)
    VALUES
    ('Production API Key', 'Main production API key for external integrations', 'hashed_key_prod_12345', 'system', DATEADD(year, 1, GETDATE()), 1, 25432, 10000, DATEADD(hour, -2, GETDATE()), 'read,write,delete', 'admin', GETDATE()),
    ('Mobile App Key', 'API key for mobile applications', 'hashed_key_mobile_67890', 'mobile-app', DATEADD(month, 6, GETDATE()), 1, 15678, 5000, DATEADD(hour, -1, GETDATE()), 'read,write', 'admin', GETDATE()),
    ('Analytics Key', 'Read-only key for analytics and reporting', 'hashed_key_analytics_11111', 'analytics', DATEADD(month, 3, GETDATE()), 1, 4568, 2000, DATEADD(day, -1, GETDATE()), 'read', 'admin', GETDATE()),
    ('Test Key', 'Testing and development key', 'hashed_key_test_22222', 'test-user', DATEADD(month, 1, GETDATE()), 0, 0, 1000, NULL, 'read', 'admin', DATEADD(day, -30, GETDATE()));

    PRINT '✓ Seeded 4 API Keys';
END

-- ============================================================================
-- PHASE 4: API ANALYTICS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM ApiAnalytics WHERE Endpoint = '/api/Products')
BEGIN
    DECLARE @i INT = 0;
    DECLARE @endpoint VARCHAR(100);
    DECLARE @statusCode INT;
    DECLARE @responseTime INT;

    WHILE @i < 1000
    BEGIN
        -- Vary endpoints
        SET @endpoint = CASE (@i % 5)
            WHEN 0 THEN '/api/Products'
            WHEN 1 THEN '/api/Customers'
            WHEN 2 THEN '/api/Orders'
            WHEN 3 THEN '/api/Reports/Generate'
            ELSE '/api/Analytics/Stats'
        END;

        -- Vary status codes (95% success, 5% errors)
        SET @statusCode = CASE WHEN (@i % 20) = 0 THEN 404
                              WHEN (@i % 25) = 0 THEN 500
                              ELSE 200
                         END;

        -- Vary response times
        SET @responseTime = CASE
            WHEN @endpoint LIKE '%Reports%' THEN 500 + (@i % 500)
            ELSE 50 + (@i % 200)
        END;

        INSERT INTO ApiAnalytics (Endpoint, Method, StatusCode, ResponseTime, IpAddress, UserAgent, RequestedAt, ErrorMessage, CreatedDate, IsActive)
        VALUES (
            @endpoint,
            'GET',
            @statusCode,
            @responseTime,
            '192.168.1.' + CAST(100 + (@i % 50) AS VARCHAR),
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            DATEADD(minute, -@i, GETDATE()),
            CASE WHEN @statusCode >= 400 THEN 'Sample error message' ELSE NULL END,
            DATEADD(minute, -@i, GETDATE()),
            1
        );

        SET @i = @i + 1;
    END;

    PRINT '✓ Seeded 1000 API Analytics records';
END

-- ============================================================================
-- PHASE 4: MOBILE DEVICES
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM MobileDevices WHERE DeviceName = 'iPhone 13 Pro')
BEGIN
    INSERT INTO MobileDevices (DeviceId, DeviceName, Platform, AppVersion, PushToken, NotificationsEnabled, LastActiveAt, CreatedDate, IsActive)
    VALUES
    ('device_001', 'iPhone 13 Pro', 'iOS', '2.1.0', 'push_token_ios_001', 1, DATEADD(hour, -1, GETDATE()), GETDATE(), 1),
    ('device_002', 'Samsung Galaxy S21', 'Android', '2.1.0', 'push_token_android_002', 1, DATEADD(hour, -2, GETDATE()), GETDATE(), 1),
    ('device_003', 'iPad Pro', 'iOS', '2.0.5', 'push_token_ios_003', 0, DATEADD(day, -5, GETDATE()), DATEADD(day, -30, GETDATE()), 1),
    ('device_004', 'Google Pixel 6', 'Android', '2.1.0', 'push_token_android_004', 1, DATEADD(hour, -3, GETDATE()), DATEADD(day, -15, GETDATE()), 1);

    PRINT '✓ Seeded 4 Mobile Devices';
END

-- ============================================================================
-- PHASE 4: MOBILE ANALYTICS EVENTS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM MobileAnalyticsEvents WHERE EventName = 'screen_view')
BEGIN
    DECLARE @j INT = 0;
    DECLARE @deviceId VARCHAR(50);
    DECLARE @eventName VARCHAR(100);
    DECLARE @screenName VARCHAR(100);

    WHILE @j < 500
    BEGIN
        SET @deviceId = 'device_00' + CAST(1 + (@j % 4) AS VARCHAR);
        SET @eventName = CASE (@j % 4)
            WHEN 0 THEN 'screen_view'
            WHEN 1 THEN 'button_click'
            WHEN 2 THEN 'session_start'
            ELSE 'error_occurred'
        END;

        SET @screenName = CASE (@j % 5)
            WHEN 0 THEN 'Production'
            WHEN 1 THEN 'Dashboard'
            WHEN 2 THEN 'Orders'
            WHEN 3 THEN 'Analytics'
            ELSE 'Settings'
        END;

        INSERT INTO MobileAnalyticsEvents (DeviceId, EventName, EventCategory, ScreenName, EventData, Value, CreatedDate, IsActive)
        VALUES (
            @deviceId,
            @eventName,
            'User Interaction',
            @screenName,
            '{"action":"view","duration":' + CAST(30 + (@j % 120) AS VARCHAR) + '}',
            30 + (@j % 120),
            DATEADD(minute, -@j, GETDATE()),
            1
        );

        SET @j = @j + 1;
    END;

    PRINT '✓ Seeded 500 Mobile Analytics Events';
END

-- ============================================================================
-- PHASE 4: PUSH NOTIFICATIONS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM PushNotifications WHERE Title = 'Production Complete')
BEGIN
    INSERT INTO PushNotifications (Title, Body, TargetType, TargetValue, TargetDeviceCount, DeliveredCount, FailedCount, Status, SentAt, CreatedDate, CreatedBy, IsActive)
    VALUES
    ('Production Complete', 'Batch #12345 has been completed successfully', 'All', NULL, 4, 4, 0, 'Delivered', DATEADD(hour, -2, GETDATE()), DATEADD(hour, -2, GETDATE()), 'system', 1),
    ('Inventory Alert', 'Low stock alert for Premium Rice - 20 bags remaining', 'Android', NULL, 2, 2, 0, 'Delivered', DATEADD(hour, -5, GETDATE()), DATEADD(hour, -5, GETDATE()), 'system', 1),
    ('Order Confirmed', 'Your order #ORD-789 has been confirmed', 'User', 'device_001', 1, 1, 0, 'Delivered', DATEADD(day, -1, GETDATE()), DATEADD(day, -1, GETDATE()), 'system', 1),
    ('System Maintenance', 'Scheduled maintenance tonight at 10 PM', 'PushEnabled', NULL, 3, 2, 1, 'PartiallyFailed', DATEADD(day, -2, GETDATE()), DATEADD(day, -2, GETDATE()), 'admin', 1);

    PRINT '✓ Seeded 4 Push Notifications';
END

-- ============================================================================
-- PHASE 4: WEBHOOKS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM Webhooks WHERE Name = 'Production Alerts')
BEGIN
    INSERT INTO Webhooks (Name, Url, EventType, HttpMethod, Headers, IsActive, LastTriggeredAt, TimeoutSeconds, CreatedDate, CreatedBy)
    VALUES
    ('Production Alerts', 'https://api.example.com/webhooks/production', 'ProductionComplete', 'POST', '{"Authorization":"Bearer token123"}', 1, DATEADD(hour, -2, GETDATE()), 30, DATEADD(day, -30, GETDATE()), 'admin'),
    ('Order Notifications', 'https://api.example.com/webhooks/orders', 'OrderCreated', 'POST', '{"Authorization":"Bearer token456"}', 1, DATEADD(minute, -30, GETDATE()), 30, DATEADD(day, -20, GETDATE()), 'admin'),
    ('Inventory Alerts', 'https://api.example.com/webhooks/inventory', 'LowStock', 'POST', '{"Authorization":"Bearer token789"}', 1, DATEADD(hour, -5, GETDATE()), 30, DATEADD(day, -15, GETDATE()), 'admin'),
    ('Payment Received', 'https://api.example.com/webhooks/payments', 'PaymentReceived', 'POST', '{"Authorization":"Bearer tokenABC"}', 0, NULL, 30, DATEADD(day, -10, GETDATE()), 'admin'),
    ('All Events Monitor', 'https://api.example.com/webhooks/all', 'All', 'POST', '{"Authorization":"Bearer tokenXYZ"}', 1, DATEADD(minute, -5, GETDATE()), 60, DATEADD(day, -5, GETDATE()), 'admin');

    PRINT '✓ Seeded 5 Webhooks';
END

-- ============================================================================
-- PHASE 4: INTEGRATIONS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM Integrations WHERE Name = 'SAP ERP Integration')
BEGIN
    INSERT INTO Integrations (Name, Type, Endpoint, ApiKey, Status, LastSyncAt, ResponseTime, SuccessCount, FailureCount, ErrorMessage, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('SAP ERP Integration', 'ERP', 'https://sap.example.com/api', 'sap_key_12345', 'Connected', DATEADD(hour, -1, GETDATE()), 245, 1250, 3, NULL, 1, DATEADD(month, -6, GETDATE()), 'admin'),
    ('Salesforce CRM', 'CRM', 'https://salesforce.example.com/api', 'sf_key_67890', 'Connected', DATEADD(hour, -2, GETDATE()), 180, 892, 1, NULL, 1, DATEADD(month, -4, GETDATE()), 'admin'),
    ('QuickBooks Accounting', 'Accounting', 'https://quickbooks.example.com/api', 'qb_key_11111', 'Error', DATEADD(day, -2, GETDATE()), 0, 456, 23, 'Authentication failed - Token expired', 1, DATEADD(month, -3, GETDATE()), 'admin'),
    ('Shipping Provider API', 'Logistics', 'https://shipping.example.com/api', 'ship_key_22222', 'Connected', DATEADD(minute, -30, GETDATE()), 312, 2103, 5, NULL, 1, DATEADD(month, -2, GETDATE()), 'admin'),
    ('Payment Gateway', 'Payment', 'https://payment.example.com/api', 'pay_key_33333', 'Disconnected', DATEADD(day, -10, GETDATE()), 0, 0, 0, NULL, 0, DATEADD(month, -1, GETDATE()), 'admin');

    PRINT '✓ Seeded 5 Integrations';
END

-- ============================================================================
-- PHASE 4: REALTIME METRICS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM RealtimeMetrics)
BEGIN
    DECLARE @k INT = 0;
    WHILE @k < 100
    BEGIN
        INSERT INTO RealtimeMetrics (MetricType, Value, CreatedDate, IsActive)
        VALUES (
            CASE (@k % 3)
                WHEN 0 THEN 'API Request'
                WHEN 1 THEN 'Page Load'
                ELSE 'Database Query'
            END,
            50 + (@k % 200),
            DATEADD(second, -@k * 30, GETDATE()),
            1
        );
        SET @k = @k + 1;
    END;

    PRINT '✓ Seeded 100 Realtime Metrics';
END

-- ============================================================================
-- PHASE 3: MASTER DATA ENTITIES
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM MasterDataEntities WHERE EntityType = 'Product')
BEGIN
    INSERT INTO MasterDataEntities (EntityType, EntityId, EntityName, DataQualityScore, IsGoldenRecord, LastSyncedAt, CreatedDate, CreatedBy, IsActive)
    VALUES
    ('Product', 1, 'Premium Basmati Rice', 95, 1, DATEADD(hour, -3, GETDATE()), GETDATE(), 'admin', 1),
    ('Product', 2, 'Standard Rice', 88, 0, DATEADD(day, -1, GETDATE()), GETDATE(), 'admin', 1),
    ('Customer', 1, 'ABC Corp', 92, 1, DATEADD(hour, -2, GETDATE()), GETDATE(), 'admin', 1),
    ('Vendor', 1, 'Rice Supplier Ltd', 85, 0, DATEADD(day, -2, GETDATE()), GETDATE(), 'admin', 1);

    PRINT '✓ Seeded 4 Master Data Entities';
END

-- ============================================================================
-- PHASE 3: AUDIT TRAIL
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM AuditTrail WHERE EntityType = 'Product')
BEGIN
    DECLARE @m INT = 0;
    WHILE @m < 50
    BEGIN
        INSERT INTO AuditTrail (EntityType, EntityId, Action, OldValue, NewValue, UserId, IpAddress, CreatedDate, IsActive)
        VALUES (
            CASE (@m % 4)
                WHEN 0 THEN 'Product'
                WHEN 1 THEN 'Order'
                WHEN 2 THEN 'Customer'
                ELSE 'Invoice'
            END,
            1 + (@m % 10),
            CASE (@m % 3)
                WHEN 0 THEN 'Create'
                WHEN 1 THEN 'Update'
                ELSE 'Delete'
            END,
            CASE WHEN (@m % 3) = 1 THEN '{"price":100}' ELSE NULL END,
            CASE WHEN (@m % 3) = 1 THEN '{"price":120}' ELSE NULL END,
            'admin',
            '192.168.1.' + CAST(100 + (@m % 20) AS VARCHAR),
            DATEADD(hour, -@m, GETDATE()),
            1
        );
        SET @m = @m + 1;
    END;

    PRINT '✓ Seeded 50 Audit Trail records';
END

-- ============================================================================
-- PHASE 3: DATA VALIDATION RULES
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM DataValidationRules WHERE RuleName = 'Price Range Check')
BEGIN
    INSERT INTO DataValidationRules (RuleName, EntityType, FieldName, ValidationExpression, ErrorMessage, Severity, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('Price Range Check', 'Product', 'Price', 'value >= 0 AND value <= 10000', 'Price must be between 0 and 10000', 'Error', 1, GETDATE(), 'admin'),
    ('Email Format', 'Customer', 'Email', 'LIKE ''%@%.%''', 'Invalid email format', 'Warning', 1, GETDATE(), 'admin'),
    ('Quantity Positive', 'Order', 'Quantity', 'value > 0', 'Quantity must be greater than zero', 'Error', 1, GETDATE(), 'admin');

    PRINT '✓ Seeded 3 Data Validation Rules';
END

-- ============================================================================
-- PHASE 3: SCHEDULED REPORTS
-- ============================================================================
IF NOT EXISTS (SELECT 1 FROM ScheduledReports WHERE ReportName = 'Daily Sales Summary')
BEGIN
    INSERT INTO ScheduledReports (ReportName, ReportType, CronExpression, Recipients, LastExecutedAt, NextExecutionAt, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('Daily Sales Summary', 'Sales', '0 8 * * *', 'admin@example.com,manager@example.com', DATEADD(day, -1, GETDATE()), DATEADD(day, 1, GETDATE()), 1, GETDATE(), 'admin'),
    ('Weekly Inventory Report', 'Inventory', '0 9 * * 1', 'inventory@example.com', DATEADD(week, -1, GETDATE()), DATEADD(week, 1, GETDATE()), 1, GETDATE(), 'admin'),
    ('Monthly Financial Report', 'Financial', '0 0 1 * *', 'finance@example.com,cfo@example.com', DATEADD(month, -1, GETDATE()), DATEADD(month, 1, GETDATE()), 1, GETDATE(), 'admin');

    PRINT '✓ Seeded 3 Scheduled Reports';
END

PRINT '============================================================================';
PRINT '✓ SEED DATA COMPLETE - All Phase 3 & 4 tables populated';
PRINT '============================================================================';
GO
