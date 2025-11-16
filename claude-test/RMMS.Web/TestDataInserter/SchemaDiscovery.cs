using Microsoft.Data.SqlClient;
using System;
using System.Data;

class SchemaDiscovery
{
    public static void DiscoverAndInsert()
    {
        string connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            conn.Open();
            Console.WriteLine("Discovering database schema...\n");

            // Get all table names
            string tableQuery = @"
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME NOT LIKE '%sysdiagrams%'
                ORDER BY TABLE_NAME";

            using (SqlCommand cmd = new SqlCommand(tableQuery, conn))
            {
                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    Console.WriteLine("Tables in database:");
                    Console.WriteLine("===================");
                    while (reader.Read())
                    {
                        Console.WriteLine($"  - {reader["TABLE_NAME"]}");
                    }
                }
            }

            Console.WriteLine("\nChecking ByProductSales columns:");
            Console.WriteLine("=================================");
            CheckTableColumns(conn, "ByProductSales");

            Console.WriteLine("\nChecking ExternalRiceSales columns:");
            Console.WriteLine("====================================");
            CheckTableColumns(conn, "ExternalRiceSales");

            Console.WriteLine("\nChecking LoansAdvances columns:");
            Console.WriteLine("================================");
            CheckTableColumns(conn, "LoansAdvances");

            Console.WriteLine("\nChecking FixedAssets columns:");
            Console.WriteLine("==============================");
            CheckTableColumns(conn, "FixedAssets");

            Console.WriteLine("\nChecking Vouchers columns:");
            Console.WriteLine("===========================");
            CheckTableColumns(conn, "Vouchers");

            Console.WriteLine("\nChecking ReceivablesOverdue columns:");
            Console.WriteLine("=====================================");
            CheckTableColumns(conn, "ReceivablesOverdue");

            Console.WriteLine("\nChecking PayablesOverdue columns:");
            Console.WriteLine("==================================");
            CheckTableColumns(conn, "PayablesOverdue");

            Console.WriteLine("\nChecking RiceProcurementExternal columns:");
            Console.WriteLine("==========================================");
            CheckTableColumns(conn, "RiceProcurementExternal");
        }
    }

    static void CheckTableColumns(SqlConnection conn, string tableName)
    {
        string columnQuery = @"
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = @TableName
            ORDER BY ORDINAL_POSITION";

        using (SqlCommand cmd = new SqlCommand(columnQuery, conn))
        {
            cmd.Parameters.AddWithValue("@TableName", tableName);
            using (SqlDataReader reader = cmd.ExecuteReader())
            {
                if (!reader.HasRows)
                {
                    Console.WriteLine($"  ⚠ Table '{tableName}' not found!");
                    return;
                }

                while (reader.Read())
                {
                    Console.WriteLine($"  {reader["COLUMN_NAME"],-30} {reader["DATA_TYPE"],-15} {reader["IS_NULLABLE"]}");
                }
            }
        }
    }
}
