-- Create InventoryLedger table for Sprint 2 - Inventory Management

USE RMMS_Production;
GO

-- Drop table if exists (for testing)
IF OBJECT_ID('InventoryLedger', 'U') IS NOT NULL
    DROP TABLE InventoryLedger;
GO

-- Create InventoryLedger table
CREATE TABLE InventoryLedger
(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ProductId INT NOT NULL,
    WarehouseId INT NOT NULL,
    ZoneId INT NULL,
    CurrentStock DECIMAL(18,3) NOT NULL DEFAULT 0,
    MinimumLevel DECIMAL(18,3) NOT NULL DEFAULT 0,
    MaximumLevel DECIMAL(18,3) NOT NULL DEFAULT 0,
    ReorderLevel DECIMAL(18,3) NOT NULL DEFAULT 0,
    UnitCost DECIMAL(18,2) NOT NULL DEFAULT 0,
    TotalValue DECIMAL(18,2) NOT NULL DEFAULT 0,
    LastMovementDate DATETIME NULL,
    LastUpdated DATETIME NOT NULL DEFAULT GETDATE(),
    Remarks NVARCHAR(500) NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedBy NVARCHAR(100) NULL,
    ModifiedDate DATETIME NULL,
    ModifiedBy NVARCHAR(100) NULL,
    IsActive BIT NOT NULL DEFAULT 1,

    -- Foreign key constraints
    CONSTRAINT FK_InventoryLedger_Product FOREIGN KEY (ProductId) REFERENCES Products(Id),
    CONSTRAINT FK_InventoryLedger_Warehouse FOREIGN KEY (WarehouseId) REFERENCES Warehouses(Id),
    CONSTRAINT FK_InventoryLedger_Zone FOREIGN KEY (ZoneId) REFERENCES StorageZones(Id) ON DELETE SET NULL
);
GO

-- Create unique index for Product + Warehouse + Zone combination
CREATE UNIQUE INDEX IX_InventoryLedger_Product_Warehouse_Zone
ON InventoryLedger(ProductId, WarehouseId, ZoneId);
GO

-- Create indexes for better query performance
CREATE INDEX IX_InventoryLedger_ProductId ON InventoryLedger(ProductId);
GO

CREATE INDEX IX_InventoryLedger_WarehouseId ON InventoryLedger(WarehouseId);
GO

CREATE INDEX IX_InventoryLedger_CurrentStock ON InventoryLedger(CurrentStock);
GO

CREATE INDEX IX_InventoryLedger_LowStock ON InventoryLedger(CurrentStock, MinimumLevel)
WHERE IsActive = 1;
GO

CREATE INDEX IX_InventoryLedger_ReorderRequired ON InventoryLedger(CurrentStock, ReorderLevel)
WHERE IsActive = 1;
GO

PRINT 'InventoryLedger table created successfully!';
GO
