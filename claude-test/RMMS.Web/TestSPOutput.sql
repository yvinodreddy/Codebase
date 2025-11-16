-- Test that stored procedures return data
USE RMMS_Production;
GO

PRINT 'Testing ByProductSales SP:';
SELECT COUNT(*) AS RowCount FROM ByProductSales WHERE IsActive = 1;
EXEC sp_ByProductSales_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing ExternalRiceSales SP:';
SELECT COUNT(*) AS RowCount FROM ExternalRiceSales WHERE IsActive = 1;
EXEC sp_ExternalRiceSales_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing LoansAdvances SP:';
SELECT COUNT(*) AS RowCount FROM LoansAdvances WHERE IsActive = 1;
EXEC sp_LoansAdvances_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing FixedAssets SP:';
SELECT COUNT(*) AS RowCount FROM FixedAssets WHERE IsActive = 1;
EXEC sp_FixedAssets_GetAll @IsActiveOnly = 1;

GO
