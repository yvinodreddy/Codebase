using System;
using System.Data;
using Microsoft.Data.SqlClient;

class DbValidator
{
    static void Main(string[] args)
    {
        string connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

        try
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                Console.WriteLine("✅ Database connection successful!\n");

                // Get all tables
                Console.WriteLine("=== TABLES ===");
                using (SqlCommand cmd = new SqlCommand(@"
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME", conn))
                {
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        int count = 0;
                        while (reader.Read())
                        {
                            count++;
                            Console.WriteLine($"{count}. {reader["TABLE_NAME"]}");
                        }
                        Console.WriteLine($"\nTotal Tables: {count}\n");
                    }
                }

                // Get all stored procedures
                Console.WriteLine("=== STORED PROCEDURES ===");
                using (SqlCommand cmd = new SqlCommand(@"
                    SELECT ROUTINE_NAME
                    FROM INFORMATION_SCHEMA.ROUTINES
                    WHERE ROUTINE_TYPE = 'PROCEDURE'
                    ORDER BY ROUTINE_NAME", conn))
                {
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        int count = 0;
                        while (reader.Read())
                        {
                            count++;
                            Console.WriteLine($"{count}. {reader["ROUTINE_NAME"]}");
                        }
                        Console.WriteLine($"\nTotal Stored Procedures: {count}\n");
                    }
                }

                // Test a simple query
                Console.WriteLine("=== DATABASE INFO ===");
                using (SqlCommand cmd = new SqlCommand("SELECT DB_NAME() AS DatabaseName, @@VERSION AS Version", conn))
                {
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            Console.WriteLine($"Database: {reader["DatabaseName"]}");
                            Console.WriteLine($"SQL Server Version: {reader["Version"]?.ToString()?.Split('\n')[0]}");
                        }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
            Console.WriteLine($"Stack Trace: {ex.StackTrace}");
        }
    }
}
