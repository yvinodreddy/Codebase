-- ============================================
-- RMMS Test Data Insertion Script
-- ============================================
-- This script inserts comprehensive test data for all inventory and production modules
-- Run this after the database schema has been created via migrations

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Starting Test Data Insertion';
PRINT '========================================';
GO

-- ============================================
-- 1. Products (Master Data)
-- ============================================
PRINT 'Inserting Products...';

SET IDENTITY_INSERT Products ON;

INSERT INTO Products (Id, ProductCode, ProductName, Category, Unit, Description, IsActive, CreatedDate)
VALUES
(1, 'RAW-001', 'Raw Paddy - Basmati', 'Raw Material', 'KG', 'Premium Basmati Paddy', 1, GETDATE()),
(2, 'RAW-002', 'Raw Paddy - Sona Mas', 'Raw Material', 'KG', 'Sona Masuri Paddy', 1, GETDATE()),
(3, 'RICE-001', 'Basmati Rice - Premium', 'Finished Product', 'KG', 'Premium Quality Basmati Rice', 1, GETDATE()),
(4, 'RICE-002', 'Sona Masuri Rice', 'Finished Product', 'KG', 'Sona Masuri White Rice', 1, GETDATE()),
(5, 'BP-001', 'Rice Bran', 'By-Product', 'KG', 'Rice Bran for Animal Feed', 1, GETDATE()),
(6, 'BP-002', 'Rice Husk', 'By-Product', 'KG', 'Rice Husk', 1, GETDATE());

SET IDENTITY_INSERT Products OFF;

PRINT '✓ Products inserted: 6 records';
GO

-- ============================================
-- 2. Warehouses
-- ============================================
PRINT 'Inserting Warehouses...';

SET IDENTITY_INSERT Warehouses ON;

INSERT INTO Warehouses (Id, WarehouseCode, WarehouseName, Location, Capacity, IsActive, CreatedDate)
VALUES
(1, 'WH-001', 'Main Warehouse', 'Building A, Ground Floor', 10000.00, 1, GETDATE()),
(2, 'WH-002', 'Raw Material Storage', 'Building B', 5000.00, 1, GETDATE()),
(3, 'WH-003', 'Finished Goods Storage', 'Building C', 8000.00, 1, GETDATE());

SET IDENTITY_INSERT Warehouses OFF;

PRINT '✓ Warehouses inserted: 3 records';
GO

-- ============================================
-- 3. Storage Zones (Optional)
-- ============================================
PRINT 'Inserting Storage Zones...';

SET IDENTITY_INSERT StorageZones ON;

INSERT INTO StorageZones (Id, ZoneCode, ZoneName, WarehouseId, Capacity, IsActive, CreatedDate)
VALUES
(1, 'Z-A1', 'Zone A1 - Raw Materials', 1, 2000.00, 1, GETDATE()),
(2, 'Z-A2', 'Zone A2 - Finished Goods', 1, 3000.00, 1, GETDATE()),
(3, 'Z-B1', 'Zone B1 - Raw Paddy', 2, 2500.00, 1, GETDATE());

SET IDENTITY_INSERT StorageZones OFF;

PRINT '✓ Storage Zones inserted: 3 records';
GO

-- ============================================
-- 4. Inventory Ledger
-- ============================================
PRINT 'Inserting Inventory Ledger...';

SET IDENTITY_INSERT InventoryLedger ON;

INSERT INTO InventoryLedger (
    Id, ProductId, WarehouseId, ZoneId,
    CurrentStock, MinimumLevel, MaximumLevel, ReorderLevel,
    UnitCost, TotalValue, LastMovementDate, LastUpdated,
    Remarks, CreatedDate, CreatedBy, IsActive
)
VALUES
(1, 1, 2, 3, 5000.00, 1000.00, 10000.00, 2000.00, 25.00, 125000.00, GETDATE(), GETDATE(), 'Raw Basmati Paddy Stock', GETDATE(), 'System', 1),
(2, 2, 2, 3, 4500.00, 1000.00, 10000.00, 2000.00, 22.00, 99000.00, GETDATE(), GETDATE(), 'Raw Sona Masuri Stock', GETDATE(), 'System', 1),
(3, 3, 3, 2, 3000.00, 500.00, 8000.00, 1000.00, 50.00, 150000.00, GETDATE(), GETDATE(), 'Premium Basmati Rice', GETDATE(), 'System', 1),
(4, 4, 3, 2, 3500.00, 500.00, 8000.00, 1000.00, 45.00, 157500.00, GETDATE(), GETDATE(), 'Sona Masuri Rice', GETDATE(), 'System', 1),
(5, 5, 1, 1, 800.00, 100.00, 2000.00, 200.00, 5.00, 4000.00, GETDATE(), GETDATE(), 'Rice Bran', GETDATE(), 'System', 1),
(6, 6, 1, 1, 1200.00, 100.00, 2000.00, 200.00, 3.00, 3600.00, GETDATE(), GETDATE(), 'Rice Husk', GETDATE(), 'System', 1);

SET IDENTITY_INSERT InventoryLedger OFF;

PRINT '✓ Inventory Ledger inserted: 6 records';
GO

-- ============================================
-- 5. Stock Movements
-- ============================================
PRINT 'Inserting Stock Movements...';

SET IDENTITY_INSERT StockMovements ON;

INSERT INTO StockMovements (
    Id, ProductId, WarehouseId, ZoneId, MovementType,
    Quantity, UnitCost, TotalCost, MovementDate,
    ReferenceNo, Remarks, CreatedDate, CreatedBy, IsActive
)
VALUES
(1, 1, 2, 3, 'IN', 2000.00, 25.00, 50000.00, DATEADD(day, -10, GETDATE()), 'PO-2025-001', 'Purchase from Farmer Group A', DATEADD(day, -10, GETDATE()), 'Admin', 1),
(2, 1, 2, 3, 'IN', 3000.00, 25.00, 75000.00, DATEADD(day, -5, GETDATE()), 'PO-2025-002', 'Purchase from Farmer Group B', DATEADD(day, -5, GETDATE()), 'Admin', 1),
(3, 2, 2, 3, 'IN', 4500.00, 22.00, 99000.00, DATEADD(day, -8, GETDATE()), 'PO-2025-003', 'Purchase from Local Market', DATEADD(day, -8, GETDATE()), 'Admin', 1),
(4, 3, 3, 2, 'IN', 1500.00, 50.00, 75000.00, DATEADD(day, -3, GETDATE()), 'PROD-001', 'Production Output', DATEADD(day, -3, GETDATE()), 'Production', 1),
(5, 3, 3, 2, 'OUT', 500.00, 50.00, 25000.00, DATEADD(day, -1, GETDATE()), 'SO-2025-001', 'Sales Order', DATEADD(day, -1, GETDATE()), 'Sales', 1),
(6, 4, 3, 2, 'IN', 2000.00, 45.00, 90000.00, DATEADD(day, -4, GETDATE()), 'PROD-002', 'Production Output', DATEADD(day, -4, GETDATE()), 'Production', 1),
(7, 4, 3, 2, 'OUT', 800.00, 45.00, 36000.00, DATEADD(day, -2, GETDATE()), 'SO-2025-002', 'Sales Order', DATEADD(day, -2, GETDATE()), 'Sales', 1),
(8, 5, 1, 1, 'IN', 800.00, 5.00, 4000.00, DATEADD(day, -3, GETDATE()), 'PROD-001-BP', 'By-product from Production', DATEADD(day, -3, GETDATE()), 'Production', 1),
(9, 6, 1, 1, 'IN', 1200.00, 3.00, 3600.00, DATEADD(day, -3, GETDATE()), 'PROD-002-BP', 'By-product from Production', DATEADD(day, -3, GETDATE()), 'Production', 1);

SET IDENTITY_INSERT StockMovements OFF;

PRINT '✓ Stock Movements inserted: 9 records';
GO

-- ============================================
-- 6. Stock Adjustments
-- ============================================
PRINT 'Inserting Stock Adjustments...';

SET IDENTITY_INSERT StockAdjustments ON;

INSERT INTO StockAdjustments (
    Id, ProductId, WarehouseId, ZoneId, AdjustmentType,
    Quantity, Reason, AdjustmentDate, ReferenceNo,
    Remarks, ApprovedBy, CreatedDate, CreatedBy, IsActive
)
VALUES
(1, 1, 2, 3, 'Increase', 100.00, 'Physical Count Adjustment', DATEADD(day, -2, GETDATE()), 'ADJ-001', 'Monthly stock verification found excess', 'Manager', DATEADD(day, -2, GETDATE()), 'Warehouse Staff', 1),
(2, 3, 3, 2, 'Decrease', 50.00, 'Damaged Goods', DATEADD(day, -1, GETDATE()), 'ADJ-002', 'Water damage in packaging', 'Manager', DATEADD(day, -1, GETDATE()), 'QC Inspector', 1),
(3, 4, 3, 2, 'Increase', 300.00, 'Reconciliation', DATEADD(day, -3, GETDATE()), 'ADJ-003', 'System reconciliation adjustment', 'Manager', DATEADD(day, -3, GETDATE()), 'Admin', 1);

SET IDENTITY_INSERT StockAdjustments OFF;

PRINT '✓ Stock Adjustments inserted: 3 records';
GO

-- ============================================
-- 7. Employees (for Production Batches)
-- ============================================
PRINT 'Inserting Employees...';

SET IDENTITY_INSERT Employees ON;

INSERT INTO Employees (
    Id, EmployeeCode, FirstName, LastName, Department,
    Designation, PhoneNumber, Email, JoiningDate,
    IsActive, CreatedDate
)
VALUES
(1, 'EMP-001', 'Rajesh', 'Kumar', 'Production', 'Production Supervisor', '9876543210', 'rajesh.kumar@rmms.com', '2023-01-15', 1, GETDATE()),
(2, 'EMP-002', 'Priya', 'Sharma', 'Production', 'Machine Operator', '9876543211', 'priya.sharma@rmms.com', '2023-03-20', 1, GETDATE()),
(3, 'EMP-003', 'Amit', 'Patel', 'Production', 'Quality Inspector', '9876543212', 'amit.patel@rmms.com', '2023-02-10', 1, GETDATE());

SET IDENTITY_INSERT Employees OFF;

PRINT '✓ Employees inserted: 3 records';
GO

-- ============================================
-- 8. Machines (for Production Batches)
-- ============================================
PRINT 'Inserting Machines...';

SET IDENTITY_INSERT Machines ON;

INSERT INTO Machines (
    Id, MachineCode, MachineName, MachineType, Capacity,
    RunningHours, PurchaseDate, Status, IsActive, CreatedDate
)
VALUES
(1, 'MCH-001', 'Rice Mill Machine 1', 'Milling', 500.00, 1250.50, '2022-06-01', 'Running', 1, GETDATE()),
(2, 'MCH-002', 'Rice Mill Machine 2', 'Milling', 500.00, 980.25, '2022-08-15', 'Running', 1, GETDATE()),
(3, 'MCH-003', 'Sorting Machine', 'Sorting', 300.00, 750.00, '2023-01-10', 'Running', 1, GETDATE());

SET IDENTITY_INSERT Machines OFF;

PRINT '✓ Machines inserted: 3 records';
GO

-- ============================================
-- 9. Production Orders (for Production Batches)
-- ============================================
PRINT 'Inserting Production Orders...';

SET IDENTITY_INSERT ProductionOrders ON;

INSERT INTO ProductionOrders (
    Id, OrderNumber, OrderDate, PlannedStartDate, PlannedEndDate,
    Status, Priority, Remarks, CreatedDate, CreatedBy, IsActive
)
VALUES
(1, 'PO-2025-001', DATEADD(day, -15, GETDATE()), DATEADD(day, -14, GETDATE()), DATEADD(day, -10, GETDATE()), 'Completed', 'High', 'Basmati rice production batch', DATEADD(day, -15, GETDATE()), 'Production Manager', 1),
(2, 'PO-2025-002', DATEADD(day, -10, GETDATE()), DATEADD(day, -9, GETDATE()), DATEADD(day, -5, GETDATE()), 'Completed', 'Medium', 'Sona Masuri production batch', DATEADD(day, -10, GETDATE()), 'Production Manager', 1),
(3, 'PO-2025-003', DATEADD(day, -3, GETDATE()), DATEADD(day, -2, GETDATE()), DATEADD(day, 2, GETDATE()), 'In Progress', 'High', 'Ongoing production', DATEADD(day, -3, GETDATE()), 'Production Manager', 1);

SET IDENTITY_INSERT ProductionOrders OFF;

PRINT '✓ Production Orders inserted: 3 records';
GO

-- ============================================
-- 10. Production Batches
-- ============================================
PRINT 'Inserting Production Batches...';

SET IDENTITY_INSERT ProductionBatches ON;

INSERT INTO ProductionBatches (
    Id, BatchNumber, ProductionOrderId, ProductId, MachineId,
    PlannedQuantity, ActualQuantity, StartDate, EndDate,
    Status, OperatorId, SupervisorId, Remarks,
    CreatedDate, CreatedBy, IsActive
)
VALUES
(1, 'BATCH-2025-001', 1, 3, 1, 2000.00, 1950.00, DATEADD(day, -14, GETDATE()), DATEADD(day, -12, GETDATE()), 'Completed', 2, 1, 'Basmati rice milling batch 1', DATEADD(day, -14, GETDATE()), 'System', 1),
(2, 'BATCH-2025-002', 1, 3, 2, 2000.00, 1900.00, DATEADD(day, -12, GETDATE()), DATEADD(day, -10, GETDATE()), 'Completed', 2, 1, 'Basmati rice milling batch 2', DATEADD(day, -12, GETDATE()), 'System', 1),
(3, 'BATCH-2025-003', 2, 4, 1, 2500.00, 2450.00, DATEADD(day, -9, GETDATE()), DATEADD(day, -7, GETDATE()), 'Completed', 2, 1, 'Sona Masuri milling batch', DATEADD(day, -9, GETDATE()), 'System', 1),
(4, 'BATCH-2025-004', 3, 3, 2, 1500.00, 0.00, DATEADD(day, -2, GETDATE()), NULL, 'In Progress', 2, 1, 'Ongoing Basmati batch', DATEADD(day, -2, GETDATE()), 'System', 1);

SET IDENTITY_INSERT ProductionBatches OFF;

PRINT '✓ Production Batches inserted: 4 records';
GO

-- ============================================
-- Summary
-- ============================================
PRINT '';
PRINT '========================================';
PRINT 'Test Data Insertion Complete!';
PRINT '========================================';
PRINT '';
PRINT 'Summary:';
PRINT '  Products: 6';
PRINT '  Warehouses: 3';
PRINT '  Storage Zones: 3';
PRINT '  Inventory Ledger: 6';
PRINT '  Stock Movements: 9';
PRINT '  Stock Adjustments: 3';
PRINT '  Employees: 3';
PRINT '  Machines: 3';
PRINT '  Production Orders: 3';
PRINT '  Production Batches: 4';
PRINT '';
PRINT 'You can now access:';
PRINT '  http://localhost:5090/Inventory';
PRINT '  http://localhost:5090/StockMovements';
PRINT '  http://localhost:5090/StockAdjustments';
PRINT '  http://localhost:5090/ProductionBatches';
PRINT '';
PRINT '========================================';
GO
