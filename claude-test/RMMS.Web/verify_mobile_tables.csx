#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var connection = new SqlConnection(connectionString);
connection.Open();

var command = new SqlCommand(@"
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
AND TABLE_NAME LIKE 'Mobile%'
ORDER BY TABLE_NAME", connection);

Console.WriteLine("\n📱 MOBILE TABLES IN DATABASE:");
Console.WriteLine("================================");
var reader = command.ExecuteReader();
int count = 0;
while (reader.Read())
{
    Console.WriteLine($"✅ {reader.GetString(0)}");
    count++;
}
reader.Close();
connection.Close();
Console.WriteLine($"\nTotal Mobile Tables: {count}");

if (count >= 5)
{
    Console.WriteLine("✅ All mobile tables created successfully!");
}
else
{
    Console.WriteLine($"⚠️ Expected 5 mobile tables, found {count}");
}
