-- =============================================
-- RMMS Master Data Tables Migration Script
-- Creates: Customers, Vendors, Products, Employees
-- and related tables (Contacts, Addresses)
-- =============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Creating Master Data Tables';
PRINT '========================================';

-- =============================================
-- 1. CUSTOMERS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Customers')
BEGIN
    PRINT 'Creating Customers table...';

    CREATE TABLE Customers (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerCode NVARCHAR(20) NOT NULL UNIQUE,
        CustomerName NVARCHAR(200) NOT NULL,
        CustomerType NVARCHAR(50) NULL,
        Category NVARCHAR(50) NULL,
        GSTIN NVARCHAR(15) NULL,
        PAN NVARCHAR(10) NULL,
        CreditLimit DECIMAL(18,2) NULL,
        CreditDays INT NULL,
        PaymentTerms NVARCHAR(50) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );

    CREATE INDEX IX_Customers_CustomerCode ON Customers(CustomerCode);
    CREATE INDEX IX_Customers_CustomerName ON Customers(CustomerName);
    CREATE INDEX IX_Customers_Status ON Customers(Status);
    CREATE INDEX IX_Customers_IsActive ON Customers(IsActive);

    PRINT 'Customers table created successfully!';
END
ELSE
    PRINT 'Customers table already exists.';
GO

-- =============================================
-- 2. CUSTOMER CONTACTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerContacts')
BEGIN
    PRINT 'Creating CustomerContacts table...';

    CREATE TABLE CustomerContacts (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100) NULL,
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerContacts_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );

    CREATE INDEX IX_CustomerContacts_CustomerId ON CustomerContacts(CustomerId);
    CREATE INDEX IX_CustomerContacts_IsPrimary ON CustomerContacts(IsPrimary);

    PRINT 'CustomerContacts table created successfully!';
END
ELSE
    PRINT 'CustomerContacts table already exists.';
GO

-- =============================================
-- 3. CUSTOMER ADDRESSES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerAddresses')
BEGIN
    PRINT 'Creating CustomerAddresses table...';

    CREATE TABLE CustomerAddresses (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CustomerId INT NOT NULL,
        AddressType NVARCHAR(50) NOT NULL DEFAULT 'Billing',
        AddressLine1 NVARCHAR(200) NOT NULL,
        AddressLine2 NVARCHAR(200) NULL,
        City NVARCHAR(100) NOT NULL,
        State NVARCHAR(100) NOT NULL,
        Country NVARCHAR(50) NOT NULL DEFAULT 'India',
        Pincode NVARCHAR(10) NOT NULL,
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_CustomerAddresses_Customers FOREIGN KEY (CustomerId)
            REFERENCES Customers(Id) ON DELETE CASCADE
    );

    CREATE INDEX IX_CustomerAddresses_CustomerId ON CustomerAddresses(CustomerId);
    CREATE INDEX IX_CustomerAddresses_IsDefault ON CustomerAddresses(IsDefault);

    PRINT 'CustomerAddresses table created successfully!';
END
ELSE
    PRINT 'CustomerAddresses table already exists.';
GO

-- =============================================
-- 4. VENDORS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Vendors')
BEGIN
    PRINT 'Creating Vendors table...';

    CREATE TABLE Vendors (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorCode NVARCHAR(20) NOT NULL UNIQUE,
        VendorName NVARCHAR(200) NOT NULL,
        VendorType NVARCHAR(50) NULL,
        Category NVARCHAR(50) NULL,
        GSTIN NVARCHAR(15) NULL,
        PAN NVARCHAR(10) NULL,
        PaymentTerms NVARCHAR(50) NULL,
        BankName NVARCHAR(100) NULL,
        BankAccountNumber NVARCHAR(20) NULL,
        IFSCCode NVARCHAR(11) NULL,
        Rating INT NULL CHECK (Rating BETWEEN 1 AND 5),
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );

    CREATE INDEX IX_Vendors_VendorCode ON Vendors(VendorCode);
    CREATE INDEX IX_Vendors_VendorName ON Vendors(VendorName);
    CREATE INDEX IX_Vendors_Status ON Vendors(Status);
    CREATE INDEX IX_Vendors_IsActive ON Vendors(IsActive);

    PRINT 'Vendors table created successfully!';
END
ELSE
    PRINT 'Vendors table already exists.';
GO

-- =============================================
-- 5. VENDOR CONTACTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorContacts')
BEGIN
    PRINT 'Creating VendorContacts table...';

    CREATE TABLE VendorContacts (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorId INT NOT NULL,
        ContactPerson NVARCHAR(100) NOT NULL,
        Designation NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100) NULL,
        IsPrimary BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorContacts_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );

    CREATE INDEX IX_VendorContacts_VendorId ON VendorContacts(VendorId);
    CREATE INDEX IX_VendorContacts_IsPrimary ON VendorContacts(IsPrimary);

    PRINT 'VendorContacts table created successfully!';
END
ELSE
    PRINT 'VendorContacts table already exists.';
GO

-- =============================================
-- 6. VENDOR ADDRESSES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'VendorAddresses')
BEGIN
    PRINT 'Creating VendorAddresses table...';

    CREATE TABLE VendorAddresses (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        VendorId INT NOT NULL,
        AddressType NVARCHAR(50) NOT NULL DEFAULT 'Office',
        AddressLine1 NVARCHAR(200) NOT NULL,
        AddressLine2 NVARCHAR(200) NULL,
        City NVARCHAR(100) NOT NULL,
        State NVARCHAR(100) NOT NULL,
        Country NVARCHAR(50) NOT NULL DEFAULT 'India',
        Pincode NVARCHAR(10) NOT NULL,
        IsDefault BIT NOT NULL DEFAULT 0,
        CONSTRAINT FK_VendorAddresses_Vendors FOREIGN KEY (VendorId)
            REFERENCES Vendors(Id) ON DELETE CASCADE
    );

    CREATE INDEX IX_VendorAddresses_VendorId ON VendorAddresses(VendorId);
    CREATE INDEX IX_VendorAddresses_IsDefault ON VendorAddresses(IsDefault);

    PRINT 'VendorAddresses table created successfully!';
END
ELSE
    PRINT 'VendorAddresses table already exists.';
GO

-- =============================================
-- 7. PRODUCTS TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    PRINT 'Creating Products table...';

    CREATE TABLE Products (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ProductCode NVARCHAR(20) NOT NULL UNIQUE,
        ProductName NVARCHAR(200) NOT NULL,
        ProductCategory NVARCHAR(50) NOT NULL,
        ProductType NVARCHAR(100) NULL,
        Grade NVARCHAR(50) NULL,
        Description NVARCHAR(500) NULL,
        UnitOfMeasure NVARCHAR(20) NOT NULL DEFAULT 'Kg',
        UnitWeight DECIMAL(18,3) NULL,
        HSNCode NVARCHAR(12) NULL,
        GSTRate DECIMAL(5,2) NULL,
        StandardCost DECIMAL(18,2) NULL,
        SellingPrice DECIMAL(18,2) NULL,
        MinimumStockLevel DECIMAL(18,3) NULL,
        MaximumStockLevel DECIMAL(18,3) NULL,
        ReorderLevel DECIMAL(18,3) NULL,
        StorageLocation NVARCHAR(100) NULL,
        ShelfLifeDays INT NULL,
        PackagingType NVARCHAR(50) NULL,
        IsRawMaterial BIT NOT NULL DEFAULT 0,
        IsFinishedProduct BIT NOT NULL DEFAULT 0,
        IsByProduct BIT NOT NULL DEFAULT 0,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );

    CREATE INDEX IX_Products_ProductCode ON Products(ProductCode);
    CREATE INDEX IX_Products_ProductName ON Products(ProductName);
    CREATE INDEX IX_Products_ProductCategory ON Products(ProductCategory);
    CREATE INDEX IX_Products_Status ON Products(Status);
    CREATE INDEX IX_Products_IsActive ON Products(IsActive);
    CREATE INDEX IX_Products_IsRawMaterial ON Products(IsRawMaterial);
    CREATE INDEX IX_Products_IsFinishedProduct ON Products(IsFinishedProduct);
    CREATE INDEX IX_Products_IsByProduct ON Products(IsByProduct);

    PRINT 'Products table created successfully!';
END
ELSE
    PRINT 'Products table already exists.';
GO

-- =============================================
-- 8. EMPLOYEES TABLE
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Employees')
BEGIN
    PRINT 'Creating Employees table...';

    CREATE TABLE Employees (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        EmployeeCode NVARCHAR(20) NOT NULL UNIQUE,
        EmployeeName NVARCHAR(100) NOT NULL,
        Department NVARCHAR(50) NULL,
        Designation NVARCHAR(100) NULL,
        Mobile NVARCHAR(15) NOT NULL,
        Email NVARCHAR(100) NULL,
        DateOfJoining DATE NULL,
        DateOfBirth DATE NULL,
        Address NVARCHAR(200) NULL,
        City NVARCHAR(100) NULL,
        State NVARCHAR(100) NULL,
        Pincode NVARCHAR(10) NULL,
        AadharNumber NVARCHAR(12) NULL,
        PAN NVARCHAR(10) NULL,
        BasicSalary DECIMAL(18,2) NULL,
        EmploymentType NVARCHAR(50) NULL,
        BankAccountNumber NVARCHAR(100) NULL,
        IFSCCode NVARCHAR(11) NULL,
        Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedDate DATETIME NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );

    CREATE INDEX IX_Employees_EmployeeCode ON Employees(EmployeeCode);
    CREATE INDEX IX_Employees_EmployeeName ON Employees(EmployeeName);
    CREATE INDEX IX_Employees_Department ON Employees(Department);
    CREATE INDEX IX_Employees_Status ON Employees(Status);
    CREATE INDEX IX_Employees_IsActive ON Employees(IsActive);

    PRINT 'Employees table created successfully!';
END
ELSE
    PRINT 'Employees table already exists.';
GO

PRINT '========================================';
PRINT 'Master Data Tables Migration Complete!';
PRINT '========================================';
PRINT '';
PRINT 'Tables Created:';
PRINT '  1. Customers (with unique CustomerCode)';
PRINT '  2. CustomerContacts';
PRINT '  3. CustomerAddresses';
PRINT '  4. Vendors (with unique VendorCode)';
PRINT '  5. VendorContacts';
PRINT '  6. VendorAddresses';
PRINT '  7. Products (with unique ProductCode)';
PRINT '  8. Employees (with unique EmployeeCode)';
PRINT '';
PRINT 'Total Indexes Created: 33';
PRINT 'Total Foreign Keys: 6';
PRINT '';
