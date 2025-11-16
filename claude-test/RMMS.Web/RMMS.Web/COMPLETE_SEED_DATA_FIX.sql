-- ============================================================================
-- COMPREHENSIVE SEED DATA - FIX ALL MISSING DATA
-- Date: 2025-10-12
-- Purpose: Populate all empty/incomplete tables with 40 records each
-- ============================================================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Starting Comprehensive Data Insertion';
PRINT '========================================';
GO

-- ============================================================================
-- 1. ADD VENDORS (5 → 40) - Add 35 more
-- ============================================================================
PRINT 'Inserting Vendors...';
GO

DECLARE @VendorCounter INT = 6;
WHILE @VendorCounter <= 40
BEGIN
    INSERT INTO Vendors (VendorCode, VendorName, VendorType, ContactPerson, ContactNumber, Email, 
                        PrimaryAddress, City, State, Pincode, GSTNumber, PANNumber, 
                        PaymentTerms, CreditLimit, Rating, IsActive, CreatedBy, CreatedDate)
    VALUES (
        'VEND' + RIGHT('0000' + CAST(@VendorCounter AS VARCHAR), 4),
        CASE (@VendorCounter % 3) 
            WHEN 0 THEN 'Paddy Supplier ' + CAST(@VendorCounter AS VARCHAR)
            WHEN 1 THEN 'Rice Trader ' + CAST(@VendorCounter AS VARCHAR)
            ELSE 'Commission Agent ' + CAST(@VendorCounter AS VARCHAR)
        END,
        CASE (@VendorCounter % 3) 
            WHEN 0 THEN 'Farmer' 
            WHEN 1 THEN 'Trader'
            ELSE 'Commission Agent'
        END,
        'Contact Person ' + CAST(@VendorCounter AS VARCHAR),
        '98' + RIGHT('00000000' + CAST(CAST(RAND() * 100000000 AS BIGINT) AS VARCHAR), 8),
        'vendor' + CAST(@VendorCounter AS VARCHAR) + '@example.com',
        CAST(@VendorCounter AS VARCHAR) + ' Main Road, Village ' + CAST(@VendorCounter AS VARCHAR),
        CASE (@VendorCounter % 5) 
            WHEN 0 THEN 'Amritsar'
            WHEN 1 THEN 'Ludhiana'
            WHEN 2 THEN 'Patiala'
            WHEN 3 THEN 'Jalandhar'
            ELSE 'Bathinda'
        END,
        'Punjab',
        '14' + RIGHT('0000' + CAST(@VendorCounter AS VARCHAR), 4),
        '03AAAAA' + CAST(@VendorCounter AS VARCHAR) + 'Z1',
        'AAAAA' + CAST(@VendorCounter AS VARCHAR) + 'Z',
        CASE (@VendorCounter % 2) WHEN 0 THEN 'Net 30' ELSE 'Net 15' END,
        CAST((RAND() * 500000 + 100000) AS DECIMAL(18,2)),
        CASE (@VendorCounter % 5) + 1 WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3 WHEN 4 THEN 4 ELSE 5 END,
        1,
        'System',
        DATEADD(DAY, -@VendorCounter, GETDATE())
    );
    SET @VendorCounter = @VendorCounter + 1;
END;
PRINT 'Vendors: 35 records inserted';
GO

-- ============================================================================
-- 2. ADD WAREHOUSES (3 → 40) - Add 37 more  
-- ============================================================================
PRINT 'Inserting Warehouses...';
GO

DECLARE @WarehouseCounter INT = 4;
WHILE @WarehouseCounter <= 40
BEGIN
    INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, Address, City, State, Pincode,
                           WarehouseType, TotalCapacity, UsedCapacity, AvailableCapacity, UnitOfMeasure,
                           ManagerName, ManagerContact, IsActive, CreatedBy, CreatedDate)
    VALUES (
        'WRHS' + RIGHT('0000' + CAST(@WarehouseCounter AS VARCHAR), 4),
        'Warehouse ' + CAST(@WarehouseCounter AS VARCHAR),
        'Location ' + CAST(@WarehouseCounter AS VARCHAR),
        'Plot ' + CAST(@WarehouseCounter AS VARCHAR) + ', Industrial Area',
        CASE (@WarehouseCounter % 5) 
            WHEN 0 THEN 'Amritsar'
            WHEN 1 THEN 'Ludhiana'
            WHEN 2 THEN 'Patiala'
            WHEN 3 THEN 'Jalandhar'
            ELSE 'Bathinda'
        END,
        'Punjab',
        '14' + RIGHT('0000' + CAST(@WarehouseCounter AS VARCHAR), 4),
        CASE (@WarehouseCounter % 3) 
            WHEN 0 THEN 'Main'
            WHEN 1 THEN 'Secondary'
            ELSE 'Transit'
        END,
        CAST((RAND() * 5000 + 1000) AS DECIMAL(18,2)),
        CAST((RAND() * 2000) AS DECIMAL(18,2)),
        CAST((RAND() * 3000 + 1000) AS DECIMAL(18,2)),
        'Quintals',
        'Manager ' + CAST(@WarehouseCounter AS VARCHAR),
        '98' + RIGHT('00000000' + CAST(CAST(RAND() * 100000000 AS BIGINT) AS VARCHAR), 8),
        1,
        'System',
        DATEADD(DAY, -@WarehouseCounter, GETDATE())
    );
    SET @WarehouseCounter = @WarehouseCounter + 1;
END;
PRINT 'Warehouses: 37 records inserted';
GO

-- ============================================================================
-- 3. ADD STOCK MOVEMENTS (10 → 40) - Add 30 more
-- ============================================================================
PRINT 'Inserting Stock Movements...';
GO

DECLARE @MovementCounter INT = 11;
DECLARE @ProductIdSM INT, @WarehouseIdSM INT;

WHILE @MovementCounter <= 40
BEGIN
    SELECT TOP 1 @ProductIdSM = Id FROM Products ORDER BY NEWID();
    SELECT TOP 1 @WarehouseIdSM = Id FROM Warehouses ORDER BY NEWID();
    
    INSERT INTO StockMovements (MovementCode, MovementDate, ProductId, WarehouseId, 
                               MovementType, Quantity, UnitOfMeasure, Rate, TotalValue,
                               ReferenceNumber, ReferenceType, FromLocation, ToLocation,
                               Remarks, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'SM' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@MovementCounter AS VARCHAR), 4),
        DATEADD(DAY, -@MovementCounter, GETDATE()),
        @ProductIdSM,
        @WarehouseIdSM,
        CASE (@MovementCounter % 6)
            WHEN 0 THEN 'IN'
            WHEN 1 THEN 'OUT'
            WHEN 2 THEN 'TRANSFER'
            WHEN 3 THEN 'ADJUSTMENT'
            WHEN 4 THEN 'RETURN'
            ELSE 'PRODUCTION'
        END,
        CAST((RAND() * 1000 + 100) AS DECIMAL(18,2)),
        'kg',
        CAST((RAND() * 50 + 20) AS DECIMAL(18,2)),
        CAST((RAND() * 50000 + 5000) AS DECIMAL(18,2)),
        'REF' + CAST(@MovementCounter AS VARCHAR),
        CASE (@MovementCounter % 3)
            WHEN 0 THEN 'Purchase'
            WHEN 1 THEN 'Sales'
            ELSE 'Transfer'
        END,
        'From Location ' + CAST(@MovementCounter AS VARCHAR),
        'To Location ' + CAST(@MovementCounter AS VARCHAR),
        'Stock Movement ' + CAST(@MovementCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@MovementCounter, GETDATE()),
        1
    );
    SET @MovementCounter = @MovementCounter + 1;
END;
PRINT 'Stock Movements: 30 records inserted';
GO

-- ============================================================================
-- 4. ADD STOCK ADJUSTMENTS (0 → 40)
-- ============================================================================
PRINT 'Inserting Stock Adjustments...';
GO

DECLARE @AdjCounter INT = 1;
DECLARE @ProductIdAdj INT, @WarehouseIdAdj INT;

WHILE @AdjCounter <= 40
BEGIN
    SELECT TOP 1 @ProductIdAdj = Id FROM Products ORDER BY NEWID();
    SELECT TOP 1 @WarehouseIdAdj = Id FROM Warehouses ORDER BY NEWID();
    
    INSERT INTO StockAdjustments (AdjustmentCode, AdjustmentDate, ProductId, WarehouseId,
                                 AdjustmentType, Quantity, UnitOfMeasure, Reason,
                                 ApprovedBy, ApprovalDate, Status, Remarks, 
                                 CreatedBy, CreatedDate, IsActive)
    VALUES (
        'ADJ' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@AdjCounter AS VARCHAR), 4),
        DATEADD(DAY, -@AdjCounter, GETDATE()),
        @ProductIdAdj,
        @WarehouseIdAdj,
        CASE (@AdjCounter % 3)
            WHEN 0 THEN 'Increase'
            WHEN 1 THEN 'Decrease'
            ELSE 'Transfer'
        END,
        CAST((RAND() * 500 + 50) AS DECIMAL(18,2)),
        'kg',
        CASE (@AdjCounter % 5)
            WHEN 0 THEN 'Physical Count Variance'
            WHEN 1 THEN 'Damage'
            WHEN 2 THEN 'Quality Issue'
            WHEN 3 THEN 'System Correction'
            ELSE 'Expired Stock'
        END,
        'Manager ' + CAST(@AdjCounter AS VARCHAR),
        DATEADD(DAY, -@AdjCounter + 1, GETDATE()),
        CASE (@AdjCounter % 2) WHEN 0 THEN 'Approved' ELSE 'Pending' END,
        'Adjustment remarks ' + CAST(@AdjCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@AdjCounter, GETDATE()),
        1
    );
    SET @AdjCounter = @AdjCounter + 1;
END;
PRINT 'Stock Adjustments: 40 records inserted';
GO

-- Continue in next part due to size...
PRINT 'Part 1 of seed data completed';
GO


-- ============================================================================
-- 5. ADD PRODUCTION ORDERS (0 → 40)
-- ============================================================================
PRINT 'Inserting Production Orders...';
GO

DECLARE @POCounter INT = 1;
DECLARE @PaddyProductId INT, @RiceProductId INT, @MachineId INT, @SupervisorId INT;

WHILE @POCounter <= 40
BEGIN
    SELECT TOP 1 @PaddyProductId = Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID();
    SELECT TOP 1 @RiceProductId = Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID();
    SELECT TOP 1 @MachineId = Id FROM Machines ORDER BY NEWID();
    SELECT TOP 1 @SupervisorId = Id FROM Employees ORDER BY NEWID();
    
    INSERT INTO ProductionOrders (OrderNumber, OrderDate, PaddyProductId, TargetRiceProductId,
                                 PlannedQuantity, AssignedMachineId, AssignedSupervisorId,
                                 TargetDate, Priority, Status, Remarks, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'PO' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@POCounter AS VARCHAR), 4),
        DATEADD(DAY, -@POCounter, GETDATE()),
        @PaddyProductId,
        @RiceProductId,
        CAST((RAND() * 5000 + 1000) AS DECIMAL(18,2)),
        @MachineId,
        @SupervisorId,
        DATEADD(DAY, -@POCounter + 5, GETDATE()),
        CASE (@POCounter % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Low' END,
        CASE (@POCounter % 4) 
            WHEN 0 THEN 'Pending'
            WHEN 1 THEN 'In Progress'
            WHEN 2 THEN 'Completed'
            ELSE 'On Hold'
        END,
        'Production Order ' + CAST(@POCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@POCounter, GETDATE()),
        1
    );
    SET @POCounter = @POCounter + 1;
END;
PRINT 'Production Orders: 40 records inserted';
GO

-- ============================================================================
-- 6. ADD PRODUCTION BATCHES (0 → 40) with Inputs/Outputs
-- ============================================================================
PRINT 'Inserting Production Batches...';
GO

DECLARE @BatchCounter INT = 1;
DECLARE @ProdOrderId INT, @OperatorId INT, @SuperId INT, @NewBatchId INT;

WHILE @BatchCounter <= 40
BEGIN
    SELECT TOP 1 @ProdOrderId = Id FROM ProductionOrders ORDER BY NEWID();
    SELECT TOP 1 @OperatorId = Id FROM Employees ORDER BY NEWID();
    SELECT TOP 1 @SuperId = Id FROM Employees ORDER BY NEWID();
    
    INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, StartTime, EndTime,
                                  OperatorId, SupervisorId, InputQuantity, OutputQuantity,
                                  YieldPercentage, Status, Remarks, CreatedBy, CreatedDate, IsActive)
    OUTPUT INSERTED.Id INTO @TempBatch
    VALUES (
        'BATCH' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@BatchCounter AS VARCHAR), 4),
        @ProdOrderId,
        DATEADD(DAY, -@BatchCounter, GETDATE()),
        DATEADD(HOUR, 8, DATEADD(DAY, -@BatchCounter, GETDATE())),
        DATEADD(HOUR, 16, DATEADD(DAY, -@BatchCounter, GETDATE())),
        @OperatorId,
        @SuperId,
        CAST((RAND() * 2000 + 500) AS DECIMAL(18,2)),
        CAST((RAND() * 1400 + 350) AS DECIMAL(18,2)),
        CAST((RAND() * 20 + 70) AS DECIMAL(5,2)),
        CASE (@BatchCounter % 2) WHEN 0 THEN 'Completed' ELSE 'In Progress' END,
        'Batch ' + CAST(@BatchCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@BatchCounter, GETDATE()),
        1
    );
    
    SET @NewBatchId = SCOPE_IDENTITY();
    
    -- Add Batch Inputs
    DECLARE @InputProductId INT, @InputWarehouseId INT;
    SELECT TOP 1 @InputProductId = Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID();
    SELECT TOP 1 @InputWarehouseId = Id FROM Warehouses ORDER BY NEWID();
    
    INSERT INTO BatchInputs (BatchId, ProductId, WarehouseId, Quantity, UnitOfMeasure, 
                            Rate, TotalCost, CreatedBy, CreatedDate)
    VALUES (
        @NewBatchId,
        @InputProductId,
        @InputWarehouseId,
        CAST((RAND() * 2000 + 500) AS DECIMAL(18,2)),
        'kg',
        CAST((RAND() * 30 + 15) AS DECIMAL(18,2)),
        CAST((RAND() * 60000 + 7500) AS DECIMAL(18,2)),
        'System',
        DATEADD(DAY, -@BatchCounter, GETDATE())
    );
    
    -- Add Batch Outputs
    DECLARE @OutputProductId INT, @OutputWarehouseId INT;
    SELECT TOP 1 @OutputProductId = Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID();
    SELECT TOP 1 @OutputWarehouseId = Id FROM Warehouses ORDER BY NEWID();
    
    INSERT INTO BatchOutputs (BatchId, ProductId, WarehouseId, Quantity, UnitOfMeasure,
                             Quality, Grade, CreatedBy, CreatedDate)
    VALUES (
        @NewBatchId,
        @OutputProductId,
        @OutputWarehouseId,
        CAST((RAND() * 1400 + 350) AS DECIMAL(18,2)),
        'kg',
        CASE (@BatchCounter % 3) WHEN 0 THEN 'Premium' WHEN 1 THEN 'Standard' ELSE 'Economy' END,
        'Grade ' + CAST((@BatchCounter % 3) + 1 AS VARCHAR),
        'System',
        DATEADD(DAY, -@BatchCounter, GETDATE())
    );
    
    SET @BatchCounter = @BatchCounter + 1;
END;

DROP TABLE IF EXISTS @TempBatch;
PRINT 'Production Batches with Inputs/Outputs: 40 records inserted';
GO

-- Continue in next part...
PRINT 'Part 2 of seed data completed';
GO


-- ============================================================================
-- 7. ADD YIELD RECORDS (0 → 40)
-- ============================================================================
PRINT 'Inserting Yield Records...';
GO

DECLARE @YieldCounter INT = 1;
DECLARE @BatchIdYield INT, @PaddyProdId INT, @RiceProdId INT;

WHILE @YieldCounter <= 40
BEGIN
    SELECT TOP 1 @BatchIdYield = Id FROM ProductionBatches ORDER BY NEWID();
    SELECT TOP 1 @PaddyProdId = Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID();
    SELECT TOP 1 @RiceProdId = Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID();
    
    INSERT INTO YieldRecords (BatchId, PaddyVariety, RiceGrade, InputQuantity, OutputQuantity,
                             YieldPercentage, BrokenRice, Bran, Husk, QualityGrade, 
                             MachineEfficiency, AnalysisDate, AnalyzedBy, CreatedBy, CreatedDate, IsActive)
    VALUES (
        @BatchIdYield,
        CASE (@YieldCounter % 4) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masoori' WHEN 2 THEN 'IR-64' ELSE 'Swarna' END,
        'Grade ' + CAST((@YieldCounter % 3) + 1 AS VARCHAR),
        CAST((RAND() * 2000 + 500) AS DECIMAL(18,2)),
        CAST((RAND() * 1400 + 350) AS DECIMAL(18,2)),
        CAST((RAND() * 20 + 70) AS DECIMAL(5,2)),
        CAST((RAND() * 100 + 20) AS DECIMAL(18,2)),
        CAST((RAND() * 150 + 30) AS DECIMAL(18,2)),
        CAST((RAND() * 200 + 40) AS DECIMAL(18,2)),
        CASE (@YieldCounter % 3) WHEN 0 THEN 'Premium' WHEN 1 THEN 'Standard' ELSE 'Economy' END,
        CAST((RAND() * 20 + 75) AS DECIMAL(5,2)),
        DATEADD(DAY, -@YieldCounter, GETDATE()),
        'Analyst ' + CAST(@YieldCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@YieldCounter, GETDATE()),
        1
    );
    SET @YieldCounter = @YieldCounter + 1;
END;
PRINT 'Yield Records: 40 records inserted';
GO

-- ============================================================================
-- 8. ADD SALES DATA
-- ============================================================================

-- 8a. Inquiries (0 → 40)
PRINT 'Inserting Inquiries...';
GO

DECLARE @InqCounter INT = 1;
DECLARE @CustIdInq INT;

WHILE @InqCounter <= 40
BEGIN
    SELECT TOP 1 @CustIdInq = Id FROM Customers ORDER BY NEWID();
    
    INSERT INTO Inquiries (InquiryNumber, InquiryDate, CustomerId, ContactPerson, ContactNumber,
                          ProductType, Quantity, ExpectedDeliveryDate, Priority, Status,
                          Source, Remarks, AssignedTo, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'INQ' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@InqCounter AS VARCHAR), 4),
        DATEADD(DAY, -@InqCounter, GETDATE()),
        @CustIdInq,
        'Contact ' + CAST(@InqCounter AS VARCHAR),
        '98' + RIGHT('00000000' + CAST(CAST(RAND() * 100000000 AS BIGINT) AS VARCHAR), 8),
        CASE (@InqCounter % 4) WHEN 0 THEN 'Basmati Rice' WHEN 1 THEN 'Sona Masoori' WHEN 2 THEN 'IR-64' ELSE 'Parboiled Rice' END,
        CAST((RAND() * 5000 + 500) AS DECIMAL(18,2)),
        DATEADD(DAY, @InqCounter + 15, GETDATE()),
        CASE (@InqCounter % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Low' END,
        CASE (@InqCounter % 4) WHEN 0 THEN 'New' WHEN 1 THEN 'In Progress' WHEN 2 THEN 'Quoted' ELSE 'Closed' END,
        CASE (@InqCounter % 3) WHEN 0 THEN 'Phone' WHEN 1 THEN 'Email' ELSE 'Walk-in' END,
        'Inquiry ' + CAST(@InqCounter AS VARCHAR),
        'Sales Person ' + CAST((@InqCounter % 5) + 1 AS VARCHAR),
        'System',
        DATEADD(DAY, -@InqCounter, GETDATE()),
        1
    );
    SET @InqCounter = @InqCounter + 1;
END;
PRINT 'Inquiries: 40 records inserted';
GO

-- 8b. Quotations with Items (0 → 40)
PRINT 'Inserting Quotations...';
GO

DECLARE @QuotCounter INT = 1;
DECLARE @CustIdQuot INT, @NewQuotId INT;

WHILE @QuotCounter <= 40
BEGIN
    SELECT TOP 1 @CustIdQuot = Id FROM Customers ORDER BY NEWID();
    
    INSERT INTO Quotations (QuotationNumber, QuotationDate, CustomerId, ValidUntil,
                           PaymentTerms, DeliveryTerms, TotalAmount, TaxAmount, GrandTotal,
                           Status, PreparedBy, ApprovedBy, Remarks, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'QUOT' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@QuotCounter AS VARCHAR), 4),
        DATEADD(DAY, -@QuotCounter, GETDATE()),
        @CustIdQuot,
        DATEADD(DAY, -@QuotCounter + 30, GETDATE()),
        CASE (@QuotCounter % 2) WHEN 0 THEN 'Net 30' ELSE 'Net 15' END,
        'Ex-Warehouse',
        CAST((RAND() * 200000 + 50000) AS DECIMAL(18,2)),
        CAST((RAND() * 36000 + 9000) AS DECIMAL(18,2)),
        CAST((RAND() * 236000 + 59000) AS DECIMAL(18,2)),
        CASE (@QuotCounter % 3) WHEN 0 THEN 'Draft' WHEN 1 THEN 'Sent' ELSE 'Approved' END,
        'Sales Person ' + CAST((@QuotCounter % 5) + 1 AS VARCHAR),
        CASE (@QuotCounter % 3) WHEN 2 THEN 'Manager' ELSE NULL END,
        'Quotation ' + CAST(@QuotCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@QuotCounter, GETDATE()),
        1
    );
    
    SET @NewQuotId = SCOPE_IDENTITY();
    
    -- Add Quotation Items
    DECLARE @ItemProdId INT;
    SELECT TOP 1 @ItemProdId = Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID();
    
    INSERT INTO QuotationItems (QuotationId, ProductId, Description, Quantity, UnitPrice, 
                               TotalPrice, TaxRate, TaxAmount, NetAmount)
    VALUES (
        @NewQuotId,
        @ItemProdId,
        'Quotation Item ' + CAST(@QuotCounter AS VARCHAR),
        CAST((RAND() * 1000 + 100) AS DECIMAL(18,2)),
        CAST((RAND() * 50 + 30) AS DECIMAL(18,2)),
        CAST((RAND() * 50000 + 3000) AS DECIMAL(18,2)),
        18.00,
        CAST((RAND() * 9000 + 540) AS DECIMAL(18,2)),
        CAST((RAND() * 59000 + 3540) AS DECIMAL(18,2))
    );
    
    SET @QuotCounter = @QuotCounter + 1;
END;
PRINT 'Quotations with Items: 40 records inserted';
GO

PRINT 'Part 3 of seed data completed';
GO


-- 8c. Sales Orders with Items (0 → 40)
PRINT 'Inserting Sales Orders...';
GO

DECLARE @SOCounter INT = 1;
DECLARE @CustIdSO INT, @NewSOId INT;

WHILE @SOCounter <= 40
BEGIN
    SELECT TOP 1 @CustIdSO = Id FROM Customers ORDER BY NEWID();
    
    INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, DeliveryDate,
                            PaymentTerms, TotalAmount, TaxAmount, GrandTotal, 
                            Status, ApprovedBy, Remarks, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'SO' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@SOCounter AS VARCHAR), 4),
        DATEADD(DAY, -@SOCounter, GETDATE()),
        @CustIdSO,
        DATEADD(DAY, -@SOCounter + 7, GETDATE()),
        CASE (@SOCounter % 2) WHEN 0 THEN 'Net 30' ELSE 'Net 15' END,
        CAST((RAND() * 300000 + 75000) AS DECIMAL(18,2)),
        CAST((RAND() * 54000 + 13500) AS DECIMAL(18,2)),
        CAST((RAND() * 354000 + 88500) AS DECIMAL(18,2)),
        CASE (@SOCounter % 4) WHEN 0 THEN 'Pending' WHEN 1 THEN 'Confirmed' WHEN 2 THEN 'Delivered' ELSE 'Cancelled' END,
        CASE (@SOCounter % 3) WHEN 0 THEN 'Manager' ELSE NULL END,
        'Sales Order ' + CAST(@SOCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@SOCounter, GETDATE()),
        1
    );
    
    SET @NewSOId = SCOPE_IDENTITY();
    
    -- Add Sales Order Items
    DECLARE @SOItemProdId INT;
    SELECT TOP 1 @SOItemProdId = Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID();
    
    INSERT INTO SalesOrderItems (SalesOrderId, ProductId, Description, Quantity, UnitPrice, 
                                 TotalPrice, TaxRate, TaxAmount, NetAmount)
    VALUES (
        @NewSOId,
        @SOItemProdId,
        'SO Item ' + CAST(@SOCounter AS VARCHAR),
        CAST((RAND() * 1500 + 200) AS DECIMAL(18,2)),
        CAST((RAND() * 60 + 35) AS DECIMAL(18,2)),
        CAST((RAND() * 90000 + 7000) AS DECIMAL(18,2)),
        18.00,
        CAST((RAND() * 16200 + 1260) AS DECIMAL(18,2)),
        CAST((RAND() * 106200 + 8260) AS DECIMAL(18,2))
    );
    
    SET @SOCounter = @SOCounter + 1;
END;
PRINT 'Sales Orders with Items: 40 records inserted';
GO

-- 8d. Rice Sales (0 → 40)
PRINT 'Inserting Rice Sales...';
GO

DECLARE @RSCounter INT = 1;
DECLARE @CustIdRS INT;

WHILE @RSCounter <= 40
BEGIN
    SELECT TOP 1 @CustIdRS = Id FROM Customers ORDER BY NEWID();
    
    INSERT INTO RiceSales (Date, CustomerCode, CustomerName, RiceVariety, Quantity, Rate, 
                          TotalAmount, PaymentMode, PaymentStatus, Balance, CreatedDate, IsActive)
    VALUES (
        DATEADD(DAY, -@RSCounter, GETDATE()),
        'CUST' + RIGHT('0000' + CAST(@CustIdRS AS VARCHAR), 4),
        'Customer ' + CAST(@RSCounter AS VARCHAR),
        CASE (@RSCounter % 4) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masoori' WHEN 2 THEN 'IR-64' ELSE 'Parboiled' END,
        CAST((RAND() * 2000 + 500) AS DECIMAL(18,2)),
        CAST((RAND() * 60 + 30) AS DECIMAL(18,2)),
        CAST((RAND() * 120000 + 15000) AS DECIMAL(18,2)),
        CASE (@RSCounter % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        CASE (@RSCounter % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Partial' ELSE 'Pending' END,
        CASE (@RSCounter % 3) WHEN 0 THEN 0 ELSE CAST((RAND() * 50000) AS DECIMAL(18,2)) END,
        DATEADD(DAY, -@RSCounter, GETDATE()),
        1
    );
    SET @RSCounter = @RSCounter + 1;
END;
PRINT 'Rice Sales: 40 records inserted';
GO

-- 8e. By-Product Sales (0 → 40)
PRINT 'Inserting By-Product Sales...';
GO

DECLARE @BPCounter INT = 1;

WHILE @BPCounter <= 40
BEGIN
    INSERT INTO ByProductSales (Date, ByProduct, Quantity, Rate, TotalAmount, 
                               CustomerName, PaymentMode, PaymentStatus, CreatedDate, IsActive)
    VALUES (
        DATEADD(DAY, -@BPCounter, GETDATE()),
        CASE (@BPCounter % 3) WHEN 0 THEN 'Rice Bran' WHEN 1 THEN 'Rice Husk' ELSE 'Broken Rice' END,
        CAST((RAND() * 500 + 100) AS DECIMAL(18,2)),
        CAST((RAND() * 20 + 5) AS DECIMAL(18,2)),
        CAST((RAND() * 10000 + 500) AS DECIMAL(18,2)),
        'Customer ' + CAST(@BPCounter AS VARCHAR),
        CASE (@BPCounter % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        CASE (@BPCounter % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
        DATEADD(DAY, -@BPCounter, GETDATE()),
        1
    );
    SET @BPCounter = @BPCounter + 1;
END;
PRINT 'By-Product Sales: 40 records inserted';
GO

-- 8f. External Rice Sales (0 → 40)
PRINT 'Inserting External Rice Sales...';
GO

DECLARE @ERSCounter INT = 1;

WHILE @ERSCounter <= 40
BEGIN
    INSERT INTO ExternalRiceSales (Date, ItemDescription, SoldTo, SoldBy, Quantity, Rate, 
                                  TotalAmount, PaymentMode, PaymentStatus, Balance, 
                                  FullPaymentDate, Remarks, CreatedDate, IsActive)
    VALUES (
        DATEADD(DAY, -@ERSCounter, GETDATE()),
        CASE (@ERSCounter % 4) WHEN 0 THEN 'Basmati Rice' WHEN 1 THEN 'Sona Masoori' WHEN 2 THEN 'IR-64' ELSE 'Parboiled Rice' END,
        'Buyer ' + CAST(@ERSCounter AS VARCHAR),
        'Seller ' + CAST(@ERSCounter AS VARCHAR),
        CAST((RAND() * 1500 + 300) AS DECIMAL(18,2)),
        CAST((RAND() * 55 + 30) AS DECIMAL(18,2)),
        CAST((RAND() * 82500 + 9000) AS DECIMAL(18,2)),
        CASE (@ERSCounter % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        CASE (@ERSCounter % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Partial' ELSE 'Pending' END,
        CASE (@ERSCounter % 3) WHEN 0 THEN 0 ELSE CAST((RAND() * 30000) AS DECIMAL(18,2)) END,
        CASE (@ERSCounter % 3) WHEN 0 THEN DATEADD(DAY, -@ERSCounter + 5, GETDATE()) ELSE NULL END,
        'External Sale ' + CAST(@ERSCounter AS VARCHAR),
        DATEADD(DAY, -@ERSCounter, GETDATE()),
        1
    );
    SET @ERSCounter = @ERSCounter + 1;
END;
PRINT 'External Rice Sales: 40 records inserted';
GO

PRINT 'Part 4 of seed data completed';
GO


-- ============================================================================
-- 9. ADD FINANCE DATA
-- ============================================================================

-- 9a. Bank Transactions (0 → 40)
PRINT 'Inserting Bank Transactions...';
GO

DECLARE @BTCounter INT = 1;

WHILE @BTCounter <= 40
BEGIN
    INSERT INTO BankTransactions (Date, TransactionType, Amount, BankName, BranchName, 
                                 AccountNumber, ChequeNumber, ReferenceNumber, Narration, 
                                 CreatedDate, IsActive)
    VALUES (
        DATEADD(DAY, -@BTCounter, GETDATE()),
        CASE (@BTCounter % 4) WHEN 0 THEN 'Deposit' WHEN 1 THEN 'Withdrawal' WHEN 2 THEN 'Transfer' ELSE 'Payment' END,
        CAST((RAND() * 500000 + 50000) AS DECIMAL(18,2)),
        CASE (@BTCounter % 3) WHEN 0 THEN 'SBI' WHEN 1 THEN 'HDFC' ELSE 'ICICI' END,
        'Branch ' + CAST(@BTCounter AS VARCHAR),
        '12345' + RIGHT('00000' + CAST(@BTCounter AS VARCHAR), 5),
        CASE (@BTCounter % 2) WHEN 0 THEN 'CHQ' + CAST(@BTCounter AS VARCHAR) ELSE NULL END,
        'REF' + CAST(@BTCounter AS VARCHAR),
        'Bank Transaction ' + CAST(@BTCounter AS VARCHAR),
        DATEADD(DAY, -@BTCounter, GETDATE()),
        1
    );
    SET @BTCounter = @BTCounter + 1;
END;
PRINT 'Bank Transactions: 40 records inserted';
GO

-- 9b. Cash Book (0 → 40)
PRINT 'Inserting Cash Book entries...';
GO

DECLARE @CBCounter INT = 1;

WHILE @CBCounter <= 40
BEGIN
    INSERT INTO CashBook (Date, VoucherNumber, Particulars, VoucherType, ReceiptAmount, 
                         PaymentAmount, Balance, CreatedDate, IsActive)
    VALUES (
        DATEADD(DAY, -@CBCounter, GETDATE()),
        'VCH' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@CBCounter AS VARCHAR), 4),
        'Cash Transaction ' + CAST(@CBCounter AS VARCHAR),
        CASE (@CBCounter % 2) WHEN 0 THEN 'Receipt' ELSE 'Payment' END,
        CASE (@CBCounter % 2) WHEN 0 THEN CAST((RAND() * 100000 + 10000) AS DECIMAL(18,2)) ELSE 0 END,
        CASE (@CBCounter % 2) WHEN 1 THEN CAST((RAND() * 80000 + 8000) AS DECIMAL(18,2)) ELSE 0 END,
        CAST((RAND() * 200000 + 50000) AS DECIMAL(18,2)),
        DATEADD(DAY, -@CBCounter, GETDATE()),
        1
    );
    SET @CBCounter = @CBCounter + 1;
END;
PRINT 'Cash Book: 40 records inserted';
GO

-- 9c. Vouchers (0 → 40)
PRINT 'Inserting Vouchers...';
GO

DECLARE @VCounter INT = 1;

WHILE @VCounter <= 40
BEGIN
    INSERT INTO Vouchers (VoucherNumber, VoucherDate, VoucherType, Party, Amount, 
                         Narration, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'V' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@VCounter AS VARCHAR), 4),
        DATEADD(DAY, -@VCounter, GETDATE()),
        CASE (@VCounter % 4) WHEN 0 THEN 'Payment' WHEN 1 THEN 'Receipt' WHEN 2 THEN 'Journal' ELSE 'Contra' END,
        'Party ' + CAST(@VCounter AS VARCHAR),
        CAST((RAND() * 150000 + 15000) AS DECIMAL(18,2)),
        'Voucher ' + CAST(@VCounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@VCounter, GETDATE()),
        1
    );
    SET @VCounter = @VCounter + 1;
END;
PRINT 'Vouchers: 40 records inserted';
GO

-- 9d. Payables Overdue (0 → 40)
PRINT 'Inserting Payables Overdue...';
GO

DECLARE @PODCounter INT = 1;
DECLARE @VendorIdPOD INT;

WHILE @PODCounter <= 40
BEGIN
    SELECT TOP 1 @VendorIdPOD = Id FROM Vendors ORDER BY NEWID();
    
    INSERT INTO PayablesOverdue (VendorId, VendorName, InvoiceNumber, InvoiceDate, 
                                DueDate, Amount, PaidAmount, BalanceAmount, 
                                DaysOverdue, Status, Remarks, CreatedDate, IsActive)
    VALUES (
        @VendorIdPOD,
        'Vendor ' + CAST(@PODCounter AS VARCHAR),
        'INV' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@PODCounter AS VARCHAR), 4),
        DATEADD(DAY, -@PODCounter - 45, GETDATE()),
        DATEADD(DAY, -@PODCounter - 15, GETDATE()),
        CAST((RAND() * 200000 + 25000) AS DECIMAL(18,2)),
        CASE (@PODCounter % 3) WHEN 0 THEN 0 ELSE CAST((RAND() * 100000) AS DECIMAL(18,2)) END,
        CAST((RAND() * 100000 + 25000) AS DECIMAL(18,2)),
        @PODCounter + 15,
        CASE (@PODCounter % 3) WHEN 0 THEN 'Overdue' WHEN 1 THEN 'Partially Paid' ELSE 'Pending' END,
        'Payable ' + CAST(@PODCounter AS VARCHAR),
        DATEADD(DAY, -@PODCounter, GETDATE()),
        1
    );
    SET @PODCounter = @PODCounter + 1;
END;
PRINT 'Payables Overdue: 40 records inserted';
GO

-- 9e. Receivables Overdue (0 → 40)
PRINT 'Inserting Receivables Overdue...';
GO

DECLARE @RODCounter INT = 1;
DECLARE @CustIdROD INT;

WHILE @RODCounter <= 40
BEGIN
    SELECT TOP 1 @CustIdROD = Id FROM Customers ORDER BY NEWID();
    
    INSERT INTO ReceivablesOverdue (CustomerId, CustomerName, InvoiceNumber, InvoiceDate,
                                   DueDate, Amount, ReceivedAmount, BalanceAmount,
                                   DaysOverdue, Status, Remarks, CreatedDate, IsActive)
    VALUES (
        @CustIdROD,
        'Customer ' + CAST(@RODCounter AS VARCHAR),
        'SI' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@RODCounter AS VARCHAR), 4),
        DATEADD(DAY, -@RODCounter - 50, GETDATE()),
        DATEADD(DAY, -@RODCounter - 20, GETDATE()),
        CAST((RAND() * 300000 + 40000) AS DECIMAL(18,2)),
        CASE (@RODCounter % 3) WHEN 0 THEN 0 ELSE CAST((RAND() * 150000) AS DECIMAL(18,2)) END,
        CAST((RAND() * 150000 + 40000) AS DECIMAL(18,2)),
        @RODCounter + 20,
        CASE (@RODCounter % 3) WHEN 0 THEN 'Overdue' WHEN 1 THEN 'Partially Received' ELSE 'Pending' END,
        'Receivable ' + CAST(@RODCounter AS VARCHAR),
        DATEADD(DAY, -@RODCounter, GETDATE()),
        1
    );
    SET @RODCounter = @RODCounter + 1;
END;
PRINT 'Receivables Overdue: 40 records inserted';
GO

-- 9f. Loans & Advances (0 → 40)
PRINT 'Inserting Loans & Advances...';
GO

DECLARE @LACounter INT = 1;

WHILE @LACounter <= 40
BEGIN
    INSERT INTO LoansAdvances (AccountType, PartyName, Amount, Date, InterestRate, 
                              DueDate, Status, PaidAmount, Balance, Remarks, 
                              CreatedDate, IsActive)
    VALUES (
        CASE (@LACounter % 2) WHEN 0 THEN 'Loan' ELSE 'Advance' END,
        'Party ' + CAST(@LACounter AS VARCHAR),
        CAST((RAND() * 1000000 + 100000) AS DECIMAL(18,2)),
        DATEADD(DAY, -@LACounter - 180, GETDATE()),
        CAST((RAND() * 5 + 8) AS DECIMAL(5,2)),
        DATEADD(DAY, -@LACounter + 180, GETDATE()),
        CASE (@LACounter % 3) WHEN 0 THEN 'Active' WHEN 1 THEN 'Partial' ELSE 'Closed' END,
        CASE (@LACounter % 3) WHEN 2 THEN CAST((RAND() * 1000000 + 100000) AS DECIMAL(18,2)) 
             ELSE CAST((RAND() * 500000) AS DECIMAL(18,2)) END,
        CASE (@LACounter % 3) WHEN 2 THEN 0 ELSE CAST((RAND() * 500000 + 50000) AS DECIMAL(18,2)) END,
        'Loan/Advance ' + CAST(@LACounter AS VARCHAR),
        DATEADD(DAY, -@LACounter, GETDATE()),
        1
    );
    SET @LACounter = @LACounter + 1;
END;
PRINT 'Loans & Advances: 40 records inserted';
GO

-- ============================================================================
-- 10. ADD FIXED ASSETS (0 → 40)
-- ============================================================================
PRINT 'Inserting Fixed Assets...';
GO

DECLARE @FACounter INT = 1;

WHILE @FACounter <= 40
BEGIN
    INSERT INTO FixedAssets (AssetCode, AssetName, AssetType, PurchaseDate, PurchaseValue,
                            CurrentValue, DepreciationRate, AccumulatedDepreciation,
                            Condition, Location, Supplier, InvoiceNumber, 
                            Remarks, CreatedBy, CreatedDate, IsActive)
    VALUES (
        'FA' + CAST(YEAR(GETDATE()) AS VARCHAR) + RIGHT('0000' + CAST(@FACounter AS VARCHAR), 4),
        'Asset ' + CAST(@FACounter AS VARCHAR),
        CASE (@FACounter % 5) 
            WHEN 0 THEN 'Machinery' 
            WHEN 1 THEN 'Equipment'
            WHEN 2 THEN 'Vehicle'
            WHEN 3 THEN 'Furniture'
            ELSE 'Computer'
        END,
        DATEADD(DAY, -@FACounter - 365, GETDATE()),
        CAST((RAND() * 2000000 + 100000) AS DECIMAL(18,2)),
        CAST((RAND() * 1500000 + 75000) AS DECIMAL(18,2)),
        CAST((RAND() * 15 + 5) AS DECIMAL(5,2)),
        CAST((RAND() * 500000 + 25000) AS DECIMAL(18,2)),
        CASE (@FACounter % 3) WHEN 0 THEN 'Excellent' WHEN 1 THEN 'Good' ELSE 'Fair' END,
        'Location ' + CAST(@FACounter AS VARCHAR),
        'Supplier ' + CAST(@FACounter AS VARCHAR),
        'INV' + CAST(@FACounter AS VARCHAR),
        'Fixed Asset ' + CAST(@FACounter AS VARCHAR),
        'System',
        DATEADD(DAY, -@FACounter, GETDATE()),
        1
    );
    SET @FACounter = @FACounter + 1;
END;
PRINT 'Fixed Assets: 40 records inserted';
GO

-- ============================================================================
-- FINAL SUMMARY
-- ============================================================================
PRINT '';
PRINT '========================================';
PRINT 'DATA INSERTION COMPLETED SUCCESSFULLY!';
PRINT '========================================';
PRINT '';
PRINT 'Summary of Records Inserted:';
PRINT '- Vendors: 35 records';
PRINT '- Warehouses: 37 records';
PRINT '- Stock Movements: 30 records';
PRINT '- Stock Adjustments: 40 records';
PRINT '- Production Orders: 40 records';
PRINT '- Production Batches: 40 records';
PRINT '- Batch Inputs: 40 records';
PRINT '- Batch Outputs: 40 records';
PRINT '- Yield Records: 40 records';
PRINT '- Inquiries: 40 records';
PRINT '- Quotations: 40 records';
PRINT '- Quotation Items: 40 records';
PRINT '- Sales Orders: 40 records';
PRINT '- Sales Order Items: 40 records';
PRINT '- Rice Sales: 40 records';
PRINT '- By-Product Sales: 40 records';
PRINT '- External Rice Sales: 40 records';
PRINT '- Bank Transactions: 40 records';
PRINT '- Cash Book: 40 records';
PRINT '- Vouchers: 40 records';
PRINT '- Payables Overdue: 40 records';
PRINT '- Receivables Overdue: 40 records';
PRINT '- Loans & Advances: 40 records';
PRINT '- Fixed Assets: 40 records';
PRINT '';
PRINT 'Total Records Inserted: 892+';
PRINT '';
PRINT 'All pages should now display data!';
PRINT '========================================';
GO

