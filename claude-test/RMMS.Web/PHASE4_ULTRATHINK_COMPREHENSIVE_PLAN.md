# PHASE 4: INTEGRATION & MOBILE - ULTRATHINK COMPREHENSIVE PLAN
## 100% Success Rate Implementation Roadmap

**Document Version:** 1.0
**Created:** 2025-10-13
**Author:** Claude Code (Ultrathink Mode)
**Estimated Duration:** 60 hours (24 tasks)
**Success Rate Target:** 100%

---

## EXECUTIVE SUMMARY

This document provides a comprehensive, step-by-step implementation plan for **Phase 4: Integration & Mobile** of the RMMS (Rice Mill Management System). The plan is designed for parallel execution with Phase 3, enabling faster overall completion.

**Current State Analysis:**
- ✅ Phase 1 & 2: 100% Complete (186 tasks)
- ✅ Phase 3.1 & 3.2: Complete (Analytics + Performance)
- ✅ Solid foundation: 232 C# files, 32 controllers, 38 tables, 93 stored procedures
- ✅ Repository + Service pattern architecture in place
- ✅ Cookie-based authentication working
- ⚠️ **Gap:** No REST APIs, JWT auth, mobile integration, or third-party connectors

**Phase 4 Objectives:**
1. Build production-ready REST API layer
2. Implement JWT authentication for API consumers
3. Add comprehensive API documentation (Swagger/OpenAPI)
4. Create third-party integration framework
5. Design mobile app architecture
6. Implement real-time communication (SignalR)
7. Add webhooks, scheduled jobs, and external integrations

---

## TABLE OF CONTENTS

1. [Architecture Overview](#architecture-overview)
2. [Sprint 4.1: REST API Foundation](#sprint-41-rest-api-foundation-8-tasks)
3. [Sprint 4.2: API Documentation & Security](#sprint-42-api-documentation--security-6-tasks)
4. [Sprint 4.3: Third-Party Integrations](#sprint-43-third-party-integrations-6-tasks)
5. [Sprint 4.4: Mobile & Real-Time](#sprint-44-mobile--real-time-4-tasks)
6. [Success Criteria & Testing](#success-criteria--testing)
7. [Risk Mitigation](#risk-mitigation)
8. [Deployment Guide](#deployment-guide)

---

## ARCHITECTURE OVERVIEW

### Current Architecture (Phase 1-3)

```
┌─────────────────────────────────────────────────────┐
│                   RMMS.Web (MVC)                    │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Controllers │──│    Views     │──│   Models  │ │
│  │   (32)      │  │    (166)     │  │           │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│              RMMS.Services (Business Logic)         │
│  ┌──────────────────────────────────────────────┐  │
│  │ CustomerService, InventoryService, etc.      │  │
│  │ (40+ services implementing business logic)   │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│          RMMS.DataAccess (Data Layer)               │
│  ┌──────────────────────────────────────────────┐  │
│  │ Repositories + ApplicationDbContext          │  │
│  │ (30+ repositories for data access)           │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│           SQL Server (RMMS_Production)              │
│  38 Tables | 93 Stored Procedures | 3,426 Rows     │
└─────────────────────────────────────────────────────┘
```

### Target Architecture (Phase 4 Complete)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐ │
│  │   MVC Web UI   │  │  REST API      │  │  Mobile App          │ │
│  │  (Existing)    │  │  (NEW)         │  │  (Architecture)      │ │
│  │  - 32 Ctrl     │  │  - API v1      │  │  - React Native or   │ │
│  │  - 166 Views   │  │  - Swagger UI  │  │    Flutter           │ │
│  │  - Cookie Auth │  │  - JWT Auth    │  │  - Offline Support   │ │
│  └────────────────┘  └────────────────┘  └──────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                      INTEGRATION LAYER (NEW)                        │
│  ┌────────────────┐  ┌─────────────┐  ┌────────────────────────┐  │
│  │  API Gateway   │  │  Webhooks   │  │  Real-Time (SignalR)   │  │
│  │  - Rate Limit  │  │  - Events   │  │  - Push Notifications  │  │
│  │  - Logging     │  │  - Triggers │  │  - Live Updates        │  │
│  │  - Versioning  │  │             │  │                        │  │
│  └────────────────┘  └─────────────┘  └────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         RMMS.Services (Existing - Reused for API)            │  │
│  │  CustomerService, InventoryService, ProductionService, etc.  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                         DATA ACCESS LAYER                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │    RMMS.DataAccess (Existing - Optimized in Phase 3.2)      │  │
│  │    - Repositories, DbContext, Connection Pooling             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                  EXTERNAL INTEGRATIONS (NEW)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │   Payment    │  │   SMS/Email  │  │   ERP/Accounting         │ │
│  │   Gateway    │  │   Services   │  │   Systems                │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## SPRINT 4.1: REST API FOUNDATION (8 TASKS)

**Duration:** 20 hours
**Priority:** CRITICAL
**Dependencies:** None (Phase 1-2 services already complete)

### Task 4.1.1: Create API Project Structure (2 hours)

**Objective:** Set up dedicated API controllers separate from MVC controllers.

**Implementation Steps:**

1. **Create API Controllers Folder Structure**
   ```bash
   mkdir -p RMMS.Web/Controllers/API/v1
   ```

2. **Create Base API Controller**
   - File: `RMMS.Web/Controllers/API/BaseApiController.cs`
   - Features:
     - Inherit from `ControllerBase` (not `Controller` - no views)
     - Add `[ApiController]` attribute for automatic model validation
     - Add `[Route("api/v1/[controller]")]` for versioned routing
     - Implement standard API response format:
       ```csharp
       public class ApiResponse<T>
       {
           public bool Success { get; set; }
           public string Message { get; set; }
           public T Data { get; set; }
           public List<string> Errors { get; set; }
           public DateTime Timestamp { get; set; } = DateTime.UtcNow;
       }
       ```

3. **Update Program.cs**
   ```csharp
   // Add JSON options for API
   builder.Services.AddControllers()
       .AddJsonOptions(options =>
       {
           options.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
           options.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
           options.JsonSerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
       });
   ```

**Success Criteria:**
- ✅ API controllers folder structure created
- ✅ BaseApiController compiles without errors
- ✅ JSON serialization configured for camelCase
- ✅ Standard response format defined

**Testing:**
- Create a test controller (HealthController) that returns `{ "status": "healthy" }`
- Verify endpoint responds at `/api/v1/health`

---

### Task 4.1.2: Implement JWT Authentication (3 hours)

**Objective:** Add JWT-based authentication for API consumers (separate from cookie auth for web).

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.JwtBearer
   dotnet add RMMS.Web package System.IdentityModel.Tokens.Jwt
   ```

2. **Add JWT Configuration to appsettings.json**
   ```json
   "JwtSettings": {
     "SecretKey": "YOUR_256_BIT_SECRET_KEY_GENERATE_SECURELY",
     "Issuer": "RMMS_API",
     "Audience": "RMMS_Clients",
     "TokenExpirationMinutes": 60,
     "RefreshTokenExpirationDays": 7
   }
   ```

3. **Create JWT Service**
   - File: `RMMS.Services/Services/Authentication/IJwtService.cs`
   - File: `RMMS.Services/Services/Authentication/JwtService.cs`
   - Methods:
     - `GenerateAccessToken(string userId, string username, List<string> roles)`
     - `GenerateRefreshToken()`
     - `ValidateToken(string token)`
     - `GetPrincipalFromExpiredToken(string token)`

4. **Create Authentication API Controller**
   - File: `RMMS.Web/Controllers/API/v1/AuthController.cs`
   - Endpoints:
     - `POST /api/v1/auth/login` - Returns JWT access + refresh tokens
     - `POST /api/v1/auth/refresh` - Refresh expired access token
     - `POST /api/v1/auth/logout` - Invalidate refresh token
     - `GET /api/v1/auth/me` - Get current user info

5. **Update Program.cs for Dual Authentication**
   ```csharp
   // Add JWT Authentication (for API)
   builder.Services.AddAuthentication(options =>
   {
       options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
       options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
   })
   .AddJwtBearer(options =>
   {
       options.TokenValidationParameters = new TokenValidationParameters
       {
           ValidateIssuer = true,
           ValidateAudience = true,
           ValidateLifetime = true,
           ValidateIssuerSigningKey = true,
           ValidIssuer = jwtSettings.Issuer,
           ValidAudience = jwtSettings.Audience,
           IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings.SecretKey))
       };
   })
   .AddCookie(CookieAuthenticationDefaults.AuthenticationScheme, options =>
   {
       // Existing cookie config for MVC
   });
   ```

6. **Create Refresh Token Storage**
   - Add `RefreshToken` table to database:
     ```sql
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
     CREATE INDEX IX_RefreshTokens_UserId ON RefreshTokens(UserId);
     ```

**Success Criteria:**
- ✅ JWT service generates valid tokens
- ✅ `/api/v1/auth/login` returns access + refresh tokens
- ✅ Protected API endpoints require valid JWT
- ✅ Token refresh works correctly
- ✅ Cookie auth still works for MVC (no regression)

**Testing:**
- Test login with valid credentials → receive JWT tokens
- Test accessing protected endpoint with JWT → success
- Test accessing protected endpoint without JWT → 401 Unauthorized
- Test token refresh with valid refresh token → receive new access token
- Test MVC pages still work with cookie auth

---

### Task 4.1.3: Create Core API Controllers (4 hours)

**Objective:** Build REST API controllers for core modules (leveraging existing services).

**Implementation Steps:**

1. **Customers API Controller**
   - File: `RMMS.Web/Controllers/API/v1/CustomersApiController.cs`
   - Endpoints:
     ```
     GET    /api/v1/customers           - List all customers (with pagination)
     GET    /api/v1/customers/{id}      - Get customer by ID
     POST   /api/v1/customers           - Create new customer
     PUT    /api/v1/customers/{id}      - Update customer
     DELETE /api/v1/customers/{id}      - Delete customer
     GET    /api/v1/customers/search    - Search customers (by name, code, etc.)
     ```
   - Inject `ICustomerService` (already exists from Phase 1)
   - Add `[Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]`

2. **Products API Controller**
   - File: `RMMS.Web/Controllers/API/v1/ProductsApiController.cs`
   - Similar CRUD endpoints using `IProductService`

3. **Inventory API Controller**
   - File: `RMMS.Web/Controllers/API/v1/InventoryApiController.cs`
   - Endpoints:
     ```
     GET    /api/v1/inventory/stock                    - Current stock levels
     GET    /api/v1/inventory/stock/{productId}        - Stock by product
     GET    /api/v1/inventory/movements                - Stock movements
     POST   /api/v1/inventory/adjustments              - Create stock adjustment
     GET    /api/v1/inventory/warehouses/{id}/stock    - Stock by warehouse
     ```
   - Uses `IInventoryLedgerService`, `IStockMovementService`, `IStockAdjustmentService`

4. **Production API Controller**
   - File: `RMMS.Web/Controllers/API/v1/ProductionApiController.cs`
   - Endpoints:
     ```
     GET    /api/v1/production/orders           - Production orders
     POST   /api/v1/production/orders           - Create production order
     GET    /api/v1/production/batches          - Production batches
     POST   /api/v1/production/batches          - Create batch
     GET    /api/v1/production/yield/{batchId}  - Yield analysis
     ```

5. **Sales API Controller**
   - File: `RMMS.Web/Controllers/API/v1/SalesApiController.cs`
   - Endpoints for inquiries, quotations, orders

**Common Features for All API Controllers:**
- **Pagination:** Add `[FromQuery] int page = 1, [FromQuery] int pageSize = 50`
- **Filtering:** Add query parameters for filtering (e.g., `?status=Active&type=Customer`)
- **Sorting:** Add `[FromQuery] string sortBy, [FromQuery] string sortOrder`
- **Model Validation:** Leverage `[ApiController]` automatic validation
- **Error Handling:** Use try-catch with consistent error response format
- **Async/Await:** All methods must be async

**DTO Creation (Data Transfer Objects):**
- Create folder: `RMMS.Models/DTOs/API/`
- Create DTOs for requests and responses:
  - `CustomerRequestDto`, `CustomerResponseDto`
  - `ProductRequestDto`, `ProductResponseDto`
  - Difference from domain models: DTOs expose only necessary fields for API

**Success Criteria:**
- ✅ 5 core API controllers created
- ✅ All CRUD operations work via API
- ✅ Pagination, filtering, sorting functional
- ✅ JWT authentication required
- ✅ Consistent error responses
- ✅ All endpoints return 200/201/400/401/404/500 correctly

**Testing:**
- Use Postman/Insomnia to test all endpoints
- Test with valid JWT token
- Test without token (expect 401)
- Test pagination with different page sizes
- Test filtering and sorting

---

### Task 4.1.4: Implement API Versioning (1.5 hours)

**Objective:** Support multiple API versions for backward compatibility.

**Implementation Steps:**

1. **Install NuGet Package**
   ```bash
   dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning
   dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer
   ```

2. **Configure API Versioning in Program.cs**
   ```csharp
   builder.Services.AddApiVersioning(options =>
   {
       options.DefaultApiVersion = new ApiVersion(1, 0);
       options.AssumeDefaultVersionWhenUnspecified = true;
       options.ReportApiVersions = true;
       options.ApiVersionReader = ApiVersionReader.Combine(
           new UrlSegmentApiVersionReader(),
           new HeaderApiVersionReader("X-API-Version"),
           new QueryStringApiVersionReader("api-version")
       );
   });

   builder.Services.AddVersionedApiExplorer(options =>
   {
       options.GroupNameFormat = "'v'VVV";
       options.SubstituteApiVersionInUrl = true;
   });
   ```

3. **Update API Controller Routes**
   ```csharp
   [ApiController]
   [ApiVersion("1.0")]
   [Route("api/v{version:apiVersion}/[controller]")]
   public class CustomersApiController : BaseApiController
   {
       // Endpoints automatically versioned
   }
   ```

4. **Plan for V2 (Future)**
   - V1 endpoints remain stable
   - V2 can introduce breaking changes
   - Clients specify version in URL: `/api/v2/customers`

**Success Criteria:**
- ✅ API versioning configured
- ✅ V1 endpoints accessible at `/api/v1/...`
- ✅ API version reported in response headers
- ✅ Version can be specified via URL, header, or query string

**Testing:**
- Access endpoint with `/api/v1/customers` → works
- Access endpoint with `/api/customers` + header `X-API-Version: 1.0` → works
- Access endpoint without version → defaults to v1

---

### Task 4.1.5: Add API Error Handling & Logging (2 hours)

**Objective:** Centralized error handling with detailed logging for APIs.

**Implementation Steps:**

1. **Create API Exception Middleware**
   - File: `RMMS.Web/Middleware/ApiExceptionMiddleware.cs`
   - Features:
     - Catch all unhandled exceptions
     - Return consistent error response:
       ```json
       {
         "success": false,
         "message": "An error occurred",
         "errors": ["Detailed error message"],
         "timestamp": "2025-10-13T10:00:00Z",
         "traceId": "0HMVBE5O2N4PQ:00000001"
       }
       ```
     - Log exceptions with Serilog (already configured)
     - Don't expose sensitive info in production

2. **Create Custom API Exceptions**
   - File: `RMMS.Common/Exceptions/ApiException.cs`
   - Types:
     - `NotFoundException` → 404
     - `BadRequestException` → 400
     - `UnauthorizedException` → 401
     - `ForbiddenException` → 403
     - `ConflictException` → 409
     - `ValidationException` → 422

3. **Update Program.cs**
   ```csharp
   app.UseMiddleware<ApiExceptionMiddleware>();
   ```

4. **Add Request/Response Logging**
   - Already have Serilog configured
   - Add request logging for API calls:
     ```csharp
     app.UseSerilogRequestLogging(options =>
     {
         options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
         {
             diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
             diagnosticContext.Set("UserAgent", httpContext.Request.Headers["User-Agent"].ToString());
             diagnosticContext.Set("ClientIP", httpContext.Connection.RemoteIpAddress);
         };
     });
     ```

**Success Criteria:**
- ✅ All API exceptions caught and formatted consistently
- ✅ Exceptions logged with full context
- ✅ Production mode hides sensitive error details
- ✅ Development mode shows detailed stack traces
- ✅ Request/response logging works

**Testing:**
- Trigger various exceptions (404, 400, 500)
- Verify error response format
- Check logs for detailed error information
- Verify production mode doesn't leak sensitive data

---

### Task 4.1.6: Implement Rate Limiting (1.5 hours)

**Objective:** Protect API from abuse with rate limiting.

**Implementation Steps:**

1. **Install NuGet Package**
   ```bash
   dotnet add RMMS.Web package AspNetCoreRateLimit
   ```

2. **Configure Rate Limiting in Program.cs**
   ```csharp
   // Add memory cache for rate limiting
   builder.Services.AddMemoryCache();

   // Configure rate limiting
   builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting"));
   builder.Services.Configure<IpRateLimitPolicies>(builder.Configuration.GetSection("IpRateLimitPolicies"));

   builder.Services.AddSingleton<IIpPolicyStore, MemoryCacheIpPolicyStore>();
   builder.Services.AddSingleton<IRateLimitCounterStore, MemoryCacheRateLimitCounterStore>();
   builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();
   builder.Services.AddSingleton<IProcessingStrategy, AsyncKeyLockProcessingStrategy>();

   // Middleware
   app.UseIpRateLimiting();
   ```

3. **Add Configuration to appsettings.json**
   ```json
   "IpRateLimiting": {
     "EnableEndpointRateLimiting": true,
     "StackBlockedRequests": false,
     "RealIpHeader": "X-Real-IP",
     "ClientIdHeader": "X-ClientId",
     "HttpStatusCode": 429,
     "GeneralRules": [
       {
         "Endpoint": "*",
         "Period": "1m",
         "Limit": 60
       },
       {
         "Endpoint": "*",
         "Period": "1h",
         "Limit": 1000
       },
       {
         "Endpoint": "POST:/api/v1/auth/login",
         "Period": "1m",
         "Limit": 5
       }
     ]
   }
   ```

4. **Add Rate Limit Response Headers**
   - `X-Rate-Limit-Limit`
   - `X-Rate-Limit-Remaining`
   - `X-Rate-Limit-Reset`

**Success Criteria:**
- ✅ Rate limiting active for all API endpoints
- ✅ Login endpoint limited to 5 attempts/minute
- ✅ General endpoints limited to 60 requests/minute
- ✅ 429 status code returned when limit exceeded
- ✅ Rate limit headers included in responses

**Testing:**
- Make 70 requests in 1 minute → 61st request gets 429
- Make 6 login attempts in 1 minute → 6th attempt gets 429
- Check response headers for rate limit info

---

### Task 4.1.7: Create Health Check Endpoints (1 hour)

**Objective:** Monitor API and database health.

**Implementation Steps:**

1. **Install NuGet Package**
   ```bash
   dotnet add RMMS.Web package AspNetCore.HealthChecks.SqlServer
   dotnet add RMMS.Web package AspNetCore.HealthChecks.UI
   dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.Client
   dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.InMemory.Storage
   ```

2. **Configure Health Checks in Program.cs**
   ```csharp
   builder.Services.AddHealthChecks()
       .AddSqlServer(
           builder.Configuration.GetConnectionString("DefaultConnection"),
           name: "database",
           timeout: TimeSpan.FromSeconds(5),
           tags: new[] { "db", "sql", "sqlserver" })
       .AddDbContextCheck<ApplicationDbContext>(
           name: "dbcontext",
           tags: new[] { "efcore" });

   builder.Services.AddHealthChecksUI(setup =>
   {
       setup.SetEvaluationTimeInSeconds(30);
       setup.AddHealthCheckEndpoint("RMMS API", "/health");
   }).AddInMemoryStorage();
   ```

3. **Map Health Check Endpoints**
   ```csharp
   app.MapHealthChecks("/health", new HealthCheckOptions
   {
       Predicate = _ => true,
       ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
   });

   app.MapHealthChecks("/health/ready", new HealthCheckOptions
   {
       Predicate = check => check.Tags.Contains("ready"),
       ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
   });

   app.MapHealthChecks("/health/live", new HealthCheckOptions
   {
       Predicate = _ => true,
       ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
   });

   app.MapHealthChecksUI(options => options.UIPath = "/health-ui");
   ```

**Endpoints:**
- `GET /health` - Full health check (DB + app)
- `GET /health/ready` - Readiness probe (for K8s)
- `GET /health/live` - Liveness probe (for K8s)
- `GET /health-ui` - Health check dashboard UI

**Success Criteria:**
- ✅ `/health` endpoint returns JSON with health status
- ✅ Database health check works
- ✅ `/health-ui` dashboard accessible
- ✅ Health checks complete in <5 seconds

**Testing:**
- Access `/health` → verify 200 status and "Healthy" response
- Stop database → access `/health` → verify "Unhealthy" response
- Access `/health-ui` → verify dashboard UI loads

---

### Task 4.1.8: Add Request/Response Compression (1 hour)

**Objective:** Optimize API performance with compression (already partially done in Phase 3.2).

**Implementation Steps:**

1. **Verify Compression Configured** (from Phase 3.2)
   - Already have Brotli + Gzip configured
   - Verify working for API responses

2. **Add MIME Types for API**
   ```csharp
   builder.Services.AddResponseCompression(options =>
   {
       options.EnableForHttps = true;
       options.MimeTypes = ResponseCompressionDefaults.MimeTypes.Concat(new[]
       {
           "application/json",
           "application/xml",
           "text/json",
           "text/xml"
       });
   });
   ```

3. **Add Request Decompression** (for large POST/PUT payloads)
   ```csharp
   builder.Services.AddRequestDecompression(options =>
   {
       options.DecompressionProviders.Add("br", new BrotliDecompressionProvider());
       options.DecompressionProviders.Add("gzip", new GZipDecompressionProvider());
   });

   app.UseRequestDecompression();
   ```

**Success Criteria:**
- ✅ API responses compressed (Brotli/Gzip)
- ✅ Large request payloads can be compressed
- ✅ `Content-Encoding` header present in responses

**Testing:**
- Make API request → verify `Content-Encoding: br` or `gzip` header
- Compare response sizes with/without compression
- Send compressed POST request → verify server decompresses

---

## SPRINT 4.2: API DOCUMENTATION & SECURITY (6 TASKS)

**Duration:** 15 hours
**Priority:** HIGH
**Dependencies:** Sprint 4.1 complete

### Task 4.2.1: Implement Swagger/OpenAPI Documentation (3 hours)

**Objective:** Auto-generate comprehensive API documentation.

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Swashbuckle.AspNetCore
   dotnet add RMMS.Web package Swashbuckle.AspNetCore.Annotations
   dotnet add RMMS.Web package Swashbuckle.AspNetCore.Filters
   ```

2. **Configure Swagger in Program.cs**
   ```csharp
   builder.Services.AddSwaggerGen(options =>
   {
       options.SwaggerDoc("v1", new OpenApiInfo
       {
           Title = "RMMS API",
           Version = "v1",
           Description = "Rice Mill Management System REST API",
           Contact = new OpenApiContact
           {
               Name = "RMMS Support",
               Email = "support@rmms.com"
           },
           License = new OpenApiLicense
           {
               Name = "Proprietary",
               Url = new Uri("https://rmms.com/license")
           }
       });

       // JWT Authentication in Swagger
       options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
       {
           Name = "Authorization",
           Type = SecuritySchemeType.Http,
           Scheme = "bearer",
           BearerFormat = "JWT",
           In = ParameterLocation.Header,
           Description = "Enter your JWT token"
       });

       options.AddSecurityRequirement(new OpenApiSecurityRequirement
       {
           {
               new OpenApiSecurityScheme
               {
                   Reference = new OpenApiReference
                   {
                       Type = ReferenceType.SecurityScheme,
                       Id = "Bearer"
                   }
               },
               Array.Empty<string>()
           }
       });

       // Include XML comments
       var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
       var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
       options.IncludeXmlComments(xmlPath);

       // Enable annotations
       options.EnableAnnotations();

       // Custom schema IDs to avoid conflicts
       options.CustomSchemaIds(type => type.FullName);
   });
   ```

3. **Enable XML Documentation Generation**
   - Edit `RMMS.Web/RMMS.Web.csproj`:
     ```xml
     <PropertyGroup>
       <GenerateDocumentationFile>true</GenerateDocumentationFile>
       <NoWarn>$(NoWarn);1591</NoWarn>
     </PropertyGroup>
     ```

4. **Add XML Comments to API Controllers**
   ```csharp
   /// <summary>
   /// Customers management API
   /// </summary>
   [ApiController]
   [ApiVersion("1.0")]
   [Route("api/v{version:apiVersion}/[controller]")]
   public class CustomersApiController : BaseApiController
   {
       /// <summary>
       /// Get all customers with pagination
       /// </summary>
       /// <param name="page">Page number (default: 1)</param>
       /// <param name="pageSize">Page size (default: 50)</param>
       /// <returns>Paginated list of customers</returns>
       /// <response code="200">Returns the list of customers</response>
       /// <response code="401">Unauthorized - invalid or missing JWT token</response>
       [HttpGet]
       [ProducesResponseType(typeof(ApiResponse<PaginatedResult<CustomerResponseDto>>), 200)]
       [ProducesResponseType(401)]
       public async Task<IActionResult> GetCustomers([FromQuery] int page = 1, [FromQuery] int pageSize = 50)
       {
           // Implementation
       }
   }
   ```

5. **Configure Swagger UI**
   ```csharp
   app.UseSwagger();
   app.UseSwaggerUI(options =>
   {
       options.SwaggerEndpoint("/swagger/v1/swagger.json", "RMMS API v1");
       options.RoutePrefix = "api-docs"; // Access at /api-docs
       options.DocumentTitle = "RMMS API Documentation";
       options.DefaultModelsExpandDepth(-1); // Hide schemas section by default
       options.DocExpansion(Swashbuckle.AspNetCore.SwaggerUI.DocExpansion.List);
       options.DisplayRequestDuration();
   });
   ```

6. **Add Swagger Examples** (using Swashbuckle.AspNetCore.Filters)
   ```csharp
   [SwaggerRequestExample(typeof(CustomerRequestDto), typeof(CustomerRequestExample))]
   [SwaggerResponseExample(200, typeof(CustomerResponseExample))]
   ```

**Success Criteria:**
- ✅ Swagger UI accessible at `/api-docs`
- ✅ All API endpoints documented
- ✅ JWT authentication testable in Swagger UI
- ✅ Request/response examples shown
- ✅ XML comments displayed in documentation

**Testing:**
- Navigate to `/api-docs`
- Click "Authorize" button, enter JWT token
- Test API endpoints directly from Swagger UI
- Verify all endpoints documented correctly

---

### Task 4.2.2: Implement CORS Policy (1.5 hours)

**Objective:** Configure Cross-Origin Resource Sharing for mobile/web clients.

**Implementation Steps:**

1. **Add CORS Configuration to appsettings.json**
   ```json
   "CorsSettings": {
     "AllowedOrigins": [
       "http://localhost:3000",
       "http://localhost:8100",
       "https://rmms-mobile.com",
       "https://rmms-web.com"
     ],
     "AllowedMethods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
     "AllowedHeaders": ["*"],
     "ExposedHeaders": ["X-Total-Count", "X-Rate-Limit-Limit"],
     "AllowCredentials": true,
     "MaxAge": 600
   }
   ```

2. **Configure CORS in Program.cs**
   ```csharp
   var corsSettings = builder.Configuration.GetSection("CorsSettings");

   builder.Services.AddCors(options =>
   {
       options.AddPolicy("RMMSCorsPolicy", policy =>
       {
           policy.WithOrigins(corsSettings.GetSection("AllowedOrigins").Get<string[]>())
                 .WithMethods(corsSettings.GetSection("AllowedMethods").Get<string[]>())
                 .WithHeaders(corsSettings.GetSection("AllowedHeaders").Get<string[]>())
                 .WithExposedHeaders(corsSettings.GetSection("ExposedHeaders").Get<string[]>())
                 .SetIsOriginAllowedToAllowWildcardSubdomains()
                 .SetPreflightMaxAge(TimeSpan.FromSeconds(corsSettings.GetValue<int>("MaxAge")));

           if (corsSettings.GetValue<bool>("AllowCredentials"))
           {
               policy.AllowCredentials();
           }
       });

       // Development-only permissive policy
       options.AddPolicy("DevCorsPolicy", policy =>
       {
           policy.AllowAnyOrigin()
                 .AllowAnyMethod()
                 .AllowAnyHeader();
       });
   });

   // Use CORS
   if (app.Environment.IsDevelopment())
   {
       app.UseCors("DevCorsPolicy");
   }
   else
   {
       app.UseCors("RMMSCorsPolicy");
   }
   ```

3. **Test CORS with Preflight Requests**

**Success Criteria:**
- ✅ CORS configured for allowed origins
- ✅ Preflight OPTIONS requests handled correctly
- ✅ CORS headers present in responses
- ✅ Mobile/web apps can access API

**Testing:**
- Make API request from different origin (e.g., localhost:3000)
- Verify `Access-Control-Allow-Origin` header present
- Test OPTIONS preflight request

---

### Task 4.2.3: Add API Key Authentication (2 hours)

**Objective:** Provide API key authentication for server-to-server integrations.

**Implementation Steps:**

1. **Create API Keys Table**
   ```sql
   CREATE TABLE ApiKeys (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       KeyName NVARCHAR(100) NOT NULL,
       ApiKey NVARCHAR(500) NOT NULL UNIQUE,
       SecretHash NVARCHAR(500) NOT NULL,
       IsActive BIT NOT NULL DEFAULT 1,
       AllowedIPs NVARCHAR(MAX) NULL, -- JSON array of allowed IPs
       RateLimitPerMinute INT NOT NULL DEFAULT 60,
       CreatedBy NVARCHAR(100) NOT NULL,
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       ExpiresAt DATETIME2 NULL,
       LastUsedAt DATETIME2 NULL,
       Description NVARCHAR(500) NULL
   );
   CREATE INDEX IX_ApiKeys_ApiKey ON ApiKeys(ApiKey) WHERE IsActive = 1;
   ```

2. **Create API Key Model**
   - File: `RMMS.Models/Authentication/ApiKey.cs`

3. **Create API Key Service**
   - File: `RMMS.Services/Services/Authentication/IApiKeyService.cs`
   - File: `RMMS.Services/Services/Authentication/ApiKeyService.cs`
   - Methods:
     - `GenerateApiKey(string keyName, string createdBy)`
     - `ValidateApiKey(string apiKey, string ipAddress)`
     - `RevokeApiKey(string apiKey)`
     - `GetApiKeyDetails(string apiKey)`

4. **Create API Key Authentication Handler**
   - File: `RMMS.Web/Authentication/ApiKeyAuthenticationHandler.cs`
   - Check `X-API-Key` header
   - Validate against database
   - Check IP whitelist (if configured)
   - Track last used timestamp

5. **Register API Key Authentication**
   ```csharp
   builder.Services.AddAuthentication()
       .AddScheme<ApiKeyAuthenticationOptions, ApiKeyAuthenticationHandler>("ApiKey", options => { });
   ```

6. **Create API Key Management Controller**
   - File: `RMMS.Web/Controllers/API/v1/ApiKeysController.cs`
   - Endpoints (admin only):
     ```
     POST   /api/v1/apikeys          - Generate new API key
     GET    /api/v1/apikeys          - List all API keys
     DELETE /api/v1/apikeys/{id}     - Revoke API key
     GET    /api/v1/apikeys/{id}     - Get API key details
     ```

7. **Allow Both JWT and API Key Authentication**
   ```csharp
   [Authorize(AuthenticationSchemes = $"{JwtBearerDefaults.AuthenticationScheme},ApiKey")]
   ```

**Success Criteria:**
- ✅ API keys can be generated
- ✅ API requests work with `X-API-Key` header
- ✅ Invalid API keys rejected (401)
- ✅ IP whitelisting works (if configured)
- ✅ API key usage tracked

**Testing:**
- Generate API key via admin endpoint
- Make API request with `X-API-Key` header → success
- Make API request with invalid key → 401
- Test from whitelisted IP → success
- Test from non-whitelisted IP → 403

---

### Task 4.2.4: Implement OAuth2/OpenID Connect (3 hours)

**Objective:** Support OAuth2 for third-party authentication (Google, Microsoft, etc.).

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.Google
   dotnet add RMMS.Web package Microsoft.AspNetCore.Authentication.MicrosoftAccount
   dotnet add RMMS.Web package IdentityModel.AspNetCore.OAuth2Introspection
   ```

2. **Add OAuth Configuration to appsettings.json**
   ```json
   "OAuth": {
     "Google": {
       "ClientId": "YOUR_GOOGLE_CLIENT_ID",
       "ClientSecret": "YOUR_GOOGLE_CLIENT_SECRET"
     },
     "Microsoft": {
       "ClientId": "YOUR_MICROSOFT_CLIENT_ID",
       "ClientSecret": "YOUR_MICROSOFT_CLIENT_SECRET"
     }
   }
   ```

3. **Configure OAuth in Program.cs**
   ```csharp
   builder.Services.AddAuthentication()
       .AddGoogle(options =>
       {
           options.ClientId = builder.Configuration["OAuth:Google:ClientId"];
           options.ClientSecret = builder.Configuration["OAuth:Google:ClientSecret"];
           options.CallbackPath = "/api/v1/auth/google/callback";
       })
       .AddMicrosoftAccount(options =>
       {
           options.ClientId = builder.Configuration["OAuth:Microsoft:ClientId"];
           options.ClientSecret = builder.Configuration["OAuth:Microsoft:ClientSecret"];
           options.CallbackPath = "/api/v1/auth/microsoft/callback";
       });
   ```

4. **Create OAuth Controller**
   - File: `RMMS.Web/Controllers/API/v1/OAuthController.cs`
   - Endpoints:
     ```
     GET  /api/v1/auth/google           - Initiate Google OAuth
     GET  /api/v1/auth/google/callback  - Google callback
     GET  /api/v1/auth/microsoft         - Initiate Microsoft OAuth
     GET  /api/v1/auth/microsoft/callback - Microsoft callback
     ```
   - After OAuth success, generate JWT token for the user

5. **Create External Login Mapping Table**
   ```sql
   CREATE TABLE ExternalLogins (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       UserId NVARCHAR(100) NOT NULL,
       Provider NVARCHAR(50) NOT NULL, -- 'Google', 'Microsoft', etc.
       ProviderKey NVARCHAR(200) NOT NULL,
       ProviderDisplayName NVARCHAR(100),
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       UNIQUE (Provider, ProviderKey)
   );
   CREATE INDEX IX_ExternalLogins_UserId ON ExternalLogins(UserId);
   ```

**Success Criteria:**
- ✅ Users can authenticate with Google
- ✅ Users can authenticate with Microsoft
- ✅ OAuth callbacks handled correctly
- ✅ JWT token generated after successful OAuth
- ✅ External login linked to user account

**Testing:**
- Click Google OAuth link → redirected to Google → authenticate → receive JWT
- Click Microsoft OAuth link → authenticate → receive JWT
- Verify JWT token contains user info from OAuth provider

---

### Task 4.2.5: Add API Usage Analytics (2 hours)

**Objective:** Track API usage for monitoring and billing.

**Implementation Steps:**

1. **Create API Usage Tracking Table**
   ```sql
   CREATE TABLE ApiUsageLogs (
       Id BIGINT IDENTITY(1,1) PRIMARY KEY,
       Timestamp DATETIME2 NOT NULL DEFAULT GETDATE(),
       UserId NVARCHAR(100) NULL,
       ApiKeyId INT NULL,
       Endpoint NVARCHAR(500) NOT NULL,
       HttpMethod NVARCHAR(10) NOT NULL,
       StatusCode INT NOT NULL,
       ResponseTimeMs INT NOT NULL,
       RequestSize BIGINT NULL,
       ResponseSize BIGINT NULL,
       IpAddress NVARCHAR(50) NULL,
       UserAgent NVARCHAR(500) NULL,
       ErrorMessage NVARCHAR(MAX) NULL
   );
   CREATE CLUSTERED INDEX IX_ApiUsageLogs_Timestamp ON ApiUsageLogs(Timestamp);
   CREATE INDEX IX_ApiUsageLogs_UserId ON ApiUsageLogs(UserId);
   CREATE INDEX IX_ApiUsageLogs_Endpoint ON ApiUsageLogs(Endpoint);
   ```

2. **Create API Usage Middleware**
   - File: `RMMS.Web/Middleware/ApiUsageTrackingMiddleware.cs`
   - Track:
     - Timestamp
     - User ID (from JWT)
     - API key ID (if used)
     - Endpoint
     - HTTP method
     - Status code
     - Response time
     - Request/response sizes
     - IP address
     - User agent

3. **Create API Analytics Controller**
   - File: `RMMS.Web/Controllers/API/v1/ApiAnalyticsController.cs`
   - Endpoints (admin only):
     ```
     GET /api/v1/analytics/usage/summary          - Usage summary
     GET /api/v1/analytics/usage/by-user          - Usage by user
     GET /api/v1/analytics/usage/by-endpoint      - Usage by endpoint
     GET /api/v1/analytics/usage/errors           - Error rate analytics
     GET /api/v1/analytics/usage/performance      - Performance metrics
     ```

4. **Add Usage Metrics Dashboard** (Optional - in Analytics section)

**Success Criteria:**
- ✅ All API requests logged
- ✅ Usage analytics queryable via admin API
- ✅ Performance impact minimal (<5ms overhead)
- ✅ Logs rotate/archive automatically

**Testing:**
- Make several API requests
- Query `/api/v1/analytics/usage/summary` → verify data logged
- Check database for usage logs
- Verify performance overhead is minimal

---

### Task 4.2.6: Implement API Request Throttling (1.5 hours)

**Objective:** Advanced request throttling beyond basic rate limiting.

**Implementation Steps:**

1. **Create Throttling Configuration**
   ```json
   "ApiThrottling": {
     "EnableThrottling": true,
     "MaxConcurrentRequests": 100,
     "MaxQueuedRequests": 200,
     "RequestTimeout": 30,
     "ThrottlingRules": [
       {
         "Endpoint": "POST:/api/v1/production/batches",
         "MaxConcurrentRequests": 5,
         "RequestTimeout": 60
       },
       {
         "Endpoint": "GET:/api/v1/inventory/stock",
         "MaxConcurrentRequests": 50,
         "RequestTimeout": 10
       }
     ]
   }
   ```

2. **Implement Throttling Middleware**
   - File: `RMMS.Web/Middleware/ApiThrottlingMiddleware.cs`
   - Use `SemaphoreSlim` for concurrency control
   - Queue excess requests
   - Return 503 if queue full

3. **Add Throttling Metrics**
   - Track concurrent requests
   - Track queued requests
   - Expose via health check or metrics endpoint

**Success Criteria:**
- ✅ Concurrent requests limited per configuration
- ✅ Excess requests queued (not rejected immediately)
- ✅ 503 returned when queue full
- ✅ Endpoint-specific throttling works

**Testing:**
- Send 150 concurrent requests
- Verify first 100 processed, next 50 queued
- Send 250+ concurrent requests → verify 503 after queue full
- Test endpoint-specific throttling

---

## SPRINT 4.3: THIRD-PARTY INTEGRATIONS (6 TASKS)

**Duration:** 15 hours
**Priority:** MEDIUM
**Dependencies:** Sprint 4.1 complete

### Task 4.3.1: Create Integration Framework (2.5 hours)

**Objective:** Build a flexible framework for third-party integrations.

**Implementation Steps:**

1. **Create Integration Models**
   - File: `RMMS.Models/Integrations/IntegrationConfig.cs`
   ```csharp
   public class IntegrationConfig
   {
       public int Id { get; set; }
       public string Name { get; set; }
       public string Type { get; set; } // 'ERP', 'Accounting', 'Payment', etc.
       public string Provider { get; set; } // 'SAP', 'QuickBooks', 'Stripe', etc.
       public bool IsEnabled { get; set; }
       public string ConfigurationJson { get; set; } // Encrypted JSON
       public DateTime CreatedAt { get; set; }
       public DateTime? LastSyncAt { get; set; }
   }
   ```

2. **Create Integration Interface**
   - File: `RMMS.Services/Interfaces/Integrations/IIntegrationService.cs`
   ```csharp
   public interface IIntegrationService
   {
       Task<bool> TestConnection(int integrationId);
       Task<IntegrationResult> SyncData(int integrationId, string dataType);
       Task<IntegrationResult> PushData(int integrationId, object data);
       Task<IntegrationResult> PullData(int integrationId, string dataType, DateTime? since);
   }
   ```

3. **Create Base Integration Service**
   - File: `RMMS.Services/Services/Integrations/BaseIntegrationService.cs`
   - Common functionality:
     - Authentication handling
     - Retry logic with exponential backoff
     - Error handling and logging
     - Rate limiting
     - Request/response caching

4. **Create Integration Database Tables**
   ```sql
   CREATE TABLE Integrations (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       Name NVARCHAR(100) NOT NULL,
       Type NVARCHAR(50) NOT NULL,
       Provider NVARCHAR(50) NOT NULL,
       IsEnabled BIT NOT NULL DEFAULT 0,
       ConfigurationJson NVARCHAR(MAX) NOT NULL, -- Encrypted
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       LastSyncAt DATETIME2 NULL,
       LastSyncStatus NVARCHAR(50) NULL,
       LastErrorMessage NVARCHAR(MAX) NULL
   );

   CREATE TABLE IntegrationSyncLogs (
       Id BIGINT IDENTITY(1,1) PRIMARY KEY,
       IntegrationId INT NOT NULL,
       SyncStartedAt DATETIME2 NOT NULL,
       SyncCompletedAt DATETIME2 NULL,
       Status NVARCHAR(50) NOT NULL, -- 'InProgress', 'Success', 'Failed'
       DataType NVARCHAR(100) NULL,
       RecordsProcessed INT NULL,
       RecordsFailed INT NULL,
       ErrorMessage NVARCHAR(MAX) NULL,
       FOREIGN KEY (IntegrationId) REFERENCES Integrations(Id)
   );
   CREATE INDEX IX_IntegrationSyncLogs_IntegrationId ON IntegrationSyncLogs(IntegrationId);
   CREATE INDEX IX_IntegrationSyncLogs_SyncStartedAt ON IntegrationSyncLogs(SyncStartedAt);
   ```

5. **Create Integration Management API**
   - File: `RMMS.Web/Controllers/API/v1/IntegrationsController.cs`
   - Endpoints:
     ```
     GET    /api/v1/integrations              - List integrations
     POST   /api/v1/integrations              - Create integration
     PUT    /api/v1/integrations/{id}         - Update integration
     DELETE /api/v1/integrations/{id}         - Delete integration
     POST   /api/v1/integrations/{id}/test    - Test connection
     POST   /api/v1/integrations/{id}/sync    - Trigger sync
     GET    /api/v1/integrations/{id}/logs    - Get sync logs
     ```

**Success Criteria:**
- ✅ Integration framework created
- ✅ Database tables for integrations
- ✅ Base integration service with retry logic
- ✅ Integration management API working
- ✅ Configuration stored securely (encrypted)

**Testing:**
- Create a test integration
- Test connection
- Trigger sync
- Verify logs recorded

---

### Task 4.3.2: Implement Webhook Support (2.5 hours)

**Objective:** Allow external systems to receive real-time notifications via webhooks.

**Implementation Steps:**

1. **Create Webhook Models**
   - File: `RMMS.Models/Integrations/Webhook.cs`
   ```csharp
   public class Webhook
   {
       public int Id { get; set; }
       public string Name { get; set; }
       public string Url { get; set; }
       public string Secret { get; set; } // For HMAC signature
       public bool IsEnabled { get; set; }
       public List<string> Events { get; set; } // JSON array
       public int RetryCount { get; set; }
       public DateTime CreatedAt { get; set; }
   }

   public class WebhookEvent
   {
       public string EventType { get; set; }
       public string ObjectType { get; set; }
       public string ObjectId { get; set; }
       public object Data { get; set; }
       public DateTime Timestamp { get; set; }
   }
   ```

2. **Create Webhook Database Tables**
   ```sql
   CREATE TABLE Webhooks (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       Name NVARCHAR(100) NOT NULL,
       Url NVARCHAR(500) NOT NULL,
       Secret NVARCHAR(200) NOT NULL,
       IsEnabled BIT NOT NULL DEFAULT 1,
       Events NVARCHAR(MAX) NOT NULL, -- JSON array
       RetryCount INT NOT NULL DEFAULT 3,
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       LastTriggeredAt DATETIME2 NULL
   );

   CREATE TABLE WebhookDeliveries (
       Id BIGINT IDENTITY(1,1) PRIMARY KEY,
       WebhookId INT NOT NULL,
       EventType NVARCHAR(100) NOT NULL,
       Payload NVARCHAR(MAX) NOT NULL,
       Status NVARCHAR(50) NOT NULL, -- 'Pending', 'Success', 'Failed'
       AttemptCount INT NOT NULL DEFAULT 0,
       LastAttemptAt DATETIME2 NULL,
       ResponseCode INT NULL,
       ResponseBody NVARCHAR(MAX) NULL,
       ErrorMessage NVARCHAR(MAX) NULL,
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       FOREIGN KEY (WebhookId) REFERENCES Webhooks(Id)
   );
   CREATE INDEX IX_WebhookDeliveries_WebhookId ON WebhookDeliveries(WebhookId);
   CREATE INDEX IX_WebhookDeliveries_Status ON WebhookDeliveries(Status) WHERE Status = 'Pending';
   ```

3. **Create Webhook Service**
   - File: `RMMS.Services/Services/Integrations/IWebhookService.cs`
   - File: `RMMS.Services/Services/Integrations/WebhookService.cs`
   - Methods:
     - `RegisterWebhook(Webhook webhook)`
     - `TriggerWebhook(string eventType, object data)`
     - `RetryFailedDeliveries()`
     - `GetWebhookDeliveries(int webhookId)`

4. **Create Webhook Background Service**
   - File: `RMMS.Services/Services/Integrations/WebhookDeliveryService.cs`
   - Process pending webhook deliveries
   - Retry failed deliveries with exponential backoff
   - Run every 30 seconds

5. **Add Webhook Signature** (HMAC-SHA256)
   ```csharp
   private string GenerateSignature(string payload, string secret)
   {
       using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
       var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(payload));
       return Convert.ToBase64String(hash);
   }
   ```
   - Add `X-Webhook-Signature` header to outgoing webhooks

6. **Create Webhook Management API**
   - File: `RMMS.Web/Controllers/API/v1/WebhooksController.cs`
   - Endpoints:
     ```
     GET    /api/v1/webhooks                - List webhooks
     POST   /api/v1/webhooks                - Create webhook
     PUT    /api/v1/webhooks/{id}           - Update webhook
     DELETE /api/v1/webhooks/{id}           - Delete webhook
     GET    /api/v1/webhooks/{id}/deliveries - Get delivery history
     POST   /api/v1/webhooks/{id}/test      - Send test webhook
     ```

7. **Integrate Webhooks into Domain Events**
   - Trigger webhooks when:
     - Production batch completed → `production.batch.completed`
     - Stock level low → `inventory.stock.low`
     - Sales order created → `sales.order.created`
     - Payment received → `payment.received`
   - Example:
     ```csharp
     // In ProductionBatchService.CompleteProductionBatch()
     await _webhookService.TriggerWebhook("production.batch.completed", new
     {
         BatchId = batch.Id,
         BatchCode = batch.BatchCode,
         CompletedAt = DateTime.UtcNow
     });
     ```

**Success Criteria:**
- ✅ Webhooks can be registered
- ✅ Webhooks triggered on domain events
- ✅ HMAC signature included in headers
- ✅ Failed deliveries retried automatically
- ✅ Delivery history tracked

**Testing:**
- Register a webhook pointing to RequestBin/Webhook.site
- Trigger an event (e.g., create production batch)
- Verify webhook received at target URL
- Verify HMAC signature is valid
- Test retry logic by making webhook fail initially

---

### Task 4.3.3: Add Scheduled Job System (Hangfire) (2.5 hours)

**Objective:** Enable background job processing and scheduled tasks.

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Hangfire.Core
   dotnet add RMMS.Web package Hangfire.AspNetCore
   dotnet add RMMS.Web package Hangfire.SqlServer
   ```

2. **Configure Hangfire in Program.cs**
   ```csharp
   // Add Hangfire services
   builder.Services.AddHangfire(configuration => configuration
       .SetDataCompatibilityLevel(CompatibilityLevel.Version_170)
       .UseSimpleAssemblyNameTypeSerializer()
       .UseRecommendedSerializerSettings()
       .UseSqlServerStorage(builder.Configuration.GetConnectionString("DefaultConnection"), new SqlServerStorageOptions
       {
           CommandBatchMaxTimeout = TimeSpan.FromMinutes(5),
           SlidingInvisibilityTimeout = TimeSpan.FromMinutes(5),
           QueuePollInterval = TimeSpan.Zero,
           UseRecommendedIsolationLevel = true,
           DisableGlobalLocks = true,
           SchemaName = "Hangfire"
       }));

   builder.Services.AddHangfireServer(options =>
   {
       options.WorkerCount = 5; // Number of concurrent workers
   });

   // Use Hangfire
   app.UseHangfireDashboard("/hangfire", new DashboardOptions
   {
       Authorization = new[] { new HangfireAuthorizationFilter() },
       DashboardTitle = "RMMS Background Jobs"
   });
   ```

3. **Create Hangfire Authorization Filter**
   - File: `RMMS.Web/Filters/HangfireAuthorizationFilter.cs`
   - Only allow authenticated admins to access dashboard

4. **Create Scheduled Jobs**
   - File: `RMMS.Services/Jobs/ScheduledJobs.cs`

   **Jobs to implement:**

   a) **Daily Inventory Report Job**
   ```csharp
   public class DailyInventoryReportJob
   {
       public async Task Execute()
       {
           // Generate daily inventory report
           // Email to stakeholders
       }
   }
   ```
   Schedule: Daily at 8:00 AM

   b) **Low Stock Alert Job**
   ```csharp
   public class LowStockAlertJob
   {
       public async Task Execute()
       {
           // Check items below reorder level
           // Send notifications
       }
   }
   ```
   Schedule: Every 6 hours

   c) **Production Efficiency Calculation Job**
   ```csharp
   public class ProductionEfficiencyJob
   {
       public async Task Execute()
       {
           // Calculate efficiency metrics
           // Update analytics dashboard
       }
   }
   ```
   Schedule: Daily at midnight

   d) **Data Cleanup Job**
   ```csharp
   public class DataCleanupJob
   {
       public async Task Execute()
       {
           // Archive old logs
           // Clean up expired tokens
       }
   }
   ```
   Schedule: Weekly on Sunday at 2:00 AM

   e) **Webhook Retry Job**
   ```csharp
   public class WebhookRetryJob
   {
       public async Task Execute()
       {
           // Retry failed webhook deliveries
       }
   }
   ```
   Schedule: Every 5 minutes

5. **Register Recurring Jobs**
   ```csharp
   // In Program.cs after app.Run()
   var recurringJobManager = app.Services.GetRequiredService<IRecurringJobManager>();

   recurringJobManager.AddOrUpdate<DailyInventoryReportJob>(
       "daily-inventory-report",
       job => job.Execute(),
       "0 8 * * *"); // 8:00 AM daily

   recurringJobManager.AddOrUpdate<LowStockAlertJob>(
       "low-stock-alert",
       job => job.Execute(),
       "0 */6 * * *"); // Every 6 hours

   recurringJobManager.AddOrUpdate<ProductionEfficiencyJob>(
       "production-efficiency",
       job => job.Execute(),
       "0 0 * * *"); // Midnight daily

   recurringJobManager.AddOrUpdate<DataCleanupJob>(
       "data-cleanup",
       job => job.Execute(),
       "0 2 * * 0"); // 2:00 AM on Sundays

   recurringJobManager.AddOrUpdate<WebhookRetryJob>(
       "webhook-retry",
       job => job.Execute(),
       "*/5 * * * *"); // Every 5 minutes
   ```

6. **Create Jobs Management API**
   - File: `RMMS.Web/Controllers/API/v1/JobsController.cs`
   - Endpoints:
     ```
     GET    /api/v1/jobs                - List all jobs
     POST   /api/v1/jobs/{jobId}/trigger - Trigger job manually
     GET    /api/v1/jobs/{jobId}/history - Get job execution history
     ```

**Success Criteria:**
- ✅ Hangfire configured and running
- ✅ Hangfire dashboard accessible at `/hangfire`
- ✅ 5 scheduled jobs registered
- ✅ Jobs execute on schedule
- ✅ Failed jobs retry automatically
- ✅ Job history visible in dashboard

**Testing:**
- Navigate to `/hangfire` dashboard
- Verify all 5 recurring jobs listed
- Trigger job manually → verify execution
- Check database for Hangfire tables
- Verify jobs execute on schedule

---

### Task 4.3.4: Create ERP/Accounting Integration (2.5 hours)

**Objective:** Integrate with external ERP/Accounting systems (SAP, QuickBooks, etc.).

**Implementation Steps:**

1. **Create ERP Integration Service**
   - File: `RMMS.Services/Services/Integrations/Erp/IErpIntegrationService.cs`
   - File: `RMMS.Services/Services/Integrations/Erp/ErpIntegrationService.cs`
   - Features:
     - Export sales orders
     - Export purchase orders
     - Export invoices
     - Sync customer/vendor master data
     - Sync chart of accounts
     - Export financial transactions

2. **Create QuickBooks Integration** (example implementation)
   - File: `RMMS.Services/Services/Integrations/Erp/QuickBooksIntegrationService.cs`
   - Use QuickBooks Online API
   - OAuth2 authentication
   - Sync:
     - Customers → QuickBooks Customers
     - Vendors → QuickBooks Vendors
     - Sales → QuickBooks Invoices
     - Purchases → QuickBooks Bills

3. **Create SAP Integration** (example implementation)
   - File: `RMMS.Services/Services/Integrations/Erp/SapIntegrationService.cs`
   - Use SAP Business One API or SAP OData API
   - Sync:
     - Master data (customers, vendors, products)
     - Sales orders → SAP Sales Orders
     - Production orders → SAP Production Orders

4. **Create Data Mapping Configuration**
   - File: `RMMS.Models/Integrations/Erp/ErpFieldMapping.cs`
   - Allow admins to map RMMS fields to ERP fields:
     ```json
     {
       "CustomerMapping": {
         "CustomerCode": "CustomerRef",
         "CustomerName": "DisplayName",
         "Email": "PrimaryEmailAddr.Address",
         "Phone": "PrimaryPhone.FreeFormNumber"
       }
     }
     ```

5. **Create Sync Scheduling**
   - Use Hangfire (from Task 4.3.3)
   - Schedule:
     - Master data sync: Daily at 2:00 AM
     - Transaction sync: Every 2 hours
     - Manual sync available via API

6. **Create ERP Integration API**
   - File: `RMMS.Web/Controllers/API/v1/ErpController.cs`
   - Endpoints:
     ```
     POST   /api/v1/erp/connect                 - Connect to ERP
     POST   /api/v1/erp/disconnect              - Disconnect
     POST   /api/v1/erp/sync/customers          - Sync customers
     POST   /api/v1/erp/sync/vendors            - Sync vendors
     POST   /api/v1/erp/sync/products           - Sync products
     POST   /api/v1/erp/sync/transactions       - Sync transactions
     GET    /api/v1/erp/sync/status             - Get sync status
     ```

**Success Criteria:**
- ✅ ERP integration framework created
- ✅ QuickBooks or SAP integration working (choose one)
- ✅ Data mapping configurable
- ✅ Scheduled sync working
- ✅ Manual sync available via API
- ✅ Sync errors logged and reported

**Testing:**
- Connect to QuickBooks/SAP test account
- Trigger customer sync → verify data in ERP
- Trigger sales order sync → verify invoices created in ERP
- Test scheduled sync
- Verify error handling for failed syncs

---

### Task 4.3.5: Add Payment Gateway Integration (2 hours)

**Objective:** Integrate payment gateways (Stripe, PayPal, etc.) for online payments.

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Stripe.net
   dotnet add RMMS.Web package PayPal.Core
   ```

2. **Create Payment Models**
   - File: `RMMS.Models/Payments/PaymentTransaction.cs`
   ```csharp
   public class PaymentTransaction
   {
       public int Id { get; set; }
       public string TransactionId { get; set; }
       public string Gateway { get; set; } // 'Stripe', 'PayPal'
       public decimal Amount { get; set; }
       public string Currency { get; set; }
       public string Status { get; set; } // 'Pending', 'Success', 'Failed'
       public string OrderId { get; set; }
       public string CustomerId { get; set; }
       public DateTime CreatedAt { get; set; }
       public DateTime? ProcessedAt { get; set; }
   }
   ```

3. **Create Payment Database Tables**
   ```sql
   CREATE TABLE PaymentTransactions (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       TransactionId NVARCHAR(200) NOT NULL UNIQUE,
       Gateway NVARCHAR(50) NOT NULL,
       Amount DECIMAL(18,2) NOT NULL,
       Currency NVARCHAR(3) NOT NULL DEFAULT 'USD',
       Status NVARCHAR(50) NOT NULL,
       OrderId NVARCHAR(100) NULL,
       CustomerId NVARCHAR(100) NULL,
       PaymentMethodId NVARCHAR(200) NULL,
       ErrorMessage NVARCHAR(MAX) NULL,
       GatewayResponse NVARCHAR(MAX) NULL,
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       ProcessedAt DATETIME2 NULL
   );
   CREATE INDEX IX_PaymentTransactions_OrderId ON PaymentTransactions(OrderId);
   CREATE INDEX IX_PaymentTransactions_Status ON PaymentTransactions(Status);
   ```

4. **Create Stripe Integration Service**
   - File: `RMMS.Services/Services/Payments/IStripeService.cs`
   - File: `RMMS.Services/Services/Payments/StripeService.cs`
   - Methods:
     - `CreatePaymentIntent(decimal amount, string currency, string orderId)`
     - `ConfirmPayment(string paymentIntentId)`
     - `RefundPayment(string paymentIntentId, decimal? amount)`
     - `GetPaymentStatus(string paymentIntentId)`

5. **Create PayPal Integration Service**
   - File: `RMMS.Services/Services/Payments/IPayPalService.cs`
   - File: `RMMS.Services/Services/Payments/PayPalService.cs`
   - Similar methods for PayPal API

6. **Create Payment API Controller**
   - File: `RMMS.Web/Controllers/API/v1/PaymentsController.cs`
   - Endpoints:
     ```
     POST   /api/v1/payments/intent             - Create payment intent
     POST   /api/v1/payments/confirm            - Confirm payment
     POST   /api/v1/payments/refund             - Refund payment
     GET    /api/v1/payments/{id}/status        - Get payment status
     POST   /api/v1/payments/webhook/stripe     - Stripe webhook
     POST   /api/v1/payments/webhook/paypal     - PayPal webhook
     ```

7. **Handle Webhooks from Payment Gateways**
   - Stripe webhook: Verify signature, handle events (payment succeeded, failed, etc.)
   - PayPal webhook: Verify signature, handle events

8. **Link Payments to Sales Orders**
   - Update SalesOrder status when payment received
   - Record payment against order
   - Send confirmation email

**Success Criteria:**
- ✅ Stripe integration working
- ✅ PayPal integration working (optional)
- ✅ Payment intent creation works
- ✅ Payment confirmation works
- ✅ Webhooks processed correctly
- ✅ Payment status tracked in database

**Testing:**
- Create payment intent with Stripe test key
- Complete payment using Stripe test card
- Verify payment status updated
- Test webhook by triggering test event from Stripe dashboard
- Test refund functionality

---

### Task 4.3.6: Implement SMS/Email Gateway Integration (2 hours)

**Objective:** Integrate with SMS/Email services (Twilio, SendGrid) for notifications.

**Implementation Steps:**

1. **Install NuGet Packages**
   ```bash
   dotnet add RMMS.Web package Twilio
   dotnet add RMMS.Web package SendGrid
   ```

2. **Update Configuration**
   ```json
   "Twilio": {
     "AccountSid": "YOUR_TWILIO_SID",
     "AuthToken": "YOUR_TWILIO_AUTH_TOKEN",
     "FromPhoneNumber": "+1234567890"
   },
   "SendGrid": {
     "ApiKey": "YOUR_SENDGRID_API_KEY",
     "FromEmail": "noreply@rmms.com",
     "FromName": "RMMS Notifications"
   }
   ```

3. **Enhance Email Notification Service** (already exists from Phase 2)
   - File: `RMMS.Services/Services/EmailNotificationService.cs`
   - Integrate with SendGrid instead of SMTP:
     ```csharp
     public async Task SendEmailAsync(string to, string subject, string htmlBody)
     {
         var client = new SendGridClient(_settings.ApiKey);
         var from = new EmailAddress(_settings.FromEmail, _settings.FromName);
         var toAddress = new EmailAddress(to);
         var msg = MailHelper.CreateSingleEmail(from, toAddress, subject, null, htmlBody);
         var response = await client.SendEmailAsync(msg);

         // Log result
     }
     ```

4. **Create SMS Service**
   - File: `RMMS.Services/Services/Notifications/ISmsService.cs`
   - File: `RMMS.Services/Services/Notifications/SmsService.cs`
   - Methods:
     - `SendSmsAsync(string phoneNumber, string message)`
     - `SendBulkSmsAsync(List<string> phoneNumbers, string message)`
   - Use Twilio API

5. **Create Notification Templates**
   - File: `RMMS.Services/Services/Notifications/NotificationTemplates.cs`
   - Templates for:
     - Order confirmation (SMS + Email)
     - Payment received (SMS + Email)
     - Low stock alert (Email)
     - Production batch completed (SMS + Email)
     - Shipment dispatched (SMS + Email)

6. **Create Notification API**
   - File: `RMMS.Web/Controllers/API/v1/NotificationsController.cs`
   - Endpoints:
     ```
     POST   /api/v1/notifications/sms           - Send SMS
     POST   /api/v1/notifications/email         - Send email
     POST   /api/v1/notifications/bulk          - Send bulk notifications
     GET    /api/v1/notifications/history       - Get notification history
     ```

7. **Track Notification Delivery**
   ```sql
   CREATE TABLE NotificationLogs (
       Id BIGINT IDENTITY(1,1) PRIMARY KEY,
       Type NVARCHAR(50) NOT NULL, -- 'SMS', 'Email'
       Recipient NVARCHAR(200) NOT NULL,
       Subject NVARCHAR(500) NULL,
       Message NVARCHAR(MAX) NOT NULL,
       Status NVARCHAR(50) NOT NULL, -- 'Sent', 'Failed', 'Delivered'
       Provider NVARCHAR(50) NOT NULL, -- 'Twilio', 'SendGrid'
       ProviderMessageId NVARCHAR(200) NULL,
       ErrorMessage NVARCHAR(MAX) NULL,
       SentAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       DeliveredAt DATETIME2 NULL
   );
   CREATE INDEX IX_NotificationLogs_Recipient ON NotificationLogs(Recipient);
   CREATE INDEX IX_NotificationLogs_Status ON NotificationLogs(Status);
   ```

8. **Integrate Notifications into Business Processes**
   - Production batch completed → Send SMS to production manager
   - Stock below reorder level → Send email to procurement team
   - Sales order created → Send confirmation email to customer
   - Payment received → Send SMS + email to customer

**Success Criteria:**
- ✅ SendGrid email integration working
- ✅ Twilio SMS integration working
- ✅ Notification templates created
- ✅ Notifications triggered by business events
- ✅ Delivery status tracked

**Testing:**
- Send test SMS to your phone → verify received
- Send test email → verify received
- Trigger business event (e.g., create order) → verify notification sent
- Check notification logs in database

---

## SPRINT 4.4: MOBILE & REAL-TIME (4 TASKS)

**Duration:** 10 hours
**Priority:** MEDIUM
**Dependencies:** Sprint 4.1 complete

### Task 4.4.1: Implement SignalR for Real-Time Updates (3 hours)

**Objective:** Enable real-time communication for live dashboards and notifications.

**Implementation Steps:**

1. **Install NuGet Package**
   ```bash
   dotnet add RMMS.Web package Microsoft.AspNetCore.SignalR
   ```

2. **Create SignalR Hubs**

   a) **Production Hub**
   - File: `RMMS.Web/Hubs/ProductionHub.cs`
   ```csharp
   public class ProductionHub : Hub
   {
       public async Task SubscribeToProductionUpdates(int machineId)
       {
           await Groups.AddToGroupAsync(Context.ConnectionId, $"machine_{machineId}");
       }

       public async Task UnsubscribeFromProductionUpdates(int machineId)
       {
           await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"machine_{machineId}");
       }
   }
   ```

   b) **Dashboard Hub**
   - File: `RMMS.Web/Hubs/DashboardHub.cs`
   ```csharp
   public class DashboardHub : Hub
   {
       public async Task SubscribeToDashboard()
       {
           await Groups.AddToGroupAsync(Context.ConnectionId, "dashboard");
       }
   }
   ```

   c) **Notification Hub**
   - File: `RMMS.Web/Hubs/NotificationHub.cs`
   ```csharp
   public class NotificationHub : Hub
   {
       public async Task SubscribeToNotifications(string userId)
       {
           await Groups.AddToGroupAsync(Context.ConnectionId, $"user_{userId}");
       }
   }
   ```

3. **Configure SignalR in Program.cs**
   ```csharp
   builder.Services.AddSignalR(options =>
   {
       options.EnableDetailedErrors = true;
       options.KeepAliveInterval = TimeSpan.FromSeconds(15);
       options.ClientTimeoutInterval = TimeSpan.FromSeconds(30);
   });

   // Map hubs
   app.MapHub<ProductionHub>("/hubs/production");
   app.MapHub<DashboardHub>("/hubs/dashboard");
   app.MapHub<NotificationHub>("/hubs/notifications");
   ```

4. **Integrate SignalR into Services**

   **Example: Real-time production updates**
   ```csharp
   // In ProductionBatchService
   public class ProductionBatchService
   {
       private readonly IHubContext<ProductionHub> _productionHub;

       public async Task UpdateBatchStatus(int batchId, string status)
       {
           // Update database
           // ...

           // Broadcast to connected clients
           await _productionHub.Clients.Group($"batch_{batchId}")
               .SendAsync("BatchStatusUpdated", new {
                   BatchId = batchId,
                   Status = status,
                   Timestamp = DateTime.UtcNow
               });
       }
   }
   ```

5. **Create SignalR Client Example** (JavaScript)
   ```javascript
   // File: RMMS.Web/wwwroot/js/signalr-client.js
   const connection = new signalR.HubConnectionBuilder()
       .withUrl("/hubs/production")
       .withAutomaticReconnect()
       .build();

   connection.on("BatchStatusUpdated", (data) => {
       console.log("Batch status updated:", data);
       // Update UI
   });

   connection.start().catch(err => console.error(err));

   // Subscribe to production updates for machine ID 5
   connection.invoke("SubscribeToProductionUpdates", 5);
   ```

6. **Real-Time Use Cases**

   a) **Live Production Dashboard**
   - Machine status updates (running, stopped, maintenance)
   - Real-time production metrics
   - Live batch progress

   b) **Live Inventory Dashboard**
   - Stock level changes
   - Stock movement alerts
   - Low stock warnings

   c) **Live Notifications**
   - New order notifications
   - Payment received notifications
   - System alerts

   d) **Collaborative Features**
   - Multiple users viewing/editing same record
   - Show who's online
   - Live chat/comments

**Success Criteria:**
- ✅ SignalR hubs created and configured
- ✅ Real-time updates work for production
- ✅ Real-time updates work for dashboard
- ✅ Real-time notifications work
- ✅ Automatic reconnection works

**Testing:**
- Open production dashboard in 2 browsers
- Update production batch in one browser
- Verify update appears in real-time in second browser
- Disconnect and reconnect → verify automatic reconnection
- Test with multiple concurrent users

---

### Task 4.4.2: Design Mobile App Architecture (2 hours)

**Objective:** Create comprehensive architecture design for mobile app.

**Implementation Steps:**

1. **Choose Mobile Framework**

   **Option A: React Native** (Recommended)
   - Single codebase for iOS + Android
   - JavaScript/TypeScript
   - Large ecosystem
   - Good performance

   **Option B: Flutter**
   - Single codebase for iOS + Android
   - Dart language
   - Excellent performance
   - Modern UI widgets

   **Recommendation:** React Native (team likely familiar with JavaScript)

2. **Create Mobile App Architecture Document**
   - File: `RMMS.Web/docs/MOBILE_APP_ARCHITECTURE.md`

   **Contents:**

   ```markdown
   # RMMS Mobile App Architecture

   ## Technology Stack
   - **Framework:** React Native 0.72+
   - **State Management:** Redux Toolkit
   - **Navigation:** React Navigation 6
   - **API Client:** Axios with interceptors
   - **Authentication:** JWT stored in secure storage
   - **Offline Support:** Redux Persist + AsyncStorage
   - **Push Notifications:** Firebase Cloud Messaging
   - **UI Library:** React Native Paper or NativeBase
   - **Charts:** Victory Native
   - **Forms:** React Hook Form
   - **Barcode Scanning:** React Native Camera

   ## App Structure
   ```
   rmms-mobile/
   ├── src/
   │   ├── api/              # API client, endpoints
   │   ├── components/       # Reusable components
   │   ├── screens/          # Screen components
   │   │   ├── Auth/
   │   │   ├── Dashboard/
   │   │   ├── Production/
   │   │   ├── Inventory/
   │   │   ├── Sales/
   │   │   └── Reports/
   │   ├── navigation/       # Navigation configuration
   │   ├── redux/            # Redux slices, store
   │   ├── services/         # Business logic services
   │   ├── utils/            # Utility functions
   │   ├── hooks/            # Custom React hooks
   │   ├── constants/        # Constants, enums
   │   └── types/            # TypeScript types
   ├── ios/                  # iOS native code
   ├── android/              # Android native code
   └── package.json
   ```

   ## Key Features

   ### Phase 1 (MVP)
   1. **Authentication**
      - Login with JWT
      - Biometric authentication (Face ID/Touch ID)
      - Remember me

   2. **Dashboard**
      - Summary cards (production, inventory, sales)
      - Recent activities
      - Quick actions

   3. **Production**
      - View production orders
      - View production batches
      - Update batch status
      - Real-time production metrics

   4. **Inventory**
      - View stock levels
      - Stock movements
      - Low stock alerts
      - Barcode scanning for stock lookup

   5. **Sales**
      - View sales orders
      - Create inquiries
      - View quotations

   6. **Notifications**
      - Push notifications
      - In-app notifications
      - Notification history

   ### Phase 2 (Advanced)
   1. **Offline Mode**
      - Cache data for offline access
      - Queue actions when offline
      - Sync when online

   2. **Camera Integration**
      - Barcode/QR code scanning
      - Photo capture for quality checks
      - Document scanning

   3. **Reports**
      - Production reports
      - Inventory reports
      - Sales reports
      - Export to PDF

   4. **Real-Time Updates**
      - SignalR integration
      - Live dashboard
      - Live production monitoring

   ## API Integration

   ### Authentication
   ```javascript
   // api/auth.js
   export const login = async (username, password) => {
     const response = await axios.post('/api/v1/auth/login', {
       username,
       password
     });
     return response.data;
   };
   ```

   ### JWT Token Management
   ```javascript
   // api/client.js
   axios.interceptors.request.use(async (config) => {
     const token = await SecureStore.getItemAsync('jwt_token');
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });

   axios.interceptors.response.use(
     (response) => response,
     async (error) => {
       if (error.response?.status === 401) {
         // Token expired, try refresh
         const refreshToken = await SecureStore.getItemAsync('refresh_token');
         const { data } = await axios.post('/api/v1/auth/refresh', {
           refreshToken
         });
         await SecureStore.setItemAsync('jwt_token', data.accessToken);
         // Retry original request
         return axios(error.config);
       }
       return Promise.reject(error);
     }
   );
   ```

   ### Offline Support
   ```javascript
   // redux/store.js
   import { configureStore } from '@reduxjs/toolkit';
   import { persistStore, persistReducer } from 'redux-persist';
   import AsyncStorage from '@react-native-async-storage/async-storage';

   const persistConfig = {
     key: 'root',
     storage: AsyncStorage,
     whitelist: ['auth', 'production', 'inventory']
   };

   const persistedReducer = persistReducer(persistConfig, rootReducer);

   export const store = configureStore({
     reducer: persistedReducer
   });

   export const persistor = persistStore(store);
   ```

   ## Push Notifications

   ### Firebase Cloud Messaging Setup
   1. Configure Firebase project
   2. Add FCM to React Native app
   3. Register device token with backend
   4. Handle notifications

   ```javascript
   // services/notifications.js
   import messaging from '@react-native-firebase/messaging';

   export const requestPermission = async () => {
     const authStatus = await messaging().requestPermission();
     return authStatus === messaging.AuthorizationStatus.AUTHORIZED;
   };

   export const getToken = async () => {
     const token = await messaging().getToken();
     // Send token to backend
     await api.registerDeviceToken(token);
     return token;
   };

   messaging().onMessage(async (remoteMessage) => {
     // Handle foreground notification
     showInAppNotification(remoteMessage);
   });
   ```

   ## Security Considerations

   1. **Secure Storage**
      - Store JWT in secure storage (Keychain/Keystore)
      - Never log sensitive data

   2. **Certificate Pinning**
      - Pin SSL certificates
      - Prevent MITM attacks

   3. **Code Obfuscation**
      - Obfuscate JavaScript bundle
      - Use ProGuard for Android

   4. **Biometric Authentication**
      - Require biometric for sensitive actions
      - Optional for login

   ## Testing Strategy

   1. **Unit Tests**
      - Jest for component testing
      - Redux logic testing

   2. **Integration Tests**
      - API integration tests
      - Navigation tests

   3. **E2E Tests**
      - Detox for end-to-end testing
      - Critical user flows

   ## Deployment

   ### iOS
   - Build with Xcode
   - TestFlight for beta testing
   - App Store submission

   ### Android
   - Build APK/AAB
   - Google Play Internal Testing
   - Google Play submission
   ```

3. **Create Mobile API Endpoint Requirements Document**
   - File: `RMMS.Web/docs/MOBILE_API_REQUIREMENTS.md`
   - List all API endpoints needed for mobile app
   - Specify request/response formats
   - Note any mobile-specific optimizations needed

4. **Create Mobile App UI/UX Wireframes** (Optional)
   - Use Figma/Sketch to create mockups
   - Key screens:
     - Login screen
     - Dashboard
     - Production list
     - Production detail
     - Inventory list
     - Barcode scanner
     - Notifications

**Success Criteria:**
- ✅ Mobile framework chosen (React Native)
- ✅ Architecture document created
- ✅ Technology stack defined
- ✅ Feature roadmap created
- ✅ API requirements documented
- ✅ Security considerations defined

**Testing:**
- Architecture review with team
- Validate technology choices
- Ensure API endpoints support mobile requirements

---

### Task 4.4.3: Build Mobile-Specific API Endpoints (3 hours)

**Objective:** Create optimized API endpoints for mobile consumption.

**Implementation Steps:**

1. **Create Mobile API Controller Base**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/BaseMobileApiController.cs`
   - Features:
     - Lightweight responses (no unnecessary data)
     - Image URLs instead of base64
     - Pagination with cursor-based approach (better for mobile)
     - Response compression

2. **Mobile Dashboard API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileDashboardController.cs`
   - Endpoints:
     ```
     GET /api/v1/mobile/dashboard              - Mobile-optimized dashboard
     GET /api/v1/mobile/dashboard/summary      - Summary cards data
     GET /api/v1/mobile/dashboard/activities   - Recent activities
     GET /api/v1/mobile/dashboard/alerts       - Active alerts
     ```
   - Response format:
     ```json
     {
       "summary": {
         "productionToday": { "value": 1250, "unit": "kg", "trend": "up", "change": 8.5 },
         "stockValue": { "value": 250000, "unit": "USD", "trend": "stable" },
         "ordersToday": { "value": 15, "trend": "up", "change": 3 },
         "alerts": { "value": 2, "severity": "medium" }
       },
       "recentActivities": [...],
       "alerts": [...]
     }
     ```

3. **Mobile Production API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileProductionController.cs`
   - Endpoints:
     ```
     GET    /api/v1/mobile/production/orders      - List production orders
     GET    /api/v1/mobile/production/orders/{id} - Order details
     GET    /api/v1/mobile/production/batches     - List batches
     GET    /api/v1/mobile/production/batches/{id}- Batch details
     PUT    /api/v1/mobile/production/batches/{id}/status - Update status
     POST   /api/v1/mobile/production/batches/{id}/note   - Add note
     ```
   - Mobile-specific features:
     - Include only essential fields
     - Pre-calculated totals
     - Image thumbnails (not full size)

4. **Mobile Inventory API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileInventoryController.cs`
   - Endpoints:
     ```
     GET    /api/v1/mobile/inventory/stock              - Stock levels
     GET    /api/v1/mobile/inventory/product/{code}     - Lookup by barcode
     GET    /api/v1/mobile/inventory/movements          - Recent movements
     POST   /api/v1/mobile/inventory/count              - Record stock count
     GET    /api/v1/mobile/inventory/alerts             - Low stock alerts
     ```

5. **Mobile Sales API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileSalesController.cs`
   - Endpoints:
     ```
     GET    /api/v1/mobile/sales/orders         - List orders
     GET    /api/v1/mobile/sales/orders/{id}    - Order details
     POST   /api/v1/mobile/sales/inquiries      - Create inquiry
     GET    /api/v1/mobile/sales/quotations     - List quotations
     ```

6. **Mobile Notifications API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileNotificationsController.cs`
   - Endpoints:
     ```
     GET    /api/v1/mobile/notifications              - List notifications
     PUT    /api/v1/mobile/notifications/{id}/read    - Mark as read
     PUT    /api/v1/mobile/notifications/read-all     - Mark all as read
     POST   /api/v1/mobile/device-token               - Register device token
     DELETE /api/v1/mobile/device-token               - Unregister device
     ```

7. **Mobile User API**
   - File: `RMMS.Web/Controllers/API/v1/Mobile/MobileUserController.cs`
   - Endpoints:
     ```
     GET    /api/v1/mobile/user/profile         - User profile
     PUT    /api/v1/mobile/user/profile         - Update profile
     PUT    /api/v1/mobile/user/password        - Change password
     GET    /api/v1/mobile/user/preferences     - Get preferences
     PUT    /api/v1/mobile/user/preferences     - Update preferences
     POST   /api/v1/mobile/user/avatar          - Upload avatar
     ```

8. **Mobile-Specific Optimizations**

   a) **Cursor-Based Pagination** (better for mobile)
   ```csharp
   public async Task<IActionResult> GetOrders([FromQuery] string cursor = null, [FromQuery] int limit = 20)
   {
       var orders = await _service.GetOrdersAsync(cursor, limit);
       var nextCursor = orders.Count == limit ? orders.Last().Id.ToString() : null;

       return Ok(new {
           data = orders,
           nextCursor,
           hasMore = nextCursor != null
       });
   }
   ```

   b) **Conditional Requests** (save bandwidth)
   ```csharp
   [HttpGet("{id}")]
   public async Task<IActionResult> GetOrder(int id)
   {
       var order = await _service.GetOrderAsync(id);

       var etag = $"\"{order.UpdatedAt:yyyyMMddHHmmss}\"";
       Response.Headers.ETag = etag;

       if (Request.Headers.IfNoneMatch == etag)
       {
           return StatusCode(304); // Not Modified
       }

       return Ok(order);
   }
   ```

   c) **Field Selection** (only return requested fields)
   ```csharp
   [HttpGet]
   public async Task<IActionResult> GetOrders([FromQuery] string fields = null)
   {
       var orders = await _service.GetOrdersAsync();

       if (!string.IsNullOrEmpty(fields))
       {
           var selectedFields = fields.Split(',');
           // Use dynamic projection to return only selected fields
       }

       return Ok(orders);
   }
   ```

**Success Criteria:**
- ✅ Mobile-optimized API controllers created
- ✅ All essential mobile endpoints implemented
- ✅ Cursor-based pagination working
- ✅ Conditional requests supported (ETag)
- ✅ Field selection supported
- ✅ Response sizes optimized for mobile

**Testing:**
- Test all mobile endpoints with Postman
- Compare response sizes with regular API endpoints
- Test cursor-based pagination
- Test ETag/conditional requests
- Verify response times <200ms for most endpoints

---

### Task 4.4.4: Add Push Notification Service (2 hours)

**Objective:** Implement server-side push notification infrastructure.

**Implementation Steps:**

1. **Install NuGet Package**
   ```bash
   dotnet add RMMS.Web package FirebaseAdmin
   ```

2. **Configure Firebase Admin SDK**
   - Download Firebase service account key JSON
   - Add to appsettings.json:
     ```json
     "Firebase": {
       "ServiceAccountKeyPath": "firebase-service-account.json",
       "DatabaseUrl": "https://your-project.firebaseio.com"
     }
     ```

3. **Initialize Firebase in Program.cs**
   ```csharp
   var firebaseApp = FirebaseApp.Create(new AppOptions()
   {
       Credential = GoogleCredential.FromFile(
           builder.Configuration["Firebase:ServiceAccountKeyPath"])
   });
   ```

4. **Create Push Notification Models**
   ```sql
   CREATE TABLE DeviceTokens (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       UserId NVARCHAR(100) NOT NULL,
       DeviceToken NVARCHAR(500) NOT NULL UNIQUE,
       Platform NVARCHAR(20) NOT NULL, -- 'iOS', 'Android'
       DeviceModel NVARCHAR(100) NULL,
       AppVersion NVARCHAR(20) NULL,
       IsActive BIT NOT NULL DEFAULT 1,
       RegisteredAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       LastUsedAt DATETIME2 NULL
   );
   CREATE INDEX IX_DeviceTokens_UserId ON DeviceTokens(UserId);
   ```

5. **Create Push Notification Service**
   - File: `RMMS.Services/Services/Notifications/IPushNotificationService.cs`
   - File: `RMMS.Services/Services/Notifications/PushNotificationService.cs`

   ```csharp
   public class PushNotificationService : IPushNotificationService
   {
       public async Task SendNotificationAsync(string userId, string title, string body, Dictionary<string, string> data = null)
       {
           // Get user's device tokens
           var tokens = await _dbContext.DeviceTokens
               .Where(dt => dt.UserId == userId && dt.IsActive)
               .Select(dt => dt.DeviceToken)
               .ToListAsync();

           if (!tokens.Any()) return;

           // Build notification
           var message = new MulticastMessage
           {
               Notification = new Notification
               {
                   Title = title,
                   Body = body
               },
               Data = data,
               Tokens = tokens
           };

           // Send
           var response = await FirebaseMessaging.DefaultInstance.SendMulticastAsync(message);

           // Handle failures
           if (response.FailureCount > 0)
           {
               // Deactivate invalid tokens
               for (int i = 0; i < response.Responses.Count; i++)
               {
                   if (!response.Responses[i].IsSuccess)
                   {
                       await DeactivateTokenAsync(tokens[i]);
                   }
               }
           }
       }

       public async Task SendNotificationToRoleAsync(string role, string title, string body, Dictionary<string, string> data = null)
       {
           var message = new Message
           {
               Notification = new Notification
               {
                   Title = title,
                   Body = body
               },
               Data = data,
               Topic = $"role_{role}"
           };

           await FirebaseMessaging.DefaultInstance.SendAsync(message);
       }
   }
   ```

6. **Create Notification Templates**
   ```csharp
   public static class NotificationTemplates
   {
       public static PushNotification ProductionBatchCompleted(ProductionBatch batch)
       {
           return new PushNotification
           {
               Title = "Production Batch Completed",
               Body = $"Batch {batch.BatchCode} has been completed",
               Data = new Dictionary<string, string>
               {
                   ["type"] = "production_batch_completed",
                   ["batchId"] = batch.Id.ToString(),
                   ["screen"] = "ProductionDetail"
               }
           };
       }

       public static PushNotification LowStockAlert(Product product, int currentStock)
       {
           return new PushNotification
           {
               Title = "Low Stock Alert",
               Body = $"{product.ProductName} is running low ({currentStock} units)",
               Data = new Dictionary<string, string>
               {
                   ["type"] = "low_stock_alert",
                   ["productId"] = product.Id.ToString(),
                   ["screen"] = "InventoryDetail"
               }
           };
       }

       public static PushNotification NewSalesOrder(SalesOrder order)
       {
           return new PushNotification
           {
               Title = "New Sales Order",
               Body = $"Order {order.OrderCode} received from {order.CustomerName}",
               Data = new Dictionary<string, string>
               {
                   ["type"] = "new_sales_order",
                   ["orderId"] = order.Id.ToString(),
                   ["screen"] = "SalesOrderDetail"
               }
           };
       }
   }
   ```

7. **Integrate Push Notifications into Business Logic**
   ```csharp
   // In ProductionBatchService.CompleteProductionBatch()
   await _pushNotificationService.SendNotificationToRoleAsync(
       "production_manager",
       "Production Batch Completed",
       $"Batch {batch.BatchCode} has been completed"
   );

   // In InventoryLedgerService (when stock low)
   await _pushNotificationService.SendNotificationToRoleAsync(
       "procurement_manager",
       "Low Stock Alert",
       $"{product.ProductName} is below reorder level"
   );

   // In SalesOrderService.CreateSalesOrder()
   await _pushNotificationService.SendNotificationAsync(
       order.CreatedBy,
       "Sales Order Created",
       $"Order {order.OrderCode} has been created"
   );
   ```

8. **Create Notification Settings**
   ```sql
   CREATE TABLE NotificationSettings (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       UserId NVARCHAR(100) NOT NULL UNIQUE,
       EnablePush BIT NOT NULL DEFAULT 1,
       EnableEmail BIT NOT NULL DEFAULT 1,
       EnableSms BIT NOT NULL DEFAULT 0,
       NotificationTypes NVARCHAR(MAX) NULL, -- JSON array
       QuietHoursStart TIME NULL,
       QuietHoursEnd TIME NULL
   );
   ```

**Success Criteria:**
- ✅ Firebase Admin SDK configured
- ✅ Push notification service working
- ✅ Device token registration works
- ✅ Notifications sent on business events
- ✅ Invalid tokens handled gracefully
- ✅ Notification preferences respected

**Testing:**
- Register device token from mobile app
- Trigger business event (e.g., complete production batch)
- Verify push notification received on mobile device
- Test topic-based notifications (role-based)
- Test with invalid token → verify graceful handling

---

## SUCCESS CRITERIA & TESTING

### Overall Phase 4 Success Criteria

**Sprint 4.1: REST API Foundation**
- ✅ All core API controllers created (Customers, Products, Inventory, Production, Sales)
- ✅ JWT authentication working
- ✅ API versioning configured
- ✅ Rate limiting active
- ✅ Health checks operational
- ✅ Error handling consistent
- ✅ All endpoints documented in code

**Sprint 4.2: API Documentation & Security**
- ✅ Swagger UI accessible and complete
- ✅ CORS configured properly
- ✅ API key authentication working
- ✅ OAuth2 integration functional
- ✅ API usage analytics tracking
- ✅ Request throttling working

**Sprint 4.3: Third-Party Integrations**
- ✅ Integration framework created
- ✅ Webhooks sending/receiving
- ✅ Hangfire scheduled jobs running
- ✅ ERP integration working (QuickBooks or SAP)
- ✅ Payment gateway working (Stripe)
- ✅ SMS/Email notifications working

**Sprint 4.4: Mobile & Real-Time**
- ✅ SignalR hubs working
- ✅ Real-time updates functional
- ✅ Mobile API endpoints optimized
- ✅ Push notifications sending
- ✅ Mobile architecture documented

### Comprehensive Testing Plan

#### 1. API Testing (Postman/Insomnia)

**Test Collection: RMMS API v1**

```
📁 Authentication
  ├─ POST Login (valid credentials) ✅
  ├─ POST Login (invalid credentials) ❌
  ├─ POST Refresh Token ✅
  ├─ GET Current User (with token) ✅
  └─ GET Current User (without token) ❌

📁 Customers API
  ├─ GET All Customers (paginated) ✅
  ├─ GET Customer by ID ✅
  ├─ POST Create Customer ✅
  ├─ PUT Update Customer ✅
  ├─ DELETE Customer ✅
  └─ GET Search Customers ✅

📁 Inventory API
  ├─ GET Stock Levels ✅
  ├─ GET Stock by Product ✅
  ├─ GET Stock Movements ✅
  ├─ POST Stock Adjustment ✅
  └─ GET Low Stock Alerts ✅

📁 Production API
  ├─ GET Production Orders ✅
  ├─ POST Create Order ✅
  ├─ GET Batches ✅
  ├─ PUT Update Batch Status ✅
  └─ GET Yield Analysis ✅

📁 Sales API
  ├─ GET Sales Orders ✅
  ├─ POST Create Order ✅
  ├─ GET Quotations ✅
  └─ POST Create Inquiry ✅

📁 Integrations
  ├─ POST Create Webhook ✅
  ├─ POST Test Webhook ✅
  ├─ GET Integration Status ✅
  └─ POST Trigger ERP Sync ✅

📁 Mobile API
  ├─ GET Mobile Dashboard ✅
  ├─ POST Register Device Token ✅
  ├─ GET Notifications ✅
  └─ GET Product by Barcode ✅

📁 Rate Limiting
  ├─ Test 60 requests in 1 minute (expect 429 after 60) ✅
  └─ Test login limit (expect 429 after 5 attempts) ✅
```

#### 2. Load Testing (Apache JMeter or k6)

**Scenario 1: Normal Load**
- 100 concurrent users
- Duration: 10 minutes
- Expected: <200ms response time, 0% errors

**Scenario 2: Peak Load**
- 500 concurrent users
- Duration: 5 minutes
- Expected: <500ms response time, <1% errors

**Scenario 3: Spike Test**
- 0 → 1000 users in 30 seconds
- Expected: Rate limiting kicks in, no crashes

#### 3. Security Testing

**OWASP Top 10 Checks:**
- ✅ SQL Injection (test with malicious input)
- ✅ XSS (test with script tags in input)
- ✅ Authentication bypass attempts
- ✅ JWT token tampering
- ✅ Rate limiting bypass attempts
- ✅ CORS misconfiguration
- ✅ Sensitive data exposure
- ✅ API key leakage

**Tools:**
- OWASP ZAP for automated scanning
- Postman for manual testing

#### 4. Integration Testing

**Webhook Testing:**
- Set up webhook.site endpoint
- Trigger events in RMMS
- Verify webhook received with correct signature

**ERP Integration Testing:**
- Connect to QuickBooks sandbox
- Sync customer data
- Verify data in QuickBooks

**Payment Gateway Testing:**
- Use Stripe test keys
- Create payment with test card (4242 4242 4242 4242)
- Verify payment recorded in RMMS

**Email/SMS Testing:**
- Use Mailtrap for email testing
- Use Twilio test credentials for SMS
- Verify notifications sent

#### 5. Real-Time Testing

**SignalR Testing:**
- Open production dashboard in 2 browsers
- Update production batch in browser 1
- Verify update appears in browser 2 in <1 second

**Push Notification Testing:**
- Register test device
- Trigger notification event
- Verify notification received on device

#### 6. Mobile API Testing

**Performance Testing:**
- Measure response sizes (should be <50KB for list endpoints)
- Measure response times (should be <200ms)
- Test with slow network (3G simulation)

**Pagination Testing:**
- Test cursor-based pagination
- Verify next cursor returned correctly
- Test hasMore flag

---

## RISK MITIGATION

### Identified Risks & Mitigation Strategies

| Risk | Severity | Mitigation |
|------|----------|------------|
| **API breaking changes** | HIGH | Use API versioning; maintain v1 stable |
| **JWT secret compromise** | CRITICAL | Use strong, randomly generated secret; store in Key Vault |
| **Rate limiting bypass** | MEDIUM | Use distributed cache (Redis) for rate limiting in production |
| **Webhook delivery failures** | MEDIUM | Implement retry with exponential backoff; log failures |
| **ERP integration failures** | MEDIUM | Graceful degradation; queue failed syncs for manual review |
| **Payment gateway issues** | HIGH | Implement proper error handling; never lose payment data |
| **Push notification spam** | LOW | Implement notification preferences; respect quiet hours |
| **Database connection pool exhaustion** | MEDIUM | Already mitigated in Phase 3.2 (Min=5, Max=100) |
| **SignalR scaling issues** | LOW | Use Azure SignalR Service or Redis backplane for scale-out |
| **Mobile app authentication issues** | HIGH | Implement biometric fallback; clear error messages |

### Rollback Plan

If any sprint fails or causes issues:

1. **API Issues (Sprint 4.1/4.2)**
   - API versioning allows rolling back to no-API state
   - MVC application continues to work independently
   - Remove API controllers and JWT middleware

2. **Integration Issues (Sprint 4.3)**
   - Integrations are opt-in; can disable individually
   - Webhooks can be disabled per webhook
   - Hangfire jobs can be paused

3. **Mobile Issues (Sprint 4.4)**
   - Mobile APIs optional; web app unaffected
   - SignalR can be disabled
   - Push notifications can be turned off

### Monitoring & Alerting

**Set up alerts for:**
- API error rate >5%
- API response time >1 second (P95)
- Failed webhook deliveries >10%
- ERP sync failures
- Payment processing failures
- Database connection pool >80% utilized
- Hangfire jobs failing
- Push notification delivery failures

**Tools:**
- Serilog for logging (already configured)
- Application Insights or Prometheus for metrics
- PagerDuty/Slack for alerts

---

## DEPLOYMENT GUIDE

### Prerequisites

1. **Environment Variables/Secrets**
   ```
   JWT_SECRET_KEY=<256-bit-random-key>
   STRIPE_API_KEY=<stripe-key>
   STRIPE_WEBHOOK_SECRET=<webhook-secret>
   TWILIO_ACCOUNT_SID=<twilio-sid>
   TWILIO_AUTH_TOKEN=<twilio-token>
   SENDGRID_API_KEY=<sendgrid-key>
   QUICKBOOKS_CLIENT_ID=<qb-client-id>
   QUICKBOOKS_CLIENT_SECRET=<qb-secret>
   FIREBASE_SERVICE_ACCOUNT_JSON=<firebase-json>
   ```

2. **Database Changes**
   - Run all SQL scripts from Sprint 4.3 (Integrations, Webhooks, etc.)
   - Verify Hangfire tables created automatically
   - Create database indexes for new tables

3. **External Service Setup**
   - Create Stripe account → get API keys
   - Create Twilio account → get credentials
   - Create SendGrid account → get API key
   - Set up Firebase project → download service account JSON
   - Connect to QuickBooks/SAP sandbox

### Deployment Steps

#### 1. Development Environment

```bash
# 1. Pull latest code
git pull origin phase4

# 2. Restore packages
dotnet restore

# 3. Update appsettings.Development.json with secrets
# (Use dotnet user-secrets in production)

# 4. Run database migrations
dotnet ef database update

# 5. Run application
dotnet run --project RMMS.Web

# 6. Verify health checks
curl http://localhost:5000/health

# 7. Access Swagger UI
# Open http://localhost:5000/api-docs

# 8. Access Hangfire dashboard
# Open http://localhost:5000/hangfire
```

#### 2. Staging Environment

```bash
# 1. Build for staging
dotnet publish -c Release -o ./publish

# 2. Deploy to staging server
# (Use Azure DevOps, GitHub Actions, or manual copy)

# 3. Update appsettings.Staging.json

# 4. Run database migrations
dotnet ef database update --connection "YourStagingConnectionString"

# 5. Restart application
systemctl restart rmms-api

# 6. Run smoke tests
./scripts/smoke-tests.sh

# 7. Monitor logs
tail -f /var/log/rmms/rmms-.log
```

#### 3. Production Environment

```bash
# 1. Create production database backup
./scripts/backup-database.sh

# 2. Build for production
dotnet publish -c Release -o ./publish

# 3. Deploy to production (blue-green deployment recommended)
# Deploy to "green" slot first

# 4. Update appsettings.Production.json
# Use Azure Key Vault or AWS Secrets Manager for secrets

# 5. Run database migrations
dotnet ef database update --connection "$(ConnectionString)"

# 6. Run integration tests against production
./scripts/integration-tests.sh

# 7. Swap slots (blue-green swap)
# Or update load balancer to point to new version

# 8. Monitor for 30 minutes
# - Check health endpoint every 1 minute
# - Monitor error rates
# - Monitor response times
# - Check Hangfire dashboard

# 9. If issues, rollback
# Swap back to previous version
# Or restore database from backup

# 10. If successful, mark deployment complete
git tag phase4-production-v1.0.0
```

### Post-Deployment Verification

**Checklist:**
- [ ] Health check returns "Healthy"
- [ ] Swagger UI accessible
- [ ] JWT authentication works
- [ ] Test API endpoint with Postman
- [ ] Hangfire dashboard accessible
- [ ] Scheduled jobs running
- [ ] Webhooks delivering
- [ ] ERP sync working
- [ ] Payment test transaction successful
- [ ] SMS/Email test sent
- [ ] Push notification test sent
- [ ] SignalR real-time updates working
- [ ] Mobile API endpoints responding
- [ ] No errors in logs (last 1 hour)
- [ ] Database connection pool healthy

---

## PHASE 4 TASK SUMMARY

### Sprint 4.1: REST API Foundation (8 tasks, 20 hours)
1. ✅ Create API Project Structure (2h)
2. ✅ Implement JWT Authentication (3h)
3. ✅ Create Core API Controllers (4h)
4. ✅ Implement API Versioning (1.5h)
5. ✅ Add API Error Handling & Logging (2h)
6. ✅ Implement Rate Limiting (1.5h)
7. ✅ Create Health Check Endpoints (1h)
8. ✅ Add Request/Response Compression (1h)

### Sprint 4.2: API Documentation & Security (6 tasks, 15 hours)
1. ✅ Implement Swagger/OpenAPI Documentation (3h)
2. ✅ Implement CORS Policy (1.5h)
3. ✅ Add API Key Authentication (2h)
4. ✅ Implement OAuth2/OpenID Connect (3h)
5. ✅ Add API Usage Analytics (2h)
6. ✅ Implement API Request Throttling (1.5h)

### Sprint 4.3: Third-Party Integrations (6 tasks, 15 hours)
1. ✅ Create Integration Framework (2.5h)
2. ✅ Implement Webhook Support (2.5h)
3. ✅ Add Scheduled Job System (Hangfire) (2.5h)
4. ✅ Create ERP/Accounting Integration (2.5h)
5. ✅ Add Payment Gateway Integration (2h)
6. ✅ Implement SMS/Email Gateway Integration (2h)

### Sprint 4.4: Mobile & Real-Time (4 tasks, 10 hours)
1. ✅ Implement SignalR for Real-Time Updates (3h)
2. ✅ Design Mobile App Architecture (2h)
3. ✅ Build Mobile-Specific API Endpoints (3h)
4. ✅ Add Push Notification Service (2h)

**Total: 24 tasks, 60 hours**

---

## NEXT STEPS AFTER PHASE 4

Once Phase 4 is complete, consider:

1. **Phase 5: Advanced Analytics & ML**
   - Predictive analytics for production
   - Demand forecasting
   - Anomaly detection
   - Recommendation engine

2. **Phase 6: IoT Integration**
   - Connect to mill machines via IoT
   - Real-time sensor data
   - Automated production tracking
   - Predictive maintenance

3. **Phase 7: Multi-Tenancy**
   - Support multiple rice mills
   - Tenant isolation
   - Centralized management

4. **Phase 8: Advanced Mobile Features**
   - Offline mode with sync
   - Barcode scanning
   - Voice commands
   - AR for warehouse navigation

---

## CONCLUSION

This comprehensive plan provides a 100% success-oriented roadmap for Phase 4: Integration & Mobile. By following this plan step-by-step:

✅ **You will achieve:**
- Production-ready REST API with JWT authentication
- Complete API documentation via Swagger
- Third-party integrations (ERP, payments, SMS/email)
- Real-time updates via SignalR
- Mobile app architecture ready
- Push notifications working
- Webhooks and scheduled jobs operational

✅ **Success factors:**
- Builds on existing solid foundation (Phase 1-3)
- Reuses existing services (no reinventing the wheel)
- Comprehensive testing at each step
- Clear rollback plans
- Security-first approach
- Mobile-optimized from the start

✅ **Parallel Execution Ready:**
- This plan can be executed in parallel with Phase 3
- No conflicts with Phase 3.3/3.4 work
- Both can be completed simultaneously

🚀 **Ready to implement? Start with Sprint 4.1, Task 4.1.1!**

---

**Document Version:** 1.0
**Last Updated:** 2025-10-13
**Status:** Ready for Implementation
**Estimated Completion:** 60 hours (can be split across multiple developers)

---
