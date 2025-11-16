-- List all stored procedures in database
USE RMMS_Production;
GO

SELECT
    ROUTINE_NAME AS StoredProcedure,
    CREATED AS CreatedDate,
    LAST_ALTERED AS LastModified
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
ORDER BY ROUTINE_NAME;
GO
