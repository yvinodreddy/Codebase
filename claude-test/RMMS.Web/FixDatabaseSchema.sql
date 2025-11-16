-- Fix Database Schema Issues
-- Add missing TotalValue column to InventoryLedger if it doesn't exist

USE RMMS_Production;
GO

-- Check and add TotalValue to InventoryLedger
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS
               WHERE TABLE_NAME = 'InventoryLedger'
               AND COLUMN_NAME = 'TotalValue')
BEGIN
    ALTER TABLE InventoryLedger
    ADD TotalValue decimal(18,2) NOT NULL DEFAULT 0;
    PRINT 'Added TotalValue column to InventoryLedger';
END
ELSE
BEGIN
    PRINT 'TotalValue column already exists in InventoryLedger';
END
GO

-- Update TotalValue for existing records
UPDATE InventoryLedger
SET TotalValue = CurrentStock * UnitCost
WHERE TotalValue = 0 OR TotalValue IS NULL;
GO

PRINT 'Database schema fixed successfully';
GO
