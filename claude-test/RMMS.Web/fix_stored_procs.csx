#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;
using System;
using System.IO;
using System.Text.RegularExpressions;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
var sqlFile = "/home/user01/claude-test/RMMS.Web/CreateMissingReportProcedures.sql";

try
{
    var sqlScript = File.ReadAllText(sqlFile);

    // Remove USE statement
    sqlScript = Regex.Replace(sqlScript, @"USE\s+\w+\s*;", "", RegexOptions.IgnoreCase);

    // Split by GO
    var batches = Regex.Split(sqlScript, @"^\s*GO\s*$",
        RegexOptions.Multiline | RegexOptions.IgnoreCase);

    using (var connection = new SqlConnection(connectionString))
    {
        connection.Open();
        Console.WriteLine($"Connected to: {connection.Database}");

        int created = 0;
        foreach (var batch in batches)
        {
            var trimmed = batch.Trim();
            if (string.IsNullOrWhiteSpace(trimmed) || (trimmed.StartsWith("--") && !trimmed.Contains("CREATE")))
                continue;

            try
            {
                using (var cmd = new SqlCommand(trimmed, connection))
                {
                    cmd.CommandTimeout = 300;
                    cmd.ExecuteNonQuery();

                    var match = Regex.Match(trimmed, @"CREATE\s+OR\s+ALTER\s+PROCEDURE\s+(\w+)", RegexOptions.IgnoreCase);
                    if (match.Success)
                    {
                        Console.WriteLine($"✓ {match.Groups[1].Value}");
                        created++;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ Error: {ex.Message.Substring(0, Math.Min(ex.Message.Length, 100))}");
            }
        }

        Console.WriteLine($"\n{created} procedures created");

        // Verify
        Console.WriteLine("\nVerifying:");
        using (var cmd = new SqlCommand("SELECT name FROM sys.procedures WHERE name LIKE 'sp_%DateRange' ORDER BY name", connection))
        using (var reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                Console.WriteLine($"  • {reader.GetString(0)}");
            }
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
