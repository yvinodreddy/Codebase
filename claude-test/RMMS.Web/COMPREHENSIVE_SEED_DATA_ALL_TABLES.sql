-- ============================================
-- COMPREHENSIVE SEED DATA FOR ALL TABLES
-- Generated: 2025-10-12
-- Purpose: Add 40+ records to all empty/incomplete tables
-- ============================================

USE RMMS_Production;
GO

SET NOCOUNT ON;
PRINT '════════════════════════════════════════════════════════════';
PRINT '  RMMS COMPREHENSIVE DATA SEEDING';
PRINT '  Target: 40+ records per table';
PRINT '════════════════════════════════════════════════════════════';
PRINT '';

-- ============================================
-- SECTION 1: MASTER DATA (Complete existing data)
-- ============================================

PRINT '📊 MASTER DATA SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 1.1 VENDORS (Currently 5, need 35 more to reach 40)
PRINT 'Adding Vendors (35 more records)...';

INSERT INTO Vendors (VendorCode, VendorName, VendorType, Category, GSTIN, CreditLimit, CreditDays,
                     PaymentTerms, Status, CreatedDate, IsActive)
SELECT
    'VEN-' + RIGHT('00000' + CAST((n + 5) AS VARCHAR), 5),
    'Vendor ' + CAST((n + 5) AS VARCHAR) + ' Suppliers',
    CASE WHEN n % 3 = 0 THEN 'Farmer'
         WHEN n % 3 = 1 THEN 'Trader'
         ELSE 'Agent' END,
    CASE WHEN n % 2 = 0 THEN 'Local' ELSE 'Interstate' END,
    '29VEND' + RIGHT('00000' + CAST((n + 5) AS VARCHAR), 5) + 'Z1',
    100000.0 + ((n + 5) * 2000),
    45 + ((n + 5) % 45),
    'NET 60',
    'Active',
    DATEADD(DAY, -(n + 5), GETDATE()),
    1
FROM (SELECT TOP 35 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Vendors: Added 35 records (Total: 40)';
GO

-- 1.2 WAREHOUSES (Currently 3, need 37 more to reach 40)
PRINT 'Adding Warehouses (37 more records)...';

INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, Address, City, State, Pincode,
                        TotalCapacity, AvailableCapacity, Status, CreatedDate, IsActive)
SELECT
    'WH-' + RIGHT('00000' + CAST((n + 3) AS VARCHAR), 5),
    'Warehouse ' + CAST((n + 3) AS VARCHAR),
    'Location ' + CAST((n + 3) AS VARCHAR),
    'Warehouse Address ' + CAST((n + 3) AS VARCHAR) + ', Industrial Area',
    CASE (n + 3) % 10
        WHEN 0 THEN 'Bangalore'
        WHEN 1 THEN 'Mysore'
        WHEN 2 THEN 'Mandya'
        WHEN 3 THEN 'Tumkur'
        WHEN 4 THEN 'Hassan'
        WHEN 5 THEN 'Belgaum'
        WHEN 6 THEN 'Hubli'
        WHEN 7 THEN 'Mangalore'
        WHEN 8 THEN 'Gulbarga'
        ELSE 'Davangere' END,
    'Karnataka',
    '5600' + RIGHT('00' + CAST((n + 3) AS VARCHAR), 2),
    5000.0 + ((n + 3) * 200),
    4000.0 + ((n + 3) * 150),
    'Active',
    DATEADD(DAY, -(n + 3), GETDATE()),
    1
FROM (SELECT TOP 37 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Warehouses: Added 37 records (Total: 40)';
GO

-- 1.3 STORAGE ZONES (40 records - distributed across warehouses)
PRINT 'Adding Storage Zones (40 records)...';

INSERT INTO StorageZones (WarehouseId, ZoneCode, ZoneName, Capacity, CurrentOccupancy, Status, CreatedDate, IsActive)
SELECT
    ((n - 1) % 40) + 1,  -- Distribute across first 40 warehouses
    'ZONE-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'Zone ' + CAST(n AS VARCHAR) + ' - ' +
        CASE (n % 4)
            WHEN 0 THEN 'Raw Material'
            WHEN 1 THEN 'Finished Goods'
            WHEN 2 THEN 'By-Products'
            ELSE 'Quarantine' END,
    1000.0 + (n * 50),
    500.0 + (n * 25),
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Storage Zones: Added 40 records';
GO

-- ============================================
-- SECTION 2: INVENTORY (Complete missing data)
-- ============================================

PRINT '';
PRINT '📦 INVENTORY SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 2.1 STOCK MOVEMENTS (Currently 10, need 30 more to reach 40)
PRINT 'Adding Stock Movements (30 more records)...';

INSERT INTO StockMovements (MovementCode, MovementDate, ProductId, FromWarehouseId, FromZoneId,
                            ToWarehouseId, ToZoneId, Quantity, UnitOfMeasure, MovementType,
                            Reason, ApprovedBy, Status, CreatedDate, IsActive)
SELECT
    'MOV-' + FORMAT(DATEADD(DAY, -(n + 10), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST((n + 10) AS VARCHAR), 4),
    DATEADD(DAY, -(n + 10), GETDATE()),
    ((n + 10) % 59) + 1,  -- Product IDs 1-59
    ((n + 10) % 40) + 1,  -- From Warehouse
    ((n + 10) % 40) + 1,  -- From Zone
    (((n + 10) + 1) % 40) + 1,  -- To Warehouse (different from From)
    (((n + 10) + 1) % 40) + 1,  -- To Zone
    100.0 + ((n + 10) * 10),
    'KG',
    CASE ((n + 10) % 3)
        WHEN 0 THEN 'Transfer'
        WHEN 1 THEN 'Relocation'
        ELSE 'Consolidation' END,
    'Stock optimization',
    ((n + 10) % 45) + 1,  -- Employee ID
    'Completed',
    DATEADD(DAY, -(n + 10), GETDATE()),
    1
FROM (SELECT TOP 30 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Stock Movements: Added 30 records (Total: 40)';
GO

-- 2.2 STOCK ADJUSTMENTS (40 records)
PRINT 'Adding Stock Adjustments (40 records)...';

INSERT INTO StockAdjustments (AdjustmentCode, AdjustmentDate, ProductId, WarehouseId, ZoneId,
                              AdjustmentType, Quantity, UnitOfMeasure, Reason, ApprovedBy,
                              Status, CreatedDate, IsActive)
SELECT
    'ADJ-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    (n % 59) + 1,  -- Product IDs
    (n % 40) + 1,  -- Warehouse IDs
    (n % 40) + 1,  -- Zone IDs
    CASE (n % 4)
        WHEN 0 THEN 'Physical Count'
        WHEN 1 THEN 'Damage'
        WHEN 2 THEN 'Expiry'
        ELSE 'System Correction' END,
    CASE (n % 2)
        WHEN 0 THEN (n * 5.0)  -- Positive adjustment
        ELSE -(n * 3.0) END,    -- Negative adjustment
    'KG',
    'Adjustment reason for entry ' + CAST(n AS VARCHAR),
    (n % 45) + 1,  -- Employee ID
    'Approved',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Stock Adjustments: Added 40 records';
GO

-- ============================================
-- SECTION 3: PRODUCTION (All empty - need 40+ each)
-- ============================================

PRINT '';
PRINT '🏭 PRODUCTION SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 3.1 PRODUCTION ORDERS (45 records)
PRINT 'Adding Production Orders (45 records)...';

INSERT INTO ProductionOrders (OrderNumber, OrderDate, PaddyProductId, TargetRiceProductId,
                              QuantityRequired, QuantityProduced, AssignedMachineId, AssignedSupervisorId,
                              PlannedStartDate, ActualStartDate, PlannedEndDate, ActualEndDate,
                              Priority, Status, Remarks, CreatedDate, IsActive)
SELECT
    'PO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(DAY, -n, GETDATE()),
    CASE (n % 15) + 1 WHEN 0 THEN 1 ELSE (n % 15) + 1 END,  -- Paddy products (1-15)
    ((n % 20) + 16),  -- Rice products (16-35)
    1000.0 + (n * 50),
    CASE (n % 4)
        WHEN 0 THEN 1000.0 + (n * 50)  -- Completed
        WHEN 1 THEN 500.0 + (n * 25)   -- Partial
        ELSE 0 END,  -- Not started
    (n % 45) + 1,  -- Machine ID
    ((n % 10) + 1),  -- Supervisor (first 10 employees)
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN (n % 4) <= 1 THEN DATEADD(DAY, -n+1, GETDATE()) ELSE NULL END,
    DATEADD(DAY, -n+7, GETDATE()),
    CASE WHEN (n % 4) = 0 THEN DATEADD(DAY, -n+6, GETDATE()) ELSE NULL END,
    CASE (n % 3)
        WHEN 0 THEN 'High'
        WHEN 1 THEN 'Medium'
        ELSE 'Low' END,
    CASE (n % 4)
        WHEN 0 THEN 'Completed'
        WHEN 1 THEN 'In Progress'
        WHEN 2 THEN 'Pending'
        ELSE 'Planned' END,
    'Production order ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Orders: Added 45 records';
GO

-- 3.2 PRODUCTION BATCHES (48 records)
PRINT 'Adding Production Batches (48 records)...';

INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, MachineId, OperatorId, SupervisorId,
                               ShiftType, StartTime, EndTime, Status, CompletionPercent, QualityScore,
                               Remarks, CreatedDate, IsActive)
SELECT
    'BATCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    ((n - 1) % 45) + 1,  -- Production Order IDs (1-45)
    DATEADD(DAY, -n, GETDATE()),
    (n % 45) + 1,  -- Machine IDs
    ((n % 35) + 11),  -- Operator IDs (employees 11-45)
    ((n % 10) + 1),  -- Supervisor IDs (employees 1-10)
    CASE (n % 3)
        WHEN 0 THEN 'Morning'
        WHEN 1 THEN 'Evening'
        ELSE 'Night' END,
    DATEADD(HOUR, (n % 3) * 8, CAST(DATEADD(DAY, -n, GETDATE()) AS DATETIME)),
    CASE (n % 3)
        WHEN 0 THEN DATEADD(HOUR, ((n % 3) * 8) + 7, CAST(DATEADD(DAY, -n, GETDATE()) AS DATETIME))
        ELSE NULL END,
    CASE (n % 3)
        WHEN 0 THEN 'Completed'
        WHEN 1 THEN 'In Progress'
        ELSE 'Started' END,
    CASE (n % 3)
        WHEN 0 THEN 100.0
        WHEN 1 THEN 50.0 + (n % 40)
        ELSE 10.0 + (n % 20) END,
    85.0 + (n % 15),
    'Batch processing ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Batches: Added 48 records';
GO

-- 3.3 BATCH INPUTS (120 records - avg 2.5 per batch)
PRINT 'Adding Batch Inputs (120 records)...';

INSERT INTO BatchInputs (BatchId, ProductId, WarehouseId, ZoneId, Quantity, UnitOfMeasure, CreatedDate, IsActive)
SELECT
    ((n - 1) % 48) + 1,  -- Batch IDs (1-48)
    ((n % 15) + 1),  -- Paddy products (1-15)
    ((n % 40) + 1),  -- Warehouse IDs
    ((n % 40) + 1),  -- Zone IDs
    200.0 + (n * 10),
    'KG',
    DATEADD(DAY, -((n - 1) % 48), GETDATE()),
    1
FROM (SELECT TOP 120 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Batch Inputs: Added 120 records';
GO

-- 3.4 BATCH OUTPUTS (144 records - avg 3 per batch)
PRINT 'Adding Batch Outputs (144 records)...';

INSERT INTO BatchOutputs (BatchId, ProductId, WarehouseId, ZoneId, Quantity, UnitOfMeasure, CreatedDate, IsActive)
SELECT
    ((n - 1) % 48) + 1,  -- Batch IDs
    CASE ((n - 1) % 3)
        WHEN 0 THEN ((n % 20) + 16)  -- Rice products (16-35)
        WHEN 1 THEN ((n % 15) + 36)  -- By-products (36-50)
        ELSE ((n % 20) + 16) END,  -- More rice
    ((n % 40) + 1),  -- Warehouse IDs
    ((n % 40) + 1),  -- Zone IDs
    150.0 + (n * 8),
    'KG',
    DATEADD(DAY, -((n - 1) % 48), GETDATE()),
    1
FROM (SELECT TOP 144 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Batch Outputs: Added 144 records';
GO

-- 3.5 YIELD RECORDS (48 records - one per completed batch)
PRINT 'Adding Yield Records (48 records)...';

INSERT INTO YieldRecords (BatchId, TotalInputQuantity, TotalOutputQuantity, RiceYieldPercentage,
                          BrokenRicePercentage, BranPercentage, HuskPercentage, YieldEfficiency,
                          QualityGrade, Remarks, CreatedDate, IsActive)
SELECT
    n,  -- Batch IDs (1-48)
    200.0 + (n * 10),  -- Total input
    150.0 + (n * 8),   -- Total output
    65.0 + (n % 15),   -- Rice yield %
    8.0 + (n % 5),     -- Broken rice %
    15.0 + (n % 3),    -- Bran %
    12.0 + (n % 3),    -- Husk %
    85.0 + (n % 15),   -- Efficiency
    CASE (n % 3)
        WHEN 0 THEN 'Grade A'
        WHEN 1 THEN 'Grade B'
        ELSE 'Standard' END,
    'Yield analysis for batch ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Yield Records: Added 48 records';
GO

-- ============================================
-- SECTION 4: PROCUREMENT (Missing tables)
-- ============================================

PRINT '';
PRINT '🛒 PROCUREMENT SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 4.1 RICE PROCUREMENT EXTERNAL (40 records)
PRINT 'Adding Rice Procurement External (40 records)...';

INSERT INTO RiceProcurementExternal (ReceiptDate, VoucherNumber, SupplierName, SupplierContact,
                                     RiceType, Grade, Quantity, Rate, TotalAmount, PaymentMode,
                                     PaymentStatus, WarehouseLocation, VehicleNumber, Remarks,
                                     CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'EXT-PROC-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'External Supplier ' + CAST(n AS VARCHAR),
    '98765' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    CASE (n % 4)
        WHEN 0 THEN 'Basmati Rice'
        WHEN 1 THEN 'Sona Masuri Rice'
        WHEN 2 THEN 'IR-64 Rice'
        ELSE 'Ponni Rice' END,
    CASE (n % 3)
        WHEN 0 THEN 'Grade A'
        WHEN 1 THEN 'Grade B'
        ELSE 'Standard' END,
    500.0 + (n * 25),
    40.0 + (n * 2),
    (500.0 + (n * 25)) * (40.0 + (n * 2)),
    CASE (n % 3)
        WHEN 0 THEN 'Cash'
        WHEN 1 THEN 'Credit'
        ELSE 'Online' END,
    CASE (n % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending' END,
    'Warehouse ' + CAST(((n % 40) + 1) AS VARCHAR),
    'KA' + RIGHT('00' + CAST(n AS VARCHAR), 2) + 'AB' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'External procurement ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Rice Procurement External: Added 40 records';
GO

-- ============================================
-- SECTION 5: SALES (All empty)
-- ============================================

PRINT '';
PRINT '💰 SALES SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 5.1 INQUIRIES (50 records)
PRINT 'Adding Inquiries (50 records)...';

INSERT INTO Inquiries (InquiryNumber, InquiryDate, CustomerId, Source, ProductType, ApproximateQuantity,
                       UnitOfMeasure, ExpectedDeliveryDate, Status, AssignedToEmployeeId, Priority,
                       CustomerRequirements, Remarks, FollowUpDate, CreatedDate, IsActive)
SELECT
    'INQ-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 60) + 1),  -- Customer IDs (1-60)
    CASE (n % 4)
        WHEN 0 THEN 'Phone'
        WHEN 1 THEN 'Email'
        WHEN 2 THEN 'Walk-in'
        ELSE 'Reference' END,
    CASE (n % 4)
        WHEN 0 THEN 'Basmati Rice'
        WHEN 1 THEN 'Sona Masuri'
        WHEN 2 THEN 'IR-64'
        ELSE 'By-Products' END,
    100.0 + (n * 50),
    'KG',
    DATEADD(DAY, -n+15, GETDATE()),
    CASE (n % 4)
        WHEN 0 THEN 'New'
        WHEN 1 THEN 'In Progress'
        WHEN 2 THEN 'Quoted'
        ELSE 'Converted' END,
    ((n % 45) + 1),  -- Employee IDs
    CASE (n % 3)
        WHEN 0 THEN 'High'
        WHEN 1 THEN 'Medium'
        ELSE 'Low' END,
    'Customer requirements: ' + CAST(n AS VARCHAR),
    'Inquiry ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n+3, GETDATE()),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Inquiries: Added 50 records';
GO

-- 5.2 QUOTATIONS (45 records)
PRINT 'Adding Quotations (45 records)...';

INSERT INTO Quotations (QuotationNumber, QuotationDate, CustomerId, InquiryId, ValidUntil,
                        TotalAmount, DiscountPercent, DiscountAmount, TaxAmount, NetAmount,
                        Status, PreparedBy, ApprovedBy, Remarks, CreatedDate, IsActive)
SELECT
    'QUO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 60) + 1),  -- Customer IDs
    ((n % 50) + 1),  -- Inquiry IDs
    DATEADD(DAY, -n+30, GETDATE()),
    100000.0 + (n * 5000),
    5.0,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 0.95 + ((100000.0 + (n * 5000)) * 0.05),
    CASE (n % 4)
        WHEN 0 THEN 'Draft'
        WHEN 1 THEN 'Sent'
        WHEN 2 THEN 'Accepted'
        ELSE 'Rejected' END,
    ((n % 45) + 1),  -- Prepared by Employee ID
    CASE WHEN (n % 4) = 2 THEN ((n % 10) + 1) ELSE NULL END,  -- Approved by (if accepted)
    'Quotation ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Quotations: Added 45 records';
GO

-- 5.3 QUOTATION ITEMS (135 records - avg 3 per quotation)
PRINT 'Adding Quotation Items (135 records)...';

INSERT INTO QuotationItems (QuotationId, ProductId, Quantity, UnitPrice, Discount, TaxPercent,
                            Amount, Remarks, CreatedDate, IsActive)
SELECT
    ((n - 1) % 45) + 1,  -- Quotation IDs (1-45)
    ((n % 50) + 1),  -- Product IDs
    50.0 + (n * 10),
    45.0 + (n * 2.5),
    (50.0 + (n * 10)) * (45.0 + (n * 2.5)) * 0.05,
    5.0,
    (50.0 + (n * 10)) * (45.0 + (n * 2.5)) * 1.05,
    'Item ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -((n - 1) % 45), GETDATE()),
    1
FROM (SELECT TOP 135 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Quotation Items: Added 135 records';
GO

-- 5.4 SALES ORDERS (48 records)
PRINT 'Adding Sales Orders (48 records)...';

INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, ExpectedDeliveryDate,
                         TotalAmount, AdvanceAmount, BalanceAmount, PaymentTerms, Status,
                         ApprovedBy, Remarks, CreatedDate, IsActive)
SELECT
    'SO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 60) + 1),  -- Customer IDs
    ((n % 45) + 1),  -- Quotation IDs
    DATEADD(DAY, -n+10, GETDATE()),
    150000.0 + (n * 7500),
    50000.0 + (n * 2500),
    100000.0 + (n * 5000),
    'NET 30',
    CASE (n % 4)
        WHEN 0 THEN 'Pending'
        WHEN 1 THEN 'Confirmed'
        WHEN 2 THEN 'In Production'
        ELSE 'Completed' END,
    ((n % 10) + 1),  -- Approved by Employee ID
    'Sales order ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Sales Orders: Added 48 records';
GO

-- 5.5 SALES ORDER ITEMS (144 records - avg 3 per order)
PRINT 'Adding Sales Order Items (144 records)...';

INSERT INTO SalesOrderItems (SalesOrderId, ProductId, Quantity, UnitPrice, Discount, TaxPercent,
                             Amount, DeliveryStatus, Remarks, CreatedDate, IsActive)
SELECT
    ((n - 1) % 48) + 1,  -- Sales Order IDs (1-48)
    ((n % 50) + 1),  -- Product IDs
    60.0 + (n * 12),
    48.0 + (n * 2.8),
    (60.0 + (n * 12)) * (48.0 + (n * 2.8)) * 0.05,
    5.0,
    (60.0 + (n * 12)) * (48.0 + (n * 2.8)) * 1.05,
    CASE (n % 3)
        WHEN 0 THEN 'Delivered'
        WHEN 1 THEN 'In Transit'
        ELSE 'Pending' END,
    'Order item ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -((n - 1) % 48), GETDATE()),
    1
FROM (SELECT TOP 144 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Sales Order Items: Added 144 records';
GO

-- 5.6 RICE SALES (50 records)
PRINT 'Adding Rice Sales (50 records)...';

INSERT INTO RiceSales (SaleDate, InvoiceNumber, BillNumber, CustomerName, RiceType, BagSize,
                       NumberOfBags, Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus,
                       DispatchDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'RICE-INV-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'BILL-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Customer ' + CAST(((n % 60) + 1) AS VARCHAR) + ' Pvt Ltd',
    CASE (n % 4)
        WHEN 0 THEN 'Basmati'
        WHEN 1 THEN 'Sona Masuri'
        WHEN 2 THEN 'IR-64'
        ELSE 'Ponni' END,
    CASE (n % 2)
        WHEN 0 THEN '25 KG'
        ELSE '50 KG' END,
    10 + (n * 2),
    250.0 + (n * 50),
    50.0 + (n * 2.5),
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)),
    CASE (n % 3)
        WHEN 0 THEN 'Cash'
        WHEN 1 THEN 'Credit'
        ELSE 'Online' END,
    CASE (n % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending' END,
    DATEADD(DAY, -n+1, GETDATE()),
    'Rice sale ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Rice Sales: Added 50 records';
GO

-- 5.7 BY-PRODUCT SALES (45 records)
PRINT 'Adding By-Product Sales (45 records)...';

INSERT INTO ByProductSales (SaleDate, TransactionNumber, ProductType, BuyerName, BuyerContact,
                            Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus, Remarks,
                            CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'BP-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    CASE (n % 3)
        WHEN 0 THEN 'Rice Bran'
        WHEN 1 THEN 'Rice Husk'
        ELSE 'Broken Rice' END,
    'Buyer ' + CAST(n AS VARCHAR),
    '98765' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    500.0 + (n * 25),
    5.0 + (n * 0.5),
    (500.0 + (n * 25)) * (5.0 + (n * 0.5)),
    CASE (n % 2)
        WHEN 0 THEN 'Cash'
        ELSE 'Credit' END,
    CASE (n % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending' END,
    'By-product sale ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ By-Product Sales: Added 45 records';
GO

-- 5.8 EXTERNAL RICE SALES (40 records)
PRINT 'Adding External Rice Sales (40 records)...';

INSERT INTO ExternalRiceSales (Date, ItemDescription, SoldTo, SoldBy, Quantity, Rate, TotalAmount,
                               PaymentMode, PaymentStatus, Balance, FullPaymentClearanceDate,
                               Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'External Rice Type ' + CAST(n AS VARCHAR),
    'External Customer ' + CAST(n AS VARCHAR),
    'Agent ' + CAST(n AS VARCHAR),
    300.0 + (n * 30),
    45.0 + (n * 2),
    (300.0 + (n * 30)) * (45.0 + (n * 2)),
    CASE (n % 2)
        WHEN 0 THEN 'Cash'
        ELSE 'Credit' END,
    CASE (n % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending' END,
    CASE (n % 2)
        WHEN 1 THEN (300.0 + (n * 30)) * (45.0 + (n * 2)) * 0.3
        ELSE 0 END,
    CASE (n % 2)
        WHEN 0 THEN DATEADD(DAY, -n+5, GETDATE())
        ELSE NULL END,
    'External sale ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ External Rice Sales: Added 40 records';
GO

-- ============================================
-- SECTION 6: FINANCE (All empty)
-- ============================================

PRINT '';
PRINT '💵 FINANCE SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 6.1 BANK TRANSACTIONS (45 records)
PRINT 'Adding Bank Transactions (45 records)...';

INSERT INTO BankTransactions (TransactionDate, ChequeUTRNumber, BankName, AccountNumber, Particulars,
                              Deposits, Withdrawals, Balance, TransactionType, ReconciliationStatus,
                              Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'UTR' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + FORMAT(n, '000000'),
    CASE (n % 3)
        WHEN 0 THEN 'State Bank of India'
        WHEN 1 THEN 'HDFC Bank'
        ELSE 'ICICI Bank' END,
    '1234567890',
    'Transaction ' + CAST(n AS VARCHAR),
    CASE (n % 2)
        WHEN 0 THEN 10000.0 + (n * 500)
        ELSE 0 END,
    CASE (n % 2)
        WHEN 1 THEN 5000.0 + (n * 250)
        ELSE 0 END,
    100000.0 + (n * 1000),
    CASE (n % 2)
        WHEN 0 THEN 'Deposit'
        ELSE 'Withdrawal' END,
    CASE (n % 3)
        WHEN 0 THEN 'Reconciled'
        ELSE 'Pending' END,
    'Bank transaction ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Bank Transactions: Added 45 records';
GO

-- 6.2 CASH BOOK (48 records)
PRINT 'Adding Cash Book (48 records)...';

INSERT INTO CashBook (TransactionDate, VoucherNumber, Particulars, Receipts, Payments, Balance,
                      Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'CASH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'Cash transaction ' + CAST(n AS VARCHAR),
    CASE (n % 2)
        WHEN 0 THEN 5000.0 + (n * 200)
        ELSE 0 END,
    CASE (n % 2)
        WHEN 1 THEN 3000.0 + (n * 150)
        ELSE 0 END,
    50000.0 + (n * 500),
    'Daily cash ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Cash Book: Added 48 records';
GO

-- 6.3 VOUCHERS (50 records)
PRINT 'Adding Vouchers (50 records)...';

INSERT INTO Vouchers (VoucherDate, VoucherType, VoucherNumber, Particulars, Amount, PaymentMode,
                      ReceivedFromPaidTo, ReferenceNumber, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    CASE (n % 3)
        WHEN 0 THEN 'Receipt'
        WHEN 1 THEN 'Payment'
        ELSE 'Journal' END,
    'VCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'Voucher particulars ' + CAST(n AS VARCHAR),
    10000.0 + (n * 500),
    CASE (n % 3)
        WHEN 0 THEN 'Cash'
        WHEN 1 THEN 'Cheque'
        ELSE 'Online' END,
    'Party ' + CAST(n AS VARCHAR),
    'REF-' + CAST(n AS VARCHAR),
    'Voucher ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Vouchers: Added 50 records';
GO

-- 6.4 PAYABLES OVERDUE (40 records)
PRINT 'Adding Payables Overdue (40 records)...';

INSERT INTO PayablesOverdue (VendorName, InvoiceNumber, PurchaseDate, Amount, DueDate, OverdueDays,
                             Status, Remarks, CreatedDate, IsActive)
SELECT
    'Vendor ' + CAST(((n % 40) + 1) AS VARCHAR) + ' Suppliers',
    'PINV-' + FORMAT(DATEADD(DAY, -(n + 60), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(DAY, -(n + 60), GETDATE()),
    50000.0 + (n * 2000),
    DATEADD(DAY, -(n + 30), GETDATE()),
    n,
    CASE (n % 2)
        WHEN 0 THEN 'Overdue'
        ELSE 'Critical' END,
    'Overdue payment ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -(n + 60), GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Payables Overdue: Added 40 records';
GO

-- 6.5 RECEIVABLES OVERDUE (42 records)
PRINT 'Adding Receivables Overdue (42 records)...';

INSERT INTO ReceivablesOverdue (CustomerName, InvoiceNumber, InvoiceDate, Amount, DueDate, OverdueDays,
                                Status, Remarks, CreatedDate, IsActive)
SELECT
    'Customer ' + CAST(((n % 60) + 1) AS VARCHAR) + ' Pvt Ltd',
    'SINV-' + FORMAT(DATEADD(DAY, -(n + 60), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(DAY, -(n + 60), GETDATE()),
    75000.0 + (n * 3000),
    DATEADD(DAY, -(n + 30), GETDATE()),
    n,
    CASE (n % 2)
        WHEN 0 THEN 'Overdue'
        ELSE 'Follow-up' END,
    'Overdue receipt ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -(n + 60), GETDATE()),
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Receivables Overdue: Added 42 records';
GO

-- 6.6 LOANS & ADVANCES (45 records)
PRINT 'Adding Loans & Advances (45 records)...';

INSERT INTO LoansAdvances (TransactionDate, TransactionType, PartyName, Amount, InterestRate,
                           TenureMonths, DueDate, Status, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    CASE (n % 2)
        WHEN 0 THEN 'Loan'
        ELSE 'Advance' END,
    'Party ' + CAST(n AS VARCHAR),
    100000.0 + (n * 5000),
    8.0 + (n % 5),
    12 + (n % 36),
    DATEADD(MONTH, 12, DATEADD(DAY, -n, GETDATE())),
    CASE (n % 3)
        WHEN 0 THEN 'Active'
        WHEN 1 THEN 'Closed'
        ELSE 'Overdue' END,
    'Loan/Advance ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Loans & Advances: Added 45 records';
GO

-- ============================================
-- SECTION 7: ASSETS (Empty)
-- ============================================

PRINT '';
PRINT '🏢 ASSETS SECTION';
PRINT '────────────────────────────────────────────────────────────';

-- 7.1 FIXED ASSETS (42 records)
PRINT 'Adding Fixed Assets (42 records)...';

INSERT INTO FixedAssets (AssetId, PurchaseDate, AssetName, Description, Supplier, PurchaseValue,
                         DepreciationRate, AccumulatedDepreciation, NetBookValue, PresentValueApprox,
                         Status, CreatedDate, IsActive)
SELECT
    'ASSET-' + FORMAT(DATEADD(MONTH, -n, GETDATE()), 'yyyyMM') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(MONTH, -n, GETDATE()),
    CASE (n % 6)
        WHEN 0 THEN 'Rice Mill Machine ' + CAST(n AS VARCHAR)
        WHEN 1 THEN 'Warehouse Equipment ' + CAST(n AS VARCHAR)
        WHEN 2 THEN 'Office Furniture ' + CAST(n AS VARCHAR)
        WHEN 3 THEN 'Vehicle ' + CAST(n AS VARCHAR)
        WHEN 4 THEN 'Computer System ' + CAST(n AS VARCHAR)
        ELSE 'Building Infrastructure ' + CAST(n AS VARCHAR) END,
    'Asset description ' + CAST(n AS VARCHAR),
    'Vendor ' + CAST(((n % 40) + 1) AS VARCHAR) + ' Suppliers',
    500000.0 + (n * 10000),
    10.0 + (n % 10),
    50000.0 + (n * 1000),
    450000.0 + (n * 9000),
    400000.0 + (n * 8000),
    CASE (n % 3)
        WHEN 0 THEN 'Active'
        WHEN 1 THEN 'Under Maintenance'
        ELSE 'Idle' END,
    DATEADD(MONTH, -n, GETDATE()),
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Fixed Assets: Added 42 records';
GO

-- ============================================
-- FINAL SUMMARY
-- ============================================

PRINT '';
PRINT '════════════════════════════════════════════════════════════';
PRINT '  DATA INSERTION COMPLETE!';
PRINT '════════════════════════════════════════════════════════════';
PRINT '';

-- Show summary of all tables
PRINT 'TABLE RECORD COUNTS:';
PRINT '────────────────────────────────────────────────────────────';

SELECT 'MASTER DATA' AS Section, 'Customers' AS TableName, COUNT(*) AS RecordCount FROM Customers
UNION ALL SELECT 'MASTER DATA', 'Vendors', COUNT(*) FROM Vendors
UNION ALL SELECT 'MASTER DATA', 'Products', COUNT(*) FROM Products
UNION ALL SELECT 'MASTER DATA', 'Employees', COUNT(*) FROM Employees
UNION ALL SELECT 'INVENTORY', 'Warehouses', COUNT(*) FROM Warehouses
UNION ALL SELECT 'INVENTORY', 'StorageZones', COUNT(*) FROM StorageZones
UNION ALL SELECT 'INVENTORY', 'InventoryLedger', COUNT(*) FROM InventoryLedger
UNION ALL SELECT 'INVENTORY', 'StockMovements', COUNT(*) FROM StockMovements
UNION ALL SELECT 'INVENTORY', 'StockAdjustments', COUNT(*) FROM StockAdjustments
UNION ALL SELECT 'PRODUCTION', 'Machines', COUNT(*) FROM Machines
UNION ALL SELECT 'PRODUCTION', 'ProductionOrders', COUNT(*) FROM ProductionOrders
UNION ALL SELECT 'PRODUCTION', 'ProductionBatches', COUNT(*) FROM ProductionBatches
UNION ALL SELECT 'PRODUCTION', 'BatchInputs', COUNT(*) FROM BatchInputs
UNION ALL SELECT 'PRODUCTION', 'BatchOutputs', COUNT(*) FROM BatchOutputs
UNION ALL SELECT 'PRODUCTION', 'YieldRecords', COUNT(*) FROM YieldRecords
UNION ALL SELECT 'PROCUREMENT', 'PaddyProcurement', COUNT(*) FROM PaddyProcurement
UNION ALL SELECT 'PROCUREMENT', 'RiceProcurementExternal', COUNT(*) FROM RiceProcurementExternal
UNION ALL SELECT 'SALES', 'Inquiries', COUNT(*) FROM Inquiries
UNION ALL SELECT 'SALES', 'Quotations', COUNT(*) FROM Quotations
UNION ALL SELECT 'SALES', 'QuotationItems', COUNT(*) FROM QuotationItems
UNION ALL SELECT 'SALES', 'SalesOrders', COUNT(*) FROM SalesOrders
UNION ALL SELECT 'SALES', 'SalesOrderItems', COUNT(*) FROM SalesOrderItems
UNION ALL SELECT 'SALES', 'RiceSales', COUNT(*) FROM RiceSales
UNION ALL SELECT 'SALES', 'ByProductSales', COUNT(*) FROM ByProductSales
UNION ALL SELECT 'SALES', 'ExternalRiceSales', COUNT(*) FROM ExternalRiceSales
UNION ALL SELECT 'FINANCE', 'BankTransactions', COUNT(*) FROM BankTransactions
UNION ALL SELECT 'FINANCE', 'CashBook', COUNT(*) FROM CashBook
UNION ALL SELECT 'FINANCE', 'Vouchers', COUNT(*) FROM Vouchers
UNION ALL SELECT 'FINANCE', 'PayablesOverdue', COUNT(*) FROM PayablesOverdue
UNION ALL SELECT 'FINANCE', 'ReceivablesOverdue', COUNT(*) FROM ReceivablesOverdue
UNION ALL SELECT 'FINANCE', 'LoansAdvances', COUNT(*) FROM LoansAdvances
UNION ALL SELECT 'ASSETS', 'FixedAssets', COUNT(*) FROM FixedAssets
ORDER BY Section, TableName;

PRINT '';
PRINT '════════════════════════════════════════════════════════════';
PRINT '  ✅ ALL TABLES NOW HAVE 40+ RECORDS!';
PRINT '════════════════════════════════════════════════════════════';

SET NOCOUNT OFF;
GO
