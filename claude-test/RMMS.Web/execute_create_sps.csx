#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlScript = File.ReadAllText("/home/user01/claude-test/RMMS.Web/CREATE_ALL_STORED_PROCEDURES.sql");

// Split by GO statements
var batches = sqlScript.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" }, StringSplitOptions.RemoveEmptyEntries);

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("Connected to database...\n");

    int successCount = 0;
    int errorCount = 0;

    foreach (var batch in batches)
    {
        var trimmedBatch = batch.Trim();
        if (string.IsNullOrWhiteSpace(trimmedBatch) || trimmedBatch.StartsWith("--")) continue;

        try
        {
            using (var cmd = new SqlCommand(trimmedBatch, connection))
            {
                cmd.CommandTimeout = 120;
                var result = cmd.ExecuteNonQuery();
            }
            successCount++;
        }
        catch (Exception ex)
        {
            errorCount++;
            Console.WriteLine($"Error executing batch: {ex.Message}");
            Console.WriteLine($"Batch: {trimmedBatch.Substring(0, Math.Min(100, trimmedBatch.Length))}...\n");
        }
    }

    Console.WriteLine($"\n✅ Execution complete!");
    Console.WriteLine($"   Successful batches: {successCount}");
    Console.WriteLine($"   Errors: {errorCount}");

    // Verify stored procedures
    var countCmd = new SqlCommand("SELECT COUNT(*) FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'PROCEDURE'", connection);
    var count = (int)countCmd.ExecuteScalar();
    Console.WriteLine($"   Total stored procedures in database: {count}");
}
