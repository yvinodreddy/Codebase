-- RMMS Application - Test Data Scripts
-- Purpose: Insert test data for comprehensive testing
-- Date: October 4, 2025

-- NOTE: Run these scripts AFTER your database schema is created
-- Adjust table/column names if they differ from assumptions

USE RMMS_Production;  -- Change to your database name
GO

-- =============================================
-- 1. PADDY PROCUREMENT TEST DATA
-- =============================================

PRINT 'Inserting Paddy Procurement test data...';

INSERT INTO PaddyProcurement (
    ReceiptDate, VoucherNumber, SupplierName, PaddyVariety,
    QuantityReceived, UnitPrice, Grade, StorageLocation,
    OpeningStock, Issues, ClosingStock,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'PP-2025-001', 'Ramesh Traders', 'Basmati', 1000.00, 45.50, 'A', 'Warehouse 1', 0, 0, 1000.00, 'TestUser', GETDATE(), 1),
('2025-10-02', 'PP-2025-002', 'Kumar Seeds', 'Sonam', 1500.50, 42.75, 'A', 'Warehouse 1', 1000.00, 200.00, 2300.50, 'TestUser', GETDATE(), 1),
('2025-10-03', 'PP-2025-003', 'Sharma Suppliers', 'Basmati', 800.25, 46.00, 'B', 'Warehouse 2', 2300.50, 300.00, 2800.75, 'TestUser', GETDATE(), 1),
('2025-10-04', 'PP-2025-004', 'Ramesh Traders', 'Mansuri', 2000.00, 40.25, 'A', 'Warehouse 1', 2800.75, 500.00, 4300.75, 'TestUser', GETDATE(), 1),
('2025-10-05', 'PP-2025-005', 'Patel Enterprises', 'Katrni', 1200.75, 38.50, 'A', 'Warehouse 2', 4300.75, 100.00, 5400.50, 'TestUser', GETDATE(), 1);

PRINT 'Paddy Procurement: 5 records inserted';

-- =============================================
-- 2. RICE SALES TEST DATA
-- =============================================

PRINT 'Inserting Rice Sales test data...';

INSERT INTO RiceSales (
    InvoiceNumber, SaleDate, BuyerName, BuyerGSTIN, BuyerAddress,
    RiceGrade, Quantity, UnitPrice, TotalInvoiceValue,
    Discount, FreightCharges, OtherCharges, GrossInvoiceAmount,
    PaymentMode, PaymentStatus, DueDate,
    CreatedBy, CreatedDate, IsActive
) VALUES
('INV-2025-001', '2025-10-01', 'ABC Retail Store', '27AABCU9603R1Z5', '123 Market St', 'Basmati Premium', 500.00, 60.00, 30000.00, 500.00, 200.00, 100.00, 29800.00, 'Cash', 'Paid', NULL, 'TestUser', GETDATE(), 1),
('INV-2025-002', '2025-10-02', 'XYZ Wholesalers', '29AABCU9603R1Z6', '456 Trade Ave', 'Sonam', 750.50, 55.00, 41277.50, 1000.00, 300.00, 150.00, 40727.50, 'Credit', 'Pending', '2025-11-02', 'TestUser', GETDATE(), 1),
('INV-2025-003', '2025-10-03', 'Ramesh Retail', NULL, '789 Shop Rd', 'Basmati Standard', 300.00, 50.00, 15000.00, 0, 100.00, 50.00, 15150.00, 'Cash', 'Paid', NULL, 'TestUser', GETDATE(), 1),
('INV-2025-004', '2025-10-04', 'Kumar Traders', '27AABCU9603R1Z7', '321 Business Park', 'Mansuri', 1000.00, 48.00, 48000.00, 2000.00, 500.00, 200.00, 46700.00, 'UPI', 'Paid', NULL, 'TestUser', GETDATE(), 1),
('INV-2025-005', '2025-10-05', 'ABC Retail Store', '27AABCU9603R1Z5', '123 Market St', 'Basmati Premium', 600.00, 60.00, 36000.00, 1000.00, 250.00, 100.00, 35350.00, 'Credit', 'Pending', '2025-11-05', 'TestUser', GETDATE(), 1);

PRINT 'Rice Sales: 5 records inserted';

-- =============================================
-- 3. BYPRODUCT SALES TEST DATA
-- =============================================

PRINT 'Inserting Byproduct Sales test data...';

INSERT INTO ByProductSales (
    SaleDate, InvoiceNumber, CustomerName, ProductType,
    Quantity, UnitPrice, TotalAmount,
    PaymentMode, PaymentStatus,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'BP-2025-001', 'Poultry Farm A', 'Rice Bran', 200.00, 15.00, 3000.00, 'Cash', 'Paid', 'TestUser', GETDATE(), 1),
('2025-10-02', 'BP-2025-002', 'Cattle Feed Supplier', 'Broken Rice', 500.50, 12.50, 6256.25, 'Credit', 'Pending', 'TestUser', GETDATE(), 1),
('2025-10-03', 'BP-2025-003', 'Local Trader', 'Rice Husk', 1000.00, 5.00, 5000.00, 'Cash', 'Paid', 'TestUser', GETDATE(), 1),
('2025-10-04', 'BP-2025-004', 'Poultry Farm B', 'Rice Bran', 300.00, 15.00, 4500.00, 'UPI', 'Paid', 'TestUser', GETDATE(), 1),
('2025-10-05', 'BP-2025-005', 'Feed Mill', 'Broken Rice', 400.00, 12.00, 4800.00, 'Cash', 'Paid', 'TestUser', GETDATE(), 1);

PRINT 'Byproduct Sales: 5 records inserted';

-- =============================================
-- 4. EXTERNAL RICE SALES TEST DATA
-- =============================================

PRINT 'Inserting External Rice Sales test data...';

INSERT INTO ExternalRiceSales (
    SaleDate, InvoiceNumber, CustomerName, Destination,
    RiceGrade, Quantity, UnitPrice, TotalAmount,
    PaymentMode, PaymentStatus,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'EXT-2025-001', 'Export Company Ltd', 'Dubai, UAE', 'Basmati Premium', 5000.00, 75.00, 375000.00, 'Wire Transfer', 'Paid', 'TestUser', GETDATE(), 1),
('2025-10-02', 'EXT-2025-002', 'International Traders', 'Singapore', 'Sonam', 3000.00, 65.00, 195000.00, 'LC', 'Pending', 'TestUser', GETDATE(), 1),
('2025-10-03', 'EXT-2025-003', 'Global Rice Co', 'Malaysia', 'Basmati Standard', 4000.00, 55.00, 220000.00, 'Wire Transfer', 'Paid', 'TestUser', GETDATE(), 1);

PRINT 'External Rice Sales: 3 records inserted';

-- =============================================
-- 5. BANK TRANSACTIONS TEST DATA
-- =============================================

PRINT 'Inserting Bank Transactions test data...';

INSERT INTO BankTransactions (
    TransactionDate, BankName, AccountNumber, TransactionType,
    Amount, ChequeNumber, Particulars, Balance,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'State Bank', '1234567890', 'Deposit', 50000.00, NULL, 'Cash deposit from rice sales', 150000.00, 'TestUser', GETDATE(), 1),
('2025-10-02', 'HDFC Bank', '0987654321', 'Withdrawal', 25000.00, 'CHQ123456', 'Payment to supplier', 125000.00, 'TestUser', GETDATE(), 1),
('2025-10-03', 'State Bank', '1234567890', 'Deposit', 30000.00, NULL, 'Customer payment received', 155000.00, 'TestUser', GETDATE(), 1),
('2025-10-04', 'ICICI Bank', '1122334455', 'Withdrawal', 15000.00, 'CHQ123457', 'Office expenses', 140000.00, 'TestUser', GETDATE(), 1),
('2025-10-05', 'State Bank', '1234567890', 'Deposit', 40000.00, NULL, 'Export payment', 180000.00, 'TestUser', GETDATE(), 1);

PRINT 'Bank Transactions: 5 records inserted';

-- =============================================
-- 6. CASH BOOK TEST DATA
-- =============================================

PRINT 'Inserting Cash Book test data...';

INSERT INTO CashBook (
    TransactionDate, VoucherNumber, Particulars, TransactionType,
    Amount, Balance,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'CB-001', 'Opening Balance', 'Receipt', 50000.00, 50000.00, 'TestUser', GETDATE(), 1),
('2025-10-01', 'CB-002', 'Rice sale payment', 'Receipt', 10000.00, 60000.00, 'TestUser', GETDATE(), 1),
('2025-10-02', 'CB-003', 'Supplier payment', 'Payment', 5000.00, 55000.00, 'TestUser', GETDATE(), 1),
('2025-10-03', 'CB-004', 'Byproduct sale', 'Receipt', 3000.00, 58000.00, 'TestUser', GETDATE(), 1),
('2025-10-04', 'CB-005', 'Office expenses', 'Payment', 2000.00, 56000.00, 'TestUser', GETDATE(), 1),
('2025-10-05', 'CB-006', 'Customer payment', 'Receipt', 15000.00, 71000.00, 'TestUser', GETDATE(), 1);

PRINT 'Cash Book: 6 records inserted';

-- =============================================
-- 7. VOUCHERS TEST DATA
-- =============================================

PRINT 'Inserting Vouchers test data...';

INSERT INTO Vouchers (
    VoucherDate, VoucherNumber, VoucherType, Particulars,
    Amount, PaymentMode, PayeeName,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-10-01', 'V-001', 'Payment', 'Paddy purchase payment', 45000.00, 'Cash', 'Ramesh Traders', 'TestUser', GETDATE(), 1),
('2025-10-02', 'V-002', 'Receipt', 'Rice sale payment received', 30000.00, 'Cheque', 'ABC Retail Store', 'TestUser', GETDATE(), 1),
('2025-10-03', 'V-003', 'Payment', 'Office rent', 10000.00, 'Bank Transfer', 'Landlord', 'TestUser', GETDATE(), 1),
('2025-10-04', 'V-004', 'Receipt', 'Byproduct sale', 5000.00, 'Cash', 'Poultry Farm A', 'TestUser', GETDATE(), 1),
('2025-10-05', 'V-005', 'Payment', 'Electricity bill', 3500.00, 'UPI', 'Power Company', 'TestUser', GETDATE(), 1);

PRINT 'Vouchers: 5 records inserted';

-- =============================================
-- 8. PAYABLES OVERDUE TEST DATA
-- =============================================

PRINT 'Inserting Payables test data...';

INSERT INTO PayablesOverdue (
    PurchaseDate, InvoiceNumber, SupplierName, InvoiceAmount,
    AmountPaid, BalancePayable, DueDate, DaysOverdue,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-09-01', 'SUP-001', 'Ramesh Traders', 50000.00, 20000.00, 30000.00, '2025-09-30', DATEDIFF(DAY, '2025-09-30', GETDATE()), 'TestUser', GETDATE(), 1),
('2025-09-15', 'SUP-002', 'Kumar Seeds', 75000.00, 50000.00, 25000.00, '2025-10-15', 0, 'TestUser', GETDATE(), 1),
('2025-08-20', 'SUP-003', 'Sharma Suppliers', 100000.00, 60000.00, 40000.00, '2025-09-20', DATEDIFF(DAY, '2025-09-20', GETDATE()), 'TestUser', GETDATE(), 1),
('2025-09-25', 'SUP-004', 'Patel Enterprises', 30000.00, 15000.00, 15000.00, '2025-10-25', 0, 'TestUser', GETDATE(), 1),
('2025-07-10', 'SUP-005', 'Singh Traders', 80000.00, 20000.00, 60000.00, '2025-08-10', DATEDIFF(DAY, '2025-08-10', GETDATE()), 'TestUser', GETDATE(), 1);

PRINT 'Payables: 5 records inserted';

-- =============================================
-- 9. RECEIVABLES OVERDUE TEST DATA
-- =============================================

PRINT 'Inserting Receivables test data...';

INSERT INTO ReceivablesOverdue (
    InvoiceDate, InvoiceNumber, CustomerName, ItemSupplied,
    InvoiceAmount, AmountReceived, BalanceDue, DueDate, DaysOverdue,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-09-01', 'INV-001', 'ABC Retail Store', 'Basmati Rice', 40000.00, 20000.00, 20000.00, '2025-09-30', DATEDIFF(DAY, '2025-09-30', GETDATE()), 'TestUser', GETDATE(), 1),
('2025-09-10', 'INV-002', 'XYZ Wholesalers', 'Sonam Rice', 60000.00, 30000.00, 30000.00, '2025-10-10', 0, 'TestUser', GETDATE(), 1),
('2025-08-15', 'INV-003', 'Kumar Traders', 'Mansuri Rice', 50000.00, 10000.00, 40000.00, '2025-09-15', DATEDIFF(DAY, '2025-09-15', GETDATE()), 'TestUser', GETDATE(), 1),
('2025-09-20', 'INV-004', 'Sharma Retail', 'Basmati Rice', 35000.00, 35000.00, 0, '2025-10-20', 0, 'TestUser', GETDATE(), 1),
('2025-07-25', 'INV-005', 'Ramesh Store', 'Broken Rice', 25000.00, 5000.00, 20000.00, '2025-08-25', DATEDIFF(DAY, '2025-08-25', GETDATE()), 'TestUser', GETDATE(), 1);

PRINT 'Receivables: 5 records inserted';

-- =============================================
-- 10. LOAN ADVANCES TEST DATA
-- =============================================

PRINT 'Inserting Loan Advances test data...';

INSERT INTO LoansAdvances (
    LoanDate, LoanNumber, BorrowerName, LoanAmount,
    InterestRate, LoanTerm, RepaymentAmount, BalanceAmount,
    Status, DueDate,
    CreatedBy, CreatedDate, IsActive
) VALUES
('2025-01-15', 'LA-001', 'Ramesh Kumar', 100000.00, 10.00, 12, 8333.33, 91666.67, 'Active', '2025-11-15', 'TestUser', GETDATE(), 1),
('2025-03-20', 'LA-002', 'Suresh Sharma', 50000.00, 8.00, 6, 8333.33, 41666.67, 'Active', '2025-11-20', 'TestUser', GETDATE(), 1),
('2025-06-10', 'LA-003', 'Mahesh Patel', 75000.00, 9.00, 12, 6250.00, 68750.00, 'Active', '2025-12-10', 'TestUser', GETDATE(), 1),
('2024-12-01', 'LA-004', 'Rajesh Singh', 150000.00, 12.00, 24, 6250.00, 0, 'Closed', '2025-10-01', 'TestUser', GETDATE(), 1);

PRINT 'Loan Advances: 4 records inserted';

-- =============================================
-- 11. FIXED ASSETS TEST DATA
-- =============================================

PRINT 'Inserting Fixed Assets test data...';

INSERT INTO FixedAssets (
    AssetName, AssetCategory, PurchaseDate, PurchaseValue,
    CurrentValue, DepreciationRate, Location, Status,
    CreatedBy, CreatedDate, IsActive
) VALUES
('Rice Milling Machine', 'Machinery', '2023-01-15', 500000.00, 400000.00, 10.00, 'Main Factory', 'Operational', 'TestUser', GETDATE(), 1),
('Delivery Truck', 'Vehicle', '2022-06-20', 800000.00, 560000.00, 15.00, 'Warehouse', 'Operational', 'TestUser', GETDATE(), 1),
('Weighing Scale (Electronic)', 'Equipment', '2024-03-10', 50000.00, 48000.00, 5.00, 'Reception', 'Operational', 'TestUser', GETDATE(), 1),
('Office Computer System', 'IT Equipment', '2023-09-01', 100000.00, 70000.00, 20.00, 'Office', 'Operational', 'TestUser', GETDATE(), 1),
('Storage Racks', 'Furniture', '2022-12-15', 200000.00, 160000.00, 10.00, 'Warehouse 1', 'Operational', 'TestUser', GETDATE(), 1);

PRINT 'Fixed Assets: 5 records inserted';

-- =============================================
-- SUMMARY
-- =============================================

PRINT '';
PRINT '========================================';
PRINT 'TEST DATA INSERTION COMPLETE';
PRINT '========================================';
PRINT '';
PRINT 'Records Inserted:';
PRINT '  - Paddy Procurement: 5';
PRINT '  - Rice Sales: 5';
PRINT '  - Byproduct Sales: 5';
PRINT '  - External Rice Sales: 3';
PRINT '  - Bank Transactions: 5';
PRINT '  - Cash Book: 6';
PRINT '  - Vouchers: 5';
PRINT '  - Payables: 5';
PRINT '  - Receivables: 5';
PRINT '  - Loan Advances: 4';
PRINT '  - Fixed Assets: 5';
PRINT '';
PRINT 'TOTAL: 53 test records';
PRINT '';
PRINT 'Next Steps:';
PRINT '1. Run the application';
PRINT '2. Execute the Comprehensive Test Plan';
PRINT '3. Document any issues found';
PRINT '========================================';
