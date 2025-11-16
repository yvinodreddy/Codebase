-- Insert Test Data for ALL Remaining Tables
-- 40 records for each table

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Inserting 40 records for ALL tables...';
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
PRINT 'Inserting By-Product Sales records...';

INSERT INTO ByProductSales
(SaleDate, TransactionNumber, ProductType, BuyerName, BuyerContact, Quantity, Rate, TotalAmount,
 PaymentMode, PaymentStatus, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'BPS-TEST-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 4)
        WHEN 0 THEN 'Rice Bran'
        WHEN 1 THEN 'Rice Husk'
        WHEN 2 THEN 'Broken Rice'
        ELSE 'Rice Powder'
    END,
    'Test Buyer ' + CAST(N AS VARCHAR),
    '9876543' + RIGHT('000' + CAST(N AS VARCHAR), 3),
    200 + (N * 15),
    15 + (N % 8),
    (200 + (N * 15)) * (15 + (N % 8)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
    'Test by-product sale - record ' + CAST(N AS VARCHAR),
    'TestScript',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'By-Product Sales: 40 records inserted';
GO

--============================================
-- 2. EXTERNAL RICE SALES - 40 records
--============================================
PRINT 'Inserting External Rice Sales records...';

INSERT INTO ExternalRiceSales
(Date, ItemDescription, SoldTo, SoldBy, Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus,
 Balance, FullPaymentClearanceDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    CASE (N % 4)
        WHEN 0 THEN 'Premium Rice'
        WHEN 1 THEN 'Standard Rice'
        WHEN 2 THEN 'Economy Rice'
        ELSE 'Special Grade'
    END,
    'Test PAC/Customer ' + CAST(N AS VARCHAR),
    'Sales Person ' + CAST(N AS VARCHAR),
    600 + (N * 40),
    45 + (N % 12),
    (600 + (N * 40)) * (45 + (N % 12)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Pending' ELSE 'Partial' END,
    CASE (N % 3) WHEN 0 THEN 0 ELSE ((600 + (N * 40)) * (45 + (N % 12)) * 0.4) END,
    NULL,
    'Test external rice sale - record ' + CAST(N AS VARCHAR),
    GETDATE(),
    1
FROM #Numbers;

PRINT 'External Rice Sales: 40 records inserted';
GO

--============================================
-- 3. RICE PROCUREMENT EXTERNAL - 40 records
--============================================
PRINT 'Inserting Rice Procurement External records...';

INSERT INTO RiceProcurementExternal
(Date, ItemDescription, ProcuredFrom, ProcuredBy, Quantity, Rate, TotalAmount, PaymentMode,
 PaymentStatus, Balance, FullPaymentDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    CASE (N % 4)
        WHEN 0 THEN 'Mansuri Rice'
        WHEN 1 THEN 'Katrni Rice'
        WHEN 2 THEN 'Sonam Rice'
        ELSE 'Premium Variety'
    END,
    'Test Supplier/Mill ' + CAST(N AS VARCHAR),
    'Procurement Officer ' + CAST(N AS VARCHAR),
    500 + (N * 25),
    40 + (N % 10),
    (500 + (N * 25)) * (40 + (N % 10)),
    CASE (N % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
    CASE (N % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Pending' ELSE 'Partial' END,
    CASE (N % 3) WHEN 0 THEN 0 ELSE ((500 + (N * 25)) * (40 + (N % 10)) * 0.3) END,
    NULL,
    'Test rice procurement - record ' + CAST(N AS VARCHAR),
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Rice Procurement External: 40 records inserted';
GO

--============================================
-- 4. LOANS & ADVANCES - 40 records
--============================================
PRINT 'Inserting Loans & Advances records...';

INSERT INTO LoanAdvance
(Date, VoucherNumber, Particulars, PartyName, AmountGiven, Repayment, RepaymentDate, Balance,
 Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'LA-TEST-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 2)
        WHEN 0 THEN 'Advance given to employee'
        ELSE 'Loan taken from party'
    END,
    'Test Party/Employee ' + CAST(N AS VARCHAR),
    10000 + (N * 1000),
    CASE (N % 3) WHEN 0 THEN (10000 + (N * 1000)) WHEN 1 THEN 0 ELSE ((10000 + (N * 1000)) * 0.5) END,
    CASE (N % 3) WHEN 0 THEN DATEADD(DAY, -N + 10, GETDATE()) ELSE NULL END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (10000 + (N * 1000)) ELSE ((10000 + (N * 1000)) * 0.5) END,
    'Test loan/advance - record ' + CAST(N AS VARCHAR),
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Loans & Advances: 40 records inserted';
GO

--============================================
-- 5. FIXED ASSETS - 40 records
--============================================
PRINT 'Inserting Fixed Assets records...';

INSERT INTO FixedAsset
(AssetId, PurchaseDate, AssetName, Description, Supplier, PurchaseValue, DepreciationRate,
 AccumulatedDepreciation, NetBookValue, PresentValueApprox, Status, CreatedDate, IsActive)
SELECT
    'ASSET-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    DATEADD(DAY, -(N * 10), GETDATE()),
    CASE (N % 5)
        WHEN 0 THEN 'Rice Milling Machine ' + CAST(N AS VARCHAR)
        WHEN 1 THEN 'Delivery Vehicle ' + CAST(N AS VARCHAR)
        WHEN 2 THEN 'Office Equipment ' + CAST(N AS VARCHAR)
        WHEN 3 THEN 'Storage Tank ' + CAST(N AS VARCHAR)
        ELSE 'Weighing Scale ' + CAST(N AS VARCHAR)
    END,
    'Test asset for operations - Item ' + CAST(N AS VARCHAR),
    'Test Supplier ' + CAST(N AS VARCHAR),
    50000 + (N * 5000),
    10.0,
    (50000 + (N * 5000)) * 0.15,
    (50000 + (N * 5000)) * 0.85,
    (50000 + (N * 5000)) * 0.80,
    CASE (N % 3) WHEN 0 THEN 'Active' WHEN 1 THEN 'Under Maintenance' ELSE 'Active' END,
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Fixed Assets: 40 records inserted';
GO

--============================================
-- 6. VOUCHERS - 40 records
--============================================
PRINT 'Inserting Vouchers records...';

INSERT INTO Voucher
(VoucherDate, VoucherNumber, VoucherType, Particulars, Amount, Remarks, CreatedBy, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -N, GETDATE()),
    'VCH-TEST-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    CASE (N % 4)
        WHEN 0 THEN 'Payment'
        WHEN 1 THEN 'Receipt'
        WHEN 2 THEN 'Journal'
        ELSE 'Contra'
    END,
    'Test voucher entry for ' +
    CASE (N % 4)
        WHEN 0 THEN 'supplier payment'
        WHEN 1 THEN 'customer receipt'
        WHEN 2 THEN 'adjustment entry'
        ELSE 'bank transfer'
    END + ' - record ' + CAST(N AS VARCHAR),
    3000 + (N * 400),
    'Test voucher remark - record ' + CAST(N AS VARCHAR),
    'TestScript',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Vouchers: 40 records inserted';
GO

--============================================
-- 7. RECEIVABLES OVERDUE - 40 records
--============================================
PRINT 'Inserting Receivables Overdue records...';

INSERT INTO ReceivableOverdue
(InvoiceDate, InvoiceNumber, CustomerName, ItemSupplied, InvoiceAmount, AmountReceived, BalanceDue,
 DueDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(N + 30), GETDATE()),
    'RO-INV-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    'Test Customer ' + CAST(N AS VARCHAR),
    CASE (N % 4)
        WHEN 0 THEN 'Premium Rice - 500kg'
        WHEN 1 THEN 'Standard Rice - 800kg'
        WHEN 2 THEN 'Broken Rice - 200kg'
        ELSE 'Rice Bran - 300kg'
    END,
    5000 + (N * 500),
    CASE (N % 3) WHEN 0 THEN (5000 + (N * 500)) WHEN 1 THEN 0 ELSE ((5000 + (N * 500)) * 0.6) END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (5000 + (N * 500)) ELSE ((5000 + (N * 500)) * 0.4) END,
    DATEADD(DAY, -N, GETDATE()),
    'Test receivable - overdue ' + CAST(N AS VARCHAR) + ' days',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Receivables Overdue: 40 records inserted';
GO

--============================================
-- 8. PAYABLES OVERDUE - 40 records
--============================================
PRINT 'Inserting Payables Overdue records...';

INSERT INTO PayableOverdue
(PurchaseDate, InvoiceNumber, SupplierName, ItemPurchased, InvoiceAmount, AmountPaid, BalancePayable,
 DueDate, Remarks, CreatedDate, IsActive)
SELECT
    DATEADD(DAY, -(N + 30), GETDATE()),
    'PO-INV-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    'Test Supplier ' + CAST(N AS VARCHAR),
    CASE (N % 4)
        WHEN 0 THEN 'Paddy Procurement - 1000kg'
        WHEN 1 THEN 'Rice Purchase - 600kg'
        WHEN 2 THEN 'Packaging Material'
        ELSE 'Transportation Services'
    END,
    7000 + (N * 600),
    CASE (N % 3) WHEN 0 THEN (7000 + (N * 600)) WHEN 1 THEN 0 ELSE ((7000 + (N * 600)) * 0.7) END,
    CASE (N % 3) WHEN 0 THEN 0 WHEN 1 THEN (7000 + (N * 600)) ELSE ((7000 + (N * 600)) * 0.3) END,
    DATEADD(DAY, -N, GETDATE()),
    'Test payable - overdue ' + CAST(N AS VARCHAR) + ' days',
    GETDATE(),
    1
FROM #Numbers;

PRINT 'Payables Overdue: 40 records inserted';
GO

-- Clean up
DROP TABLE #Numbers;
GO

PRINT '========================================';
PRINT 'ALL DATA INSERTION COMPLETE!';
PRINT 'Verifying all table counts...';
PRINT '========================================';
GO

-- Comprehensive verification
SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS Total FROM PaddyProcurement WHERE IsActive = 1
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
SELECT 'Vouchers', COUNT(*) FROM Voucher WHERE IsActive = 1
UNION ALL
SELECT 'LoansAdvances', COUNT(*) FROM LoanAdvance WHERE IsActive = 1
UNION ALL
SELECT 'FixedAssets', COUNT(*) FROM FixedAsset WHERE IsActive = 1
UNION ALL
SELECT 'ReceivablesOverdue', COUNT(*) FROM ReceivableOverdue WHERE IsActive = 1
UNION ALL
SELECT 'PayablesOverdue', COUNT(*) FROM PayableOverdue WHERE IsActive = 1
ORDER BY TableName;
GO

PRINT '========================================';
PRINT 'SUCCESS! All tables now have test data!';
PRINT 'You can now test paging on ALL pages!';
PRINT '========================================';
GO
