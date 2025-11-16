-- Sprint 2: Warehouse Management Tables
-- Created: 2025-10-06
-- Description: Creates Warehouses and StorageZones tables for inventory management

USE RMMS_Production;
GO

-- Create Warehouses table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Warehouses')
BEGIN
    CREATE TABLE Warehouses (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        WarehouseCode NVARCHAR(20) NOT NULL UNIQUE,
        WarehouseName NVARCHAR(200) NOT NULL,
        Location NVARCHAR(200) NULL,
        Address NVARCHAR(500) NULL,
        City NVARCHAR(100) NULL,
        State NVARCHAR(100) NULL,
        Pincode NVARCHAR(10) NULL,
        TotalCapacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        UsedCapacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        AvailableCapacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        ContactPerson NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NULL,
        Email NVARCHAR(100) NULL,
        WarehouseType NVARCHAR(50) NULL,
        IsTemperatureControlled BIT NOT NULL DEFAULT 0,
        Temperature DECIMAL(5,2) NULL,
        Humidity DECIMAL(5,2) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        Remarks NVARCHAR(500) NULL,
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );

    PRINT 'Table Warehouses created successfully';
END
ELSE
BEGIN
    PRINT 'Table Warehouses already exists';
END
GO

-- Create StorageZones table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'StorageZones')
BEGIN
    CREATE TABLE StorageZones (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        WarehouseId INT NOT NULL,
        ZoneCode NVARCHAR(20) NOT NULL UNIQUE,
        ZoneName NVARCHAR(100) NOT NULL,
        ZoneType NVARCHAR(50) NULL,
        Capacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        UsedCapacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        AvailableCapacity DECIMAL(18,2) NOT NULL DEFAULT 0,
        Temperature DECIMAL(5,2) NULL,
        Humidity DECIMAL(5,2) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        Remarks NVARCHAR(200) NULL,
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_StorageZones_Warehouses FOREIGN KEY (WarehouseId)
            REFERENCES Warehouses(Id) ON DELETE CASCADE
    );

    PRINT 'Table StorageZones created successfully';
END
ELSE
BEGIN
    PRINT 'Table StorageZones already exists';
END
GO

-- Create indexes for better performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Warehouses_WarehouseCode')
BEGIN
    CREATE INDEX IX_Warehouses_WarehouseCode ON Warehouses(WarehouseCode);
    PRINT 'Index IX_Warehouses_WarehouseCode created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Warehouses_Status')
BEGIN
    CREATE INDEX IX_Warehouses_Status ON Warehouses(Status);
    PRINT 'Index IX_Warehouses_Status created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_StorageZones_WarehouseId')
BEGIN
    CREATE INDEX IX_StorageZones_WarehouseId ON StorageZones(WarehouseId);
    PRINT 'Index IX_StorageZones_WarehouseId created';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_StorageZones_ZoneCode')
BEGIN
    CREATE INDEX IX_StorageZones_ZoneCode ON StorageZones(ZoneCode);
    PRINT 'Index IX_StorageZones_ZoneCode created';
END
GO

-- Insert sample warehouse data (optional)
IF NOT EXISTS (SELECT * FROM Warehouses WHERE WarehouseCode = 'WRHS0001')
BEGIN
    INSERT INTO Warehouses (WarehouseCode, WarehouseName, Location, City, State,
                            TotalCapacity, UsedCapacity, AvailableCapacity,
                            WarehouseType, Status, ContactPerson, Mobile, CreatedBy)
    VALUES ('WRHS0001', 'Main Godown', 'Industrial Area', 'Mumbai', 'Maharashtra',
            5000.00, 0.00, 5000.00, 'Main Godown', 'Active',
            'Warehouse Manager', '9876543210', 'System');

    PRINT 'Sample warehouse WRHS0001 inserted';
END
GO

PRINT '';
PRINT '================================================';
PRINT 'Warehouse tables created successfully!';
PRINT 'Tables: Warehouses, StorageZones';
PRINT 'Sprint 2: Warehouse Management - Complete';
PRINT '================================================';
GO
