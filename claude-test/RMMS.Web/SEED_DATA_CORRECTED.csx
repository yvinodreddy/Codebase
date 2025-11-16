#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;

var conn = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;Connection Timeout=180;";

void Execute(string sql, string description)
{
    try
    {
        using var connection = new SqlConnection(conn);
        connection.Open();
        var command = new SqlCommand(sql, connection);
        command.CommandTimeout = 180;
        var rows = command.ExecuteNonQuery();
        Console.WriteLine($"✅ {description}: {rows} records");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"❌ {description}: {ex.Message}");
    }
}

Console.WriteLine("=== DATA SEEDING STARTED ===\n");

// 1. Storage Zones (0 -> 40)
Execute(@"
DECLARE @counter INT = 1;
WHILE @counter <= 40
BEGIN
    DECLARE @warehouseId INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
    INSERT INTO StorageZones (WarehouseId, ZoneCode, ZoneName, ZoneType, Capacity, UsedCapacity, AvailableCapacity, Temperature, Humidity, Status, Remarks, CreatedDate, CreatedBy, IsActive)
    VALUES (@warehouseId,
            'ZONE-' + RIGHT('00' + CAST(@counter AS VARCHAR), 2),
            CASE (@counter % 5) WHEN 0 THEN 'Dry Storage' WHEN 1 THEN 'Climate Controlled' WHEN 2 THEN 'High Security' WHEN 3 THEN 'Bulk Storage' ELSE 'General Storage' END,
            CASE (@counter % 4) WHEN 0 THEN 'Dry' WHEN 1 THEN 'Cold' WHEN 2 THEN 'Frozen' ELSE 'Ambient' END,
            1000 + (@counter * 100),
            500 + (@counter * 20),
            500 + (@counter * 80),
            25.0 + (@counter % 10),
            50.0 + (@counter % 20),
            'Active',
            'Auto-generated zone ' + CAST(@counter AS VARCHAR),
            GETDATE(),
            'System',
            1);
    SET @counter = @counter + 1;
END
", "StorageZones");

// 2. Batch Inputs (0 -> 40)
Execute(@"
DECLARE @i INT = 1;
WHILE @i <= 40
BEGIN
    DECLARE @batchId INT = (SELECT TOP 1 Id FROM ProductionBatches WHERE Id NOT IN (SELECT DISTINCT BatchId FROM BatchInputs WHERE BatchId IS NOT NULL) ORDER BY Id OFFSET (@i-1) ROWS FETCH NEXT 1 ROWS ONLY);
    IF @batchId IS NOT NULL
    BEGIN
        DECLARE @productId INT = (SELECT TOP 1 Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID());
        DECLARE @warehouseId INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
        DECLARE @zoneId INT = (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID());

        INSERT INTO BatchInputs (BatchId, InputType, ProductId, Quantity, UOM, WarehouseId, ZoneId, MoistureContent, BatchLotNumber, Grade, UnitCost, Remarks, CreatedDate, CreatedBy)
        VALUES (@batchId, 'Paddy', @productId, 500.0 + (@i * 10), 'Kg', @warehouseId, @zoneId, 12.0 + (@i % 5), 'LOT-' + RIGHT('000' + CAST(@i AS VARCHAR), 4), 'Grade A', 25.0, 'Batch input ' + CAST(@i AS VARCHAR), GETDATE(), 'System');
    END
    SET @i = @i + 1;
END
", "BatchInputs");

// 3. Batch Outputs (0 -> 40)
Execute(@"
DECLARE @j INT = 1;
WHILE @j <= 40
BEGIN
    DECLARE @batchId2 INT = (SELECT TOP 1 Id FROM ProductionBatches WHERE Id NOT IN (SELECT DISTINCT BatchId FROM BatchOutputs WHERE BatchId IS NOT NULL) ORDER BY Id OFFSET (@j-1) ROWS FETCH NEXT 1 ROWS ONLY);
    IF @batchId2 IS NOT NULL
    BEGIN
        DECLARE @productId2 INT = (SELECT TOP 1 Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID());
        DECLARE @warehouseId2 INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
        DECLARE @zoneId2 INT = (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID());

        INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, ZoneId, QualityScore, MoistureContent, BatchLotNumber, UnitCost, BagsCount, BagsWeight, Remarks, CreatedDate, CreatedBy)
        VALUES (@batchId2, 'Rice', @productId2, 'Premium', 350.0 + (@j * 8), 'Kg', @warehouseId2, @zoneId2, 85.0 + (@j % 15), 10.0 + (@j % 3), 'OUT-' + RIGHT('000' + CAST(@j AS VARCHAR), 4), 50.0, 7 + (@j % 3), 50.0, 'Batch output ' + CAST(@j AS VARCHAR), GETDATE(), 'System');
    END
    SET @j = @j + 1;
END
", "BatchOutputs");

// 4. Quotation Items (2-3 per quotation = ~60 items)
Execute(@"
INSERT INTO QuotationItems (QuotationId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountPercent, DiscountAmount, TaxPercent, TaxAmount, TotalAmount, Remarks)
SELECT TOP 60
    q.Id,
    p.Id,
    p.ProductName,
    50.0 + (ROW_NUMBER() OVER (ORDER BY q.Id, p.Id) % 150),
    'Kg',
    100.0 + (ROW_NUMBER() OVER (ORDER BY q.Id, p.Id) % 100),
    5.0,
    250.0,
    13.0,
    650.0,
    5000.0 + (ROW_NUMBER() OVER (ORDER BY q.Id, p.Id) % 15000),
    'Auto-generated item'
FROM Quotations q
CROSS APPLY (SELECT TOP 3 Id, ProductName FROM Products ORDER BY NEWID()) p
WHERE NOT EXISTS (SELECT 1 FROM QuotationItems WHERE QuotationId = q.Id)
", "QuotationItems");

// 5. Sales Order Items (2-3 per order = ~60 items)
Execute(@"
INSERT INTO SalesOrderItems (SalesOrderId, ProductId, ProductDescription, Quantity, UnitOfMeasure, UnitPrice, DiscountAmount, TaxAmount, TotalAmount, AllocatedQuantity, DispatchedQuantity, WarehouseId, Remarks)
SELECT TOP 60
    so.Id,
    p.Id,
    p.ProductName,
    60.0 + (ROW_NUMBER() OVER (ORDER BY so.Id, p.Id) % 140),
    'Kg',
    105.0 + (ROW_NUMBER() OVER (ORDER BY so.Id, p.Id) % 95),
    300.0,
    700.0,
    5400.0 + (ROW_NUMBER() OVER (ORDER BY so.Id, p.Id) % 14600),
    0.0,
    0.0,
    w.Id,
    'Auto-generated item'
FROM SalesOrders so
CROSS APPLY (SELECT TOP 3 Id, ProductName FROM Products ORDER BY NEWID()) p
CROSS APPLY (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()) w
WHERE NOT EXISTS (SELECT 1 FROM SalesOrderItems WHERE SalesOrderId = so.Id)
", "SalesOrderItems");

// 6. Stock Movements (10 -> 40)
Execute(@"
DECLARE @k INT = 1;
WHILE @k <= 30
BEGIN
    DECLARE @productId3 INT = (SELECT TOP 1 Id FROM Products ORDER BY NEWID());
    DECLARE @warehouseId3 INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
    DECLARE @zoneId3 INT = (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID());
    DECLARE @empName VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees ORDER BY NEWID());

    INSERT INTO StockMovements (MovementCode, ProductId, WarehouseId, ZoneId, MovementType, MovementCategory, Quantity, UnitCost, TotalCost, ReferenceType, ReferenceId, ReferenceNumber, MovementDate, PerformedBy, Remarks, IsApproved, CreatedDate, CreatedBy, IsActive)
    VALUES ('MOVE-' + RIGHT('0000' + CAST(10000 + @k AS VARCHAR), 5),
            @productId3, @warehouseId3, @zoneId3,
            CASE (@k % 4) WHEN 0 THEN 'In' WHEN 1 THEN 'Out' WHEN 2 THEN 'Transfer' ELSE 'Adjustment' END,
            'Purchase',
            250.0 + (@k * 10),
            50.0,
            12500.0 + (@k * 500),
            'Purchase',
            1000 + @k,
            'REF-' + CAST(5000 + @k AS VARCHAR),
            DATEADD(DAY, -30, GETDATE()),
            @empName,
            'Auto-generated movement',
            1,
            GETDATE(),
            'System',
            1);
    SET @k = @k + 1;
END
", "StockMovements (+30)");

// 7. Yield Records (20 -> 40)
Execute(@"
INSERT INTO YieldRecords (BatchId, PaddyVariety, InputPaddyQuantity, OutputHeadRice, OutputBrokenRice, OutputBran, OutputHusk, OutputWastage, HeadRicePercent, BrokenRicePercent, BranPercent, HuskPercent, WastagePercent, TotalYieldPercent, StandardHeadRicePercent, StandardTotalYieldPercent, YieldGrade, QualityScore, MillingRecovery, HeadRiceToBrokenRatio, Remarks, VarianceAnalysis, CalculatedDate, CalculatedBy, IsVerified)
SELECT TOP 20
    pb.Id,
    'Basmati',
    1000.0,
    700.0,
    150.0,
    80.0,
    60.0,
    10.0,
    70.0,
    15.0,
    8.0,
    6.0,
    1.0,
    70.0,
    68.0,
    70.0,
    'A',
    85.0,
    85.0,
    4.67,
    'Standard yield achieved',
    'Within acceptable range',
    GETDATE(),
    e.EmployeeName,
    1
FROM ProductionBatches pb
CROSS APPLY (SELECT TOP 1 EmployeeName FROM Employees ORDER BY NEWID()) e
WHERE NOT EXISTS (SELECT 1 FROM YieldRecords WHERE BatchId = pb.Id)
", "YieldRecords (+20)");

// 8. Quotations (23 -> 40)
Execute(@"
DECLARE @m INT = 1;
WHILE @m <= 17
BEGIN
    DECLARE @custId INT = (SELECT TOP 1 Id FROM Customers ORDER BY NEWID());
    DECLARE @inqId INT = (SELECT TOP 1 Id FROM Inquiries ORDER BY NEWID());
    DECLARE @empId INT = (SELECT TOP 1 Id FROM Employees ORDER BY NEWID());

    INSERT INTO Quotations (QuotationNumber, QuotationDate, CustomerId, InquiryId, ValidUntil, PaymentTerms, DeliveryTerms, SubtotalAmount, DiscountPercent, DiscountAmount, TaxAmount, TotalAmount, Status, ApprovedByEmployeeId, TermsAndConditions, Remarks, CreatedDate, CreatedBy, IsActive)
    VALUES ('QT-2024-' + RIGHT('000' + CAST(1000 + @m AS VARCHAR), 4),
            DATEADD(DAY, -20, GETDATE()),
            @custId,
            @inqId,
            DATEADD(DAY, 20, GETDATE()),
            'Net 30',
            'FOB',
            25000.0,
            5.0,
            1250.0,
            3250.0,
            27000.0,
            'Sent',
            @empId,
            'Standard terms apply',
            'Auto-generated quotation',
            GETDATE(),
            'System',
            1);
    SET @m = @m + 1;
END
", "Quotations (+17)");

// 9. Sales Orders (23 -> 40)
Execute(@"
DECLARE @n INT = 1;
WHILE @n <= 17
BEGIN
    DECLARE @custId2 INT = (SELECT TOP 1 Id FROM Customers ORDER BY NEWID());
    DECLARE @empId2 INT = (SELECT TOP 1 Id FROM Employees ORDER BY NEWID());

    INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, DeliveryDate, DeliveryAddress, PaymentTerms, DeliveryTerms, SubtotalAmount, DiscountAmount, TaxAmount, FreightCharges, OtherCharges, TotalAmount, Status, Priority, ApprovedByEmployeeId, SpecialInstructions, Remarks, CreatedDate, CreatedBy, StockReserved, IsActive)
    VALUES ('SO-2024-' + RIGHT('000' + CAST(2000 + @n AS VARCHAR), 4),
            DATEADD(DAY, -15, GETDATE()),
            @custId2,
            NULL,
            DATEADD(DAY, 15, GETDATE()),
            'Customer Address',
            'Net 30',
            'FOB',
            28000.0,
            1400.0,
            3640.0,
            500.0,
            100.0,
            30740.0,
            'Confirmed',
            'Normal',
            @empId2,
            'Standard delivery',
            'Auto-generated order',
            GETDATE(),
            'System',
            0,
            1);
    SET @n = @n + 1;
END
", "SalesOrders (+17)");

Console.WriteLine("\n=== VERIFICATION ===");

void Count(string table)
{
    using var connection = new SqlConnection(conn);
    connection.Open();
    var command = new SqlCommand($"SELECT COUNT(*) FROM {table}", connection);
    var count = (int)command.ExecuteScalar();
    Console.WriteLine($"{table}: {count} records");
}

Count("StorageZones");
Count("BatchInputs");
Count("BatchOutputs");
Count("QuotationItems");
Count("SalesOrderItems");
Count("StockMovements");
Count("YieldRecords");
Count("Quotations");
Count("SalesOrders");

Console.WriteLine("\n✅ ALL MEDIUM PRIORITY TASKS COMPLETED!");
