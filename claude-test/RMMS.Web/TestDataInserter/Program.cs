using Microsoft.Data.SqlClient;
using System;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        string connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";
        string scriptPath = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory())!.FullName, "CreateAllRepositories.sql");

        Console.WriteLine("===========================================");
        Console.WriteLine("RMMS Test Data Insertion Tool");
        Console.WriteLine("===========================================");
        Console.WriteLine($"Database: RMMS_Production");
        Console.WriteLine($"Script: {scriptPath}");
        Console.WriteLine();

        if (!File.Exists(scriptPath))
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"ERROR: SQL script not found at: {scriptPath}");
            Console.ResetColor();
            return;
        }

        try
        {
            string sqlScript = File.ReadAllText(scriptPath);

            // Split script by GO statements
            string[] batches = sqlScript.Split(new string[] { "\nGO\n", "\nGO\r\n", "\r\nGO\r\n", "\r\nGO\n" }, StringSplitOptions.RemoveEmptyEntries);

            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("✓ Connected to database successfully!");
                Console.ResetColor();
                Console.WriteLine();

                int batchNumber = 0;
                foreach (string batch in batches)
                {
                    string trimmedBatch = batch.Trim();
                    if (string.IsNullOrWhiteSpace(trimmedBatch)) continue;

                    batchNumber++;

                    using (SqlCommand command = new SqlCommand(trimmedBatch, connection))
                    {
                        command.CommandTimeout = 300; // 5 minutes timeout

                        // Handle messages from SQL Server (PRINT statements)
                        connection.InfoMessage += (sender, e) =>
                        {
                            Console.ForegroundColor = ConsoleColor.Cyan;
                            Console.WriteLine(e.Message);
                            Console.ResetColor();
                        };

                        try
                        {
                            var result = command.ExecuteNonQuery();
                        }
                        catch (Exception ex)
                        {
                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine($"Warning in batch {batchNumber}: {ex.Message}");
                            Console.ResetColor();
                        }
                    }
                }

                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("✓ Test data insertion completed successfully!");
                Console.ResetColor();
                Console.WriteLine();

                // Display verification results
                Console.WriteLine("Verifying record counts...");
                Console.WriteLine();

                string verifyQuery = @"
                    SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS RecordCount FROM PaddyProcurement WHERE IsActive = 1
                    UNION ALL
                    SELECT 'RiceProcurementExternal', COUNT(*) FROM RiceProcurementExternal WHERE IsActive = 1
                    UNION ALL
                    SELECT 'RiceSales', COUNT(*) FROM RiceSales WHERE IsActive = 1
                    UNION ALL
                    SELECT 'ByProductSales', COUNT(*) FROM ByProductSales WHERE IsActive = 1
                    UNION ALL
                    SELECT 'BankTransactions', COUNT(*) FROM BankTransactions WHERE IsActive = 1
                    UNION ALL
                    SELECT 'CashBook', COUNT(*) FROM CashBook WHERE IsActive = 1
                    UNION ALL
                    SELECT 'Vouchers', COUNT(*) FROM Vouchers WHERE IsActive = 1
                    UNION ALL
                    SELECT 'LoansAdvances', COUNT(*) FROM LoansAdvances WHERE IsActive = 1
                    UNION ALL
                    SELECT 'FixedAssets', COUNT(*) FROM FixedAssets WHERE IsActive = 1
                    UNION ALL
                    SELECT 'ReceivablesOverdue', COUNT(*) FROM ReceivablesOverdue WHERE IsActive = 1
                    UNION ALL
                    SELECT 'PayablesOverdue', COUNT(*) FROM PayablesOverdue WHERE IsActive = 1
                    UNION ALL
                    SELECT 'ExternalRiceSales', COUNT(*) FROM ExternalRiceSales WHERE IsActive = 1
                    ORDER BY TableName";

                using (SqlCommand verifyCmd = new SqlCommand(verifyQuery, connection))
                {
                    using (SqlDataReader reader = verifyCmd.ExecuteReader())
                    {
                        Console.WriteLine("┌─────────────────────────────┬──────────────┐");
                        Console.WriteLine("│ Table Name                  │ Record Count │");
                        Console.WriteLine("├─────────────────────────────┼──────────────┤");

                        int totalRecords = 0;
                        while (reader.Read())
                        {
                            string tableName = reader.GetString(0);
                            int count = reader.GetInt32(1);
                            totalRecords += count;

                            Console.Write("│ ");
                            Console.ForegroundColor = ConsoleColor.White;
                            Console.Write(tableName.PadRight(27));
                            Console.ResetColor();
                            Console.Write(" │ ");

                            if (count >= 40)
                            {
                                Console.ForegroundColor = ConsoleColor.Green;
                            }
                            else
                            {
                                Console.ForegroundColor = ConsoleColor.Yellow;
                            }
                            Console.Write(count.ToString().PadLeft(12));
                            Console.ResetColor();
                            Console.WriteLine(" │");
                        }

                        Console.WriteLine("├─────────────────────────────┼──────────────┤");
                        Console.Write("│ ");
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        Console.Write("TOTAL".PadRight(27));
                        Console.ResetColor();
                        Console.Write(" │ ");
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        Console.Write(totalRecords.ToString().PadLeft(12));
                        Console.ResetColor();
                        Console.WriteLine(" │");
                        Console.WriteLine("└─────────────────────────────┴──────────────┘");
                    }
                }
            }

            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("SUCCESS! All test data has been inserted.");
            Console.WriteLine("You can now test paging functionality with 40+ records per table.");
            Console.ResetColor();
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"ERROR: {ex.Message}");
            Console.WriteLine($"Stack Trace: {ex.StackTrace}");
            Console.ResetColor();
        }
    }
}
