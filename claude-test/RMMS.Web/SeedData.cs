using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using RMMS.Models.Production;
using System;
using System.Linq;

namespace RMMS.Seeder
{
    public class DatabaseSeeder
    {
        public static void SeedData(ApplicationDbContext context)
        {
            Console.WriteLine("========================================");
            Console.WriteLine("RMMS Data Seeding");
            Console.WriteLine("========================================\n");

            // Step 1: Seed Products
            Console.WriteLine("Step 1: Seeding Products...");
            SeedProducts(context);
            Console.WriteLine("✓ Products seeded\n");

            // Step 2: Seed Machines (if not exists)
            Console.WriteLine("Step 2: Seeding Machines...");
            SeedMachines(context);
            Console.WriteLine("✓ Machines seeded\n");

            // Step 3: Seed Production Data
            Console.WriteLine("Step 3: Seeding Production Data...");
            SeedProductionData(context);
            Console.WriteLine("✓ Production data seeded\n");

            Console.WriteLine("========================================");
            Console.WriteLine("✅ DATA SEEDING COMPLETE!");
            Console.WriteLine("========================================");
        }

        private static void SeedProducts(ApplicationDbContext context)
        {
            var products = new[]
            {
                new Product { ProductCode = "PADDY-BR11", ProductName = "Basmati Rice BR-11", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "PADDY-SONA", ProductName = "Sona Masuri Paddy", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "PADDY-IR64", ProductName = "IR-64 Paddy", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "RICE-BR11", ProductName = "Basmati Rice BR-11", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsFinishedProduct = true, IsActive = true },
                new Product { ProductCode = "RICE-SONA", ProductName = "Sona Masuri Rice", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsFinishedProduct = true, IsActive = true },
                new Product { ProductCode = "RICE-BROKEN", ProductName = "Broken Rice", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true },
                new Product { ProductCode = "BRAN-001", ProductName = "Rice Bran", ProductCategory = "By-Product", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true },
                new Product { ProductCode = "HUSK-001", ProductName = "Rice Husk", ProductCategory = "By-Product", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true }
            };

            foreach (var product in products)
            {
                if (!context.Products.Any(p => p.ProductCode == product.ProductCode))
                {
                    context.Products.Add(product);
                    Console.WriteLine($"  + {product.ProductName}");
                }
            }
            context.SaveChanges();
        }

        private static void SeedMachines(ApplicationDbContext context)
        {
            var machines = new[]
            {
                new Machine
                {
                    MachineCode = "MILL-01",
                    MachineName = "Rice Huller Machine #1",
                    MachineType = "Husker",
                    Manufacturer = "Satake Corporation",
                    ModelNumber = "SH-5000",
                    Capacity = 5.0m,
                    CapacityUnit = "tons/hour",
                    Status = "Operational",
                    Location = "Production Floor A",
                    PurchaseDate = DateTime.Now.AddYears(-3),
                    IsActive = true
                },
                new Machine
                {
                    MachineCode = "MILL-02",
                    MachineName = "Rice Polisher #2",
                    MachineType = "Polisher",
                    Manufacturer = "Buhler Group",
                    ModelNumber = "BP-3000",
                    Capacity = 3.5m,
                    CapacityUnit = "tons/hour",
                    Status = "Operational",
                    Location = "Production Floor A",
                    PurchaseDate = DateTime.Now.AddYears(-2),
                    IsActive = true
                },
                new Machine
                {
                    MachineCode = "MILL-03",
                    MachineName = "Rice Grader & Sorter #3",
                    MachineType = "Grader",
                    Manufacturer = "Fowler Westrup",
                    ModelNumber = "GS-2500",
                    Capacity = 4.0m,
                    CapacityUnit = "tons/hour",
                    Status = "Operational",
                    Location = "Production Floor B",
                    PurchaseDate = DateTime.Now.AddYears(-1),
                    IsActive = true
                }
            };

            foreach (var machine in machines)
            {
                if (!context.Machines.Any(m => m.MachineCode == machine.MachineCode))
                {
                    context.Machines.Add(machine);
                    Console.WriteLine($"  + {machine.MachineName}");
                }
            }
            context.SaveChanges();
        }

        private static void SeedProductionData(ApplicationDbContext context)
        {
            var machines = context.Machines.ToList();
            if (!machines.Any())
            {
                Console.WriteLine("  ⚠ No machines found, skipping production data");
                return;
            }

            var random = new Random(42);
            var varieties = new[] { "Basmati BR-11", "Sona Masuri", "IR-64" };
            var shifts = new[] { "Morning", "Evening", "Night" };

            for (int i = 1; i <= 10; i++)
            {
                var batchDate = DateTime.Now.AddDays(-30 + i * 3);
                var variety = varieties[(i - 1) % 3];
                var shift = shifts[i % 3];
                var machine = machines[(i - 1) % machines.Count];

                // Check if order exists
                var orderNumber = $"PO{i:D4}";
                if (context.ProductionOrders.Any(o => o.OrderNumber == orderNumber))
                    continue;

                // Create Production Order
                var order = new ProductionOrder
                {
                    OrderNumber = orderNumber,
                    OrderDate = batchDate,
                    PaddyVariety = variety,
                    PaddyQuantity = 50 + random.Next(20),
                    TargetQuantity = 40 + random.Next(15),
                    AssignedMachineId = machine.Id,
                    Status = "Completed",
                    IsActive = true,
                    CreatedDate = batchDate
                };
                context.ProductionOrders.Add(order);
                context.SaveChanges();

                // Create Production Batch
                var inputQty = 50.0m + random.Next(20);
                var yieldPercent = 62.0m + (decimal)(random.NextDouble() * 10);
                var outputQty = inputQty * yieldPercent / 100;

                var batch = new ProductionBatch
                {
                    BatchNumber = $"BATCH{i:D4}",
                    ProductionOrderId = order.Id,
                    BatchDate = batchDate,
                    ShiftType = shift,
                    StartTime = batchDate,
                    EndTime = batchDate.AddHours(4),
                    Status = "Completed",
                    QualityScore = 7 + random.Next(3),
                    IsActive = true,
                    CreatedDate = batchDate
                };
                context.ProductionBatches.Add(batch);
                context.SaveChanges();

                // Create Yield Record
                var headRice = outputQty * 0.7m;
                var brokenRice = outputQty * 0.15m;
                var bran = inputQty * 0.08m;
                var husk = inputQty * 0.20m;

                var yieldRecord = new YieldRecord
                {
                    BatchId = batch.Id,
                    PaddyVariety = variety,
                    InputPaddyQuantity = inputQty,
                    OutputHeadRice = headRice,
                    OutputBrokenRice = brokenRice,
                    OutputBran = bran,
                    OutputHusk = husk,
                    HeadRicePercent = headRice / inputQty * 100,
                    BrokenRicePercent = brokenRice / inputQty * 100,
                    BranPercent = bran / inputQty * 100,
                    HuskPercent = husk / inputQty * 100,
                    TotalYieldPercent = yieldPercent,
                    MillingRecovery = outputQty / inputQty * 100,
                    QualityScore = 7 + random.Next(3)
                };
                context.YieldRecords.Add(yieldRecord);
                context.SaveChanges();

                Console.WriteLine($"  + Batch {i}/10: {variety}, Yield: {yieldPercent:F1}%");
            }
        }
    }
}
