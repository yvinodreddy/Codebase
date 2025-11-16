#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[] { "Products", "Customers", "Employees", "Machines", "ProductionBatches", "PaddyProcurement" };

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();

    foreach (var table in tables)
    {
        Console.WriteLine($"\n{table} Columns:");
        Console.WriteLine("=".PadRight(60, '='));

        var cmd = new SqlCommand($@"
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION", connection);

        using (var reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                var col = reader.GetString(0);
                var type = reader.GetString(1);
                var nullable = reader.GetString(2);
                Console.WriteLine($"  {col,-30} {type,-15} {nullable}");
            }
        }
    }
}
