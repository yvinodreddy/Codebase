#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;
using System.Text.RegularExpressions;

Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
Console.WriteLine("║       RMMS COMPREHENSIVE DATA SEEDING                      ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════╝\n");

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlFile = "CORRECTED_SEED_DATA.sql";

if (!File.Exists(sqlFile))
{
    Console.WriteLine($"❌ ERROR: {sqlFile} not found!");
    Environment.Exit(1);
}

Console.WriteLine($"📄 Reading SQL file: {sqlFile}");
var sqlContent = File.ReadAllText(sqlFile);

Console.WriteLine("📊 Connecting to database...");

try
{
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine("✅ Connected successfully!\n");

        // Split SQL content by GO statements
        var batches = Regex.Split(sqlContent, @"^\s*GO\s*$", RegexOptions.Multiline | RegexOptions.IgnoreCase);

        int batchNumber = 0;
        int successCount = 0;
        int errorCount = 0;

        foreach (var batch in batches)
        {
            var trimmedBatch = batch.Trim();
            if (string.IsNullOrWhiteSpace(trimmedBatch))
                continue;

            // Skip USE DATABASE statements
            if (trimmedBatch.StartsWith("USE ", StringComparison.OrdinalIgnoreCase))
                continue;

            batchNumber++;

            try
            {
                using (var command = new SqlCommand(trimmedBatch, connection))
                {
                    command.CommandTimeout = 300; // 5 minutes timeout

                    // Execute and capture any messages/print statements
                    command.ExecuteNonQuery();
                    successCount++;

                    // Show progress every 10 batches
                    if (batchNumber % 10 == 0)
                    {
                        Console.WriteLine($"⏳ Processing batch {batchNumber}...");
                    }
                }
            }
            catch (Exception ex)
            {
                errorCount++;
                Console.WriteLine($"\n⚠️  Batch {batchNumber} warning: {ex.Message}");

                // Continue execution even if one batch fails
                // (might be due to existing data or constraints)
            }
        }

        Console.WriteLine($"\n{'═',60}");
        Console.WriteLine($"✅ Execution Complete!");
        Console.WriteLine($"{'═',60}");
        Console.WriteLine($"Total Batches: {batchNumber}");
        Console.WriteLine($"Successful: {successCount}");
        Console.WriteLine($"Warnings/Errors: {errorCount}");
        Console.WriteLine();

        // Now verify the results
        Console.WriteLine("📊 Verifying data insertion...\n");

        var tables = new[]
        {
            "Customers", "Vendors", "Products", "Employees",
            "Warehouses", "StorageZones", "InventoryLedger", "StockMovements", "StockAdjustments",
            "Machines", "ProductionOrders", "ProductionBatches", "BatchInputs", "BatchOutputs", "YieldRecords",
            "PaddyProcurement", "RiceProcurementExternal",
            "Inquiries", "Quotations", "QuotationItems", "SalesOrders", "SalesOrderItems",
            "RiceSales", "ByProductSales", "ExternalRiceSales",
            "BankTransactions", "CashBook", "Vouchers", "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances",
            "FixedAssets"
        };

        var allGood = true;
        var tablesWith40Plus = 0;
        var tablesWithData = 0;
        var emptyTables = 0;

        foreach (var table in tables)
        {
            try
            {
                var countCommand = new SqlCommand($"SELECT COUNT(*) FROM [{table}]", connection);
                var count = (int)countCommand.ExecuteScalar();

                var status = count >= 40 ? "✅" : count > 0 ? "⚠️ " : "❌";

                if (count >= 40) tablesWith40Plus++;
                if (count > 0) tablesWithData++;
                if (count == 0) emptyTables++;

                if (count < 40) allGood = false;

                Console.WriteLine($"  {status} {table,-30} {count,5} records");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ❌ {table,-30} ERROR: {ex.Message}");
            }
        }

        Console.WriteLine($"\n{'═',60}");
        Console.WriteLine("📈 FINAL SUMMARY:");
        Console.WriteLine($"{'═',60}");
        Console.WriteLine($"Total Tables: {tables.Length}");
        Console.WriteLine($"Tables with 40+ records: {tablesWith40Plus} ({tablesWith40Plus * 100 / tables.Length}%)");
        Console.WriteLine($"Tables with data: {tablesWithData} ({tablesWithData * 100 / tables.Length}%)");
        Console.WriteLine($"Empty tables: {emptyTables}");
        Console.WriteLine();

        if (allGood && emptyTables == 0)
        {
            Console.WriteLine("🎉 SUCCESS! All tables now have 40+ records!");
        }
        else if (tablesWith40Plus > 6)
        {
            Console.WriteLine("✅ PROGRESS! More tables now have sufficient data!");
            Console.WriteLine("⚠️  Some tables may still need more records.");
        }
        else
        {
            Console.WriteLine("⚠️  WARNING: Some tables still don't have enough data.");
            Console.WriteLine("   This might be due to foreign key constraints or existing data.");
        }

        Console.WriteLine($"\n{'═',60}");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ FATAL ERROR: {ex.Message}");
    Console.WriteLine($"\nStack Trace:\n{ex.StackTrace}");
    Environment.Exit(1);
}

Console.WriteLine("\n✨ Script execution completed!");
