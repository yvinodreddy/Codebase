# PHASE 4: QUICK START GUIDE
## Fast-Track Implementation Reference

**Purpose:** Quick reference for implementing Phase 4 tasks
**Full Details:** See `PHASE4_ULTRATHINK_COMPREHENSIVE_PLAN.md`
**Duration:** 60 hours (24 tasks)

---

## QUICK TASK CHECKLIST

### Sprint 4.1: REST API Foundation (20h) ⭐ HIGHEST PRIORITY

- [ ] **Task 4.1.1:** API Project Structure (2h)
  ```bash
  mkdir -p RMMS.Web/Controllers/API/v1
  # Create BaseApiController.cs with ApiResponse<T>
  ```

- [ ] **Task 4.1.2:** JWT Authentication (3h)
  ```bash
  dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.JwtBearer
  # Create JwtService, AuthController, RefreshToken table
  ```

- [ ] **Task 4.1.3:** Core API Controllers (4h)
  ```bash
  # Create: CustomersApiController, ProductsApiController,
  # InventoryApiController, ProductionApiController, SalesApiController
  # Endpoints: GET, POST, PUT, DELETE with pagination
  ```

- [ ] **Task 4.1.4:** API Versioning (1.5h)
  ```bash
  dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning
  # Add [ApiVersion("1.0")] to controllers
  ```

- [ ] **Task 4.1.5:** Error Handling & Logging (2h)
  ```bash
  # Create ApiExceptionMiddleware
  # Custom exceptions: NotFoundException, BadRequestException, etc.
  ```

- [ ] **Task 4.1.6:** Rate Limiting (1.5h)
  ```bash
  dotnet add RMMS.Web package AspNetCoreRateLimit
  # Configure: 60 req/min general, 5 req/min login
  ```

- [ ] **Task 4.1.7:** Health Checks (1h)
  ```bash
  dotnet add RMMS.Web package AspNetCore.HealthChecks.SqlServer
  # Endpoints: /health, /health/ready, /health/live, /health-ui
  ```

- [ ] **Task 4.1.8:** Request/Response Compression (1h)
  ```bash
  # Verify Phase 3.2 compression works for API
  # Add request decompression
  ```

**After Sprint 4.1:**
- ✅ Test all API endpoints with Postman
- ✅ Verify JWT authentication
- ✅ Check rate limiting works
- ✅ Confirm health checks operational

---

### Sprint 4.2: API Documentation & Security (15h)

- [ ] **Task 4.2.1:** Swagger/OpenAPI (3h)
  ```bash
  dotnet add RMMS.Web package Swashbuckle.AspNetCore
  # Access at /api-docs
  # Add XML comments to controllers
  ```

- [ ] **Task 4.2.2:** CORS Policy (1.5h)
  ```bash
  # Configure allowed origins in appsettings.json
  # Add CORS middleware
  ```

- [ ] **Task 4.2.3:** API Key Authentication (2h)
  ```bash
  # Create ApiKeys table
  # Create ApiKeyAuthenticationHandler
  # Support X-API-Key header
  ```

- [ ] **Task 4.2.4:** OAuth2/OpenID Connect (3h)
  ```bash
  dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.Google
  # Google & Microsoft OAuth
  # Generate JWT after OAuth success
  ```

- [ ] **Task 4.2.5:** API Usage Analytics (2h)
  ```bash
  # Create ApiUsageLogs table
  # Create ApiUsageTrackingMiddleware
  # Create AnalyticsController for admin
  ```

- [ ] **Task 4.2.6:** Request Throttling (1.5h)
  ```bash
  # Create ApiThrottlingMiddleware
  # Limit concurrent requests per endpoint
  ```

**After Sprint 4.2:**
- ✅ Test Swagger UI
- ✅ Test JWT + API Key + OAuth authentication
- ✅ Verify CORS with mobile/web client
- ✅ Check usage analytics tracking

---

### Sprint 4.3: Third-Party Integrations (15h)

- [ ] **Task 4.3.1:** Integration Framework (2.5h)
  ```bash
  # Create Integrations table
  # Create IIntegrationService interface
  # Create BaseIntegrationService with retry logic
  # Create IntegrationsController API
  ```

- [ ] **Task 4.3.2:** Webhook Support (2.5h)
  ```bash
  # Create Webhooks table
  # Create WebhookService with HMAC signature
  # Create WebhookDeliveryService (background)
  # Integrate into domain events
  ```

- [ ] **Task 4.3.3:** Scheduled Jobs (Hangfire) (2.5h)
  ```bash
  dotnet add RMMS.Web package Hangfire.AspNetCore
  dotnet add RMMS.Web package Hangfire.SqlServer
  # Create scheduled jobs:
  # - Daily inventory report
  # - Low stock alerts
  # - Production efficiency
  # - Data cleanup
  # - Webhook retry
  # Dashboard: /hangfire
  ```

- [ ] **Task 4.3.4:** ERP/Accounting Integration (2.5h)
  ```bash
  # Choose: QuickBooks OR SAP
  # Create ErpIntegrationService
  # Sync: customers, vendors, products, transactions
  # Create ErpController API
  ```

- [ ] **Task 4.3.5:** Payment Gateway (2h)
  ```bash
  dotnet add RMMS.Web package Stripe.net
  # Create PaymentTransactions table
  # Create StripeService
  # Create PaymentsController
  # Handle webhooks
  ```

- [ ] **Task 4.3.6:** SMS/Email Gateway (2h)
  ```bash
  dotnet add RMMS.Web package Twilio
  dotnet add RMMS.Web package SendGrid
  # Enhance EmailNotificationService with SendGrid
  # Create SmsService with Twilio
  # Create notification templates
  # Integrate into business processes
  ```

**After Sprint 4.3:**
- ✅ Test webhook delivery (webhook.site)
- ✅ Verify Hangfire jobs running
- ✅ Test ERP sync (sandbox account)
- ✅ Complete test payment (Stripe test card)
- ✅ Send test SMS and email

---

### Sprint 4.4: Mobile & Real-Time (10h)

- [ ] **Task 4.4.1:** SignalR Real-Time (3h)
  ```bash
  # Create hubs:
  # - ProductionHub (/hubs/production)
  # - DashboardHub (/hubs/dashboard)
  # - NotificationHub (/hubs/notifications)
  # Integrate into services for real-time broadcasts
  ```

- [ ] **Task 4.4.2:** Mobile App Architecture (2h)
  ```bash
  # Create MOBILE_APP_ARCHITECTURE.md
  # Choose: React Native (recommended)
  # Define tech stack, features, security
  # Create wireframes (optional)
  ```

- [ ] **Task 4.4.3:** Mobile API Endpoints (3h)
  ```bash
  # Create Mobile API controllers:
  # - MobileDashboardController
  # - MobileProductionController
  # - MobileInventoryController
  # - MobileSalesController
  # - MobileNotificationsController
  # - MobileUserController
  # Features: Cursor pagination, ETag, field selection
  ```

- [ ] **Task 4.4.4:** Push Notifications (2h)
  ```bash
  dotnet add RMMS.Web package FirebaseAdmin
  # Create DeviceTokens table
  # Create PushNotificationService
  # Create notification templates
  # Integrate into business events
  ```

**After Sprint 4.4:**
- ✅ Test SignalR in 2 browsers
- ✅ Test mobile API endpoints
- ✅ Register test device token
- ✅ Receive push notification on device

---

## INSTALLATION COMMANDS (All NuGet Packages)

```bash
# Sprint 4.1
dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add RMMS.Web package System.IdentityModel.Tokens.Jwt
dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning
dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer
dotnet add RMMS.Web package AspNetCoreRateLimit
dotnet add RMMS.Web package AspNetCore.HealthChecks.SqlServer
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.Client
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.InMemory.Storage

# Sprint 4.2
dotnet add RMMS.Web package Swashbuckle.AspNetCore
dotnet add RMMS.Web package Swashbuckle.AspNetCore.Annotations
dotnet add RMMS.Web package Swashbuckle.AspNetCore.Filters
dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.Google
dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.MicrosoftAccount
dotnet add RMMS.Web package IdentityModel.AspNetCore.OAuth2Introspection

# Sprint 4.3
dotnet add RMMS.Web package Hangfire.Core
dotnet add RMMS.Web package Hangfire.AspNetCore
dotnet add RMMS.Web package Hangfire.SqlServer
dotnet add RMMS.Web package Stripe.net
dotnet add RMMS.Web package PayPal.Core
dotnet add RMMS.Web package Twilio
dotnet add RMMS.Web package SendGrid

# Sprint 4.4
dotnet add RMMS.Web package FirebaseAdmin

# Total: 25 packages
```

---

## DATABASE SCRIPTS

### JWT & Authentication
```sql
-- Refresh Tokens
CREATE TABLE RefreshTokens (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Token NVARCHAR(500) NOT NULL,
    UserId NVARCHAR(100) NOT NULL,
    ExpiresAt DATETIME2 NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    RevokedAt DATETIME2 NULL,
    IsRevoked BIT NOT NULL DEFAULT 0
);
CREATE INDEX IX_RefreshTokens_Token ON RefreshTokens(Token);

-- API Keys
CREATE TABLE ApiKeys (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    KeyName NVARCHAR(100) NOT NULL,
    ApiKey NVARCHAR(500) NOT NULL UNIQUE,
    SecretHash NVARCHAR(500) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    ExpiresAt DATETIME2 NULL
);

-- External Logins (OAuth)
CREATE TABLE ExternalLogins (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId NVARCHAR(100) NOT NULL,
    Provider NVARCHAR(50) NOT NULL,
    ProviderKey NVARCHAR(200) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    UNIQUE (Provider, ProviderKey)
);
```

### API Usage & Analytics
```sql
CREATE TABLE ApiUsageLogs (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    Timestamp DATETIME2 NOT NULL DEFAULT GETDATE(),
    UserId NVARCHAR(100) NULL,
    Endpoint NVARCHAR(500) NOT NULL,
    HttpMethod NVARCHAR(10) NOT NULL,
    StatusCode INT NOT NULL,
    ResponseTimeMs INT NOT NULL
);
CREATE CLUSTERED INDEX IX_ApiUsageLogs_Timestamp ON ApiUsageLogs(Timestamp);
```

### Integrations
```sql
CREATE TABLE Integrations (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Type NVARCHAR(50) NOT NULL,
    Provider NVARCHAR(50) NOT NULL,
    IsEnabled BIT NOT NULL DEFAULT 0,
    ConfigurationJson NVARCHAR(MAX) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    LastSyncAt DATETIME2 NULL
);

CREATE TABLE IntegrationSyncLogs (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    IntegrationId INT NOT NULL,
    SyncStartedAt DATETIME2 NOT NULL,
    SyncCompletedAt DATETIME2 NULL,
    Status NVARCHAR(50) NOT NULL,
    RecordsProcessed INT NULL,
    FOREIGN KEY (IntegrationId) REFERENCES Integrations(Id)
);
```

### Webhooks
```sql
CREATE TABLE Webhooks (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Url NVARCHAR(500) NOT NULL,
    Secret NVARCHAR(200) NOT NULL,
    IsEnabled BIT NOT NULL DEFAULT 1,
    Events NVARCHAR(MAX) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE()
);

CREATE TABLE WebhookDeliveries (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    WebhookId INT NOT NULL,
    EventType NVARCHAR(100) NOT NULL,
    Payload NVARCHAR(MAX) NOT NULL,
    Status NVARCHAR(50) NOT NULL,
    AttemptCount INT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (WebhookId) REFERENCES Webhooks(Id)
);
```

### Payments
```sql
CREATE TABLE PaymentTransactions (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    TransactionId NVARCHAR(200) NOT NULL UNIQUE,
    Gateway NVARCHAR(50) NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Currency NVARCHAR(3) NOT NULL DEFAULT 'USD',
    Status NVARCHAR(50) NOT NULL,
    OrderId NVARCHAR(100) NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE()
);
```

### Notifications
```sql
CREATE TABLE NotificationLogs (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    Type NVARCHAR(50) NOT NULL,
    Recipient NVARCHAR(200) NOT NULL,
    Message NVARCHAR(MAX) NOT NULL,
    Status NVARCHAR(50) NOT NULL,
    SentAt DATETIME2 NOT NULL DEFAULT GETDATE()
);

CREATE TABLE DeviceTokens (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId NVARCHAR(100) NOT NULL,
    DeviceToken NVARCHAR(500) NOT NULL UNIQUE,
    Platform NVARCHAR(20) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    RegisteredAt DATETIME2 NOT NULL DEFAULT GETDATE()
);
```

---

## CONFIGURATION TEMPLATE

### appsettings.json Additions

```json
{
  "JwtSettings": {
    "SecretKey": "GENERATE_256_BIT_KEY_HERE",
    "Issuer": "RMMS_API",
    "Audience": "RMMS_Clients",
    "TokenExpirationMinutes": 60,
    "RefreshTokenExpirationDays": 7
  },

  "IpRateLimiting": {
    "EnableEndpointRateLimiting": true,
    "HttpStatusCode": 429,
    "GeneralRules": [
      { "Endpoint": "*", "Period": "1m", "Limit": 60 },
      { "Endpoint": "POST:/api/v1/auth/login", "Period": "1m", "Limit": 5 }
    ]
  },

  "CorsSettings": {
    "AllowedOrigins": ["http://localhost:3000", "http://localhost:8100"],
    "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
    "AllowCredentials": true
  },

  "OAuth": {
    "Google": {
      "ClientId": "YOUR_GOOGLE_CLIENT_ID",
      "ClientSecret": "YOUR_GOOGLE_CLIENT_SECRET"
    }
  },

  "Twilio": {
    "AccountSid": "YOUR_TWILIO_SID",
    "AuthToken": "YOUR_TWILIO_AUTH_TOKEN",
    "FromPhoneNumber": "+1234567890"
  },

  "SendGrid": {
    "ApiKey": "YOUR_SENDGRID_API_KEY",
    "FromEmail": "noreply@rmms.com",
    "FromName": "RMMS Notifications"
  },

  "Stripe": {
    "ApiKey": "YOUR_STRIPE_KEY",
    "WebhookSecret": "YOUR_WEBHOOK_SECRET"
  },

  "Firebase": {
    "ServiceAccountKeyPath": "firebase-service-account.json"
  }
}
```

---

## TESTING CHECKLIST

### ✅ API Testing (Postman)
- [ ] POST /api/v1/auth/login (get JWT token)
- [ ] GET /api/v1/customers (with Bearer token)
- [ ] GET /api/v1/customers (without token) → 401
- [ ] GET /api/v1/inventory/stock
- [ ] GET /api/v1/production/batches
- [ ] GET /health → "Healthy"
- [ ] GET /api-docs → Swagger UI loads

### ✅ Rate Limiting
- [ ] Make 61 requests in 1 minute → 61st gets 429
- [ ] Make 6 login attempts → 6th gets 429

### ✅ Integrations
- [ ] Create webhook at webhook.site
- [ ] Trigger event → verify webhook received
- [ ] Access /hangfire → dashboard loads
- [ ] Verify scheduled jobs listed
- [ ] Complete Stripe test payment
- [ ] Send test SMS
- [ ] Send test email

### ✅ Real-Time
- [ ] Open dashboard in 2 browsers
- [ ] Update data in browser 1
- [ ] Verify update in browser 2 instantly

### ✅ Mobile
- [ ] GET /api/v1/mobile/dashboard
- [ ] Verify response size < 50KB
- [ ] Register device token
- [ ] Trigger notification → received on device

---

## COMMON ISSUES & SOLUTIONS

### Issue: JWT Token Not Working
**Solution:** Verify JwtSettings.SecretKey is at least 256 bits (32 characters)

### Issue: Rate Limiting Not Working
**Solution:** Ensure `app.UseIpRateLimiting()` is before `app.UseRouting()`

### Issue: CORS Error
**Solution:** Add origin to AllowedOrigins in appsettings.json

### Issue: Hangfire Jobs Not Running
**Solution:** Check Hangfire dashboard (/hangfire) for errors

### Issue: Webhook Not Receiving
**Solution:** Verify HMAC signature generation matches on both sides

### Issue: Push Notification Not Received
**Solution:**
1. Check Firebase service account JSON is correct
2. Verify device token is registered
3. Check device token is not expired

### Issue: Swagger Not Showing Endpoints
**Solution:** Ensure XML documentation generation enabled in .csproj

---

## PERFORMANCE TARGETS

| Metric | Target | Monitoring |
|--------|--------|------------|
| API Response Time (P95) | <500ms | Health checks, logs |
| JWT Generation Time | <50ms | Performance logs |
| Rate Limiting Overhead | <5ms | Middleware timing |
| Webhook Delivery Time | <2s | WebhookDeliveries table |
| ERP Sync Duration | <5 minutes | IntegrationSyncLogs |
| Push Notification Delivery | <3s | FCM metrics |
| SignalR Message Latency | <100ms | Client-side timing |

---

## SECURITY CHECKLIST

- [ ] JWT secret is strong (256+ bits)
- [ ] API keys stored hashed (not plain text)
- [ ] Refresh tokens revoked on logout
- [ ] Rate limiting configured
- [ ] CORS properly restricted (not *)
- [ ] Webhook signatures verified (HMAC)
- [ ] Payment gateway uses test keys initially
- [ ] Sensitive config in Key Vault (not appsettings)
- [ ] HTTPS enforced in production
- [ ] SQL injection prevented (EF Core parameterization)
- [ ] XSS prevented (API doesn't render HTML)
- [ ] Authentication required on all sensitive endpoints

---

## QUICK REFERENCE: Key Files to Create

### Sprint 4.1
```
RMMS.Web/Controllers/API/BaseApiController.cs
RMMS.Web/Controllers/API/v1/AuthController.cs
RMMS.Web/Controllers/API/v1/CustomersApiController.cs
RMMS.Web/Controllers/API/v1/InventoryApiController.cs
RMMS.Web/Controllers/API/v1/ProductionApiController.cs
RMMS.Services/Services/Authentication/IJwtService.cs
RMMS.Services/Services/Authentication/JwtService.cs
RMMS.Web/Middleware/ApiExceptionMiddleware.cs
```

### Sprint 4.2
```
RMMS.Web/Filters/HangfireAuthorizationFilter.cs
RMMS.Web/Authentication/ApiKeyAuthenticationHandler.cs
RMMS.Web/Middleware/ApiUsageTrackingMiddleware.cs
RMMS.Web/Middleware/ApiThrottlingMiddleware.cs
```

### Sprint 4.3
```
RMMS.Services/Services/Integrations/IIntegrationService.cs
RMMS.Services/Services/Integrations/IWebhookService.cs
RMMS.Services/Services/Integrations/WebhookService.cs
RMMS.Services/Jobs/DailyInventoryReportJob.cs
RMMS.Services/Services/Integrations/Erp/QuickBooksIntegrationService.cs
RMMS.Services/Services/Payments/IStripeService.cs
RMMS.Services/Services/Notifications/ISmsService.cs
```

### Sprint 4.4
```
RMMS.Web/Hubs/ProductionHub.cs
RMMS.Web/Hubs/DashboardHub.cs
RMMS.Web/Hubs/NotificationHub.cs
RMMS.Web/Controllers/API/v1/Mobile/MobileDashboardController.cs
RMMS.Services/Services/Notifications/IPushNotificationService.cs
docs/MOBILE_APP_ARCHITECTURE.md
```

---

## SUCCESS METRICS

At the end of Phase 4, you should have:

✅ **API Endpoints:** 50+ REST API endpoints
✅ **Authentication:** JWT + API Key + OAuth2
✅ **Documentation:** Complete Swagger UI
✅ **Integrations:** ERP + Payment + SMS/Email + Webhooks
✅ **Background Jobs:** 5+ scheduled jobs via Hangfire
✅ **Real-Time:** SignalR hubs for live updates
✅ **Mobile Ready:** Mobile-optimized API endpoints
✅ **Push Notifications:** FCM integration working
✅ **Security:** Rate limiting + CORS + API usage tracking
✅ **Monitoring:** Health checks + Analytics + Logging

**Total New Code:** ~15,000 lines
**Total New API Endpoints:** ~60 endpoints
**Total New Database Tables:** ~15 tables
**Total External Integrations:** 6+ (Stripe, Twilio, SendGrid, Firebase, ERP, OAuth)

---

## DEPLOYMENT COMMAND

```bash
# After all sprints complete:

# 1. Run all SQL scripts
sqlcmd -S localhost -d RMMS_Production -i phase4_database_setup.sql

# 2. Build
dotnet build --configuration Release

# 3. Run tests
dotnet test

# 4. Publish
dotnet publish -c Release -o ./publish

# 5. Deploy (adjust for your environment)
# Azure: az webapp deploy...
# AWS: eb deploy...
# Docker: docker build -t rmms-api . && docker push...

# 6. Verify
curl https://your-api.com/health
curl https://your-api.com/api-docs

# 7. Celebrate! 🎉
```

---

## NEXT: Start Implementation!

1. **Read:** `PHASE4_ULTRATHINK_COMPREHENSIVE_PLAN.md` for full details
2. **Start:** Sprint 4.1, Task 4.1.1
3. **Track:** Update PROGRESS_TRACKER.md after each task
4. **Test:** Use Postman after each sprint
5. **Document:** Update API documentation as you go

**Estimated Timeline:**
- Week 1: Sprint 4.1 + 4.2 (API foundation + security)
- Week 2: Sprint 4.3 (Integrations)
- Week 3: Sprint 4.4 (Mobile + real-time)

**Parallel with Phase 3:** Can be done simultaneously!

---

**Good luck! 🚀**

**Questions?** Refer to the comprehensive plan or ask Claude for clarification on specific tasks.

---
