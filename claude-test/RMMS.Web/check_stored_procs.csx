#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();

    // List all stored procedures
    var cmd = new SqlCommand(@"
        SELECT ROUTINE_NAME
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE ROUTINE_TYPE = 'PROCEDURE'
        ORDER BY ROUTINE_NAME", connection);

    Console.WriteLine("Current Stored Procedures in Database:");
    Console.WriteLine("==========================================");

    int count = 0;
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read())
        {
            count++;
            Console.WriteLine($"{count}. {reader.GetString(0)}");
        }
    }

    Console.WriteLine($"\nTotal: {count} stored procedures");
}
