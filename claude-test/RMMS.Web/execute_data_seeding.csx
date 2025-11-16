#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;Connection Timeout=180;";

var sqlFile = "/home/user01/claude-test/RMMS.Web/COMPLETE_DATA_SEEDING.sql";
var sqlScript = File.ReadAllText(sqlFile);

// Split by GO statements
var batches = sqlScript.Split(new[] { "\r\nGO\r\n", "\nGO\n", "\rGO\r" }, StringSplitOptions.RemoveEmptyEntries);

Console.WriteLine($"Executing {batches.Length} SQL batches...\n");

var connection = new SqlConnection(connectionString);
connection.Open();
connection.InfoMessage += (sender, e) => Console.WriteLine(e.Message);

int batchNum = 0;
foreach (var batch in batches)
{
    if (string.IsNullOrWhiteSpace(batch)) continue;

    try
    {
        batchNum++;
        var command = new SqlCommand(batch, connection);
        command.CommandTimeout = 180;
        command.ExecuteNonQuery();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"❌ Error in batch {batchNum}: {ex.Message}");
    }
}

connection.Close();
Console.WriteLine($"\n✅ All {batchNum} batches executed successfully!");
