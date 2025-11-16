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

        Console.WriteLine("=== TABLES ===");
        var tablesCmd = new SqlCommand(@"
            SELECT TABLE_NAME,
                   (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = t.TABLE_NAME) as ColumnCount
            FROM INFORMATION_SCHEMA.TABLES t
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME", connection);

        using (var reader = tablesCmd.ExecuteReader())
        {
            while (reader.Read())
            {
                Console.WriteLine($"{reader["TABLE_NAME"],-40} ({reader["ColumnCount"]} columns)");
            }
        }

        Console.WriteLine("\n=== STORED PROCEDURES ===");
        var procsCmd = new SqlCommand(@"
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_NAME", connection);

        using (var reader = procsCmd.ExecuteReader())
        {
            int count = 0;
            while (reader.Read())
            {
                Console.WriteLine(reader["ROUTINE_NAME"]);
                count++;
            }
            if (count == 0) Console.WriteLine("(No stored procedures found)");
        }

        Console.WriteLine("\n=== ROW COUNTS ===");
        var countCmd = new SqlCommand(@"
            SELECT t.NAME AS TableName,
                   p.rows AS RowCount
            FROM sys.tables t
            INNER JOIN sys.partitions p ON t.object_id = p.OBJECT_ID
            WHERE p.index_id IN (0,1)
            AND t.is_ms_shipped = 0
            ORDER BY t.NAME", connection);

        using (var reader = countCmd.ExecuteReader())
        {
            while (reader.Read())
            {
                Console.WriteLine($"{reader["TableName"],-40} {reader["RowCount"],10} rows");
            }
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine($"ERROR: {ex.Message}");
}
