#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();

    // Get all tables and row counts
    var cmd = new SqlCommand(@"
        SELECT
            t.TABLE_NAME,
            ISNULL(p.rows, 0) AS [RowCnt]
        FROM INFORMATION_SCHEMA.TABLES t
        LEFT JOIN sys.tables st ON st.name = t.TABLE_NAME
        LEFT JOIN sys.partitions p ON st.object_id = p.object_id AND p.index_id IN (0,1)
        WHERE t.TABLE_TYPE = 'BASE TABLE'
        AND t.TABLE_NAME NOT LIKE '__EFMigrationsHistory'
        ORDER BY t.TABLE_NAME", connection);

    Console.WriteLine("DATABASE TABLES AND ROW COUNTS");
    Console.WriteLine("=".PadRight(60, '='));
    Console.WriteLine($"{"Table Name",-40} {"Row Count",10}");
    Console.WriteLine("-".PadRight(60, '-'));

    int totalTables = 0;
    int emptyTables = 0;
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read())
        {
            totalTables++;
            var tableName = reader.GetString(0);
            var rowCount = reader.IsDBNull(1) ? 0 : (int)reader.GetInt64(1);

            if (rowCount == 0) emptyTables++;

            var status = rowCount >= 40 ? "✅" : rowCount > 0 ? "⚠️ " : "❌";
            Console.WriteLine($"{status} {tableName,-38} {rowCount,10}");
        }
    }

    Console.WriteLine("=".PadRight(60, '='));
    Console.WriteLine($"Total Tables: {totalTables}");
    Console.WriteLine($"Empty Tables: {emptyTables}");
    Console.WriteLine($"Tables with <40 records: {totalTables - emptyTables}");
}
