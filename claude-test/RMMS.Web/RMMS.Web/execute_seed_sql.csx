#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlFile = "SCHEMA_ACCURATE_SEED_DATA.sql";

Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
Console.WriteLine("║           EXECUTING SCHEMA-ACCURATE SEED DATA SCRIPT               ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
Console.WriteLine();

try
{
    if (!File.Exists(sqlFile))
    {
        Console.WriteLine($"❌ Error: {sqlFile} not found!");
        return 1;
    }

    var sqlContent = File.ReadAllText(sqlFile);

    // Split by GO statements
    var batches = sqlContent.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" },
                                   StringSplitOptions.RemoveEmptyEntries);

    int errorCount = 0;

    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine("✅ Connected to database: RMMS_Production");
        Console.WriteLine($"📦 Executing {batches.Length} SQL batches...");
        Console.WriteLine();

        connection.InfoMessage += (sender, e) => {
            Console.WriteLine($"   {e.Message}");
        };

        connection.FireInfoMessageEventOnUserErrors = true;

        int batchNumber = 0;
        int successCount = 0;

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
                    successCount++;
                }
            }
            catch (Exception ex)
            {
                errorCount++;
                Console.WriteLine($"❌ Error in batch {batchNumber}: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"   Inner: {ex.InnerException.Message}");
                }
            }
        }

        Console.WriteLine();
        Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        Console.WriteLine($"Execution Summary:");
        Console.WriteLine($"  Total Batches: {batchNumber}");
        Console.WriteLine($"  Success: {successCount} ✅");
        Console.WriteLine($"  Errors: {errorCount} {(errorCount > 0 ? "❌" : "")}");
        Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

        // Verify counts
        Console.WriteLine();
        Console.WriteLine("🔍 Verifying Record Counts:");

        var tables = new[] {
            "StockAdjustments", "ProductionOrders", "ProductionBatches", "YieldRecords",
            "Inquiries", "Quotations", "SalesOrders", "Vouchers",
            "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances"
        };

        foreach (var table in tables)
        {
            var countQuery = $"SELECT COUNT(*) FROM {table} WHERE IsActive = 1";
            try
            {
                using (var cmd = new SqlCommand(countQuery, connection))
                {
                    var count = (int)cmd.ExecuteScalar();
                    var status = count >= 40 ? "✅" : "⚠️ ";
                    Console.WriteLine($"  {table,-25}: {count,3} records {status}");
                }
            }
            catch
            {
                // Try without IsActive
                countQuery = $"SELECT COUNT(*) FROM {table}";
                using (var cmd = new SqlCommand(countQuery, connection))
                {
                    var count = (int)cmd.ExecuteScalar();
                    var status = count >= 40 ? "✅" : "⚠️ ";
                    Console.WriteLine($"  {table,-25}: {count,3} records {status}");
                }
            }
        }
    }

    Console.WriteLine();
    Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
    Console.WriteLine("║                  ✅ EXECUTION COMPLETED!                           ║");
    Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");

    return errorCount > 0 ? 1 : 0;
}
catch (Exception ex)
{
    Console.WriteLine($"❌ Fatal Error: {ex.Message}");
    if (ex.InnerException != null)
    {
        Console.WriteLine($"   Inner: {ex.InnerException.Message}");
    }
    return 1;
}
