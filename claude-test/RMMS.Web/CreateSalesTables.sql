-- Create Sales Tables for RMMS
-- Date: 2025-10-07
-- Description: Creates Inquiries, Quotations, QuotationItems, SalesOrders, and SalesOrderItems tables

USE RMMS_Production;
GO

-- Table 1: Inquiries
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Inquiries')
BEGIN
    CREATE TABLE Inquiries (
        Id INT PRIMARY KEY IDENTITY(1,1),
        InquiryNumber NVARCHAR(20) NOT NULL UNIQUE,
        InquiryDate DATETIME2 NOT NULL,
        CustomerId INT NOT NULL,
        Source NVARCHAR(50) NOT NULL,
        ProductType NVARCHAR(100) NULL,
        ApproximateQuantity DECIMAL(18,3) NULL,
        UnitOfMeasure NVARCHAR(20) NULL,
        ExpectedDeliveryDate DATETIME2 NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'New',
        AssignedToEmployeeId INT NULL,
        Priority NVARCHAR(50) NOT NULL DEFAULT 'Normal',
        CustomerRequirements NVARCHAR(1000) NULL,
        Remarks NVARCHAR(500) NULL,
        FollowUpDate DATETIME2 NULL,
        LostReason NVARCHAR(50) NULL,
        ConvertedToQuotationId INT NULL,
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(MAX) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Inquiries_Customers FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
        CONSTRAINT FK_Inquiries_Employees FOREIGN KEY (AssignedToEmployeeId) REFERENCES Employees(Id)
    );
    PRINT 'Table Inquiries created successfully';
END
ELSE
BEGIN
    PRINT 'Table Inquiries already exists';
END
GO

-- Table 2: Quotations
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Quotations')
BEGIN
    CREATE TABLE Quotations (
        Id INT PRIMARY KEY IDENTITY(1,1),
        QuotationNumber NVARCHAR(20) NOT NULL UNIQUE,
        QuotationDate DATETIME2 NOT NULL,
        InquiryId INT NULL,
        CustomerId INT NOT NULL,
        ValidUntil DATETIME2 NOT NULL,
        PaymentTerms NVARCHAR(200) NULL,
        DeliveryTerms NVARCHAR(200) NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Draft',
        SubTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
        DiscountAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TaxAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TermsAndConditions NVARCHAR(MAX) NULL,
        ApprovedBy INT NULL,
        ApprovedDate DATETIME2 NULL,
        ConvertedToSalesOrderId INT NULL,
        Remarks NVARCHAR(500) NULL,
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(MAX) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Quotations_Inquiries FOREIGN KEY (InquiryId) REFERENCES Inquiries(Id),
        CONSTRAINT FK_Quotations_Customers FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
        CONSTRAINT FK_Quotations_Employees FOREIGN KEY (ApprovedBy) REFERENCES Employees(Id)
    );
    PRINT 'Table Quotations created successfully';
END
ELSE
BEGIN
    PRINT 'Table Quotations already exists';
END
GO

-- Table 3: QuotationItems
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'QuotationItems')
BEGIN
    CREATE TABLE QuotationItems (
        Id INT PRIMARY KEY IDENTITY(1,1),
        QuotationId INT NOT NULL,
        ProductId INT NOT NULL,
        Description NVARCHAR(500) NULL,
        Quantity DECIMAL(18,3) NOT NULL,
        UnitOfMeasure NVARCHAR(20) NULL,
        UnitPrice DECIMAL(18,2) NOT NULL,
        DiscountPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
        DiscountAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TaxPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
        TaxAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        LineTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
        CONSTRAINT FK_QuotationItems_Quotations FOREIGN KEY (QuotationId) REFERENCES Quotations(Id) ON DELETE CASCADE,
        CONSTRAINT FK_QuotationItems_Products FOREIGN KEY (ProductId) REFERENCES Products(Id)
    );
    PRINT 'Table QuotationItems created successfully';
END
ELSE
BEGIN
    PRINT 'Table QuotationItems already exists';
END
GO

-- Table 4: SalesOrders
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SalesOrders')
BEGIN
    CREATE TABLE SalesOrders (
        Id INT PRIMARY KEY IDENTITY(1,1),
        OrderNumber NVARCHAR(20) NOT NULL UNIQUE,
        OrderDate DATETIME2 NOT NULL,
        QuotationId INT NULL,
        CustomerId INT NOT NULL,
        DeliveryDate DATETIME2 NULL,
        DeliveryAddress NVARCHAR(MAX) NULL,
        PaymentTerms NVARCHAR(200) NULL,
        DeliveryTerms NVARCHAR(200) NULL,
        Status NVARCHAR(50) NOT NULL DEFAULT 'Pending',
        Priority NVARCHAR(50) NOT NULL DEFAULT 'Normal',
        SubTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
        DiscountAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TaxAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        FreightCharges DECIMAL(18,2) NOT NULL DEFAULT 0,
        OtherCharges DECIMAL(18,2) NOT NULL DEFAULT 0,
        TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        SpecialInstructions NVARCHAR(MAX) NULL,
        IsStockReserved BIT NOT NULL DEFAULT 0,
        ApprovedBy INT NULL,
        ApprovedDate DATETIME2 NULL,
        Remarks NVARCHAR(500) NULL,
        CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(MAX) NULL,
        ModifiedDate DATETIME2 NULL,
        ModifiedBy NVARCHAR(MAX) NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_SalesOrders_Quotations FOREIGN KEY (QuotationId) REFERENCES Quotations(Id),
        CONSTRAINT FK_SalesOrders_Customers FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
        CONSTRAINT FK_SalesOrders_Employees FOREIGN KEY (ApprovedBy) REFERENCES Employees(Id)
    );
    PRINT 'Table SalesOrders created successfully';
END
ELSE
BEGIN
    PRINT 'Table SalesOrders already exists';
END
GO

-- Table 5: SalesOrderItems
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SalesOrderItems')
BEGIN
    CREATE TABLE SalesOrderItems (
        Id INT PRIMARY KEY IDENTITY(1,1),
        SalesOrderId INT NOT NULL,
        ProductId INT NOT NULL,
        WarehouseId INT NULL,
        Description NVARCHAR(500) NULL,
        Quantity DECIMAL(18,3) NOT NULL,
        AllocatedQuantity DECIMAL(18,3) NOT NULL DEFAULT 0,
        DispatchedQuantity DECIMAL(18,3) NOT NULL DEFAULT 0,
        UnitOfMeasure NVARCHAR(20) NULL,
        UnitPrice DECIMAL(18,2) NOT NULL,
        DiscountPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
        DiscountAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        TaxPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
        TaxAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
        LineTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
        CONSTRAINT FK_SalesOrderItems_SalesOrders FOREIGN KEY (SalesOrderId) REFERENCES SalesOrders(Id) ON DELETE CASCADE,
        CONSTRAINT FK_SalesOrderItems_Products FOREIGN KEY (ProductId) REFERENCES Products(Id),
        CONSTRAINT FK_SalesOrderItems_Warehouses FOREIGN KEY (WarehouseId) REFERENCES Warehouses(Id)
    );
    PRINT 'Table SalesOrderItems created successfully';
END
ELSE
BEGIN
    PRINT 'Table SalesOrderItems already exists';
END
GO

PRINT 'Sales tables creation script completed successfully!';
GO
