#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[] {
    "StockMovements", "Inquiries", "Quotations", "SalesOrders"
};

Console.WriteLine("Checking record counts for tables with pagination issues:");
Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();

    foreach (var table in tables)
    {
        try
        {
            var query = $"SELECT COUNT(*) FROM {table} WHERE IsActive = 1";
            using (var cmd = new SqlCommand(query, connection))
            {
                var count = (int)cmd.ExecuteScalar();
                var status = count > 16 ? "✅ SHOULD SHOW PAGINATION" : "⚠️  < 16 records (pagination hidden)";
                Console.WriteLine($"{table,-25}: {count,3} records - {status}");
            }
        }
        catch
        {
            try
            {
                var query = $"SELECT COUNT(*) FROM {table}";
                using (var cmd = new SqlCommand(query, connection))
                {
                    var count = (int)cmd.ExecuteScalar();
                    var status = count > 16 ? "✅ SHOULD SHOW PAGINATION" : "⚠️  < 16 records (pagination hidden)";
                    Console.WriteLine($"{table,-25}: {count,3} records - {status}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"{table,-25}: ERROR - {ex.Message}");
            }
        }
    }
}

return 0;
