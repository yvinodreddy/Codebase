# PHASE 4: ULTRATHINK EXECUTION PLAN
## 100% Success Rate Strategic Implementation Guide

**Document Version:** 1.0
**Created:** 2025-10-13
**Status:** ✅ Sprint 4.1.1 & 4.1.2 COMPLETE (2/24 tasks)
**Remaining:** 22 tasks, ~55 hours
**Success Guarantee:** Comprehensive step-by-step approach

---

## 📊 CURRENT STATUS SUMMARY

### ✅ COMPLETED (2/24)
- **Sprint 4.1.1**: API Project Structure ✅
  - Created `/Controllers/API/v1/` structure
  - Implemented `BaseApiController` with `ApiResponse<T>`
  - Created `HealthController`
  - JSON serialization configured
  - **TESTED**: `/api/v1/health` working

- **Sprint 4.1.2**: JWT Authentication ✅
  - Packages installed: `Microsoft.AspNetCore.Authentication.JwtBearer` v8.0.0
  - JWT configuration in `appsettings.json`
  - `IJwtService` & `JwtService` implemented
  - `RefreshToken` model created
  - `AuthController` with login/refresh/logout/me endpoints
  - Dual authentication (Cookie + JWT Bearer) in Program.cs
  - **BUILD**: 0 errors, 28 warnings (nullable only)
  - **DATABASE**: RefreshTokens table SQL script ready

---

## 🎯 REMAINING TASKS BREAKDOWN

### SPRINT 4.1: REST API FOUNDATION (6 remaining tasks - 12h)

**Priority:** CRITICAL | **Dependencies:** 4.1.1 & 4.1.2 ✅ Complete

#### **Task 4.1.3: Create Core API Controllers (4h)**

**Objective:** Build REST API controllers for all core business modules

**Files to Create:**
1. `RMMS.Web/Controllers/API/v1/CustomersApiController.cs`
2. `RMMS.Web/Controllers/API/v1/ProductsApiController.cs`
3. `RMMS.Web/Controllers/API/v1/InventoryApiController.cs`
4. `RMMS.Web/Controllers/API/v1/ProductionApiController.cs`
5. `RMMS.Web/Controllers/API/v1/SalesApiController.cs`

**Implementation Steps:**

1. **Customers API Controller** (45 min)
   ```csharp
   [Route("api/v1/[controller]")]
   [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
   public class CustomersApiController : BaseApiController
   {
       private readonly ICustomerService _customerService;

       // GET /api/v1/customers?page=1&pageSize=50&search=keyword
       [HttpGet]
       public async Task<IActionResult> GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 50, [FromQuery] string? search = null)

       // GET /api/v1/customers/{id}
       [HttpGet("{id}")]
       public async Task<IActionResult> GetById(int id)

       // POST /api/v1/customers
       [HttpPost]
       public async Task<IActionResult> Create([FromBody] CustomerRequestDto dto)

       // PUT /api/v1/customers/{id}
       [HttpPut("{id}")]
       public async Task<IActionResult> Update(int id, [FromBody] CustomerRequestDto dto)

       // DELETE /api/v1/customers/{id}
       [HttpDelete("{id}")]
       public async Task<IActionResult> Delete(int id)
   }
   ```

2. **Create DTOs** (30 min)
   - Location: `RMMS.Models/DTOs/API/`
   - Files: `CustomerRequestDto`, `CustomerResponseDto`
   - Pattern: Separate request/response DTOs from domain models
   - Include: Data annotations for validation

3. **Inventory API Controller** (60 min)
   - Endpoints: `/stock`, `/stock/{productId}`, `/movements`, `/adjustments`
   - Special: Real-time stock queries with warehouse filtering
   - Services: Inject `IInventoryLedgerService`, `IStockMovementService`

4. **Production API Controller** (60 min)
   - Endpoints: `/orders`, `/batches`, `/yield/{batchId}`, `/machines`
   - Complex: Batch inputs/outputs with yield calculations
   - Services: `IProductionOrderService`, `IProductionBatchService`, `IYieldAnalysisService`

5. **Sales API Controller** (45 min)
   - Endpoints: `/inquiries`, `/quotations`, `/orders`
   - Workflow: Inquiry → Quotation → Order conversion
   - Services: `IInquiryService`, `IQuotationService`, `ISalesOrderService`

**Testing Checklist:**
- [ ] All endpoints return 200 OK with valid JWT
- [ ] Unauthorized access returns 401
- [ ] Pagination works correctly
- [ ] Filtering and sorting functional
- [ ] DTOs serialize to camelCase JSON
- [ ] Create/Update operations persist to database

**Success Criteria:**
- 5 API controllers created
- 30+ REST endpoints functional
- All CRUD operations working
- JWT authorization enforced
- Swagger-ready XML comments

---

#### **Task 4.1.4: Implement API Versioning (1.5h)**

**Objective:** Support multiple API versions for backward compatibility

**Packages Required:**
```bash
dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning --version 5.1.0
dotnet add RMMS.Web package Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer --version 5.1.0
```

**Implementation Steps:**

1. **Configure Versioning in Program.cs** (30 min)
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

2. **Update Controller Routes** (30 min)
   ```csharp
   [ApiController]
   [ApiVersion("1.0")]
   [Route("api/v{version:apiVersion}/[controller]")]
   public class CustomersApiController : BaseApiController
   ```

3. **Test Version Discovery** (30 min)
   - Access `/api/v1/customers` → works
   - Check response headers for `api-supported-versions`
   - Test header-based versioning: `X-API-Version: 1.0`
   - Test query string: `?api-version=1.0`

**Success Criteria:**
- API versioning configured
- V1 endpoints accessible
- Version reported in response headers
- Multiple version readers supported

---

#### **Task 4.1.5: Add API Error Handling & Logging (2h)**

**Objective:** Centralized exception handling with detailed logging

**Files to Create:**
1. `RMMS.Web/Middleware/ApiExceptionMiddleware.cs`
2. `RMMS.Common/Exceptions/` (custom exceptions)

**Implementation Steps:**

1. **Create Custom API Exceptions** (30 min)
   ```csharp
   // RMMS.Common/Exceptions/ApiException.cs
   public class ApiException : Exception
   {
       public int StatusCode { get; }
       public List<string> Errors { get; }

       public ApiException(int statusCode, string message, List<string>? errors = null)
           : base(message)
       {
           StatusCode = statusCode;
           Errors = errors ?? new List<string>();
       }
   }

   public class NotFoundException : ApiException
   {
       public NotFoundException(string message)
           : base(404, message) { }
   }

   public class BadRequestException : ApiException
   {
       public BadRequestException(string message, List<string>? errors = null)
           : base(400, message, errors) { }
   }

   // UnauthorizedException, ForbiddenException, ConflictException, ValidationException
   ```

2. **Create Exception Middleware** (60 min)
   ```csharp
   public class ApiExceptionMiddleware
   {
       private readonly RequestDelegate _next;
       private readonly ILogger<ApiExceptionMiddleware> _logger;
       private readonly IHostEnvironment _env;

       public async Task InvokeAsync(HttpContext context)
       {
           try
           {
               await _next(context);
           }
           catch (ApiException apiEx)
           {
               await HandleApiExceptionAsync(context, apiEx);
           }
           catch (Exception ex)
           {
               await HandleGenericExceptionAsync(context, ex);
           }
       }

       private async Task HandleApiExceptionAsync(HttpContext context, ApiException exception)
       {
           _logger.LogError(exception, "API Exception: {Message}", exception.Message);

           context.Response.ContentType = "application/json";
           context.Response.StatusCode = exception.StatusCode;

           var response = new ApiResponse<object>
           {
               Success = false,
               Message = exception.Message,
               Errors = exception.Errors,
               Timestamp = DateTime.UtcNow
           };

           await context.Response.WriteAsJsonAsync(response);
       }

       private async Task HandleGenericExceptionAsync(HttpContext context, Exception exception)
       {
           _logger.LogError(exception, "Unhandled exception");

           context.Response.ContentType = "application/json";
           context.Response.StatusCode = 500;

           var response = new ApiResponse<object>
           {
               Success = false,
               Message = "An internal server error occurred",
               Errors = _env.IsDevelopment()
                   ? new List<string> { exception.Message, exception.StackTrace ?? "" }
                   : new List<string>(),
               Timestamp = DateTime.UtcNow
           };

           await context.Response.WriteAsJsonAsync(response);
       }
   }
   ```

3. **Register Middleware in Program.cs** (15 min)
   ```csharp
   // Add BEFORE app.UseRouting()
   app.UseMiddleware<ApiExceptionMiddleware>();
   ```

4. **Enhance Request Logging** (15 min)
   ```csharp
   app.UseSerilogRequestLogging(options =>
   {
       options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
       {
           diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
           diagnosticContext.Set("RequestScheme", httpContext.Request.Scheme);
           diagnosticContext.Set("UserAgent", httpContext.Request.Headers["User-Agent"].ToString());
           diagnosticContext.Set("ClientIP", httpContext.Connection.RemoteIpAddress);
           diagnosticContext.Set("UserId", httpContext.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "Anonymous");
       };
   });
   ```

**Testing:**
- Trigger 404: Access non-existent endpoint
- Trigger 400: Send invalid request body
- Trigger 401: Access protected endpoint without token
- Trigger 500: Force unhandled exception
- Verify logs capture full context

**Success Criteria:**
- All exceptions handled gracefully
- Consistent error response format
- Production hides sensitive details
- Development shows stack traces
- All requests logged with context

---

#### **Task 4.1.6: Implement Rate Limiting (1.5h)**

**Objective:** Protect API from abuse with configurable rate limits

**Package Required:**
```bash
dotnet add RMMS.Web package AspNetCoreRateLimit --version 5.0.0
```

**Implementation Steps:**

1. **Configure Rate Limiting in appsettings.json** (15 min)
   ```json
   "IpRateLimiting": {
       "EnableEndpointRateLimiting": true,
       "StackBlockedRequests": false,
       "RealIpHeader": "X-Real-IP",
       "HttpStatusCode": 429,
       "GeneralRules": [
           {
               "Endpoint": "*",
               "Period": "1m",
               "Limit": 60
           },
           {
               "Endpoint": "POST:/api/v1/auth/login",
               "Period": "1m",
               "Limit": 5
           },
           {
               "Endpoint": "POST:/api/*",
               "Period": "1m",
               "Limit": 30
           }
       ]
   }
   ```

2. **Register Rate Limiting in Program.cs** (45 min)
   ```csharp
   // Add services
   builder.Services.AddMemoryCache();
   builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting"));
   builder.Services.AddSingleton<IIpPolicyStore, MemoryCacheIpPolicyStore>();
   builder.Services.AddSingleton<IRateLimitCounterStore, MemoryCacheRateLimitCounterStore>();
   builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();
   builder.Services.AddSingleton<IProcessingStrategy, AsyncKeyLockProcessingStrategy>();
   builder.Services.AddInMemoryRateLimiting();

   // Add middleware (BEFORE UseRouting)
   app.UseIpRateLimiting();
   ```

3. **Test Rate Limiting** (30 min)
   ```bash
   # Test general rate limit (61 requests in 1 minute)
   for i in {1..65}; do
       curl -s http://localhost:5090/api/v1/health -o /dev/null -w "%{http_code}\n"
   done
   # Expected: First 60 return 200, remaining return 429

   # Test login rate limit (6 attempts in 1 minute)
   for i in {1..7}; do
       curl -s -X POST http://localhost:5090/api/v1/auth/login \
           -H "Content-Type: application/json" \
           -d '{"username":"test","password":"test"}' \
           -w "%{http_code}\n"
   done
   # Expected: First 5 attempts process, 6th returns 429
   ```

**Success Criteria:**
- Rate limiting active for all endpoints
- Login endpoint has stricter limits
- 429 response includes retry-after header
- Rate limits configurable per endpoint
- IP-based rate limiting working

---

#### **Task 4.1.7: Add API Health Checks (1h)**

**Objective:** Comprehensive health monitoring for production

**Packages Required:**
```bash
dotnet add RMMS.Web package AspNetCore.HealthChecks.SqlServer --version 8.0.0
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI --version 8.0.0
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.Client --version 8.0.0
dotnet add RMMS.Web package AspNetCore.HealthChecks.UI.InMemory.Storage --version 8.0.0
```

**Implementation Steps:**

1. **Configure Health Checks in Program.cs** (30 min)
   ```csharp
   builder.Services.AddHealthChecks()
       .AddSqlServer(
           connectionString: builder.Configuration.GetConnectionString("DefaultConnection") ?? "",
           healthQuery: "SELECT 1",
           name: "SQL Server",
           failureStatus: HealthStatus.Unhealthy,
           tags: new[] { "db", "sql", "sqlserver" })
       .AddCheck("API", () => HealthCheckResult.Healthy("API is running"))
       .AddCheck("Memory", () =>
       {
           var allocated = GC.GetTotalMemory(forceFullCollection: false);
           var threshold = 1024L * 1024L * 1024L; // 1 GB
           return allocated < threshold
               ? HealthCheckResult.Healthy($"Memory: {allocated / 1024 / 1024} MB")
               : HealthCheckResult.Degraded($"Memory: {allocated / 1024 / 1024} MB");
       });

   // Health Checks UI
   builder.Services.AddHealthChecksUI(options =>
   {
       options.SetEvaluationTimeInSeconds(30);
       options.MaximumHistoryEntriesPerEndpoint(50);
       options.AddHealthCheckEndpoint("RMMS API", "/health");
   }).AddInMemoryStorage();

   // Map health check endpoints
   app.MapHealthChecks("/health", new HealthCheckOptions
   {
       Predicate = _ => true,
       ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
   });
   app.MapHealthChecks("/health/ready", new HealthCheckOptions
   {
       Predicate = check => check.Tags.Contains("ready")
   });
   app.MapHealthChecks("/health/live", new HealthCheckOptions
   {
       Predicate = _ => true
   });
   app.MapHealthChecksUI(options => options.UIPath = "/health-ui");
   ```

2. **Test Health Endpoints** (20 min)
   - `/health` → JSON with all check results
   - `/health/ready` → Readiness probe
   - `/health/live` → Liveness probe
   - `/health-ui` → Visual dashboard

3. **Document for DevOps** (10 min)
   - K8s readiness probe: `/health/ready`
   - K8s liveness probe: `/health/live`
   - Monitoring dashboard: `/health-ui`

**Success Criteria:**
- Database connectivity checked
- Memory usage monitored
- Health UI accessible
- JSON response format standard
- Ready for container orchestration

---

#### **Task 4.1.8: Verify Request/Response Compression (1h)**

**Objective:** Ensure Phase 3.2 compression works for API endpoints

**Implementation:**

1. **Verify Existing Configuration** (20 min)
   - Check Program.cs for `AddResponseCompression`
   - Confirm Brotli + Gzip configured
   - Verify `UseResponseCompression()` before routing

2. **Add Request Decompression** (20 min)
   ```csharp
   builder.Services.AddRequestDecompression();
   app.UseRequestDecompression();
   ```

3. **Test Compression** (20 min)
   ```bash
   # Test Brotli compression
   curl -H "Accept-Encoding: br" http://localhost:5090/api/v1/customers -I | grep -i "content-encoding"
   # Expected: content-encoding: br

   # Test Gzip compression
   curl -H "Accept-Encoding: gzip" http://localhost:5090/api/v1/customers -I | grep -i "content-encoding"
   # Expected: content-encoding: gzip

   # Measure size reduction
   curl -s http://localhost:5090/api/v1/customers | wc -c  # Uncompressed
   curl -s -H "Accept-Encoding: br" http://localhost:5090/api/v1/customers | wc -c  # Compressed
   # Expected: 60-70% reduction
   ```

**Success Criteria:**
- Response compression active for API
- Brotli preferred over Gzip
- 60-70% size reduction achieved
- Request decompression working
- No performance degradation

---

### SPRINT 4.2: API DOCUMENTATION & SECURITY (6 tasks - 15h)

**Priority:** HIGH | **Dependencies:** Sprint 4.1 complete

#### **Task 4.2.1: Implement Swagger/OpenAPI Documentation (3h)**

**Objective:** Interactive API documentation accessible at `/api-docs`

**Package Required:**
```bash
dotnet add RMMS.Web package Swashbuckle.AspNetCore --version 6.5.0
dotnet add RMMS.Web package Swashbuckle.AspNetCore.Annotations --version 6.5.0
dotnet add RMMS.Web package Swashbuckle.AspNetCore.Filters --version 8.0.0
```

**Implementation Steps:**

1. **Enable XML Documentation** (15 min)
   ```xml
   <!-- RMMS.Web.csproj -->
   <PropertyGroup>
       <GenerateDocumentationFile>true</GenerateDocumentationFile>
       <NoWarn>$(NoWarn);1591</NoWarn>
   </PropertyGroup>
   ```

2. **Configure Swagger in Program.cs** (60 min)
   ```csharp
   builder.Services.AddSwaggerGen(options =>
   {
       options.SwaggerDoc("v1", new OpenApiInfo
       {
           Version = "v1",
           Title = "RMMS API",
           Description = "Rice Mill Management System REST API",
           Contact = new OpenApiContact
           {
               Name = "RMMS Support",
               Email = "support@rmms.com"
           }
       });

       // JWT Authentication in Swagger
       options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
       {
           Description = "JWT Authorization header using Bearer scheme. Enter 'Bearer' [space] and then your token",
           Name = "Authorization",
           In = ParameterLocation.Header,
           Type = SecuritySchemeType.ApiKey,
           Scheme = "Bearer"
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
   });

   // Enable middleware
   if (app.Environment.IsDevelopment() || app.Environment.IsStaging())
   {
       app.UseSwagger();
       app.UseSwaggerUI(options =>
       {
           options.SwaggerEndpoint("/swagger/v1/swagger.json", "RMMS API v1");
           options.RoutePrefix = "api-docs";
       });
   }
   ```

3. **Add XML Comments to Controllers** (60 min)
   ```csharp
   /// <summary>
   /// Gets all customers with pagination and filtering
   /// </summary>
   /// <param name="page">Page number (1-based)</param>
   /// <param name="pageSize">Number of items per page</param>
   /// <param name="search">Search keyword for customer name or code</param>
   /// <returns>Paginated list of customers</returns>
   /// <response code="200">Returns the list of customers</response>
   /// <response code="401">Unauthorized - JWT token missing or invalid</response>
   [HttpGet]
   [ProducesResponseType(typeof(ApiResponse<List<CustomerResponseDto>>), 200)]
   [ProducesResponseType(401)]
   public async Task<IActionResult> GetAll(...)
   ```

4. **Test Swagger UI** (45 min)
   - Access `/api-docs`
   - Test authentication (click Authorize button)
   - Execute test requests for each endpoint
   - Verify request/response schemas
   - Export OpenAPI spec (JSON/YAML)

**Success Criteria:**
- Swagger UI accessible at `/api-docs`
- All endpoints documented
- JWT authentication in UI works
- Request/response examples shown
- Try-it-out functionality works

---

#### **Task 4.2.2: Configure CORS Policy (1.5h)**

**Objective:** Allow cross-origin requests from mobile/web clients

**Implementation Steps:**

1. **Add CORS Configuration to appsettings.json** (15 min)
   ```json
   "CorsSettings": {
       "AllowedOrigins": [
           "http://localhost:3000",
           "http://localhost:8100",
           "https://rmms-mobile.app",
           "https://rmms-web.app"
       ],
       "AllowedMethods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
       "AllowedHeaders": ["*"],
       "AllowCredentials": true,
       "MaxAge": 3600
   }
   ```

2. **Configure CORS in Program.cs** (45 min)
   ```csharp
   var corsSettings = builder.Configuration.GetSection("CorsSettings");
   var allowedOrigins = corsSettings.GetSection("AllowedOrigins").Get<string[]>() ?? Array.Empty<string>();

   builder.Services.AddCors(options =>
   {
       options.AddPolicy("DefaultCorsPolicy", builder =>
       {
           builder.WithOrigins(allowedOrigins)
                  .WithMethods(corsSettings["AllowedMethods"]?.Split(',') ?? Array.Empty<string>())
                  .AllowAnyHeader()
                  .AllowCredentials()
                  .SetPreflightMaxAge(TimeSpan.FromSeconds(corsSettings.GetValue<int>("MaxAge")));
       });
   });

   // Enable CORS (AFTER UseRouting, BEFORE UseAuthorization)
   app.UseCors("DefaultCorsPolicy");
   ```

3. **Test CORS** (30 min)
   ```bash
   # Test preflight request
   curl -X OPTIONS http://localhost:5090/api/v1/customers \
       -H "Origin: http://localhost:3000" \
       -H "Access-Control-Request-Method: GET" \
       -I

   # Expected headers in response:
   # Access-Control-Allow-Origin: http://localhost:3000
   # Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   # Access-Control-Allow-Credentials: true
   ```

**Success Criteria:**
- CORS enabled for configured origins
- Preflight requests handled
- Credentials allowed
- Cross-origin requests work
- Unauthorized origins blocked

---

#### **Task 4.2.3: Implement API Key Authentication (2h)**

**Objective:** Support API key-based auth for server-to-server communication

**Implementation Steps:**

1. **Create ApiKeys Table** (15 min)
   ```sql
   CREATE TABLE ApiKeys (
       Id INT IDENTITY(1,1) PRIMARY KEY,
       KeyName NVARCHAR(100) NOT NULL,
       ApiKey NVARCHAR(500) NOT NULL UNIQUE,
       SecretHash NVARCHAR(500) NOT NULL,
       IsActive BIT NOT NULL DEFAULT 1,
       CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
       ExpiresAt DATETIME2 NULL,
       LastUsedAt DATETIME2 NULL,
       CONSTRAINT UQ_ApiKey UNIQUE (ApiKey)
   );
   CREATE INDEX IX_ApiKeys_ApiKey ON ApiKeys(ApiKey);
   ```

2. **Create API Key Model** (10 min)
   ```csharp
   // RMMS.Models/Authentication/ApiKey.cs
   public class ApiKey
   {
       public int Id { get; set; }
       public string KeyName { get; set; } = string.Empty;
       public string ApiKey { get; set; } = string.Empty;
       public string SecretHash { get; set; } = string.Empty;
       public bool IsActive { get; set; } = true;
       public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
       public DateTime? ExpiresAt { get; set; }
       public DateTime? LastUsedAt { get; set; }
   }
   ```

3. **Implement API Key Authentication Handler** (60 min)
   ```csharp
   // RMMS.Web/Authentication/ApiKeyAuthenticationHandler.cs
   public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
   {
       private const string ApiKeyHeaderName = "X-API-Key";
       private readonly ApplicationDbContext _context;

       protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
       {
           if (!Request.Headers.TryGetValue(ApiKeyHeaderName, out var apiKeyHeaderValues))
           {
               return AuthenticateResult.NoResult();
           }

           var providedApiKey = apiKeyHeaderValues.FirstOrDefault();
           if (string.IsNullOrWhiteSpace(providedApiKey))
           {
               return AuthenticateResult.NoResult();
           }

           var apiKey = await _context.ApiKeys
               .FirstOrDefaultAsync(k => k.ApiKey == providedApiKey && k.IsActive);

           if (apiKey == null)
           {
               return AuthenticateResult.Fail("Invalid API Key");
           }

           if (apiKey.ExpiresAt.HasValue && apiKey.ExpiresAt.Value < DateTime.UtcNow)
           {
               return AuthenticateResult.Fail("API Key expired");
           }

           // Update last used
           apiKey.LastUsedAt = DateTime.UtcNow;
           await _context.SaveChangesAsync();

           var claims = new[]
           {
               new Claim(ClaimTypes.Name, apiKey.KeyName),
               new Claim("ApiKeyId", apiKey.Id.ToString())
           };

           var identity = new ClaimsIdentity(claims, Scheme.Name);
           var principal = new ClaimsPrincipal(identity);
           var ticket = new AuthenticationTicket(principal, Scheme.Name);

           return AuthenticateResult.Success(ticket);
       }
   }
   ```

4. **Register API Key Authentication** (20 min)
   ```csharp
   builder.Services.AddAuthentication()
       .AddScheme<ApiKeyAuthenticationOptions, ApiKeyAuthenticationHandler>("ApiKey", options => { });
   ```

5. **Create API Key Management Endpoint** (15 min)
   ```csharp
   [Route("api/v1/[controller]")]
   [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme, Roles = "Admin")]
   public class ApiKeysController : BaseApiController
   {
       [HttpPost]
       public async Task<IActionResult> GenerateApiKey([FromBody] string keyName)
       {
           var apiKey = Guid.NewGuid().ToString("N");
           var secret = Guid.NewGuid().ToString("N");
           var secretHash = BCrypt.Net.BCrypt.HashPassword(secret);

           // Save to database...

           return Success(new { apiKey, secret, message = "Store secret securely - it won't be shown again" });
       }
   }
   ```

**Testing:**
```bash
# Generate API key (requires admin JWT)
curl -X POST http://localhost:5090/api/v1/apikeys \
    -H "Authorization: Bearer $ADMIN_JWT" \
    -H "Content-Type: application/json" \
    -d '"MyServerApp"'

# Use API key
curl http://localhost:5090/api/v1/customers \
    -H "X-API-Key: generated-api-key-here"
```

**Success Criteria:**
- API key authentication works
- API keys stored securely (hashed)
- Last used timestamp updated
- Expired keys rejected
- API key management endpoints functional

---

#### **Tasks 4.2.4-4.2.6: Quick Reference**

**Task 4.2.4: OAuth2/OpenID Connect (3h)**
- Packages: `Microsoft.AspNetCore.Authentication.Google`, `Microsoft.AspNetCore.Authentication.MicrosoftAccount`
- Providers: Google & Microsoft OAuth
- Flow: OAuth → JWT generation
- Table: `ExternalLogins` (UserId, Provider, ProviderKey)

**Task 4.2.5: API Usage Analytics (2h)**
- Table: `ApiUsageLogs` (Timestamp, UserId, Endpoint, HttpMethod, StatusCode, ResponseTimeMs)
- Middleware: `ApiUsageTrackingMiddleware`
- Dashboard: `AnalyticsController` with usage statistics

**Task 4.2.6: Request Throttling (1.5h)**
- Middleware: `ApiThrottlingMiddleware`
- Limit concurrent requests per endpoint
- Separate from rate limiting (this is concurrency control)

---

### SPRINT 4.3: THIRD-PARTY INTEGRATIONS (6 tasks - 15h)

**Priority:** MEDIUM | **Dependencies:** Sprint 4.1-4.2 complete

**Quick Task Overview:**

**4.3.1: Integration Framework (2.5h)**
- Table: `Integrations`, `IntegrationSyncLogs`
- Interface: `IIntegrationService`
- Base: `BaseIntegrationService` with retry logic

**4.3.2: Webhook Support (2.5h)**
- Tables: `Webhooks`, `WebhookDeliveries`
- Service: `WebhookService` with HMAC signatures
- Background: `WebhookDeliveryService`

**4.3.3: Scheduled Jobs - Hangfire (2.5h)**
- Packages: `Hangfire.AspNetCore`, `Hangfire.SqlServer`
- Dashboard: `/hangfire`
- Jobs: Daily inventory report, low stock alerts, production efficiency, data cleanup

**4.3.4: ERP/Accounting Integration (2.5h)**
- Choose: QuickBooks OR SAP
- Service: `ErpIntegrationService`
- Sync: customers, vendors, products, transactions

**4.3.5: Payment Gateway (2h)**
- Package: `Stripe.net`
- Table: `PaymentTransactions`
- Service: `StripeService`

**4.3.6: SMS/Email Gateway (2h)**
- Packages: `Twilio`, `SendGrid`
- Enhance: `EmailNotificationService`
- Create: `SmsService`

---

### SPRINT 4.4: MOBILE & REAL-TIME (4 tasks - 10h)

**Priority:** MEDIUM | **Dependencies:** Sprint 4.1-4.3 complete

**Task Overview:**

**4.4.1: SignalR Real-Time (3h)**
- Hubs: `ProductionHub`, `DashboardHub`, `NotificationHub`
- Routes: `/hubs/production`, `/hubs/dashboard`, `/hubs/notifications`
- Integration: Broadcast on data changes

**4.4.2: Mobile App Architecture (2h)**
- Document: `MOBILE_APP_ARCHITECTURE.md`
- Choice: React Native (recommended) or Flutter
- Features: Offline support, real-time sync, push notifications

**4.4.3: Mobile API Endpoints (3h)**
- Controllers: `MobileDashboardController`, `MobileProductionController`, etc.
- Optimizations: Cursor pagination, ETag caching, field selection

**4.4.4: Push Notifications (2h)**
- Package: `FirebaseAdmin`
- Table: `DeviceTokens`
- Service: `PushNotificationService`

---

## 🎯 CRITICAL SUCCESS FACTORS

### Dependencies Management
```
4.1.1 → 4.1.2 → 4.1.3 → 4.1.4 → 4.1.5 → 4.1.6 → 4.1.7 → 4.1.8
  ↓
4.2.1 → 4.2.2 → 4.2.3 → 4.2.4 → 4.2.5 → 4.2.6
  ↓
4.3.1 → 4.3.2 → 4.3.3 → 4.3.4 → 4.3.5 → 4.3.6
  ↓
4.4.1 → 4.4.2 → 4.4.3 → 4.4.4
```

### Quality Gates
- **After Sprint 4.1:** All API endpoints tested in Postman
- **After Sprint 4.2:** Swagger docs complete, security verified
- **After Sprint 4.3:** All integrations tested with sandbox accounts
- **After Sprint 4.4:** Mobile endpoints tested, real-time working

### Testing Strategy
1. **Unit Tests:** For services and business logic
2. **Integration Tests:** For API endpoints
3. **Manual Testing:** Use Postman collections
4. **Load Testing:** Use k6 or Apache Bench
5. **Security Testing:** Use OWASP ZAP

---

## 📊 PROGRESS TRACKING

Update `PROGRESS_TRACKER.md` after each task:
```markdown
- Sprint 4.1.3: [completed/in_progress/pending]
```

---

## 🚀 EXECUTION STRATEGY

### Recommended Order
1. **Week 1:** Sprint 4.1 (REST API Foundation)
2. **Week 2:** Sprint 4.2 (Documentation & Security)
3. **Week 3:** Sprint 4.3 (Integrations)
4. **Week 4:** Sprint 4.4 (Mobile & Real-Time)

### Parallel Execution with Phase 3
- Phase 3 (Analytics) and Phase 4 (API) are independent
- Can be executed simultaneously in separate instances
- No conflicts or dependencies

---

## ✅ COMPLETION CHECKLIST

### Sprint 4.1 Complete When:
- [ ] 5 API controllers created
- [ ] 30+ REST endpoints functional
- [ ] API versioning working
- [ ] Error handling consistent
- [ ] Rate limiting active
- [ ] Health checks operational
- [ ] Compression verified

### Sprint 4.2 Complete When:
- [ ] Swagger UI accessible
- [ ] CORS configured
- [ ] API key auth working
- [ ] OAuth integration functional
- [ ] Usage analytics tracking
- [ ] Request throttling active

### Sprint 4.3 Complete When:
- [ ] Integration framework ready
- [ ] Webhooks delivering
- [ ] Hangfire jobs scheduled
- [ ] ERP sync working
- [ ] Payment processing functional
- [ ] SMS/Email sending

### Sprint 4.4 Complete When:
- [ ] SignalR real-time working
- [ ] Mobile architecture documented
- [ ] Mobile endpoints optimized
- [ ] Push notifications sending

---

## 🎉 SUCCESS METRICS

### API Performance
- **Response Time (P95):** < 500ms
- **Throughput:** 1000+ requests/sec
- **Uptime:** 99.9%

### Code Quality
- **Build:** 0 errors
- **Warnings:** < 50
- **Test Coverage:** > 80%

### Documentation
- **Swagger Endpoints:** 60+ documented
- **API Examples:** All endpoints with examples
- **Mobile Guide:** Complete architecture doc

---

**READY TO EXECUTE!** 🚀

Start with Sprint 4.1.3: Create Core API Controllers
