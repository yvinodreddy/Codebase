#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlFile = "COMPLETE_SEED_DATA_FIX.sql";

Console.WriteLine("========================================");
Console.WriteLine("Executing Comprehensive Seed Data Script");
Console.WriteLine("========================================");
Console.WriteLine();

try
{
    if (!File.Exists(sqlFile))
    {
        Console.WriteLine($"Error: {sqlFile} not found!");
        return 1;
    }

    var sqlContent = File.ReadAllText(sqlFile);
    
    // Split by GO statements
    var batches = sqlContent.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" }, 
                                   StringSplitOptions.RemoveEmptyEntries);
    
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine("✅ Connected to database");
        Console.WriteLine($"Executing {batches.Length} SQL batches...");
        Console.WriteLine();
        
        int batchNumber = 0;
        foreach (var batch in batches)
        {
            var trimmedBatch = batch.Trim();
            if (string.IsNullOrWhiteSpace(trimmedBatch)) continue;
            
            batchNumber++;
            
            try
            {
                using (var command = new SqlCommand(trimmedBatch, connection))
                {
                    command.CommandTimeout = 300; // 5 minutes
                    command.ExecuteNonQuery();
                }
                
                if (trimmedBatch.Contains("PRINT"))
                {
                    var printLine = trimmedBatch.Split('\n')
                        .FirstOrDefault(l => l.Contains("PRINT") && l.Contains("'"));
                    if (printLine != null)
                    {
                        var message = printLine.Split('\'')[1];
                        Console.WriteLine($"  {message}");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error in batch {batchNumber}: {ex.Message}");
            }
        }
        
        Console.WriteLine();
        Console.WriteLine("========================================");
        Console.WriteLine("✅ Seed Data Insertion Completed!");
        Console.WriteLine("========================================");
    }
    
    return 0;
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Fatal Error: {ex.Message}");
    return 1;
}
