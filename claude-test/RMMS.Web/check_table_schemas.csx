#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[]
{
    "Vendors", "Warehouses", "StorageZones", "StockMovements", "StockAdjustments",
    "ProductionOrders", "ProductionBatches", "BatchInputs", "BatchOutputs", "YieldRecords",
    "RiceProcurementExternal", "Inquiries", "Quotations", "QuotationItems",
    "SalesOrders", "SalesOrderItems", "RiceSales", "Vouchers",
    "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances"
};

Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
Console.WriteLine("║         DATABASE SCHEMA ANALYSIS                           ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════╝\n");

try
{
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();

        foreach (var table in tables)
        {
            Console.WriteLine($"\n📋 {table}:");
            Console.WriteLine("─────────────────────────────────────────────");

            var query = $@"
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE,
                       COLUMNPROPERTY(OBJECT_ID(TABLE_NAME), COLUMN_NAME, 'IsIdentity') AS IsIdentity
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table}'
                ORDER BY ORDINAL_POSITION";

            using (var command = new SqlCommand(query, connection))
            using (var reader = command.ExecuteReader())
            {
                var columns = new List<string>();
                while (reader.Read())
                {
                    var colName = reader["COLUMN_NAME"].ToString();
                    var dataType = reader["DATA_TYPE"].ToString();
                    var isNullable = reader["IS_NULLABLE"].ToString();
                    var isIdentity = reader["IsIdentity"].ToString() == "1";

                    if (!isIdentity && colName != "Id")
                    {
                        columns.Add(colName);
                    }
                }

                if (columns.Count > 0)
                {
                    Console.WriteLine($"  Columns: {string.Join(", ", columns)}");
                }
                else
                {
                    Console.WriteLine($"  ⚠️  No columns found or table doesn't exist");
                }
            }
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
}
