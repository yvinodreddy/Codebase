#!/usr/bin/env dotnet script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

var connectionString = "Server=172.17.208.1;Database=RMMS_Production;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;";
var sqlFilePath = "05_CreateProductionTables.sql";

try
{
    Console.WriteLine("Reading SQL migration file...");
    var sqlScript = File.ReadAllText(sqlFilePath);

    Console.WriteLine("Connecting to database...");
    using var connection = new SqlConnection(connectionString);
    connection.Open();

    Console.WriteLine("Executing migration...");

    // Split by GO statements
    var batches = sqlScript.Split(new[] { "\nGO\n", "\ngo\n", "\nGo\n" }, StringSplitOptions.RemoveEmptyEntries);

    foreach (var batch in batches)
    {
        if (!string.IsNullOrWhiteSpace(batch))
        {
            using var command = new SqlCommand(batch, connection);
            command.CommandTimeout = 300; // 5 minutes timeout
            command.ExecuteNonQuery();
        }
    }

    Console.WriteLine("✅ Migration completed successfully!");
    Console.WriteLine("Created 6 production tables:");
    Console.WriteLine("  - Machines");
    Console.WriteLine("  - ProductionOrders");
    Console.WriteLine("  - ProductionBatches");
    Console.WriteLine("  - BatchInputs");
    Console.WriteLine("  - BatchOutputs");
    Console.WriteLine("  - YieldRecords");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Error: {ex.Message}");
    Console.WriteLine($"Stack trace: {ex.StackTrace}");
    Environment.Exit(1);
}
