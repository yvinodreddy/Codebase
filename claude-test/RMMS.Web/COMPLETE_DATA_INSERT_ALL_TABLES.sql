-- ============================================
-- COMPLETE DATA INSERTION FOR ALL EMPTY TABLES
-- Using correct schema from database
-- ============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'INSERTING DATA FOR ALL EMPTY TABLES';
PRINT '========================================';
GO

-- ============================================
-- 1. BANK TRANSACTIONS (45 records)
-- ============================================
PRINT 'Inserting Bank Transactions...';

INSERT INTO BankTransactions (TransactionDate, ChequeUTRNumber, BankName, AccountNumber, Particulars,
                              Deposits, Withdrawals, Balance, TransactionType, ReconciliationStatus,
                              Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'UTR' + FORMAT(n, '000000000'),
    CASE WHEN n % 3 = 0 THEN 'SBI' WHEN n % 3 = 1 THEN 'HDFC' ELSE 'ICICI' END,
    '1234567890',
    'Transaction ' + CAST(n AS VARCHAR),
    CASE WHEN n % 2 = 0 THEN 10000.0 + (n * 500) ELSE 0 END,
    CASE WHEN n % 2 = 1 THEN 5000.0 + (n * 250) ELSE 0 END,
    100000.0 + (n * 1000),
    CASE WHEN n % 2 = 0 THEN 'Deposit' ELSE 'Withdrawal' END,
    CASE WHEN n % 3 = 0 THEN 'Reconciled' ELSE 'Pending' END,
    'Bank transaction ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Bank Transactions: 45 records';
GO

-- ============================================
-- 2. CASH BOOK (48 records)
-- ============================================
PRINT 'Inserting Cash Book...';

INSERT INTO CashBook (TransactionDate, VoucherNumber, Particulars, Receipts, Payments, Balance, Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'CASH-' + FORMAT(n, '00000'),
    'Cash transaction ' + CAST(n AS VARCHAR),
    CASE WHEN n % 2 = 0 THEN 5000.0 + (n * 200) ELSE 0 END,
    CASE WHEN n % 2 = 1 THEN 3000.0 + (n * 150) ELSE 0 END,
    50000.0 + (n * 500),
    'Daily cash ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Cash Book: 48 records';
GO

-- ============================================
-- 3. VOUCHERS (50 records)
-- ============================================
PRINT 'Inserting Vouchers...';

INSERT INTO Vouchers (VoucherDate, VoucherType, VoucherNumber, Particulars, Amount, PaymentMode,
                      ReceivedFromPaidTo, ReferenceNumber, Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'Receipt' WHEN n % 3 = 1 THEN 'Payment' ELSE 'Journal' END,
    'VCH-' + FORMAT(n, '00000'),
    'Voucher particulars ' + CAST(n AS VARCHAR),
    10000.0 + (n * 500),
    CASE WHEN n % 3 = 0 THEN 'Cash' WHEN n % 3 = 1 THEN 'Cheque' ELSE 'Online' END,
    'Party ' + CAST(n AS VARCHAR),
    'REF-' + CAST(n AS VARCHAR),
    'Voucher ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Vouchers: 50 records';
GO

-- ============================================
-- 4. FIXED ASSETS (42 records)
-- ============================================
PRINT 'Inserting Fixed Assets...';

INSERT INTO FixedAssets (AssetId, PurchaseDate, AssetName, Description, Supplier, PurchaseValue,
                         DepreciationRate, AccumulatedDepreciation, NetBookValue, PresentValueApprox,
                         Status, IsActive)
SELECT
    'ASSET-' + FORMAT(n, '00000'),
    DATEADD(MONTH, -n, GETDATE()),
    'Asset ' + CAST(n AS VARCHAR),
    'Asset description ' + CAST(n AS VARCHAR),
    'Supplier ' + CAST(1 + (n % 45) AS VARCHAR),
    500000.0 + (n * 10000),
    10.0 + (n % 10),
    50000.0 + (n * 1000),
    450000.0 + (n * 9000),
    400000.0 + (n * 8000),
    'Active',
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Fixed Assets: 42 records';
GO

-- ============================================
-- 5. LOANS & ADVANCES (45 records)
-- ============================================
PRINT 'Inserting Loans & Advances...';

INSERT INTO LoansAdvances (TransactionDate, TransactionType, PartyName, Amount, InterestRate,
                           TenureMonths, DueDate, Status, Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN n % 2 = 0 THEN 'Loan' ELSE 'Advance' END,
    'Party ' + CAST(n AS VARCHAR),
    100000.0 + (n * 5000),
    8.0 + (n % 5),
    12 + (n % 36),
    DATEADD(MONTH, 12, DATEADD(DAY, -n, GETDATE())),
    CASE WHEN n % 3 = 0 THEN 'Active' WHEN n % 3 = 1 THEN 'Closed' ELSE 'Overdue' END,
    'Loan/Advance ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Loans & Advances: 45 records';
GO

-- ============================================
-- 6. PAYABLES OVERDUE (40 records)
-- ============================================
PRINT 'Inserting Payables Overdue...';

INSERT INTO PayablesOverdue (VendorName, InvoiceNumber, PurchaseDate, Amount, DueDate, OverdueDays,
                             Status, Remarks, IsActive)
SELECT
    'Vendor ' + CAST(1 + (n % 45) AS VARCHAR) + ' Suppliers',
    'PINV-' + FORMAT(n, '00000'),
    DATEADD(DAY, -(n + 60), GETDATE()),
    50000.0 + (n * 2000),
    DATEADD(DAY, -(n + 30), GETDATE()),
    n,
    CASE WHEN n % 2 = 0 THEN 'Overdue' ELSE 'Critical' END,
    'Overdue payment ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Payables Overdue: 40 records';
GO

-- ============================================
-- 7. RECEIVABLES OVERDUE (42 records)
-- ============================================
PRINT 'Inserting Receivables Overdue...';

INSERT INTO ReceivablesOverdue (CustomerName, InvoiceNumber, InvoiceDate, Amount, DueDate, OverdueDays,
                                Status, Remarks, IsActive)
SELECT
    'Customer ' + CAST(1 + (n % 50) AS VARCHAR) + ' Pvt Ltd',
    'SINV-' + FORMAT(n, '00000'),
    DATEADD(DAY, -(n + 60), GETDATE()),
    75000.0 + (n * 3000),
    DATEADD(DAY, -(n + 30), GETDATE()),
    n,
    CASE WHEN n % 2 = 0 THEN 'Overdue' ELSE 'Follow-up' END,
    'Overdue receipt ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 42 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Receivables Overdue: 42 records';
GO

-- ============================================
-- 8. PRODUCTION ORDERS (50 records)
-- ============================================
PRINT 'Inserting Production Orders...';

INSERT INTO ProductionOrders (OrderNumber, OrderDate, RiceType, Quantity, QuantityUOM,
                              DueDate, Priority, Status, Remarks, IsActive)
SELECT
    'PO-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + FORMAT(n, '000'),
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN n % 4 = 0 THEN 'Basmati' WHEN n % 4 = 1 THEN 'Sona Masuri'
         WHEN n % 4 = 2 THEN 'IR-64' ELSE 'Ponni' END,
    1000.0 + (n * 100),
    'KG',
    DATEADD(DAY, -n+7, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'High' WHEN n % 3 = 1 THEN 'Medium' ELSE 'Low' END,
    CASE WHEN n % 4 = 0 THEN 'Completed' WHEN n % 4 = 1 THEN 'In Progress'
         WHEN n % 4 = 2 THEN 'Pending' ELSE 'Planned' END,
    'Production order ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Orders: 50 records';
GO

-- ============================================
-- 9. PRODUCTION BATCHES (50 records)
-- ============================================
PRINT 'Inserting Production Batches...';

INSERT INTO ProductionBatches (BatchNumber, ProductionOrderId, BatchDate, ShiftType,
                               OperatorId, SupervisorId, Status, CompletionPercent,
                               QualityScore, Remarks, IsActive)
SELECT
    'BATCH-' + FORMAT(DATEADD(DAY, -n, GETDATE()), 'yyyyMMdd') + '-' + FORMAT(n, '000'),
    (n % 50) + 1,  -- Production Order IDs
    DATEADD(DAY, -n, GETDATE()),
    CASE WHEN n % 3 = 0 THEN 'Morning' WHEN n % 3 = 1 THEN 'Evening' ELSE 'Night' END,
    (n % 40) + 1,  -- Operator Employee ID
    ((n % 10) + 1),  -- Supervisor Employee ID
    CASE WHEN n % 3 = 0 THEN 'Completed' WHEN n % 3 = 1 THEN 'In Progress' ELSE 'Started' END,
    CASE WHEN n % 3 = 0 THEN 100.0 WHEN n % 3 = 1 THEN 50.0 ELSE 10.0 END,
    85.0 + (n % 15),
    'Batch ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Production Batches: 50 records';
GO

-- ============================================
-- 10. RICE SALES (50 records)
-- ============================================
PRINT 'Inserting Rice Sales...';

INSERT INTO RiceSales (SaleDate, InvoiceNumber, BillNumber, CustomerName, RiceType, BagSize,
                       NumberOfBags, Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus,
                       DispatchDate, Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'RICE-INV-' + FORMAT(n, '00000'),
    'BILL-' + FORMAT(n, '00000'),
    'Customer ' + CAST(1 + (n % 50) AS VARCHAR) + ' Pvt Ltd',
    CASE WHEN n % 4 = 0 THEN 'Basmati' WHEN n % 4 = 1 THEN 'Sona Masuri'
         WHEN n % 4 = 2 THEN 'IR-64' ELSE 'Ponni' END,
    CASE WHEN n % 2 = 0 THEN '25 KG' ELSE '50 KG' END,
    10 + (n * 2),
    250.0 + (n * 50),
    50.0 + (n * 2.5),
    (250.0 + (n * 50)) * (50.0 + (n * 2.5)),
    CASE WHEN n % 3 = 0 THEN 'Cash' WHEN n % 3 = 1 THEN 'Credit' ELSE 'Online' END,
    CASE WHEN n % 2 = 0 THEN 'Paid' ELSE 'Pending' END,
    DATEADD(DAY, -n+1, GETDATE()),
    'Rice sale ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Rice Sales: 50 records';
GO

-- ============================================
-- 11. BY-PRODUCT SALES (45 records)
-- ============================================
PRINT 'Inserting By-Product Sales...';

INSERT INTO ByProductSales (SaleDate, TransactionNumber, ProductType, BuyerName, BuyerContact,
                            Quantity, Rate, TotalAmount, PaymentMode, PaymentStatus, Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'BP-' + FORMAT(n, '00000'),
    CASE WHEN n % 3 = 0 THEN 'Rice Bran' WHEN n % 3 = 1 THEN 'Rice Husk' ELSE 'Broken Rice' END,
    'Buyer ' + CAST(n AS VARCHAR),
    '98765' + FORMAT(n, '00000'),
    500.0 + (n * 25),
    5.0 + (n * 0.5),
    (500.0 + (n * 25)) * (5.0 + (n * 0.5)),
    CASE WHEN n % 2 = 0 THEN 'Cash' ELSE 'Credit' END,
    CASE WHEN n % 2 = 0 THEN 'Paid' ELSE 'Pending' END,
    'By-product sale ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ By-Product Sales: 45 records';
GO

-- ============================================
-- 12. EXTERNAL RICE SALES (40 records)
-- ============================================
PRINT 'Inserting External Rice Sales...';

INSERT INTO ExternalRiceSales (Date, ItemDescription, SoldTo, SoldBy, Quantity, Rate, TotalAmount,
                               PaymentMode, PaymentStatus, Balance, FullPaymentClearanceDate,
                               Remarks, IsActive)
SELECT
    DATEADD(DAY, -n, GETDATE()),
    'External Rice Type ' + CAST(n AS VARCHAR),
    'External Customer ' + CAST(n AS VARCHAR),
    'Agent ' + CAST(n AS VARCHAR),
    300.0 + (n * 30),
    45.0 + (n * 2),
    (300.0 + (n * 30)) * (45.0 + (n * 2)),
    CASE WHEN n % 2 = 0 THEN 'Cash' ELSE 'Credit' END,
    CASE WHEN n % 2 = 0 THEN 'Paid' ELSE 'Pending' END,
    CASE WHEN n % 2 = 1 THEN (300.0 + (n * 30)) * (45.0 + (n * 2)) * 0.3 ELSE 0 END,
    CASE WHEN n % 2 = 0 THEN DATEADD(DAY, -n+5, GETDATE()) ELSE NULL END,
    'External sale ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 40 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ External Rice Sales: 40 records';
GO

-- ============================================
-- 13. INQUIRIES (50 records)
-- ============================================
PRINT 'Inserting Inquiries...';

INSERT INTO Inquiries (InquiryNumber, InquiryDate, CustomerId, Source, ProductType, ApproximateQuantity,
                       UnitOfMeasure, ExpectedDeliveryDate, Status, AssignedToEmployeeId, Priority,
                       CustomerRequirements, Remarks, FollowUpDate, IsActive)
SELECT
    'INQ-' + FORMAT(n, '00000'),
    DATEADD(DAY, -n, GETDATE()),
    1 + (n % 50),
    CASE WHEN n % 4 = 0 THEN 'Phone' WHEN n % 4 = 1 THEN 'Email'
         WHEN n % 4 = 2 THEN 'Walk-in' ELSE 'Reference' END,
    CASE WHEN n % 4 = 0 THEN 'Basmati Rice' WHEN n % 4 = 1 THEN 'Sona Masuri'
         WHEN n % 4 = 2 THEN 'IR-64' ELSE 'Ponni' END,
    100.0 + (n * 50),
    'KG',
    DATEADD(DAY, -n+15, GETDATE()),
    CASE WHEN n % 4 = 0 THEN 'New' WHEN n % 4 = 1 THEN 'In Progress'
         WHEN n % 4 = 2 THEN 'Quoted' ELSE 'Converted' END,
    1 + (n % 40),
    CASE WHEN n % 3 = 0 THEN 'High' WHEN n % 3 = 1 THEN 'Medium' ELSE 'Low' END,
    'Customer requirements ' + CAST(n AS VARCHAR),
    'Inquiry ' + CAST(n AS VARCHAR),
    DATEADD(DAY, -n+3, GETDATE()),
    1
FROM (SELECT TOP 50 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Inquiries: 50 records';
GO

-- ============================================
-- 14. QUOTATIONS (45 records)
-- ============================================
PRINT 'Inserting Quotations...';

INSERT INTO Quotations (QuotationNumber, QuotationDate, CustomerId, InquiryId, ValidUntil, TotalAmount,
                        DiscountPercent, DiscountAmount, TaxAmount, NetAmount, Status, PreparedBy,
                        Remarks, IsActive)
SELECT
    'QUO-' + FORMAT(n, '00000'),
    DATEADD(DAY, -n, GETDATE()),
    1 + (n % 50),
    (n % 50) + 1,
    DATEADD(DAY, -n+30, GETDATE()),
    100000.0 + (n * 5000),
    5.0,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 0.05,
    (100000.0 + (n * 5000)) * 0.95 + (100000.0 + (n * 5000)) * 0.05,
    CASE WHEN n % 4 = 0 THEN 'Draft' WHEN n % 4 = 1 THEN 'Sent'
         WHEN n % 4 = 2 THEN 'Accepted' ELSE 'Rejected' END,
    1 + (n % 40),
    'Quotation ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 45 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Quotations: 45 records';
GO

-- ============================================
-- 15. SALES ORDERS (48 records)
-- ============================================
PRINT 'Inserting Sales Orders...';

INSERT INTO SalesOrders (OrderNumber, OrderDate, CustomerId, QuotationId, ExpectedDeliveryDate,
                         TotalAmount, AdvanceAmount, BalanceAmount, PaymentTerms, Status,
                         ApprovedBy, Remarks, IsActive)
SELECT
    'SO-' + FORMAT(n, '00000'),
    DATEADD(DAY, -n, GETDATE()),
    1 + (n % 50),
    (n % 45) + 1,
    DATEADD(DAY, -n+10, GETDATE()),
    150000.0 + (n * 7500),
    50000.0 + (n * 2500),
    100000.0 + (n * 5000),
    'NET 30',
    CASE WHEN n % 4 = 0 THEN 'Pending' WHEN n % 4 = 1 THEN 'Confirmed'
         WHEN n % 4 = 2 THEN 'In Production' ELSE 'Completed' END,
    1 + (n % 10),
    'Sales order ' + CAST(n AS VARCHAR),
    1
FROM (SELECT TOP 48 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n FROM sys.all_columns) nums;

PRINT '✓ Sales Orders: 48 records';
GO

PRINT '';
PRINT '========================================';
PRINT 'DATA INSERTION COMPLETE!';
PRINT '========================================';
PRINT '';

-- Show summary
SELECT
    'BankTransactions' AS TableName, COUNT(*) AS RecordCount FROM BankTransactions
UNION ALL SELECT 'CashBook', COUNT(*) FROM CashBook
UNION ALL SELECT 'Vouchers', COUNT(*) FROM Vouchers
UNION ALL SELECT 'FixedAssets', COUNT(*) FROM FixedAssets
UNION ALL SELECT 'LoansAdvances', COUNT(*) FROM LoansAdvances
UNION ALL SELECT 'PayablesOverdue', COUNT(*) FROM PayablesOverdue
UNION ALL SELECT 'ReceivablesOverdue', COUNT(*) FROM ReceivablesOverdue
UNION ALL SELECT 'ProductionOrders', COUNT(*) FROM ProductionOrders
UNION ALL SELECT 'ProductionBatches', COUNT(*) FROM ProductionBatches
UNION ALL SELECT 'RiceSales', COUNT(*) FROM RiceSales
UNION ALL SELECT 'ByProductSales', COUNT(*) FROM ByProductSales
UNION ALL SELECT 'ExternalRiceSales', COUNT(*) FROM ExternalRiceSales
UNION ALL SELECT 'Inquiries', COUNT(*) FROM Inquiries
UNION ALL SELECT 'Quotations', COUNT(*) FROM Quotations
UNION ALL SELECT 'SalesOrders', COUNT(*) FROM SalesOrders;
GO
