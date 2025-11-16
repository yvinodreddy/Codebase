#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

var connStr = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=sa;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

try
{
    using (var connection = new SqlConnection(connStr))
    {
        connection.Open();

        var tables = new[] {
            "Products", "Customers", "Vendors", "Employees", "Warehouses", "StorageZones",
            "Machines", "InventoryLedger", "StockMovements", "StockAdjustments",
            "ProductionOrders", "ProductionBatches", "BatchInputs", "BatchOutputs",
            "PaddyProcurement", "RiceSales", "RiceProcurementExternal",
            "ExternalRiceSales", "ByProductSales", "CashBook", "BankTransactions",
            "Vouchers", "LoansAdvances", "FixedAssets", "PayablesOverdue",
            "ReceivablesOverdue", "Inquiries", "Quotations", "QuotationItems",
            "SalesOrders", "SalesOrderItems", "CustomerAddresses", "CustomerContacts",
            "VendorAddresses", "VendorContacts", "YieldRecords"
        };

        Console.WriteLine("=== ROW COUNTS ===\n");
        int totalRows = 0;

        foreach (var table in tables)
        {
            var cmd = new SqlCommand($"SELECT COUNT(*) FROM [{table}]", connection);
            var count = (int)cmd.ExecuteScalar();
            Console.WriteLine($"{table,-40} {count,5} rows");
            totalRows += count;
        }

        Console.WriteLine($"\n{"TOTAL",-40} {totalRows,5} rows");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"ERROR: {ex.Message}");
}
