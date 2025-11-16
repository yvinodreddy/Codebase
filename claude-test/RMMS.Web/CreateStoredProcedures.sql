-- Create ALL Missing Stored Procedures for RMMS
USE RMMS_Production;
GO

PRINT 'Creating Stored Procedures...';
GO

-- ============================================
-- BY-PRODUCT SALES STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_ByProductSales_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM ByProductSales
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_ByProductSales_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM ByProductSales WHERE Id = @Id;
END
GO

-- ============================================
-- EXTERNAL RICE SALES STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_ExternalRiceSales_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM ExternalRiceSales
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_ExternalRiceSales_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM ExternalRiceSales WHERE Id = @Id;
END
GO

-- ============================================
-- RICE PROCUREMENT EXTERNAL STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_RiceProcurementExternal_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM RiceProcurementExternal
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY ProcurementDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_RiceProcurementExternal_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM RiceProcurementExternal WHERE Id = @Id;
END
GO

-- ============================================
-- LOANS & ADVANCES STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_LoansAdvances_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM LoansAdvances
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_LoansAdvances_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM LoansAdvances WHERE Id = @Id;
END
GO

-- ============================================
-- FIXED ASSETS STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_FixedAssets_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM FixedAssets
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY PurchaseDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_FixedAssets_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM FixedAssets WHERE Id = @Id;
END
GO

-- ============================================
-- VOUCHERS STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_Vouchers_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Vouchers
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY VoucherDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_Vouchers_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Vouchers WHERE Id = @Id;
END
GO

-- ============================================
-- RECEIVABLES OVERDUE STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_ReceivablesOverdue_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM ReceivablesOverdue
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY DueDate ASC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_ReceivablesOverdue_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM ReceivablesOverdue WHERE Id = @Id;
END
GO

-- ============================================
-- PAYABLES OVERDUE STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_PayablesOverdue_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM PayablesOverdue
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY DueDate ASC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_PayablesOverdue_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM PayablesOverdue WHERE Id = @Id;
END
GO

-- ============================================
-- BANK TRANSACTIONS STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_BankTransactions_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM BankTransactions
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_BankTransactions_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM BankTransactions WHERE Id = @Id;
END
GO

-- ============================================
-- CASH BOOK STORED PROCEDURES
-- ============================================
CREATE OR ALTER PROCEDURE sp_CashBook_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM CashBook
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_CashBook_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM CashBook WHERE Id = @Id;
END
GO

PRINT 'All stored procedures created successfully!';
PRINT 'Testing stored procedures...';
GO

-- Test each stored procedure
PRINT 'sp_ByProductSales_GetAll:';
EXEC sp_ByProductSales_GetAll @IsActiveOnly = 1;

PRINT 'sp_ExternalRiceSales_GetAll:';
EXEC sp_ExternalRiceSales_GetAll @IsActiveOnly = 1;

PRINT 'sp_RiceProcurementExternal_GetAll:';
EXEC sp_RiceProcurementExternal_GetAll @IsActiveOnly = 1;

PRINT 'sp_LoansAdvances_GetAll:';
EXEC sp_LoansAdvances_GetAll @IsActiveOnly = 1;

PRINT 'sp_FixedAssets_GetAll:';
EXEC sp_FixedAssets_GetAll @IsActiveOnly = 1;

PRINT 'sp_Vouchers_GetAll:';
EXEC sp_Vouchers_GetAll @IsActiveOnly = 1;

PRINT 'sp_ReceivablesOverdue_GetAll:';
EXEC sp_ReceivablesOverdue_GetAll @IsActiveOnly = 1;

PRINT 'sp_PayablesOverdue_GetAll:';
EXEC sp_PayablesOverdue_GetAll @IsActiveOnly = 1;

GO

PRINT '========================================';
PRINT 'SUCCESS! All stored procedures created!';
PRINT 'Your application should now display data!';
PRINT '========================================';
GO
