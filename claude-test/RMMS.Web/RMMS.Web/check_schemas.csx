#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[] { "Vendors", "Warehouses", "StockMovements", "StockAdjustments", 
                     "ProductionOrders", "ProductionBatches", "YieldRecords",
                     "Inquiries", "Quotations", "RiceSales", "ByProductSales" };

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    
    foreach (var table in tables)
    {
        Console.WriteLine($"\n{table} columns:");
        Console.WriteLine("=".PadRight(50, '='));
        
        var query = $@"
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION";
        
        using (var cmd = new SqlCommand(query, connection))
        using (var reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                Console.WriteLine($"  {reader["COLUMN_NAME"],-40} {reader["DATA_TYPE"]}");
            }
        }
    }
}
