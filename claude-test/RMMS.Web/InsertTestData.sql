-- Test Data Insertion Script for RMMS System
-- This script inserts 40 records for each table to test paging functionality
-- Run this script against RMMS_Production database

USE RMMS_Production;
GO

PRINT 'Starting test data insertion...';
PRINT 'Database: RMMS_Production';
PRINT 'Records per table: 40';
PRINT '========================================';

-- ============================================
-- 1. PADDY PROCUREMENT - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Paddy Procurement records...';

DECLARE @i INT = 1;
DECLARE @NewId INT;

WHILE @i <= 40
BEGIN
    DECLARE @ReceiptDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @VoucherNum VARCHAR(50) = 'PP-2024-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4);
    DECLARE @SupplierName VARCHAR(200) = 'Supplier ' + CAST(@i AS VARCHAR);
    DECLARE @PaddyVariety VARCHAR(100) = CASE (@i % 5)
        WHEN 0 THEN 'Basmati'
        WHEN 1 THEN 'Sona Masuri'
        WHEN 2 THEN 'IR-64'
        WHEN 3 THEN 'Swarna'
        ELSE 'Ponni'
    END;
    DECLARE @Grade VARCHAR(50) = CASE (@i % 3)
        WHEN 0 THEN 'Grade A'
        WHEN 1 THEN 'Grade B'
        ELSE 'Grade C'
    END;
    DECLARE @Quantity DECIMAL(18,2) = 1000 + (@i * 50);
    DECLARE @Weight DECIMAL(18,2) = @Quantity * 1.05;

    EXEC sp_PaddyProcurement_Insert
        @ReceiptDate = @ReceiptDate,
        @VoucherNumber = @VoucherNum,
        @SupplierName = @SupplierName,
        @PurchaseOrderNumber = NULL,
        @PaddyVariety = @PaddyVariety,
        @Grade = @Grade,
        @MoistureContent = 12.5,
        @QuantityReceived = @Quantity,
        @WeightPerBag = 50,
        @TotalNetWeight = @Weight,
        @StorageDate = @ReceiptDate,
        @StorageLocation = 'Warehouse A',
        @OpeningStock = 0,
        @Issues = 0,
        @ClosingStock = @Quantity,
        @LossShrinkage = 0,
        @Remarks = 'Test data record ' + CAST(@i AS VARCHAR),
        @ResponsiblePerson = 'Manager',
        @CreatedBy = 'TestUser',
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Paddy Procurement: 40 records inserted';

-- ============================================
-- 2. RICE PROCUREMENT EXTERNAL - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Rice Procurement External records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @RPEDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @ItemDesc VARCHAR(200) = CASE (@i % 4)
        WHEN 0 THEN 'Mansuri'
        WHEN 1 THEN 'Katrni'
        WHEN 2 THEN 'Sonam'
        ELSE 'Premium Rice'
    END;
    DECLARE @RPEQuantity DECIMAL(18,2) = 500 + (@i * 25);
    DECLARE @RPERate DECIMAL(18,2) = 40 + (@i % 10);

    EXEC sp_RiceProcurementExternal_Insert
        @Date = @RPEDate,
        @ItemDescription = @ItemDesc,
        @ProcuredFrom = 'Supplier ' + CAST(@i AS VARCHAR),
        @ProcuredBy = 'Buyer ' + CAST(@i AS VARCHAR),
        @Quantity = @RPEQuantity,
        @Rate = @RPERate,
        @TotalAmount = @RPEQuantity * @RPERate,
        @PaymentMode = CASE (@i % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        @PaymentStatus = CASE (@i % 3) WHEN 0 THEN 'Paid' WHEN 1 THEN 'Pending' ELSE 'Partial' END,
        @Balance = CASE (@i % 3) WHEN 0 THEN 0 ELSE (@RPEQuantity * @RPERate * 0.3) END,
        @FullPaymentDate = NULL,
        @Remarks = 'Test procurement record ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Rice Procurement External: 40 records inserted';

-- ============================================
-- 3. RICE SALES - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Rice Sales records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @SaleDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @InvoiceNum VARCHAR(50) = 'INV-2024-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4);
    DECLARE @RSQuantity DECIMAL(18,2) = 800 + (@i * 30);
    DECLARE @UnitPrice DECIMAL(18,2) = 50 + (@i % 15);
    DECLARE @TotalValue DECIMAL(18,2) = @RSQuantity * @UnitPrice;
    DECLARE @TaxableValue DECIMAL(18,2) = @TotalValue;
    DECLARE @CGST DECIMAL(18,2) = @TaxableValue * 0.025;
    DECLARE @SGST DECIMAL(18,2) = @TaxableValue * 0.025;

    EXEC sp_RiceSales_Insert
        @SaleDate = @SaleDate,
        @InvoiceNumber = @InvoiceNum,
        @BuyerName = 'Customer ' + CAST(@i AS VARCHAR),
        @BuyerAddress = 'Address Line ' + CAST(@i AS VARCHAR),
        @BuyerGSTIN = '27AAACR5055K1Z' + CAST(@i AS VARCHAR),
        @RiceGrade = CASE (@i % 3) WHEN 0 THEN 'Premium' WHEN 1 THEN 'Standard' ELSE 'Economy' END,
        @Quantity = @RSQuantity,
        @UnitPrice = @UnitPrice,
        @TotalInvoiceValue = @TotalValue,
        @Discount = 0,
        @TaxableValue = @TaxableValue,
        @CGSTAmount = @CGST,
        @SGSTAmount = @SGST,
        @IGSTAmount = 0,
        @TotalTaxAmount = @CGST + @SGST,
        @FreightCharges = 100,
        @OtherCharges = 50,
        @GrossInvoiceAmount = @TotalValue + @CGST + @SGST + 150,
        @PaymentMode = CASE (@i % 3) WHEN 0 THEN 'Cash' WHEN 1 THEN 'Online' ELSE 'Cheque' END,
        @DueDate = DATEADD(DAY, 30, @SaleDate),
        @PaymentStatus = CASE (@i % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
        @Remarks = 'Test sales record ' + CAST(@i AS VARCHAR),
        @CreatedBy = 'TestUser',
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Rice Sales: 40 records inserted';

-- ============================================
-- 4. BY-PRODUCT SALES - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting By-Product Sales records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @BPSDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @ProductType VARCHAR(100) = CASE (@i % 4)
        WHEN 0 THEN 'Rice Bran'
        WHEN 1 THEN 'Rice Husk'
        WHEN 2 THEN 'Broken Rice'
        ELSE 'Rice Powder'
    END;
    DECLARE @BPSQuantity DECIMAL(18,2) = 200 + (@i * 15);
    DECLARE @BPSRate DECIMAL(18,2) = 15 + (@i % 8);

    EXEC sp_ByProductSales_Insert
        @SaleDate = @BPSDate,
        @TransactionNumber = 'BPS-2024-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @ProductType = @ProductType,
        @BuyerName = 'Buyer ' + CAST(@i AS VARCHAR),
        @BuyerContact = '9876543' + RIGHT('000' + CAST(@i AS VARCHAR), 3),
        @Quantity = @BPSQuantity,
        @Rate = @BPSRate,
        @TotalAmount = @BPSQuantity * @BPSRate,
        @PaymentMode = CASE (@i % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        @PaymentStatus = CASE (@i % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
        @Remarks = 'Test by-product sale ' + CAST(@i AS VARCHAR),
        @CreatedBy = 'TestUser',
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'By-Product Sales: 40 records inserted';

-- ============================================
-- 5. BANK TRANSACTIONS - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Bank Transaction records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @BTDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @IsDeposit BIT = CASE WHEN @i % 2 = 0 THEN 1 ELSE 0 END;
    DECLARE @Amount DECIMAL(18,2) = 5000 + (@i * 500);

    EXEC sp_BankTransactions_Insert
        @TransactionDate = @BTDate,
        @ChequeUtrNumber = 'CHQ' + RIGHT('000000' + CAST(@i AS VARCHAR), 6),
        @BankName = CASE (@i % 3) WHEN 0 THEN 'State Bank' WHEN 1 THEN 'HDFC Bank' ELSE 'ICICI Bank' END,
        @AccountNumber = 'ACC100' + CAST(@i AS VARCHAR),
        @Particulars = CASE WHEN @IsDeposit = 1 THEN 'Customer Payment' ELSE 'Supplier Payment' END,
        @Deposits = CASE WHEN @IsDeposit = 1 THEN @Amount ELSE 0 END,
        @Withdrawals = CASE WHEN @IsDeposit = 0 THEN @Amount ELSE 0 END,
        @Balance = 0,
        @Remarks = 'Test transaction ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Bank Transactions: 40 records inserted';

-- ============================================
-- 6. CASH BOOK - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Cash Book records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @CBDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @IsReceipt BIT = CASE WHEN @i % 2 = 0 THEN 1 ELSE 0 END;
    DECLARE @CBAmount DECIMAL(18,2) = 2000 + (@i * 300);

    EXEC sp_CashBook_Insert
        @TransactionDate = @CBDate,
        @VoucherNumber = 'CB-2024-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @Particulars = CASE WHEN @IsReceipt = 1 THEN 'Cash Receipt' ELSE 'Cash Payment' END,
        @Receipts = CASE WHEN @IsReceipt = 1 THEN @CBAmount ELSE 0 END,
        @Payments = CASE WHEN @IsReceipt = 0 THEN @CBAmount ELSE 0 END,
        @Balance = 0,
        @Remarks = 'Test cash book entry ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Cash Book: 40 records inserted';

-- ============================================
-- 7. VOUCHERS - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Voucher records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @VDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @VType VARCHAR(50) = CASE (@i % 4)
        WHEN 0 THEN 'Payment'
        WHEN 1 THEN 'Receipt'
        WHEN 2 THEN 'Journal'
        ELSE 'Contra'
    END;
    DECLARE @VAmount DECIMAL(18,2) = 3000 + (@i * 400);

    EXEC sp_Vouchers_Insert
        @VoucherDate = @VDate,
        @VoucherNumber = 'V-2024-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @VoucherType = @VType,
        @PartyName = 'Party ' + CAST(@i AS VARCHAR),
        @Amount = @VAmount,
        @PaymentMode = CASE (@i % 3) WHEN 0 THEN 'Cash' WHEN 1 THEN 'Bank' ELSE 'Cheque' END,
        @Narration = 'Test voucher entry ' + CAST(@i AS VARCHAR),
        @Remarks = 'Test remark ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Vouchers: 40 records inserted';

-- ============================================
-- 8. LOANS & ADVANCES - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Loans & Advances records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @LADate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @LAType VARCHAR(50) = CASE (@i % 2) WHEN 0 THEN 'Loan Taken' ELSE 'Advance Given' END;
    DECLARE @LAAmount DECIMAL(18,2) = 10000 + (@i * 1000);

    EXEC sp_LoansAdvances_Insert
        @Date = @LADate,
        @TransactionType = @LAType,
        @PartyName = 'Party ' + CAST(@i AS VARCHAR),
        @Amount = @LAAmount,
        @InterestRate = 8.5,
        @DueDate = DATEADD(MONTH, 6, @LADate),
        @Status = CASE (@i % 3) WHEN 0 THEN 'Active' WHEN 1 THEN 'Closed' ELSE 'Overdue' END,
        @Remarks = 'Test loan/advance record ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Loans & Advances: 40 records inserted';

-- ============================================
-- 9. FIXED ASSETS - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Fixed Assets records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @FADate DATE = DATEADD(DAY, -@i * 10, GETDATE());
    DECLARE @AssetType VARCHAR(100) = CASE (@i % 5)
        WHEN 0 THEN 'Machinery'
        WHEN 1 THEN 'Vehicle'
        WHEN 2 THEN 'Building'
        WHEN 3 THEN 'Equipment'
        ELSE 'Furniture'
    END;
    DECLARE @PurchaseValue DECIMAL(18,2) = 50000 + (@i * 5000);

    EXEC sp_FixedAssets_Insert
        @AssetName = 'Asset ' + CAST(@i AS VARCHAR),
        @AssetType = @AssetType,
        @PurchaseDate = @FADate,
        @PurchaseValue = @PurchaseValue,
        @DepreciationRate = 10,
        @CurrentValue = @PurchaseValue * 0.85,
        @Location = 'Location ' + CAST(@i AS VARCHAR),
        @SerialNumber = 'SN-' + RIGHT('00000' + CAST(@i AS VARCHAR), 5),
        @Remarks = 'Test asset record ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Fixed Assets: 40 records inserted';

-- ============================================
-- 10. RECEIVABLES OVERDUE - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Receivables Overdue records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @RODate DATE = DATEADD(DAY, -(@i + 30), GETDATE());
    DECLARE @RODueDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @ROAmount DECIMAL(18,2) = 5000 + (@i * 500);

    EXEC sp_ReceivablesOverdue_Insert
        @InvoiceNumber = 'RO-INV-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @InvoiceDate = @RODate,
        @CustomerName = 'Customer ' + CAST(@i AS VARCHAR),
        @Amount = @ROAmount,
        @DueDate = @RODueDate,
        @OverdueDays = @i,
        @Status = CASE (@i % 3) WHEN 0 THEN 'Follow-up' WHEN 1 THEN 'Legal Notice' ELSE 'Payment Plan' END,
        @Remarks = 'Test receivable record ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Receivables Overdue: 40 records inserted';

-- ============================================
-- 11. PAYABLES OVERDUE - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting Payables Overdue records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @PODate DATE = DATEADD(DAY, -(@i + 30), GETDATE());
    DECLARE @PODueDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @POAmount DECIMAL(18,2) = 7000 + (@i * 600);

    EXEC sp_PayablesOverdue_Insert
        @BillNumber = 'PO-BILL-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @BillDate = @PODate,
        @SupplierName = 'Supplier ' + CAST(@i AS VARCHAR),
        @Amount = @POAmount,
        @DueDate = @PODueDate,
        @OverdueDays = @i,
        @Status = CASE (@i % 3) WHEN 0 THEN 'Pending' WHEN 1 THEN 'Arranged' ELSE 'Partial Payment' END,
        @Remarks = 'Test payable record ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'Payables Overdue: 40 records inserted';

-- ============================================
-- 12. EXTERNAL RICE SALES - 40 Records
-- ============================================
PRINT '';
PRINT 'Inserting External Rice Sales records...';

SET @i = 1;
WHILE @i <= 40
BEGIN
    DECLARE @ERSDate DATE = DATEADD(DAY, -@i, GETDATE());
    DECLARE @ERSQuantity DECIMAL(18,2) = 600 + (@i * 40);
    DECLARE @ERSRate DECIMAL(18,2) = 45 + (@i % 12);

    EXEC sp_ExternalRiceSales_Insert
        @SaleDate = @ERSDate,
        @InvoiceNumber = 'ERS-' + RIGHT('0000' + CAST(@i AS VARCHAR), 4),
        @CustomerName = 'External Customer ' + CAST(@i AS VARCHAR),
        @RiceType = CASE (@i % 4) WHEN 0 THEN 'Basmati' WHEN 1 THEN 'Sona Masuri' WHEN 2 THEN 'IR-64' ELSE 'Ponni' END,
        @Quantity = @ERSQuantity,
        @Rate = @ERSRate,
        @TotalAmount = @ERSQuantity * @ERSRate,
        @PaymentMode = CASE (@i % 2) WHEN 0 THEN 'Cash' ELSE 'Online' END,
        @PaymentStatus = CASE (@i % 2) WHEN 0 THEN 'Paid' ELSE 'Pending' END,
        @Remarks = 'Test external sale ' + CAST(@i AS VARCHAR),
        @NewId = @NewId OUTPUT;

    SET @i = @i + 1;
END

PRINT 'External Rice Sales: 40 records inserted';

-- ============================================
-- SUMMARY
-- ============================================
PRINT '';
PRINT '========================================';
PRINT 'TEST DATA INSERTION COMPLETED';
PRINT '========================================';
PRINT 'Total tables populated: 12';
PRINT 'Records per table: 40';
PRINT 'Total records inserted: 480';
PRINT '';
PRINT 'Tables populated:';
PRINT '  1. PaddyProcurement: 40 records';
PRINT '  2. RiceProcurementExternal: 40 records';
PRINT '  3. RiceSales: 40 records';
PRINT '  4. ByProductSales: 40 records';
PRINT '  5. BankTransactions: 40 records';
PRINT '  6. CashBook: 40 records';
PRINT '  7. Vouchers: 40 records';
PRINT '  8. LoansAdvances: 40 records';
PRINT '  9. FixedAssets: 40 records';
PRINT ' 10. ReceivablesOverdue: 40 records';
PRINT ' 11. PayablesOverdue: 40 records';
PRINT ' 12. ExternalRiceSales: 40 records';
PRINT '';
PRINT 'Data insertion complete! You can now test paging functionality.';
PRINT '========================================';

-- Verify record counts
SELECT 'PaddyProcurement' AS TableName, COUNT(*) AS RecordCount FROM PaddyProcurement WHERE IsActive = 1
UNION ALL
SELECT 'RiceProcurementExternal', COUNT(*) FROM RiceProcurementExternal WHERE IsActive = 1
UNION ALL
SELECT 'RiceSales', COUNT(*) FROM RiceSales WHERE IsActive = 1
UNION ALL
SELECT 'ByProductSales', COUNT(*) FROM ByProductSales WHERE IsActive = 1
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
UNION ALL
SELECT 'ExternalRiceSales', COUNT(*) FROM ExternalRiceSales WHERE IsActive = 1;

GO
