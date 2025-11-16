#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new List<string>
{
    // Master Data
    "Customers", "Vendors", "Products", "Employees",

    // Inventory
    "Warehouses", "StorageZones", "InventoryLedger", "StockMovements", "StockAdjustments",

    // Production
    "Machines", "ProductionOrders", "ProductionBatches", "BatchInputs", "BatchOutputs", "YieldRecords",

    // Procurement
    "PaddyProcurement", "RiceProcurementExternal",

    // Sales
    "Inquiries", "Quotations", "QuotationItems", "SalesOrders", "SalesOrderItems",
    "RiceSales", "ByProductSales", "ExternalRiceSales",

    // Finance
    "BankTransactions", "CashBook", "Vouchers", "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances",

    // Assets
    "FixedAssets"
};

Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
Console.WriteLine("║           RMMS DATABASE - TABLE ROW COUNTS                 ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════╝\n");

try
{
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();

        var results = new Dictionary<string, int>();

        foreach (var table in tables)
        {
            try
            {
                var command = new SqlCommand($"SELECT COUNT(*) FROM [{table}]", connection);
                var count = (int)command.ExecuteScalar();
                results[table] = count;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ {table}: ERROR - {ex.Message}");
            }
        }

        // Display results by section
        Console.WriteLine("\n📊 MASTER DATA SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "Customers");
        DisplayTableCount(results, "Vendors");
        DisplayTableCount(results, "Products");
        DisplayTableCount(results, "Employees");

        Console.WriteLine("\n📦 INVENTORY SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "Warehouses");
        DisplayTableCount(results, "StorageZones");
        DisplayTableCount(results, "InventoryLedger");
        DisplayTableCount(results, "StockMovements");
        DisplayTableCount(results, "StockAdjustments");

        Console.WriteLine("\n🏭 PRODUCTION SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "Machines");
        DisplayTableCount(results, "ProductionOrders");
        DisplayTableCount(results, "ProductionBatches");
        DisplayTableCount(results, "BatchInputs");
        DisplayTableCount(results, "BatchOutputs");
        DisplayTableCount(results, "YieldRecords");

        Console.WriteLine("\n🛒 PROCUREMENT SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "PaddyProcurement");
        DisplayTableCount(results, "RiceProcurementExternal");

        Console.WriteLine("\n💰 SALES SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "Inquiries");
        DisplayTableCount(results, "Quotations");
        DisplayTableCount(results, "QuotationItems");
        DisplayTableCount(results, "SalesOrders");
        DisplayTableCount(results, "SalesOrderItems");
        DisplayTableCount(results, "RiceSales");
        DisplayTableCount(results, "ByProductSales");
        DisplayTableCount(results, "ExternalRiceSales");

        Console.WriteLine("\n💵 FINANCE SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "BankTransactions");
        DisplayTableCount(results, "CashBook");
        DisplayTableCount(results, "Vouchers");
        DisplayTableCount(results, "PayablesOverdue");
        DisplayTableCount(results, "ReceivablesOverdue");
        DisplayTableCount(results, "LoansAdvances");

        Console.WriteLine("\n🏢 ASSETS SECTION:");
        Console.WriteLine("─────────────────────────────────────────────");
        DisplayTableCount(results, "FixedAssets");

        // Summary
        var totalTables = results.Count;
        var tablesWithData = results.Count(r => r.Value > 0);
        var tablesWith40Plus = results.Count(r => r.Value >= 40);
        var emptyTables = results.Count(r => r.Value == 0);

        Console.WriteLine("\n\n📈 SUMMARY:");
        Console.WriteLine("═════════════════════════════════════════════");
        Console.WriteLine($"Total Tables Checked: {totalTables}");
        Console.WriteLine($"Tables with Data: {tablesWithData} ({tablesWithData * 100 / totalTables}%)");
        Console.WriteLine($"Tables with 40+ records: {tablesWith40Plus} ({tablesWith40Plus * 100 / totalTables}%)");
        Console.WriteLine($"Empty Tables: {emptyTables}");

        Console.WriteLine("\n🎯 TABLES NEEDING MORE DATA (< 40 records):");
        Console.WriteLine("─────────────────────────────────────────────");
        foreach (var kvp in results.Where(r => r.Value > 0 && r.Value < 40).OrderBy(r => r.Value))
        {
            Console.WriteLine($"  {kvp.Key}: {kvp.Value} records (need {40 - kvp.Value} more)");
        }

        Console.WriteLine("\n❌ EMPTY TABLES:");
        Console.WriteLine("─────────────────────────────────────────────");
        foreach (var kvp in results.Where(r => r.Value == 0))
        {
            Console.WriteLine($"  {kvp.Key}: 0 records");
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ CONNECTION ERROR: {ex.Message}");
}

void DisplayTableCount(Dictionary<string, int> results, string tableName)
{
    if (results.ContainsKey(tableName))
    {
        var count = results[tableName];
        var status = count >= 40 ? "✅" : count > 0 ? "⚠️ " : "❌";
        Console.WriteLine($"  {status} {tableName,-30} {count,5} records");
    }
}
