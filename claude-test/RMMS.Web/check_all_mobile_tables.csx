#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var connection = new SqlConnection(connectionString);
connection.Open();

// Check for all expected mobile tables (exact and partial matches)
var expectedTables = new[] { "MobileDevices", "PushNotifications", "SyncLogs", "MobileAppConfigs", "MobileAnalyticsEvents" };

Console.WriteLine("\n📊 CHECKING MOBILE TABLES:");
Console.WriteLine("================================");

foreach (var tableName in expectedTables)
{
    var command = new SqlCommand($@"
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{tableName}'", connection);

    var exists = (int)command.ExecuteScalar() > 0;

    if (exists)
    {
        Console.WriteLine($"✅ {tableName}");
    }
    else
    {
        Console.WriteLine($"❌ {tableName} - NOT FOUND");
    }
}

// List all tables starting with 'Push' or 'Sync' or containing 'Notification'
var searchCommand = new SqlCommand(@"
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    AND (TABLE_NAME LIKE 'Push%' OR TABLE_NAME LIKE 'Sync%' OR TABLE_NAME LIKE '%Notification%')
    ORDER BY TABLE_NAME", connection);

Console.WriteLine("\n🔍 TABLES WITH SIMILAR NAMES:");
Console.WriteLine("================================");
var reader = searchCommand.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"  {reader.GetString(0)}");
}
reader.Close();

connection.Close();
