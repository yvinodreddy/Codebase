-- Test Data Insertion Script for RMMS System (Simplified)
-- This script inserts 40 records for each table to test paging functionality

USE RMMS_Production;
GO

PRINT 'Starting test data insertion...';
GO

-- ============================================
-- 1. PADDY PROCUREMENT - 40 Records
-- ============================================
PRINT 'Inserting Paddy Procurement records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @ReceiptDate DATE;
DECLARE @VoucherNum NVARCHAR(50);
DECLARE @SupplierName NVARCHAR(200);
DECLARE @PaddyVariety NVARCHAR(100);
DECLARE @Grade NVARCHAR(50);
DECLARE @Quantity DECIMAL(18,2);
DECLARE @Weight DECIMAL(18,2);

WHILE @Counter <= 40
BEGIN
    SET @ReceiptDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @VoucherNum = N'PP-2024-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);
    SET @SupplierName = N'Supplier ' + CAST(@Counter AS NVARCHAR);

    SET @PaddyVariety = CASE (@Counter % 5)
        WHEN 0 THEN N'Basmati'
        WHEN 1 THEN N'Sona Masuri'
        WHEN 2 THEN N'IR-64'
        WHEN 3 THEN N'Swarna'
        ELSE N'Ponni'
    END;

    SET @Grade = CASE (@Counter % 3)
        WHEN 0 THEN N'Grade A'
        WHEN 1 THEN N'Grade B'
        ELSE N'Grade C'
    END;

    SET @Quantity = 1000 + (@Counter * 50);
    SET @Weight = @Quantity * 1.05;

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
        @StorageLocation = N'Warehouse A',
        @OpeningStock = 0,
        @Issues = 0,
        @ClosingStock = @Quantity,
        @LossShrinkage = 0,
        @Remarks = N'Test data',
        @ResponsiblePerson = N'Manager',
        @CreatedBy = N'TestUser',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Paddy Procurement: 40 records inserted';
GO

-- ============================================
-- 2. RICE PROCUREMENT EXTERNAL - 40 Records
-- ============================================
PRINT 'Inserting Rice Procurement External records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @RPEDate DATE;
DECLARE @ItemDesc NVARCHAR(200);
DECLARE @RPEQuantity DECIMAL(18,2);
DECLARE @RPERate DECIMAL(18,2);

WHILE @Counter <= 40
BEGIN
    SET @RPEDate = DATEADD(DAY, -@Counter, GETDATE());

    SET @ItemDesc = CASE (@Counter % 4)
        WHEN 0 THEN N'Mansuri'
        WHEN 1 THEN N'Katrni'
        WHEN 2 THEN N'Sonam'
        ELSE N'Premium Rice'
    END;

    SET @RPEQuantity = 500 + (@Counter * 25);
    SET @RPERate = 40 + (@Counter % 10);

    EXEC sp_RiceProcurementExternal_Insert
        @Date = @RPEDate,
        @ItemDescription = @ItemDesc,
        @ProcuredFrom = N'Supplier',
        @ProcuredBy = N'Buyer',
        @Quantity = @RPEQuantity,
        @Rate = @RPERate,
        @TotalAmount = @RPEQuantity * @RPERate,
        @PaymentMode = CASE (@Counter % 2) WHEN 0 THEN N'Cash' ELSE N'Online' END,
        @PaymentStatus = CASE (@Counter % 3) WHEN 0 THEN N'Paid' WHEN 1 THEN N'Pending' ELSE N'Partial' END,
        @Balance = CASE (@Counter % 3) WHEN 0 THEN 0 ELSE (@RPEQuantity * @RPERate * 0.3) END,
        @FullPaymentDate = NULL,
        @Remarks = N'Test procurement',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Rice Procurement External: 40 records inserted';
GO

-- ============================================
-- 3. RICE SALES - 40 Records
-- ============================================
PRINT 'Inserting Rice Sales records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @SaleDate DATE;
DECLARE @InvoiceNum NVARCHAR(50);
DECLARE @RSQuantity DECIMAL(18,2);
DECLARE @UnitPrice DECIMAL(18,2);
DECLARE @TotalValue DECIMAL(18,2);
DECLARE @TaxableValue DECIMAL(18,2);
DECLARE @CGST DECIMAL(18,2);
DECLARE @SGST DECIMAL(18,2);

WHILE @Counter <= 40
BEGIN
    SET @SaleDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @InvoiceNum = N'INV-2024-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);
    SET @RSQuantity = 800 + (@Counter * 30);
    SET @UnitPrice = 50 + (@Counter % 15);
    SET @TotalValue = @RSQuantity * @UnitPrice;
    SET @TaxableValue = @TotalValue;
    SET @CGST = @TaxableValue * 0.025;
    SET @SGST = @TaxableValue * 0.025;

    EXEC sp_RiceSales_Insert
        @SaleDate = @SaleDate,
        @InvoiceNumber = @InvoiceNum,
        @BuyerName = N'Customer',
        @BuyerAddress = N'Address',
        @BuyerGSTIN = N'27AAACR5055K1Z1',
        @RiceGrade = CASE (@Counter % 3) WHEN 0 THEN N'Premium' WHEN 1 THEN N'Standard' ELSE N'Economy' END,
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
        @PaymentMode = CASE (@Counter % 3) WHEN 0 THEN N'Cash' WHEN 1 THEN N'Online' ELSE N'Cheque' END,
        @DueDate = DATEADD(DAY, 30, @SaleDate),
        @PaymentStatus = CASE (@Counter % 2) WHEN 0 THEN N'Paid' ELSE N'Pending' END,
        @Remarks = N'Test sales',
        @CreatedBy = N'TestUser',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Rice Sales: 40 records inserted';
GO

-- ============================================
-- 4. BY-PRODUCT SALES - 40 Records
-- ============================================
PRINT 'Inserting By-Product Sales records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @BPSDate DATE;
DECLARE @ProductType NVARCHAR(100);
DECLARE @BPSQuantity DECIMAL(18,2);
DECLARE @BPSRate DECIMAL(18,2);
DECLARE @TransNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @BPSDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @TransNum = N'BPS-2024-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    SET @ProductType = CASE (@Counter % 4)
        WHEN 0 THEN N'Rice Bran'
        WHEN 1 THEN N'Rice Husk'
        WHEN 2 THEN N'Broken Rice'
        ELSE N'Rice Powder'
    END;

    SET @BPSQuantity = 200 + (@Counter * 15);
    SET @BPSRate = 15 + (@Counter % 8);

    EXEC sp_ByProductSales_Insert
        @SaleDate = @BPSDate,
        @TransactionNumber = @TransNum,
        @ProductType = @ProductType,
        @BuyerName = N'Buyer',
        @BuyerContact = N'9876543210',
        @Quantity = @BPSQuantity,
        @Rate = @BPSRate,
        @TotalAmount = @BPSQuantity * @BPSRate,
        @PaymentMode = CASE (@Counter % 2) WHEN 0 THEN N'Cash' ELSE N'Online' END,
        @PaymentStatus = CASE (@Counter % 2) WHEN 0 THEN N'Paid' ELSE N'Pending' END,
        @Remarks = N'Test by-product',
        @CreatedBy = N'TestUser',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'By-Product Sales: 40 records inserted';
GO

-- ============================================
-- 5. BANK TRANSACTIONS - 40 Records
-- ============================================
PRINT 'Inserting Bank Transaction records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @BTDate DATE;
DECLARE @IsDeposit BIT;
DECLARE @Amount DECIMAL(18,2);
DECLARE @ChequeNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @BTDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @IsDeposit = CASE WHEN @Counter % 2 = 0 THEN 1 ELSE 0 END;
    SET @Amount = 5000 + (@Counter * 500);
    SET @ChequeNum = N'CHQ' + RIGHT(N'000000' + CAST(@Counter AS NVARCHAR), 6);

    EXEC sp_BankTransactions_Insert
        @TransactionDate = @BTDate,
        @ChequeUtrNumber = @ChequeNum,
        @BankName = CASE (@Counter % 3) WHEN 0 THEN N'State Bank' WHEN 1 THEN N'HDFC Bank' ELSE N'ICICI Bank' END,
        @AccountNumber = N'ACC1001',
        @Particulars = CASE WHEN @IsDeposit = 1 THEN N'Customer Payment' ELSE N'Supplier Payment' END,
        @Deposits = CASE WHEN @IsDeposit = 1 THEN @Amount ELSE 0 END,
        @Withdrawals = CASE WHEN @IsDeposit = 0 THEN @Amount ELSE 0 END,
        @Balance = 0,
        @Remarks = N'Test transaction',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Bank Transactions: 40 records inserted';
GO

-- ============================================
-- 6. CASH BOOK - 40 Records
-- ============================================
PRINT 'Inserting Cash Book records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @CBDate DATE;
DECLARE @IsReceipt BIT;
DECLARE @CBAmount DECIMAL(18,2);
DECLARE @VoucherNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @CBDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @IsReceipt = CASE WHEN @Counter % 2 = 0 THEN 1 ELSE 0 END;
    SET @CBAmount = 2000 + (@Counter * 300);
    SET @VoucherNum = N'CB-2024-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    EXEC sp_CashBook_Insert
        @TransactionDate = @CBDate,
        @VoucherNumber = @VoucherNum,
        @Particulars = CASE WHEN @IsReceipt = 1 THEN N'Cash Receipt' ELSE N'Cash Payment' END,
        @Receipts = CASE WHEN @IsReceipt = 1 THEN @CBAmount ELSE 0 END,
        @Payments = CASE WHEN @IsReceipt = 0 THEN @CBAmount ELSE 0 END,
        @Balance = 0,
        @Remarks = N'Test cash book',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Cash Book: 40 records inserted';
GO

-- ============================================
-- 7. VOUCHERS - 40 Records
-- ============================================
PRINT 'Inserting Voucher records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @VDate DATE;
DECLARE @VType NVARCHAR(50);
DECLARE @VAmount DECIMAL(18,2);
DECLARE @VoucherNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @VDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @VoucherNum = N'V-2024-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    SET @VType = CASE (@Counter % 4)
        WHEN 0 THEN N'Payment'
        WHEN 1 THEN N'Receipt'
        WHEN 2 THEN N'Journal'
        ELSE N'Contra'
    END;

    SET @VAmount = 3000 + (@Counter * 400);

    EXEC sp_Vouchers_Insert
        @VoucherDate = @VDate,
        @VoucherNumber = @VoucherNum,
        @VoucherType = @VType,
        @PartyName = N'Party',
        @Amount = @VAmount,
        @PaymentMode = CASE (@Counter % 3) WHEN 0 THEN N'Cash' WHEN 1 THEN N'Bank' ELSE N'Cheque' END,
        @Narration = N'Test voucher',
        @Remarks = N'Test remark',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Vouchers: 40 records inserted';
GO

-- ============================================
-- 8. LOANS & ADVANCES - 40 Records
-- ============================================
PRINT 'Inserting Loans & Advances records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @LADate DATE;
DECLARE @LAType NVARCHAR(50);
DECLARE @LAAmount DECIMAL(18,2);

WHILE @Counter <= 40
BEGIN
    SET @LADate = DATEADD(DAY, -@Counter, GETDATE());
    SET @LAType = CASE (@Counter % 2) WHEN 0 THEN N'Loan Taken' ELSE N'Advance Given' END;
    SET @LAAmount = 10000 + (@Counter * 1000);

    EXEC sp_LoansAdvances_Insert
        @Date = @LADate,
        @TransactionType = @LAType,
        @PartyName = N'Party',
        @Amount = @LAAmount,
        @InterestRate = 8.5,
        @DueDate = DATEADD(MONTH, 6, @LADate),
        @Status = CASE (@Counter % 3) WHEN 0 THEN N'Active' WHEN 1 THEN N'Closed' ELSE N'Overdue' END,
        @Remarks = N'Test loan',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Loans & Advances: 40 records inserted';
GO

-- ============================================
-- 9. FIXED ASSETS - 40 Records
-- ============================================
PRINT 'Inserting Fixed Assets records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @FADate DATE;
DECLARE @AssetType NVARCHAR(100);
DECLARE @PurchaseValue DECIMAL(18,2);
DECLARE @SerialNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @FADate = DATEADD(DAY, -@Counter * 10, GETDATE());
    SET @SerialNum = N'SN-' + RIGHT(N'00000' + CAST(@Counter AS NVARCHAR), 5);

    SET @AssetType = CASE (@Counter % 5)
        WHEN 0 THEN N'Machinery'
        WHEN 1 THEN N'Vehicle'
        WHEN 2 THEN N'Building'
        WHEN 3 THEN N'Equipment'
        ELSE N'Furniture'
    END;

    SET @PurchaseValue = 50000 + (@Counter * 5000);

    EXEC sp_FixedAssets_Insert
        @AssetName = N'Asset',
        @AssetType = @AssetType,
        @PurchaseDate = @FADate,
        @PurchaseValue = @PurchaseValue,
        @DepreciationRate = 10,
        @CurrentValue = @PurchaseValue * 0.85,
        @Location = N'Location 1',
        @SerialNumber = @SerialNum,
        @Remarks = N'Test asset',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Fixed Assets: 40 records inserted';
GO

-- ============================================
-- 10. RECEIVABLES OVERDUE - 40 Records
-- ============================================
PRINT 'Inserting Receivables Overdue records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @RODate DATE;
DECLARE @RODueDate DATE;
DECLARE @ROAmount DECIMAL(18,2);
DECLARE @InvNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @RODate = DATEADD(DAY, -(@Counter + 30), GETDATE());
    SET @RODueDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @ROAmount = 5000 + (@Counter * 500);
    SET @InvNum = N'RO-INV-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    EXEC sp_ReceivablesOverdue_Insert
        @InvoiceNumber = @InvNum,
        @InvoiceDate = @RODate,
        @CustomerName = N'Customer',
        @Amount = @ROAmount,
        @DueDate = @RODueDate,
        @OverdueDays = @Counter,
        @Status = CASE (@Counter % 3) WHEN 0 THEN N'Follow-up' WHEN 1 THEN N'Legal Notice' ELSE N'Payment Plan' END,
        @Remarks = N'Test receivable',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Receivables Overdue: 40 records inserted';
GO

-- ============================================
-- 11. PAYABLES OVERDUE - 40 Records
-- ============================================
PRINT 'Inserting Payables Overdue records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @PODate DATE;
DECLARE @PODueDate DATE;
DECLARE @POAmount DECIMAL(18,2);
DECLARE @BillNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @PODate = DATEADD(DAY, -(@Counter + 30), GETDATE());
    SET @PODueDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @POAmount = 7000 + (@Counter * 600);
    SET @BillNum = N'PO-BILL-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    EXEC sp_PayablesOverdue_Insert
        @BillNumber = @BillNum,
        @BillDate = @PODate,
        @SupplierName = N'Supplier',
        @Amount = @POAmount,
        @DueDate = @PODueDate,
        @OverdueDays = @Counter,
        @Status = CASE (@Counter % 3) WHEN 0 THEN N'Pending' WHEN 1 THEN N'Arranged' ELSE N'Partial Payment' END,
        @Remarks = N'Test payable',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'Payables Overdue: 40 records inserted';
GO

-- ============================================
-- 12. EXTERNAL RICE SALES - 40 Records
-- ============================================
PRINT 'Inserting External Rice Sales records...';

DECLARE @Counter INT = 1;
DECLARE @NewId INT;
DECLARE @ERSDate DATE;
DECLARE @ERSQuantity DECIMAL(18,2);
DECLARE @ERSRate DECIMAL(18,2);
DECLARE @InvNum NVARCHAR(50);

WHILE @Counter <= 40
BEGIN
    SET @ERSDate = DATEADD(DAY, -@Counter, GETDATE());
    SET @ERSQuantity = 600 + (@Counter * 40);
    SET @ERSRate = 45 + (@Counter % 12);
    SET @InvNum = N'ERS-' + RIGHT(N'0000' + CAST(@Counter AS NVARCHAR), 4);

    EXEC sp_ExternalRiceSales_Insert
        @SaleDate = @ERSDate,
        @InvoiceNumber = @InvNum,
        @CustomerName = N'External Customer',
        @RiceType = CASE (@Counter % 4) WHEN 0 THEN N'Basmati' WHEN 1 THEN N'Sona Masuri' WHEN 2 THEN N'IR-64' ELSE N'Ponni' END,
        @Quantity = @ERSQuantity,
        @Rate = @ERSRate,
        @TotalAmount = @ERSQuantity * @ERSRate,
        @PaymentMode = CASE (@Counter % 2) WHEN 0 THEN N'Cash' ELSE N'Online' END,
        @PaymentStatus = CASE (@Counter % 2) WHEN 0 THEN N'Paid' ELSE N'Pending' END,
        @Remarks = N'Test external sale',
        @NewId = @NewId OUTPUT;

    SET @Counter = @Counter + 1;
END

PRINT 'External Rice Sales: 40 records inserted';
GO

PRINT '========================================';
PRINT 'TEST DATA INSERTION COMPLETED!';
PRINT '========================================';
GO
