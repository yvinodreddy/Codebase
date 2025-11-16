using Microsoft.Data.SqlClient;
using System;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        var masterConnectionString = "Server=172.17.208.1,1433;Database=master;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;Encrypt=False;";
        var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;Encrypt=False;";
        var scriptPath = "/home/user01/claude-test/RMMS.Web/DbSetup/CREATE_STOCK_MOVEMENTS_TABLE.sql";

        Console.WriteLine("==================================================");
        Console.WriteLine("RMMS Database Initialization");
        Console.WriteLine("==================================================");
        Console.WriteLine();

        try
        {
            // First, create the database if it doesn't exist
            Console.WriteLine("Creating database if it doesn't exist...");
            using (var connection = new SqlConnection(masterConnectionString))
            {
                connection.Open();
                var createDbSql = @"
                    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RMMS_Production')
                    BEGIN
                        CREATE DATABASE RMMS_Production;
                    END";

                using (var command = new SqlCommand(createDbSql, connection))
                {
                    command.ExecuteNonQuery();
                }
            }
            Console.WriteLine("✓ Database created or already exists");
            Console.WriteLine();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Warning creating database: {ex.Message}");
            Console.WriteLine();
        }

        try
        {
            Console.WriteLine("Reading SQL script...");
            var sqlScript = File.ReadAllText(scriptPath);
            Console.WriteLine($"✓ Script loaded ({sqlScript.Length} characters)");
            Console.WriteLine();

            Console.WriteLine("Connecting to database...");
            using (var connection = new SqlConnection(connectionString))
            {
                connection.Open();
                Console.WriteLine("✓ Connected to RMMS_Production");
                Console.WriteLine();

                // Split by GO and execute each batch
                var batches = sqlScript.Replace("\r\n", "\n").Split(new[] { "\nGO\n", "\nGO\r\n" }, StringSplitOptions.None);

                int batchCount = 0;
                int successCount = 0;

                foreach (var batch in batches)
                {
                    var trimmedBatch = batch.Trim();
                    if (string.IsNullOrWhiteSpace(trimmedBatch) || trimmedBatch.StartsWith("--"))
                        continue;

                    batchCount++;
                    try
                    {
                        using (var command = new SqlCommand(trimmedBatch, connection))
                        {
                            command.CommandTimeout = 120;

                            // Handle PRINT statements
                            connection.InfoMessage += (sender, e) =>
                            {
                                Console.WriteLine(e.Message);
                            };

                            command.ExecuteNonQuery();
                            successCount++;
                        }
                    }
                    catch (Exception ex)
                    {
                        // Ignore "already exists" errors
                        if (!ex.Message.Contains("already an object") &&
                            !ex.Message.Contains("already exists"))
                        {
                            Console.WriteLine($"Warning: {ex.Message}");
                        }
                    }
                }

                Console.WriteLine();
                Console.WriteLine($"✓ Processed {batchCount} batches, {successCount} succeeded");
                Console.WriteLine();
                Console.WriteLine("==================================================");
                Console.WriteLine("DATABASE INITIALIZATION COMPLETE!");
                Console.WriteLine("==================================================");
                Console.WriteLine();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine();
            Console.WriteLine($"ERROR: {ex.Message}");
            Console.WriteLine();
            Console.WriteLine("Details: " + ex.ToString());
            Environment.Exit(1);
        }
    }
}
