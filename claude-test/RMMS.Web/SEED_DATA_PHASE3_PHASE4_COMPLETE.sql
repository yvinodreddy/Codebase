-- ============================================================================
-- COMPREHENSIVE SEED DATA FOR PHASE 3 & PHASE 4
-- Rice Mill Management System (RMMS)
-- ============================================================================

USE RiceMillDB;
GO

-- ============================================================================
-- PHASE 3: REPORTING TABLES
-- ============================================================================

-- Custom Report Definitions
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'CustomReportDefinitions')
BEGIN
    CREATE TABLE CustomReportDefinitions (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Description NVARCHAR(500),
        DataSource NVARCHAR(100),
        SQL NVARCHAR(MAX),
        Columns NVARCHAR(MAX),
        Filters NVARCHAR(MAX),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedBy NVARCHAR(100),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO CustomReportDefinitions (Name, Description, DataSource, SQL, IsActive, CreatedBy, CreatedDate) VALUES
('Sales by Customer', 'Total sales grouped by customer', 'RiceSales', 'SELECT CustomerName, SUM(TotalAmount) as Total FROM RiceSales GROUP BY CustomerName', 1, 'admin', DATEADD(DAY, -30, GETDATE())),
('Inventory Summary', 'Current inventory levels by product', 'Inventory', 'SELECT ProductName, SUM(Quantity) as Stock FROM Inventory GROUP BY ProductName', 1, 'admin', DATEADD(DAY, -25, GETDATE())),
('Production Efficiency', 'Production output by machine', 'ProductionBatches', 'SELECT MachineName, AVG(Yield) as AvgYield FROM ProductionBatches GROUP BY MachineName', 1, 'admin', DATEADD(DAY, -20, GETDATE())),
('Revenue Analysis', 'Monthly revenue trends', 'RiceSales', 'SELECT MONTH(SaleDate) as Month, SUM(TotalAmount) as Revenue FROM RiceSales GROUP BY MONTH(SaleDate)', 1, 'admin', DATEADD(DAY, -15, GETDATE())),
('Stock Movement Report', 'Track all stock movements', 'StockMovements', 'SELECT * FROM StockMovements WHERE MovementDate >= DATEADD(MONTH, -1, GETDATE())', 1, 'admin', DATEADD(DAY, -10, GETDATE()));
GO

-- Scheduled Reports
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ScheduledReports')
BEGIN
    CREATE TABLE ScheduledReports (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ReportName NVARCHAR(200) NOT NULL,
        Description NVARCHAR(500),
        Schedule NVARCHAR(100), -- Cron expression
        Recipients NVARCHAR(MAX), -- Email addresses
        Format NVARCHAR(50), -- PDF, Excel, CSV
        IsActive BIT DEFAULT 1,
        LastRun DATETIME,
        NextRun DATETIME,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO ScheduledReports (ReportName, Description, Schedule, Recipients, Format, IsActive, LastRun, NextRun, CreatedBy, CreatedDate) VALUES
('Daily Sales Report', 'Daily sales summary sent every morning', '0 8 * * *', 'admin@rmms.com,sales@rmms.com', 'PDF', 1, GETDATE(), DATEADD(DAY, 1, GETDATE()), 'admin', DATEADD(DAY, -60, GETDATE())),
('Weekly Inventory Report', 'Weekly inventory status', '0 9 * * 1', 'warehouse@rmms.com', 'Excel', 1, DATEADD(DAY, -7, GETDATE()), DATEADD(DAY, 0, GETDATE()), 'admin', DATEADD(DAY, -50, GETDATE())),
('Monthly Financial Summary', 'Comprehensive monthly financials', '0 10 1 * *', 'finance@rmms.com,ceo@rmms.com', 'PDF', 1, DATEADD(MONTH, -1, GETDATE()), DATEADD(MONTH, 1, GETDATE()), 'admin', DATEADD(DAY, -40, GETDATE())),
('Production Performance', 'Weekly production metrics', '0 10 * * 5', 'production@rmms.com', 'Excel', 1, DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, 4, GETDATE()), 'admin', DATEADD(DAY, -30, GETDATE()));
GO

-- Dashboard Definitions
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DashboardDefinitions')
BEGIN
    CREATE TABLE DashboardDefinitions (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Description NVARCHAR(500),
        Layout NVARCHAR(MAX), -- JSON layout configuration
        Widgets NVARCHAR(MAX), -- JSON widget configuration
        RefreshInterval INT DEFAULT 60, -- seconds
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO DashboardDefinitions (Name, Description, Layout, RefreshInterval, IsActive, CreatedBy, CreatedDate) VALUES
('Executive Dashboard', 'High-level KPIs for executives', '{"rows": 3, "cols": 4}', 30, 1, 'admin', DATEADD(DAY, -45, GETDATE())),
('Sales Dashboard', 'Real-time sales monitoring', '{"rows": 2, "cols": 3}', 60, 1, 'admin', DATEADD(DAY, -40, GETDATE())),
('Production Dashboard', 'Live production metrics', '{"rows": 2, "cols": 4}', 15, 1, 'admin', DATEADD(DAY, -35, GETDATE())),
('Inventory Dashboard', 'Stock levels and movements', '{"rows": 3, "cols": 3}', 120, 1, 'admin', DATEADD(DAY, -30, GETDATE()));
GO

-- Comparison Reports
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ComparisonReports')
BEGIN
    CREATE TABLE ComparisonReports (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Description NVARCHAR(500),
        Period1Start DATE,
        Period1End DATE,
        Period2Start DATE,
        Period2End DATE,
        ReportType NVARCHAR(50), -- Sales, Production, Inventory
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO ComparisonReports (Name, Description, Period1Start, Period1End, Period2Start, Period2End, ReportType, IsActive, CreatedBy, CreatedDate) VALUES
('Q1 vs Q2 Sales', 'Compare sales between quarters', '2025-01-01', '2025-03-31', '2025-04-01', '2025-06-30', 'Sales', 1, 'admin', DATEADD(DAY, -50, GETDATE())),
('Year over Year Production', 'Annual production comparison', '2024-01-01', '2024-12-31', '2025-01-01', '2025-12-31', 'Production', 1, 'admin', DATEADD(DAY, -45, GETDATE())),
('Month over Month Inventory', 'Monthly inventory trends', '2025-09-01', '2025-09-30', '2025-10-01', '2025-10-31', 'Inventory', 1, 'admin', DATEADD(DAY, -40, GETDATE()));
GO

-- Drilldown Reports (metadata)
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DrilldownReports')
BEGIN
    CREATE TABLE DrilldownReports (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Description NVARCHAR(500),
        ReportType NVARCHAR(50), -- Sales, Inventory, Production
        Hierarchy NVARCHAR(MAX), -- JSON array of levels
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO DrilldownReports (Name, Description, ReportType, Hierarchy, IsActive, CreatedBy, CreatedDate) VALUES
('Sales Hierarchy Report', 'Navigate sales from year to product level', 'Sales', '["Year", "Quarter", "Month", "Customer", "Product"]', 1, 'admin', DATEADD(DAY, -35, GETDATE())),
('Inventory Hierarchy', 'Drill down inventory by warehouse and category', 'Inventory', '["Warehouse", "Category", "Product"]', 1, 'admin', DATEADD(DAY, -30, GETDATE())),
('Production Analysis', 'Production drilldown by time and batch', 'Production', '["Year", "Month", "Batch", "Status"]', 1, 'admin', DATEADD(DAY, -25, GETDATE()));
GO

-- ============================================================================
-- PHASE 3: DATA MANAGEMENT TABLES
-- ============================================================================

-- Bulk Operations
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'BulkOperations')
BEGIN
    CREATE TABLE BulkOperations (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        OperationType NVARCHAR(50), -- Import, Export
        EntityType NVARCHAR(50), -- Products, Customers, Sales, etc.
        FileName NVARCHAR(200),
        RecordsProcessed INT DEFAULT 0,
        RecordsSucceeded INT DEFAULT 0,
        RecordsFailed INT DEFAULT 0,
        Status NVARCHAR(50), -- Pending, InProgress, Completed, Failed
        ErrorLog NVARCHAR(MAX),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        CompletedDate DATETIME
    );
END
GO

INSERT INTO BulkOperations (OperationType, EntityType, FileName, RecordsProcessed, RecordsSucceeded, RecordsFailed, Status, IsActive, CreatedBy, CreatedDate, CompletedDate) VALUES
('Import', 'Products', 'products_import_oct2025.xlsx', 150, 145, 5, 'Completed', 1, 'admin', DATEADD(DAY, -20, GETDATE()), DATEADD(DAY, -20, GETDATE())),
('Export', 'Customers', 'customers_export_oct2025.xlsx', 89, 89, 0, 'Completed', 1, 'admin', DATEADD(DAY, -15, GETDATE()), DATEADD(DAY, -15, GETDATE())),
('Import', 'Inventory', 'inventory_update_oct2025.xlsx', 500, 485, 15, 'Completed', 1, 'admin', DATEADD(DAY, -10, GETDATE()), DATEADD(DAY, -10, GETDATE())),
('Export', 'Sales', 'sales_data_sept2025.xlsx', 1250, 1250, 0, 'Completed', 1, 'admin', DATEADD(DAY, -5, GETDATE()), DATEADD(DAY, -5, GETDATE()));
GO

-- Data Backup Jobs
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'BackupJobs')
BEGIN
    CREATE TABLE BackupJobs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        BackupName NVARCHAR(200) NOT NULL,
        BackupType NVARCHAR(50), -- Full, Differential, Transaction
        DatabaseName NVARCHAR(100),
        BackupPath NVARCHAR(500),
        FileSizeMB DECIMAL(10,2),
        Status NVARCHAR(50), -- Pending, InProgress, Completed, Failed
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        CompletedDate DATETIME
    );
END
GO

INSERT INTO BackupJobs (BackupName, BackupType, DatabaseName, BackupPath, FileSizeMB, Status, IsActive, CreatedBy, CreatedDate, CompletedDate) VALUES
('Daily Full Backup - Oct 20', 'Full', 'RiceMillDB', '/backups/full_20251020.bak', 1250.50, 'Completed', 1, 'system', DATEADD(DAY, -2, GETDATE()), DATEADD(DAY, -2, GETDATE())),
('Daily Full Backup - Oct 21', 'Full', 'RiceMillDB', '/backups/full_20251021.bak', 1275.25, 'Completed', 1, 'system', DATEADD(DAY, -1, GETDATE()), DATEADD(DAY, -1, GETDATE())),
('Hourly Transaction Log', 'Transaction', 'RiceMillDB', '/backups/tlog_current.trn', 45.75, 'Completed', 1, 'system', GETDATE(), GETDATE());
GO

-- Data Archival Jobs
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ArchivalJobs')
BEGIN
    CREATE TABLE ArchivalJobs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        JobName NVARCHAR(200) NOT NULL,
        TableName NVARCHAR(100),
        ArchivalCriteria NVARCHAR(500), -- e.g., "Records older than 2 years"
        RecordsArchived INT DEFAULT 0,
        ArchiveLocation NVARCHAR(500),
        Status NVARCHAR(50),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        CompletedDate DATETIME
    );
END
GO

INSERT INTO ArchivalJobs (JobName, TableName, ArchivalCriteria, RecordsArchived, ArchiveLocation, Status, IsActive, CreatedBy, CreatedDate, CompletedDate) VALUES
('Archive 2023 Sales', 'RiceSales', 'SaleDate < 2024-01-01', 5420, '/archive/sales_2023.db', 'Completed', 1, 'admin', DATEADD(DAY, -60, GETDATE()), DATEADD(DAY, -60, GETDATE())),
('Archive Old Production Batches', 'ProductionBatches', 'BatchDate < 2023-01-01', 3150, '/archive/production_old.db', 'Completed', 1, 'admin', DATEADD(DAY, -45, GETDATE()), DATEADD(DAY, -45, GETDATE()));
GO

-- Audit Trail
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AuditLogs')
BEGIN
    CREATE TABLE AuditLogs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TableName NVARCHAR(100),
        RecordId INT,
        Action NVARCHAR(50), -- INSERT, UPDATE, DELETE
        OldValues NVARCHAR(MAX),
        NewValues NVARCHAR(MAX),
        Username NVARCHAR(100),
        IPAddress NVARCHAR(50),
        Timestamp DATETIME DEFAULT GETDATE(),
        IsActive BIT DEFAULT 1,
        CreatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

INSERT INTO AuditLogs (TableName, RecordId, Action, OldValues, NewValues, Username, IPAddress, Timestamp, CreatedDate) VALUES
('Products', 15, 'UPDATE', '{"Price": 1500}', '{"Price": 1550}', 'admin', '192.168.1.10', DATEADD(HOUR, -2, GETDATE()), DATEADD(HOUR, -2, GETDATE())),
('Customers', 45, 'INSERT', NULL, '{"Name": "New Customer LLC"}', 'admin', '192.168.1.10', DATEADD(HOUR, -1, GETDATE()), DATEADD(HOUR, -1, GETDATE())),
('RiceSales', 125, 'DELETE', '{"Amount": 50000}', NULL, 'manager', '192.168.1.15', DATEADD(MINUTE, -30, GETDATE()), DATEADD(MINUTE, -30, GETDATE()));
GO

-- Version Control
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DataVersions')
BEGIN
    CREATE TABLE DataVersions (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TableName NVARCHAR(100),
        RecordId INT,
        VersionNumber INT,
        VersionData NVARCHAR(MAX), -- JSON snapshot
        ChangeDescription NVARCHAR(500),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

INSERT INTO DataVersions (TableName, RecordId, VersionNumber, VersionData, ChangeDescription, IsActive, CreatedBy, CreatedDate) VALUES
('Products', 10, 1, '{"Name":"Basmati Rice","Price":1200}', 'Initial version', 1, 'admin', DATEADD(DAY, -30, GETDATE())),
('Products', 10, 2, '{"Name":"Basmati Rice Premium","Price":1350}', 'Updated name and price', 1, 'admin', DATEADD(DAY, -15, GETDATE())),
('Products', 10, 3, '{"Name":"Basmati Rice Premium","Price":1400}', 'Price adjustment', 1, 'admin', DATEADD(DAY, -5, GETDATE()));
GO

-- Validation Rules
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ValidationRules')
BEGIN
    CREATE TABLE ValidationRules (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        RuleName NVARCHAR(200) NOT NULL,
        TableName NVARCHAR(100),
        FieldName NVARCHAR(100),
        RuleType NVARCHAR(50), -- Required, Range, Regex, Custom
        RuleExpression NVARCHAR(MAX),
        ErrorMessage NVARCHAR(500),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO ValidationRules (RuleName, TableName, FieldName, RuleType, RuleExpression, ErrorMessage, IsActive, CreatedBy, CreatedDate) VALUES
('Product Price Minimum', 'Products', 'Price', 'Range', 'value >= 0', 'Price must be non-negative', 1, 'admin', DATEADD(DAY, -40, GETDATE())),
('Customer Email Format', 'Customers', 'Email', 'Regex', '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 'Invalid email format', 1, 'admin', DATEADD(DAY, -35, GETDATE())),
('Sales Amount Positive', 'RiceSales', 'TotalAmount', 'Range', 'value > 0', 'Sales amount must be positive', 1, 'admin', DATEADD(DAY, -30, GETDATE()));
GO

-- Cleansing Jobs
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'CleansingJobs')
BEGIN
    CREATE TABLE CleansingJobs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        JobName NVARCHAR(200) NOT NULL,
        TableName NVARCHAR(100),
        CleansingType NVARCHAR(50), -- Duplicates, Orphans, InvalidData
        RecordsFound INT DEFAULT 0,
        RecordsCleansed INT DEFAULT 0,
        Status NVARCHAR(50),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        CompletedDate DATETIME
    );
END
GO

INSERT INTO CleansingJobs (JobName, TableName, CleansingType, RecordsFound, RecordsCleansed, Status, IsActive, CreatedBy, CreatedDate, CompletedDate) VALUES
('Remove Duplicate Customers', 'Customers', 'Duplicates', 15, 15, 'Completed', 1, 'admin', DATEADD(DAY, -25, GETDATE()), DATEADD(DAY, -25, GETDATE())),
('Clean Orphan Inventory Records', 'Inventory', 'Orphans', 8, 8, 'Completed', 1, 'admin', DATEADD(DAY, -20, GETDATE()), DATEADD(DAY, -20, GETDATE())),
('Fix Invalid Product Prices', 'Products', 'InvalidData', 3, 3, 'Completed', 1, 'admin', DATEADD(DAY, -15, GETDATE()), DATEADD(DAY, -15, GETDATE()));
GO

-- Master Data Entities
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MasterDataEntities')
BEGIN
    CREATE TABLE MasterDataEntities (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        EntityType NVARCHAR(100), -- Customer, Product, Vendor, etc.
        MasterRecordId INT,
        GoldenRecordData NVARCHAR(MAX), -- JSON of master record
        SourceSystems NVARCHAR(MAX), -- JSON array of source systems
        ConfidenceScore DECIMAL(5,2),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO MasterDataEntities (EntityType, MasterRecordId, GoldenRecordData, ConfidenceScore, IsActive, CreatedBy, CreatedDate) VALUES
('Customer', 1, '{"Name":"ABC Trading Co","Email":"abc@trading.com","Phone":"555-0100"}', 98.5, 1, 'system', DATEADD(DAY, -50, GETDATE())),
('Product', 5, '{"Name":"Basmati Rice 1121","Category":"Premium","Price":1450}', 99.2, 1, 'system', DATEADD(DAY, -45, GETDATE())),
('Vendor', 10, '{"Name":"Quality Mills Inc","Rating":"A+","Contact":"vendor@qm.com"}', 97.8, 1, 'system', DATEADD(DAY, -40, GETDATE()));
GO

-- Export Jobs
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ExportJobs')
BEGIN
    CREATE TABLE ExportJobs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ExportName NVARCHAR(200) NOT NULL,
        ExportType NVARCHAR(50), -- Excel, PDF, CSV
        DataSource NVARCHAR(100),
        FilePath NVARCHAR(500),
        RecordCount INT DEFAULT 0,
        Status NVARCHAR(50),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        CompletedDate DATETIME
    );
END
GO

INSERT INTO ExportJobs (ExportName, ExportType, DataSource, FilePath, RecordCount, Status, IsActive, CreatedBy, CreatedDate, CompletedDate) VALUES
('October Sales Export', 'Excel', 'RiceSales', '/exports/sales_oct2025.xlsx', 1250, 'Completed', 1, 'admin', DATEADD(DAY, -10, GETDATE()), DATEADD(DAY, -10, GETDATE())),
('Product Catalog PDF', 'PDF', 'Products', '/exports/products_catalog.pdf', 350, 'Completed', 1, 'admin', DATEADD(DAY, -7, GETDATE()), DATEADD(DAY, -7, GETDATE())),
('Customer List CSV', 'CSV', 'Customers', '/exports/customers.csv', 89, 'Completed', 1, 'admin', DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, -3, GETDATE()));
GO

-- ============================================================================
-- PHASE 4: API & INTEGRATIONS TABLES
-- ============================================================================

-- API Analytics
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ApiAnalytics')
BEGIN
    CREATE TABLE ApiAnalytics (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Endpoint NVARCHAR(200),
        Method NVARCHAR(10), -- GET, POST, PUT, DELETE
        StatusCode INT,
        ResponseTime INT, -- milliseconds
        RequestSize INT, -- bytes
        ResponseSize INT, -- bytes
        UserId NVARCHAR(100),
        IPAddress NVARCHAR(50),
        UserAgent NVARCHAR(500),
        IsActive BIT DEFAULT 1,
        CreatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

INSERT INTO ApiAnalytics (Endpoint, Method, StatusCode, ResponseTime, RequestSize, ResponseSize, UserId, IPAddress, UserAgent, CreatedDate) VALUES
('/api/v1/products', 'GET', 200, 45, 0, 15420, 'api_user1', '203.0.113.1', 'Mobile App v2.1', DATEADD(HOUR, -2, GETDATE())),
('/api/v1/sales', 'POST', 201, 125, 850, 250, 'api_user2', '203.0.113.2', 'Web Client v1.5', DATEADD(HOUR, -1, GETDATE())),
('/api/v1/inventory', 'GET', 200, 65, 0, 8500, 'api_user1', '203.0.113.1', 'Mobile App v2.1', DATEADD(MINUTE, -30, GETDATE())),
('/api/v1/customers', 'PUT', 200, 95, 450, 450, 'api_user3', '203.0.113.3', 'Integration Service', DATEADD(MINUTE, -15, GETDATE()));
GO

-- Webhooks
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Webhooks')
BEGIN
    CREATE TABLE Webhooks (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Url NVARCHAR(500) NOT NULL,
        Event NVARCHAR(100), -- sale.created, product.updated, etc.
        Secret NVARCHAR(100),
        IsActive BIT DEFAULT 1,
        LastTriggered DATETIME,
        FailureCount INT DEFAULT 0,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO Webhooks (Name, Url, Event, Secret, IsActive, LastTriggered, FailureCount, CreatedBy, CreatedDate) VALUES
('Sales Notification', 'https://api.partner1.com/webhooks/sales', 'sale.created', 'secret_abc123', 1, DATEADD(HOUR, -3, GETDATE()), 0, 'admin', DATEADD(DAY, -30, GETDATE())),
('Inventory Alert', 'https://api.warehouse.com/webhooks/inventory', 'inventory.low', 'secret_xyz789', 1, DATEADD(DAY, -1, GETDATE()), 2, 'admin', DATEADD(DAY, -25, GETDATE())),
('Production Update', 'https://api.erp.com/webhooks/production', 'batch.completed', 'secret_prod456', 1, DATEADD(HOUR, -5, GETDATE()), 0, 'admin', DATEADD(DAY, -20, GETDATE()));
GO

-- Integration Status
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'IntegrationStatus')
BEGIN
    CREATE TABLE IntegrationStatus (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        IntegrationName NVARCHAR(200) NOT NULL,
        IntegrationType NVARCHAR(50), -- REST, SOAP, FTP, etc.
        Status NVARCHAR(50), -- Active, Inactive, Error
        LastSync DATETIME,
        NextSync DATETIME,
        RecordsSynced INT DEFAULT 0,
        ErrorMessage NVARCHAR(MAX),
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO IntegrationStatus (IntegrationName, IntegrationType, Status, LastSync, NextSync, RecordsSynced, IsActive, CreatedBy, CreatedDate) VALUES
('ERP System Integration', 'REST', 'Active', DATEADD(HOUR, -1, GETDATE()), DATEADD(HOUR, 3, GETDATE()), 1250, 1, 'system', DATEADD(DAY, -60, GETDATE())),
('Accounting Software Sync', 'REST', 'Active', DATEADD(HOUR, -2, GETDATE()), DATEADD(HOUR, 22, GETDATE()), 450, 1, 'system', DATEADD(DAY, -50, GETDATE())),
('Warehouse Management', 'SOAP', 'Active', DATEADD(MINUTE, -30, GETDATE()), DATEADD(MINUTE, 30, GETDATE()), 180, 1, 'system', DATEADD(DAY, -40, GETDATE())),
('Legacy System Bridge', 'FTP', 'Error', DATEADD(DAY, -2, GETDATE()), NULL, 0, 0, 'system', DATEADD(DAY, -30, GETDATE()));
GO

-- API Keys
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ApiKeys')
BEGIN
    CREATE TABLE ApiKeys (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        KeyName NVARCHAR(200) NOT NULL,
        ApiKey NVARCHAR(100) NOT NULL UNIQUE,
        KeySecret NVARCHAR(100),
        Permissions NVARCHAR(MAX), -- JSON array of permissions
        RateLimit INT DEFAULT 1000, -- requests per hour
        ExpiryDate DATETIME,
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        LastUsed DATETIME,
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO ApiKeys (KeyName, ApiKey, KeySecret, Permissions, RateLimit, ExpiryDate, IsActive, CreatedBy, CreatedDate, LastUsed) VALUES
('Mobile App Key', 'key_mobile_2025_abc123', 'secret_mobile_xyz789', '["read:products","read:inventory","write:sales"]', 5000, DATEADD(YEAR, 1, GETDATE()), 1, 'admin', DATEADD(DAY, -90, GETDATE()), DATEADD(HOUR, -1, GETDATE())),
('Partner Integration', 'key_partner1_def456', 'secret_partner1_uvw012', '["read:products","read:sales"]', 2000, DATEADD(MONTH, 6, GETDATE()), 1, 'admin', DATEADD(DAY, -60, GETDATE()), DATEADD(HOUR, -3, GETDATE())),
('Internal Dashboard', 'key_internal_ghi789', 'secret_internal_rst345', '["read:*","write:*"]', 10000, DATEADD(YEAR, 2, GETDATE()), 1, 'admin', DATEADD(DAY, -30, GETDATE()), DATEADD(MINUTE, -15, GETDATE()));
GO

-- ============================================================================
-- PHASE 4: MOBILE & REAL-TIME TABLES
-- ============================================================================

-- Mobile Dashboard
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MobileDashboards')
BEGIN
    CREATE TABLE MobileDashboards (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        DashboardName NVARCHAR(200) NOT NULL,
        UserId NVARCHAR(100),
        Layout NVARCHAR(MAX), -- JSON configuration
        Widgets NVARCHAR(MAX), -- JSON widgets
        RefreshInterval INT DEFAULT 60,
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE(),
        ModifiedDate DATETIME
    );
END
GO

INSERT INTO MobileDashboards (DashboardName, UserId, Layout, RefreshInterval, IsActive, CreatedBy, CreatedDate) VALUES
('Sales Rep Dashboard', 'salesrep1', '{"rows": 2, "cols": 2}', 30, 1, 'salesrep1', DATEADD(DAY, -40, GETDATE())),
('Warehouse Manager View', 'warehouse1', '{"rows": 3, "cols": 2}', 60, 1, 'warehouse1', DATEADD(DAY, -35, GETDATE())),
('Production Supervisor', 'production1', '{"rows": 2, "cols": 3}', 15, 1, 'production1', DATEADD(DAY, -30, GETDATE()));
GO

-- Push Notifications
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PushNotifications')
BEGIN
    CREATE TABLE PushNotifications (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Title NVARCHAR(200) NOT NULL,
        Message NVARCHAR(500),
        NotificationType NVARCHAR(50), -- Info, Warning, Alert, Success
        TargetUsers NVARCHAR(MAX), -- JSON array of user IDs
        DeviceTokens NVARCHAR(MAX), -- JSON array of FCM tokens
        Status NVARCHAR(50), -- Pending, Sent, Failed
        SentDate DATETIME,
        IsActive BIT DEFAULT 1,
        CreatedBy NVARCHAR(100),
        CreatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

INSERT INTO PushNotifications (Title, Message, NotificationType, TargetUsers, Status, SentDate, IsActive, CreatedBy, CreatedDate) VALUES
('Low Stock Alert', 'Basmati Rice 1121 stock below minimum threshold', 'Warning', '["warehouse1","manager1"]', 'Sent', DATEADD(HOUR, -4, GETDATE()), 1, 'system', DATEADD(HOUR, -4, GETDATE())),
('Production Complete', 'Batch #B2025-1045 completed successfully', 'Success', '["production1","supervisor1"]', 'Sent', DATEADD(HOUR, -2, GETDATE()), 1, 'system', DATEADD(HOUR, -2, GETDATE())),
('New Order Received', 'Order #SO-2025-8975 requires attention', 'Info', '["salesrep1","salesrep2"]', 'Sent', DATEADD(HOUR, -1, GETDATE()), 1, 'system', DATEADD(HOUR, -1, GETDATE()));
GO

-- Real-time Metrics
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'RealtimeMetrics')
BEGIN
    CREATE TABLE RealtimeMetrics (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        MetricName NVARCHAR(200) NOT NULL,
        MetricValue DECIMAL(18,2),
        MetricUnit NVARCHAR(50),
        Category NVARCHAR(50), -- Production, Sales, Inventory
        Timestamp DATETIME DEFAULT GETDATE(),
        IsActive BIT DEFAULT 1,
        CreatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

INSERT INTO RealtimeMetrics (MetricName, MetricValue, MetricUnit, Category, Timestamp, CreatedDate) VALUES
('Current Production Rate', 125.5, 'kg/hour', 'Production', GETDATE(), GETDATE()),
('Active Machines', 8, 'count', 'Production', GETDATE(), GETDATE()),
('Today Sales', 285000, 'INR', 'Sales', GETDATE(), GETDATE()),
('Current Stock Level', 45000, 'kg', 'Inventory', GETDATE(), GETDATE()),
('Pending Orders', 15, 'count', 'Sales', GETDATE(), GETDATE());
GO

PRINT 'Seed data created successfully!';
PRINT 'Total tables seeded: 19';
PRINT '- Custom Report Definitions: 5 records';
PRINT '- Scheduled Reports: 4 records';
PRINT '- Dashboard Definitions: 4 records';
PRINT '- Comparison Reports: 3 records';
PRINT '- Drilldown Reports: 3 records';
PRINT '- Bulk Operations: 4 records';
PRINT '- Backup Jobs: 3 records';
PRINT '- Archival Jobs: 2 records';
PRINT '- Audit Logs: 3 records';
PRINT '- Data Versions: 3 records';
PRINT '- Validation Rules: 3 records';
PRINT '- Cleansing Jobs: 3 records';
PRINT '- Master Data Entities: 3 records';
PRINT '- Export Jobs: 3 records';
PRINT '- API Analytics: 4 records';
PRINT '- Webhooks: 3 records';
PRINT '- Integration Status: 4 records';
PRINT '- API Keys: 3 records';
PRINT '- Mobile Dashboards: 3 records';
PRINT '- Push Notifications: 3 records';
PRINT '- Realtime Metrics: 5 records';
GO
