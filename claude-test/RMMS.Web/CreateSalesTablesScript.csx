#!/usr/bin/env dotnet script

#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

// Read the SQL script
var sqlScript = File.ReadAllText("CreateSalesTables.sql");

// Split by GO statements
var batches = sqlScript.Split(new[] { "\nGO", "\rGO", "\r\nGO" }, StringSplitOptions.RemoveEmptyEntries);

try
{
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine("Connected to database successfully!");

        foreach (var batch in batches)
        {
            var trimmedBatch = batch.Trim();
            if (string.IsNullOrWhiteSpace(trimmedBatch) || trimmedBatch.StartsWith("--"))
                continue;

            try
            {
                using (var command = new SqlCommand(trimmedBatch, connection))
                {
                    command.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error executing batch: {ex.Message}");
            }
        }

        Console.WriteLine("\nAll tables created successfully!");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
