-- Verify all test data exists
USE RMMS_Production;
GO

PRINT 'Verifying test data in all tables...';
PRINT '====================================';

-- 1. By-Product Sales
SELECT 'ByProductSales' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(SaleDate) AS OldestDate, MAX(SaleDate) AS NewestDate
FROM ByProductSales;

-- 2. External Rice Sales
SELECT 'ExternalRiceSales' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(SaleDate) AS OldestDate, MAX(SaleDate) AS NewestDate
FROM ExternalRiceSales;

-- 3. Rice Procurement External
SELECT 'RiceProcurementExternal' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(ProcurementDate) AS OldestDate, MAX(ProcurementDate) AS NewestDate
FROM RiceProcurementExternal;

-- 4. Loans & Advances
SELECT 'LoansAdvances' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(TransactionDate) AS OldestDate, MAX(TransactionDate) AS NewestDate
FROM LoansAdvances;

-- 5. Fixed Assets
SELECT 'FixedAssets' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(PurchaseDate) AS OldestDate, MAX(PurchaseDate) AS NewestDate
FROM FixedAssets;

-- 6. Vouchers
SELECT 'Vouchers' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(VoucherDate) AS OldestDate, MAX(VoucherDate) AS NewestDate
FROM Vouchers;

-- 7. Receivables Overdue
SELECT 'ReceivablesOverdue' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(InvoiceDate) AS OldestDate, MAX(InvoiceDate) AS NewestDate
FROM ReceivablesOverdue;

-- 8. Payables Overdue
SELECT 'PayablesOverdue' AS TableName, COUNT(*) AS Total,
       COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS Active,
       MIN(PurchaseDate) AS OldestDate, MAX(PurchaseDate) AS NewestDate
FROM PayablesOverdue;

-- Show sample records from ByProductSales
PRINT '';
PRINT 'Sample ByProductSales records:';
SELECT TOP 5 Id, SaleDate, InvoiceNumber, BuyerName, ProductType, Quantity, TotalAmount, IsActive, CreatedBy
FROM ByProductSales
ORDER BY Id DESC;

-- Show sample from ExternalRiceSales
PRINT '';
PRINT 'Sample ExternalRiceSales records:';
SELECT TOP 5 Id, SaleDate, ItemDescription, SoldTo, Quantity, TotalAmount, IsActive, CreatedBy
FROM ExternalRiceSales
ORDER BY Id DESC;

GO
