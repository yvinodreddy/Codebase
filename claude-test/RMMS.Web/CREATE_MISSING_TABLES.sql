-- =====================================================
-- CREATE MISSING MASTER DATA AND INVENTORY TABLES
-- =====================================================
-- This script creates all missing tables that the application expects
-- =====================================================

USE RMMS_Production;
GO

PRINT '======================================================';
PRINT 'CREATING MISSING TABLES';
PRINT '======================================================';
PRINT '';

-- =====================================================
-- TABLE: Products
-- =====================================================
PRINT 'Creating Products table...';

IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL
BEGIN
    PRINT '  - Products table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.Products
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ProductCode NVARCHAR(20) NOT NULL UNIQUE,
        ProductName NVARCHAR(100) NOT NULL,
        ProductCategory NVARCHAR(50) NOT NULL, -- Rice, Paddy, ByProduct
        ProductType NVARCHAR(50) NULL,
        Grade NVARCHAR(50) NULL,
        Description NVARCHAR(500) NULL,
        UOM NVARCHAR(20) NOT NULL DEFAULT 'Quintals',
        MinimumStock DECIMAL(18,3) NULL DEFAULT 0,
        ReorderLevel DECIMAL(18,3) NULL DEFAULT 0,
        MaximumStock DECIMAL(18,3) NULL DEFAULT 0,
        StandardCost DECIMAL(18,2) NULL DEFAULT 0,
        SellingPrice DECIMAL(18,2) NULL DEFAULT 0,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL
    );

    CREATE NONCLUSTERED INDEX IX_Products_Code ON dbo.Products(ProductCode);
    CREATE NONCLUSTERED INDEX IX_Products_Category ON dbo.Products(ProductCategory);
    CREATE NONCLUSTERED INDEX IX_Products_Active ON dbo.Products(IsActive);

    PRINT '  ✓ Products table created successfully!';
END
GO

-- =====================================================
-- TABLE: Employees
-- =====================================================
PRINT 'Creating Employees table...';

IF OBJECT_ID('dbo.Employees', 'U') IS NOT NULL
BEGIN
    PRINT '  - Employees table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.Employees
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        EmployeeCode NVARCHAR(20) NOT NULL UNIQUE,
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100) NULL,
        Phone NVARCHAR(20) NULL,
        DateOfBirth DATE NULL,
        DateOfJoining DATE NOT NULL,
        Department NVARCHAR(50) NULL,
        Designation NVARCHAR(50) NULL,
        Salary DECIMAL(18,2) NULL,
        Address NVARCHAR(500) NULL,
        City NVARCHAR(50) NULL,
        State NVARCHAR(50) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL
    );

    CREATE NONCLUSTERED INDEX IX_Employees_Code ON dbo.Employees(EmployeeCode);
    CREATE NONCLUSTERED INDEX IX_Employees_Active ON dbo.Employees(IsActive);

    PRINT '  ✓ Employees table created successfully!';
END
GO

-- =====================================================
-- TABLE: Vendors
-- =====================================================
PRINT 'Creating Vendors table...';

IF OBJECT_ID('dbo.Vendors', 'U') IS NOT NULL
BEGIN
    PRINT '  - Vendors table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.Vendors
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorCode NVARCHAR(20) NOT NULL UNIQUE,
        VendorName NVARCHAR(100) NOT NULL,
        VendorType NVARCHAR(50) NULL,
        ContactPerson NVARCHAR(100) NULL,
        Email NVARCHAR(100) NULL,
        Phone NVARCHAR(20) NULL,
        Address NVARCHAR(500) NULL,
        City NVARCHAR(50) NULL,
        State NVARCHAR(50) NULL,
        PinCode NVARCHAR(10) NULL,
        GSTIN NVARCHAR(15) NULL,
        PAN NVARCHAR(10) NULL,
        CreditLimit DECIMAL(18,2) NULL DEFAULT 0,
        CreditDays INT NULL DEFAULT 0,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL
    );

    CREATE NONCLUSTERED INDEX IX_Vendors_Code ON dbo.Vendors(VendorCode);
    CREATE NONCLUSTERED INDEX IX_Vendors_Active ON dbo.Vendors(IsActive);

    PRINT '  ✓ Vendors table created successfully!';
END
GO

-- =====================================================
-- TABLE: StorageZones
-- =====================================================
PRINT 'Creating StorageZones table...';

IF OBJECT_ID('dbo.StorageZones', 'U') IS NOT NULL
BEGIN
    PRINT '  - StorageZones table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.StorageZones
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        WarehouseId INT NOT NULL,
        ZoneCode NVARCHAR(20) NOT NULL,
        ZoneName NVARCHAR(100) NOT NULL,
        ZoneType NVARCHAR(50) NULL,
        Capacity DECIMAL(18,3) NULL DEFAULT 0,
        CurrentStock DECIMAL(18,3) NULL DEFAULT 0,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        CONSTRAINT FK_StorageZones_Warehouse FOREIGN KEY (WarehouseId) REFERENCES dbo.Warehouses(Id),
        CONSTRAINT UQ_StorageZones_Code UNIQUE (WarehouseId, ZoneCode)
    );

    CREATE NONCLUSTERED INDEX IX_StorageZones_Warehouse ON dbo.StorageZones(WarehouseId);

    PRINT '  ✓ StorageZones table created successfully!';
END
GO

-- =====================================================
-- TABLE: InventoryLedger
-- =====================================================
PRINT 'Creating InventoryLedger table...';

IF OBJECT_ID('dbo.InventoryLedger', 'U') IS NOT NULL
BEGIN
    PRINT '  - InventoryLedger table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.InventoryLedger
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ProductId INT NOT NULL,
        WarehouseId INT NOT NULL,
        ZoneId INT NULL,
        CurrentQuantity DECIMAL(18,3) NOT NULL DEFAULT 0,
        MinimumStock DECIMAL(18,3) NULL DEFAULT 0,
        ReorderLevel DECIMAL(18,3) NULL DEFAULT 0,
        MaximumStock DECIMAL(18,3) NULL DEFAULT 0,
        LastUpdated DATETIME NOT NULL DEFAULT GETDATE(),
        UpdatedBy NVARCHAR(100) NULL,
        CONSTRAINT FK_InventoryLedger_Product FOREIGN KEY (ProductId) REFERENCES dbo.Products(Id),
        CONSTRAINT FK_InventoryLedger_Warehouse FOREIGN KEY (WarehouseId) REFERENCES dbo.Warehouses(Id),
        CONSTRAINT FK_InventoryLedger_Zone FOREIGN KEY (ZoneId) REFERENCES dbo.StorageZones(Id),
        CONSTRAINT UQ_InventoryLedger UNIQUE (ProductId, WarehouseId, ZoneId)
    );

    CREATE NONCLUSTERED INDEX IX_InventoryLedger_Product ON dbo.InventoryLedger(ProductId);
    CREATE NONCLUSTERED INDEX IX_InventoryLedger_Warehouse ON dbo.InventoryLedger(WarehouseId);

    PRINT '  ✓ InventoryLedger table created successfully!';
END
GO

-- =====================================================
-- TABLE: StockMovements
-- =====================================================
PRINT 'Creating StockMovements table...';

IF OBJECT_ID('dbo.StockMovements', 'U') IS NOT NULL
BEGIN
    PRINT '  - StockMovements table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.StockMovements
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        MovementNumber NVARCHAR(20) NOT NULL UNIQUE,
        MovementDate DATETIME NOT NULL DEFAULT GETDATE(),
        MovementType NVARCHAR(20) NOT NULL, -- IN, OUT
        MovementCategory NVARCHAR(50) NULL, -- Procurement, Sales, Production, Transfer, Adjustment, Return
        ProductId INT NOT NULL,
        WarehouseId INT NOT NULL,
        ZoneId INT NULL,
        Quantity DECIMAL(18,3) NOT NULL,
        UnitCost DECIMAL(18,2) NULL DEFAULT 0,
        TotalCost DECIMAL(18,2) NULL DEFAULT 0,
        ReferenceType NVARCHAR(50) NULL,
        ReferenceId INT NULL,
        ReferenceNumber NVARCHAR(50) NULL,
        Remarks NVARCHAR(500) NULL,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        CONSTRAINT FK_StockMovements_Product FOREIGN KEY (ProductId) REFERENCES dbo.Products(Id),
        CONSTRAINT FK_StockMovements_Warehouse FOREIGN KEY (WarehouseId) REFERENCES dbo.Warehouses(Id),
        CONSTRAINT FK_StockMovements_Zone FOREIGN KEY (ZoneId) REFERENCES dbo.StorageZones(Id)
    );

    CREATE NONCLUSTERED INDEX IX_StockMovements_Product ON dbo.StockMovements(ProductId);
    CREATE NONCLUSTERED INDEX IX_StockMovements_Warehouse ON dbo.StockMovements(WarehouseId);
    CREATE NONCLUSTERED INDEX IX_StockMovements_Date ON dbo.StockMovements(MovementDate DESC);
    CREATE NONCLUSTERED INDEX IX_StockMovements_Number ON dbo.StockMovements(MovementNumber);

    PRINT '  ✓ StockMovements table created successfully!';
END
GO

-- =====================================================
-- TABLE: StockAdjustments
-- =====================================================
PRINT 'Creating StockAdjustments table...';

IF OBJECT_ID('dbo.StockAdjustments', 'U') IS NOT NULL
BEGIN
    PRINT '  - StockAdjustments table already exists';
END
ELSE
BEGIN
    CREATE TABLE dbo.StockAdjustments
    (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        AdjustmentNumber NVARCHAR(20) NOT NULL UNIQUE,
        AdjustmentDate DATETIME NOT NULL DEFAULT GETDATE(),
        AdjustmentType NVARCHAR(20) NOT NULL, -- Increase, Decrease, Transfer
        AdjustmentReason NVARCHAR(100) NULL,
        ProductId INT NOT NULL,
        WarehouseId INT NOT NULL,
        ZoneId INT NULL,
        QuantityBefore DECIMAL(18,3) NOT NULL DEFAULT 0,
        QuantityAdjusted DECIMAL(18,3) NOT NULL,
        QuantityAfter DECIMAL(18,3) NOT NULL DEFAULT 0,
        RequiresApproval BIT NOT NULL DEFAULT 1,
        IsApproved BIT NULL,
        ApprovedBy NVARCHAR(100) NULL,
        ApprovedDate DATETIME NULL,
        Remarks NVARCHAR(500) NULL,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_StockAdjustments_Product FOREIGN KEY (ProductId) REFERENCES dbo.Products(Id),
        CONSTRAINT FK_StockAdjustments_Warehouse FOREIGN KEY (WarehouseId) REFERENCES dbo.Warehouses(Id),
        CONSTRAINT FK_StockAdjustments_Zone FOREIGN KEY (ZoneId) REFERENCES dbo.StorageZones(Id)
    );

    CREATE NONCLUSTERED INDEX IX_StockAdjustments_Product ON dbo.StockAdjustments(ProductId);
    CREATE NONCLUSTERED INDEX IX_StockAdjustments_Warehouse ON dbo.StockAdjustments(WarehouseId);
    CREATE NONCLUSTERED INDEX IX_StockAdjustments_Date ON dbo.StockAdjustments(AdjustmentDate DESC);
    CREATE NONCLUSTERED INDEX IX_StockAdjustments_Number ON dbo.StockAdjustments(AdjustmentNumber);

    PRINT '  ✓ StockAdjustments table created successfully!';
END
GO

-- =====================================================
-- SUMMARY
-- =====================================================
PRINT '';
PRINT '======================================================';
PRINT 'MISSING TABLES CREATED SUCCESSFULLY!';
PRINT '======================================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  1. ✓ Products (Master Data)';
PRINT '  2. ✓ Employees (Master Data)';
PRINT '  3. ✓ Vendors (Master Data)';
PRINT '  4. ✓ StorageZones (Inventory)';
PRINT '  5. ✓ InventoryLedger (Inventory)';
PRINT '  6. ✓ StockMovements (Inventory)';
PRINT '  7. ✓ StockAdjustments (Inventory)';
PRINT '';
PRINT 'The application should now work properly!';
PRINT '';
PRINT '======================================================';
GO
