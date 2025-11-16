#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

Console.WriteLine("===========================================");
Console.WriteLine("RMMS Database Creator");
Console.WriteLine("===========================================\n");

// Try different connection strings
var connectionStrings = new[] {
    ("SA (YourStrong@Passw0rd)", "Server=172.17.208.1,1433;Database=master;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;Encrypt=False;"),
    ("SA (localhost)", "Server=localhost;Database=master;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;Encrypt=False;"),
    ("RMMS User (Windows Auth)", "Server=172.17.208.1,1433;Database=master;Integrated Security=True;TrustServerCertificate=True;"),
};

bool success = false;

foreach (var (name, connStr) in connectionStrings)
{
    try
    {
        Console.WriteLine($"Trying: {name}...");
        using (var connection = new SqlConnection(connStr))
        {
            connection.Open();
            Console.WriteLine($"✓ Connected using {name}");

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
                Console.WriteLine("✓ Database RMMS_Production created/verified");

                // Grant permissions to rmms_user
                var grantSql = @"
                    USE RMMS_Production;
                    IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'rmms_user')
                    BEGIN
                        CREATE USER [rmms_user] FOR LOGIN [rmms_user];
                    END
                    ALTER ROLE db_owner ADD MEMBER [rmms_user];";

                try
                {
                    using (var grantCmd = new SqlCommand(grantSql, connection))
                    {
                        grantCmd.ExecuteNonQuery();
                        Console.WriteLine("✓ Permissions granted to rmms_user");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"⚠ Warning: Could not grant permissions: {ex.Message}");
                }

                success = true;
                break;
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"✗ Failed: {ex.Message}\n");
    }
}

if (success)
{
    Console.WriteLine("\n===========================================");
    Console.WriteLine("SUCCESS! Database is ready.");
    Console.WriteLine("You can now run: dotnet run");
    Console.WriteLine("===========================================");
}
else
{
    Console.WriteLine("\n===========================================");
    Console.WriteLine("FAILED to create database.");
    Console.WriteLine("Please run CREATE_DATABASE_MANUAL.sql manually");
    Console.WriteLine("using SQL Server Management Studio or sqlcmd");
    Console.WriteLine("with administrator credentials.");
    Console.WriteLine("===========================================");
    Environment.Exit(1);
}
