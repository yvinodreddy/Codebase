#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.Data;

var connectionString = "Server=localhost;Database=RMMS_Production;User ID=rmms_user;Password=rmms_pass;TrustServerCertificate=True;";

Console.WriteLine("=== DATABASE PERFORMANCE BASELINE ===\n");

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    
    // Check table sizes and row counts
    Console.WriteLine("TABLE SIZES AND ROW COUNTS:");
    Console.WriteLine("─".PadRight(80, '─'));
    
    var tableQuery = @"
        SELECT 
            t.NAME AS TableName,
            p.rows AS RowCounts,
            SUM(a.total_pages) * 8 AS TotalSpaceKB,
            SUM(a.used_pages) * 8 AS UsedSpaceKB
        FROM sys.tables t
        INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
        INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
        INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
        WHERE t.is_ms_shipped = 0
        GROUP BY t.Name, p.Rows
        ORDER BY p.rows DESC";
    
    using (var cmd = new SqlCommand(tableQuery, connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read())
        {
            var table = reader["TableName"].ToString();
            var rows = reader["RowCounts"].ToString();
            var sizeKB = reader["UsedSpaceKB"].ToString();
            Console.WriteLine($"{table,-30} {rows,10} rows  {sizeKB,10} KB");
        }
    }
    
    Console.WriteLine("\n" + "─".PadRight(80, '─'));
    
    // Check existing indexes
    Console.WriteLine("\nEXISTING INDEXES:");
    Console.WriteLine("─".PadRight(80, '─'));
    
    var indexQuery = @"
        SELECT 
            t.name AS TableName,
            i.name AS IndexName,
            i.type_desc AS IndexType
        FROM sys.indexes i
        INNER JOIN sys.tables t ON i.object_id = t.object_id
        WHERE i.name IS NOT NULL 
        AND t.is_ms_shipped = 0
        ORDER BY t.name, i.name";
    
    using (var cmd = new SqlCommand(indexQuery, connection))
    using (var reader = cmd.ExecuteReader())
    {
        var count = 0;
        while (reader.Read())
        {
            var table = reader["TableName"].ToString();
            var index = reader["IndexName"].ToString();
            var type = reader["IndexType"].ToString();
            Console.WriteLine($"{table,-30} {index,-40} {type}");
            count++;
        }
        Console.WriteLine($"\nTotal Indexes: {count}");
    }
}

Console.WriteLine("\n✓ Baseline measurement complete");
