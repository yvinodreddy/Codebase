#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Threading.Tasks;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;";

Console.WriteLine("🚀 Starting COMPREHENSIVE Phase 4 data seeding...");
Console.WriteLine("Target: 40+ records per table for complete testing\n");

try
{
    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();
    Console.WriteLine("✓ Database connected successfully\n");

    // ============================================================
    // 1. SEED API KEYS (50 records with realistic data)
    // ============================================================
    Console.WriteLine("📊 Seeding API Keys (50 records)...");
    await ExecuteSqlAsync(connection, @"
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
                    WHEN @i % 10 = 0 THEN DATEADD(day, -5, @now)  -- Some expired
                    WHEN @i % 5 = 0 THEN DATEADD(month, 1, @now)  -- Expiring soon
                    ELSE DATEADD(year, 1, @now)                   -- Valid for 1 year
                END,
                CASE WHEN @i % 7 = 0 THEN 0 ELSE 1 END,          -- Some inactive
                CAST(RAND(CHECKSUM(NEWID())) * 10000 AS INT),    -- Random request count
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
    ");
    Console.WriteLine("   ✓ Seeded 50 API Keys with varied usage patterns\n");

    // ============================================================
    // 2. SEED API ANALYTICS (1000 records for graphs)
    // ============================================================
    Console.WriteLine("📊 Seeding API Analytics (1000 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM ApiAnalytics;
        
        DECLARE @j INT = 1;
        DECLARE @now2 DATETIME = GETDATE();
        DECLARE @endpoint VARCHAR(100);
        DECLARE @statusCode INT;
        DECLARE @responseTime INT;
        
        WHILE @j <= 1000
        BEGIN
            -- Vary endpoints
            SET @endpoint = CASE (@j % 10)
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
            
            -- 90% success, 10% errors
            SET @statusCode = CASE 
                WHEN (@j % 10) = 0 THEN 404
                WHEN (@j % 20) = 0 THEN 500
                WHEN (@j % 15) = 0 THEN 400
                ELSE 200
            END;
            
            -- Vary response times
            SET @responseTime = CASE
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
    ");
    Console.WriteLine("   ✓ Seeded 1000 API Analytics records across 10 endpoints\n");

    // ============================================================
    // 3. SEED WEBHOOKS (50 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Webhooks (50 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM Webhooks;
        
        DECLARE @k INT = 1;
        DECLARE @now3 DATETIME = GETDATE();
        
        WHILE @k <= 50
        BEGIN
            INSERT INTO Webhooks (
                Name, Url, EventType, HttpMethod, Headers,
                IsActive, LastTriggeredAt, TimeoutSeconds,
                CreatedDate, CreatedBy
            )
            VALUES (
                'Webhook ' + CAST(@k AS VARCHAR),
                'https://api.example.com/webhooks/endpoint' + CAST(@k AS VARCHAR),
                CASE (@k % 10)
                    WHEN 0 THEN 'ProductionComplete'
                    WHEN 1 THEN 'OrderCreated'
                    WHEN 2 THEN 'OrderUpdated'
                    WHEN 3 THEN 'LowStock'
                    WHEN 4 THEN 'PaymentReceived'
                    WHEN 5 THEN 'ShipmentDispatched'
                    WHEN 6 THEN 'CustomerCreated'
                    WHEN 7 THEN 'InventoryUpdate'
                    WHEN 8 THEN 'BatchComplete'
                    ELSE 'All'
                END,
                CASE WHEN @k % 3 = 0 THEN 'PUT' ELSE 'POST' END,
                '{"Authorization":"Bearer token_' + CAST(@k AS VARCHAR) + '","Content-Type":"application/json"}',
                CASE WHEN @k % 6 = 0 THEN 0 ELSE 1 END,
                CASE 
                    WHEN @k % 5 = 0 THEN NULL
                    ELSE DATEADD(minute, -CAST(RAND(CHECKSUM(NEWID())) * 1440 AS INT), @now3)
                END,
                CASE 
                    WHEN @k % 3 = 0 THEN 60
                    WHEN @k % 3 = 1 THEN 30
                    ELSE 45
                END,
                DATEADD(day, -(@k % 30), @now3),
                'admin'
            );
            
            SET @k = @k + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 50 Webhooks with various event types\n");

    // ============================================================
    // 4. SEED INTEGRATIONS (50 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Integrations (50 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM Integrations;
        
        DECLARE @l INT = 1;
        DECLARE @now4 DATETIME = GETDATE();
        
        WHILE @l <= 50
        BEGIN
            DECLARE @status VARCHAR(20) = CASE (@l % 5)
                WHEN 0 THEN 'Error'
                WHEN 1 THEN 'Disconnected'
                ELSE 'Connected'
            END;
            
            INSERT INTO Integrations (
                Name, Type, Endpoint, ApiKey, Status,
                LastSyncAt, ResponseTime, SuccessCount, FailureCount,
                ErrorMessage, IsActive, CreatedDate, CreatedBy
            )
            VALUES (
                'Integration ' + CAST(@l AS VARCHAR),
                CASE (@l % 9)
                    WHEN 0 THEN 'ERP'
                    WHEN 1 THEN 'CRM'
                    WHEN 2 THEN 'Accounting'
                    WHEN 3 THEN 'Logistics'
                    WHEN 4 THEN 'Payment'
                    WHEN 5 THEN 'Warehouse'
                    WHEN 6 THEN 'Analytics'
                    WHEN 7 THEN 'Communication'
                    ELSE 'Other'
                END,
                'https://integration' + CAST(@l AS VARCHAR) + '.example.com/api',
                'apikey_' + CAST(NEWID() AS VARCHAR(50)),
                @status,
                CASE 
                    WHEN @status = 'Disconnected' THEN DATEADD(day, -10, @now4)
                    ELSE DATEADD(minute, -CAST(RAND(CHECKSUM(NEWID())) * 120 AS INT), @now4)
                END,
                CASE 
                    WHEN @status = 'Connected' THEN 150 + (@l % 300)
                    ELSE 0
                END,
                CASE 
                    WHEN @status = 'Connected' THEN 100 + (@l * 10)
                    ELSE @l * 5
                END,
                CASE 
                    WHEN @status = 'Error' THEN @l * 2
                    WHEN @status = 'Disconnected' THEN 0
                    ELSE @l
                END,
                CASE 
                    WHEN @status = 'Error' THEN 'Connection timeout - endpoint not responding'
                    WHEN @status = 'Disconnected' THEN 'Integration disabled by administrator'
                    ELSE NULL
                END,
                CASE WHEN @status = 'Disconnected' THEN 0 ELSE 1 END,
                DATEADD(day, -(@l % 60), @now4),
                'admin'
            );
            
            SET @l = @l + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 50 Integrations with mixed statuses\n");

    // ============================================================
    // 5. SEED MOBILE DEVICES (100 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Mobile Devices (100 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM MobileDevices;
        
        DECLARE @m INT = 1;
        DECLARE @now5 DATETIME = GETDATE();
        
        WHILE @m <= 100
        BEGIN
            DECLARE @platform VARCHAR(10) = CASE WHEN @m % 2 = 0 THEN 'Android' ELSE 'iOS' END;
            
            INSERT INTO MobileDevices (
                DeviceId, Platform, AppVersion, PushToken,
                NotificationsEnabled, LastActiveAt, RegisteredAt,
                UserId, IsActive
            )
            VALUES (
                'device_' + CAST(@m AS VARCHAR),
                @platform,
                CASE 
                    WHEN @m % 5 = 0 THEN '1.9.0'
                    WHEN @m % 4 = 0 THEN '2.0.0'
                    ELSE '2.1.0'
                END,
                'push_token_' + @platform + '_' + CAST(@m AS VARCHAR),
                CASE WHEN @m % 4 = 0 THEN 0 ELSE 1 END,
                DATEADD(minute, -CAST(RAND(CHECKSUM(NEWID())) * 10080 AS INT), @now5),
                DATEADD(day, -(@m % 90), @now5),
                'user_' + CAST(@m AS VARCHAR),
                CASE WHEN @m % 10 = 0 THEN 0 ELSE 1 END
            );
            
            SET @m = @m + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 100 Mobile Devices (50 Android, 50 iOS)\n");

    // ============================================================
    // 6. SEED PUSH NOTIFICATIONS (200 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Push Notifications (200 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM PushNotifications;
        
        DECLARE @n INT = 1;
        DECLARE @now6 DATETIME = GETDATE();
        
        WHILE @n <= 200
        BEGIN
            DECLARE @deviceId INT = 1 + (@n % 100);
            
            INSERT INTO PushNotifications (
                Name, Title, Body, UserId, DeviceId,
                Data, CreatedAt, SentAt, Status, AttemptCount, ErrorMessage
            )
            VALUES (
                'Notification ' + CAST(@n AS VARCHAR),
                CASE (@n % 10)
                    WHEN 0 THEN 'Production Complete'
                    WHEN 1 THEN 'Order Confirmed'
                    WHEN 2 THEN 'Low Stock Alert'
                    WHEN 3 THEN 'Payment Received'
                    WHEN 4 THEN 'Shipment Dispatched'
                    WHEN 5 THEN 'New Message'
                    WHEN 6 THEN 'System Update'
                    WHEN 7 THEN 'Inventory Alert'
                    WHEN 8 THEN 'Batch Complete'
                    ELSE 'General Notification'
                END,
                'Notification body message #' + CAST(@n AS VARCHAR) + ' - Important update',
                'user_' + CAST(@deviceId AS VARCHAR),
                @deviceId,
                '{"type":"test","id":' + CAST(@n AS VARCHAR) + ',"priority":"normal"}',
                DATEADD(minute, -(@n * 5), @now6),
                CASE 
                    WHEN @n % 15 = 0 THEN NULL
                    ELSE DATEADD(minute, -(@n * 5) + 1, @now6)
                END,
                CASE 
                    WHEN @n % 15 = 0 THEN 'pending'
                    WHEN @n % 20 = 0 THEN 'failed'
                    ELSE 'sent'
                END,
                CASE WHEN @n % 20 = 0 THEN 2 ELSE 1 END,
                CASE WHEN @n % 20 = 0 THEN 'Device token invalid' ELSE NULL END
            );
            
            SET @n = @n + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 200 Push Notifications with delivery tracking\n");

    // ============================================================
    // 7. SEED MOBILE ANALYTICS EVENTS (1000 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Mobile Analytics Events (1000 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM MobileAnalyticsEvents;
        
        DECLARE @p INT = 1;
        DECLARE @now7 DATETIME = GETDATE();
        
        WHILE @p <= 1000
        BEGIN
            INSERT INTO MobileAnalyticsEvents (
                DeviceId, UserId, Category, Action, Label,
                Value, Screen, Platform, AppVersion,
                ClientTimestamp, ServerTimestamp, IsActive
            )
            VALUES (
                1 + (@p % 100),
                'user_' + CAST(1 + (@p % 100) AS VARCHAR),
                CASE (@p % 6)
                    WHEN 0 THEN 'screen_view'
                    WHEN 1 THEN 'button_click'
                    WHEN 2 THEN 'user_interaction'
                    WHEN 3 THEN 'performance'
                    WHEN 4 THEN 'error'
                    ELSE 'session'
                END,
                CASE (@p % 10)
                    WHEN 0 THEN 'view'
                    WHEN 1 THEN 'click'
                    WHEN 2 THEN 'submit'
                    WHEN 3 THEN 'scroll'
                    WHEN 4 THEN 'load'
                    WHEN 5 THEN 'search'
                    WHEN 6 THEN 'filter'
                    WHEN 7 THEN 'export'
                    WHEN 8 THEN 'refresh'
                    ELSE 'navigate'
                END,
                'Label ' + CAST(@p AS VARCHAR),
                CAST(10 + (@p % 90) AS DECIMAL(18,2)),
                CASE (@p % 8)
                    WHEN 0 THEN 'Dashboard'
                    WHEN 1 THEN 'Production'
                    WHEN 2 THEN 'Orders'
                    WHEN 3 THEN 'Inventory'
                    WHEN 4 THEN 'Analytics'
                    WHEN 5 THEN 'Settings'
                    WHEN 6 THEN 'Reports'
                    ELSE 'Profile'
                END,
                CASE WHEN @p % 2 = 0 THEN 'Android' ELSE 'iOS' END,
                CASE WHEN @p % 3 = 0 THEN '2.0.0' ELSE '2.1.0' END,
                DATEADD(second, -(@p * 30), @now7),
                DATEADD(second, -(@p * 30) + 2, @now7),
                1
            );
            
            SET @p = @p + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 1000 Mobile Analytics Events across 8 screens\n");

    // ============================================================
    // 8. SEED REALTIME METRICS (500 records)
    // ============================================================
    Console.WriteLine("📊 Seeding Realtime Metrics (500 records)...");
    await ExecuteSqlAsync(connection, @"
        DELETE FROM RealtimeMetrics;
        
        DECLARE @q INT = 1;
        DECLARE @now8 DATETIME = GETDATE();
        
        WHILE @q <= 500
        BEGIN
            INSERT INTO RealtimeMetrics (
                MetricType, Value, CreatedDate, IsActive
            )
            VALUES (
                CASE (@q % 5)
                    WHEN 0 THEN 'API Request'
                    WHEN 1 THEN 'Page Load'
                    WHEN 2 THEN 'Database Query'
                    WHEN 3 THEN 'Cache Hit'
                    ELSE 'Background Job'
                END,
                CAST(20 + (RAND(CHECKSUM(NEWID())) * 480) AS DECIMAL(18,2)),
                DATEADD(second, -(@q * 60), @now8),
                1
            );
            
            SET @q = @q + 1;
        END
    ");
    Console.WriteLine("   ✓ Seeded 500 Realtime Metrics for monitoring\n");

    Console.WriteLine("\n" + STRING('=', 60));
    Console.WriteLine("✅ COMPREHENSIVE SEEDING COMPLETE!");
    Console.WriteLine(STRING('=', 60));
    Console.WriteLine("\n📊 SUMMARY:");
    Console.WriteLine("   • API Keys: 50 records");
    Console.WriteLine("   • API Analytics: 1000 records");
    Console.WriteLine("   • Webhooks: 50 records");
    Console.WriteLine("   • Integrations: 50 records");
    Console.WriteLine("   • Mobile Devices: 100 records");
    Console.WriteLine("   • Push Notifications: 200 records");
    Console.WriteLine("   • Mobile Analytics Events: 1000 records");
    Console.WriteLine("   • Realtime Metrics: 500 records");
    Console.WriteLine("\n   TOTAL: 2,950 RECORDS SEEDED");
    Console.WriteLine("\n🎯 All Phase 4 pages now have comprehensive test data!");
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
    Console.WriteLine(ex.StackTrace);
}

async Task ExecuteSqlAsync(SqlConnection connection, string sql)
{
    using var command = new SqlCommand(sql, connection);
    command.CommandTimeout = 300;
    await command.ExecuteNonQueryAsync();
}
