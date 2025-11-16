-- ============================================
-- CREATE ALL MISSING STORED PROCEDURES FOR RMMS
-- This script creates all GetAll and GetById procedures
-- ============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'CREATING ALL STORED PROCEDURES';
PRINT '========================================';
GO

-- ============================================
-- 1. CUSTOMERS
-- ============================================
CREATE OR ALTER PROCEDURE sp_Customers_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Customers
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY CustomerName;
END
GO

CREATE OR ALTER PROCEDURE sp_Customers_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Customers WHERE Id = @Id;
END
GO

-- ============================================
-- 2. VENDORS
-- ============================================
CREATE OR ALTER PROCEDURE sp_Vendors_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Vendors
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY VendorName;
END
GO

CREATE OR ALTER PROCEDURE sp_Vendors_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Vendors WHERE Id = @Id;
END
GO

-- ============================================
-- 3. PRODUCTS
-- ============================================
CREATE OR ALTER PROCEDURE sp_Products_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Products
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY ProductName;
END
GO

CREATE OR ALTER PROCEDURE sp_Products_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Products WHERE Id = @Id;
END
GO

-- ============================================
-- 4. EMPLOYEES
-- ============================================
CREATE OR ALTER PROCEDURE sp_Employees_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Employees
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY EmployeeName;
END
GO

CREATE OR ALTER PROCEDURE sp_Employees_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Employees WHERE Id = @Id;
END
GO

-- ============================================
-- 5. WAREHOUSES
-- ============================================
CREATE OR ALTER PROCEDURE sp_Warehouses_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Warehouses
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY WarehouseName;
END
GO

CREATE OR ALTER PROCEDURE sp_Warehouses_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Warehouses WHERE Id = @Id;
END
GO

-- ============================================
-- 6. MACHINES
-- ============================================
CREATE OR ALTER PROCEDURE sp_Machines_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Machines
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY MachineName;
END
GO

CREATE OR ALTER PROCEDURE sp_Machines_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Machines WHERE Id = @Id;
END
GO

-- ============================================
-- 7. PRODUCTION ORDERS
-- ============================================
CREATE OR ALTER PROCEDURE sp_ProductionOrders_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM ProductionOrders
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY OrderDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_ProductionOrders_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM ProductionOrders WHERE Id = @Id;
END
GO

-- ============================================
-- 8. PRODUCTION BATCHES
-- ============================================
CREATE OR ALTER PROCEDURE sp_ProductionBatches_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM ProductionBatches
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY StartDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_ProductionBatches_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM ProductionBatches WHERE Id = @Id;
END
GO

-- ============================================
-- 9. PADDY PROCUREMENT
-- ============================================
CREATE OR ALTER PROCEDURE sp_PaddyProcurement_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM PaddyProcurement
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY ReceiptDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_PaddyProcurement_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM PaddyProcurement WHERE Id = @Id;
END
GO

-- ============================================
-- 10. RICE SALES
-- ============================================
CREATE OR ALTER PROCEDURE sp_RiceSales_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM RiceSales
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_RiceSales_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM RiceSales WHERE Id = @Id;
END
GO

-- ============================================
-- 11. BY-PRODUCT SALES
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
-- 12. EXTERNAL RICE SALES
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
-- 13. BANK TRANSACTIONS
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
-- 14. CASH BOOK
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

-- ============================================
-- 15. VOUCHERS
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
-- 16. PAYABLES OVERDUE
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
-- 17. RECEIVABLES OVERDUE
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
-- 18. LOANS & ADVANCES
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
-- 19. FIXED ASSETS
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
-- 20. INQUIRIES
-- ============================================
CREATE OR ALTER PROCEDURE sp_Inquiries_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Inquiries
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY InquiryDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_Inquiries_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Inquiries WHERE Id = @Id;
END
GO

-- ============================================
-- 21. QUOTATIONS
-- ============================================
CREATE OR ALTER PROCEDURE sp_Quotations_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM Quotations
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY QuotationDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_Quotations_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM Quotations WHERE Id = @Id;
END
GO

-- ============================================
-- 22. SALES ORDERS
-- ============================================
CREATE OR ALTER PROCEDURE sp_SalesOrders_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM SalesOrders
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY OrderDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_SalesOrders_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM SalesOrders WHERE Id = @Id;
END
GO

-- ============================================
-- 23. STOCK ADJUSTMENTS
-- ============================================
CREATE OR ALTER PROCEDURE sp_StockAdjustments_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM StockAdjustments
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY AdjustmentDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_StockAdjustments_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM StockAdjustments WHERE Id = @Id;
END
GO

-- ============================================
-- 24. STOCK MOVEMENTS
-- ============================================
CREATE OR ALTER PROCEDURE sp_StockMovements_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM StockMovements
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY MovementDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_StockMovements_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM StockMovements WHERE Id = @Id;
END
GO

-- ============================================
-- 25. INVENTORY LEDGER
-- ============================================
CREATE OR ALTER PROCEDURE sp_InventoryLedger_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT * FROM InventoryLedger
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY TransactionDate DESC, Id DESC;
END
GO

CREATE OR ALTER PROCEDURE sp_InventoryLedger_GetById
    @Id INT
AS
BEGIN
    SELECT * FROM InventoryLedger WHERE Id = @Id;
END
GO

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
PRINT '';
PRINT '========================================';
PRINT 'SUCCESS! ALL STORED PROCEDURES CREATED!';
PRINT '========================================';
PRINT '';

-- List all created procedures
SELECT
    ROUTINE_NAME AS [Stored Procedure],
    CREATED AS [Created Date]
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
AND ROUTINE_NAME LIKE 'sp_%'
ORDER BY ROUTINE_NAME;
GO
