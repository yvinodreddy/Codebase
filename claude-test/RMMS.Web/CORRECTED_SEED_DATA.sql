-- ============================================
-- CORRECTED SEED DATA BASED ON ACTUAL SCHEMA
-- Generated: 2025-10-12
-- Purpose: Insert data with correct column names
-- ============================================

USE RMMS_Production;
GO

SET NOCOUNT ON;
PRINT '════════════════════════════════════════════════════════════';
PRINT '  RMMS CORRECTED DATA SEEDING';
PRINT '════════════════════════════════════════════════════════════';
PRINT '';

-- 1. VENDORS (need 35 more)
PRINT 'Inserting Vendors...';
INSERT INTO Vendors (VendorCode, VendorName, VendorType, Category, GSTIN, PAN, PaymentTerms,
                     BankName, BankAccountNumber, IFSCCode, Rating, Status, CreatedDate, IsActive)
SELECT
    'VEN-' + RIGHT('00000' + CAST((n + 5) AS VARCHAR), 5),
    'Vendor ' + CAST((n + 5) AS VARCHAR) + ' Suppliers',
    CASE WHEN n % 3 = 0 THEN 'Farmer' WHEN n % 3 = 1 THEN 'Trader' ELSE 'Agent' END,
    CASE WHEN n % 2 = 0 THEN 'Local' ELSE 'Interstate' END,
    '29VEND' + RIGHT('00000' + CAST((n + 5) AS VARCHAR), 5) + 'Z1',
    'VEND' + RIGHT('00000' + CAST((n + 5) AS VARCHAR), 5) + 'P',
    'NET 60',
    CASE WHEN n % 3 = 0 THEN 'SBI' WHEN n % 3 = 1 THEN 'HDFC' ELSE 'ICICI' END,
    '1234567890' + CAST((n + 5) AS VARCHAR),
    'SBIN0001234',
    4.0 + (n % 2),
    'Active',
    DATEADD(DAY, -(n + 5), GETDATE()),
    1
FROM (SELECT TOP 35 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Vendors: Added 35 records';
GO

-- 2. WAREHOUSES (need 37 more) - Note: UsedCapacity is required
PRINT 'Inserting Warehouses...';
INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, Address, City, State, Pincode,
                        TotalCapacity, UsedCapacity, AvailableCapacity, ContactPerson, Mobile, Email,
                        WarehouseType, IsTemperatureControlled, Temperature, Humidity, Status, Remarks,
                        CreatedDate, IsActive)
SELECT
    'WH-' + RIGHT('00000' + CAST((n + 3) AS VARCHAR), 5),
    'Warehouse ' + CAST((n + 3) AS VARCHAR),
    'Location ' + CAST((n + 3) AS VARCHAR),
    'Warehouse Address ' + CAST((n + 3) AS VARCHAR),
    CASE (n + 3) % 10 WHEN 0 THEN 'Bangalore' WHEN 1 THEN 'Mysore' WHEN 2 THEN 'Mandya' WHEN 3 THEN 'Tumkur' WHEN 4 THEN 'Hassan'
         WHEN 5 THEN 'Belgaum' WHEN 6 THEN 'Hubli' WHEN 7 THEN 'Mangalore' WHEN 8 THEN 'Gulbarga' ELSE 'Davangere' END,
    'Karnataka',
    '5600' + RIGHT('00' + CAST((n + 3) AS VARCHAR), 2),
    5000.0 + ((n + 3) * 200),
    1000.0 + ((n + 3) * 50),  -- UsedCapacity
    4000.0 + ((n + 3) * 150),  -- AvailableCapacity
    'Contact Person ' + CAST((n + 3) AS VARCHAR),
    '98765' + RIGHT('00000' + CAST((n + 3) AS VARCHAR), 5),
    'wh' + CAST((n + 3) AS VARCHAR) + '@rmms.com',
    'Standard',
    CASE WHEN (n + 3) % 3 = 0 THEN 1 ELSE 0 END,
    CASE WHEN (n + 3) % 3 = 0 THEN 20.0 ELSE NULL END,
    CASE WHEN (n + 3) % 3 = 0 THEN 60.0 ELSE NULL END,
    'Active',
    'Warehouse ' + CAST((n + 3) AS VARCHAR),
    DATEADD(DAY, -(n + 3), GETDATE()),
    1
FROM (SELECT TOP 37 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Warehouses: Added 37 records';
GO

-- 3. STORAGE ZONES (need 40)
PRINT 'Inserting Storage Zones...';
INSERT INTO StorageZones (WarehouseId, ZoneCode, ZoneName, ZoneType, Capacity, UsedCapacity, AvailableCapacity,
                          Temperature, Humidity, Status, Remarks, CreatedDate, IsActive)
SELECT
    ((n - 1) % 40) + 1,
    'ZONE-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'Zone ' + CAST(n AS VARCHAR),
    CASE (n % 4) WHEN 0 THEN 'Raw Material' WHEN 1 THEN 'Finished Goods' WHEN 2 THEN 'By-Products' ELSE 'Quarantine' END,
    1000.0 + (n * 50),
    200.0 + (n * 10),  -- UsedCapacity
    800.0 + (n * 40),   -- AvailableCapacity
    20.0 + (n % 10),
    55.0 + (n % 20),
    'Active',
    'Storage zone ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Storage Zones: Added 40 records';
GO

-- 4. STOCK MOVEMENTS (need 30 more)
PRINT 'Inserting Stock Movements...';
INSERT INTO StockMovements (MovementCode, ProductId, WarehouseId, ZoneId, MovementType, MovementCategory,
                            Quantity, UnitCost, TotalCost, ReferenceType, ReferenceId, ReferenceNumber,
                            MovementDate, PerformedBy, Remarks, IsApproved, ApprovedBy, ApprovalDate,
                            CreatedDate, IsActive)
SELECT
    'MOV-' + FORMAT(DATEADD(DAY, -(n + 10), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST((n + 10) AS VARCHAR), 4),
    ((n + 10) % 59) + 1,
    ((n + 10) % 40) + 1,
    ((n + 10) % 40) + 1,
    CASE ((n + 10) % 5) WHEN 0 THEN 'In' WHEN 1 THEN 'Out' WHEN 2 THEN 'Transfer' WHEN 3 THEN 'Adjustment' ELSE 'Return' END,
    'General',
    100.0 + ((n + 10) * 10),
    25.0 + ((n + 10) * 2),
    (100.0 + ((n + 10) * 10)) * (25.0 + ((n + 10) * 2)),
    'Manual',
    (n + 10),
    'REF-' + CAST((n + 10) AS VARCHAR),
    DATEADD(DAY, -(n + 10), GETDATE()),
    1,
    'Stock movement ' + CAST((n + 10) AS VARCHAR),
    1,
    1,
    DATEADD(DAY, -(n + 10), GETDATE()),
    DATEADD(DAY, -(n + 10), GETDATE()),
    1
FROM (SELECT TOP 30 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Stock Movements: Added 30 records';
GO

-- 5. STOCK ADJUSTMENTS (need 40)
PRINT 'Inserting Stock Adjustments...';
INSERT INTO StockAdjustments (AdjustmentCode, ProductId, WarehouseId, ZoneId, AdjustmentType, Quantity,
                              Reason, BeforeQuantity, AfterQuantity, AdjustmentDate, Remarks,
                              RequiresApproval, IsApproved, ApprovedBy, ApprovalDate, IsRejected,
                              CreatedDate, IsActive)
SELECT
    'ADJ-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    (n % 59) + 1,
    (n % 40) + 1,
    (n % 40) + 1,
    CASE (n % 4) WHEN 0 THEN 'Physical Count' WHEN 1 THEN 'Damage' WHEN 2 THEN 'Expiry' ELSE 'System Correction' END,
    CASE (n % 2) WHEN 0 THEN (n * 5.0) ELSE -(n * 3.0) END,
    'Adjustment reason ' + CAST(n AS VARCHAR),
    1000.0 + (n * 50),
    1000.0 + (n * 50) + CASE (n % 2) WHEN 0 THEN (n * 5.0) ELSE -(n * 3.0) END,
    DATEADD(DAY, -n, GETDATE()),
    'Stock adjustment ' + CAST(n AS VARCHAR),
    1,
    1,
    1,
    DATEADD(DAY, -n, GETDATE()),
    0,
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Stock Adjustments: Added 40 records';
GO

-- 6. PRODUCTION ORDERS (need 45)
PRINT 'Inserting Production Orders...';
INSERT INTO ProductionOrders (OrderNumber, OrderDate, ScheduledDate, SourceType, SourceId, SourceReferenceNumber,
                              PaddyProductId, PaddyVariety, PaddyQuantity, PaddyUOM, TargetRiceProductId,
                              TargetRiceGrade, TargetQuantity, ExpectedYieldPercent, Priority,
                              AssignedMachineId, AssignedSupervisorId, Status, ActualStartDate, Remarks,
                              CreatedDate, IsActive)
SELECT
    'PO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(DAY, -n, GETDATE()),
    DATEADD(DAY, -n+2, GETDATE()),
    'Direct',
    n,
    'SRC-' + CAST(n AS VARCHAR),
    CASE (n % 15) + 1 WHEN 0 THEN 1 ELSE (n % 15) + 1 END,
    CASE (n % 4) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masuri' WHEN 2 THEN 'IR-64' ELSE 'Ponni' END,
    1000.0 + (n * 50),
    'KG',
    ((n % 20) + 16),
    CASE (n % 3) WHEN 0 THEN 'Grade A' WHEN 1 THEN 'Grade B' ELSE 'Standard' END,
    700.0 + (n * 35),
    70.0,
    CASE (n % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Low' END,
    (n % 45) + 1,
    ((n % 10) + 1),
    CASE (n % 4) WHEN 0 THEN 'Completed' WHEN 1 THEN 'In Progress' WHEN 2 THEN 'Pending' ELSE 'Planned' END,
    CASE WHEN (n % 4) <= 1 THEN DATEADD(DAY, -n+1, GETDATE()) ELSE NULL END,
    'Production order ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Production Orders: Added 45 records';
GO

-- 7. PRODUCTION BATCHES (need 48)
PRINT 'Inserting Production Batches...';
INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, ShiftType, OperatorId, SupervisorId,
                               StartTime, EndTime, Status, CompletionPercent, QualityScore, QualityRemarks,
                               Remarks, CreatedDate, IsActive)
SELECT
    'BATCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    ((n - 1) % 45) + 1,
    DATEADD(DAY, -n, GETDATE()),
    CASE (n % 3) WHEN 0 THEN 'Morning' WHEN 1 THEN 'Evening' ELSE 'Night' END,
    ((n % 35) + 11),
    ((n % 10) + 1),
    DATEADD(HOUR, (n % 3) * 8, CAST(DATEADD(DAY, -n, GETDATE()) AS DATETIME)),
    CASE (n % 3) WHEN 0 THEN DATEADD(HOUR, ((n % 3) * 8) + 7, CAST(DATEADD(DAY, -n, GETDATE()) AS DATETIME)) ELSE NULL END,
    CASE (n % 3) WHEN 0 THEN 'Completed' WHEN 1 THEN 'In Progress' ELSE 'Started' END,
    CASE (n % 3) WHEN 0 THEN 100.0 WHEN 1 THEN 50.0 + (n % 40) ELSE 10.0 + (n % 20) END,
    85.0 + (n % 15),
    'Quality: ' + CASE WHEN (85.0 + (n % 15)) >= 90 THEN 'Excellent' WHEN (85.0 + (n % 15)) >= 80 THEN 'Good' ELSE 'Average' END,
    'Batch processing ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Production Batches: Added 48 records';
GO

-- 8. BATCH INPUTS (need 120)
PRINT 'Inserting Batch Inputs...';
INSERT INTO BatchInputs (BatchId, InputType, ProductId, Quantity, UOM, WarehouseId, ZoneId,
                         MoistureContent, BatchLotNumber, Grade, UnitCost, Remarks, CreatedDate)
SELECT
    ((n - 1) % 48) + 1,
    'Paddy',
    ((n % 15) + 1),
    200.0 + (n * 10),
    'KG',
    ((n % 40) + 1),
    ((n % 40) + 1),
    14.0 + (n % 5),
    'LOT-' + CAST(n AS VARCHAR),
    CASE (n % 3) WHEN 0 THEN 'Grade A' WHEN 1 THEN 'Grade B' ELSE 'Standard' END,
    25.0 + (n * 2),
    'Input ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -((n - 1) % 48), GETDATE())
FROM (SELECT TOP 120 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Batch Inputs: Added 120 records';
GO

-- 9. BATCH OUTPUTS (need 144)
PRINT 'Inserting Batch Outputs...';
INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, ZoneId,
                          QualityScore, MoistureContent, BatchLotNumber, UnitCost, BagsCount, BagsWeight,
                          Remarks, CreatedDate)
SELECT
    ((n - 1) % 48) + 1,
    CASE ((n - 1) % 3) WHEN 0 THEN 'Rice' WHEN 1 THEN 'Bran' ELSE 'Husk' END,
    CASE ((n - 1) % 3) WHEN 0 THEN ((n % 20) + 16) ELSE ((n % 15) + 36) END,
    CASE (n % 3) WHEN 0 THEN 'Grade A' WHEN 1 THEN 'Grade B' ELSE 'Standard' END,
    150.0 + (n * 8),
    'KG',
    ((n % 40) + 1),
    ((n % 40) + 1),
    85.0 + (n % 15),
    12.0 + (n % 3),
    'OUTLOT-' + CAST(n AS VARCHAR),
    45.0 + (n * 2),
    (150.0 + (n * 8)) / 25.0,
    25.0,
    'Output ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -((n - 1) % 48), GETDATE())
FROM (SELECT TOP 144 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Batch Outputs: Added 144 records';
GO

-- 10. YIELD RECORDS (need 48)
PRINT 'Inserting Yield Records...';
INSERT INTO YieldRecords (BatchId, PaddyVariety, InputPaddyQuantity, OutputHeadRice, OutputBrokenRice,
                          OutputBran, OutputHusk, OutputWastage, HeadRicePercent, BrokenRicePercent,
                          BranPercent, HuskPercent, WastagePercent, TotalYieldPercent,
                          StandardHeadRicePercent, StandardTotalYieldPercent, YieldGrade, QualityScore,
                          MillingRecovery, HeadRiceToBrokenRatio, Remarks, CalculatedDate)
SELECT
    n,
    CASE (n % 4) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masuri' WHEN 2 THEN 'IR-64' ELSE 'Ponni' END,
    200.0 + (n * 10),
    130.0 + (n * 6.5),
    16.0 + (n * 0.8),
    30.0 + (n * 1.5),
    24.0 + (n * 1.2),
    0.0 + (n * 0.05),
    65.0 + (n % 10),
    8.0 + (n % 5),
    15.0,
    12.0,
    0.0 + (n % 2),
    100.0,
    70.0,
    100.0,
    CASE (n % 3) WHEN 0 THEN 'A' WHEN 1 THEN 'B' ELSE 'C' END,
    85.0 + (n % 15),
    73.0 + (n % 10),
    8.125,
    'Yield analysis for batch ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE())
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Yield Records: Added 48 records';
GO

-- 11. RICE PROCUREMENT EXTERNAL (need 40)
PRINT 'Inserting Rice Procurement External...';
INSERT INTO RiceProcurementExternal (Date, ItemDescription, ProcuredFrom, ProcuredBy, Quantity, Rate,
                                     TotalAmount, PaymentMode, PaymentStatus, Balance, FullPaymentDate,
                                     Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'Rice Type ' + CAST(n AS VARCHAR),
    'Supplier ' + CAST(n AS VARCHAR),
    'Agent ' + CAST(n AS VARCHAR),
    500.0 + (n * 25),
    40.0 + (n * 2),
    (500.0 + (n * 25)) * (40.0 + (n * 2)),
    CASE (n % 3) WHEN 0 THEN 'Cash' WHEN 1 THEN 'Credit' ELSE 'Online' END,
    CASE (n % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    CASE (n % 2) WHEN 1 THEN (500.0 + (n * 25)) * (40.0 + (n * 2)) * 0.3 ELSE 0 END,
    CASE (n % 2) WHEN 0 THEN DATEADD(DAY, -n+5, GETDATE()) ELSE NULL END,
    'External procurement ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Rice Procurement External: Added 40 records';
GO

-- 12. INQUIRIES (need 50) - Note: CustomerId must exist
PRINT 'Inserting Inquiries...';
INSERT INTO Inquiries (InquiryNumber, InquiryDate, CustomerId, Source, ProductType, ApproximateQuantity,
                       UnitOfMeasure, ExpectedDeliveryDate, Status, AssignedToEmployeeId, Priority,
                       CustomerRequirements, Remarks, FollowUpDate, CreatedDate, IsActive)
SELECT
    'INQ-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 60) + 1),
    CASE (n % 4) WHEN 0 THEN 'Phone' WHEN 1 THEN 'Email' WHEN 2 THEN 'Walk-in' ELSE 'Reference' END,
    CASE (n % 4) WHEN 0 THEN 'Basmati Rice' WHEN 1 THEN 'Sona Masuri' WHEN 2 THEN 'IR-64' ELSE 'By-Products' END,
    100.0 + (n * 50),
    'KG',
    DATEADD(DAY, -n+15, GETDATE()),
    CASE (n % 4) WHEN 0 THEN 'New' WHEN 1 THEN 'In Progress' WHEN 2 THEN 'Quoted' ELSE 'Converted' END,
    ((n % 45) + 1),
    CASE (n % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Low' END,
    'Customer requirements: ' + CAST(n AS VARCHAR),
    'Inquiry ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n+3, GETDATE()),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Inquiries: Added 50 records';
GO

-- 13. QUOTATIONS (need 45)
PRINT 'Inserting Quotations...';
INSERT INTO Quotations (QuotationNumber, QuotationDate, InquiryId, CustomerId, ValidUntil, PaymentTerms,
                        DeliveryTerms, SubtotalAmount, DiscountPercent, DiscountAmount, TaxAmount, TotalAmount,
                        Status, ApprovedByEmployeeId, ApprovalDate, TermsAndConditions, Remarks,
                        CreatedDate, IsActive)
SELECT
    'QUO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 50) + 1),
    ((n % 60) + 1),
    DATEADD(DAY, -n+30, GETDATE()),
    'NET 30',
    'FOB',
    100000.0 + (n * 5000),
    5.0,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 1.0,
    CASE (n % 4) WHEN 0 THEN 'Draft' WHEN 1 THEN 'Sent' WHEN 2 THEN 'Accepted' ELSE 'Rejected' END,
    CASE WHEN (n % 4) = 2 THEN ((n % 10) + 1) ELSE NULL END,
    CASE WHEN (n % 4) = 2 THEN DATEADD(DAY, -n, GETDATE()) ELSE NULL END,
    'Standard terms and conditions',
    'Quotation ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Quotations: Added 45 records';
GO

-- 14. QUOTATION ITEMS (need 135)
PRINT 'Inserting Quotation Items...';
INSERT INTO QuotationItems (QuotationId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice,
                            DiscountPercent, DiscountAmount, TaxPercent, TaxAmount, TotalAmount, Remarks)
SELECT
    ((n - 1) % 45) + 1,
    ((n % 50) + 1),
    'Product ' + CAST(((n % 50) + 1) AS VARCHAR),
    50.0 + (n * 10),
    'KG',
    45.0 + (n * 2.5),
    5.0,
    (50.0 + (n * 10)) * (45.0 + (n * 2.5)) * 0.05,
    5.0,
    (50.0 + (n * 10)) * (45.0 + (n * 2.5)) * 0.05,
    (50.0 + (n * 10)) * (45.0 + (n * 2.5)),
    'Item ' + CAST(n AS VARCHAR)
FROM (SELECT TOP 135 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Quotation Items: Added 135 records';
GO

-- 15. SALES ORDERS (need 48)
PRINT 'Inserting Sales Orders...';
INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, DeliveryDate, DeliveryAddress,
                         PaymentTerms, DeliveryTerms, SubtotalAmount, DiscountAmount, TaxAmount,
                         FreightCharges, OtherCharges, TotalAmount, Status, Priority, ApprovedByEmployeeId,
                         ApprovalDate, StockReserved, SpecialInstructions, Remarks, CreatedDate, IsActive)
SELECT
    'SO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    DATEADD(DAY, -n, GETDATE()),
    ((n % 60) + 1),
    ((n % 45) + 1),
    DATEADD(DAY, -n+10, GETDATE()),
    'Delivery address ' + CAST(n AS VARCHAR),
    'NET 30',
    'FOB',
    150000.0 + (n * 7500),
    5000.0 + (n * 250),
    7500.0 + (n * 375),
    1000.0,
    500.0,
    150000.0 + (n * 7500),
    CASE (n % 4) WHEN 0 THEN 'Pending' WHEN 1 THEN 'Confirmed' WHEN 2 THEN 'In Production' ELSE 'Completed' END,
    CASE (n % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Low' END,
    ((n % 10) + 1),
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN (n % 2) = 0 THEN 1 ELSE 0 END,
    'Special instructions ' + CAST(n AS VARCHAR),
    'Sales order ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Sales Orders: Added 48 records';
GO

-- 16. SALES ORDER ITEMS (need 144)
PRINT 'Inserting Sales Order Items...';
INSERT INTO SalesOrderItems (SalesOrderId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice,
                             DiscountAmount, TaxAmount, TotalAmount, AllocatedQuantity, DispatchedQuantity,
                             WarehouseId, Remarks)
SELECT
    ((n - 1) % 48) + 1,
    ((n % 50) + 1),
    'Product ' + CAST(((n % 50) + 1) AS VARCHAR),
    60.0 + (n * 12),
    'KG',
    48.0 + (n * 2.8),
    (60.0 + (n * 12)) * (48.0 + (n * 2.8)) * 0.05,
    (60.0 + (n * 12)) * (48.0 + (n * 2.8)) * 0.05,
    (60.0 + (n * 12)) * (48.0 + (n * 2.8)),
    60.0 + (n * 12),
    CASE (n % 3) WHEN 0 THEN 60.0 + (n * 12) ELSE 0 END,
    ((n % 40) + 1),
    'Order item ' + CAST(n AS VARCHAR)
FROM (SELECT TOP 144 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Sales Order Items: Added 144 records';
GO

-- 17. RICE SALES (need 50)
PRINT 'Inserting Rice Sales...';
INSERT INTO RiceSales (SaleDate, InvoiceNumber, BuyerName, BuyerAddress, BuyerGSTIN, RiceGrade, Quantity,
                       UnitPrice, TotalInvoiceValue, Discount, TaxableValue, CGSTAmount, SGSTAmount, IGSTAmount,
                       TotalTaxAmount, FreightCharges, OtherCharges, GrossInvoiceAmount, PaymentMode,
                       DueDate, PaymentStatus, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'RICE-INV-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    'Buyer ' + CAST(n AS VARCHAR),
    'Address ' + CAST(n AS VARCHAR),
    '29ABC' + RIGHT('00000' + CAST(n AS VARCHAR), 5) + 'D1Z5',
    CASE (n % 3) WHEN 0 THEN 'Grade A' WHEN 1 THEN 'Grade B' ELSE 'Standard' END,
    250.0 + (n * 50),
    50.0 + (n * 2.5),
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)),
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) * 0.05,
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) * 0.95,
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) * 0.025,
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) * 0.025,
    0.0,
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) * 0.05,
    1000.0,
    500.0,
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)) + 1500.0,
    CASE (n % 3) WHEN 0 THEN 'Cash' WHEN 1 THEN 'Credit' ELSE 'Online' END,
    DATEADD(DAY, -n+30, GETDATE()),
    CASE (n % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    'Rice sale ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Rice Sales: Added 50 records';
GO

-- 18. VOUCHERS (need 50)
PRINT 'Inserting Vouchers...';
INSERT INTO Vouchers (VoucherDate, VoucherNumber, VoucherType, Particulars, Amount, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'VCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    CASE (n % 3) WHEN 0 THEN 'Receipt' WHEN 1 THEN 'Payment' ELSE 'Journal' END,
    'Voucher particulars ' + CAST(n AS VARCHAR),
    10000.0 + (n * 500),
    'Voucher ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Vouchers: Added 50 records';
GO

-- 19. PAYABLES OVERDUE (need 40)
PRINT 'Inserting Payables Overdue...';
INSERT INTO PayablesOverdue (PurchaseDate, InvoiceNumber, SupplierName, ItemPurchased, InvoiceAmount,
                             AmountPaid, BalancePayable, DueDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(n + 60), GETDATE()),
    'PINV-' + FORMAT(DATEADD(DAY, -(n + 60), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Supplier ' + CAST(n AS VARCHAR),
    'Item ' + CAST(n AS VARCHAR),
    50000.0 + (n * 2000),
    10000.0 + (n * 400),
    40000.0 + (n * 1600),
    DATEADD(DAY, -(n + 30), GETDATE()),
    'Overdue payment ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -(n + 60), GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Payables Overdue: Added 40 records';
GO

-- 20. RECEIVABLES OVERDUE (need 42)
PRINT 'Inserting Receivables Overdue...';
INSERT INTO ReceivablesOverdue (InvoiceDate, InvoiceNumber, CustomerName, ItemSupplied, InvoiceAmount,
                                AmountReceived, BalanceDue, DueDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(n + 60), GETDATE()),
    'SINV-' + FORMAT(DATEADD(DAY, -(n + 60), GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Customer ' + CAST(n AS VARCHAR),
    'Item ' + CAST(n AS VARCHAR),
    75000.0 + (n * 3000),
    25000.0 + (n * 1000),
    50000.0 + (n * 2000),
    DATEADD(DAY, -(n + 30), GETDATE()),
    'Overdue receipt ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -(n + 60), GETDATE()),
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Receivables Overdue: Added 42 records';
GO

-- 21. LOANS & ADVANCES (need 45)
PRINT 'Inserting Loans & Advances...';
INSERT INTO LoansAdvances (Date, VoucherNumber, Particulars, PartyName, AmountGiven, Repayment, RepaymentDate,
                           Balance, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'LOAN-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Loan/Advance particulars ' + CAST(n AS VARCHAR),
    'Party ' + CAST(n AS VARCHAR),
    100000.0 + (n * 5000),
    CASE (n % 3) WHEN 0 THEN 30000.0 + (n * 1500) ELSE 0 END,
    CASE (n % 3) WHEN 0 THEN DATEADD(DAY, -n+15, GETDATE()) ELSE NULL END,
    100000.0 + (n * 5000) - CASE (n % 3) WHEN 0 THEN 30000.0 + (n * 1500) ELSE 0 END,
    'Loan/Advance ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Loans & Advances: Added 45 records';
GO

SET NOCOUNT OFF;

PRINT '';
PRINT '════════════════════════════════════════════════════════════';
PRINT '  ✅ ALL DATA INSERTION COMPLETE!';
PRINT '════════════════════════════════════════════════════════════';
GO
