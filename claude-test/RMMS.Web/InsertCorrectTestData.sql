-- Insert Test Data with CORRECT Column Names
-- 40 records for each remaining table

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Inserting test data with correct schema';
PRINT '========================================';
GO

-- Create numbers table
IF OBJECT_ID('tempdb..#Numbers') IS NOT NULL DROP TABLE #Numbers;
CREATE TABLE #Numbers (N INT);
INSERT INTO #Numbers (N)
VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),
       (11),(12),(13),(14),(15),(16),(17),(18),(19),(20),
       (21),(22),(23),(24),(25),(26),(27),(28),(29),(30),
       (31),(32),(33),(34),(35),(36),(37),(38),(39),(40);
GO

--============================================
-- 1. BY-PRODUCT SALES - 40 records
--============================================
PRINT 'Inserting By-Product Sales...';

INSERT INTO ByProductSales
(SaleDate, InvoiceNumber, BuyerName, BuyerAddress, ProductType, Quantity, UnitPrice, TotalAmount,
 PaymentMode, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'BPS-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    'Buyer ' + CAST(N AS VARCHAR),
    'Address ' + CAST(N AS VARCHAR),
    CASE (N % 4) WHEN 0 THEN 'Rice Bran' WHEN 1 THEN 'Rice Husk' WHEN 2 THEN 'Broken Rice' ELSE 'Rice Powder' END,
    200 + (N * 15),
    15 + (N % 8),
    (200 + (N * 15)) * (15 + (N % 8)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    'Test by-product sale ' + CAST(N AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ By-Product Sales: 40 records inserted';
GO

--============================================
-- 2. EXTERNAL RICE SALES - 40 records
--============================================
PRINT 'Inserting External Rice Sales...';

INSERT INTO ExternalRiceSales
(SaleDate, ItemDescription, SoldTo, SoldBy, Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus,
 BalanceAmount, ClearanceDate, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    CASE (N % 4) WHEN 0 THEN 'Premium Rice' WHEN 1 THEN 'Standard Rice' WHEN 2 THEN 'Economy Rice' ELSE 'Special Grade' END,
    'Customer ' + CAST(N AS VARCHAR),
    'Sales Person ' + CAST(N AS VARCHAR),
    600 + (N * 40),
    45 + (N % 12),
    (600 + (N * 40)) * (45 + (N % 12)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Pending' ELSE 'Partial' END,
    CASE (N % 3) WHEN 0 THEN 0 ELSE ((600 + (N * 40)) * (45 + (N % 12)) * 0.4) END,
    NULL,
    'Test external rice sale ' + CAST(N AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ External Rice Sales: 40 records inserted';
GO

--============================================
-- 3. RICE PROCUREMENT EXTERNAL - 40 records
--============================================
PRINT 'Inserting Rice Procurement External...';

INSERT INTO RiceProcurementExternal
(ProcurementDate, ItemDescription, ProcuredFrom, ProcuredBy, Quantity, Rate, TotalAmount, PaymentMode,
 PaymentStatus, BalanceAmount, ClearanceDate, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    CASE (N % 4) WHEN 0 THEN 'Mansuri' WHEN 1 THEN 'Katrni' WHEN 2 THEN 'Sonam' ELSE 'Premium Variety' END,
    'Supplier ' + CAST(N AS VARCHAR),
    'Buyer ' + CAST(N AS VARCHAR),
    500 + (N * 25),
    40 + (N % 10),
    (500 + (N * 25)) * (40 + (N % 10)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Pending' ELSE 'Partial' END,
    CASE (N % 3) WHEN 0 THEN 0 ELSE ((500 + (N * 25)) * (40 + (N % 10)) * 0.3) END,
    NULL,
    'Test rice procurement ' + CAST(N AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Rice Procurement External: 40 records inserted';
GO

--============================================
-- 4. LOANS & ADVANCES - 40 records
--============================================
PRINT 'Inserting Loans & Advances...';

INSERT INTO LoansAdvances
(TransactionDate, VoucherNumber, Particulars, PartyName, PartyType, AmountGiven, Repayment, RepaymentDate,
 Balance, InterestRate, InterestAmount, Status, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'LA-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 2) WHEN 0 THEN 'Advance to employee' ELSE 'Loan taken from party' END,
    'Party ' + CAST(N AS VARCHAR),
    CASE (N % 2) WHEN 0 THEN 'Employee' ELSE 'Creditor' END,
    10000 + (N * 1000),
    CASE (N % 3) WHEN 0 THEN (10000 + (N * 1000)) WHEN 1 THEN 0 ELSE ((10000 + (N * 1000)) * 0.5) END,
    CASE (N % 3) WHEN 0 THEN DATEADD(DAY, -N + 10, GETDATE()) ELSE NULL END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (10000 + (N * 1000)) ELSE ((10000 + (N * 1000)) * 0.5) END,
    8.5,
    (10000 + (N * 1000)) * 0.085,
    CASE (N % 3) WHEN 0 THEN 'Closed' WHEN 1 THEN 'Active' ELSE 'Partial' END,
    'Test loan/advance ' + CAST(N AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Loans & Advances: 40 records inserted';
GO

--============================================
-- 5. FIXED ASSETS - 40 records
--============================================
PRINT 'Inserting Fixed Assets...';

INSERT INTO FixedAssets
(AssetCode, PurchaseDate, AssetName, Description, Supplier, PurchaseValue, DepreciationRate,
 AccumulatedDepreciation, NetBookValue, PresentValueApprox, AssetStatus, Location, ResponsiblePerson,
 CreatedBy, CreatedDate, IsActive)
SELECT
    'ASSET-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    DATEADD(DAY, -(N * 10), GETDATE()),
    CASE (N % 5) WHEN 0 THEN 'Milling Machine' WHEN 1 THEN 'Vehicle' WHEN 2 THEN 'Office Equipment' WHEN 3 THEN 'Storage Tank' ELSE 'Weighing Scale' END + ' ' + CAST(N AS VARCHAR),
    'Test asset for operations',
    'Supplier ' + CAST(N AS VARCHAR),
    50000 + (N * 5000),
    10.0,
    (50000 + (N * 5000)) * 0.15,
    (50000 + (N * 5000)) * 0.85,
    (50000 + (N * 5000)) * 0.80,
    CASE (N % 3) WHEN 0 THEN 'Active' WHEN 1 THEN 'Under Maintenance' ELSE 'Active' END,
    'Location ' + CAST((N % 5) + 1 AS VARCHAR),
    'Manager ' + CAST((N % 3) + 1 AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Fixed Assets: 40 records inserted';
GO

--============================================
-- 6. VOUCHERS - 40 records
--============================================
PRINT 'Inserting Vouchers...';

INSERT INTO Vouchers
(VoucherDate, VoucherNumber, VoucherType, Particulars, Amount, DebitAccount, CreditAccount,
 Narration, ApprovedBy, ApprovalStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'VCH-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 4) WHEN 0 THEN 'Payment' WHEN 1 THEN 'Receipt' WHEN 2 THEN 'Journal' ELSE 'Contra' END,
    'Test voucher entry ' + CAST(N AS VARCHAR),
    3000 + (N * 400),
    'Debit Account ' + CAST(N AS VARCHAR),
    'Credit Account ' + CAST(N AS VARCHAR),
    'Narration for voucher ' + CAST(N AS VARCHAR),
    'Manager',
    CASE (N % 2) WHEN 0 THEN 'Approved' ELSE 'Pending' END,
    'Test voucher ' + CAST(N AS VARCHAR),
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Vouchers: 40 records inserted';
GO

--============================================
-- 7. RECEIVABLES OVERDUE - 40 records
--============================================
PRINT 'Inserting Receivables Overdue...';

INSERT INTO ReceivablesOverdue
(InvoiceDate, InvoiceNumber, CustomerName, ItemSupplied, InvoiceAmount, AmountReceived, BalanceDue,
 DueDate, DaysOverdue, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(N + 30), GETDATE()),
    'RO-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    'Customer ' + CAST(N AS VARCHAR),
    CASE (N % 4) WHEN 0 THEN 'Premium Rice 500kg' WHEN 1 THEN 'Standard Rice 800kg' WHEN 2 THEN 'Broken Rice 200kg' ELSE 'Rice Bran 300kg' END,
    5000 + (N * 500),
    CASE (N % 3) WHEN 0 THEN (5000 + (N * 500)) WHEN 1 THEN 0 ELSE ((5000 + (N * 500)) * 0.6) END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (5000 + (N * 500)) ELSE ((5000 + (N * 500)) * 0.4) END,
    DATEADD(DAY, -N, GETDATE()),
    N,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Overdue' ELSE 'Partial' END,
    'Test receivable overdue ' + CAST(N AS VARCHAR) + ' days',
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Receivables Overdue: 40 records inserted';
GO

--============================================
-- 8. PAYABLES OVERDUE - 40 records
--============================================
PRINT 'Inserting Payables Overdue...';

INSERT INTO PayablesOverdue
(PurchaseDate, InvoiceNumber, SupplierName, ItemPurchased, InvoiceAmount, AmountPaid, BalancePayable,
 DueDate, DaysOverdue, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(N + 30), GETDATE()),
    'PO-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    'Supplier ' + CAST(N AS VARCHAR),
    CASE (N % 4) WHEN 0 THEN 'Paddy 1000kg' WHEN 1 THEN 'Rice 600kg' WHEN 2 THEN 'Packaging Material' ELSE 'Transport Services' END,
    7000 + (N * 600),
    CASE (N % 3) WHEN 0 THEN (7000 + (N * 600)) WHEN 1 THEN 0 ELSE ((7000 + (N * 600)) * 0.7) END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (7000 + (N * 600)) ELSE ((7000 + (N * 600)) * 0.3) END,
    DATEADD(DAY, -N, GETDATE()),
    N,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Overdue' ELSE 'Partial' END,
    'Test payable overdue ' + CAST(N AS VARCHAR) + ' days',
    'TestUser',
    GETDATE(),
    1
FROM #Numbers;
PRINT '✓ Payables Overdue: 40 records inserted';
GO

-- Clean up
DROP TABLE #Numbers;
GO

PRINT '';
PRINT '========================================';
PRINT 'SUCCESS! All test data inserted!';
PRINT '========================================';
GO

-- Final verification
SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS RecordCount FROM PaddyProcurement WHERE IsActive = 1
UNION ALL
SELECT 'RiceSales', COUNT(*) FROM RiceSales WHERE IsActive = 1
UNION ALL
SELECT 'RiceProcurementExternal', COUNT(*) FROM RiceProcurementExternal WHERE IsActive = 1
UNION ALL
SELECT 'ByProductSales', COUNT(*) FROM ByProductSales WHERE IsActive = 1
UNION ALL
SELECT 'ExternalRiceSales', COUNT(*) FROM ExternalRiceSales WHERE IsActive = 1
UNION ALL
SELECT 'BankTransactions', COUNT(*) FROM BankTransactions WHERE IsActive = 1
UNION ALL
SELECT 'CashBook', COUNT(*) FROM CashBook WHERE IsActive = 1
UNION ALL
SELECT 'Vouchers', COUNT(*) FROM Vouchers WHERE IsActive = 1
UNION ALL
SELECT 'LoansAdvances', COUNT(*) FROM LoansAdvances WHERE IsActive = 1
UNION ALL
SELECT 'FixedAssets', COUNT(*) FROM FixedAssets WHERE IsActive = 1
UNION ALL
SELECT 'ReceivablesOverdue', COUNT(*) FROM ReceivablesOverdue WHERE IsActive = 1
UNION ALL
SELECT 'PayablesOverdue', COUNT(*) FROM PayablesOverdue WHERE IsActive = 1
ORDER BY TableName;
GO
