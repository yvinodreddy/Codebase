-- RMMS Complete Database Setup
-- Creates all Sprint 1 & Sprint 2 tables
-- Run this script to fix all database table issues

USE RMMS_Production;
GO

PRINT '================================================';
PRINT 'RMMS - Creating All Required Tables';
PRINT 'Sprint 1: Master Data + Sprint 2: Warehouses';
PRINT '================================================';
PRINT '';

-- ========================================
-- SPRINT 1: MASTER DATA TABLES
-- ========================================

-- Customers Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Customers')
BEGIN
    CREATE TABLE Customers (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerCode NVARCHAR(20) NOT NULL UNIQUE,
        CustomerName NVARCHAR(200) NOT NULL,
        CustomerType NVARCHAR(50) NULL,
        Category NVARCHAR(10) NULL,
        GSTIN NVARCHAR(15) NULL,
        PAN NVARCHAR(10) NULL,
        CreditLimit DECIMAL(18,2) NULL,
        CreditDays INT NULL,
        PaymentTerms NVARCHAR(100) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT '✓ Created table: Customers';
END
ELSE PRINT '  Table Customers already exists';
GO

-- CustomerContacts Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerContacts')
BEGIN
    CREATE TABLE CustomerContacts (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NULL,
        Email NVARCHAR(100) NULL,
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerContacts_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );
    PRINT '✓ Created table: CustomerContacts';
END
ELSE PRINT '  Table CustomerContacts already exists';
GO

-- CustomerAddresses Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerAddresses')
BEGIN
    CREATE TABLE CustomerAddresses (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerId INT NOT NULL,
        AddressType NVARCHAR(50) NULL,
        AddressLine1 NVARCHAR(200) NULL,
        AddressLine2 NVARCHAR(200) NULL,
        City NVARCHAR(100) NULL,
        State NVARCHAR(100) NULL,
        Pincode NVARCHAR(10) NULL,
        Country NVARCHAR(100) NULL DEFAULT 'India',
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerAddresses_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );
    PRINT '✓ Created table: CustomerAddresses';
END
ELSE PRINT '  Table CustomerAddresses already exists';
GO

-- Vendors Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Vendors')
BEGIN
    CREATE TABLE Vendors (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorCode NVARCHAR(20) NOT NULL UNIQUE,
        VendorName NVARCHAR(200) NOT NULL,
        VendorType NVARCHAR(50) NULL,
        Category NVARCHAR(50) NULL,
        GSTIN NVARCHAR(15) NULL,
        PAN NVARCHAR(10) NULL,
        Rating INT NULL,
        PaymentTerms NVARCHAR(100) NULL,
        BankName NVARCHAR(100) NULL,
        BankAccountNumber NVARCHAR(50) NULL,
        IFSCCode NVARCHAR(20) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT '✓ Created table: Vendors';
END
ELSE PRINT '  Table Vendors already exists';
GO

-- VendorContacts Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorContacts')
BEGIN
    CREATE TABLE VendorContacts (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NULL,
        Email NVARCHAR(100) NULL,
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorContacts_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );
    PRINT '✓ Created table: VendorContacts';
END
ELSE PRINT '  Table VendorContacts already exists';
GO

-- VendorAddresses Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorAddresses')
BEGIN
    CREATE TABLE VendorAddresses (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorId INT NOT NULL,
        AddressType NVARCHAR(50) NULL,
        AddressLine1 NVARCHAR(200) NULL,
        AddressLine2 NVARCHAR(200) NULL,
        City NVARCHAR(100) NULL,
        State NVARCHAR(100) NULL,
        Pincode NVARCHAR(10) NULL,
        Country NVARCHAR(100) NULL DEFAULT 'India',
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorAddresses_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );
    PRINT '✓ Created table: VendorAddresses';
END
ELSE PRINT '  Table VendorAddresses already exists';
GO

-- Products Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    CREATE TABLE Products (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ProductCode NVARCHAR(20) NOT NULL UNIQUE,
        ProductName NVARCHAR(200) NOT NULL,
        Category NVARCHAR(50) NOT NULL,
        ProductType NVARCHAR(50) NULL,
        Brand NVARCHAR(100) NULL,
        Variety NVARCHAR(100) NULL,
        Grade NVARCHAR(50) NULL,
        HSNCode NVARCHAR(20) NULL,
        GSTRate DECIMAL(5,2) NULL,
        BaseUOM NVARCHAR(20) NULL DEFAULT 'KG',
        PackingUOM NVARCHAR(20) NULL,
        ConversionFactor DECIMAL(10,4) NULL,
        MinimumStock DECIMAL(18,2) NULL DEFAULT 0,
        MaximumStock DECIMAL(18,2) NULL DEFAULT 0,
        ReorderLevel DECIMAL(18,2) NULL DEFAULT 0,
        StandardCost DECIMAL(18,2) NULL DEFAULT 0,
        SellingPrice DECIMAL(18,2) NULL DEFAULT 0,
        Description NVARCHAR(500) NULL,
        Specifications NVARCHAR(500) NULL,
        StorageLocation NVARCHAR(100) NULL,
        ShelfLife INT NULL,
        IsPurchasable BIT NOT NULL DEFAULT 1,
        IsSaleable BIT NOT NULL DEFAULT 1,
        IsProducible BIT NOT NULL DEFAULT 0,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT '✓ Created table: Products';
END
ELSE PRINT '  Table Products already exists';
GO

-- Employees Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    CREATE TABLE Employees (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        EmployeeCode NVARCHAR(20) NOT NULL UNIQUE,
        FirstName NVARCHAR(100) NOT NULL,
        LastName NVARCHAR(100) NULL,
        Department NVARCHAR(100) NULL,
        Designation NVARCHAR(100) NULL,
        Email NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NULL,
        DateOfBirth DATE NULL,
        DateOfJoining DATE NULL,
        EmploymentType NVARCHAR(50) NULL,
        Salary DECIMAL(18,2) NULL,
        AadharNumber NVARCHAR(20) NULL,
        PANNumber NVARCHAR(10) NULL,
        BankAccountNumber NVARCHAR(50) NULL,
        BankName NVARCHAR(100) NULL,
        IFSCCode NVARCHAR(20) NULL,
        Address NVARCHAR(500) NULL,
        City NVARCHAR(100) NULL,
        State NVARCHAR(100) NULL,
        Pincode NVARCHAR(10) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT '✓ Created table: Employees';
END
ELSE PRINT '  Table Employees already exists';
GO

PRINT '';
PRINT '================================================';
PRINT 'Sprint 1 Master Data Tables: COMPLETE';
PRINT '================================================';
PRINT '';

-- ========================================
-- SPRINT 2: WAREHOUSE/INVENTORY TABLES
-- ========================================

-- Warehouses Table
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
    PRINT '✓ Created table: Warehouses';
END
ELSE PRINT '  Table Warehouses already exists';
GO

-- StorageZones Table
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
    PRINT '✓ Created table: StorageZones';
END
ELSE PRINT '  Table StorageZones already exists';
GO

PRINT '';
PRINT '================================================';
PRINT 'Sprint 2 Warehouse Tables: COMPLETE';
PRINT '================================================';
PRINT '';

-- ========================================
-- CREATE INDEXES FOR PERFORMANCE
-- ========================================

PRINT 'Creating indexes for better performance...';
PRINT '';

-- Customer indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Customers_CustomerCode')
    CREATE INDEX IX_Customers_CustomerCode ON Customers(CustomerCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Customers_CustomerName')
    CREATE INDEX IX_Customers_CustomerName ON Customers(CustomerName);

-- Vendor indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Vendors_VendorCode')
    CREATE INDEX IX_Vendors_VendorCode ON Vendors(VendorCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Vendors_VendorName')
    CREATE INDEX IX_Vendors_VendorName ON Vendors(VendorName);

-- Product indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_ProductCode')
    CREATE INDEX IX_Products_ProductCode ON Products(ProductCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_Category')
    CREATE INDEX IX_Products_Category ON Products(Category);

-- Employee indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_EmployeeCode')
    CREATE INDEX IX_Employees_EmployeeCode ON Employees(EmployeeCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_Department')
    CREATE INDEX IX_Employees_Department ON Employees(Department);

-- Warehouse indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Warehouses_WarehouseCode')
    CREATE INDEX IX_Warehouses_WarehouseCode ON Warehouses(WarehouseCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_StorageZones_WarehouseId')
    CREATE INDEX IX_StorageZones_WarehouseId ON StorageZones(WarehouseId);

PRINT '✓ All indexes created';
GO

PRINT '';
PRINT '================================================';
PRINT 'DATABASE SETUP COMPLETE!';
PRINT '================================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  Sprint 1: Customers, CustomerContacts, CustomerAddresses';
PRINT '           Vendors, VendorContacts, VendorAddresses';
PRINT '           Products, Employees';
PRINT '  Sprint 2: Warehouses, StorageZones';
PRINT '';
PRINT 'Total Tables: 10';
PRINT 'All indexes created for performance';
PRINT '';
PRINT 'Status: ✓ READY FOR USE';
PRINT '================================================';
GO
