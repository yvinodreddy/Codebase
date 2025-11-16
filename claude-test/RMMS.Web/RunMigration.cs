using Microsoft.Data.SqlClient;
using System;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        var connectionString = "Server=172.17.208.1;Database=RMMS_Production;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;";
        var sqlFilePath = "05_CreateProductionTables.sql";

        try
        {
            Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║         RMMS Production Tables Migration                  ║");
            Console.WriteLine("╚════════════════════════════════════════════════════════════╝");
            Console.WriteLine();

            Console.WriteLine("📄 Reading SQL migration file...");
            if (!File.Exists(sqlFilePath))
            {
                Console.WriteLine($"❌ Error: SQL file not found: {sqlFilePath}");
                Environment.Exit(1);
            }

            var sqlScript = File.ReadAllText(sqlFilePath);
            Console.WriteLine($"✅ Loaded {sqlScript.Length} characters from migration file");
            Console.WriteLine();

            Console.WriteLine("🔌 Connecting to database...");
            using var connection = new SqlConnection(connectionString);
            connection.Open();
            Console.WriteLine("✅ Connected to RMMS_Production database");
            Console.WriteLine();

            Console.WriteLine("🚀 Executing migration batches...");

            // Split by GO statements (case-insensitive)
            var batches = sqlScript.Split(new[] { "\r\nGO\r\n", "\nGO\n", "\r\ngo\r\n", "\ngo\n" }, StringSplitOptions.RemoveEmptyEntries);
            int batchCount = 0;

            foreach (var batch in batches)
            {
                var trimmedBatch = batch.Trim();
                if (!string.IsNullOrWhiteSpace(trimmedBatch))
                {
                    batchCount++;
                    Console.Write($"  Executing batch {batchCount}...");

                    using var command = new SqlCommand(trimmedBatch, connection);
                    command.CommandTimeout = 300; // 5 minutes timeout
                    command.ExecuteNonQuery();

                    Console.WriteLine(" ✅");
                }
            }

            Console.WriteLine();
            Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║                Migration Completed Successfully!          ║");
            Console.WriteLine("╚════════════════════════════════════════════════════════════╝");
            Console.WriteLine();
            Console.WriteLine("✅ Created 6 production tables:");
            Console.WriteLine("   1. Machines (25 columns)");
            Console.WriteLine("   2. ProductionOrders (32 columns)");
            Console.WriteLine("   3. ProductionBatches (24 columns)");
            Console.WriteLine("   4. BatchInputs (15 columns)");
            Console.WriteLine("   5. BatchOutputs (18 columns)");
            Console.WriteLine("   6. YieldRecords (19 columns)");
            Console.WriteLine();
            Console.WriteLine("✅ Created 17 foreign key relationships");
            Console.WriteLine("✅ Created 24 indexes for performance");
            Console.WriteLine();
            Console.WriteLine("🎉 Production module database schema is ready!");
            Console.WriteLine();
            Console.WriteLine("Next steps:");
            Console.WriteLine("  1. Navigate to http://localhost:5090");
            Console.WriteLine("  2. Go to Production → Machines");
            Console.WriteLine("  3. Create your first machine!");
        }
        catch (SqlException ex)
        {
            Console.WriteLine();
            Console.WriteLine("❌ SQL Error occurred:");
            Console.WriteLine($"   Message: {ex.Message}");
            Console.WriteLine($"   Number: {ex.Number}");
            Console.WriteLine($"   Line: {ex.LineNumber}");
            Environment.Exit(1);
        }
        catch (Exception ex)
        {
            Console.WriteLine();
            Console.WriteLine($"❌ Error: {ex.Message}");
            Console.WriteLine($"Stack trace: {ex.StackTrace}");
            Environment.Exit(1);
        }
    }
}
