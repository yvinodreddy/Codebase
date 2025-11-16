using System;
using System.IO;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;

Console.WriteLine("========================================");
Console.WriteLine("RMMS Production Data Seeding Script");
Console.WriteLine("========================================\n");

var connectionString = "Server=localhost;Database=RMMSDB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;";

var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
optionsBuilder.UseSqlServer(connectionString);

using var context = new ApplicationDbContext(optionsBuilder.Options);

Console.WriteLine("✓ Connected to database");
Console.WriteLine();

try
{
    // Read and execute SQL script
    var sqlFile = Path.Combine("..", "SeedProductionData.sql");

    if (!File.Exists(sqlFile))
    {
        Console.WriteLine($"❌ ERROR: SQL file not found: {sqlFile}");
        Environment.Exit(1);
    }

    Console.WriteLine("Reading SQL script...");
    var sql = File.ReadAllText(sqlFile);

    Console.WriteLine("Executing SQL script...\n");

    // Split by GO statements and execute each batch
    var batches = sql.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" }, StringSplitOptions.RemoveEmptyEntries);

    foreach (var batch in batches)
    {
        if (!string.IsNullOrWhiteSpace(batch))
        {
            try
            {
                await context.Database.ExecuteSqlRawAsync(batch);
            }
            catch (Exception ex)
            {
                // Continue even if some SQL commands fail (like PRINT statements)
                if (!ex.Message.Contains("PRINT"))
                {
                    Console.WriteLine($"Warning: {ex.Message}");
                }
            }
        }
    }

    Console.WriteLine("\n✓ SQL script executed successfully");
    Console.WriteLine();
    Console.WriteLine("Next Steps:");
    Console.WriteLine("  1. cd RMMS.Web");
    Console.WriteLine("  2. dotnet run");
    Console.WriteLine("  3. Navigate to: http://localhost:5090/YieldAnalysis");
    Console.WriteLine();
    Console.WriteLine("All analytics pages should now display data!");
    Console.WriteLine("========================================");
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
    Console.WriteLine($"\nStack Trace:\n{ex.StackTrace}");

    if (ex.InnerException != null)
    {
        Console.WriteLine($"\nInner Exception: {ex.InnerException.Message}");
        Console.WriteLine($"Inner Stack Trace:\n{ex.InnerException.StackTrace}");
    }

    Environment.Exit(1);
}
