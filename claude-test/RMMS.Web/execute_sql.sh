#!/bin/bash
# Script to execute SQL file using dotnet and Microsoft.Data.SqlClient

cd "$(dirname "$0")"

# Create a temporary C# console app to execute the SQL
cat > /tmp/ExecuteSQL.cs << 'EOF'
using Microsoft.Data.SqlClient;
using System;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Usage: dotnet script <connection-string> <sql-file>");
            return;
        }

        string connectionString = args[0];
        string sqlFile = args[1];

        try
        {
            string sqlScript = File.ReadAllText(sqlFile);

            // Split the script by GO statements
            string[] batches = sqlScript.Split(new[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" },
                StringSplitOptions.RemoveEmptyEntries);

            using (var connection = new SqlConnection(connectionString))
            {
                connection.Open();
                Console.WriteLine("Connected to database successfully!");

                int batchNumber = 1;
                foreach (var batch in batches)
                {
                    var trimmedBatch = batch.Trim();
                    if (string.IsNullOrWhiteSpace(trimmedBatch) || trimmedBatch.StartsWith("--"))
                        continue;

                    try
                    {
                        using (var command = new SqlCommand(trimmedBatch, connection))
                        {
                            command.CommandTimeout = 300;
                            command.ExecuteNonQuery();
                            Console.WriteLine($"Batch {batchNumber} executed successfully");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error in batch {batchNumber}: {ex.Message}");
                    }
                    batchNumber++;
                }

                Console.WriteLine("SQL script executed successfully!");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            Environment.Exit(1);
        }
    }
}
EOF

# Create a temporary project file
cat > /tmp/ExecuteSQL.csproj << 'EOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Data.SqlClient" Version="5.1.1" />
  </ItemGroup>
</Project>
EOF

# Execute the C# program
CONNECTION_STRING="Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;"
SQL_FILE="$PWD/CreateMissingReportProcedures.sql"

echo "Executing SQL file: $SQL_FILE"
cd /tmp
dotnet run --project ExecuteSQL.csproj "$CONNECTION_STRING" "$SQL_FILE"

# Cleanup
rm -f ExecuteSQL.cs ExecuteSQL.csproj
