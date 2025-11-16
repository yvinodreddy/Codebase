-- =============================================
-- RMMS Database - Seed Missing Data Script
-- Populates empty tables with realistic test data
-- =============================================

USE RMMS_Production;
GO

PRINT 'Starting data seeding for empty tables...';
GO

-- =============================================
-- 1. STORAGE ZONES (Empty - 0 records)
-- =============================================
PRINT 'Seeding StorageZones...';
GO

-- Get warehouse IDs
DECLARE @Warehouse1 INT = (SELECT TOP 1 Id FROM Warehouses WHERE IsActive = 1 ORDER BY Id);
DECLARE @Warehouse2 INT = (SELECT TOP 1 Id FROM Warehouses WHERE IsActive = 1 AND Id > @Warehouse1 ORDER BY Id);

IF @Warehouse1 IS NOT NULL
BEGIN
    INSERT INTO StorageZones (WarehouseId, ZoneName, ZoneCode, ZoneType, Capacity, CurrentUtilization, TemperatureControlled, HumidityControlled, IsActive, CreatedDate, CreatedBy)
    VALUES
    -- Warehouse 1 Zones
    (@Warehouse1, 'Raw Material Zone A', 'WH1-RM-A', 'Raw Material', 5000.00, 3200.50, 0, 0, 1, GETDATE(), 'DataSeeder'),
    (@Warehouse1, 'Raw Material Zone B', 'WH1-RM-B', 'Raw Material', 5000.00, 2800.75, 0, 0, 1, GETDATE(), 'DataSeeder'),
    (@Warehouse1, 'Finished Goods Zone A', 'WH1-FG-A', 'Finished Goods', 8000.00, 5600.25, 0, 1, 1, GETDATE(), 'DataSeeder'),
    (@Warehouse1, 'Finished Goods Zone B', 'WH1-FG-B', 'Finished Goods', 8000.00, 4200.00, 0, 1, 1, GETDATE(), 'DataSeeder'),
    (@Warehouse1, 'By-Products Zone', 'WH1-BP-A', 'By-Products', 3000.00, 1500.50, 0, 0, 1, GETDATE(), 'DataSeeder'),
    (@Warehouse1, 'Quality Check Zone', 'WH1-QC-A', 'QC/Quarantine', 1000.00, 250.00, 1, 1, 1, GETDATE(), 'DataSeeder');

    IF @Warehouse2 IS NOT NULL
    BEGIN
        INSERT INTO StorageZones (WarehouseId, ZoneName, ZoneCode, ZoneType, Capacity, CurrentUtilization, TemperatureControlled, HumidityControlled, IsActive, CreatedDate, CreatedBy)
        VALUES
        -- Warehouse 2 Zones
        (@Warehouse2, 'Raw Material Zone A', 'WH2-RM-A', 'Raw Material', 6000.00, 4100.00, 0, 0, 1, GETDATE(), 'DataSeeder'),
        (@Warehouse2, 'Finished Goods Zone A', 'WH2-FG-A', 'Finished Goods', 10000.00, 7200.00, 0, 1, 1, GETDATE(), 'DataSeeder'),
        (@Warehouse2, 'By-Products Zone', 'WH2-BP-A', 'By-Products', 2000.00, 800.00, 0, 0, 1, GETDATE(), 'DataSeeder'),
        (@Warehouse2, 'Dispatch Zone', 'WH2-DP-A', 'Dispatch', 2000.00, 500.00, 0, 0, 1, GETDATE(), 'DataSeeder');
    END

    PRINT 'StorageZones seeded successfully!';
END
ELSE
BEGIN
    PRINT 'WARNING: No warehouses found. Skipping StorageZones seeding.';
END
GO

-- =============================================
-- 2. QUOTATION ITEMS (Empty - 0 records)
-- =============================================
PRINT 'Seeding QuotationItems...';
GO

-- Get sample data
DECLARE @SampleQuotations TABLE (QuotationId INT);
INSERT INTO @SampleQuotations (QuotationId)
SELECT TOP 20 Id FROM Quotations WHERE IsActive = 1 ORDER BY NEWID();

DECLARE @SampleProducts TABLE (ProductId INT, ProductName NVARCHAR(100), UnitPrice DECIMAL(18,2));
INSERT INTO @SampleProducts (ProductId, ProductName, UnitPrice)
SELECT TOP 10 Id, ProductName, SellingPrice FROM Products WHERE IsActive = 1 ORDER BY NEWID();

-- Create quotation items
INSERT INTO QuotationItems (QuotationId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountAmount, TaxAmount, TotalAmount, Remarks)
SELECT
    q.QuotationId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 50 + 10) AS DECIMAL(18,3)) AS Quantity, -- 10-60 quintals
    'Quintals' AS UnitOfMeasure,
    p.UnitPrice,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 50 + 10) * 0.05) AS DECIMAL(18,2)) AS DiscountAmount, -- 5% discount
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 50 + 10) * 0.05) AS DECIMAL(18,2)) AS TaxAmount, -- 5% GST
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 50 + 10) * 1.05 - p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 50 + 10) * 0.05) AS DECIMAL(18,2)) AS TotalAmount,
    'Standard quotation item' AS Remarks
FROM @SampleQuotations q
CROSS APPLY (SELECT TOP 1 * FROM @SampleProducts ORDER BY NEWID()) p;

-- Add more items to some quotations (2-3 items per quotation)
INSERT INTO QuotationItems (QuotationId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountAmount, TaxAmount, TotalAmount, Remarks)
SELECT TOP 15
    q.QuotationId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 30 + 5) AS DECIMAL(18,3)) AS Quantity,
    'Quintals' AS UnitOfMeasure,
    p.UnitPrice,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 30 + 5) * 0.03) AS DECIMAL(18,2)) AS DiscountAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 30 + 5) * 0.05) AS DECIMAL(18,2)) AS TaxAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 30 + 5) * 1.02) AS DECIMAL(18,2)) AS TotalAmount,
    'Additional quotation item' AS Remarks
FROM @SampleQuotations q
CROSS APPLY (SELECT TOP 1 * FROM @SampleProducts ORDER BY NEWID()) p
ORDER BY NEWID();

PRINT 'QuotationItems seeded successfully!';
GO

-- =============================================
-- 3. SALES ORDER ITEMS (Empty - 0 records)
-- =============================================
PRINT 'Seeding SalesOrderItems...';
GO

-- Get sample data
DECLARE @SampleOrders TABLE (OrderId INT);
INSERT INTO @SampleOrders (OrderId)
SELECT TOP 20 Id FROM SalesOrders WHERE IsActive = 1 ORDER BY NEWID();

DECLARE @SampleProducts2 TABLE (ProductId INT, ProductName NVARCHAR(100), UnitPrice DECIMAL(18,2));
INSERT INTO @SampleProducts2 (ProductId, ProductName, UnitPrice)
SELECT TOP 10 Id, ProductName, SellingPrice FROM Products WHERE IsActive = 1 ORDER BY NEWID();

DECLARE @SampleWarehouses TABLE (WarehouseId INT);
INSERT INTO @SampleWarehouses (WarehouseId)
SELECT TOP 3 Id FROM Warehouses WHERE IsActive = 1;

-- Create sales order items
INSERT INTO SalesOrderItems (SalesOrderId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountAmount, TaxAmount, TotalAmount, AllocatedQuantity, DispatchedQuantity, WarehouseId, Remarks)
SELECT
    o.OrderId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 80 + 20) AS DECIMAL(18,3)) AS Quantity, -- 20-100 quintals
    'Quintals' AS UnitOfMeasure,
    p.UnitPrice,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 80 + 20) * 0.05) AS DECIMAL(18,2)) AS DiscountAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 80 + 20) * 0.05) AS DECIMAL(18,2)) AS TaxAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 80 + 20) * 1.00) AS DECIMAL(18,2)) AS TotalAmount,
    NULL AS AllocatedQuantity, -- Not yet allocated
    0 AS DispatchedQuantity,
    (SELECT TOP 1 WarehouseId FROM @SampleWarehouses ORDER BY NEWID()) AS WarehouseId,
    'Order confirmed' AS Remarks
FROM @SampleOrders o
CROSS APPLY (SELECT TOP 1 * FROM @SampleProducts2 ORDER BY NEWID()) p;

-- Add more items to some orders (2-3 items per order)
INSERT INTO SalesOrderItems (SalesOrderId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountAmount, TaxAmount, TotalAmount, AllocatedQuantity, DispatchedQuantity, WarehouseId, Remarks)
SELECT TOP 20
    o.OrderId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 40 + 10) AS DECIMAL(18,3)) AS Quantity,
    'Quintals' AS UnitOfMeasure,
    p.UnitPrice,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 40 + 10) * 0.03) AS DECIMAL(18,2)) AS DiscountAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 40 + 10) * 0.05) AS DECIMAL(18,2)) AS TaxAmount,
    CAST((p.UnitPrice * (RAND(CHECKSUM(NEWID())) * 40 + 10) * 0.97) AS DECIMAL(18,2)) AS TotalAmount,
    NULL AS AllocatedQuantity,
    0 AS DispatchedQuantity,
    (SELECT TOP 1 WarehouseId FROM @SampleWarehouses ORDER BY NEWID()) AS WarehouseId,
    'Bulk order item' AS Remarks
FROM @SampleOrders o
CROSS APPLY (SELECT TOP 1 * FROM @SampleProducts2 ORDER BY NEWID()) p
ORDER BY NEWID();

PRINT 'SalesOrderItems seeded successfully!';
GO

-- =============================================
-- 4. BATCH INPUTS (Empty - 0 records)
-- =============================================
PRINT 'Seeding BatchInputs...';
GO

-- Get sample production batches
DECLARE @SampleBatches TABLE (BatchId INT, BatchNumber NVARCHAR(50));
INSERT INTO @SampleBatches (BatchId, BatchNumber)
SELECT TOP 30 Id, BatchNumber FROM ProductionBatches WHERE IsActive = 1 ORDER BY NEWID();

DECLARE @PaddyProducts TABLE (ProductId INT, ProductName NVARCHAR(100));
INSERT INTO @PaddyProducts (ProductId, ProductName)
SELECT TOP 5 Id, ProductName FROM Products WHERE ProductName LIKE '%Paddy%' AND IsActive = 1;

-- Create batch inputs
INSERT INTO BatchInputs (BatchId, ProductId, ProductName, Quantity, UnitOfMeasure, UnitCost, TotalCost, SourceType, SourceReferenceId, LotNumber, QualityGrade, MoistureContent, ForeignMatter, BrokenGrains, Remarks, CreatedDate, CreatedBy, IsActive)
SELECT
    b.BatchId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 500 + 100) AS DECIMAL(18,3)) AS Quantity, -- 100-600 kg
    'kg' AS UnitOfMeasure,
    CAST((RAND(CHECKSUM(NEWID())) * 20 + 25) AS DECIMAL(18,2)) AS UnitCost, -- Rs 25-45 per kg
    CAST((RAND(CHECKSUM(NEWID())) * 500 + 100) * (RAND(CHECKSUM(NEWID())) * 20 + 25) AS DECIMAL(18,2)) AS TotalCost,
    'Purchase' AS SourceType,
    NULL AS SourceReferenceId,
    'LOT-' + CAST(CAST((RAND(CHECKSUM(NEWID())) * 9000 + 1000) AS INT) AS NVARCHAR(10)) AS LotNumber,
    CASE CAST((RAND(CHECKSUM(NEWID())) * 3) AS INT)
        WHEN 0 THEN 'Grade A'
        WHEN 1 THEN 'Grade B'
        ELSE 'Grade C'
    END AS QualityGrade,
    CAST((RAND(CHECKSUM(NEWID())) * 5 + 12) AS DECIMAL(5,2)) AS MoistureContent, -- 12-17%
    CAST((RAND(CHECKSUM(NEWID())) * 2) AS DECIMAL(5,2)) AS ForeignMatter, -- 0-2%
    CAST((RAND(CHECKSUM(NEWID())) * 3 + 1) AS DECIMAL(5,2)) AS BrokenGrains, -- 1-4%
    'Raw material input for production batch' AS Remarks,
    GETDATE() AS CreatedDate,
    'DataSeeder' AS CreatedBy,
    1 AS IsActive
FROM @SampleBatches b
CROSS APPLY (SELECT TOP 1 * FROM @PaddyProducts ORDER BY NEWID()) p;

PRINT 'BatchInputs seeded successfully!';
GO

-- =============================================
-- 5. BATCH OUTPUTS (Empty - 0 records)
-- =============================================
PRINT 'Seeding BatchOutputs...';
GO

-- Get sample production batches
DECLARE @SampleBatches2 TABLE (BatchId INT, BatchNumber NVARCHAR(50));
INSERT INTO @SampleBatches2 (BatchId, BatchNumber)
SELECT TOP 30 Id, BatchNumber FROM ProductionBatches WHERE IsActive = 1 AND Status = 'Completed' ORDER BY NEWID();

DECLARE @RiceProducts TABLE (ProductId INT, ProductName NVARCHAR(100));
INSERT INTO @RiceProducts (ProductId, ProductName)
SELECT TOP 8 Id, ProductName FROM Products WHERE ProductName LIKE '%Rice%' AND ProductName NOT LIKE '%Paddy%' AND IsActive = 1;

DECLARE @ByProducts TABLE (ProductId INT, ProductName NVARCHAR(100));
INSERT INTO @ByProducts (ProductId, ProductName)
SELECT TOP 3 Id, ProductName FROM Products WHERE (ProductName LIKE '%Husk%' OR ProductName LIKE '%Bran%') AND IsActive = 1;

-- Create batch outputs for finished rice
INSERT INTO BatchOutputs (BatchId, ProductId, ProductName, Quantity, UnitOfMeasure, UnitCost, TotalValue, OutputType, QualityGrade, MoistureContent, BrokenPercentage, YieldPercentage, StorageLocation, Remarks, CreatedDate, CreatedBy, IsActive)
SELECT
    b.BatchId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 350 + 150) AS DECIMAL(18,3)) AS Quantity, -- 150-500 kg rice output
    'kg' AS UnitOfMeasure,
    CAST((RAND(CHECKSUM(NEWID())) * 15 + 35) AS DECIMAL(18,2)) AS UnitCost, -- Rs 35-50 per kg
    CAST((RAND(CHECKSUM(NEWID())) * 350 + 150) * (RAND(CHECKSUM(NEWID())) * 15 + 35) AS DECIMAL(18,2)) AS TotalValue,
    'Finished Goods' AS OutputType,
    CASE CAST((RAND(CHECKSUM(NEWID())) * 3) AS INT)
        WHEN 0 THEN 'Premium'
        WHEN 1 THEN 'Grade A'
        ELSE 'Standard'
    END AS QualityGrade,
    CAST((RAND(CHECKSUM(NEWID())) * 2 + 12) AS DECIMAL(5,2)) AS MoistureContent, -- 12-14%
    CAST((RAND(CHECKSUM(NEWID())) * 3 + 1) AS DECIMAL(5,2)) AS BrokenPercentage, -- 1-4%
    CAST((RAND(CHECKSUM(NEWID())) * 10 + 65) AS DECIMAL(5,2)) AS YieldPercentage, -- 65-75%
    'Main Warehouse - FG Zone' AS StorageLocation,
    'Primary rice output from milling' AS Remarks,
    GETDATE() AS CreatedDate,
    'DataSeeder' AS CreatedBy,
    1 AS IsActive
FROM @SampleBatches2 b
CROSS APPLY (SELECT TOP 1 * FROM @RiceProducts ORDER BY NEWID()) p;

-- Create batch outputs for by-products
INSERT INTO BatchOutputs (BatchId, ProductId, ProductName, Quantity, UnitOfMeasure, UnitCost, TotalValue, OutputType, QualityGrade, MoistureContent, BrokenPercentage, YieldPercentage, StorageLocation, Remarks, CreatedDate, CreatedBy, IsActive)
SELECT
    b.BatchId,
    p.ProductId,
    p.ProductName,
    CAST((RAND(CHECKSUM(NEWID())) * 80 + 30) AS DECIMAL(18,3)) AS Quantity, -- 30-110 kg by-product
    'kg' AS UnitOfMeasure,
    CAST((RAND(CHECKSUM(NEWID())) * 5 + 5) AS DECIMAL(18,2)) AS UnitCost, -- Rs 5-10 per kg
    CAST((RAND(CHECKSUM(NEWID())) * 80 + 30) * (RAND(CHECKSUM(NEWID())) * 5 + 5) AS DECIMAL(18,2)) AS TotalValue,
    'By-Product' AS OutputType,
    'Standard' AS QualityGrade,
    CAST((RAND(CHECKSUM(NEWID())) * 5 + 10) AS DECIMAL(5,2)) AS MoistureContent,
    NULL AS BrokenPercentage,
    CAST((RAND(CHECKSUM(NEWID())) * 5 + 15) AS DECIMAL(5,2)) AS YieldPercentage, -- 15-20%
    'By-Product Storage' AS StorageLocation,
    'By-product from rice milling process' AS Remarks,
    GETDATE() AS CreatedDate,
    'DataSeeder' AS CreatedBy,
    1 AS IsActive
FROM @SampleBatches2 b
CROSS APPLY (SELECT TOP 1 * FROM @ByProducts ORDER BY NEWID()) p
WHERE CAST((RAND(CHECKSUM(NEWID())) * 2) AS INT) = 1; -- Only 50% of batches

PRINT 'BatchOutputs seeded successfully!';
GO

-- =============================================
-- VERIFICATION SUMMARY
-- =============================================
PRINT '';
PRINT '==============================================';
PRINT 'DATA SEEDING COMPLETED SUCCESSFULLY!';
PRINT '==============================================';
PRINT '';
PRINT 'Record Counts:';
SELECT 'StorageZones' AS TableName, COUNT(*) AS RecordCount FROM StorageZones
UNION ALL
SELECT 'QuotationItems', COUNT(*) FROM QuotationItems
UNION ALL
SELECT 'SalesOrderItems', COUNT(*) FROM SalesOrderItems
UNION ALL
SELECT 'BatchInputs', COUNT(*) FROM BatchInputs
UNION ALL
SELECT 'BatchOutputs', COUNT(*) FROM BatchOutputs
ORDER BY TableName;
GO

PRINT '';
PRINT 'Data seeding script completed successfully!';
GO
