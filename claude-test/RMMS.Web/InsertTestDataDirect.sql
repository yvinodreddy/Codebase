-- Direct INSERT Test Data for RMMS System
-- 40 records for each table

USE RMMS_Production;
GO

PRINT 'Starting direct INSERT test data...';
GO

-- First, let's check if tables exist and get sample data structure
-- We'll insert records directly using INSERT INTO statements

--============================================
-- 1. PADDY PROCUREMENT - 38 more records (already has 2+40 = 42)
--============================================
PRINT 'Inserting additional Paddy Procurement records via direct INSERT...';

INSERT INTO PaddyProcurement
(ReceiptDate, VoucherNumber, SupplierName, PurchaseOrderNumber, PaddyVariety, Grade, MoistureContent,
 QuantityReceived, WeightPerBag, TotalNetWeight, StorageDate, StorageLocation, OpeningStock, Issues,
 ClosingStock, LossShrinkage, Remarks, ResponsiblePerson, CreatedDate, CreatedBy, IsActive)
SELECT
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS ReceiptDate,
    'PP-2024-' + RIGHT('0000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) + 100 AS VARCHAR), 4) AS VoucherNumber,
    'Test Supplier ' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR) AS SupplierName,
    NULL AS PurchaseOrderNumber,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5)
        WHEN 0 THEN 'Basmati'
        WHEN 1 THEN 'Sona Masuri'
        WHEN 2 THEN 'IR-64'
        WHEN 3 THEN 'Swarna'
        ELSE 'Ponni'
    END AS PaddyVariety,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3)
        WHEN 0 THEN 'Grade A'
        WHEN 1 THEN 'Grade B'
        ELSE 'Grade C'
    END AS Grade,
    12.5 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3) AS MoistureContent,
    1000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 50) AS QuantityReceived,
    50.0 AS WeightPerBag,
    1000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 50) AS TotalNetWeight,
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS StorageDate,
    'Warehouse ' + CAST((ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5) + 1 AS VARCHAR) AS StorageLocation,
    0 AS OpeningStock,
    0 AS Issues,
    1000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 50) AS ClosingStock,
    0 AS LossShrinkage,
    'Test data record for paging' AS Remarks,
    'Test Manager' AS ResponsiblePerson,
    GETDATE() AS CreatedDate,
    'TestDataScript' AS CreatedBy,
    1 AS IsActive
FROM sys.all_objects
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) AS n
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 38;

PRINT 'Paddy Procurement: Additional records inserted';
GO

--============================================
-- 2. RICE SALES - 39 more records (already has 1)
--============================================
PRINT 'Inserting Rice Sales records via direct INSERT...';

INSERT INTO RiceSales
(SaleDate, InvoiceNumber, BuyerName, BuyerAddress, BuyerGSTIN, RiceGrade, Quantity, UnitPrice,
 TotalInvoiceValue, Discount, TaxableValue, CGSTAmount, SGSTAmount, IGSTAmount, TotalTaxAmount,
 FreightCharges, OtherCharges, GrossInvoiceAmount, PaymentMode, DueDate, PaymentStatus, Remarks,
 CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS SaleDate,
    'RS-INV-2024-' + RIGHT('0000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) + 100 AS VARCHAR), 4) AS InvoiceNumber,
    'Test Customer ' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR) AS BuyerName,
    'Test Address Line ' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR) AS BuyerAddress,
    '27AAACR5055K1Z' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR) AS BuyerGSTIN,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3)
        WHEN 0 THEN 'Premium'
        WHEN 1 THEN 'Standard'
        ELSE 'Economy'
    END AS RiceGrade,
    800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30) AS Quantity,
    50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15) AS UnitPrice,
    (800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15)) AS TotalInvoiceValue,
    0 AS Discount,
    (800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15)) AS TaxableValue,
    ((800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15))) * 0.025 AS CGSTAmount,
    ((800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15))) * 0.025 AS SGSTAmount,
    0 AS IGSTAmount,
    ((800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15))) * 0.05 AS TotalTaxAmount,
    100 AS FreightCharges,
    50 AS OtherCharges,
    ((800 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 30)) * (50 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 15))) * 1.05 + 150 AS GrossInvoiceAmount,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3)
        WHEN 0 THEN 'Cash'
        WHEN 1 THEN 'Online'
        ELSE 'Cheque'
    END AS PaymentMode,
    DATEADD(DAY, 30 - ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS DueDate,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending'
    END AS PaymentStatus,
    'Test sales record for paging' AS Remarks,
    'TestDataScript' AS CreatedBy,
    GETDATE() AS CreatedDate,
    1 AS IsActive
FROM sys.all_objects
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) AS n
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 39;

PRINT 'Rice Sales: 39 additional records inserted';
GO

--============================================
-- 3. BY-PRODUCT SALES - 40 records
--============================================
PRINT 'Inserting By-Product Sales records via direct INSERT...';

INSERT INTO ByProductSales
(SaleDate, TransactionNumber, ProductType, BuyerName, BuyerContact, Quantity, Rate, TotalAmount,
 PaymentMode, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS SaleDate,
    'BPS-2024-' + RIGHT('0000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 4) AS TransactionNumber,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 4)
        WHEN 0 THEN 'Rice Bran'
        WHEN 1 THEN 'Rice Husk'
        WHEN 2 THEN 'Broken Rice'
        ELSE 'Rice Powder'
    END AS ProductType,
    'Test Buyer ' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR) AS BuyerName,
    '9876543' + RIGHT('000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 3) AS BuyerContact,
    200 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 15) AS Quantity,
    15 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 8) AS Rate,
    (200 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 15)) * (15 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 8)) AS TotalAmount,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2)
        WHEN 0 THEN 'Cash'
        ELSE 'Online'
    END AS PaymentMode,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2)
        WHEN 0 THEN 'Paid'
        ELSE 'Pending'
    END AS PaymentStatus,
    'Test by-product sale for paging' AS Remarks,
    'TestDataScript' AS CreatedBy,
    GETDATE() AS CreatedDate,
    1 AS IsActive
FROM sys.all_objects
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) AS n
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 40;

PRINT 'By-Product Sales: 40 records inserted';
GO

--============================================
-- 4. BANK TRANSACTIONS - 40 records
--============================================
PRINT 'Inserting Bank Transaction records via direct INSERT...';

INSERT INTO BankTransactions
(TransactionDate, ChequeUtrNumber, BankName, AccountNumber, Particulars, Deposits, Withdrawals, Balance, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS TransactionDate,
    'CHQ' + RIGHT('000000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 6) AS ChequeUtrNumber,
    CASE (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 3)
        WHEN 0 THEN 'State Bank'
        WHEN 1 THEN 'HDFC Bank'
        ELSE 'ICICI Bank'
    END AS BankName,
    'ACC100' + CAST((ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 5) + 1 AS VARCHAR) AS AccountNumber,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 0 THEN 'Customer Payment' ELSE 'Supplier Payment' END AS Particulars,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 0 THEN (5000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 500)) ELSE 0 END AS Deposits,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 1 THEN (5000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 500)) ELSE 0 END AS Withdrawals,
    50000 AS Balance,
    'Test bank transaction for paging' AS Remarks,
    GETDATE() AS CreatedDate,
    1 AS IsActive
FROM sys.all_objects
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) AS n
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 40;

PRINT 'Bank Transactions: 40 records inserted';
GO

--============================================
-- 5. CASH BOOK - 40 records
--============================================
PRINT 'Inserting Cash Book records via direct INSERT...';

INSERT INTO CashBook
(TransactionDate, VoucherNumber, Particulars, Receipts, Payments, Balance, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -ROW_NUMBER() OVER (ORDER BY (SELECT NULL)), GETDATE()) AS TransactionDate,
    'CB-2024-' + RIGHT('0000' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR), 4) AS VoucherNumber,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 0 THEN 'Cash Receipt' ELSE 'Cash Payment' END AS Particulars,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 0 THEN (2000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 300)) ELSE 0 END AS Receipts,
    CASE WHEN (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) % 2) = 1 THEN (2000 + (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) * 300)) ELSE 0 END AS Payments,
    20000 AS Balance,
    'Test cash book entry for paging' AS Remarks,
    GETDATE() AS CreatedDate,
    1 AS IsActive
FROM sys.all_objects
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) AS n
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 40;

PRINT 'Cash Book: 40 records inserted';
GO

PRINT '========================================';
PRINT 'TEST DATA INSERTION COMPLETED!';
PRINT 'Verifying counts...';
GO

-- Verify counts
SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS RecordCount FROM PaddyProcurement WHERE IsActive = 1
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

PRINT '========================================';
PRINT 'You can now test paging functionality!';
PRINT '========================================';
GO
