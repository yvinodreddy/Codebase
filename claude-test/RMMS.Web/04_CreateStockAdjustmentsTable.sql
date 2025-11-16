-- =====================================================
-- CREATE STOCK ADJUSTMENTS TABLE
-- =====================================================
-- Sprint 2: Inventory Management - Stock Adjustments Module
-- This script creates the StockAdjustments table with approval workflow
-- Run this script after creating the StockMovements table
-- =====================================================

USE RMMS_Production;
GO

-- Drop table if exists (for clean reinstall)
IF OBJECT_ID('dbo.StockAdjustments', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing StockAdjustments table...';
    DROP TABLE dbo.StockAdjustments;
END
GO

-- Create StockAdjustments table
CREATE TABLE dbo.StockAdjustments
(
    Id INT IDENTITY(1,1) PRIMARY KEY,

    -- Adjustment Information
    AdjustmentCode NVARCHAR(20) NOT NULL UNIQUE,
    ProductId INT NOT NULL,
    WarehouseId INT NOT NULL,
    ZoneId INT NULL,

    -- Adjustment Details
    AdjustmentType NVARCHAR(20) NOT NULL,  -- Increase, Decrease, Transfer
    Quantity DECIMAL(18,3) NOT NULL,
    Reason NVARCHAR(50) NOT NULL,  -- Damage, Theft, Spoilage, Counting Error, Physical Verification, Moisture Loss, Other

    -- Quantities
    BeforeQuantity DECIMAL(18,3) NOT NULL DEFAULT 0,
    AfterQuantity DECIMAL(18,3) NOT NULL DEFAULT 0,

    -- Dates
    AdjustmentDate DATETIME NOT NULL DEFAULT GETDATE(),

    -- Remarks
    Remarks NVARCHAR(500) NULL,

    -- Approval Workflow
    RequiresApproval BIT NOT NULL DEFAULT 1,
    IsApproved BIT NOT NULL DEFAULT 0,
    ApprovedBy NVARCHAR(100) NULL,
    ApprovalDate DATETIME NULL,
    ApprovalRemarks NVARCHAR(500) NULL,

    -- Rejection
    IsRejected BIT NOT NULL DEFAULT 0,
    RejectionReason NVARCHAR(500) NULL,

    -- Audit Fields
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    CreatedBy NVARCHAR(100) NULL,
    ModifiedDate DATETIME NULL,
    ModifiedBy NVARCHAR(100) NULL,
    IsActive BIT NOT NULL DEFAULT 1,

    -- Foreign Key Constraints
    CONSTRAINT FK_StockAdjustments_Products FOREIGN KEY (ProductId)
        REFERENCES dbo.Products(Id),
    CONSTRAINT FK_StockAdjustments_Warehouses FOREIGN KEY (WarehouseId)
        REFERENCES dbo.Warehouses(Id),
    CONSTRAINT FK_StockAdjustments_StorageZones FOREIGN KEY (ZoneId)
        REFERENCES dbo.StorageZones(Id) ON DELETE SET NULL,

    -- Check Constraints
    CONSTRAINT CHK_StockAdjustments_Quantity CHECK (Quantity > 0),
    CONSTRAINT CHK_StockAdjustments_Type CHECK (AdjustmentType IN ('Increase', 'Decrease', 'Transfer')),
    CONSTRAINT CHK_StockAdjustments_AfterQty CHECK (AfterQuantity >= 0)
);
GO

-- Create Indexes for Performance
CREATE NONCLUSTERED INDEX IX_StockAdjustments_ProductId
    ON dbo.StockAdjustments(ProductId)
    INCLUDE (WarehouseId, AdjustmentDate, Quantity);

CREATE NONCLUSTERED INDEX IX_StockAdjustments_WarehouseId
    ON dbo.StockAdjustments(WarehouseId)
    INCLUDE (ProductId, AdjustmentDate, Quantity);

CREATE NONCLUSTERED INDEX IX_StockAdjustments_AdjustmentDate
    ON dbo.StockAdjustments(AdjustmentDate DESC)
    INCLUDE (ProductId, WarehouseId, Quantity, AdjustmentType);

CREATE NONCLUSTERED INDEX IX_StockAdjustments_Approval
    ON dbo.StockAdjustments(RequiresApproval, IsApproved, IsRejected)
    WHERE IsActive = 1;

CREATE NONCLUSTERED INDEX IX_StockAdjustments_Active
    ON dbo.StockAdjustments(IsActive)
    INCLUDE (Id, AdjustmentCode, AdjustmentDate);
GO

PRINT '✓ StockAdjustments table created successfully!';
PRINT '✓ Indexes created for optimal performance';
PRINT '';
PRINT 'Table Details:';
PRINT '- Primary Key: Id (Identity)';
PRINT '- Unique Constraint: AdjustmentCode';
PRINT '- Foreign Keys: ProductId, WarehouseId, ZoneId';
PRINT '- Indexes: 5 performance indexes';
PRINT '';
PRINT 'Features:';
PRINT '- Adjustment Types: Increase, Decrease, Transfer';
PRINT '- Approval Workflow: RequiresApproval, IsApproved, IsRejected';
PRINT '- Adjustment Reasons: Damage, Theft, Spoilage, Counting Error, Physical Verification, Moisture Loss, Other';
PRINT '- Before/After Quantity Tracking';
PRINT '- Audit Trail: CreatedBy, CreatedDate, ModifiedBy, ModifiedDate';
PRINT '';
PRINT 'Next Steps:';
PRINT '1. Run the application: dotnet run';
PRINT '2. Navigate to Inventory → Stock Adjustments';
PRINT '3. Create test adjustments';
PRINT '4. Test approval workflow';
GO
