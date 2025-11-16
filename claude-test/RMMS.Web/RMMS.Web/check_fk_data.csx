#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var fkTables = new[] {
    "Products", "Warehouses", "Employees", "Machines", "Customers", "Zones"
};

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("Checking Foreign Key Tables:");
    Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    foreach (var table in fkTables)
    {
        var query = $"SELECT COUNT(*) FROM {table} WHERE IsActive = 1";
        int count = 0;

        try
        {
            using (var cmd = new SqlCommand(query, connection))
            {
                count = (int)cmd.ExecuteScalar();
            }

            Console.WriteLine($"{table,-20}: {count,4} records {(count > 0 ? "✅" : "❌")}");

            // Get first 5 IDs if available
            if (count > 0)
            {
                var idQuery = $"SELECT TOP 5 Id FROM {table} WHERE IsActive = 1 ORDER BY Id";
                using (var cmd = new SqlCommand(idQuery, connection))
                using (var reader = cmd.ExecuteReader())
                {
                    var ids = new List<int>();
                    while (reader.Read()) ids.Add(reader.GetInt32(0));
                    Console.WriteLine($"  Sample IDs: {string.Join(", ", ids)}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"{table,-20}: ERROR - {ex.Message}");
        }
    }
}

return 0;
