-- =============================================
-- Missing Stored Procedures for Reports
-- Created to fix report functionality
-- =============================================

USE RMMS_Production;
GO

-- =============================================
-- By-Product Sales - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_ByProductSales_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM ByProductSales
    WHERE SaleDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

-- =============================================
-- External Rice Sales - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_ExternalRiceSales_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM ExternalRiceSales
    WHERE SaleDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

-- =============================================
-- Rice Sales - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_RiceSales_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM RiceSales
    WHERE SaleDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

-- =============================================
-- Paddy Procurement - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_PaddyProcurement_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM PaddyProcurement
    WHERE ReceiptDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY ReceiptDate DESC, Id DESC;
END
GO

-- =============================================
-- Bank Transactions - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_BankTransactions_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM BankTransactions
    WHERE TransactionDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

-- =============================================
-- Cash Book - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_CashBook_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM CashBook
    WHERE TransactionDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

-- =============================================
-- Vouchers - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_Vouchers_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM Vouchers
    WHERE VoucherDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY VoucherDate DESC, Id DESC;
END
GO

-- =============================================
-- Loans & Advances - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_LoansAdvances_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM LoansAdvances
    WHERE TransactionDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

-- =============================================
-- Fixed Assets - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_FixedAssets_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM FixedAssets
    WHERE PurchaseDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY PurchaseDate DESC, Id DESC;
END
GO

-- =============================================
-- Receivables Overdue - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_ReceivablesOverdue_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM ReceivablesOverdue
    WHERE InvoiceDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY InvoiceDate DESC, Id DESC;
END
GO

-- =============================================
-- Payables Overdue - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_PayablesOverdue_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM PayablesOverdue
    WHERE PurchaseDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY PurchaseDate DESC, Id DESC;
END
GO

-- =============================================
-- Rice Procurement External - GetByDateRange
-- =============================================
CREATE OR ALTER PROCEDURE sp_RiceProcurementExternal_GetByDateRange
    @StartDate DATE,
    @EndDate DATE,
    @IsActiveOnly BIT = 1
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM RiceProcurementExternal
    WHERE ProcurementDate BETWEEN @StartDate AND @EndDate
        AND (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY ProcurementDate DESC, Id DESC;
END
GO

PRINT 'All missing report stored procedures created successfully!';
