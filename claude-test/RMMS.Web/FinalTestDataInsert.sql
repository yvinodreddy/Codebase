-- Final Test Data Insert - Using simple numbered approach
-- Inserts 40 test records for each table

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'RMMS Test Data Insertion';
PRINT 'Inserting 40 records per table...';
PRINT '========================================';
GO

-- Create a numbers table for generating test data
IF OBJECT_ID('tempdb..#Numbers') IS NOT NULL DROP TABLE #Numbers;
CREATE TABLE #Numbers (N INT);

INSERT INTO #Numbers (N)
VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),
       (11),(12),(13),(14),(15),(16),(17),(18),(19),(20),
       (21),(22),(23),(24),(25),(26),(27),(28),(29),(30),
       (31),(32),(33),(34),(35),(36),(37),(38),(39),(40);
GO

--============================================
-- 1. PADDY PROCUREMENT
--============================================
PRINT 'Inserting Paddy Procurement records...';

INSERT INTO PaddyProcurement
(ReceiptDate, VoucherNumber, SupplierName, PurchaseOrderNumber, PaddyVariety, Grade, MoistureContent,
 QuantityReceived, WeightPerBag, TotalNetWeight, StorageDate, StorageLocation, OpeningStock, Issues,
 ClosingStock, LossShrinkage, Remarks, ResponsiblePerson, CreatedDate, CreatedBy, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'PP-TEST-' + RIGHT('0000' + CAST(N + 200 AS VARCHAR), 4),
    'Test Supplier ' + CAST(N AS VARCHAR),
    NULL,
    CASE (N % 5) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masuri' WHEN 2 THEN 'IR-64' WHEN 3 THEN 'Swarna' ELSE 'Ponni' END,
    CASE (N % 3) WHEN 0 THEN 'Grade A' WHEN 1 THEN 'Grade B' ELSE 'Grade C' END,
    12.5,
    1000 + (N * 50),
    50.0,
    1050 + (N * 50),
    DATEADD(DAY, -N, GETDATE()),
    'Warehouse ' + CAST((N % 5) + 1 AS VARCHAR),
    0, 0,
    1000 + (N * 50),
    0,
    'Test data for paging - record ' + CAST(N AS VARCHAR),
    'Test Manager',
    GETDATE(),
    'TestScript',
    1
FROM #Numbers;

PRINT 'Paddy Procurement: 40 records inserted';
GO

--============================================
-- 2. RICE SALES
--============================================
PRINT 'Inserting Rice Sales records...';

INSERT INTO RiceSales
(SaleDate, InvoiceNumber, BuyerName, BuyerAddress, BuyerGSTIN, RiceGrade, Quantity, UnitPrice,
 TotalInvoiceValue, Discount, TaxableValue, CGSTAmount, SGSTAmount, IGSTAmount, TotalTaxAmount,
 FreightCharges, OtherCharges, GrossInvoiceAmount, PaymentMode, DueDate, PaymentStatus, Remarks,
 CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'RS-TEST-' + RIGHT('0000' + CAST(N + 200 AS VARCHAR), 4),
    'Test Customer ' + CAST(N AS VARCHAR),
    'Test Address ' + CAST(N AS VARCHAR),
    '27AAACR5055K1Z' + CAST(N AS VARCHAR),
    CASE (N % 3) WHEN 0 THEN 'Premium' WHEN 1 THEN 'Standard' ELSE 'Economy' END,
    800 + (N * 30),
    50 + (N % 15),
    (800 + (N * 30)) * (50 + (N % 15)),
    0,
    (800 + (N * 30)) * (50 + (N % 15)),
    (800 + (N * 30)) * (50 + (N % 15)) * 0.025,
    (800 + (N * 30)) * (50 + (N % 15)) * 0.025,
    0,
    (800 + (N * 30)) * (50 + (N % 15)) * 0.05,
    100, 50,
    (800 + (N * 30)) * (50 + (N % 15)) * 1.05 + 150,
    CASE (N % 3) WHEN 0 THEN 'Cash' WHEN 1 THEN 'Online' ELSE 'Cheque' END,
    DATEADD(DAY, 30 - N, GETDATE()),
    CASE (N % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    'Test sales for paging - record ' + CAST(N AS VARCHAR),
    'TestScript',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Rice Sales: 40 records inserted';
GO

--============================================
-- 3. BY-PRODUCT SALES
--============================================
PRINT 'Inserting By-Product Sales records...';

INSERT INTO ByProductSales
(SaleDate, TransactionNumber, ProductType, BuyerName, BuyerContact, Quantity, Rate, TotalAmount,
 PaymentMode, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'BPS-TEST-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 4) WHEN 0 THEN 'Rice Bran' WHEN 1 THEN 'Rice Husk' WHEN 2 THEN 'Broken Rice' ELSE 'Rice Powder' END,
    'Test Buyer ' + CAST(N AS VARCHAR),
    '9876543' + RIGHT('000' + CAST(N AS VARCHAR), 3),
    200 + (N * 15),
    15 + (N % 8),
    (200 + (N * 15)) * (15 + (N % 8)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    'Test by-product for paging - record ' + CAST(N AS VARCHAR),
    'TestScript',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'By-Product Sales: 40 records inserted';
GO

--============================================
-- 4. BANK TRANSACTIONS
--============================================
PRINT 'Inserting Bank Transactions records...';

INSERT INTO BankTransactions
(TransactionDate, ChequeUtrNumber, BankName, AccountNumber, Particulars, Deposits, Withdrawals, Balance, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'CHQ' + RIGHT('000000' + CAST(N AS VARCHAR), 6),
    CASE (N % 3) WHEN 0 THEN 'State Bank' WHEN 1 THEN 'HDFC Bank' ELSE 'ICICI Bank' END,
    'ACC100' + CAST((N % 5) + 1 AS VARCHAR),
    CASE WHEN (N % 2) = 0 THEN 'Customer Payment' ELSE 'Supplier Payment' END,
    CASE WHEN (N % 2) = 0 THEN (5000 + (N * 500)) ELSE 0 END,
    CASE WHEN (N % 2) = 1 THEN (5000 + (N * 500)) ELSE 0 END,
    50000,
    'Test bank transaction for paging - record ' + CAST(N AS VARCHAR),
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Bank Transactions: 40 records inserted';
GO

--============================================
-- 5. CASH BOOK
--============================================
PRINT 'Inserting Cash Book records...';

INSERT INTO CashBook
(TransactionDate, VoucherNumber, Particulars, Receipts, Payments, Balance, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'CB-TEST-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE WHEN (N % 2) = 0 THEN 'Cash Receipt' ELSE 'Cash Payment' END,
    CASE WHEN (N % 2) = 0 THEN (2000 + (N * 300)) ELSE 0 END,
    CASE WHEN (N % 2) = 1 THEN (2000 + (N * 300)) ELSE 0 END,
    20000,
    'Test cash book for paging - record ' + CAST(N AS VARCHAR),
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Cash Book: 40 records inserted';
GO

-- Clean up
DROP TABLE #Numbers;
GO

PRINT '========================================';
PRINT 'INSERTION COMPLETE!';
PRINT 'Verifying record counts...';
PRINT '========================================';
GO

-- Verify
SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS Total FROM PaddyProcurement WHERE IsActive = 1
UNION ALL
SELECT 'RiceSales', COUNT(*) FROM RiceSales WHERE IsActive = 1
UNION ALL
SELECT 'ByProductSales', COUNT(*) FROM ByProductSales WHERE IsActive = 1
UNION ALL
SELECT 'BankTransactions', COUNT(*) FROM BankTransactions WHERE IsActive = 1
UNION ALL
SELECT 'CashBook', COUNT(*) FROM CashBook WHERE IsActive = 1
ORDER BY TableName;
GO
