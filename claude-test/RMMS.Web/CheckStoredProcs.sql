-- Check what stored procedures return
USE RMMS_Production;
GO

PRINT 'Testing stored procedures...';
PRINT '============================';

-- Test ByProductSales_GetAll
PRINT 'Testing sp_ByProductSales_GetAll...';
EXEC sp_ByProductSales_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_ExternalRiceSales_GetAll...';
EXEC sp_ExternalRiceSales_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_RiceProcurementExternal_GetAll...';
EXEC sp_RiceProcurementExternal_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_LoansAdvances_GetAll...';
EXEC sp_LoansAdvances_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_FixedAssets_GetAll...';
EXEC sp_FixedAssets_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_Vouchers_GetAll...';
EXEC sp_Vouchers_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_ReceivablesOverdue_GetAll...';
EXEC sp_ReceivablesOverdue_GetAll @IsActiveOnly = 1;

PRINT '';
PRINT 'Testing sp_PayablesOverdue_GetAll...';
EXEC sp_PayablesOverdue_GetAll @IsActiveOnly = 1;

GO

-- Also check the actual stored procedure definitions
PRINT '';
PRINT 'Checking sp_ByProductSales_GetAll definition...';
EXEC sp_helptext 'sp_ByProductSales_GetAll';
GO
