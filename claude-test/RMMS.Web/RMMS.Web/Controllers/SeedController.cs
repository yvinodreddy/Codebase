using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using RMMS.Models.Production;
using RMMS.Models.Inventory;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class SeedController : Controller
    {
        private readonly ApplicationDbContext _context;

        public SeedController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult Index()
        {
            ViewBag.Message = "Click 'Seed Data' to populate the database with comprehensive test data (40+ records).";
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> SeedData()
        {
            try
            {
                var log = new System.Text.StringBuilder();
                log.AppendLine("========================================");
                log.AppendLine("RMMS COMPREHENSIVE DATA SEEDING");
                log.AppendLine("========================================\n");

                int totalRecords = 0;

                // MASTER DATA MODULE
                log.AppendLine("═══ MASTER DATA MODULE ═══\n");

                log.AppendLine("Step 1: Seeding Customers...");
                totalRecords += await SeedCustomers(log);
                log.AppendLine("✓ Customers seeded\n");

                log.AppendLine("Step 2: Seeding Vendors...");
                totalRecords += await SeedVendors(log);
                log.AppendLine("✓ Vendors seeded\n");

                log.AppendLine("Step 3: Seeding Products...");
                totalRecords += await SeedProducts(log);
                log.AppendLine("✓ Products seeded\n");

                log.AppendLine("Step 4: Seeding Employees...");
                totalRecords += await SeedEmployees(log);
                log.AppendLine("✓ Employees seeded\n");

                log.AppendLine("Step 5: Seeding Warehouses...");
                totalRecords += await SeedWarehouses(log);
                log.AppendLine("✓ Warehouses seeded\n");

                log.AppendLine("Step 6: Seeding Machines...");
                totalRecords += await SeedMachines(log);
                log.AppendLine("✓ Machines seeded\n");

                // INVENTORY MODULE
                log.AppendLine("\n═══ INVENTORY MODULE ═══\n");

                log.AppendLine("Step 7: Seeding Inventory Ledger...");
                totalRecords += await SeedInventoryLedger(log);
                log.AppendLine("✓ Inventory Ledger seeded\n");

                log.AppendLine("Step 8: Seeding Stock Movements...");
                totalRecords += await SeedStockMovements(log);
                log.AppendLine("✓ Stock Movements seeded\n");

                // PRODUCTION MODULE
                log.AppendLine("\n═══ PRODUCTION MODULE ═══\n");

                log.AppendLine("Step 9: Seeding Production Orders...");
                totalRecords += await SeedProductionOrders(log);
                log.AppendLine("✓ Production Orders seeded\n");

                log.AppendLine("Step 10: Seeding Production Batches...");
                totalRecords += await SeedProductionBatches(log);
                log.AppendLine("✓ Production Batches seeded\n");

                log.AppendLine("\n========================================");
                log.AppendLine($"✅ SEEDING COMPLETE!");
                log.AppendLine($"Total Records Created: {totalRecords}");
                log.AppendLine("========================================");

                ViewBag.Message = log.ToString();
                ViewBag.Success = true;
                return View("Index");
            }
            catch (Exception ex)
            {
                ViewBag.Message = $"❌ ERROR: {ex.Message}\n\n{ex.StackTrace}";
                ViewBag.Success = false;
                return View("Index");
            }
        }

        private async Task<int> SeedCustomers(System.Text.StringBuilder log)
        {
            var count = 0;
            var customers = new[]
            {
                new Customer { CustomerCode = "CUST001", CustomerName = "Sharma Rice Traders", CustomerType = "Wholesaler", Category = "A", GSTIN = "29ABCDE1234F1Z5", CreditLimit = 500000, CreditDays = 30, PaymentTerms = "NET 30", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST002", CustomerName = "Patel Retail Stores", CustomerType = "Retailer", Category = "B", GSTIN = "29FGHIJ5678K2Y6", CreditLimit = 200000, CreditDays = 15, PaymentTerms = "NET 15", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST003", CustomerName = "Kumar Distribution Co.", CustomerType = "Distributor", Category = "A", GSTIN = "29KLMNO9012L3X7", CreditLimit = 1000000, CreditDays = 45, PaymentTerms = "NET 45", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST004", CustomerName = "Singh Export House", CustomerType = "Export", Category = "A", GSTIN = "29PQRST3456M4W8", CreditLimit = 2000000, CreditDays = 60, PaymentTerms = "LC", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST005", CustomerName = "Reddy Super Market", CustomerType = "Retailer", Category = "B", GSTIN = "29UVWXY7890N5V9", CreditLimit = 150000, CreditDays = 10, PaymentTerms = "NET 10", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST006", CustomerName = "Gupta Wholesale Mart", CustomerType = "Wholesaler", Category = "B", GSTIN = "29ZABCD1234O6U1", CreditLimit = 300000, CreditDays = 20, PaymentTerms = "NET 20", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST007", CustomerName = "Mehta Foods Pvt Ltd", CustomerType = "Distributor", Category = "A", GSTIN = "29EFGHI5678P7T2", CreditLimit = 800000, CreditDays = 30, PaymentTerms = "NET 30", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST008", CustomerName = "Rao Enterprises", CustomerType = "Wholesaler", Category = "C", GSTIN = "29JKLMN9012Q8S3", CreditLimit = 100000, CreditDays = 7, PaymentTerms = "NET 7", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST009", CustomerName = "Bansal Rice Mill", CustomerType = "Retailer", Category = "B", GSTIN = "29OPQRS3456R9R4", CreditLimit = 250000, CreditDays = 15, PaymentTerms = "NET 15", Status = "Active", IsActive = true },
                new Customer { CustomerCode = "CUST010", CustomerName = "Verma International", CustomerType = "Export", Category = "A", GSTIN = "29TUVWX7890S1Q5", CreditLimit = 1500000, CreditDays = 60, PaymentTerms = "LC/DA", Status = "Active", IsActive = true }
            };

            foreach (var customer in customers)
            {
                if (!await _context.Customers.AnyAsync(c => c.CustomerCode == customer.CustomerCode))
                {
                    customer.CreatedDate = DateTime.Now;
                    customer.CreatedBy = "SeedData";
                    await _context.Customers.AddAsync(customer);
                    count++;
                    log.AppendLine($"  + {customer.CustomerName} ({customer.CustomerCode})");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedVendors(System.Text.StringBuilder log)
        {
            var count = 0;
            var vendors = new[]
            {
                new Vendor { VendorCode = "VEN001", VendorName = "Punjab Paddy Farmers Co-op", VendorType = "Farmer", Category = "A", GSTIN = "03VWXYZ1234A1A1", PaymentTerms = "Immediate", Rating = 5, Status = "Active", IsActive = true },
                new Vendor { VendorCode = "VEN002", VendorName = "Haryana Grain Traders", VendorType = "Trader", Category = "A", GSTIN = "06BCDEF5678B2B2", PaymentTerms = "NET 7", Rating = 4, Status = "Active", IsActive = true },
                new Vendor { VendorCode = "VEN003", VendorName = "Andhra Commission Agents", VendorType = "Commission Agent", Category = "B", GSTIN = "37GHIJK9012C3C3", PaymentTerms = "NET 15", Rating = 4, Status = "Active", IsActive = true },
                new Vendor { VendorCode = "VEN004", VendorName = "Karnataka Paddy Suppliers", VendorType = "Farmer", Category = "A", GSTIN = "29LMNOP3456D4D4", PaymentTerms = "Immediate", Rating = 5, Status = "Active", IsActive = true },
                new Vendor { VendorCode = "VEN005", VendorName = "Telangana Agri Traders", VendorType = "Trader", Category = "B", GSTIN = "36QRSTU7890E5E5", PaymentTerms = "NET 10", Rating = 3, Status = "Active", IsActive = true }
            };

            foreach (var vendor in vendors)
            {
                if (!await _context.Vendors.AnyAsync(v => v.VendorCode == vendor.VendorCode))
                {
                    vendor.CreatedDate = DateTime.Now;
                    vendor.CreatedBy = "SeedData";
                    await _context.Vendors.AddAsync(vendor);
                    count++;
                    log.AppendLine($"  + {vendor.VendorName} ({vendor.VendorCode})");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedEmployees(System.Text.StringBuilder log)
        {
            var count = 0;
            var employees = new[]
            {
                new Employee { EmployeeCode = "EMP001", EmployeeName = "Rajesh Kumar", Department = "Production", Designation = "Production Manager", Mobile = "9876543210", Email = "rajesh@rmms.com", DateOfJoining = DateTime.Now.AddYears(-3), BasicSalary = 50000, EmploymentType = "Permanent", Status = "Active", IsActive = true },
                new Employee { EmployeeCode = "EMP002", EmployeeName = "Priya Sharma", Department = "Quality Control", Designation = "QC Supervisor", Mobile = "9876543211", Email = "priya@rmms.com", DateOfJoining = DateTime.Now.AddYears(-2), BasicSalary = 40000, EmploymentType = "Permanent", Status = "Active", IsActive = true },
                new Employee { EmployeeCode = "EMP003", EmployeeName = "Amit Patel", Department = "Warehouse", Designation = "Warehouse Manager", Mobile = "9876543212", Email = "amit@rmms.com", DateOfJoining = DateTime.Now.AddYears(-4), BasicSalary = 45000, EmploymentType = "Permanent", Status = "Active", IsActive = true },
                new Employee { EmployeeCode = "EMP004", EmployeeName = "Sunita Reddy", Department = "Accounts", Designation = "Accountant", Mobile = "9876543213", Email = "sunita@rmms.com", DateOfJoining = DateTime.Now.AddYears(-1), BasicSalary = 35000, EmploymentType = "Permanent", Status = "Active", IsActive = true },
                new Employee { EmployeeCode = "EMP005", EmployeeName = "Vijay Singh", Department = "Sales", Designation = "Sales Executive", Mobile = "9876543214", Email = "vijay@rmms.com", DateOfJoining = DateTime.Now.AddMonths(-6), BasicSalary = 30000, EmploymentType = "Contract", Status = "Active", IsActive = true }
            };

            foreach (var employee in employees)
            {
                if (!await _context.Employees.AnyAsync(e => e.EmployeeCode == employee.EmployeeCode))
                {
                    employee.CreatedDate = DateTime.Now;
                    employee.CreatedBy = "SeedData";
                    await _context.Employees.AddAsync(employee);
                    count++;
                    log.AppendLine($"  + {employee.EmployeeName} ({employee.Department})");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedWarehouses(System.Text.StringBuilder log)
        {
            var count = 0;
            var warehouses = new[]
            {
                new Warehouse { WarehouseCode = "WH001", WarehouseName = "Main Godown - A Block", Location = "Factory Premises", WarehouseType = "Main Godown", TotalCapacity = 5000, UsedCapacity = 0, AvailableCapacity = 5000, ContactPerson = "Amit Patel", Mobile = "9876543212", Status = "Active", IsActive = true },
                new Warehouse { WarehouseCode = "WH002", WarehouseName = "Sub Godown - B Block", Location = "Factory Premises", WarehouseType = "Sub Godown", TotalCapacity = 3000, UsedCapacity = 0, AvailableCapacity = 3000, ContactPerson = "Ravi Kumar", Mobile = "9876543220", Status = "Active", IsActive = true },
                new Warehouse { WarehouseCode = "WH003", WarehouseName = "Finished Goods Storage", Location = "Dispatch Area", WarehouseType = "Main Godown", TotalCapacity = 2000, UsedCapacity = 0, AvailableCapacity = 2000, ContactPerson = "Suresh Babu", Mobile = "9876543221", Status = "Active", IsActive = true }
            };

            foreach (var warehouse in warehouses)
            {
                if (!await _context.Warehouses.AnyAsync(w => w.WarehouseCode == warehouse.WarehouseCode))
                {
                    warehouse.CreatedDate = DateTime.Now;
                    warehouse.CreatedBy = "SeedData";
                    await _context.Warehouses.AddAsync(warehouse);
                    count++;
                    log.AppendLine($"  + {warehouse.WarehouseName} ({warehouse.TotalCapacity} MT)");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedProducts(System.Text.StringBuilder log)
        {
            var count = 0;
            var products = new[]
            {
                new Product { ProductCode = "PADDY-BR11", ProductName = "Basmati Rice BR-11 Paddy", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "PADDY-SONA", ProductName = "Sona Masuri Paddy", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "PADDY-IR64", ProductName = "IR-64 Paddy", ProductCategory = "Paddy", UnitOfMeasure = "Quintals", IsRawMaterial = true, IsActive = true },
                new Product { ProductCode = "RICE-BR11", ProductName = "Basmati Rice BR-11", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsFinishedProduct = true, IsActive = true },
                new Product { ProductCode = "RICE-SONA", ProductName = "Sona Masuri Rice", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsFinishedProduct = true, IsActive = true },
                new Product { ProductCode = "RICE-IR64", ProductName = "IR-64 Rice", ProductCategory = "Rice", UnitOfMeasure = "Quintals", IsFinishedProduct = true, IsActive = true },
                new Product { ProductCode = "RICE-BROKEN", ProductName = "Broken Rice", ProductCategory = "By-Product", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true },
                new Product { ProductCode = "BRAN-001", ProductName = "Rice Bran", ProductCategory = "By-Product", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true },
                new Product { ProductCode = "HUSK-001", ProductName = "Rice Husk", ProductCategory = "By-Product", UnitOfMeasure = "Quintals", IsByProduct = true, IsActive = true }
            };

            foreach (var product in products)
            {
                if (!await _context.Products.AnyAsync(p => p.ProductCode == product.ProductCode))
                {
                    product.CreatedDate = DateTime.Now;
                    product.CreatedBy = "SeedData";
                    await _context.Products.AddAsync(product);
                    count++;
                    log.AppendLine($"  + {product.ProductName}");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedMachines(System.Text.StringBuilder log)
        {
            var count = 0;
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
                if (!await _context.Machines.AnyAsync(m => m.MachineCode == machine.MachineCode))
                {
                    machine.CreatedDate = DateTime.Now;
                    machine.CreatedBy = "SeedData";
                    await _context.Machines.AddAsync(machine);
                    count++;
                    log.AppendLine($"  + {machine.MachineName}");
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedInventoryLedger(System.Text.StringBuilder log)
        {
            var count = 0;
            var products = await _context.Products.ToListAsync();
            var warehouses = await _context.Warehouses.ToListAsync();

            if (!products.Any() || !warehouses.Any())
            {
                log.AppendLine("  ⚠ No products or warehouses found, skipping inventory");
                return count;
            }

            // Create inventory for each product in each warehouse
            foreach (var product in products)
            {
                foreach (var warehouse in warehouses)
                {
                    var existingInventory = await _context.InventoryLedger
                        .FirstOrDefaultAsync(i => i.ProductId == product.Id && i.WarehouseId == warehouse.Id);

                    if (existingInventory == null)
                    {
                        var random = new Random(product.Id + warehouse.Id);
                        var currentStock = random.Next(100, 1000);
                        var unitCost = product.IsRawMaterial ? random.Next(2000, 3000) :
                                      product.IsFinishedProduct ? random.Next(3500, 5000) :
                                      random.Next(500, 1500);

                        var inventory = new InventoryLedger
                        {
                            ProductId = product.Id,
                            WarehouseId = warehouse.Id,
                            CurrentStock = currentStock,
                            MinimumLevel = currentStock * 0.2m,
                            MaximumLevel = currentStock * 2m,
                            ReorderLevel = currentStock * 0.3m,
                            UnitCost = unitCost,
                            TotalValue = currentStock * unitCost,
                            LastUpdated = DateTime.Now,
                            IsActive = true,
                            CreatedDate = DateTime.Now,
                            CreatedBy = "SeedData"
                        };

                        await _context.InventoryLedger.AddAsync(inventory);
                        count++;
                        log.AppendLine($"  + {product.ProductName} @ {warehouse.WarehouseName}: {currentStock} units");
                    }
                }
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedStockMovements(System.Text.StringBuilder log)
        {
            var count = 0;
            var inventories = await _context.InventoryLedger
                .Include(i => i.Product)
                .Include(i => i.Warehouse)
                .Take(5)
                .ToListAsync();

            if (!inventories.Any())
            {
                log.AppendLine("  ⚠ No inventory found, skipping stock movements");
                return count;
            }

            var random = new Random(123);
            var movementCategories = new[] { "Procurement", "Sales", "Production", "Adjustment" };

            for (int i = 1; i <= 10; i++)
            {
                var inventory = inventories[i % inventories.Count];
                var movementCategory = movementCategories[i % movementCategories.Length];
                var movementType = i % 2 == 0 ? "IN" : "OUT";
                var quantity = random.Next(10, 100);

                var movement = new StockMovement
                {
                    MovementCode = $"SM{i:D4}",
                    MovementDate = DateTime.Now.AddDays(-random.Next(1, 30)),
                    MovementType = movementType,
                    MovementCategory = movementCategory,
                    ProductId = inventory.ProductId,
                    WarehouseId = inventory.WarehouseId,
                    Quantity = quantity,
                    UnitCost = inventory.UnitCost,
                    TotalCost = quantity * inventory.UnitCost,
                    ReferenceNumber = $"REF{i:D4}",
                    Remarks = $"Test {movementCategory} movement",
                    IsApproved = true,
                    IsActive = true,
                    CreatedDate = DateTime.Now,
                    CreatedBy = "SeedData"
                };

                await _context.StockMovements.AddAsync(movement);
                count++;
                log.AppendLine($"  + Movement {i}/10: {movementType} {movementCategory} - {inventory.Product?.ProductName}");
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedProductionOrders(System.Text.StringBuilder log)
        {
            var count = 0;
            var machines = await _context.Machines.ToListAsync();
            if (!machines.Any())
            {
                log.AppendLine("  ⚠ No machines found, skipping production orders");
                return count;
            }

            var random = new Random(42);
            var varieties = new[] { "Basmati BR-11", "Sona Masuri", "IR-64" };

            for (int i = 1; i <= 10; i++)
            {
                var orderNumber = $"PO{i:D4}";
                if (await _context.ProductionOrders.AnyAsync(o => o.OrderNumber == orderNumber))
                    continue;

                var orderDate = DateTime.Now.AddDays(-30 + i * 3);
                var variety = varieties[(i - 1) % 3];
                var machine = machines[(i - 1) % machines.Count];

                var order = new ProductionOrder
                {
                    OrderNumber = orderNumber,
                    OrderDate = orderDate,
                    PaddyVariety = variety,
                    PaddyQuantity = 50 + random.Next(20),
                    TargetQuantity = 40 + random.Next(15),
                    AssignedMachineId = machine.Id,
                    Status = "Completed",
                    IsActive = true,
                    CreatedDate = orderDate,
                    CreatedBy = "SeedData"
                };
                await _context.ProductionOrders.AddAsync(order);
                count++;
                log.AppendLine($"  + Order {i}/10: {orderNumber} - {variety}");
            }
            await _context.SaveChangesAsync();
            return count;
        }

        private async Task<int> SeedProductionBatches(System.Text.StringBuilder log)
        {
            var count = 0;
            var orders = await _context.ProductionOrders.ToListAsync();
            if (!orders.Any())
            {
                log.AppendLine("  ⚠ No production orders found, skipping batches");
                return count;
            }

            var random = new Random(42);
            var shifts = new[] { "Morning", "Evening", "Night" };

            int batchIndex = 1;
            foreach (var order in orders)
            {
                var batchNumber = $"BATCH{batchIndex:D4}";
                if (await _context.ProductionBatches.AnyAsync(b => b.BatchNumber == batchNumber))
                {
                    batchIndex++;
                    continue;
                }

                var shift = shifts[batchIndex % 3];
                var inputQty = (decimal)order.PaddyQuantity;
                var yieldPercent = 62.0m + (decimal)(random.NextDouble() * 10);
                var outputQty = inputQty * yieldPercent / 100;

                var batch = new ProductionBatch
                {
                    BatchNumber = batchNumber,
                    ProductionOrderId = order.Id,
                    BatchDate = order.OrderDate,
                    ShiftType = shift,
                    StartTime = order.OrderDate,
                    EndTime = order.OrderDate.AddHours(4),
                    Status = "Completed",
                    QualityScore = 7 + random.Next(3),
                    IsActive = true,
                    CreatedDate = order.OrderDate,
                    CreatedBy = "SeedData"
                };
                await _context.ProductionBatches.AddAsync(batch);
                await _context.SaveChangesAsync();

                // Create Yield Record
                var headRice = outputQty * 0.7m;
                var brokenRice = outputQty * 0.15m;
                var bran = inputQty * 0.08m;
                var husk = inputQty * 0.20m;

                var yieldRecord = new YieldRecord
                {
                    BatchId = batch.Id,
                    PaddyVariety = order.PaddyVariety,
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
                await _context.YieldRecords.AddAsync(yieldRecord);

                count++;
                log.AppendLine($"  + Batch {batchIndex}/10: {order.PaddyVariety}, Yield: {yieldPercent:F1}%");
                batchIndex++;
            }
            await _context.SaveChangesAsync();
            return count;
        }
    }
}
