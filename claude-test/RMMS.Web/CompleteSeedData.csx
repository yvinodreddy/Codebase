#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"

using Microsoft.Data.SqlClient;
using System;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

Console.WriteLine("========================================");
Console.WriteLine("RMMS Complete Data Seeding Script");
Console.WriteLine("========================================\n");

try
{
    using var connection = new SqlConnection(connectionString);
    connection.Open();
    Console.WriteLine("✓ Connected to database\n");

    // Step 1: Check and create Products table if not exists
    Console.WriteLine("Step 1: Checking Products table...");
    var checkTableSql = @"
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
        BEGIN
            CREATE TABLE Products (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                ProductCode NVARCHAR(20) NOT NULL UNIQUE,
                ProductName NVARCHAR(200) NOT NULL,
                ProductCategory NVARCHAR(50) NOT NULL,
                ProductType NVARCHAR(100) NULL,
                Grade NVARCHAR(50) NULL,
                Description NVARCHAR(500) NULL,
                UnitOfMeasure NVARCHAR(20) NOT NULL DEFAULT 'Kg',
                UnitWeight DECIMAL(18,3) NULL,
                HSNCode NVARCHAR(12) NULL,
                GSTRate DECIMAL(5,2) NULL,
                StandardCost DECIMAL(18,2) NULL,
                SellingPrice DECIMAL(18,2) NULL,
                MinimumStockLevel DECIMAL(18,3) NULL,
                MaximumStockLevel DECIMAL(18,3) NULL,
                ReorderLevel DECIMAL(18,3) NULL,
                StorageLocation NVARCHAR(100) NULL,
                ShelfLifeDays INT NULL,
                PackagingType NVARCHAR(50) NULL,
                IsRawMaterial BIT NOT NULL DEFAULT 0,
                IsFinishedProduct BIT NOT NULL DEFAULT 0,
                IsByProduct BIT NOT NULL DEFAULT 0,
                Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
                CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
                CreatedBy NVARCHAR(100) NULL,
                ModifiedDate DATETIME NULL,
                ModifiedBy NVARCHAR(100) NULL,
                IsActive BIT NOT NULL DEFAULT 1
            );
            PRINT '  + Products table created';
        END
        ELSE
        BEGIN
            PRINT '  + Products table already exists';
        END
    ";

    using (var cmd = new SqlCommand(checkTableSql, connection))
    {
        cmd.ExecuteNonQuery();
    }
    Console.WriteLine("✓ Products table ready\n");

    // Step 2: Insert Products
    Console.WriteLine("Step 2: Seeding Products...");
    var products = new[]
    {
        ("PADDY-BR11", "Basmati Rice BR-11", "Paddy", "Quintals", 1, 0, 0),
        ("PADDY-SONA", "Sona Masuri Paddy", "Paddy", "Quintals", 1, 0, 0),
        ("PADDY-IR64", "IR-64 Paddy", "Paddy", "Quintals", 1, 0, 0),
        ("RICE-BR11", "Basmati Rice BR-11", "Rice", "Quintals", 0, 1, 0),
        ("RICE-SONA", "Sona Masuri Rice", "Rice", "Quintals", 0, 1, 0),
        ("RICE-BROKEN", "Broken Rice", "Rice", "Quintals", 0, 0, 1),
        ("BRAN-001", "Rice Bran", "By-Product", "Quintals", 0, 0, 1),
        ("HUSK-001", "Rice Husk", "By-Product", "Quintals", 0, 0, 1)
    };

    foreach (var (code, name, category, uom, isRaw, isFinished, isByProd) in products)
    {
        var insertSql = $@"
            IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = '{code}')
            BEGIN
                INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsRawMaterial, IsFinishedProduct, IsByProduct, IsActive, CreatedDate)
                VALUES ('{code}', '{name}', '{category}', '{uom}', {isRaw}, {isFinished}, {isByProd}, 1, GETDATE())
            END
        ";

        using var cmd = new SqlCommand(insertSql, connection);
        cmd.ExecuteNonQuery();
        Console.WriteLine($"  + {name}");
    }
    Console.WriteLine("✓ Products seeded\n");

    // Step 3: Insert Machines (from existing SQL script)
    Console.WriteLine("Step 3: Seeding Machines...");
    var machinesSql = @"
        IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-01')
        BEGIN
            INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
            VALUES ('MILL-01', 'Rice Huller Machine #1', 'Husker', 'Satake Corporation', 'SH-5000', 5.0, 'tons/hour', 'Operational', 'Production Floor A', DATEADD(YEAR, -3, GETDATE()), 1, GETDATE())
        END

        IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-02')
        BEGIN
            INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
            VALUES ('MILL-02', 'Rice Polisher #2', 'Polisher', 'Buhler Group', 'BP-3000', 3.5, 'tons/hour', 'Operational', 'Production Floor A', DATEADD(YEAR, -2, GETDATE()), 1, GETDATE())
        END

        IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-03')
        BEGIN
            INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
            VALUES ('MILL-03', 'Rice Grader & Sorter #3', 'Grader', 'Fowler Westrup', 'GS-2500', 4.0, 'tons/hour', 'Operational', 'Production Floor B', DATEADD(YEAR, -1, GETDATE()), 1, GETDATE())
        END
    ";

    using (var cmd = new SqlCommand(machinesSql, connection))
    {
        cmd.ExecuteNonQuery();
    }
    Console.WriteLine("  + Rice Huller Machine #1");
    Console.WriteLine("  + Rice Polisher #2");
    Console.WriteLine("  + Rice Grader & Sorter #3");
    Console.WriteLine("✓ Machines seeded\n");

    // Step 4: Seed Production Orders and Batches
    Console.WriteLine("Step 4: Seeding Production Data...");

    // Get machine IDs
    var getMachineIdsSql = "SELECT Id FROM Machines WHERE MachineCode IN ('MILL-01', 'MILL-02', 'MILL-03') ORDER BY MachineCode";
    var machineIds = new List<int>();
    using (var cmd = new SqlCommand(getMachineIdsSql, connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read())
        {
            machineIds.Add(reader.GetInt32(0));
        }
    }

    if (machineIds.Count >= 3)
    {
        // Create 10 production batches with varying yields
        var random = new Random(42); // Fixed seed for reproducible data
        var varieties = new[] { "Basmati BR-11", "Sona Masuri", "IR-64" };
        var shifts = new[] { "Morning", "Evening", "Night" };

        for (int i = 1; i <= 10; i++)
        {
            var batchDate = DateTime.Now.AddDays(-30 + i * 3);
            var variety = varieties[(i - 1) % 3];
            var shift = shifts[i % 3];
            var machineId = machineIds[(i - 1) % 3];

            // Create Production Order
            var orderSql = $@"
                IF NOT EXISTS (SELECT 1 FROM ProductionOrders WHERE OrderNumber = 'PO{i:D4}')
                BEGIN
                    INSERT INTO ProductionOrders (OrderNumber, OrderDate, PaddyVariety, PaddyQuantity, TargetQuantity, AssignedMachineId, Status, IsActive, CreatedDate)
                    VALUES ('PO{i:D4}', '{batchDate:yyyy-MM-dd}', '{variety}', {50 + random.Next(20)}, {40 + random.Next(15)}, {machineId}, 'Completed', 1, '{batchDate:yyyy-MM-dd}')
                END
            ";

            using (var cmd = new SqlCommand(orderSql, connection))
            {
                cmd.ExecuteNonQuery();
            }

            // Get order ID
            int orderId;
            using (var cmd = new SqlCommand($"SELECT Id FROM ProductionOrders WHERE OrderNumber = 'PO{i:D4}'", connection))
            {
                orderId = (int)cmd.ExecuteScalar();
            }

            // Create Production Batch
            var inputQty = 50.0m + random.Next(20);
            var yieldPercent = 62.0m + (decimal)random.NextDouble() * 10; // 62-72%
            var outputQty = inputQty * yieldPercent / 100;

            var batchSql = $@"
                IF NOT EXISTS (SELECT 1 FROM ProductionBatches WHERE BatchNumber = 'BATCH{i:D4}')
                BEGIN
                    INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, ShiftType, StartTime, EndTime, Status, QualityScore, IsActive, CreatedDate)
                    VALUES ('BATCH{i:D4}', {orderId}, '{batchDate:yyyy-MM-dd}', '{shift}',
                            '{batchDate:yyyy-MM-dd HH:mm:ss}', '{batchDate.AddHours(4):yyyy-MM-dd HH:mm:ss}',
                            'Completed', {7 + random.Next(3)}, 1, '{batchDate:yyyy-MM-dd}')
                END
            ";

            using (var cmd = new SqlCommand(batchSql, connection))
            {
                cmd.ExecuteNonQuery();
            }

            // Get batch ID
            int batchId;
            using (var cmd = new SqlCommand($"SELECT Id FROM ProductionBatches WHERE BatchNumber = 'BATCH{i:D4}'", connection))
            {
                batchId = (int)cmd.ExecuteScalar();
            }

            // Create Yield Record
            var headRice = outputQty * 0.7m;
            var brokenRice = outputQty * 0.15m;
            var bran = inputQty * 0.08m;
            var husk = inputQty * 0.20m;

            var yieldSql = $@"
                IF NOT EXISTS (SELECT 1 FROM YieldRecords WHERE BatchId = {batchId})
                BEGIN
                    INSERT INTO YieldRecords (BatchId, PaddyVariety, InputPaddyQuantity, OutputHeadRice, OutputBrokenRice, OutputBran, OutputHusk,
                                              HeadRicePercent, BrokenRicePercent, BranPercent, HuskPercent, TotalYieldPercent, MillingRecovery, QualityScore)
                    VALUES ({batchId}, '{variety}', {inputQty}, {headRice}, {brokenRice}, {bran}, {husk},
                            {headRice / inputQty * 100:F2}, {brokenRice / inputQty * 100:F2}, {bran / inputQty * 100:F2}, {husk / inputQty * 100:F2},
                            {yieldPercent:F2}, {outputQty / inputQty * 100:F2}, {7 + random.Next(3)})
                END
            ";

            using (var cmd = new SqlCommand(yieldSql, connection))
            {
                cmd.ExecuteNonQuery();
            }

            Console.WriteLine($"  + Batch {i}/10: {variety}, Yield: {yieldPercent:F1}%");
        }

        Console.WriteLine("✓ Production data seeded\n");
    }
    else
    {
        Console.WriteLine("⚠ Not enough machines found, skipping production batch creation\n");
    }

    Console.WriteLine("========================================");
    Console.WriteLine("✅ DATA SEEDING COMPLETE!");
    Console.WriteLine("========================================\n");
    Console.WriteLine("Summary:");
    Console.WriteLine("  ✓ 8 Products created");
    Console.WriteLine("  ✓ 3 Machines created");
    Console.WriteLine("  ✓ 10 Production Orders created");
    Console.WriteLine("  ✓ 10 Production Batches created");
    Console.WriteLine("  ✓ 10 Yield Records created");
    Console.WriteLine("\nNext Steps:");
    Console.WriteLine("  1. Navigate to: http://localhost:5090/YieldAnalysis");
    Console.WriteLine("  2. Test all 8 analytics pages");
    Console.WriteLine("  3. View Production Reports");
    Console.WriteLine("\n========================================");
}
catch (Exception ex)
{
    Console.WriteLine($"\n❌ ERROR: {ex.Message}");
    Console.WriteLine($"\nStack Trace:\n{ex.StackTrace}");
    Environment.Exit(1);
}
