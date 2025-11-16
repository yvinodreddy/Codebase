#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.EntityFrameworkCore, 8.0.0"
#r "nuget: Microsoft.EntityFrameworkCore.SqlServer, 8.0.0"
#load "RMMS.DataAccess/Context/ApplicationDbContext.cs"
#load "RMMS.Models/Masters/Product.cs"
#load "RMMS.Models/Masters/Customer.cs"
#load "RMMS.Models/Masters/Vendor.cs"
#load "RMMS.Models/Masters/Employee.cs"
#load "RMMS.Models/Inventory/Warehouse.cs"
#load "RMMS.Models/Inventory/StorageZone.cs"
#load "RMMS.Models/Inventory/InventoryLedger.cs"
#load "RMMS.Models/Inventory/StockMovement.cs"
#load "RMMS.Models/Inventory/StockAdjustment.cs"
#load "RMMS.Models/Production/Machine.cs"
#load "RMMS.Models/Production/ProductionOrder.cs"
#load "RMMS.Models/Production/ProductionBatch.cs"
#load "RMMS.Models/Production/BatchInput.cs"
#load "RMMS.Models/Production/BatchOutput.cs"
#load "RMMS.Models/Production/YieldRecord.cs"
#load "SeedData.cs"

using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Seeder;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
optionsBuilder.UseSqlServer(connectionString);

using var context = new ApplicationDbContext(optionsBuilder.Options);

DatabaseSeeder.SeedData(context);
