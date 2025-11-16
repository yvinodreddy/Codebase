#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var scriptPath = "/home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql";

Console.WriteLine("==================================================");
Console.WriteLine("RMMS Database Initialization");
Console.WriteLine("==================================================");
Console.WriteLine();

try
{
    var sqlScript = File.ReadAllText(scriptPath);

    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine("✓ Connected to database");

        // Split and execute each GO-separated batch
        var batches = sqlScript.Split(new[] { "\r\nGO\r\n", "\nGO\n", "\r\nGO", "\nGO" }, StringSplitOptions.RemoveEmptyEntries);

        int batchCount = 0;
        foreach (var batch in batches)
        {
            if (!string.IsNullOrWhiteSpace(batch))
            {
                using (var command = new SqlCommand(batch, connection))
                {
                    command.CommandTimeout = 120;
                    command.ExecuteNonQuery();
                    batchCount++;
                }
            }
        }

        Console.WriteLine($"✓ Executed {batchCount} SQL batches");
        Console.WriteLine();
        Console.WriteLine("==================================================");
        Console.WriteLine("DATABASE INITIALIZED SUCCESSFULLY!");
        Console.WriteLine("==================================================");
    }
}
catch (Exception ex)
{
    Console.WriteLine();
    Console.WriteLine($"ERROR: {ex.Message}");
    Console.WriteLine();
    Console.WriteLine("Please run the SQL script manually:");
    Console.WriteLine("  File: /home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql");
    Environment.Exit(1);
}
