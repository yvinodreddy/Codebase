-- ============================================================
-- PHASE 4: COMPLETE DATABASE SETUP
-- All tables required for Phase 4 tasks
-- ============================================================

USE RMMSDb;
GO

-- ============================================================
-- TASK 4.2.3: API KEYS TABLE
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ApiKeys]'))
BEGIN
    CREATE TABLE [dbo].[ApiKeys] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [KeyName] NVARCHAR(100) NOT NULL,
        [ApiKey] NVARCHAR(500) NOT NULL UNIQUE,
        [SecretHash] NVARCHAR(500) NOT NULL,
        [IsActive] BIT NOT NULL DEFAULT 1,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [ExpiresAt] DATETIME2 NULL,
        [LastUsedAt] DATETIME2 NULL,
        CONSTRAINT [UQ_ApiKey] UNIQUE ([ApiKey])
    );
    CREATE INDEX [IX_ApiKeys_ApiKey] ON [dbo].[ApiKeys]([ApiKey]);
    PRINT 'Created ApiKeys table';
END
GO

-- ============================================================
-- TASK 4.2.4: EXTERNAL LOGINS (OAuth)
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ExternalLogins]'))
BEGIN
    CREATE TABLE [dbo].[ExternalLogins] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [UserId] NVARCHAR(100) NOT NULL,
        [Provider] NVARCHAR(50) NOT NULL, -- 'Google', 'Microsoft', etc.
        [ProviderKey] NVARCHAR(200) NOT NULL,
        [ProviderDisplayName] NVARCHAR(100) NULL,
        [Email] NVARCHAR(255) NULL,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [UQ_ExternalLogin] UNIQUE ([Provider], [ProviderKey])
    );
    CREATE INDEX [IX_ExternalLogins_UserId] ON [dbo].[ExternalLogins]([UserId]);
    PRINT 'Created ExternalLogins table';
END
GO

-- ============================================================
-- TASK 4.2.5: API USAGE ANALYTICS
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ApiUsageLogs]'))
BEGIN
    CREATE TABLE [dbo].[ApiUsageLogs] (
        [Id] BIGINT IDENTITY(1,1) PRIMARY KEY,
        [Timestamp] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [UserId] NVARCHAR(100) NULL,
        [Endpoint] NVARCHAR(500) NOT NULL,
        [HttpMethod] NVARCHAR(10) NOT NULL,
        [StatusCode] INT NOT NULL,
        [ResponseTimeMs] INT NOT NULL,
        [IpAddress] NVARCHAR(45) NULL,
        [UserAgent] NVARCHAR(500) NULL,
        [RequestSize] BIGINT NULL,
        [ResponseSize] BIGINT NULL
    );
    CREATE CLUSTERED INDEX [IX_ApiUsageLogs_Timestamp] ON [dbo].[ApiUsageLogs]([Timestamp] DESC);
    CREATE INDEX [IX_ApiUsageLogs_UserId] ON [dbo].[ApiUsageLogs]([UserId]);
    CREATE INDEX [IX_ApiUsageLogs_Endpoint] ON [dbo].[ApiUsageLogs]([Endpoint]);
    PRINT 'Created ApiUsageLogs table';
END
GO

-- ============================================================
-- TASK 4.3.1: INTEGRATIONS FRAMEWORK
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Integrations]'))
BEGIN
    CREATE TABLE [dbo].[Integrations] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [Name] NVARCHAR(100) NOT NULL,
        [Type] NVARCHAR(50) NOT NULL, -- 'ERP', 'Payment', 'SMS', 'Email', 'Webhook'
        [Provider] NVARCHAR(50) NOT NULL, -- 'QuickBooks', 'Stripe', 'Twilio', 'SendGrid'
        [IsEnabled] BIT NOT NULL DEFAULT 0,
        [ConfigurationJson] NVARCHAR(MAX) NOT NULL,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [LastSyncAt] DATETIME2 NULL,
        [LastSyncStatus] NVARCHAR(50) NULL
    );
    PRINT 'Created Integrations table';
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[IntegrationSyncLogs]'))
BEGIN
    CREATE TABLE [dbo].[IntegrationSyncLogs] (
        [Id] BIGINT IDENTITY(1,1) PRIMARY KEY,
        [IntegrationId] INT NOT NULL,
        [SyncStartedAt] DATETIME2 NOT NULL,
        [SyncCompletedAt] DATETIME2 NULL,
        [Status] NVARCHAR(50) NOT NULL, -- 'Success', 'Failed', 'Partial'
        [RecordsProcessed] INT NULL,
        [RecordsFailed] INT NULL,
        [ErrorMessage] NVARCHAR(MAX) NULL,
        [Details] NVARCHAR(MAX) NULL,
        CONSTRAINT [FK_IntegrationSyncLogs_Integration] FOREIGN KEY ([IntegrationId])
            REFERENCES [dbo].[Integrations]([Id])
    );
    CREATE INDEX [IX_IntegrationSyncLogs_IntegrationId] ON [dbo].[IntegrationSyncLogs]([IntegrationId]);
    PRINT 'Created IntegrationSyncLogs table';
END
GO

-- ============================================================
-- TASK 4.3.2: WEBHOOKS
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Webhooks]'))
BEGIN
    CREATE TABLE [dbo].[Webhooks] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [Name] NVARCHAR(100) NOT NULL,
        [Url] NVARCHAR(500) NOT NULL,
        [Secret] NVARCHAR(200) NOT NULL,
        [IsEnabled] BIT NOT NULL DEFAULT 1,
        [Events] NVARCHAR(MAX) NOT NULL, -- JSON array of event names
        [Headers] NVARCHAR(MAX) NULL, -- JSON object of custom headers
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [CreatedBy] NVARCHAR(100) NULL
    );
    PRINT 'Created Webhooks table';
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[WebhookDeliveries]'))
BEGIN
    CREATE TABLE [dbo].[WebhookDeliveries] (
        [Id] BIGINT IDENTITY(1,1) PRIMARY KEY,
        [WebhookId] INT NOT NULL,
        [EventType] NVARCHAR(100) NOT NULL,
        [Payload] NVARCHAR(MAX) NOT NULL,
        [Status] NVARCHAR(50) NOT NULL, -- 'Pending', 'Delivered', 'Failed'
        [AttemptCount] INT NOT NULL DEFAULT 0,
        [LastAttemptAt] DATETIME2 NULL,
        [NextRetryAt] DATETIME2 NULL,
        [ResponseCode] INT NULL,
        [ResponseBody] NVARCHAR(MAX) NULL,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [FK_WebhookDeliveries_Webhook] FOREIGN KEY ([WebhookId])
            REFERENCES [dbo].[Webhooks]([Id])
    );
    CREATE INDEX [IX_WebhookDeliveries_WebhookId] ON [dbo].[WebhookDeliveries]([WebhookId]);
    CREATE INDEX [IX_WebhookDeliveries_Status] ON [dbo].[WebhookDeliveries]([Status]);
    PRINT 'Created WebhookDeliveries table';
END
GO

-- ============================================================
-- TASK 4.3.5: PAYMENT TRANSACTIONS
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PaymentTransactions]'))
BEGIN
    CREATE TABLE [dbo].[PaymentTransactions] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [TransactionId] NVARCHAR(200) NOT NULL UNIQUE,
        [Gateway] NVARCHAR(50) NOT NULL, -- 'Stripe', 'PayPal', 'Razorpay'
        [Amount] DECIMAL(18,2) NOT NULL,
        [Currency] NVARCHAR(3) NOT NULL DEFAULT 'INR',
        [Status] NVARCHAR(50) NOT NULL, -- 'Pending', 'Completed', 'Failed', 'Refunded'
        [PaymentMethod] NVARCHAR(50) NULL,
        [CustomerEmail] NVARCHAR(255) NULL,
        [OrderId] NVARCHAR(100) NULL,
        [SalesOrderId] INT NULL,
        [Metadata] NVARCHAR(MAX) NULL,
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [CompletedAt] DATETIME2 NULL
    );
    CREATE INDEX [IX_PaymentTransactions_TransactionId] ON [dbo].[PaymentTransactions]([TransactionId]);
    CREATE INDEX [IX_PaymentTransactions_SalesOrderId] ON [dbo].[PaymentTransactions]([SalesOrderId]);
    PRINT 'Created PaymentTransactions table';
END
GO

-- ============================================================
-- TASK 4.3.6: NOTIFICATION LOGS (SMS/Email)
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[NotificationLogs]'))
BEGIN
    CREATE TABLE [dbo].[NotificationLogs] (
        [Id] BIGINT IDENTITY(1,1) PRIMARY KEY,
        [Type] NVARCHAR(50) NOT NULL, -- 'Email', 'SMS', 'Push'
        [Provider] NVARCHAR(50) NULL, -- 'SendGrid', 'Twilio', 'Firebase'
        [Recipient] NVARCHAR(200) NOT NULL,
        [Subject] NVARCHAR(500) NULL,
        [Message] NVARCHAR(MAX) NOT NULL,
        [Status] NVARCHAR(50) NOT NULL, -- 'Sent', 'Failed', 'Pending'
        [StatusMessage] NVARCHAR(500) NULL,
        [ExternalId] NVARCHAR(200) NULL,
        [SentAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [CreatedAt] DATETIME2 NOT NULL DEFAULT GETDATE()
    );
    CREATE INDEX [IX_NotificationLogs_Type] ON [dbo].[NotificationLogs]([Type]);
    CREATE INDEX [IX_NotificationLogs_Status] ON [dbo].[NotificationLogs]([Status]);
    CREATE INDEX [IX_NotificationLogs_SentAt] ON [dbo].[NotificationLogs]([SentAt] DESC);
    PRINT 'Created NotificationLogs table';
END
GO

-- ============================================================
-- TASK 4.4.4: DEVICE TOKENS (Push Notifications)
-- ============================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DeviceTokens]'))
BEGIN
    CREATE TABLE [dbo].[DeviceTokens] (
        [Id] INT IDENTITY(1,1) PRIMARY KEY,
        [UserId] NVARCHAR(100) NOT NULL,
        [DeviceToken] NVARCHAR(500) NOT NULL UNIQUE,
        [Platform] NVARCHAR(20) NOT NULL, -- 'iOS', 'Android', 'Web'
        [DeviceInfo] NVARCHAR(500) NULL,
        [IsActive] BIT NOT NULL DEFAULT 1,
        [RegisteredAt] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [LastUsedAt] DATETIME2 NULL
    );
    CREATE INDEX [IX_DeviceTokens_UserId] ON [dbo].[DeviceTokens]([UserId]);
    CREATE INDEX [IX_DeviceTokens_IsActive] ON [dbo].[DeviceTokens]([IsActive]);
    PRINT 'Created DeviceTokens table';
END
GO

-- ============================================================
-- COMPLETED
-- ============================================================
PRINT '';
PRINT '====================================';
PRINT 'PHASE 4 DATABASE SETUP COMPLETE';
PRINT '====================================';
PRINT 'All tables for Phase 4 tasks created successfully.';
GO
