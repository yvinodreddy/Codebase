-- Production Data Seeding Script
-- Seeds sample production batches with yield data for analytics

PRINT '========================================'
PRINT 'RMMS Production Data Seeding Script'
PRINT '========================================'
PRINT ''

-- Step 1: Create Products if they don't exist
PRINT 'Step 1: Creating Products...'

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'PADDY-BR11')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsRawMaterial, IsActive, CreatedDate)
    VALUES ('PADDY-BR11', 'Basmati Rice BR-11', 'Paddy', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added paddy: Basmati Rice BR-11'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'PADDY-SONA')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsRawMaterial, IsActive, CreatedDate)
    VALUES ('PADDY-SONA', 'Sona Masuri Paddy', 'Paddy', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added paddy: Sona Masuri Paddy'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'PADDY-IR64')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsRawMaterial, IsActive, CreatedDate)
    VALUES ('PADDY-IR64', 'IR-64 Paddy', 'Paddy', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added paddy: IR-64 Paddy'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'RICE-BR11')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsFinishedProduct, IsActive, CreatedDate)
    VALUES ('RICE-BR11', 'Basmati Rice BR-11', 'Rice', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added rice: Basmati Rice BR-11'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'RICE-SONA')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsFinishedProduct, IsActive, CreatedDate)
    VALUES ('RICE-SONA', 'Sona Masuri Rice', 'Rice', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added rice: Sona Masuri Rice'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'RICE-BROKEN')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsByProduct, IsActive, CreatedDate)
    VALUES ('RICE-BROKEN', 'Broken Rice', 'Rice', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added: Broken Rice'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'BRAN-001')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsByProduct, IsActive, CreatedDate)
    VALUES ('BRAN-001', 'Rice Bran', 'By-Product', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added: Rice Bran'
END

IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'HUSK-001')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductCategory, UnitOfMeasure, IsByProduct, IsActive, CreatedDate)
    VALUES ('HUSK-001', 'Rice Husk', 'By-Product', 'Quintals', 1, 1, GETDATE())
    PRINT '  + Added: Rice Husk'
END

PRINT '✓ Products created'
PRINT ''

-- Step 2: Create Machines
PRINT 'Step 2: Creating Machines...'

IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-01')
BEGIN
    INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
    VALUES ('MILL-01', 'Rice Huller Machine #1', 'Husker', 'Satake Corporation', 'SH-5000', 5.0, 'tons/hour', 'Operational', 'Production Floor A', DATEADD(YEAR, -3, GETDATE()), 1, GETDATE())
    PRINT '  + Added machine: Rice Huller Machine #1'
END

IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-02')
BEGIN
    INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
    VALUES ('MILL-02', 'Rice Polisher #2', 'Polisher', 'Buhler Group', 'BP-3000', 3.5, 'tons/hour', 'Operational', 'Production Floor A', DATEADD(YEAR, -2, GETDATE()), 1, GETDATE())
    PRINT '  + Added machine: Rice Polisher #2'
END

IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MILL-03')
BEGIN
    INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit, Status, Location, PurchaseDate, IsActive, CreatedDate)
    VALUES ('MILL-03', 'Rice Grader & Sorter #3', 'Grader', 'Fowler Westrup', 'GS-2500', 4.0, 'tons/hour', 'Operational', 'Production Floor B', DATEADD(YEAR, -1, GETDATE()), 1, GETDATE())
    PRINT '  + Added machine: Rice Grader & Sorter #3'
END

PRINT '✓ Machines created'
PRINT ''

-- Step 3: Create Warehouses
PRINT 'Step 3: Creating Warehouses...'

IF NOT EXISTS (SELECT 1 FROM Warehouses WHERE WarehouseCode = 'WH-MAIN')
BEGIN
    INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, TotalCapacity, UsedCapacity, AvailableCapacity, Status, IsActive, CreatedDate)
    VALUES ('WH-MAIN', 'Main Warehouse', 'Main Building', 5000, 0, 5000, 'Active', 1, GETDATE())
    PRINT '  + Added warehouse: Main Warehouse'
END

IF NOT EXISTS (SELECT 1 FROM Warehouses WHERE WarehouseCode = 'WH-PROD')
BEGIN
    INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, TotalCapacity, UsedCapacity, AvailableCapacity, Status, IsActive, CreatedDate)
    VALUES ('WH-PROD', 'Production Warehouse', 'Production Building', 2000, 0, 2000, 'Active', 1, GETDATE())
    PRINT '  + Added warehouse: Production Warehouse'
END

PRINT '✓ Warehouses created'
PRINT ''

-- Step 4: Create Production Orders, Batches, and Yield Records
PRINT 'Step 4: Creating Production Orders and Batches with Yield Data...'
PRINT 'This will create 30 batches over the last 60 days...'
PRINT ''

DECLARE @Counter INT = 1
DECLARE @BatchDate DATETIME
DECLARE @PaddyProductId INT
DECLARE @RiceProductId INT
DECLARE @BrokenRiceId INT
DECLARE @BranId INT
DECLARE @HuskId INT
DECLARE @MachineId INT
DECLARE @WarehouseMainId INT
DECLARE @WarehouseProdId INT
DECLARE @OrderId INT
DECLARE @BatchId INT
DECLARE @InputQuantity DECIMAL(18,3)
DECLARE @HeadRicePercent DECIMAL(5,2)
DECLARE @BrokenRicePercent DECIMAL(5,2)
DECLARE @BranPercent DECIMAL(5,2)
DECLARE @HuskPercent DECIMAL(5,2)
DECLARE @WastagePercent DECIMAL(5,2)
DECLARE @YieldGrade VARCHAR(20)
DECLARE @QualityScore DECIMAL(3,1)
DECLARE @ShiftType VARCHAR(20)
DECLARE @Variety VARCHAR(50)

-- Get IDs
SELECT @BrokenRiceId = Id FROM Products WHERE ProductCode = 'RICE-BROKEN'
SELECT @BranId = Id FROM Products WHERE ProductCode = 'BRAN-001'
SELECT @HuskId = Id FROM Products WHERE ProductCode = 'HUSK-001'
SELECT @WarehouseMainId = Id FROM Warehouses WHERE WarehouseCode = 'WH-MAIN'
SELECT @WarehouseProdId = Id FROM Warehouses WHERE WarehouseCode = 'WH-PROD'

WHILE @Counter <= 30
BEGIN
    -- Random variations for realistic data
    SET @BatchDate = DATEADD(DAY, -1 * (@Counter + FLOOR(RAND() * 30)), GETDATE())

    -- Rotate through products and machines
    SELECT @PaddyProductId = Id FROM Products WHERE ProductCode =
        CASE (@Counter % 3)
            WHEN 0 THEN 'PADDY-BR11'
            WHEN 1 THEN 'PADDY-SONA'
            ELSE 'PADDY-IR64'
        END

    SELECT @RiceProductId = Id FROM Products WHERE ProductCode =
        CASE (@Counter % 2)
            WHEN 0 THEN 'RICE-BR11'
            ELSE 'RICE-SONA'
        END

    SELECT @MachineId = Id FROM Machines WHERE MachineCode =
        CASE (@Counter % 3)
            WHEN 0 THEN 'MILL-01'
            WHEN 1 THEN 'MILL-02'
            ELSE 'MILL-03'
        END

    SET @ShiftType = CASE (@Counter % 3)
        WHEN 0 THEN 'Morning'
        WHEN 1 THEN 'Evening'
        ELSE 'Night'
    END

    SET @Variety = CASE (@Counter % 3)
        WHEN 0 THEN 'Basmati'
        WHEN 1 THEN 'Sona Masuri'
        ELSE 'IR-64'
    END

    SET @InputQuantity = 100 + (@Counter * 0.5) -- 100-115 quintals
    SET @HeadRicePercent = 60 + ((@Counter * 3) % 15) -- 60-75%
    SET @BrokenRicePercent = 5 + ((@Counter * 2) % 5) -- 5-10%
    SET @BranPercent = 7 + ((@Counter) % 3) -- 7-10%
    SET @HuskPercent = 19 + ((@Counter) % 4) -- 19-23%
    SET @WastagePercent = 0.8 + ((@Counter * 0.1) % 1.2) -- 0.8-2%
    SET @QualityScore = 7.0 + ((@Counter * 0.2) % 2.5) -- 7-9.5

    -- Determine yield grade
    IF @HeadRicePercent >= 68
        SET @YieldGrade = 'Excellent'
    ELSE IF @HeadRicePercent >= 62
        SET @YieldGrade = 'Good'
    ELSE IF @HeadRicePercent >= 55
        SET @YieldGrade = 'Average'
    ELSE
        SET @YieldGrade = 'Poor'

    -- Create Production Order
    INSERT INTO ProductionOrders (OrderNumber, OrderDate, ScheduledDate, SourceType, PaddyProductId, PaddyVariety, PaddyQuantity, PaddyUOM,
        TargetRiceProductId, TargetRiceGrade, ExpectedYieldPercent, Priority, AssignedMachineId, Status,
        ActualStartDate, ActualCompletionDate, ActualQuantityProduced, ActualYieldPercent,
        IsActive, CreatedDate, CreatedBy)
    VALUES (
        'PO-' + CAST(YEAR(GETDATE()) AS VARCHAR) + '-' + RIGHT('000' + CAST(@Counter AS VARCHAR), 4),
        DATEADD(DAY, -2, @BatchDate),
        @BatchDate,
        'Inventory',
        @PaddyProductId,
        @Variety,
        @InputQuantity,
        'Quintals',
        @RiceProductId,
        'Grade A',
        65.00,
        'Normal',
        @MachineId,
        'Completed',
        @BatchDate,
        DATEADD(HOUR, 8, @BatchDate),
        @InputQuantity * (@HeadRicePercent + @BrokenRicePercent) / 100,
        @HeadRicePercent + @BrokenRicePercent,
        1,
        DATEADD(DAY, -2, @BatchDate),
        'System'
    )

    SET @OrderId = SCOPE_IDENTITY()

    -- Create Production Batch
    INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, ShiftType,
        StartTime, EndTime, Status, CompletionPercent, QualityScore,
        IsActive, CreatedDate, CreatedBy)
    VALUES (
        'BATCH-' + CAST(YEAR(GETDATE()) AS VARCHAR) + '-' + RIGHT('000' + CAST(@Counter AS VARCHAR), 4),
        @OrderId,
        @BatchDate,
        @ShiftType,
        DATEADD(HOUR, CASE @ShiftType WHEN 'Morning' THEN 7 WHEN 'Evening' THEN 15 ELSE 22 END, @BatchDate),
        DATEADD(HOUR, CASE @ShiftType WHEN 'Morning' THEN 13 WHEN 'Evening' THEN 21 ELSE 6 END, DATEADD(DAY, CASE @ShiftType WHEN 'Night' THEN 1 ELSE 0 END, @BatchDate)),
        'Completed',
        100,
        @QualityScore,
        1,
        @BatchDate,
        'System'
    )

    SET @BatchId = SCOPE_IDENTITY()

    -- Create Batch Input
    INSERT INTO BatchInputs (BatchId, InputType, ProductId, Quantity, UOM, WarehouseId, MoistureContent, Grade, UnitCost, CreatedDate, CreatedBy)
    VALUES (@BatchId, 'Paddy', @PaddyProductId, @InputQuantity, 'Quintals', @WarehouseMainId, 14.0, 'Grade A', 2200, @BatchDate, 'System')

    -- Create Batch Outputs
    INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, QualityScore, UnitCost, CreatedDate, CreatedBy)
    VALUES (@BatchId, 'Rice', @RiceProductId, 'Grade A', @InputQuantity * @HeadRicePercent / 100, 'Quintals', @WarehouseProdId, @QualityScore, 4000, DATEADD(HOUR, 8, @BatchDate), 'System')

    INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, QualityScore, UnitCost, CreatedDate, CreatedBy)
    VALUES (@BatchId, 'Broken Rice', @BrokenRiceId, 'Standard', @InputQuantity * @BrokenRicePercent / 100, 'Quintals', @WarehouseProdId, @QualityScore, 1800, DATEADD(HOUR, 8, @BatchDate), 'System')

    INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, UnitCost, CreatedDate, CreatedBy)
    VALUES (@BatchId, 'Bran', @BranId, NULL, @InputQuantity * @BranPercent / 100, 'Quintals', @WarehouseProdId, 1000, DATEADD(HOUR, 8, @BatchDate), 'System')

    INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, UnitCost, CreatedDate, CreatedBy)
    VALUES (@BatchId, 'Husk', @HuskId, NULL, @InputQuantity * @HuskPercent / 100, 'Quintals', @WarehouseProdId, 400, DATEADD(HOUR, 8, @BatchDate), 'System')

    -- Create Yield Record
    INSERT INTO YieldRecords (BatchId, PaddyVariety, InputPaddyQuantity,
        OutputHeadRice, OutputBrokenRice, OutputBran, OutputHusk, OutputWastage,
        HeadRicePercent, BrokenRicePercent, BranPercent, HuskPercent, WastagePercent, TotalYieldPercent,
        StandardHeadRicePercent, StandardTotalYieldPercent, YieldGrade, QualityScore,
        MillingRecovery, HeadRiceToBrokenRatio, IsVerified,
        CalculatedDate, CalculatedBy, VerifiedBy, VerifiedDate)
    VALUES (
        @BatchId,
        @Variety,
        @InputQuantity,
        @InputQuantity * @HeadRicePercent / 100,
        @InputQuantity * @BrokenRicePercent / 100,
        @InputQuantity * @BranPercent / 100,
        @InputQuantity * @HuskPercent / 100,
        @InputQuantity * @WastagePercent / 100,
        @HeadRicePercent,
        @BrokenRicePercent,
        @BranPercent,
        @HuskPercent,
        @WastagePercent,
        @HeadRicePercent + @BrokenRicePercent + @BranPercent + @HuskPercent + @WastagePercent,
        65.00,
        98.00,
        @YieldGrade,
        @QualityScore,
        @HeadRicePercent + @BrokenRicePercent,
        (@InputQuantity * @HeadRicePercent / 100) / (@InputQuantity * @BrokenRicePercent / 100),
        1,
        DATEADD(HOUR, 8, @BatchDate),
        'System',
        'QC Team',
        DATEADD(HOUR, 9, @BatchDate)
    )

    IF @Counter % 5 = 0
        PRINT '  Progress: ' + CAST(@Counter AS VARCHAR) + '/30 batches created...'

    SET @Counter = @Counter + 1
END

PRINT '✓ Created 30 production orders'
PRINT '✓ Created 30 production batches with complete yield data'
PRINT ''

-- Summary Statistics
PRINT '========================================'
PRINT 'DATA SEEDING COMPLETED SUCCESSFULLY!'
PRINT '========================================'
PRINT ''
PRINT 'Summary Statistics:'

SELECT
    'Total Batches: ' + CAST(COUNT(*) AS VARCHAR) AS [Stat],
    'Average Yield: ' + CAST(CAST(AVG(HeadRicePercent) AS DECIMAL(5,2)) AS VARCHAR) + '%' AS [Value]
FROM YieldRecords

SELECT
    'Yield Range: ' + CAST(CAST(MIN(HeadRicePercent) AS DECIMAL(5,2)) AS VARCHAR) + '% - ' +
    CAST(CAST(MAX(HeadRicePercent) AS DECIMAL(5,2)) AS VARCHAR) + '%' AS [Range]
FROM YieldRecords

PRINT ''
PRINT 'Yield Grade Distribution:'
SELECT YieldGrade AS [Grade], COUNT(*) AS [Count]
FROM YieldRecords
GROUP BY YieldGrade
ORDER BY COUNT(*) DESC

PRINT ''
PRINT 'Next Steps:'
PRINT '  1. Start the application: dotnet run'
PRINT '  2. Navigate to: http://localhost:5090/YieldAnalysis'
PRINT '  3. Explore the analytics dashboards'
PRINT ''
PRINT 'All analytics pages should now display data!'
PRINT '========================================'
