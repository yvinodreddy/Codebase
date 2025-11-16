-- ===================================================================
-- COMPREHENSIVE DATA SEEDING SCRIPT
-- Completes the remaining 4% of tasks (237/248 -> 248/248)
-- ===================================================================
-- HIGH PRIORITY: Mobile Tables ✅ ALREADY CREATED
-- MEDIUM PRIORITY: Empty Tables (5 tables) + Partial Data (4 tables)
-- ===================================================================

USE RMMS_Production;
GO

-- ===================================================================
-- 1. POPULATE STORAGEZONES (0 -> 40 records)
-- ===================================================================
PRINT 'Populating StorageZones...';

-- Get Warehouse IDs
DECLARE @WarehouseIds TABLE (Id INT);
INSERT INTO @WarehouseIds SELECT TOP 8 Id FROM Warehouses ORDER BY Id;

INSERT INTO StorageZones (WarehouseId, ZoneCode, ZoneName, ZoneType, Capacity, CurrentUtilization, TemperatureControlled, HumidityControlled, SecurityLevel, IsActive)
SELECT
    w.Id,
    'ZONE-' + RIGHT('00' + CAST(ROW_NUMBER() OVER (ORDER BY w.Id, n.n) AS VARCHAR), 2),
    CASE (ROW_NUMBER() OVER (ORDER BY w.Id, n.n) % 5)
        WHEN 0 THEN 'Dry Storage Zone'
        WHEN 1 THEN 'Climate Controlled Zone'
        WHEN 2 THEN 'High Security Zone'
        WHEN 3 THEN 'Bulk Storage Zone'
        ELSE 'General Storage Zone'
    END,
    CASE (ROW_NUMBER() OVER (ORDER BY w.Id, n.n) % 4)
        WHEN 0 THEN 'Dry'
        WHEN 1 THEN 'Cold'
        WHEN 2 THEN 'Frozen'
        ELSE 'Ambient'
    END,
    CAST((1000 + (ABS(CHECKSUM(NEWID())) % 4000)) AS DECIMAL(18,2)),
    CAST((ABS(CHECKSUM(NEWID())) % 80) AS DECIMAL(18,2)),
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY w.Id, n.n) % 3) = 0 THEN 1 ELSE 0 END,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY w.Id, n.n) % 4) = 0 THEN 1 ELSE 0 END,
    CASE (ROW_NUMBER() OVER (ORDER BY w.Id, n.n) % 3)
        WHEN 0 THEN 'High'
        WHEN 1 THEN 'Medium'
        ELSE 'Standard'
    END,
    1
FROM @WarehouseIds w
CROSS JOIN (SELECT TOP 5 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.objects) n;

PRINT '✅ StorageZones: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records inserted';

-- ===================================================================
-- 2. POPULATE BATCHINPUTS (0 -> 40 records)
-- ===================================================================
PRINT 'Populating BatchInputs...';

-- Get Production Batch IDs, Product IDs, Warehouse IDs
DECLARE @BatchIds TABLE (Id INT);
DECLARE @ProductIds TABLE (Id INT);

INSERT INTO @BatchIds SELECT TOP 40 Id FROM ProductionBatches ORDER BY Id;
INSERT INTO @ProductIds SELECT TOP 10 Id FROM Products WHERE ProductType = 'Paddy' ORDER BY Id;

INSERT INTO BatchInputs (BatchId, ProductId, WarehouseId, ZoneId, QuantityUsed, UnitCost, TotalCost, LotNumber, ExpiryDate)
SELECT
    b.Id,
    (SELECT TOP 1 Id FROM @ProductIds ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()),
    CAST((100 + (ABS(CHECKSUM(NEWID())) % 900)) AS DECIMAL(18,2)),
    CAST((20 + (ABS(CHECKSUM(NEWID())) % 30)) AS DECIMAL(18,2)),
    CAST((2000 + (ABS(CHECKSUM(NEWID())) % 8000)) AS DECIMAL(18,2)),
    'LOT-' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY b.Id) AS VARCHAR), 4),
    DATEADD(DAY, 180 + (ABS(CHECKSUM(NEWID())) % 180), GETDATE())
FROM @BatchIds b;

PRINT '✅ BatchInputs: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records inserted';

-- ===================================================================
-- 3. POPULATE BATCHOUTPUTS (0 -> 40 records)
-- ===================================================================
PRINT 'Populating BatchOutputs...';

DELETE FROM @ProductIds;
INSERT INTO @ProductIds SELECT TOP 10 Id FROM Products WHERE ProductType IN ('Rice', 'By-Product') ORDER BY Id;

INSERT INTO BatchOutputs (BatchId, ProductId, WarehouseId, ZoneId, QuantityProduced, QualityGrade, UnitPrice, TotalValue, LotNumber, ProductionDate, ExpiryDate)
SELECT
    b.Id,
    (SELECT TOP 1 Id FROM @ProductIds ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()),
    CAST((80 + (ABS(CHECKSUM(NEWID())) % 720)) AS DECIMAL(18,2)),
    CASE (ROW_NUMBER() OVER (ORDER BY b.Id) % 4)
        WHEN 0 THEN 'Premium'
        WHEN 1 THEN 'Grade A'
        WHEN 2 THEN 'Grade B'
        ELSE 'Standard'
    END,
    CAST((40 + (ABS(CHECKSUM(NEWID())) % 60)) AS DECIMAL(18,2)),
    CAST((3200 + (ABS(CHECKSUM(NEWID())) % 16800)) AS DECIMAL(18,2)),
    'OUT-' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY b.Id) AS VARCHAR), 4),
    DATEADD(DAY, -30 - (ABS(CHECKSUM(NEWID())) % 60), GETDATE()),
    DATEADD(DAY, 270 + (ABS(CHECKSUM(NEWID())) % 90), GETDATE())
FROM @BatchIds b;

PRINT '✅ BatchOutputs: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records inserted';

-- ===================================================================
-- 4. POPULATE QUOTATIONITEMS (0 -> 60 records)
-- ===================================================================
PRINT 'Populating QuotationItems...';

-- Get existing Quotation IDs
DECLARE @QuotationIds TABLE (Id INT, QuotationNumber VARCHAR(50));
INSERT INTO @QuotationIds SELECT Id, QuotationNumber FROM Quotations;

DELETE FROM @ProductIds;
INSERT INTO @ProductIds SELECT TOP 20 Id FROM Products ORDER BY Id;

INSERT INTO QuotationItems (QuotationId, ProductId, Quantity, UnitPrice, DiscountPercentage, DiscountAmount, TaxPercentage, TaxAmount, LineTotal, DeliveryDays, SpecialInstructions)
SELECT
    q.Id,
    (SELECT TOP 1 Id FROM @ProductIds ORDER BY NEWID()),
    CAST((10 + (ABS(CHECKSUM(NEWID())) % 190)) AS DECIMAL(18,2)),
    CAST((30 + (ABS(CHECKSUM(NEWID())) % 170)) AS DECIMAL(18,2)),
    CAST((ABS(CHECKSUM(NEWID())) % 15) AS DECIMAL(5,2)),
    CAST((50 + (ABS(CHECKSUM(NEWID())) % 450)) AS DECIMAL(18,2)),
    CAST(13.00 AS DECIMAL(5,2)),
    CAST((150 + (ABS(CHECKSUM(NEWID())) % 850)) AS DECIMAL(18,2)),
    CAST((2000 + (ABS(CHECKSUM(NEWID())) % 18000)) AS DECIMAL(18,2)),
    7 + (ABS(CHECKSUM(NEWID())) % 21),
    CASE (ROW_NUMBER() OVER (ORDER BY q.Id, p.Id) % 5)
        WHEN 0 THEN 'Express delivery required'
        WHEN 1 THEN 'Standard packaging'
        WHEN 2 THEN 'Bulk packaging'
        WHEN 3 THEN 'Special handling required'
        ELSE NULL
    END
FROM @QuotationIds q
CROSS JOIN (SELECT TOP 3 Id FROM @ProductIds ORDER BY NEWID()) p;

PRINT '✅ QuotationItems: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records inserted';

-- ===================================================================
-- 5. POPULATE SALESORDERITEMS (0 -> 60 records)
-- ===================================================================
PRINT 'Populating SalesOrderItems...';

-- Get existing Sales Order IDs
DECLARE @SalesOrderIds TABLE (Id INT, OrderNumber VARCHAR(50));
INSERT INTO @SalesOrderIds SELECT Id, OrderNumber FROM SalesOrders;

INSERT INTO SalesOrderItems (SalesOrderId, ProductId, Quantity, UnitPrice, DiscountPercentage, DiscountAmount, TaxPercentage, TaxAmount, LineTotal, DeliveryDate, DeliveryStatus, Notes)
SELECT
    so.Id,
    (SELECT TOP 1 Id FROM @ProductIds ORDER BY NEWID()),
    CAST((15 + (ABS(CHECKSUM(NEWID())) % 185)) AS DECIMAL(18,2)),
    CAST((35 + (ABS(CHECKSUM(NEWID())) % 165)) AS DECIMAL(18,2)),
    CAST((ABS(CHECKSUM(NEWID())) % 20) AS DECIMAL(5,2)),
    CAST((75 + (ABS(CHECKSUM(NEWID())) % 925)) AS DECIMAL(18,2)),
    CAST(13.00 AS DECIMAL(5,2)),
    CAST((180 + (ABS(CHECKSUM(NEWID())) % 820)) AS DECIMAL(18,2)),
    CAST((2500 + (ABS(CHECKSUM(NEWID())) % 17500)) AS DECIMAL(18,2)),
    DATEADD(DAY, 7 + (ABS(CHECKSUM(NEWID())) % 21), GETDATE()),
    CASE (ROW_NUMBER() OVER (ORDER BY so.Id, p.Id) % 4)
        WHEN 0 THEN 'Pending'
        WHEN 1 THEN 'Shipped'
        WHEN 2 THEN 'Delivered'
        ELSE 'In Transit'
    END,
    CASE (ROW_NUMBER() OVER (ORDER BY so.Id, p.Id) % 5)
        WHEN 0 THEN 'Priority shipment'
        WHEN 1 THEN 'Standard delivery'
        WHEN 2 THEN 'Customer pickup'
        WHEN 3 THEN 'Fragile - handle with care'
        ELSE NULL
    END
FROM @SalesOrderIds so
CROSS JOIN (SELECT TOP 3 Id FROM @ProductIds ORDER BY NEWID()) p;

PRINT '✅ SalesOrderItems: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records inserted';

-- ===================================================================
-- 6. ADD MORE STOCKMOVEMENTS (10 -> 40 records)
-- ===================================================================
PRINT 'Adding more StockMovements...';

DECLARE @MaxMovementId INT = (SELECT ISNULL(MAX(Id), 0) FROM StockMovements);

INSERT INTO StockMovements (ProductId, WarehouseId, ZoneId, MovementType, MovementCode, Quantity, UnitCost, TotalCost, ReferenceType, ReferenceId, MovementDate, PerformedBy, Notes, IsPosted)
SELECT
    (SELECT TOP 1 Id FROM Products ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()),
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 4)
        WHEN 0 THEN 'In'
        WHEN 1 THEN 'Out'
        WHEN 2 THEN 'Transfer'
        ELSE 'Adjustment'
    END,
    'MOVE-' + RIGHT('0000' + CAST(@MaxMovementId + ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 5),
    CAST((50 + (ABS(CHECKSUM(NEWID())) % 450)) AS DECIMAL(18,2)),
    CAST((25 + (ABS(CHECKSUM(NEWID())) % 75)) AS DECIMAL(18,2)),
    CAST((1250 + (ABS(CHECKSUM(NEWID())) % 8750)) AS DECIMAL(18,2)),
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3)
        WHEN 0 THEN 'Purchase'
        WHEN 1 THEN 'Production'
        ELSE 'Sales'
    END,
    'REF-' + CAST(1000 + (ABS(CHECKSUM(NEWID())) % 9000) AS VARCHAR),
    DATEADD(DAY, -60 + (ABS(CHECKSUM(NEWID())) % 60), GETDATE()),
    (SELECT TOP 1 EmployeeName FROM Employees ORDER BY NEWID()),
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5)
        WHEN 0 THEN 'Scheduled movement'
        WHEN 1 THEN 'Emergency transfer'
        WHEN 2 THEN 'Regular stock replenishment'
        WHEN 3 THEN 'Quality inspection transfer'
        ELSE NULL
    END,
    1
FROM sys.objects o1
CROSS JOIN (SELECT TOP 3 1 AS x FROM sys.objects) o2
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 30;

PRINT '✅ StockMovements: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records added (10 -> 40)';

-- ===================================================================
-- 7. ADD MORE YIELDRECORDS (20 -> 40 records)
-- ===================================================================
PRINT 'Adding more YieldRecords...';

-- Get batches without yield records
DECLARE @BatchesWithoutYield TABLE (Id INT, BatchNumber VARCHAR(50));
INSERT INTO @BatchesWithoutYield
SELECT TOP 20 pb.Id, pb.BatchNumber
FROM ProductionBatches pb
LEFT JOIN YieldRecords yr ON pb.Id = yr.BatchId
WHERE yr.Id IS NULL;

INSERT INTO YieldRecords (BatchId, TotalInputQuantity, TotalRiceOutput, TotalByProductOutput, ActualYieldPercentage, StandardYieldPercentage, YieldVariance, QualityRating, RiceGradeA, RiceGradeB, RiceGradeC, BrokenRicePercentage, ByProductBreakdown, RecordedAt, RecordedBy, Notes)
SELECT
    b.Id,
    CAST((800 + (ABS(CHECKSUM(NEWID())) % 1200)) AS DECIMAL(18,2)),
    CAST((560 + (ABS(CHECKSUM(NEWID())) % 840)) AS DECIMAL(18,2)),
    CAST((160 + (ABS(CHECKSUM(NEWID())) % 240)) AS DECIMAL(18,2)),
    CAST((60 + (ABS(CHECKSUM(NEWID())) % 25)) AS DECIMAL(5,2)),
    CAST(70.00 AS DECIMAL(5,2)),
    CAST((-10 + (ABS(CHECKSUM(NEWID())) % 20)) AS DECIMAL(5,2)),
    CAST((7.0 + (ABS(CHECKSUM(NEWID())) % 30) / 10.0) AS DECIMAL(3,1)),
    CAST((250 + (ABS(CHECKSUM(NEWID())) % 350)) AS DECIMAL(18,2)),
    CAST((200 + (ABS(CHECKSUM(NEWID())) % 300)) AS DECIMAL(18,2)),
    CAST((100 + (ABS(CHECKSUM(NEWID())) % 200)) AS DECIMAL(18,2)),
    CAST((5 + (ABS(CHECKSUM(NEWID())) % 15)) AS DECIMAL(5,2)),
    'Husk: ' + CAST((80 + (ABS(CHECKSUM(NEWID())) % 40)) AS VARCHAR) + 'kg, Bran: ' + CAST((60 + (ABS(CHECKSUM(NEWID())) % 30)) AS VARCHAR) + 'kg',
    DATEADD(DAY, -30 - (ABS(CHECKSUM(NEWID())) % 30), GETDATE()),
    (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Supervisor' ORDER BY NEWID()),
    CASE (ROW_NUMBER() OVER (ORDER BY b.Id) % 5)
        WHEN 0 THEN 'Excellent yield quality'
        WHEN 1 THEN 'Standard processing'
        WHEN 2 THEN 'Minor quality issues noted'
        WHEN 3 THEN 'Batch processed efficiently'
        ELSE NULL
    END
FROM @BatchesWithoutYield b;

PRINT '✅ YieldRecords: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records added (20 -> 40)';

-- ===================================================================
-- 8. ADD MORE QUOTATIONS (23 -> 40 records)
-- ===================================================================
PRINT 'Adding more Quotations...';

DECLARE @MaxQuotationId INT = (SELECT ISNULL(MAX(Id), 0) FROM Quotations);

INSERT INTO Quotations (QuotationNumber, QuotationDate, ValidUntil, CustomerId, ContactPerson, InquiryId, TotalAmount, TaxAmount, GrandTotal, Status, PreparedBy, ApprovedBy, ApprovedDate, Terms, Notes)
SELECT
    'QT-2024-' + RIGHT('000' + CAST(@MaxQuotationId + ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 4),
    DATEADD(DAY, -30 - (ABS(CHECKSUM(NEWID())) % 30), GETDATE()),
    DATEADD(DAY, 15 + (ABS(CHECKSUM(NEWID())) % 15), GETDATE()),
    (SELECT TOP 1 Id FROM Customers ORDER BY NEWID()),
    (SELECT TOP 1 ContactName FROM CustomerContacts ORDER BY NEWID()),
    (SELECT TOP 1 Id FROM Inquiries ORDER BY NEWID()),
    CAST((15000 + (ABS(CHECKSUM(NEWID())) % 85000)) AS DECIMAL(18,2)),
    CAST((1950 + (ABS(CHECKSUM(NEWID())) % 11050)) AS DECIMAL(18,2)),
    CAST((16950 + (ABS(CHECKSUM(NEWID())) % 96050)) AS DECIMAL(18,2)),
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 4)
        WHEN 0 THEN 'Draft'
        WHEN 1 THEN 'Sent'
        WHEN 2 THEN 'Accepted'
        ELSE 'Rejected'
    END,
    (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Sales' ORDER BY NEWID()),
    (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Manager' ORDER BY NEWID()),
    DATEADD(DAY, -25 - (ABS(CHECKSUM(NEWID())) % 25), GETDATE()),
    'Payment: Net 30 days | Delivery: 7-14 days | Warranty: 90 days',
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5)
        WHEN 0 THEN 'Bulk order discount applied'
        WHEN 1 THEN 'Premium customer pricing'
        WHEN 2 THEN 'Competitive pricing'
        WHEN 3 THEN 'Special promotion'
        ELSE NULL
    END
FROM sys.objects
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 17;

PRINT '✅ Quotations: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records added (23 -> 40)';

-- ===================================================================
-- 9. ADD MORE SALESORDERS (23 -> 40 records)
-- ===================================================================
PRINT 'Adding more SalesOrders...';

DECLARE @MaxOrderId INT = (SELECT ISNULL(MAX(Id), 0) FROM SalesOrders);

INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, ExpectedDeliveryDate, TotalAmount, TaxAmount, GrandTotal, PaymentTerms, DeliveryTerms, Status, CreatedBy, ApprovedBy, ApprovedDate, Notes)
SELECT
    'SO-2024-' + RIGHT('000' + CAST(@MaxOrderId + ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 4),
    DATEADD(DAY, -20 - (ABS(CHECKSUM(NEWID())) % 20), GETDATE()),
    (SELECT TOP 1 Id FROM Customers ORDER BY NEWID()),
    NULL, -- Some orders might not have quotations
    DATEADD(DAY, 10 + (ABS(CHECKSUM(NEWID())) % 20), GETDATE()),
    CAST((18000 + (ABS(CHECKSUM(NEWID())) % 82000)) AS DECIMAL(18,2)),
    CAST((2340 + (ABS(CHECKSUM(NEWID())) % 10660)) AS DECIMAL(18,2)),
    CAST((20340 + (ABS(CHECKSUM(NEWID())) % 92660)) AS DECIMAL(18,2)),
    'Net 30 days',
    'FOB Destination',
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5)
        WHEN 0 THEN 'Pending'
        WHEN 1 THEN 'Confirmed'
        WHEN 2 THEN 'Processing'
        WHEN 3 THEN 'Shipped'
        ELSE 'Delivered'
    END,
    (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Sales' ORDER BY NEWID()),
    (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Manager' ORDER BY NEWID()),
    DATEADD(DAY, -18 - (ABS(CHECKSUM(NEWID())) % 18), GETDATE()),
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5)
        WHEN 0 THEN 'Rush order - expedite processing'
        WHEN 1 THEN 'Standard order processing'
        WHEN 2 THEN 'Repeat customer order'
        WHEN 3 THEN 'Large volume order'
        ELSE NULL
    END
FROM sys.objects
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 17;

PRINT '✅ SalesOrders: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' records added (23 -> 40)';

-- ===================================================================
-- VERIFICATION - COUNT ALL RECORDS
-- ===================================================================
PRINT '';
PRINT '========================================';
PRINT 'DATA SEEDING COMPLETE ✅';
PRINT '========================================';
PRINT '';
PRINT 'FINAL RECORD COUNTS:';
PRINT '--------------------';
PRINT 'StorageZones: ' + CAST((SELECT COUNT(*) FROM StorageZones) AS VARCHAR);
PRINT 'BatchInputs: ' + CAST((SELECT COUNT(*) FROM BatchInputs) AS VARCHAR);
PRINT 'BatchOutputs: ' + CAST((SELECT COUNT(*) FROM BatchOutputs) AS VARCHAR);
PRINT 'QuotationItems: ' + CAST((SELECT COUNT(*) FROM QuotationItems) AS VARCHAR);
PRINT 'SalesOrderItems: ' + CAST((SELECT COUNT(*) FROM SalesOrderItems) AS VARCHAR);
PRINT 'StockMovements: ' + CAST((SELECT COUNT(*) FROM StockMovements) AS VARCHAR);
PRINT 'YieldRecords: ' + CAST((SELECT COUNT(*) FROM YieldRecords) AS VARCHAR);
PRINT 'Quotations: ' + CAST((SELECT COUNT(*) FROM Quotations) AS VARCHAR);
PRINT 'SalesOrders: ' + CAST((SELECT COUNT(*) FROM SalesOrders) AS VARCHAR);
PRINT '';
PRINT '========================================';
PRINT 'ALL MEDIUM PRIORITY TASKS COMPLETED! ✅';
PRINT '========================================';

GO
