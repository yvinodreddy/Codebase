#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
Console.WriteLine("║         CHECKING EXISTING IDS IN KEY TABLES                ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════╝\n");

try
{
    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();

        // Check Warehouses
        var cmd = new SqlCommand("SELECT MIN(Id) AS MinId, MAX(Id) AS MaxId, COUNT(*) AS Count FROM Warehouses", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Warehouses: MinId={reader["MinId"]}, MaxId={reader["MaxId"]}, Count={reader["Count"]}");
            }
        }

        // Check StorageZones
        cmd = new SqlCommand("SELECT MIN(Id) AS MinId, MAX(Id) AS MaxId, COUNT(*) AS Count FROM StorageZones", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                var count = reader["Count"];
                Console.WriteLine($"StorageZones: Count={count}");
            }
        }

        // Check Customers
        cmd = new SqlCommand("SELECT MIN(Id) AS MinId, MAX(Id) AS MaxId, COUNT(*) AS Count FROM Customers", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Customers: MinId={reader["MinId"]}, MaxId={reader["MaxId"]}, Count={reader["Count"]}");
            }
        }

        // Check Employees
        cmd = new SqlCommand("SELECT MIN(Id) AS MinId, MAX(Id) AS MaxId, COUNT(*) AS Count FROM Employees", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Employees: MinId={reader["MinId"]}, MaxId={reader["MaxId"]}, Count={reader["Count"]}");
            }
        }

        // Check Products
        cmd = new SqlCommand("SELECT MIN(Id) AS MinId, MAX(Id) AS MaxId, COUNT(*) AS Count FROM Products", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Products: MinId={reader["MinId"]}, MaxId={reader["MaxId"]}, Count={reader["Count"]}");
            }
        }

        // Check ProductionOrders
        cmd = new SqlCommand("SELECT COUNT(*) AS Count FROM ProductionOrders", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"ProductionOrders: Count={reader["Count"]}");
            }
        }

        // Check ProductionBatches
        cmd = new SqlCommand("SELECT COUNT(*) AS Count FROM ProductionBatches", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"ProductionBatches: Count={reader["Count"]}");
            }
        }

        // Check Inquiries
        cmd = new SqlCommand("SELECT COUNT(*) AS Count FROM Inquiries", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Inquiries: Count={reader["Count"]}");
            }
        }

        // Check Quotations
        cmd = new SqlCommand("SELECT COUNT(*) AS Count FROM Quotations", connection);
        using (var reader = cmd.ExecuteReader())
        {
            if (reader.Read())
            {
                Console.WriteLine($"Quotations: Count={reader["Count"]}");
            }
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
}
