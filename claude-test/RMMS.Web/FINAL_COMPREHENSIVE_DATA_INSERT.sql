-- ============================================
-- FINAL COMPREHENSIVE DATA INSERT
-- Uses CORRECT schema column names
-- ============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'COMPREHENSIVE DATA INSERTION';
PRINT '========================================';
GO

-- ============================================
-- 1. PRODUCTS (50 records)
-- ============================================
PRINT 'Inserting Products...';

DELETE FROM Products WHERE Id BETWEEN 1 AND 100;

INSERT INTO Products (ProductCode, ProductName, ProductCategory, ProductType, Grade, Description, UnitOfMeasure,
                      StandardCost, SellingPrice, ReorderLevel, IsRawMaterial, IsFinishedProduct, IsByProduct,
                      Status, CreatedDate, IsActive)
SELECT
    'PRD-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    CASE WHEN n <= 15 THEN 'Paddy ' + CAST(n AS VARCHAR)
         WHEN n <= 35 THEN 'Rice ' + CAST(n-15 AS VARCHAR)
         ELSE 'By-Product ' + CAST(n-35 AS VARCHAR) END,
    CASE WHEN n <= 15 THEN 'Raw Material'
         WHEN n <= 35 THEN 'Finished Product'
         ELSE 'By-Product' END,
    CASE WHEN n <= 15 THEN 'Paddy'
         WHEN n <= 35 THEN 'Rice'
         ELSE 'Others' END,
    CASE WHEN n % 3 = 0 THEN 'Grade A'
         WHEN n % 3 = 1 THEN 'Grade B'
         ELSE 'Standard' END,
    'Product Description ' + CAST(n AS VARCHAR),
    'KG',
    20.0 + (n * 2.5),
    30.0 + (n * 3.0),
    100.0 + (n * 10),
    CASE WHEN n <= 15 THEN 1 ELSE 0 END,
    CASE WHEN n > 15 AND n <= 35 THEN 1 ELSE 0 END,
    CASE WHEN n > 35 THEN 1 ELSE 0 END,
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Products inserted: 50 records';
GO

-- ============================================
-- 2. CUSTOMERS (50 records)
-- ============================================
PRINT 'Inserting Customers...';

DELETE FROM Customers WHERE Id BETWEEN 1 AND 100;

INSERT INTO Customers (CustomerCode, CustomerName, CustomerType, Category, GSTIN, CreditLimit, CreditDays,
                       PaymentTerms, Status, CreatedDate, IsActive)
SELECT
    'CUST-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'Customer ' + CAST(n AS VARCHAR) + ' Pvt Ltd',
    CASE WHEN n % 3 = 0 THEN 'Wholesaler'
         WHEN n % 3 = 1 THEN 'Retailer'
         ELSE 'Distributor' END,
    CASE WHEN n % 2 = 0 THEN 'Regular' ELSE 'Premium' END,
    '29ABCDE' + RIGHT('0000' + CAST(n AS VARCHAR), 4) + 'F1Z5',
    50000.0 + (n * 1000),
    30 + (n % 60),
    CASE WHEN n % 2 = 0 THEN 'NET 30' ELSE 'NET 45' END,
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Customers inserted: 50 records';
GO

-- ============================================
-- 3. VENDORS (45 records)
-- ============================================
PRINT 'Inserting Vendors...';

DELETE FROM Vendors WHERE Id BETWEEN 1 AND 100;

INSERT INTO Vendors (VendorCode, VendorName, VendorType, Category, GSTIN, CreditLimit, CreditDays,
                     PaymentTerms, Status, CreatedDate, IsActive)
SELECT
    'VEN-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'Vendor ' + CAST(n AS VARCHAR) + ' Suppliers',
    CASE WHEN n % 3 = 0 THEN 'Farmer'
         WHEN n % 3 = 1 THEN 'Trader'
         ELSE 'Agent' END,
    CASE WHEN n % 2 = 0 THEN 'Local' ELSE 'Interstate' END,
    '29VEND' + RIGHT('00000' + CAST(n AS VARCHAR), 5) + 'Z1',
    100000.0 + (n * 2000),
    45 + (n % 45),
    'NET 60',
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Vendors inserted: 45 records';
GO

-- ============================================
-- 4. EMPLOYEES (40 records)
-- ============================================
PRINT 'Inserting Employees...';

DELETE FROM Employees WHERE Id BETWEEN 1 AND 100;

INSERT INTO Employees (EmployeeCode, EmployeeName, Department, Designation, Mobile, Email, DateOfJoining,
                       Address, City, State, BasicSalary, EmploymentType, Status, CreatedDate, IsActive)
SELECT
    'EMP-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'Employee ' + CAST(n AS VARCHAR),
    CASE WHEN n % 5 = 0 THEN 'Production'
         WHEN n % 5 = 1 THEN 'Quality'
         WHEN n % 5 = 2 THEN 'Warehouse'
         WHEN n % 5 = 3 THEN 'Sales'
         ELSE 'Admin' END,
    CASE WHEN n % 4 = 0 THEN 'Manager'
         WHEN n % 4 = 1 THEN 'Supervisor'
         WHEN n % 4 = 2 THEN 'Operator'
         ELSE 'Helper' END,
    '98765' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'emp' + CAST(n AS VARCHAR) + '@company.com',
    DATEADD(MONTH, -n, GETDATE()),
    'Address Line ' + CAST(n AS VARCHAR),
    'City ' + CAST(n % 10 AS VARCHAR),
    'Karnataka',
    15000.0 + (n * 500),
    CASE WHEN n % 2 = 0 THEN 'Permanent' ELSE 'Contract' END,
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Employees inserted: 40 records';
GO

-- ============================================
-- 5. WAREHOUSES (45 records)
-- ============================================
PRINT 'Inserting Warehouses...';

DELETE FROM Warehouses WHERE Id BETWEEN 1 AND 100;

INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, Address, City, State, Pincode,
                        TotalCapacity, AvailableCapacity, Status, CreatedDate, IsActive)
SELECT
    'WH-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'Warehouse ' + CAST(n AS VARCHAR),
    'Location ' + CAST(n AS VARCHAR),
    'Warehouse Address ' + CAST(n AS VARCHAR),
    'City ' + CAST(n % 15 AS VARCHAR),
    'Karnataka',
    '5600' + RIGHT('00' + CAST(n AS VARCHAR), 2),
    5000.0 + (n * 200),
    4000.0 + (n * 150),
    'Active',
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Warehouses inserted: 45 records';
GO

-- ============================================
-- 6. MACHINES (42 records)
-- ============================================
PRINT 'Inserting Machines...';

DELETE FROM Machines WHERE Id BETWEEN 1 AND 100;

INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, ModelNumber, Capacity, CapacityUnit,
                      PurchaseDate, PurchasePrice, Status, RunningHours, CreatedDate, IsActive)
SELECT
    'MCH-' + RIGHT('00000' + CAST(n AS VARCHAR), 5),
    'Machine ' + CAST(n AS VARCHAR),
    CASE WHEN n % 4 = 0 THEN 'Dryer'
         WHEN n % 4 = 1 THEN 'Huller'
         WHEN n % 4 = 2 THEN 'Polisher'
         ELSE 'Grader' END,
    'Manufacturer ' + CAST(n % 5 AS VARCHAR),
    'MOD-' + CAST(n AS VARCHAR),
    1000.0 + (n * 100),
    CASE WHEN n % 3 = 0 THEN 'KG/HR' WHEN n % 3 = 1 THEN 'TONS/DAY' ELSE 'BAGS/HR' END,
    DATEADD(MONTH, -n*2, GETDATE()),
    500000.0 + (n * 50000),
    'Active',
    1000.0 + (n * 100),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Machines inserted: 42 records';
GO

-- ============================================
-- 7. PRODUCTION ORDERS (45 records)
-- ============================================
PRINT 'Inserting Production Orders...';

DELETE FROM ProductionOrders WHERE Id BETWEEN 1 AND 100;

INSERT INTO ProductionOrders (OrderNumber, OrderDate, ProductId, Quantity, TargetDate,
                              Priority, Status, Remarks, CreatedDate, IsActive)
SELECT
    'PO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    DATEADD(DAY, -n, GETDATE()),
    16 + (n % 20),  -- Product IDs 16-35 (Rice products)
    1000.0 + (n * 50),
    DATEADD(DAY, -n+7, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'High' WHEN n % 3 = 1 THEN 'Medium' ELSE 'Low' END,
    CASE WHEN n % 4 = 0 THEN 'Completed'
         WHEN n % 4 = 1 THEN 'In Progress'
         WHEN n % 4 = 2 THEN 'Pending'
         ELSE 'Planned' END,
    'Production Order ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Orders inserted: 45 records';
GO

-- ============================================
-- 8. PRODUCTION BATCHES (48 records)
-- ============================================
PRINT 'Inserting Production Batches...';

DELETE FROM ProductionBatches WHERE Id BETWEEN 1 AND 100;

INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, ShiftType, OperatorId, SupervisorId,
                               Status, CompletionPercent, CreatedDate, IsActive)
SELECT
    'BATCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    1 + (n % 45),  -- Production Order IDs
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'Morning' WHEN n % 3 = 1 THEN 'Evening' ELSE 'Night' END,
    1 + (n % 40),  -- Operator Employee IDs
    1 + (n % 10),  -- Supervisor Employee IDs
    CASE WHEN n % 3 = 0 THEN 'Completed' WHEN n % 3 = 1 THEN 'In Progress' ELSE 'Started' END,
    CASE WHEN n % 3 = 0 THEN 100.0 WHEN n % 3 = 1 THEN 50.0 ELSE 10.0 END,
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Batches inserted: 48 records';
GO

-- ============================================
-- 9. PADDY PROCUREMENT (50 records)
-- ============================================
PRINT 'Inserting Paddy Procurement...';

DELETE FROM PaddyProcurement WHERE Id BETWEEN 1 AND 100;

INSERT INTO PaddyProcurement (ReceiptDate, VoucherNumber, SupplierName, PurchaseOrderNumber, PaddyVariety,
                              Grade, MoistureContent, QuantityReceived, TotalNetWeight, StorageLocation,
                              OpeningStock, ClosingStock, ResponsiblePerson, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'PROC-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Vendor ' + CAST(1 + (n % 45) AS VARCHAR) + ' Suppliers',
    'PO-PADDY-' + CAST(n AS VARCHAR),
    CASE WHEN n % 4 = 0 THEN 'Basmati'
         WHEN n % 4 = 1 THEN 'Sona Masuri'
         WHEN n % 4 = 2 THEN 'IR-64'
         ELSE 'Ponni' END,
    CASE WHEN n % 3 = 0 THEN 'Grade A' WHEN n % 3 = 1 THEN 'Grade B' ELSE 'Standard' END,
    14.0 + (n % 5),
    1000.0 + (n * 50),
    950.0 + (n * 48),
    'Warehouse ' + CAST(1 + (n % 45) AS VARCHAR),
    500.0 + (n * 25),
    1450.0 + (n * 73),
    'Employee ' + CAST(1 + (n % 40) AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Paddy Procurement inserted: 50 records';
GO

-- ============================================
-- 10. RICE SALES (50 records)
-- ============================================
PRINT 'Inserting Rice Sales...';

DELETE FROM RiceSales WHERE Id BETWEEN 1 AND 100;

INSERT INTO RiceSales (SaleDate, InvoiceNumber, CustomerId, ProductId, Quantity, UnitPrice, TotalAmount,
                       PaymentMode, PaymentStatus, DeliveryDate, DeliveryStatus, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'INV-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('0000' + CAST(n AS VARCHAR), 4),
    1 + (n % 50),  -- Customer IDs
    16 + (n % 20), -- Rice Product IDs (16-35)
    100.0 + (n * 10),
    50.0 + (n * 2.5),
    (100.0 + (n * 10)) * (50.0 + (n * 2.5)),
    CASE WHEN n % 3 = 0 THEN 'Cash' WHEN n % 3 = 1 THEN 'Credit' ELSE 'Online' END,
    CASE WHEN n % 2 = 0 THEN 'Paid' ELSE 'Pending' END,
    DATEADD(DAY, -n+2, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'Delivered' WHEN n % 3 = 1 THEN 'In Transit' ELSE 'Pending' END,
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Rice Sales inserted: 50 records';
GO

-- ============================================
-- 11. BY-PRODUCT SALES (45 records)
-- ============================================
PRINT 'Inserting By-Product Sales...';

DELETE FROM ByProductSales WHERE Id BETWEEN 1 AND 100;

INSERT INTO ByProductSales (SaleDate, InvoiceNumber, BuyerName, BuyerAddress, ProductType, Quantity,
                            UnitPrice, TotalAmount, PaymentMode, PaymentStatus, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'BP-INV-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + RIGHT('000' + CAST(n AS VARCHAR), 3),
    'Buyer ' + CAST(n AS VARCHAR),
    'Address ' + CAST(n AS VARCHAR),
    CASE WHEN n % 3 = 0 THEN 'Rice Bran' WHEN n % 3 = 1 THEN 'Rice Husk' ELSE 'Broken Rice' END,
    500.0 + (n * 25),
    5.0 + (n * 0.5),
    (500.0 + (n * 25)) * (5.0 + (n * 0.5)),
    CASE WHEN n % 2 = 0 THEN 'Cash' ELSE 'Credit' END,
    CASE WHEN n % 2 = 0 THEN 'Paid' ELSE 'Pending' END,
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ By-Product Sales inserted: 45 records';
GO

-- ============================================
-- 12. Continue with remaining tables...
-- ============================================

-- INQUIRIES
DELETE FROM Inquiries WHERE Id BETWEEN 1 AND 100;
INSERT INTO Inquiries (InquiryNumber, InquiryDate, CustomerId, ProductId, Quantity, ExpectedPrice, Status,
                       FollowUpDate, Remarks, CreatedDate, IsActive)
SELECT
    'INQ-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1 + (n % 50),
    1 + (n % 50),
    100.0 + (n * 10),
    50.0 + (n * 2),
    CASE WHEN n % 4 = 0 THEN 'New' WHEN n % 4 = 1 THEN 'In Progress'
         WHEN n % 4 = 2 THEN 'Quoted' ELSE 'Converted' END,
    DATEADD(DAY, -n+3, GETDATE()),
    'Inquiry ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n, GETDATE()),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;
PRINT '✓ Inquiries inserted: 45 records';
GO

PRINT '';
PRINT '========================================';
PRINT 'DATA INSERTION COMPLETE!';
PRINT '========================================';
PRINT '';

-- Show summary
SELECT
    'Products' AS TableName, COUNT(*) AS RecordCount FROM Products
UNION ALL SELECT 'Customers', COUNT(*) FROM Customers
UNION ALL SELECT 'Vendors', COUNT(*) FROM Vendors
UNION ALL SELECT 'Employees', COUNT(*) FROM Employees
UNION ALL SELECT 'Warehouses', COUNT(*) FROM Warehouses
UNION ALL SELECT 'Machines', COUNT(*) FROM Machines
UNION ALL SELECT 'ProductionOrders', COUNT(*) FROM ProductionOrders
UNION ALL SELECT 'ProductionBatches', COUNT(*) FROM ProductionBatches
UNION ALL SELECT 'PaddyProcurement', COUNT(*) FROM PaddyProcurement
UNION ALL SELECT 'RiceSales', COUNT(*) FROM RiceSales
UNION ALL SELECT 'ByProductSales', COUNT(*) FROM ByProductSales
UNION ALL SELECT 'Inquiries', COUNT(*) FROM Inquiries;
GO
