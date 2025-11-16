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

// 1. Storage Zones
Execute(@"
DECLARE @counter INT = 1;
WHILE @counter <= 40
BEGIN
    DECLARE @warehouseId INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
    INSERT INTO StorageZones (WarehouseId, ZoneCode, ZoneName, ZoneType, Capacity, CurrentUtilization, TemperatureControlled, HumidityControlled, SecurityLevel, IsActive)
    VALUES (@warehouseId,
            'ZONE-' + RIGHT('00' + CAST(@counter AS VARCHAR), 2),
            CASE (@counter % 5) WHEN 0 THEN 'Dry Storage' WHEN 1 THEN 'Climate Controlled' WHEN 2 THEN 'High Security' WHEN 3 THEN 'Bulk Storage' ELSE 'General Storage' END,
            CASE (@counter % 4) WHEN 0 THEN 'Dry' WHEN 1 THEN 'Cold' WHEN 2 THEN 'Frozen' ELSE 'Ambient' END,
            1000 + (@counter * 100),
            50.0 + (@counter % 30),
            CASE WHEN (@counter % 3) = 0 THEN 1 ELSE 0 END,
            CASE WHEN (@counter % 4) = 0 THEN 1 ELSE 0 END,
            CASE (@counter % 3) WHEN 0 THEN 'High' WHEN 1 THEN 'Medium' ELSE 'Standard' END,
            1);
    SET @counter = @counter + 1;
END
", "StorageZones");

// 2. Batch Inputs
Execute(@"
INSERT INTO BatchInputs (BatchId, ProductId, WarehouseId, ZoneId, QuantityUsed, UnitCost, TotalCost, LotNumber, ExpiryDate)
SELECT TOP 40
    pb.Id,
    p.Id,
    w.Id,
    sz.Id,
    200.0 + (pb.Id % 500),
    25.0 + (pb.Id % 25),
    5000.0 + (pb.Id % 5000),
    'LOT-' + RIGHT('000' + CAST(pb.Id AS VARCHAR), 4),
    DATEADD(DAY, 180, GETDATE())
FROM ProductionBatches pb
CROSS APPLY (SELECT TOP 1 Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID()) p
CROSS APPLY (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()) w
CROSS APPLY (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()) sz
WHERE NOT EXISTS (SELECT 1 FROM BatchInputs WHERE BatchId = pb.Id)
", "BatchInputs");

// 3. Batch Outputs
Execute(@"
INSERT INTO BatchOutputs (BatchId, ProductId, WarehouseId, ZoneId, QuantityProduced, QualityGrade, UnitPrice, TotalValue, LotNumber, ProductionDate, ExpiryDate)
SELECT TOP 40
    pb.Id,
    p.Id,
    w.Id,
    sz.Id,
    180.0 + (pb.Id % 400),
    CASE (pb.Id % 4) WHEN 0 THEN 'Premium' WHEN 1 THEN 'Grade A' WHEN 2 THEN 'Grade B' ELSE 'Standard' END,
    50.0 + (pb.Id % 50),
    9000.0 + (pb.Id % 11000),
    'OUT-' + RIGHT('000' + CAST(pb.Id AS VARCHAR), 4),
    DATEADD(DAY, -30, GETDATE()),
    DATEADD(DAY, 300, GETDATE())
FROM ProductionBatches pb
CROSS APPLY (SELECT TOP 1 Id FROM Products WHERE ProductType IN ('Rice', 'By-Product') ORDER BY NEWID()) p
CROSS APPLY (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()) w
CROSS APPLY (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()) sz
WHERE NOT EXISTS (SELECT 1 FROM BatchOutputs WHERE BatchId = pb.Id)
", "BatchOutputs");

// 4. Quotation Items (2-3 per quotation)
Execute(@"
INSERT INTO QuotationItems (QuotationId, ProductId, Quantity, UnitPrice, DiscountPercentage, DiscountAmount, TaxPercentage, TaxAmount, LineTotal, DeliveryDays, SpecialInstructions)
SELECT
    q.Id,
    p.Id,
    50.0 + (q.Id % 150),
    100.0 + (q.Id % 100),
    5.0,
    250.0,
    13.0,
    650.0,
    5000.0 + (q.Id % 15000),
    7 + (q.Id % 14),
    NULL
FROM Quotations q
CROSS APPLY (SELECT TOP 2 Id FROM Products ORDER BY NEWID()) p
WHERE NOT EXISTS (SELECT 1 FROM QuotationItems WHERE QuotationId = q.Id)
", "QuotationItems");

// 5. Sales Order Items (2-3 per order)
Execute(@"
INSERT INTO SalesOrderItems (SalesOrderId, ProductId, Quantity, UnitPrice, DiscountPercentage, DiscountAmount, TaxPercentage, TaxAmount, LineTotal, DeliveryDate, DeliveryStatus, Notes)
SELECT
    so.Id,
    p.Id,
    60.0 + (so.Id % 140),
    105.0 + (so.Id % 95),
    7.5,
    300.0,
    13.0,
    700.0,
    5400.0 + (so.Id % 14600),
    DATEADD(DAY, 14, GETDATE()),
    'Pending',
    NULL
FROM SalesOrders so
CROSS APPLY (SELECT TOP 2 Id FROM Products ORDER BY NEWID()) p
WHERE NOT EXISTS (SELECT 1 FROM SalesOrderItems WHERE SalesOrderId = so.Id)
", "SalesOrderItems");

// 6. Stock Movements (10 -> 40)
Execute(@"
DECLARE @i INT = 1;
WHILE @i <= 30
BEGIN
    DECLARE @productId INT = (SELECT TOP 1 Id FROM Products ORDER BY NEWID());
    DECLARE @warehouseId INT = (SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID());
    DECLARE @zoneId INT = (SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID());
    DECLARE @empName VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees ORDER BY NEWID());

    INSERT INTO StockMovements (ProductId, WarehouseId, ZoneId, MovementType, MovementCode, Quantity, UnitCost, TotalCost, ReferenceType, ReferenceId, MovementDate, PerformedBy, Notes, IsPosted)
    VALUES (@productId, @warehouseId, @zoneId,
            CASE (@i % 4) WHEN 0 THEN 'In' WHEN 1 THEN 'Out' WHEN 2 THEN 'Transfer' ELSE 'Adjustment' END,
            'MOVE-' + RIGHT('0000' + CAST(10000 + @i AS VARCHAR), 5),
            250.0 + (@i * 10),
            50.0,
            12500.0 + (@i * 500),
            'Purchase',
            'REF-' + CAST(5000 + @i AS VARCHAR),
            DATEADD(DAY, -30, GETDATE()),
            @empName,
            NULL,
            1);
    SET @i = @i + 1;
END
", "StockMovements (+30)");

// 7. Yield Records (20 -> 40)
Execute(@"
INSERT INTO YieldRecords (BatchId, TotalInputQuantity, TotalRiceOutput, TotalByProductOutput, ActualYieldPercentage, StandardYieldPercentage, YieldVariance, QualityRating, RiceGradeA, RiceGradeB, RiceGradeC, BrokenRicePercentage, ByProductBreakdown, RecordedAt, RecordedBy, Notes)
SELECT TOP 20
    pb.Id,
    1000.0 + (pb.Id % 500),
    700.0 + (pb.Id % 300),
    200.0 + (pb.Id % 100),
    70.0,
    70.0,
    0.0,
    8.5,
    350.0,
    250.0,
    100.0,
    8.0,
    'Husk: 100kg, Bran: 80kg',
    DATEADD(DAY, -15, GETDATE()),
    e.EmployeeName,
    'Standard yield achieved'
FROM ProductionBatches pb
CROSS APPLY (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Supervisor' ORDER BY NEWID()) e
WHERE NOT EXISTS (SELECT 1 FROM YieldRecords WHERE BatchId = pb.Id)
", "YieldRecords (+20)");

// 8. Quotations (23 -> 40)
Execute(@"
DECLARE @j INT = 1;
WHILE @j <= 17
BEGIN
    DECLARE @custId INT = (SELECT TOP 1 Id FROM Customers ORDER BY NEWID());
    DECLARE @inqId INT = (SELECT TOP 1 Id FROM Inquiries ORDER BY NEWID());
    DECLARE @prepBy VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Sales' ORDER BY NEWID());
    DECLARE @appBy VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Manager' ORDER BY NEWID());

    INSERT INTO Quotations (QuotationNumber, QuotationDate, ValidUntil, CustomerId, ContactPerson, InquiryId, TotalAmount, TaxAmount, GrandTotal, Status, PreparedBy, ApprovedBy, ApprovedDate, Terms, Notes)
    VALUES ('QT-2024-' + RIGHT('000' + CAST(1000 + @j AS VARCHAR), 4),
            DATEADD(DAY, -20, GETDATE()),
            DATEADD(DAY, 20, GETDATE()),
            @custId,
            'Contact Person',
            @inqId,
            25000.0 + (@j * 1000),
            3250.0 + (@j * 130),
            28250.0 + (@j * 1130),
            CASE (@j % 4) WHEN 0 THEN 'Draft' WHEN 1 THEN 'Sent' WHEN 2 THEN 'Accepted' ELSE 'Rejected' END,
            @prepBy,
            @appBy,
            DATEADD(DAY, -18, GETDATE()),
            'Payment: Net 30 | Delivery: 14 days',
            NULL);
    SET @j = @j + 1;
END
", "Quotations (+17)");

// 9. Sales Orders (23 -> 40)
Execute(@"
DECLARE @k INT = 1;
WHILE @k <= 17
BEGIN
    DECLARE @custId2 INT = (SELECT TOP 1 Id FROM Customers ORDER BY NEWID());
    DECLARE @crBy VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Sales' ORDER BY NEWID());
    DECLARE @apBy VARCHAR(100) = (SELECT TOP 1 EmployeeName FROM Employees WHERE Role = 'Manager' ORDER BY NEWID());

    INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, ExpectedDeliveryDate, TotalAmount, TaxAmount, GrandTotal, PaymentTerms, DeliveryTerms, Status, CreatedBy, ApprovedBy, ApprovedDate, Notes)
    VALUES ('SO-2024-' + RIGHT('000' + CAST(2000 + @k AS VARCHAR), 4),
            DATEADD(DAY, -15, GETDATE()),
            @custId2,
            NULL,
            DATEADD(DAY, 15, GETDATE()),
            28000.0 + (@k * 1200),
            3640.0 + (@k * 156),
            31640.0 + (@k * 1356),
            'Net 30',
            'FOB',
            CASE (@k % 5) WHEN 0 THEN 'Pending' WHEN 1 THEN 'Confirmed' WHEN 2 THEN 'Processing' WHEN 3 THEN 'Shipped' ELSE 'Delivered' END,
            @crBy,
            @apBy,
            DATEADD(DAY, -13, GETDATE()),
            NULL);
    SET @k = @k + 1;
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
