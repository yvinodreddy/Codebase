#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

// Check which script exists and is most complete
var scripts = new[] {
    "/home/user01/claude-test/RMMS.Web/INSERT_TEST_DATA.sql",
    "/home/user01/claude-test/RMMS.Web/ComprehensiveSeedData.sql",
    "/home/user01/claude-test/RMMS.Web/COMPREHENSIVE_DATA_INSERT.sql"
};

string sqlScript = null;
string selectedScript = null;
foreach (var script in scripts)
{
    if (File.Exists(script))
    {
        var lines = File.ReadAllLines(script);
        if (lines.Length > (sqlScript?.Split('\n').Length ?? 0))
        {
            sqlScript = File.ReadAllText(script);
            selectedScript = script;
        }
    }
}

if (sqlScript == null)
{
    Console.WriteLine("❌ No data insert script found!");
    return;
}

Console.WriteLine($"Using script: {Path.GetFileName(selectedScript)}");
Console.WriteLine($"Script size: {sqlScript.Length} characters\n");

// Split by GO statements
var batches = sqlScript.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n", ";GO" }, StringSplitOptions.RemoveEmptyEntries);

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("Connected to database...\n");

    int successCount = 0;
    int errorCount = 0;

    foreach (var batch in batches)
    {
        var trimmedBatch = batch.Trim();
        if (string.IsNullOrWhiteSpace(trimmedBatch)) continue;
        if (trimmedBatch.StartsWith("--") && !trimmedBatch.Contains("INSERT") && !trimmedBatch.Contains("DELETE")) continue;

        try
        {
            using (var cmd = new SqlCommand(trimmedBatch, connection))
            {
                cmd.CommandTimeout = 300;
                cmd.ExecuteNonQuery();
            }
            successCount++;
            if (trimmedBatch.Contains("INSERT"))
                Console.Write(".");
        }
        catch (Exception ex)
        {
            errorCount++;
            if (ex.Message.Contains("Cannot insert duplicate") || ex.Message.Contains("IDENTITY_INSERT"))
            {
                // Ignore duplicate/identity errors
                Console.Write("s");
            }
            else
            {
                Console.WriteLine($"\n⚠️  Error: {ex.Message}");
                Console.WriteLine($"   Batch: {trimmedBatch.Substring(0, Math.Min(150, trimmedBatch.Length))}...\n");
            }
        }
    }

    Console.WriteLine($"\n\n✅ Execution complete!");
    Console.WriteLine($"   Successful batches: {successCount}");
    Console.WriteLine($"   Errors/Skipped: {errorCount}\n");

    // Check table counts
    var tables = new[] {
        "Products", "Customers", "Vendors", "Employees", "Warehouses",
        "Machines", "ProductionOrders", "ProductionBatches", "PaddyProcurement",
        "RiceSales", "ByProductSales", "Inquiries", "Quotations", "SalesOrders"
    };

    Console.WriteLine("Table Row Counts:");
    Console.WriteLine("=================");
    foreach (var table in tables)
    {
        try
        {
            var cmd = new SqlCommand($"SELECT COUNT(*) FROM {table}", connection);
            var count = (int)cmd.ExecuteScalar();
            var status = count >= 40 ? "✅" : count > 0 ? "⚠️ " : "❌";
            Console.WriteLine($"{status} {table,-25} {count,5} rows");
        }
        catch { }
    }
}
