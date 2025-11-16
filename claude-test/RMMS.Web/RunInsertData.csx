#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

Console.WriteLine("===========================================");
Console.WriteLine("Executing INSERT_TEST_DATA.sql");
Console.WriteLine("===========================================\n");

var connStr = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=sa;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlFile = "/home/user01/claude-test/RMMS.Web/INSERT_TEST_DATA.sql";

try
{
    var sql = File.ReadAllText(sqlFile);

    using (var connection = new SqlConnection(connStr))
    {
        connection.Open();
        Console.WriteLine("✓ Connected to database\n");

        connection.InfoMessage += (sender, e) =>
        {
            Console.WriteLine(e.Message);
        };

        // Split by GO and execute each batch
        var batches = sql.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" }, StringSplitOptions.None);

        foreach (var batch in batches)
        {
            var trimmedBatch = batch.Trim();
            if (string.IsNullOrWhiteSpace(trimmedBatch) || trimmedBatch.StartsWith("--"))
                continue;

            try
            {
                using (var command = new SqlCommand(trimmedBatch, connection))
                {
                    command.CommandTimeout = 120;
                    command.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                // Ignore "already exists" errors for re-runs
                if (!ex.Message.Contains("Violation of PRIMARY KEY") &&
                    !ex.Message.Contains("duplicate key") &&
                    !ex.Message.Contains("IDENTITY_INSERT is already ON"))
                {
                    Console.WriteLine($"\n⚠ Warning: {ex.Message}");
                }
            }
        }

        Console.WriteLine("\n\n===========================================");
        Console.WriteLine("SUCCESS!");
        Console.WriteLine("===========================================");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n✗ ERROR: {ex.Message}");
    Console.WriteLine($"\nStack Trace:\n{ex.StackTrace}");
    Environment.Exit(1);
}
