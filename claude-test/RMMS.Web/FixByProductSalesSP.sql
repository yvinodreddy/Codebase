-- Fix ByProductSales stored procedure to include ALL columns
USE RMMS_Production;
GO

-- First check what columns the table actually has
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'ByProductSales'
ORDER BY ORDINAL_POSITION;
GO

-- Now recreate the stored procedure with explicit column list
CREATE OR ALTER PROCEDURE sp_ByProductSales_GetAll
    @IsActiveOnly BIT = 1
AS
BEGIN
    SELECT
        Id,
        SaleDate,
        InvoiceNumber,
        BuyerName,
        BuyerAddress,
        ProductType,
        Quantity,
        UnitPrice,
        TotalAmount,
        PaymentMode,
        PaymentStatus,
        Remarks,
        CreatedDate,
        ModifiedDate,
        CreatedBy,
        ModifiedBy,
        IsActive
    FROM ByProductSales
    WHERE (@IsActiveOnly = 0 OR IsActive = 1)
    ORDER BY SaleDate DESC, Id DESC;
END
GO

-- Test it
EXEC sp_ByProductSales_GetAll @IsActiveOnly = 1;
GO

PRINT 'Stored procedure fixed!';
GO
