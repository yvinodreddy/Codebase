-- Create StockMovements table for Sprint 2 - Inventory Management

USE RMMS_Production;
GO

-- Drop table if exists (for testing)
IF OBJECT_ID('StockMovements', 'U') IS NOT NULL
    DROP TABLE StockMovements;
GO

-- Create StockMovements table
CREATE TABLE StockMovements
(
    Id INT IDENTITY(1,1) PRIMARY KEY,
    MovementCode NVARCHAR(20) NOT NULL,
    ProductId INT NOT NULL,
    WarehouseId INT NOT NULL,
    ZoneId INT NULL,
    MovementType NVARCHAR(10) NOT NULL, -- IN, OUT
    MovementCategory NVARCHAR(50) NOT NULL, -- Procurement, Sales, Production, Transfer, Adjustment, Return
    Quantity DECIMAL(18,3) NOT NULL,
    UnitCost DECIMAL(18,2) NOT NULL DEFAULT 0,
    TotalCost DECIMAL(18,2) NOT NULL DEFAULT 0,
    ReferenceType NVARCHAR(50) NULL,
    ReferenceId INT NULL,
    ReferenceNumber NVARCHAR(50) NULL,
    MovementDate DATETIME NOT NULL DEFAULT GETDATE(),
    PerformedBy NVARCHAR(100) NULL,
    Remarks NVARCHAR(500) NULL,
    IsApproved BIT NOT NULL DEFAULT 1,
    ApprovedBy NVARCHAR(100) NULL,
    ApprovalDate DATETIME NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedBy NVARCHAR(100) NULL,
    ModifiedDate DATETIME NULL,
    ModifiedBy NVARCHAR(100) NULL,
    IsActive BIT NOT NULL DEFAULT 1,

    -- Foreign key constraints
    CONSTRAINT FK_StockMovements_Product FOREIGN KEY (ProductId) REFERENCES Products(Id),
    CONSTRAINT FK_StockMovements_Warehouse FOREIGN KEY (WarehouseId) REFERENCES Warehouses(Id),
    CONSTRAINT FK_StockMovements_Zone FOREIGN KEY (ZoneId) REFERENCES StorageZones(Id) ON DELETE SET NULL
);
GO

-- Create unique index on MovementCode
CREATE UNIQUE INDEX IX_StockMovements_MovementCode
ON StockMovements(MovementCode);
GO

-- Create indexes for better query performance
CREATE INDEX IX_StockMovements_ProductId ON StockMovements(ProductId);
GO

CREATE INDEX IX_StockMovements_WarehouseId ON StockMovements(WarehouseId);
GO

CREATE INDEX IX_StockMovements_MovementDate ON StockMovements(MovementDate);
GO

CREATE INDEX IX_StockMovements_MovementType ON StockMovements(MovementType);
GO

CREATE INDEX IX_StockMovements_MovementCategory ON StockMovements(MovementCategory);
GO

PRINT 'StockMovements table created successfully!';
GO
