#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System.Text;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[] {
    "StockAdjustments", "ProductionOrders", "ProductionBatches", "YieldRecords",
    "Inquiries", "Quotations", "SalesOrders", "RiceSales", "ByProductSales",
    "ExternalRiceSales", "BankTransactions", "CashBook", "Vouchers",
    "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances", "FixedAssets"
};

Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
Console.WriteLine("║        COMPREHENSIVE DATABASE VERIFICATION REPORT                  ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
Console.WriteLine();

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("✅ Connected to database: RMMS_Production");
    Console.WriteLine();

    var report = new StringBuilder();
    var emptyTables = new List<string>();

    foreach (var table in tables)
    {
        Console.WriteLine($"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        Console.WriteLine($"📊 TABLE: {table}");
        Console.WriteLine($"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

        // Check if table exists
        var checkTableQuery = $@"
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = '{table}'";

        using (var cmd = new SqlCommand(checkTableQuery, connection))
        {
            var tableExists = (int)cmd.ExecuteScalar() > 0;

            if (!tableExists)
            {
                Console.WriteLine($"❌ Table does NOT exist in database!");
                Console.WriteLine();
                continue;
            }
        }

        // Get row count
        var countQuery = $"SELECT COUNT(*) FROM {table} WHERE IsActive = 1";
        int rowCount = 0;
        try
        {
            using (var cmd = new SqlCommand(countQuery, connection))
            {
                rowCount = (int)cmd.ExecuteScalar();
            }
        }
        catch
        {
            // Try without IsActive filter
            countQuery = $"SELECT COUNT(*) FROM {table}";
            using (var cmd = new SqlCommand(countQuery, connection))
            {
                rowCount = (int)cmd.ExecuteScalar();
            }
        }

        Console.WriteLine($"📈 Current Row Count: {rowCount}");

        if (rowCount == 0)
        {
            emptyTables.Add(table);
        }

        // Get column schema
        var schemaQuery = $@"
            SELECT
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION";

        Console.WriteLine();
        Console.WriteLine("📋 COLUMNS:");
        Console.WriteLine($"{"Column Name",-40} {"Type",-20} {"Nullable",-10} {"Default",-20}");
        Console.WriteLine(new string('─', 100));

        var columns = new List<string>();

        using (var cmd = new SqlCommand(schemaQuery, connection))
        using (var reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                var colName = reader["COLUMN_NAME"].ToString();
                var dataType = reader["DATA_TYPE"].ToString();
                var isNullable = reader["IS_NULLABLE"].ToString();
                var colDefault = reader["COLUMN_DEFAULT"]?.ToString() ?? "NULL";
                var maxLength = reader["CHARACTER_MAXIMUM_LENGTH"];

                if (maxLength != DBNull.Value)
                {
                    dataType += $"({maxLength})";
                }

                Console.WriteLine($"{colName,-40} {dataType,-20} {isNullable,-10} {colDefault,-20}");
                columns.Add(colName);
            }
        }

        Console.WriteLine();

        // Store for SQL generation
        report.AppendLine($"-- {table}: {rowCount} rows");
        report.AppendLine($"-- Columns: {string.Join(", ", columns)}");
        report.AppendLine();
    }

    Console.WriteLine();
    Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
    Console.WriteLine("║                        SUMMARY REPORT                              ║");
    Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
    Console.WriteLine();
    Console.WriteLine($"Total Tables Checked: {tables.Length}");
    Console.WriteLine($"Empty Tables: {emptyTables.Count}");
    Console.WriteLine();

    if (emptyTables.Count > 0)
    {
        Console.WriteLine("⚠️  EMPTY TABLES REQUIRING DATA:");
        foreach (var table in emptyTables)
        {
            Console.WriteLine($"   • {table}");
        }
    }
    else
    {
        Console.WriteLine("✅ All tables have data!");
    }

    Console.WriteLine();
    Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
}

return 0;
