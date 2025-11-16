-- ============================================================
-- DATABASE SCHEMA FIX SCRIPT
-- Purpose: Add missing columns to Warehouses and StorageZones
-- Created: 2025-10-06
-- Issue: Tables were created with old schema, missing Sprint 2 columns
-- ============================================================

USE RMMS_Production;
GO

PRINT '============================================================';
PRINT 'Starting Database Schema Fix';
PRINT 'Adding missing columns to Warehouses and StorageZones tables';
PRINT '============================================================';
PRINT '';

-- ============================================================
-- FIX WAREHOUSES TABLE
-- ============================================================

PRINT 'Checking Warehouses table...';

-- Add UsedCapacity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'UsedCapacity')
BEGIN
    ALTER TABLE Warehouses ADD UsedCapacity DECIMAL(18,2) NOT NULL DEFAULT 0;
    PRINT '✓ Added column: Warehouses.UsedCapacity';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.UsedCapacity';
END
GO

-- Add AvailableCapacity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'AvailableCapacity')
BEGIN
    ALTER TABLE Warehouses ADD AvailableCapacity DECIMAL(18,2) NOT NULL DEFAULT 0;
    PRINT '✓ Added column: Warehouses.AvailableCapacity';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.AvailableCapacity';
END
GO

-- Add Temperature column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'Temperature')
BEGIN
    ALTER TABLE Warehouses ADD Temperature DECIMAL(5,2) NULL;
    PRINT '✓ Added column: Warehouses.Temperature';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.Temperature';
END
GO

-- Add Humidity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'Humidity')
BEGIN
    ALTER TABLE Warehouses ADD Humidity DECIMAL(5,2) NULL;
    PRINT '✓ Added column: Warehouses.Humidity';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.Humidity';
END
GO

-- Add Status column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'Status')
BEGIN
    ALTER TABLE Warehouses ADD Status NVARCHAR(20) NOT NULL DEFAULT 'Active';
    PRINT '✓ Added column: Warehouses.Status';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.Status';
END
GO

-- Add Remarks column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Warehouses') AND name = 'Remarks')
BEGIN
    ALTER TABLE Warehouses ADD Remarks NVARCHAR(500) NULL;
    PRINT '✓ Added column: Warehouses.Remarks';
END
ELSE
BEGIN
    PRINT '  Column already exists: Warehouses.Remarks';
END
GO

-- ============================================================
-- FIX STORAGEZONES TABLE
-- ============================================================

PRINT '';
PRINT 'Checking StorageZones table...';

-- Add UsedCapacity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'UsedCapacity')
BEGIN
    ALTER TABLE StorageZones ADD UsedCapacity DECIMAL(18,2) NOT NULL DEFAULT 0;
    PRINT '✓ Added column: StorageZones.UsedCapacity';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.UsedCapacity';
END
GO

-- Add AvailableCapacity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'AvailableCapacity')
BEGIN
    ALTER TABLE StorageZones ADD AvailableCapacity DECIMAL(18,2) NOT NULL DEFAULT 0;
    PRINT '✓ Added column: StorageZones.AvailableCapacity';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.AvailableCapacity';
END
GO

-- Add Temperature column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'Temperature')
BEGIN
    ALTER TABLE StorageZones ADD Temperature DECIMAL(5,2) NULL;
    PRINT '✓ Added column: StorageZones.Temperature';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.Temperature';
END
GO

-- Add Humidity column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'Humidity')
BEGIN
    ALTER TABLE StorageZones ADD Humidity DECIMAL(5,2) NULL;
    PRINT '✓ Added column: StorageZones.Humidity';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.Humidity';
END
GO

-- Add Status column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'Status')
BEGIN
    ALTER TABLE StorageZones ADD Status NVARCHAR(20) NOT NULL DEFAULT 'Active';
    PRINT '✓ Added column: StorageZones.Status';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.Status';
END
GO

-- Add Remarks column if missing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('StorageZones') AND name = 'Remarks')
BEGIN
    ALTER TABLE StorageZones ADD Remarks NVARCHAR(200) NULL;
    PRINT '✓ Added column: StorageZones.Remarks';
END
ELSE
BEGIN
    PRINT '  Column already exists: StorageZones.Remarks';
END
GO

-- ============================================================
-- UPDATE EXISTING DATA (Calculate AvailableCapacity)
-- ============================================================

PRINT '';
PRINT 'Updating calculated fields...';

-- Update AvailableCapacity for existing warehouses
UPDATE Warehouses
SET AvailableCapacity = TotalCapacity - UsedCapacity
WHERE AvailableCapacity = 0 AND TotalCapacity > 0;

PRINT '✓ Updated AvailableCapacity for Warehouses';

-- Update AvailableCapacity for existing storage zones
UPDATE StorageZones
SET AvailableCapacity = Capacity - UsedCapacity
WHERE AvailableCapacity = 0 AND Capacity > 0;

PRINT '✓ Updated AvailableCapacity for StorageZones';
GO

-- ============================================================
-- CREATE INDEXES FOR NEW COLUMNS (if needed)
-- ============================================================

PRINT '';
PRINT 'Checking indexes...';

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Warehouses_Status' AND object_id = OBJECT_ID('Warehouses'))
BEGIN
    CREATE INDEX IX_Warehouses_Status ON Warehouses(Status);
    PRINT '✓ Created index: IX_Warehouses_Status';
END
ELSE
BEGIN
    PRINT '  Index already exists: IX_Warehouses_Status';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_StorageZones_Status' AND object_id = OBJECT_ID('StorageZones'))
BEGIN
    CREATE INDEX IX_StorageZones_Status ON StorageZones(Status);
    PRINT '✓ Created index: IX_StorageZones_Status';
END
ELSE
BEGIN
    PRINT '  Index already exists: IX_StorageZones_Status';
END
GO

-- ============================================================
-- VERIFICATION
-- ============================================================

PRINT '';
PRINT '============================================================';
PRINT 'Verification - Checking final schema:';
PRINT '============================================================';

DECLARE @WarehouseColumns INT;
DECLARE @StorageZoneColumns INT;

SELECT @WarehouseColumns = COUNT(*)
FROM sys.columns
WHERE object_id = OBJECT_ID('Warehouses')
AND name IN ('UsedCapacity', 'AvailableCapacity', 'Temperature', 'Humidity', 'Status', 'Remarks');

SELECT @StorageZoneColumns = COUNT(*)
FROM sys.columns
WHERE object_id = OBJECT_ID('StorageZones')
AND name IN ('UsedCapacity', 'AvailableCapacity', 'Temperature', 'Humidity', 'Status', 'Remarks');

PRINT 'Warehouses table: ' + CAST(@WarehouseColumns AS VARCHAR) + '/6 required columns present';
PRINT 'StorageZones table: ' + CAST(@StorageZoneColumns AS VARCHAR) + '/6 required columns present';

IF @WarehouseColumns = 6 AND @StorageZoneColumns = 6
BEGIN
    PRINT '';
    PRINT '✓✓✓ SUCCESS! All missing columns have been added! ✓✓✓';
    PRINT '';
    PRINT 'You can now:';
    PRINT '1. Restart the application';
    PRINT '2. Test the Warehouses module';
    PRINT '3. Test the Dashboard';
END
ELSE
BEGIN
    PRINT '';
    PRINT '⚠ WARNING: Some columns may still be missing!';
    PRINT 'Please review the output above for details.';
END

PRINT '';
PRINT '============================================================';
PRINT 'Database Schema Fix Complete';
PRINT '============================================================';
GO
