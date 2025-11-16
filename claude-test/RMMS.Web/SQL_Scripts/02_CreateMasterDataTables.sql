-- Create Master Data Tables for RMMS
-- Run this script to add Customer, Vendor, Product, and Employee tables
-- Date: 2025-10-06

USE RMMS_Production;
GO

-- =============================================
-- 1. CUSTOMERS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Customers')
BEGIN
    CREATE TABLE Customers (
        Id INT PRIMARY KEY IDENTITY(1,1),
        CustomerCode NVARCHAR(20) NOT NULL,
        CustomerName NVARCHAR(200) NOT NULL,
        CustomerType NVARCHAR(50),
        Category NVARCHAR(50),
        GSTIN NVARCHAR(15),
        PAN NVARCHAR(10),
        CreditLimit DECIMAL(18,2),
        CreditDays INT,
        PaymentTerms NVARCHAR(50),
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX),
        ModifiedDate DATETIME,
        ModifiedBy NVARCHAR(MAX),
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT 'Customers table created successfully';
END
ELSE
    PRINT 'Customers table already exists';
GO

-- =============================================
-- 2. CUSTOMER CONTACTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerContacts')
BEGIN
    CREATE TABLE CustomerContacts (
        Id INT PRIMARY KEY IDENTITY(1,1),
        CustomerId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100),
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100),
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerContacts_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );
    PRINT 'CustomerContacts table created successfully';
END
ELSE
    PRINT 'CustomerContacts table already exists';
GO

-- =============================================
-- 3. CUSTOMER ADDRESSES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerAddresses')
BEGIN
    CREATE TABLE CustomerAddresses (
        Id INT PRIMARY KEY IDENTITY(1,1),
        CustomerId INT NOT NULL,
        AddressType NVARCHAR(50) NOT NULL DEFAULT 'Office',
        AddressLine1 NVARCHAR(200) NOT NULL,
        AddressLine2 NVARCHAR(200),
        City NVARCHAR(100) NOT NULL,
        State NVARCHAR(100) NOT NULL,
        Country NVARCHAR(50) DEFAULT 'India',
        Pincode NVARCHAR(10) NOT NULL,
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerAddresses_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );
    PRINT 'CustomerAddresses table created successfully';
END
ELSE
    PRINT 'CustomerAddresses table already exists';
GO

-- =============================================
-- 4. VENDORS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Vendors')
BEGIN
    CREATE TABLE Vendors (
        Id INT PRIMARY KEY IDENTITY(1,1),
        VendorCode NVARCHAR(20) NOT NULL,
        VendorName NVARCHAR(200) NOT NULL,
        VendorType NVARCHAR(50),
        Category NVARCHAR(50),
        GSTIN NVARCHAR(15),
        PAN NVARCHAR(10),
        PaymentTerms NVARCHAR(50),
        BankName NVARCHAR(100),
        BankAccountNumber NVARCHAR(20),
        IFSCCode NVARCHAR(11),
        Rating INT,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX),
        ModifiedDate DATETIME,
        ModifiedBy NVARCHAR(MAX),
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT 'Vendors table created successfully';
END
ELSE
    PRINT 'Vendors table already exists';
GO

-- =============================================
-- 5. VENDOR CONTACTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorContacts')
BEGIN
    CREATE TABLE VendorContacts (
        Id INT PRIMARY KEY IDENTITY(1,1),
        VendorId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100),
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100),
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorContacts_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );
    PRINT 'VendorContacts table created successfully';
END
ELSE
    PRINT 'VendorContacts table already exists';
GO

-- =============================================
-- 6. VENDOR ADDRESSES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorAddresses')
BEGIN
    CREATE TABLE VendorAddresses (
        Id INT PRIMARY KEY IDENTITY(1,1),
        VendorId INT NOT NULL,
        AddressType NVARCHAR(50) NOT NULL DEFAULT 'Office',
        AddressLine1 NVARCHAR(200) NOT NULL,
        AddressLine2 NVARCHAR(200),
        City NVARCHAR(100) NOT NULL,
        State NVARCHAR(100) NOT NULL,
        Country NVARCHAR(50) DEFAULT 'India',
        Pincode NVARCHAR(10) NOT NULL,
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorAddresses_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );
    PRINT 'VendorAddresses table created successfully';
END
ELSE
    PRINT 'VendorAddresses table already exists';
GO

-- =============================================
-- 7. PRODUCTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    CREATE TABLE Products (
        Id INT PRIMARY KEY IDENTITY(1,1),
        ProductCode NVARCHAR(20) NOT NULL,
        ProductName NVARCHAR(200) NOT NULL,
        ProductCategory NVARCHAR(50) NOT NULL,
        ProductType NVARCHAR(100),
        Grade NVARCHAR(50),
        Description NVARCHAR(500),
        UnitOfMeasure NVARCHAR(20) NOT NULL DEFAULT 'Kg',
        UnitWeight DECIMAL(18,3),
        HSNCode NVARCHAR(12),
        GSTRate DECIMAL(5,2),
        StandardCost DECIMAL(18,2),
        SellingPrice DECIMAL(18,2),
        MinimumStockLevel DECIMAL(18,3),
        MaximumStockLevel DECIMAL(18,3),
        ReorderLevel DECIMAL(18,3),
        StorageLocation NVARCHAR(100),
        ShelfLifeDays INT,
        PackagingType NVARCHAR(50),
        IsRawMaterial BIT NOT NULL DEFAULT 0,
        IsFinishedProduct BIT NOT NULL DEFAULT 0,
        IsByProduct BIT NOT NULL DEFAULT 0,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX),
        ModifiedDate DATETIME,
        ModifiedBy NVARCHAR(MAX),
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT 'Products table created successfully';
END
ELSE
    PRINT 'Products table already exists';
GO

-- =============================================
-- 8. EMPLOYEES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    CREATE TABLE Employees (
        Id INT PRIMARY KEY IDENTITY(1,1),
        EmployeeCode NVARCHAR(20) NOT NULL,
        EmployeeName NVARCHAR(100) NOT NULL,
        Department NVARCHAR(50),
        Designation NVARCHAR(100),
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100),
        DateOfJoining DATE,
        DateOfBirth DATE,
        Address NVARCHAR(200),
        City NVARCHAR(100),
        State NVARCHAR(100),
        Pincode NVARCHAR(10),
        AadharNumber NVARCHAR(12),
        PAN NVARCHAR(10),
        BasicSalary DECIMAL(18,2),
        EmploymentType NVARCHAR(50),
        BankAccountNumber NVARCHAR(100),
        IFSCCode NVARCHAR(11),
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX),
        ModifiedDate DATETIME,
        ModifiedBy NVARCHAR(MAX),
        IsActive BIT NOT NULL DEFAULT 1
    );
    PRINT 'Employees table created successfully';
END
ELSE
    PRINT 'Employees table already exists';
GO

-- =============================================
-- 9. CREATE INDEXES FOR PERFORMANCE
-- =============================================
-- Customers indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Customers_CustomerCode')
    CREATE UNIQUE INDEX IX_Customers_CustomerCode ON Customers(CustomerCode);

-- Vendors indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Vendors_VendorCode')
    CREATE UNIQUE INDEX IX_Vendors_VendorCode ON Vendors(VendorCode);

-- Products indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_ProductCode')
    CREATE UNIQUE INDEX IX_Products_ProductCode ON Products(ProductCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Products_Category')
    CREATE INDEX IX_Products_Category ON Products(ProductCategory);

-- Employees indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_EmployeeCode')
    CREATE UNIQUE INDEX IX_Employees_EmployeeCode ON Employees(EmployeeCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_Department')
    CREATE INDEX IX_Employees_Department ON Employees(Department);

PRINT 'Indexes created successfully';
GO

PRINT '========================================';
PRINT 'Master Data Tables Created Successfully!';
PRINT '========================================';
PRINT 'Tables created:';
PRINT '  1. Customers';
PRINT '  2. CustomerContacts';
PRINT '  3. CustomerAddresses';
PRINT '  4. Vendors';
PRINT '  5. VendorContacts';
PRINT '  6. VendorAddresses';
PRINT '  7. Products';
PRINT '  8. Employees';
PRINT '';
PRINT 'Indexes created for better performance';
PRINT '========================================';
GO
