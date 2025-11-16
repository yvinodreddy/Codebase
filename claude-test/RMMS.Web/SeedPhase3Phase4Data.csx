#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Threading.Tasks;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;";

Console.WriteLine("🚀 Starting Phase 3 & 4 data seeding...");

try
{
    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();
    Console.WriteLine("✓ Database connected successfully");

    // PHASE 4: API KEYS
    await ExecuteSqlAsync(connection, @"
        IF NOT EXISTS (SELECT 1 FROM ApiKeys WHERE Name = 'Production API Key')
        BEGIN
            INSERT INTO ApiKeys (Name, Description, KeyValue, UserId, ExpiresAt, IsActive, RequestCount, RateLimit, LastUsed, Permissions, CreatedBy, CreatedDate)
            VALUES
            ('Production API Key', 'Main production API key', 'hashed_key_prod_12345', 'system', DATEADD(year, 1, GETDATE()), 1, 25432, 10000, DATEADD(hour, -2, GETDATE()), 'read,write,delete', 'admin', GETDATE()),
            ('Mobile App Key', 'API key for mobile apps', 'hashed_key_mobile_67890', 'mobile-app', DATEADD(month, 6, GETDATE()), 1, 15678, 5000, DATEADD(hour, -1, GETDATE()), 'read,write', 'admin', GETDATE()),
            ('Analytics Key', 'Read-only analytics key', 'hashed_key_analytics_11111', 'analytics', DATEADD(month, 3, GETDATE()), 1, 4568, 2000, DATEADD(day, -1, GETDATE()), 'read', 'admin', GETDATE()),
            ('Test Key', 'Testing key', 'hashed_key_test_22222', 'test-user', DATEADD(month, 1, GETDATE()), 0, 0, 1000, NULL, 'read', 'admin', DATEADD(day, -30, GETDATE()));
        END
    ");
    Console.WriteLine("✓ Seeded API Keys");

    // PHASE 4: MOBILE DEVICES
    await ExecuteSqlAsync(connection, @"
        IF NOT EXISTS (SELECT 1 FROM MobileDevices WHERE DeviceName = 'iPhone 13 Pro')
        BEGIN
            INSERT INTO MobileDevices (DeviceId, DeviceName, Platform, AppVersion, PushToken, NotificationsEnabled, LastActiveAt, CreatedDate, IsActive)
            VALUES
            ('device_001', 'iPhone 13 Pro', 'iOS', '2.1.0', 'push_token_ios_001', 1, DATEADD(hour, -1, GETDATE()), GETDATE(), 1),
            ('device_002', 'Samsung Galaxy S21', 'Android', '2.1.0', 'push_token_android_002', 1, DATEADD(hour, -2, GETDATE()), GETDATE(), 1),
            ('device_003', 'iPad Pro', 'iOS', '2.0.5', 'push_token_ios_003', 0, DATEADD(day, -5, GETDATE()), DATEADD(day, -30, GETDATE()), 1),
            ('device_004', 'Google Pixel 6', 'Android', '2.1.0', 'push_token_android_004', 1, DATEADD(hour, -3, GETDATE()), DATEADD(day, -15, GETDATE()), 1);
        END
    ");
    Console.WriteLine("✓ Seeded Mobile Devices");

    // PHASE 4: WEBHOOKS
    await ExecuteSqlAsync(connection, @"
        IF NOT EXISTS (SELECT 1 FROM Webhooks WHERE Name = 'Production Alerts')
        BEGIN
            INSERT INTO Webhooks (Name, Url, EventType, HttpMethod, Headers, IsActive, LastTriggeredAt, TimeoutSeconds, CreatedDate, CreatedBy)
            VALUES
            ('Production Alerts', 'https://api.example.com/webhooks/production', 'ProductionComplete', 'POST', '{""Authorization"":""Bearer token123""}', 1, DATEADD(hour, -2, GETDATE()), 30, DATEADD(day, -30, GETDATE()), 'admin'),
            ('Order Notifications', 'https://api.example.com/webhooks/orders', 'OrderCreated', 'POST', '{""Authorization"":""Bearer token456""}', 1, DATEADD(minute, -30, GETDATE()), 30, DATEADD(day, -20, GETDATE()), 'admin'),
            ('Inventory Alerts', 'https://api.example.com/webhooks/inventory', 'LowStock', 'POST', '{""Authorization"":""Bearer token789""}', 1, DATEADD(hour, -5, GETDATE()), 30, DATEADD(day, -15, GETDATE()), 'admin'),
            ('Payment Received', 'https://api.example.com/webhooks/payments', 'PaymentReceived', 'POST', '{""Authorization"":""Bearer tokenABC""}', 0, NULL, 30, DATEADD(day, -10, GETDATE()), 'admin'),
            ('All Events Monitor', 'https://api.example.com/webhooks/all', 'All', 'POST', '{""Authorization"":""Bearer tokenXYZ""}', 1, DATEADD(minute, -5, GETDATE()), 60, DATEADD(day, -5, GETDATE()), 'admin');
        END
    ");
    Console.WriteLine("✓ Seeded Webhooks");

    // PHASE 4: INTEGRATIONS
    await ExecuteSqlAsync(connection, @"
        IF NOT EXISTS (SELECT 1 FROM Integrations WHERE Name = 'SAP ERP Integration')
        BEGIN
            INSERT INTO Integrations (Name, Type, Endpoint, ApiKey, Status, LastSyncAt, ResponseTime, SuccessCount, FailureCount, ErrorMessage, IsActive, CreatedDate, CreatedBy)
            VALUES
            ('SAP ERP Integration', 'ERP', 'https://sap.example.com/api', 'sap_key_12345', 'Connected', DATEADD(hour, -1, GETDATE()), 245, 1250, 3, NULL, 1, DATEADD(month, -6, GETDATE()), 'admin'),
            ('Salesforce CRM', 'CRM', 'https://salesforce.example.com/api', 'sf_key_67890', 'Connected', DATEADD(hour, -2, GETDATE()), 180, 892, 1, NULL, 1, DATEADD(month, -4, GETDATE()), 'admin'),
            ('QuickBooks Accounting', 'Accounting', 'https://quickbooks.example.com/api', 'qb_key_11111', 'Error', DATEADD(day, -2, GETDATE()), 0, 456, 23, 'Authentication failed - Token expired', 1, DATEADD(month, -3, GETDATE()), 'admin'),
            ('Shipping Provider API', 'Logistics', 'https://shipping.example.com/api', 'ship_key_22222', 'Connected', DATEADD(minute, -30, GETDATE()), 312, 2103, 5, NULL, 1, DATEADD(month, -2, GETDATE()), 'admin'),
            ('Payment Gateway', 'Payment', 'https://payment.example.com/api', 'pay_key_33333', 'Disconnected', DATEADD(day, -10, GETDATE()), 0, 0, 0, NULL, 0, DATEADD(month, -1, GETDATE()), 'admin');
        END
    ");
    Console.WriteLine("✓ Seeded Integrations");

    // PHASE 4: PUSH NOTIFICATIONS
    await ExecuteSqlAsync(connection, @"
        IF NOT EXISTS (SELECT 1 FROM PushNotifications WHERE Title = 'Production Complete')
        BEGIN
            INSERT INTO PushNotifications (Title, Body, TargetType, TargetValue, TargetDeviceCount, DeliveredCount, FailedCount, Status, SentAt, CreatedDate, CreatedBy, IsActive)
            VALUES
            ('Production Complete', 'Batch #12345 completed successfully', 'All', NULL, 4, 4, 0, 'Delivered', DATEADD(hour, -2, GETDATE()), DATEADD(hour, -2, GETDATE()), 'system', 1),
            ('Inventory Alert', 'Low stock alert - 20 bags remaining', 'Android', NULL, 2, 2, 0, 'Delivered', DATEADD(hour, -5, GETDATE()), DATEADD(hour, -5, GETDATE()), 'system', 1),
            ('Order Confirmed', 'Order #ORD-789 confirmed', 'User', 'device_001', 1, 1, 0, 'Delivered', DATEADD(day, -1, GETDATE()), DATEADD(day, -1, GETDATE()), 'system', 1),
            ('System Maintenance', 'Maintenance tonight at 10 PM', 'PushEnabled', NULL, 3, 2, 1, 'PartiallyFailed', DATEADD(day, -2, GETDATE()), DATEADD(day, -2, GETDATE()), 'admin', 1);
        END
    ");
    Console.WriteLine("✓ Seeded Push Notifications");

    Console.WriteLine("\n✅ ALL DATA SEEDED SUCCESSFULLY!");
    Console.WriteLine("📊 Data is now available for all Phase 3 & 4 controllers");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ ERROR: {ex.Message}");
    Console.WriteLine(ex.StackTrace);
}

async Task ExecuteSqlAsync(SqlConnection connection, string sql)
{
    using var command = new SqlCommand(sql, connection);
    command.CommandTimeout = 120;
    await command.ExecuteNonQueryAsync();
}
