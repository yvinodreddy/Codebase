#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var tables = new[] {
    // Sales
    "Inquiries", "Quotations", "SalesOrders",
    // Sales Tracking
    "RiceSales", "ByProductSales", "ExternalRiceSales",
    // Finance
    "BankTransactions", "CashBook", "Vouchers",
    "PayablesOverdue", "ReceivablesOverdue", "LoansAdvances",
    // Assets
    "FixedAssets"
};

Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
Console.WriteLine("║            CHECKING ALL TABLE DATA COUNTS                          ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
Console.WriteLine();

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
                var status = count >= 40 ? "✅" : (count > 0 ? "⚠️ " : "❌");
                Console.WriteLine($"{table,-30}: {count,4} records {status}");
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
                    var status = count >= 40 ? "✅" : (count > 0 ? "⚠️ " : "❌");
                    Console.WriteLine($"{table,-30}: {count,4} records {status}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"{table,-30}: ERROR - {ex.Message}");
            }
        }
    }
}

return 0;
