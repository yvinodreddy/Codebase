using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Production;
using RMMS.Models.Masters;
using RMMS.Models.Inventory;

namespace RMMS.DataSeeding
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("RMMS Production Data Seeding Script");
            Console.WriteLine("========================================\n");

            var connectionString = "Server=localhost;Database=RMMSDB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;";

            var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
            optionsBuilder.UseSqlServer(connectionString);

            using var context = new ApplicationDbContext(optionsBuilder.Options);

            Console.WriteLine("✓ Connected to database");
            Console.WriteLine();

            // Random number generator for realistic variations
            var random = new Random(42); // Fixed seed for reproducibility

            try
            {
                Console.WriteLine("Step 1: Creating Products...");

                // Create paddy products
                var paddyProducts = new[]
                {
                    new Product { ProductCode = "PADDY-BR11", ProductName = "Basmati Rice BR-11", Category = "Paddy", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "PADDY-PR106", ProductName = "Punjab Rice PR-106", Category = "Paddy", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "PADDY-SONA", ProductName = "Sona Masuri Paddy", Category = "Paddy", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "PADDY-IR64", ProductName = "IR-64 Paddy", Category = "Paddy", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "PADDY-SWARNA", ProductName = "Swarna Paddy", Category = "Paddy", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now }
                };

                foreach (var product in paddyProducts)
                {
                    if (!context.Products.Any(p => p.ProductCode == product.ProductCode))
                    {
                        context.Products.Add(product);
                        Console.WriteLine($"  + Added paddy: {product.ProductName}");
                    }
                }

                // Create rice products
                var riceProducts = new[]
                {
                    new Product { ProductCode = "RICE-BR11", ProductName = "Basmati Rice BR-11", Category = "Rice", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "RICE-PR106", ProductName = "Punjab Rice PR-106", Category = "Rice", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "RICE-SONA", ProductName = "Sona Masuri Rice", Category = "Rice", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "RICE-IR64", ProductName = "IR-64 Rice", Category = "Rice", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "RICE-BROKEN", ProductName = "Broken Rice", Category = "Rice", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "BRAN-001", ProductName = "Rice Bran", Category = "By-Product", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now },
                    new Product { ProductCode = "HUSK-001", ProductName = "Rice Husk", Category = "By-Product", UOM = "Quintals", IsActive = true, CreatedDate = DateTime.Now }
                };

                foreach (var product in riceProducts)
                {
                    if (!context.Products.Any(p => p.ProductCode == product.ProductCode))
                    {
                        context.Products.Add(product);
                        Console.WriteLine($"  + Added rice/byproduct: {product.ProductName}");
                    }
                }

                context.SaveChanges();
                Console.WriteLine($"✓ Products created\n");

                Console.WriteLine("Step 2: Creating Machines...");

                var machines = new[]
                {
                    new Machine
                    {
                        MachineCode = "MILL-01",
                        MachineName = "Rice Huller Machine #1",
                        MachineType = "Husker",
                        Manufacturer = "Satake Corporation",
                        ModelNumber = "SH-5000",
                        Capacity = 5.0M,
                        CapacityUnit = "tons/hour",
                        Status = "Operational",
                        Location = "Production Floor A",
                        PurchaseDate = DateTime.Now.AddYears(-3),
                        IsActive = true,
                        CreatedDate = DateTime.Now
                    },
                    new Machine
                    {
                        MachineCode = "MILL-02",
                        MachineName = "Rice Polisher #2",
                        MachineType = "Polisher",
                        Manufacturer = "Buhler Group",
                        ModelNumber = "BP-3000",
                        Capacity = 3.5M,
                        CapacityUnit = "tons/hour",
                        Status = "Operational",
                        Location = "Production Floor A",
                        PurchaseDate = DateTime.Now.AddYears(-2),
                        IsActive = true,
                        CreatedDate = DateTime.Now
                    },
                    new Machine
                    {
                        MachineCode = "MILL-03",
                        MachineName = "Rice Grader & Sorter #3",
                        MachineType = "Grader",
                        Manufacturer = "Fowler Westrup",
                        ModelNumber = "GS-2500",
                        Capacity = 4.0M,
                        CapacityUnit = "tons/hour",
                        Status = "Operational",
                        Location = "Production Floor B",
                        PurchaseDate = DateTime.Now.AddYears(-1),
                        IsActive = true,
                        CreatedDate = DateTime.Now
                    }
                };

                foreach (var machine in machines)
                {
                    if (!context.Machines.Any(m => m.MachineCode == machine.MachineCode))
                    {
                        context.Machines.Add(machine);
                        Console.WriteLine($"  + Added machine: {machine.MachineName}");
                    }
                }

                context.SaveChanges();
                Console.WriteLine($"✓ Machines created\n");

                Console.WriteLine("Step 3: Creating Warehouses...");

                var warehouses = new[]
                {
                    new Warehouse
                    {
                        WarehouseCode = "WH-MAIN",
                        WarehouseName = "Main Warehouse",
                        Type = "Storage",
                        Location = "Main Building",
                        Capacity = 5000,
                        CapacityUnit = "Quintals",
                        IsActive = true,
                        CreatedDate = DateTime.Now
                    },
                    new Warehouse
                    {
                        WarehouseCode = "WH-PROD",
                        WarehouseName = "Production Warehouse",
                        Type = "Production",
                        Location = "Production Building",
                        Capacity = 2000,
                        CapacityUnit = "Quintals",
                        IsActive = true,
                        CreatedDate = DateTime.Now
                    }
                };

                foreach (var warehouse in warehouses)
                {
                    if (!context.Warehouses.Any(w => w.WarehouseCode == warehouse.WarehouseCode))
                    {
                        context.Warehouses.Add(warehouse);
                        Console.WriteLine($"  + Added warehouse: {warehouse.WarehouseName}");
                    }
                }

                context.SaveChanges();
                Console.WriteLine($"✓ Warehouses created\n");

                // Load created data for references
                var dbPaddyProducts = context.Products.Where(p => p.Category == "Paddy").ToList();
                var dbRiceProducts = context.Products.Where(p => p.Category == "Rice" && !p.ProductCode.Contains("BROKEN")).ToList();
                var dbBrokenRice = context.Products.FirstOrDefault(p => p.ProductCode == "RICE-BROKEN");
                var dbBran = context.Products.FirstOrDefault(p => p.ProductCode == "BRAN-001");
                var dbHusk = context.Products.FirstOrDefault(p => p.ProductCode == "HUSK-001");
                var dbMachines = context.Machines.ToList();
                var dbMainWarehouse = context.Warehouses.FirstOrDefault(w => w.WarehouseCode == "WH-MAIN");
                var dbProdWarehouse = context.Warehouses.FirstOrDefault(w => w.WarehouseCode == "WH-PROD");

                Console.WriteLine("Step 4: Creating Production Orders and Batches...");
                Console.WriteLine("This will create 30 batches over the last 60 days with varying yields...\n");

                var paddyVarieties = new[] { "Basmati", "Sona Masuri", "IR-64", "Punjab Rice", "Swarna" };
                var shifts = new[] { "Morning", "Evening", "Night" };

                int batchesCreated = 0;
                int ordersCreated = 0;

                // Create 30 batches over 60 days
                for (int i = 0; i < 30; i++)
                {
                    // Pick random paddy and machine
                    var paddyProduct = dbPaddyProducts[random.Next(dbPaddyProducts.Count)];
                    var riceProduct = dbRiceProducts[random.Next(dbRiceProducts.Count)];
                    var machine = dbMachines[random.Next(dbMachines.Count)];
                    var variety = paddyVarieties[random.Next(paddyVarieties.Length)];
                    var shift = shifts[random.Next(shifts.Length)];
                    var days = random.Next(1, 60);
                    var batchDate = DateTime.Now.AddDays(-days).Date.AddHours(random.Next(0, 24));

                    // Create Production Order
                    var order = new ProductionOrder
                    {
                        OrderNumber = $"PO-{DateTime.Now.Year}-{(ordersCreated + 1):D4}",
                        OrderDate = batchDate.AddDays(-2),
                        ScheduledDate = batchDate,
                        SourceType = "Inventory",
                        PaddyProductId = paddyProduct.Id,
                        PaddyVariety = variety,
                        PaddyQuantity = random.Next(80, 120),
                        PaddyUOM = "Quintals",
                        TargetRiceProductId = riceProduct.Id,
                        TargetRiceGrade = random.Next(2) == 0 ? "Grade A" : "Premium",
                        ExpectedYieldPercent = 65.00M,
                        Priority = "Normal",
                        AssignedMachineId = machine.Id,
                        Status = "Completed",
                        ActualStartDate = batchDate,
                        ActualCompletionDate = batchDate.AddHours(random.Next(6, 12)),
                        IsActive = true,
                        CreatedDate = batchDate.AddDays(-2),
                        CreatedBy = "System"
                    };

                    context.ProductionOrders.Add(order);
                    context.SaveChanges(); // Save to get order ID
                    ordersCreated++;

                    // Create Production Batch
                    var variance = order.PaddyQuantity * (decimal)(random.NextDouble() * 0.04 - 0.02);
                    var inputQuantity = order.PaddyQuantity + variance;

                    var batch = new ProductionBatch
                    {
                        BatchNumber = $"BATCH-{DateTime.Now.Year}-{(batchesCreated + 1):D4}",
                        ProductionOrderId = order.Id,
                        BatchDate = batchDate,
                        ShiftType = shift,
                        StartTime = batchDate.AddHours(shift == "Morning" ? 7 : shift == "Evening" ? 15 : 22),
                        EndTime = batchDate.AddHours(shift == "Morning" ? 13 : shift == "Evening" ? 21 : 4).AddDays(shift == "Night" ? 1 : 0),
                        Status = "Completed",
                        CompletionPercent = 100,
                        QualityScore = 8.0M + (decimal)(random.NextDouble() * 2.4 - 1.2),
                        IsActive = true,
                        CreatedDate = batchDate,
                        CreatedBy = "System"
                    };

                    context.ProductionBatches.Add(batch);
                    context.SaveChanges(); // Save to get batch ID

                    // Create Batch Input
                    var batchInput = new BatchInput
                    {
                        BatchId = batch.Id,
                        InputType = "Paddy",
                        ProductId = paddyProduct.Id,
                        Quantity = inputQuantity,
                        UOM = "Quintals",
                        WarehouseId = dbMainWarehouse.Id,
                        MoistureContent = 14.0M + (decimal)(random.NextDouble() * 2.8 - 1.4),
                        Grade = "Grade A",
                        UnitCost = random.Next(2000, 2500),
                        CreatedDate = batchDate,
                        CreatedBy = "System"
                    };

                    context.BatchInputs.Add(batchInput);

                    // Generate yield with realistic variations
                    var headRicePercent = 65.0M + (decimal)(random.NextDouble() * 10.4 - 5.2);
                    var brokenRicePercent = 6.0M + (decimal)(random.NextDouble() * 3.6 - 1.8);
                    var branPercent = 8.0M + (decimal)(random.NextDouble() * 2.4 - 1.2);
                    var huskPercent = 20.0M + (decimal)(random.NextDouble() * 4 - 2);
                    var wastagePercent = 1.0M + (decimal)(random.NextDouble() * 1 - 0.5);

                    // Ensure realistic bounds
                    headRicePercent = Math.Max(55, Math.Min(70, headRicePercent));
                    brokenRicePercent = Math.Max(4, Math.Min(10, brokenRicePercent));
                    branPercent = Math.Max(6, Math.Min(10, branPercent));
                    huskPercent = Math.Max(18, Math.Min(23, huskPercent));
                    wastagePercent = Math.Max(0.5M, Math.Min(2, wastagePercent));

                    // Calculate actual output quantities
                    var outputHeadRice = inputQuantity * headRicePercent / 100;
                    var outputBrokenRice = inputQuantity * brokenRicePercent / 100;
                    var outputBran = inputQuantity * branPercent / 100;
                    var outputHusk = inputQuantity * huskPercent / 100;
                    var outputWastage = inputQuantity * wastagePercent / 100;

                    // Create Batch Outputs
                    var outputs = new[]
                    {
                        new BatchOutput
                        {
                            BatchId = batch.Id,
                            OutputType = "Rice",
                            ProductId = riceProduct.Id,
                            Grade = order.TargetRiceGrade,
                            Quantity = outputHeadRice,
                            UOM = "Quintals",
                            WarehouseId = dbProdWarehouse.Id,
                            QualityScore = batch.QualityScore,
                            UnitCost = random.Next(3500, 4500),
                            CreatedDate = batch.EndTime ?? batchDate.AddHours(8),
                            CreatedBy = "System"
                        },
                        new BatchOutput
                        {
                            BatchId = batch.Id,
                            OutputType = "Broken Rice",
                            ProductId = dbBrokenRice.Id,
                            Grade = "Standard",
                            Quantity = outputBrokenRice,
                            UOM = "Quintals",
                            WarehouseId = dbProdWarehouse.Id,
                            QualityScore = batch.QualityScore,
                            UnitCost = random.Next(1500, 2000),
                            CreatedDate = batch.EndTime ?? batchDate.AddHours(8),
                            CreatedBy = "System"
                        },
                        new BatchOutput
                        {
                            BatchId = batch.Id,
                            OutputType = "Bran",
                            ProductId = dbBran.Id,
                            Quantity = outputBran,
                            UOM = "Quintals",
                            WarehouseId = dbProdWarehouse.Id,
                            UnitCost = random.Next(800, 1200),
                            CreatedDate = batch.EndTime ?? batchDate.AddHours(8),
                            CreatedBy = "System"
                        },
                        new BatchOutput
                        {
                            BatchId = batch.Id,
                            OutputType = "Husk",
                            ProductId = dbHusk.Id,
                            Quantity = outputHusk,
                            UOM = "Quintals",
                            WarehouseId = dbProdWarehouse.Id,
                            UnitCost = random.Next(300, 500),
                            CreatedDate = batch.EndTime ?? batchDate.AddHours(8),
                            CreatedBy = "System"
                        }
                    };

                    foreach (var output in outputs)
                    {
                        context.BatchOutputs.Add(output);
                    }

                    // Create Yield Record
                    var yieldRecord = new YieldRecord
                    {
                        BatchId = batch.Id,
                        PaddyVariety = variety,
                        InputPaddyQuantity = inputQuantity,
                        OutputHeadRice = outputHeadRice,
                        OutputBrokenRice = outputBrokenRice,
                        OutputBran = outputBran,
                        OutputHusk = outputHusk,
                        OutputWastage = outputWastage,
                        HeadRicePercent = headRicePercent,
                        BrokenRicePercent = brokenRicePercent,
                        BranPercent = branPercent,
                        HuskPercent = huskPercent,
                        WastagePercent = wastagePercent,
                        TotalYieldPercent = headRicePercent + brokenRicePercent + branPercent + huskPercent + wastagePercent,
                        StandardHeadRicePercent = 65.00M,
                        StandardTotalYieldPercent = 98.00M,
                        QualityScore = batch.QualityScore,
                        MillingRecovery = headRicePercent + brokenRicePercent,
                        HeadRiceToBrokenRatio = outputHeadRice / outputBrokenRice,
                        IsVerified = true,
                        CalculatedDate = batch.EndTime ?? batchDate.AddHours(8),
                        CalculatedBy = "System",
                        VerifiedBy = "QC Team",
                        VerifiedDate = (batch.EndTime ?? batchDate.AddHours(8)).AddHours(1)
                    };

                    // Calculate grade based on head rice percent
                    if (yieldRecord.HeadRicePercent >= 68)
                        yieldRecord.YieldGrade = "Excellent";
                    else if (yieldRecord.HeadRicePercent >= 62)
                        yieldRecord.YieldGrade = "Good";
                    else if (yieldRecord.HeadRicePercent >= 55)
                        yieldRecord.YieldGrade = "Average";
                    else
                        yieldRecord.YieldGrade = "Poor";

                    context.YieldRecords.Add(yieldRecord);

                    // Update order with actual yields
                    order.ActualQuantityProduced = outputHeadRice + outputBrokenRice;
                    order.ActualYieldPercent = headRicePercent + brokenRicePercent;

                    context.SaveChanges();
                    batchesCreated++;

                    if ((batchesCreated) % 5 == 0)
                    {
                        Console.WriteLine($"  Progress: {batchesCreated}/30 batches created...");
                    }
                }

                Console.WriteLine($"✓ Created {ordersCreated} production orders");
                Console.WriteLine($"✓ Created {batchesCreated} production batches with complete yield data\n");

                // Summary statistics
                Console.WriteLine("========================================");
                Console.WriteLine("DATA SEEDING COMPLETED SUCCESSFULLY!");
                Console.WriteLine("========================================\n");

                var stats = context.YieldRecords
                    .GroupBy(y => 1)
                    .Select(g => new
                    {
                        Count = g.Count(),
                        AvgYield = g.Average(y => y.HeadRicePercent),
                        MinYield = g.Min(y => y.HeadRicePercent),
                        MaxYield = g.Max(y => y.HeadRicePercent),
                        AvgQuality = g.Average(y => y.QualityScore ?? 0)
                    })
                    .FirstOrDefault();

                if (stats != null)
                {
                    Console.WriteLine("Summary Statistics:");
                    Console.WriteLine($"  Total Batches: {stats.Count}");
                    Console.WriteLine($"  Average Yield: {stats.AvgYield:F2}%");
                    Console.WriteLine($"  Yield Range: {stats.MinYield:F2}% - {stats.MaxYield:F2}%");
                    Console.WriteLine($"  Average Quality Score: {stats.AvgQuality:F1}/10");
                    Console.WriteLine();

                    var gradeDistribution = context.YieldRecords
                        .GroupBy(y => y.YieldGrade)
                        .Select(g => new { Grade = g.Key, Count = g.Count() })
                        .OrderByDescending(x => x.Count)
                        .ToList();

                    Console.WriteLine("Yield Grade Distribution:");
                    foreach (var grade in gradeDistribution)
                    {
                        Console.WriteLine($"  {grade.Grade}: {grade.Count} batches");
                    }
                    Console.WriteLine();
                }

                Console.WriteLine("Next Steps:");
                Console.WriteLine("  1. Start the application: dotnet run");
                Console.WriteLine("  2. Navigate to: http://localhost:5090/YieldAnalysis");
                Console.WriteLine("  3. Explore the analytics dashboards");
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
        }
    }
}
