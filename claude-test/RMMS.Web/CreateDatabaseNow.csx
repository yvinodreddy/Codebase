#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

Console.WriteLine("===========================================");
Console.WriteLine("Creating RMMS_Production Database");
Console.WriteLine("===========================================\n");

var masterConnStr = "Server=172.17.208.1,1433;Database=master;User Id=sa;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

try
{
    Console.WriteLine("Connecting to SQL Server...");
    using (var connection = new SqlConnection(masterConnStr))
    {
        connection.Open();
        Console.WriteLine("✓ Connected successfully\n");

        // Create database
        Console.WriteLine("Creating database...");
        var createDbSql = @"
            IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RMMS_Production')
            BEGIN
                CREATE DATABASE RMMS_Production;
                PRINT 'Database created successfully';
            END
            ELSE
            BEGIN
                PRINT 'Database already exists';
            END";

        using (var command = new SqlCommand(createDbSql, connection))
        {
            command.ExecuteNonQuery();
            Console.WriteLine("✓ Database RMMS_Production created/verified\n");
        }

        // Switch to the database and grant permissions
        Console.WriteLine("Granting permissions to rmms_user...");
        var grantSql = @"
            USE RMMS_Production;

            IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'rmms_user')
            BEGIN
                CREATE USER [rmms_user] FOR LOGIN [rmms_user];
            END

            ALTER ROLE db_owner ADD MEMBER [rmms_user];";

        using (var grantCmd = new SqlCommand(grantSql, connection))
        {
            grantCmd.ExecuteNonQuery();
            Console.WriteLine("✓ Permissions granted to rmms_user\n");
        }

        Console.WriteLine("===========================================");
        Console.WriteLine("SUCCESS! Database is ready.");
        Console.WriteLine("===========================================");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"\n✗ ERROR: {ex.Message}");
    Console.WriteLine($"\nStack Trace:\n{ex.StackTrace}");
    Environment.Exit(1);
}
