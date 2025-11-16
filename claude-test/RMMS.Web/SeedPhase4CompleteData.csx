#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.EntityFrameworkCore.SqlServer, 8.0.0"
#r "nuget: System.Security.Cryptography.Algorithms, 4.3.1"

using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.Data.SqlClient;

Console.WriteLine("🚀 Starting Phase 4 Complete Data Seeding...");
Console.WriteLine("=".PadRight(80, '='));

// Connection string
var connectionString = "Server=localhost;Database=RMMSDB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;";

try
{
    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();
    Console.WriteLine("✅ Database connection established");

    // ==================== API KEYS ====================
    Console.WriteLine("\n📊 Seeding API Keys...");

    var apiKeysSql = @"
    -- Clear existing data
    DELETE FROM ApiKeys;
    DBCC CHECKIDENT ('ApiKeys', RESEED, 0);

    -- Insert API Keys with varied utilization
    INSERT INTO ApiKeys (Name, Description, KeyValue, RateLimit, RequestCount, IsActive, Permissions, CreatedDate, CreatedBy, LastUsed, ExpiresAt)
    VALUES
    -- Production key with high utilization (95%)
    ('Production API Key', 'Main production API access', 'rmms_prod_key_hash_123456789abcdefghijk', 10000, 9500, 1, 'read,write,delete', DATEADD(day, -30, GETDATE()), 'admin', DATEADD(hour, -2, GETDATE()), NULL),

    -- Mobile key with over-limit usage (254.3%)
    ('Mobile App Key', 'Mobile application API access', 'rmms_mobile_key_hash_987654321zyxwvut', 5000, 12715, 1, 'read,write', DATEADD(day, -20, GETDATE()), 'admin', DATEADD(minute, -15, GETDATE()), NULL),

    -- Analytics key with 228% utilization
    ('Analytics Key', 'Data analytics and reporting', 'rmms_analytics_key_hash_abcd1234efgh', 2000, 4560, 1, 'read', DATEADD(day, -15, GETDATE()), 'admin', DATEADD(hour, -1, GETDATE()), NULL),

    -- Test key with low usage
    ('Test Key', 'Development and testing', 'rmms_test_key_hash_test12345678', 1000, 0, 0, 'read', DATEADD(day, -5, GETDATE()), 'developer', NULL, DATEADD(day, 30, GETDATE()));

    PRINT '✅ Inserted 4 API Keys with varied utilization levels';
    ";

    await ExecuteSqlAsync(connection, apiKeysSql);
    Console.WriteLine("  ✅ 4 API Keys inserted (including 199%+ utilization cases)");

    // ==================== WEBHOOKS ====================
    Console.WriteLine("\n📊 Seeding Webhooks...");

    var webhooksSql = @"
    -- Clear existing data
    DELETE FROM Webhooks;
    DBCC CHECKIDENT ('Webhooks', RESEED, 0);

    -- Insert Webhooks
    INSERT INTO Webhooks (Name, Description, Url, EventType, Method, IsActive, RetryCount, TimeoutSeconds, CreatedDate, CreatedBy, LastTriggered)
    VALUES
    ('Order Created Webhook', 'Notification when new orders are created', 'https://api.example.com/webhooks/order-created', 'order.created', 'POST', 1, 3, 30, DATEADD(day, -10, GETDATE()), 'admin', DATEADD(hour, -3, GETDATE())),
    ('Production Batch Completed', 'Alert when production batches complete', 'https://api.example.com/webhooks/batch-complete', 'production.batch.completed', 'POST', 1, 5, 60, DATEADD(day, -8, GETDATE()), 'admin', DATEADD(hour, -1, GETDATE())),
    ('Low Stock Alert', 'Notification for low inventory levels', 'https://api.example.com/webhooks/low-stock', 'inventory.low_stock', 'POST', 1, 3, 30, DATEADD(day, -5, GETDATE()), 'admin', DATEADD(day, -1, GETDATE())),
    ('Payment Received', 'Customer payment notifications', 'https://api.example.com/webhooks/payment', 'payment.received', 'POST', 1, 3, 30, DATEADD(day, -3, GETDATE()), 'admin', DATEADD(hour, -6, GETDATE())),
    ('Inactive Webhook', 'Currently paused webhook', 'https://api.example.com/webhooks/inactive', 'customer.created', 'POST', 0, 3, 30, DATEADD(day, -1, GETDATE()), 'admin', NULL);

    PRINT '✅ Inserted 5 Webhooks';
    ";

    await ExecuteSqlAsync(connection, webhooksSql);
    Console.WriteLine("  ✅ 5 Webhooks inserted (4 active, 1 inactive)");

    // ==================== MOBILE DEVICES ====================
    Console.WriteLine("\n📊 Seeding Mobile Devices...");

    var mobileDevicesSql = @"
    -- Clear existing data
    DELETE FROM MobileDevices;
    DBCC CHECKIDENT ('MobileDevices', RESEED, 0);

    -- Insert Mobile Devices
    INSERT INTO MobileDevices (UserId, DeviceId, Platform, DeviceModel, OSVersion, AppVersion, PushToken, Language, NotificationsEnabled, BiometricEnabled, LastActiveAt, RegisteredAt, IsActive)
    VALUES
    -- Android devices
    ('user1', 'android-device-001', 'Android', 'Samsung Galaxy S23', '14.0', '1.2.0', 'fcm-token-android-001', 'en-US', 1, 1, DATEADD(minute, -10, GETDATE()), DATEADD(day, -30, GETDATE()), 1),
    ('user2', 'android-device-002', 'Android', 'Google Pixel 8', '14.0', '1.2.0', 'fcm-token-android-002', 'en-US', 1, 0, DATEADD(hour, -2, GETDATE()), DATEADD(day, -25, GETDATE()), 1),
    ('user3', 'android-device-003', 'Android', 'OnePlus 11', '13.0', '1.1.0', 'fcm-token-android-003', 'es-ES', 0, 1, DATEADD(day, -5, GETDATE()), DATEADD(day, -20, GETDATE()), 1),

    -- iOS devices
    ('user4', 'ios-device-001', 'iOS', 'iPhone 15 Pro', '17.1', '1.2.0', 'apns-token-ios-001', 'en-US', 1, 1, DATEADD(minute, -30, GETDATE()), DATEADD(day, -28, GETDATE()), 1),
    ('user5', 'ios-device-002', 'iOS', 'iPhone 14', '17.0', '1.2.0', 'apns-token-ios-002', 'en-GB', 1, 1, DATEADD(hour, -1, GETDATE()), DATEADD(day, -15, GETDATE()), 1),
    ('user6', 'ios-device-003', 'iOS', 'iPad Pro 12.9', '17.1', '1.2.0', 'apns-token-ios-003', 'fr-FR', 1, 0, DATEADD(day, -2, GETDATE()), DATEADD(day, -10, GETDATE()), 1),

    -- Inactive device
    ('user7', 'android-device-old', 'Android', 'Samsung Galaxy S20', '12.0', '1.0.0', 'fcm-token-old', 'en-US', 0, 0, DATEADD(day, -60, GETDATE()), DATEADD(day, -90, GETDATE()), 0);

    PRINT '✅ Inserted 7 Mobile Devices (4 Android, 3 iOS)';
    ";

    await ExecuteSqlAsync(connection, mobileDevicesSql);
    Console.WriteLine("  ✅ 7 Mobile Devices inserted (4 Android, 3 iOS)");

    // ==================== PUSH NOTIFICATIONS ====================
    Console.WriteLine("\n📊 Seeding Push Notifications...");

    var pushNotificationsSql = @"
    -- Clear existing data
    DELETE FROM PushNotifications;
    DBCC CHECKIDENT ('PushNotifications', RESEED, 0);

    -- Insert Push Notifications
    INSERT INTO PushNotifications (Name, Title, Body, UserId, DeviceId, Type, Priority, Status, CreatedAt, SentAt, IsRead, ReadAt, AttemptCount)
    VALUES
    -- Recent delivered notifications
    ('Production Alert 1', 'Production Complete', 'Batch #12345 has completed processing', 'user1', 1, 'production', 'high', 'sent', DATEADD(hour, -2, GETDATE()), DATEADD(hour, -2, GETDATE()), 1, DATEADD(hour, -1, GETDATE()), 1),
    ('Sales Notification', 'New Order Received', 'Order #98765 has been placed', 'user2', 2, 'sales', 'normal', 'delivered', DATEADD(hour, -5, GETDATE()), DATEADD(hour, -5, GETDATE()), 1, DATEADD(hour, -4, GETDATE()), 1),
    ('Inventory Alert', 'Low Stock Warning', 'Rice variety XYZ is running low', 'user4', 4, 'inventory', 'high', 'sent', DATEADD(hour, -8, GETDATE()), DATEADD(hour, -8, GETDATE()), 0, NULL, 1),

    -- Today's notifications
    ('Payment Alert', 'Payment Received', 'Payment of $5,000 received', 'user1', 1, 'payment', 'normal', 'sent', DATEADD(hour, -1, GETDATE()), DATEADD(hour, -1, GETDATE()), 1, DATEADD(minute, -30, GETDATE()), 1),
    ('Quality Check', 'Quality Inspection Due', 'Batch #12346 requires inspection', 'user2', 2, 'quality', 'normal', 'delivered', DATEADD(hour, -3, GETDATE()), DATEADD(hour, -3, GETDATE()), 0, NULL, 1),

    -- This week notifications
    ('Weekly Report', 'Weekly Summary Ready', 'Your weekly report is ready to view', 'user5', 5, 'report', 'low', 'sent', DATEADD(day, -2, GETDATE()), DATEADD(day, -2, GETDATE()), 1, DATEADD(day, -1, GETDATE()), 1),
    ('System Update', 'App Update Available', 'New version 1.3.0 is available', 'user4', 4, 'system', 'normal', 'sent', DATEADD(day, -3, GETDATE()), DATEADD(day, -3, GETDATE()), 0, NULL, 1),

    -- Pending notification
    ('Scheduled Alert', 'Scheduled Maintenance', 'System maintenance tonight at 10 PM', 'user1', 1, 'system', 'normal', 'pending', GETDATE(), NULL, 0, NULL, 0),

    -- Failed notification
    ('Failed Delivery', 'Test Notification', 'This notification failed to deliver', 'user3', 3, 'test', 'low', 'failed', DATEADD(hour, -12, GETDATE()), NULL, 0, NULL, 3);

    PRINT '✅ Inserted 9 Push Notifications (mix of sent, delivered, pending, failed)';
    ";

    await ExecuteSqlAsync(connection, pushNotificationsSql);
    Console.WriteLine("  ✅ 9 Push Notifications inserted (varied delivery states)");

    // ==================== MOBILE ANALYTICS EVENTS ====================
    Console.WriteLine("\n📊 Seeding Mobile Analytics Events...");

    var analyticsEventsSql = @"
    -- Clear existing data
    DELETE FROM MobileAnalyticsEvents;
    DBCC CHECKIDENT ('MobileAnalyticsEvents', RESEED, 0);

    -- Insert Analytics Events
    DECLARE @i INT = 0;
    WHILE @i < 50
    BEGIN
        INSERT INTO MobileAnalyticsEvents (UserId, DeviceId, EventId, Category, Action, Label, Screen, Value, Platform, AppVersion, ServerTimestamp, DeviceTimestamp)
        VALUES
        ('user' + CAST((@i % 6) + 1 AS VARCHAR), 'device-00' + CAST((@i % 6) + 1 AS VARCHAR),
         NEWID(),
         CASE (@i % 5)
            WHEN 0 THEN 'screen_view'
            WHEN 1 THEN 'button_click'
            WHEN 2 THEN 'performance'
            WHEN 3 THEN 'error'
            ELSE 'user_action'
         END,
         CASE (@i % 5)
            WHEN 0 THEN 'view'
            WHEN 1 THEN 'click'
            WHEN 2 THEN 'load_time'
            WHEN 3 THEN 'exception'
            ELSE 'submit'
         END,
         'Event ' + CAST(@i AS VARCHAR),
         CASE (@i % 6)
            WHEN 0 THEN 'Dashboard'
            WHEN 1 THEN 'Production'
            WHEN 2 THEN 'Sales'
            WHEN 3 THEN 'Inventory'
            WHEN 4 THEN 'Reports'
            ELSE 'Settings'
         END,
         RAND() * 1000,
         CASE (@i % 2) WHEN 0 THEN 'Android' ELSE 'iOS' END,
         '1.2.0',
         DATEADD(minute, -(@i * 10), GETDATE()),
         DATEADD(minute, -(@i * 10), GETDATE())
        );
        SET @i = @i + 1;
    END

    PRINT '✅ Inserted 50 Mobile Analytics Events';
    ";

    await ExecuteSqlAsync(connection, analyticsEventsSql);
    Console.WriteLine("  ✅ 50 Mobile Analytics Events inserted");

    // ==================== REALTIME METRICS ====================
    Console.WriteLine("\n📊 Seeding Realtime Metrics...");

    var realtimeMetricsSql = @"
    -- Clear existing data
    DELETE FROM RealtimeMetrics;
    DBCC CHECKIDENT ('RealtimeMetrics', RESEED, 0);

    -- Insert Realtime Metrics (last 30 minutes)
    DECLARE @j INT = 0;
    WHILE @j < 30
    BEGIN
        INSERT INTO RealtimeMetrics (MetricType, Value, CreatedDate, IsActive)
        VALUES
        (CASE (@j % 4)
            WHEN 0 THEN 'api_latency'
            WHEN 1 THEN 'db_query_time'
            WHEN 2 THEN 'memory_usage'
            ELSE 'cpu_usage'
         END,
         ABS(CHECKSUM(NEWID())) % 100 + 10.0,
         DATEADD(minute, -@j, GETDATE()),
         1);
        SET @j = @j + 1;
    END

    PRINT '✅ Inserted 30 Realtime Metrics';
    ";

    await ExecuteSqlAsync(connection, realtimeMetricsSql);
    Console.WriteLine("  ✅ 30 Realtime Metrics inserted");

    Console.WriteLine("\n" + "=".PadRight(80, '='));
    Console.WriteLine("✅ Phase 4 Data Seeding COMPLETE!");
    Console.WriteLine("\nSummary:");
    Console.WriteLine("  - 4 API Keys (with 199%+ utilization cases)");
    Console.WriteLine("  - 5 Webhooks (4 active, 1 inactive)");
    Console.WriteLine("  - 7 Mobile Devices (4 Android, 3 iOS)");
    Console.WriteLine("  - 9 Push Notifications (varied states)");
    Console.WriteLine("  - 50 Mobile Analytics Events");
    Console.WriteLine("  - 30 Realtime Metrics");
    Console.WriteLine("\n🎉 All Phase 4 pages should now show data!");
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
    Console.WriteLine($"Stack Trace: {ex.StackTrace}");
    Environment.Exit(1);
}

async Task ExecuteSqlAsync(SqlConnection connection, string sql)
{
    using var command = new SqlCommand(sql, connection);
    command.CommandTimeout = 120;
    await command.ExecuteNonQueryAsync();
}
