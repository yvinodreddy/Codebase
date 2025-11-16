using Microsoft.Data.SqlClient;
using System;

class CreateDatabase
{
    static void Main()
    {
        // Connect to master database to create the new database
        var masterConnectionString = "Server=172.17.208.1,1433;Database=master;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

        try
        {
            using (var connection = new SqlConnection(masterConnectionString))
            {
                connection.Open();
                Console.WriteLine("Connected to master database");

                var sql = @"
                    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RMMS_Production')
                    BEGIN
                        CREATE DATABASE RMMS_Production;
                        PRINT 'Database RMMS_Production created successfully.';
                    END
                    ELSE
                    BEGIN
                        PRINT 'Database RMMS_Production already exists.';
                    END";

                using (var command = new SqlCommand(sql, connection))
                {
                    command.ExecuteNonQuery();
                    Console.WriteLine("Database creation command executed successfully");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            Environment.Exit(1);
        }
    }
}
