#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Linq;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var emptyTables = new[] {
    "BankTransactions", "BatchInputs", "BatchOutputs", "ByProductSales", "CashBook",
    "CustomerAddresses", "CustomerContacts", "ExternalRiceSales", "FixedAssets",
    "Inquiries", "LoansAdvances", "PayablesOverdue", "ProductionBatches", "ProductionOrders",
    "QuotationItems", "Quotations", "ReceivablesOverdue", "RiceProcurementExternal",
    "RiceSales", "SalesOrderItems", "SalesOrders", "StockAdjustments", "StorageZones",
    "VendorAddresses", "VendorContacts", "Vouchers", "YieldRecords"
};

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();

    foreach (var table in emptyTables.Take(10)) // First 10 tables
    {
        Console.WriteLine($"\n--- {table} ---");

        var cmd = new SqlCommand($@"
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE,
                   COLUMNPROPERTY(OBJECT_ID(TABLE_NAME), COLUMN_NAME, 'IsIdentity') AS IsIdentity
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION", connection);

        var columns = new List<string>();
        var identityCol = "";

        using (var reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                var col = reader.GetString(0);
                var type = reader.GetString(1);
                var nullable = reader.GetString(2) == "YES" ? "NULL" : "NOT NULL";
                var isIdentity = reader.GetInt32(3) == 1;

                if (isIdentity)
                    identityCol = col;
                else if (col != "CreatedDate" && col != "ModifiedDate" && col != "CreatedBy" && col != "ModifiedBy")
                    columns.Add(col);
            }
        }

        Console.WriteLine($"Columns: {string.Join(", ", columns)}");
        if (!string.IsNullOrEmpty(identityCol))
            Console.WriteLine($"Identity: {identityCol}");
    }
}
