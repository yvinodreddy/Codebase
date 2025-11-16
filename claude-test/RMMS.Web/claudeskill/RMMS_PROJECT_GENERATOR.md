# RMMS Project Generator - Claude Skill
## Comprehensive ASP.NET Core 8 MVC Application Generator

**Purpose**: Generate production-ready ASP.NET Core 8 MVC applications based on proven RMMS.Web patterns and best practices.

**Skill Version**: 1.0
**Last Updated**: 2025-10-23
**Base Project**: RMMS.Web (Rice Mill Management System)

---

## 🎯 SKILL CAPABILITIES

This skill can generate complete, production-ready ASP.NET Core 8 MVC applications with:

### Core Architecture
- ✅ **Clean Architecture** (Models, Services, DataAccess, Web layers)
- ✅ **Repository Pattern** with Generic Repository & Unit of Work
- ✅ **Service Layer** with Business Logic separation
- ✅ **Dependency Injection** throughout the application
- ✅ **Entity Framework Core 8** with SQL Server
- ✅ **Async/Await** patterns everywhere

### Authentication & Security
- ✅ **JWT Authentication** with refresh tokens
- ✅ **Cookie-based Authentication** (ASP.NET Core Identity optional)
- ✅ **Role-Based Authorization** (RBAC)
- ✅ **API Key Authentication** for external integrations
- ✅ **Password Hashing** with BCrypt
- ✅ **CORS Configuration** with flexible policies
- ✅ **Rate Limiting** (AspNetCoreRateLimit)
- ✅ **SSL/TLS** enforcement

### API & Integration
- ✅ **RESTful Web APIs** with versioning (v1, v2, etc.)
- ✅ **Swagger/OpenAPI** documentation
- ✅ **API Versioning** (URL segment, header, query string)
- ✅ **Mobile API Support** with push notifications
- ✅ **SignalR** for real-time updates
- ✅ **Firebase Cloud Messaging** (FCM)
- ✅ **Apple Push Notification Service** (APNS)

### Database & Data Management
- ✅ **SQL Server** with connection pooling
- ✅ **Entity Framework Core** migrations
- ✅ **Stored Procedures** integration with ADO.NET
- ✅ **Data Seeding** patterns
- ✅ **Soft Delete** patterns
- ✅ **Audit Fields** (CreatedBy, CreatedDate, ModifiedBy, ModifiedDate)
- ✅ **Database Health Checks**

### Background Jobs & Scheduling
- ✅ **Hangfire** for background job processing
- ✅ **Recurring Jobs** configuration
- ✅ **Job Dashboard** (/hangfire)

### Reporting & Export
- ✅ **PDF Generation** with QuestPDF
- ✅ **Excel Export** with ClosedXML
- ✅ **Report Service** patterns
- ✅ **Custom Report Templates**

### Logging & Monitoring
- ✅ **Serilog** structured logging
- ✅ **File Logging** with rolling intervals
- ✅ **Console Logging**
- ✅ **Health Checks** UI (/health-ui)
- ✅ **Request/Response Logging** middleware

### Frontend Patterns
- ✅ **Razor Views** with MVC patterns
- ✅ **Bootstrap 5** responsive layouts
- ✅ **jQuery** for client-side interactions
- ✅ **DataTables** for grid functionality
- ✅ **Chart.js** for visualizations
- ✅ **Partial Views** and View Components

### DevOps & Configuration
- ✅ **Multi-Environment Configuration** (Development, Staging, Production)
- ✅ **appsettings.json** best practices
- ✅ **Environment Variables** support
- ✅ **Docker** support (optional)
- ✅ **CI/CD** ready structure

---

## 🚀 HOW TO USE THIS SKILL

### 1. Generate Complete New Project

**Prompt Example**:
```
Using the RMMS Project Generator skill, create a new ASP.NET Core 8 MVC application for:

Domain: Healthcare Data Management
Project Name: HealthcareHub
Database Name: HealthcareHub_DB

Core Entities:
- Patient (Id, FirstName, LastName, DOB, Gender, Phone, Email, Address)
- Doctor (Id, FirstName, LastName, Specialization, Phone, Email, LicenseNumber)
- Appointment (Id, PatientId, DoctorId, AppointmentDate, Status, Notes)
- MedicalRecord (Id, PatientId, DoctorId, Diagnosis, Prescription, RecordDate)

Features Required:
- Patient Management (CRUD)
- Doctor Management (CRUD)
- Appointment Scheduling
- Medical Records Management
- Dashboard with statistics
- JWT Authentication
- Role-based authorization (Admin, Doctor, Nurse, Patient)
- RESTful API with Swagger
- PDF Report generation for medical records
- Real-time appointment notifications (SignalR)

Generate complete project structure, Program.cs, all models, repositories, services, controllers, and basic views.
```

### 2. Add Feature to Existing Project

**Prompt Example**:
```
Using the RMMS Project Generator skill, add an Inventory Management feature to my existing project:

Entities:
- InventoryItem (Id, Name, Category, Quantity, UnitPrice, ReorderLevel)
- StockMovement (Id, ItemId, MovementType, Quantity, MovementDate, Notes)

Requirements:
- CRUD operations for inventory items
- Track stock movements (IN/OUT)
- Low stock alerts
- Stock report generation
- API endpoints for mobile access

Generate: Model classes, Repository, Service, Controller, Views, and API endpoints.
```

### 3. Generate Specific Components

**Prompt Example**:
```
Using the RMMS Project Generator skill:

1. Generate a complete Dashboard Service with:
   - Summary statistics (total records, recent activity)
   - Chart data methods (line, bar, pie charts)
   - Performance optimization with caching
   - Async/await patterns

2. Generate corresponding DashboardController with API endpoints

3. Generate Razor view with Chart.js integration

Domain: Sales Management System
```

### 4. Database Design & Seeding

**Prompt Example**:
```
Using the RMMS Project Generator skill:

Generate complete database setup for an E-commerce platform:

Entities:
- Product, Category, Customer, Order, OrderItem, Payment, Shipping

Requirements:
1. SQL migration scripts
2. Entity Framework Core DbContext
3. Data seeding class with realistic test data
4. Stored procedures for complex queries
5. Database initialization script

Include: Foreign keys, indexes, audit fields, soft delete support.
```

---

## 📋 PROJECT TEMPLATES

### 1. Standard Multi-Layer ASP.NET Core MVC Project

**Structure**:
```
YourProject.sln
├── YourProject.Web (ASP.NET Core MVC)
│   ├── Controllers
│   ├── Views
│   ├── wwwroot
│   ├── Program.cs
│   ├── appsettings.json
│   └── Middleware
├── YourProject.Models (Class Library)
│   ├── Entities
│   ├── ViewModels
│   ├── DTOs
│   └── Enums
├── YourProject.Services (Class Library)
│   ├── Interfaces
│   ├── Implementations
│   └── Helpers
├── YourProject.DataAccess (Class Library)
│   ├── Context
│   ├── Repositories
│   ├── Interfaces
│   └── Migrations
└── YourProject.Common (Class Library)
    ├── Constants
    ├── Utilities
    └── Extensions
```

### 2. API-First Project (Web API + Separate Frontend)

**Structure**:
```
YourProject.sln
├── YourProject.API (ASP.NET Core Web API)
├── YourProject.Models
├── YourProject.Services
├── YourProject.DataAccess
└── YourProject.Common
```

### 3. Microservices-Ready Project

**Structure**:
```
YourProject/
├── Services/
│   ├── YourProject.Identity.API
│   ├── YourProject.Catalog.API
│   ├── YourProject.Orders.API
│   └── YourProject.Notifications.API
├── Shared/
│   ├── YourProject.Common
│   └── YourProject.EventBus
└── Gateway/
    └── YourProject.Gateway
```

---

## 🏗️ CORE PATTERNS & CODE TEMPLATES

### 1. Entity Base Class Template

```csharp
public abstract class BaseEntity
{
    public int Id { get; set; }
    public DateTime CreatedDate { get; set; } = DateTime.UtcNow;
    public DateTime? ModifiedDate { get; set; }
    public string? CreatedBy { get; set; }
    public string? ModifiedBy { get; set; }
    public bool IsDeleted { get; set; } = false;
    public DateTime? DeletedDate { get; set; }
    public string? DeletedBy { get; set; }
}
```

### 2. Generic Repository Pattern

```csharp
public interface IRepository<T> where T : BaseEntity
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> GetActiveAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id); // Soft delete
    Task HardDeleteAsync(int id);
    Task<bool> ExistsAsync(int id);
    Task<int> CountAsync();
}

public class Repository<T> : IRepository<T> where T : BaseEntity
{
    protected readonly ApplicationDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(ApplicationDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(int id)
    {
        return await _dbSet.FirstOrDefaultAsync(e => e.Id == id && !e.IsDeleted);
    }

    public virtual async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _dbSet.Where(e => !e.IsDeleted).ToListAsync();
    }

    public virtual async Task<IEnumerable<T>> GetActiveAsync()
    {
        return await _dbSet.Where(e => !e.IsDeleted).ToListAsync();
    }

    public virtual async Task<T> AddAsync(T entity)
    {
        entity.CreatedDate = DateTime.UtcNow;
        await _dbSet.AddAsync(entity);
        await _context.SaveChangesAsync();
        return entity;
    }

    public virtual async Task UpdateAsync(T entity)
    {
        entity.ModifiedDate = DateTime.UtcNow;
        _context.Entry(entity).State = EntityState.Modified;
        await _context.SaveChangesAsync();
    }

    public virtual async Task DeleteAsync(int id)
    {
        var entity = await GetByIdAsync(id);
        if (entity != null)
        {
            entity.IsDeleted = true;
            entity.DeletedDate = DateTime.UtcNow;
            await UpdateAsync(entity);
        }
    }

    public virtual async Task HardDeleteAsync(int id)
    {
        var entity = await _dbSet.FindAsync(id);
        if (entity != null)
        {
            _dbSet.Remove(entity);
            await _context.SaveChangesAsync();
        }
    }

    public virtual async Task<bool> ExistsAsync(int id)
    {
        return await _dbSet.AnyAsync(e => e.Id == id && !e.IsDeleted);
    }

    public virtual async Task<int> CountAsync()
    {
        return await _dbSet.CountAsync(e => !e.IsDeleted);
    }
}
```

### 3. Service Layer Pattern

```csharp
public interface IEntityService<TEntity, TViewModel> where TEntity : BaseEntity
{
    Task<TViewModel?> GetByIdAsync(int id);
    Task<IEnumerable<TViewModel>> GetAllAsync();
    Task<TViewModel> CreateAsync(TViewModel model);
    Task UpdateAsync(int id, TViewModel model);
    Task DeleteAsync(int id);
}

public abstract class BaseService<TEntity, TViewModel> : IEntityService<TEntity, TViewModel>
    where TEntity : BaseEntity
{
    protected readonly IRepository<TEntity> _repository;
    protected readonly IMapper _mapper; // If using AutoMapper

    protected BaseService(IRepository<TEntity> repository)
    {
        _repository = repository;
    }

    public virtual async Task<TViewModel?> GetByIdAsync(int id)
    {
        var entity = await _repository.GetByIdAsync(id);
        return entity == null ? default : MapToViewModel(entity);
    }

    public virtual async Task<IEnumerable<TViewModel>> GetAllAsync()
    {
        var entities = await _repository.GetAllAsync();
        return entities.Select(MapToViewModel);
    }

    public virtual async Task<TViewModel> CreateAsync(TViewModel model)
    {
        var entity = MapToEntity(model);
        var created = await _repository.AddAsync(entity);
        return MapToViewModel(created);
    }

    public virtual async Task UpdateAsync(int id, TViewModel model)
    {
        var entity = await _repository.GetByIdAsync(id);
        if (entity == null)
            throw new NotFoundException($"Entity with ID {id} not found");

        UpdateEntityFromViewModel(entity, model);
        await _repository.UpdateAsync(entity);
    }

    public virtual async Task DeleteAsync(int id)
    {
        await _repository.DeleteAsync(id);
    }

    protected abstract TViewModel MapToViewModel(TEntity entity);
    protected abstract TEntity MapToEntity(TViewModel model);
    protected abstract void UpdateEntityFromViewModel(TEntity entity, TViewModel model);
}
```

### 4. API Controller Template

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
[Produces("application/json")]
public class BaseApiController<TViewModel> : ControllerBase
{
    protected readonly ILogger _logger;

    public BaseApiController(ILogger logger)
    {
        _logger = logger;
    }

    protected IActionResult Success<T>(T data, string message = "Success")
    {
        return Ok(new ApiResponse<T>
        {
            Success = true,
            Message = message,
            Data = data
        });
    }

    protected IActionResult Created<T>(T data, string message = "Created successfully")
    {
        return StatusCode(201, new ApiResponse<T>
        {
            Success = true,
            Message = message,
            Data = data
        });
    }

    protected IActionResult Error(string message, int statusCode = 400)
    {
        return StatusCode(statusCode, new ApiResponse<object>
        {
            Success = false,
            Message = message,
            Data = null
        });
    }
}

[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
[Authorize]
public class PatientsController : BaseApiController<PatientViewModel>
{
    private readonly IPatientService _patientService;

    public PatientsController(IPatientService patientService, ILogger<PatientsController> logger)
        : base(logger)
    {
        _patientService = patientService;
    }

    [HttpGet]
    [ProducesResponseType(typeof(ApiResponse<IEnumerable<PatientViewModel>>), 200)]
    public async Task<IActionResult> GetAll()
    {
        try
        {
            var patients = await _patientService.GetAllAsync();
            return Success(patients, "Patients retrieved successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving patients");
            return Error("An error occurred while retrieving patients", 500);
        }
    }

    [HttpGet("{id}")]
    [ProducesResponseType(typeof(ApiResponse<PatientViewModel>), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetById(int id)
    {
        try
        {
            var patient = await _patientService.GetByIdAsync(id);
            if (patient == null)
                return NotFound(new ApiResponse<object> { Success = false, Message = "Patient not found" });

            return Success(patient, "Patient retrieved successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving patient {PatientId}", id);
            return Error("An error occurred while retrieving the patient", 500);
        }
    }

    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<PatientViewModel>), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> Create([FromBody] PatientViewModel model)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        try
        {
            var patient = await _patientService.CreateAsync(model);
            return Created(patient, "Patient created successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating patient");
            return Error("An error occurred while creating the patient", 500);
        }
    }

    [HttpPut("{id}")]
    [ProducesResponseType(200)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Update(int id, [FromBody] PatientViewModel model)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        try
        {
            await _patientService.UpdateAsync(id, model);
            return Success<object>(null, "Patient updated successfully");
        }
        catch (NotFoundException)
        {
            return NotFound(new ApiResponse<object> { Success = false, Message = "Patient not found" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating patient {PatientId}", id);
            return Error("An error occurred while updating the patient", 500);
        }
    }

    [HttpDelete("{id}")]
    [ProducesResponseType(200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Delete(int id)
    {
        try
        {
            await _patientService.DeleteAsync(id);
            return Success<object>(null, "Patient deleted successfully");
        }
        catch (NotFoundException)
        {
            return NotFound(new ApiResponse<object> { Success = false, Message = "Patient not found" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting patient {PatientId}", id);
            return Error("An error occurred while deleting the patient", 500);
        }
    }
}

public class ApiResponse<T>
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public T? Data { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}
```

### 5. Program.cs Template (Complete ASP.NET Core 8 Setup)

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Serilog;
using System.Text;
using YourProject.DataAccess.Context;
using YourProject.DataAccess.Repositories;
using YourProject.Services.Implementations;
using YourProject.Services.Interfaces;

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .WriteTo.Console()
    .WriteTo.File("logs/app-.log", rollingInterval: RollingInterval.Day)
    .CreateLogger();

try
{
    Log.Information("Starting application");

    var builder = WebApplication.CreateBuilder(args);

    // Add Serilog
    builder.Host.UseSerilog();

    // Add Controllers with Views
    builder.Services.AddControllersWithViews()
        .AddJsonOptions(options =>
        {
            options.JsonSerializerOptions.ReferenceHandler =
                System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
            options.JsonSerializerOptions.PropertyNamingPolicy =
                System.Text.Json.JsonNamingPolicy.CamelCase;
        });

    // Database Context
    builder.Services.AddDbContext<ApplicationDbContext>(options =>
        options.UseSqlServer(
            builder.Configuration.GetConnectionString("DefaultConnection"),
            b => b.MigrationsAssembly("YourProject.DataAccess")
        ));

    // JWT Authentication
    var jwtSettings = builder.Configuration.GetSection("JwtSettings");
    var secretKey = jwtSettings.GetValue<string>("SecretKey");

    builder.Services.AddAuthentication(options =>
    {
        options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
    })
    .AddJwtBearer(options =>
    {
        options.RequireHttpsMetadata = false;
        options.SaveToken = true;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
            ValidateIssuer = true,
            ValidIssuer = jwtSettings.GetValue<string>("Issuer"),
            ValidateAudience = true,
            ValidAudience = jwtSettings.GetValue<string>("Audience"),
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });

    // API Versioning
    builder.Services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new Asp.Versioning.ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
    })
    .AddApiExplorer(options =>
    {
        options.GroupNameFormat = "'v'VVV";
        options.SubstituteApiVersionInUrl = true;
    });

    // CORS
    builder.Services.AddCors(options =>
    {
        options.AddPolicy("AllowAll", policy =>
        {
            policy.AllowAnyOrigin()
                  .AllowAnyMethod()
                  .AllowAnyHeader();
        });
    });

    // Swagger/OpenAPI
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen(c =>
    {
        c.SwaggerDoc("v1", new OpenApiInfo
        {
            Title = "Your Project API",
            Version = "v1",
            Description = "Your Project API Documentation"
        });

        // JWT Bearer Authentication
        c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
        {
            Description = "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\"",
            Name = "Authorization",
            In = ParameterLocation.Header,
            Type = SecuritySchemeType.ApiKey,
            Scheme = "Bearer"
        });

        c.AddSecurityRequirement(new OpenApiSecurityRequirement
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
    });

    // Health Checks
    builder.Services.AddHealthChecks()
        .AddSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"));

    // Register Repositories
    builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

    // Register Services
    builder.Services.AddScoped<IPatientService, PatientService>();
    builder.Services.AddScoped<IDoctorService, DoctorService>();
    // Add more services...

    // Build the application
    var app = builder.Build();

    // Configure HTTP request pipeline
    if (app.Environment.IsDevelopment())
    {
        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.SwaggerEndpoint("/swagger/v1/swagger.json", "Your Project API v1");
            c.RoutePrefix = "api/docs";
        });
        app.UseDeveloperExceptionPage();
    }
    else
    {
        app.UseExceptionHandler("/Home/Error");
        app.UseHsts();
    }

    app.UseHttpsRedirection();
    app.UseStaticFiles();
    app.UseRouting();

    app.UseCors("AllowAll");

    app.UseAuthentication();
    app.UseAuthorization();

    // Health Check Endpoints
    app.MapHealthChecks("/health");

    // API Routes
    app.MapControllers();

    // MVC Routes
    app.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");

    Log.Information("Application started successfully");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### 6. appsettings.json Template

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=YourProjectDB;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=true"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "AllowedHosts": "*",
  "AppSettings": {
    "ApplicationName": "Your Project Name",
    "Version": "1.0.0",
    "CompanyName": "Your Company"
  },
  "JwtSettings": {
    "SecretKey": "YOUR_SECRET_KEY_MINIMUM_256_BITS_CHANGE_IN_PRODUCTION",
    "Issuer": "YourProject_API",
    "Audience": "YourProject_Clients",
    "TokenExpirationMinutes": 60,
    "RefreshTokenExpirationDays": 7
  },
  "CorsSettings": {
    "AllowedOrigins": [
      "http://localhost:3000",
      "http://localhost:4200",
      "https://yourdomain.com"
    ],
    "AllowedMethods": [ "GET", "POST", "PUT", "DELETE", "OPTIONS" ],
    "AllowedHeaders": [ "*" ],
    "AllowCredentials": true
  },
  "IpRateLimiting": {
    "EnableEndpointRateLimiting": true,
    "GeneralRules": [
      {
        "Endpoint": "*:/api/*",
        "Period": "1m",
        "Limit": 60
      },
      {
        "Endpoint": "POST:/api/v1/Auth/login",
        "Period": "5m",
        "Limit": 5
      }
    ]
  }
}
```

---

## 📊 DASHBOARD PATTERNS

### Dashboard Service Example

```csharp
public interface IDashboardService
{
    Task<DashboardSummaryViewModel> GetSummaryAsync();
    Task<IEnumerable<ChartDataPoint>> GetMonthlyTrendsAsync(int months = 12);
    Task<IEnumerable<CategoryDistribution>> GetCategoryDistributionAsync();
    Task<IEnumerable<RecentActivity>> GetRecentActivitiesAsync(int count = 10);
}

public class DashboardService : IDashboardService
{
    private readonly ApplicationDbContext _context;
    private readonly IMemoryCache _cache;

    public DashboardService(ApplicationDbContext context, IMemoryCache cache)
    {
        _context = context;
        _cache = cache;
    }

    public async Task<DashboardSummaryViewModel> GetSummaryAsync()
    {
        return await _cache.GetOrCreateAsync("dashboard_summary", async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);

            var totalPatients = await _context.Patients.CountAsync(p => !p.IsDeleted);
            var totalDoctors = await _context.Doctors.CountAsync(d => !d.IsDeleted);
            var todayAppointments = await _context.Appointments
                .CountAsync(a => a.AppointmentDate.Date == DateTime.Today && !a.IsDeleted);
            var pendingAppointments = await _context.Appointments
                .CountAsync(a => a.Status == "Pending" && !a.IsDeleted);

            return new DashboardSummaryViewModel
            {
                TotalPatients = totalPatients,
                TotalDoctors = totalDoctors,
                TodayAppointments = todayAppointments,
                PendingAppointments = pendingAppointments,
                LastUpdated = DateTime.UtcNow
            };
        });
    }

    public async Task<IEnumerable<ChartDataPoint>> GetMonthlyTrendsAsync(int months = 12)
    {
        var startDate = DateTime.Today.AddMonths(-months);

        var data = await _context.Appointments
            .Where(a => a.AppointmentDate >= startDate && !a.IsDeleted)
            .GroupBy(a => new { a.AppointmentDate.Year, a.AppointmentDate.Month })
            .Select(g => new ChartDataPoint
            {
                Label = $"{g.Key.Year}-{g.Key.Month:D2}",
                Value = g.Count()
            })
            .OrderBy(d => d.Label)
            .ToListAsync();

        return data;
    }

    public async Task<IEnumerable<CategoryDistribution>> GetCategoryDistributionAsync()
    {
        return await _context.Appointments
            .Where(a => !a.IsDeleted)
            .GroupBy(a => a.Status)
            .Select(g => new CategoryDistribution
            {
                Category = g.Key,
                Count = g.Count(),
                Percentage = (double)g.Count() / _context.Appointments.Count(a => !a.IsDeleted) * 100
            })
            .ToListAsync();
    }

    public async Task<IEnumerable<RecentActivity>> GetRecentActivitiesAsync(int count = 10)
    {
        return await _context.Appointments
            .Where(a => !a.IsDeleted)
            .OrderByDescending(a => a.CreatedDate)
            .Take(count)
            .Select(a => new RecentActivity
            {
                Id = a.Id,
                Description = $"Appointment scheduled for {a.Patient.FirstName} {a.Patient.LastName}",
                Date = a.CreatedDate,
                Type = "Appointment"
            })
            .ToListAsync();
    }
}
```

---

## 🔐 AUTHENTICATION PATTERNS

### JWT Authentication Service

```csharp
public interface IAuthService
{
    Task<AuthResult> LoginAsync(LoginRequest request);
    Task<AuthResult> RefreshTokenAsync(string refreshToken);
    Task<bool> LogoutAsync(string userId);
    Task<bool> RevokeTokenAsync(string token);
}

public class AuthService : IAuthService
{
    private readonly IConfiguration _configuration;
    private readonly IUserRepository _userRepository;
    private readonly IRefreshTokenRepository _refreshTokenRepository;

    public AuthService(
        IConfiguration configuration,
        IUserRepository userRepository,
        IRefreshTokenRepository refreshTokenRepository)
    {
        _configuration = configuration;
        _userRepository = userRepository;
        _refreshTokenRepository = refreshTokenRepository;
    }

    public async Task<AuthResult> LoginAsync(LoginRequest request)
    {
        // Validate user credentials
        var user = await _userRepository.GetByUsernameAsync(request.Username);
        if (user == null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash))
        {
            return new AuthResult
            {
                Success = false,
                Message = "Invalid username or password"
            };
        }

        // Generate JWT token
        var token = GenerateJwtToken(user);
        var refreshToken = GenerateRefreshToken();

        // Save refresh token
        await _refreshTokenRepository.AddAsync(new RefreshToken
        {
            UserId = user.Id,
            Token = refreshToken,
            ExpiryDate = DateTime.UtcNow.AddDays(7),
            CreatedDate = DateTime.UtcNow
        });

        return new AuthResult
        {
            Success = true,
            Token = token,
            RefreshToken = refreshToken,
            ExpiresIn = 3600,
            User = new UserViewModel
            {
                Id = user.Id,
                Username = user.Username,
                Email = user.Email,
                FirstName = user.FirstName,
                LastName = user.LastName,
                Roles = user.Roles.Select(r => r.Name).ToList()
            }
        };
    }

    private string GenerateJwtToken(User user)
    {
        var jwtSettings = _configuration.GetSection("JwtSettings");
        var secretKey = jwtSettings.GetValue<string>("SecretKey");
        var issuer = jwtSettings.GetValue<string>("Issuer");
        var audience = jwtSettings.GetValue<string>("Audience");
        var expirationMinutes = jwtSettings.GetValue<int>("TokenExpirationMinutes");

        var claims = new List<Claim>
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(JwtRegisteredClaimNames.Sub, user.Username),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        // Add role claims
        foreach (var role in user.Roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role.Name));
        }

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(expirationMinutes),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    private string GenerateRefreshToken()
    {
        var randomNumber = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomNumber);
        return Convert.ToBase64String(randomNumber);
    }

    public async Task<AuthResult> RefreshTokenAsync(string refreshToken)
    {
        var token = await _refreshTokenRepository.GetByTokenAsync(refreshToken);

        if (token == null || token.ExpiryDate < DateTime.UtcNow || token.IsRevoked)
        {
            return new AuthResult
            {
                Success = false,
                Message = "Invalid or expired refresh token"
            };
        }

        var user = await _userRepository.GetByIdAsync(token.UserId);
        if (user == null)
        {
            return new AuthResult
            {
                Success = false,
                Message = "User not found"
            };
        }

        // Generate new tokens
        var newToken = GenerateJwtToken(user);
        var newRefreshToken = GenerateRefreshToken();

        // Revoke old refresh token
        token.IsRevoked = true;
        await _refreshTokenRepository.UpdateAsync(token);

        // Save new refresh token
        await _refreshTokenRepository.AddAsync(new RefreshToken
        {
            UserId = user.Id,
            Token = newRefreshToken,
            ExpiryDate = DateTime.UtcNow.AddDays(7),
            CreatedDate = DateTime.UtcNow
        });

        return new AuthResult
        {
            Success = true,
            Token = newToken,
            RefreshToken = newRefreshToken,
            ExpiresIn = 3600
        };
    }

    public async Task<bool> LogoutAsync(string userId)
    {
        await _refreshTokenRepository.RevokeAllUserTokensAsync(userId);
        return true;
    }

    public async Task<bool> RevokeTokenAsync(string token)
    {
        return await _refreshTokenRepository.RevokeTokenAsync(token);
    }
}
```

---

## 📄 REPORT GENERATION PATTERNS

### PDF Report Service (QuestPDF)

```csharp
public interface IReportService
{
    Task<byte[]> GeneratePatientReportAsync(int patientId);
    Task<byte[]> GenerateMedicalRecordReportAsync(int recordId);
    Task<byte[]> GenerateMonthlyStatisticsReportAsync(int year, int month);
}

public class ReportService : IReportService
{
    private readonly IPatientRepository _patientRepository;
    private readonly IMedicalRecordRepository _medicalRecordRepository;

    public ReportService(
        IPatientRepository patientRepository,
        IMedicalRecordRepository medicalRecordRepository)
    {
        _patientRepository = patientRepository;
        _medicalRecordRepository = medicalRecordRepository;
    }

    public async Task<byte[]> GeneratePatientReportAsync(int patientId)
    {
        var patient = await _patientRepository.GetByIdWithDetailsAsync(patientId);
        if (patient == null)
            throw new NotFoundException("Patient not found");

        var document = Document.Create(container =>
        {
            container.Page(page =>
            {
                page.Size(PageSizes.A4);
                page.Margin(50);

                page.Header().Column(column =>
                {
                    column.Item().Text("Patient Report")
                        .FontSize(20)
                        .Bold()
                        .AlignCenter();

                    column.Item().Text($"Generated: {DateTime.Now:dd/MM/yyyy HH:mm}")
                        .FontSize(10)
                        .AlignCenter();
                });

                page.Content().Column(column =>
                {
                    column.Spacing(20);

                    // Patient Information
                    column.Item().Text("Patient Information").FontSize(16).Bold();
                    column.Item().Row(row =>
                    {
                        row.RelativeItem().Text($"Name: {patient.FirstName} {patient.LastName}");
                        row.RelativeItem().Text($"DOB: {patient.DateOfBirth:dd/MM/yyyy}");
                    });
                    column.Item().Row(row =>
                    {
                        row.RelativeItem().Text($"Gender: {patient.Gender}");
                        row.RelativeItem().Text($"Phone: {patient.Phone}");
                    });
                    column.Item().Text($"Email: {patient.Email}");
                    column.Item().Text($"Address: {patient.Address}");

                    column.Item().LineHorizontal(1);

                    // Medical Records
                    column.Item().Text("Medical History").FontSize(16).Bold();
                    foreach (var record in patient.MedicalRecords.OrderByDescending(r => r.RecordDate))
                    {
                        column.Item().Column(recordColumn =>
                        {
                            recordColumn.Item().Text($"Date: {record.RecordDate:dd/MM/yyyy}").Bold();
                            recordColumn.Item().Text($"Doctor: {record.Doctor.FirstName} {record.Doctor.LastName}");
                            recordColumn.Item().Text($"Diagnosis: {record.Diagnosis}");
                            recordColumn.Item().Text($"Prescription: {record.Prescription}");
                            recordColumn.Item().PaddingBottom(10);
                        });
                    }
                });

                page.Footer().AlignCenter().Text(text =>
                {
                    text.Span("Page ");
                    text.CurrentPageNumber();
                    text.Span(" of ");
                    text.TotalPages();
                });
            });
        });

        return document.GeneratePdf();
    }
}
```

### Excel Export Service (ClosedXML)

```csharp
public interface IExcelExportService
{
    Task<byte[]> ExportPatientsToExcelAsync();
    Task<byte[]> ExportAppointmentsToExcelAsync(DateTime startDate, DateTime endDate);
}

public class ExcelExportService : IExcelExportService
{
    private readonly IPatientRepository _patientRepository;
    private readonly IAppointmentRepository _appointmentRepository;

    public ExcelExportService(
        IPatientRepository patientRepository,
        IAppointmentRepository appointmentRepository)
    {
        _patientRepository = patientRepository;
        _appointmentRepository = appointmentRepository;
    }

    public async Task<byte[]> ExportPatientsToExcelAsync()
    {
        var patients = await _patientRepository.GetAllWithDetailsAsync();

        using var workbook = new XLWorkbook();
        var worksheet = workbook.Worksheets.Add("Patients");

        // Header
        worksheet.Cell(1, 1).Value = "ID";
        worksheet.Cell(1, 2).Value = "First Name";
        worksheet.Cell(1, 3).Value = "Last Name";
        worksheet.Cell(1, 4).Value = "Date of Birth";
        worksheet.Cell(1, 5).Value = "Gender";
        worksheet.Cell(1, 6).Value = "Phone";
        worksheet.Cell(1, 7).Value = "Email";
        worksheet.Cell(1, 8).Value = "Address";

        // Style header
        var headerRange = worksheet.Range(1, 1, 1, 8);
        headerRange.Style.Font.Bold = true;
        headerRange.Style.Fill.BackgroundColor = XLColor.LightBlue;

        // Data
        int row = 2;
        foreach (var patient in patients)
        {
            worksheet.Cell(row, 1).Value = patient.Id;
            worksheet.Cell(row, 2).Value = patient.FirstName;
            worksheet.Cell(row, 3).Value = patient.LastName;
            worksheet.Cell(row, 4).Value = patient.DateOfBirth;
            worksheet.Cell(row, 5).Value = patient.Gender;
            worksheet.Cell(row, 6).Value = patient.Phone;
            worksheet.Cell(row, 7).Value = patient.Email;
            worksheet.Cell(row, 8).Value = patient.Address;
            row++;
        }

        // Auto-fit columns
        worksheet.Columns().AdjustToContents();

        // Convert to byte array
        using var stream = new MemoryStream();
        workbook.SaveAs(stream);
        return stream.ToArray();
    }
}
```

---

## 🧪 TESTING PATTERNS

### Unit Test Template (xUnit)

```csharp
public class PatientServiceTests
{
    private readonly Mock<IPatientRepository> _mockRepo;
    private readonly PatientService _service;

    public PatientServiceTests()
    {
        _mockRepo = new Mock<IPatientRepository>();
        _service = new PatientService(_mockRepo.Object);
    }

    [Fact]
    public async Task GetByIdAsync_ValidId_ReturnsPatient()
    {
        // Arrange
        var patientId = 1;
        var expectedPatient = new Patient
        {
            Id = patientId,
            FirstName = "John",
            LastName = "Doe",
            Email = "john.doe@example.com"
        };

        _mockRepo.Setup(r => r.GetByIdAsync(patientId))
            .ReturnsAsync(expectedPatient);

        // Act
        var result = await _service.GetByIdAsync(patientId);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(patientId, result.Id);
        Assert.Equal("John", result.FirstName);
        _mockRepo.Verify(r => r.GetByIdAsync(patientId), Times.Once);
    }

    [Fact]
    public async Task CreateAsync_ValidData_CreatesPatient()
    {
        // Arrange
        var createModel = new PatientCreateViewModel
        {
            FirstName = "Jane",
            LastName = "Smith",
            Email = "jane.smith@example.com",
            DateOfBirth = new DateTime(1990, 1, 1)
        };

        _mockRepo.Setup(r => r.AddAsync(It.IsAny<Patient>()))
            .ReturnsAsync((Patient p) => p);

        // Act
        var result = await _service.CreateAsync(createModel);

        // Assert
        Assert.NotNull(result);
        Assert.Equal("Jane", result.FirstName);
        _mockRepo.Verify(r => r.AddAsync(It.IsAny<Patient>()), Times.Once);
    }

    [Fact]
    public async Task DeleteAsync_ExistingPatient_DeletesSuccessfully()
    {
        // Arrange
        var patientId = 1;
        _mockRepo.Setup(r => r.DeleteAsync(patientId))
            .Returns(Task.CompletedTask);

        // Act
        await _service.DeleteAsync(patientId);

        // Assert
        _mockRepo.Verify(r => r.DeleteAsync(patientId), Times.Once);
    }
}
```

---

## 🚀 DEPLOYMENT PATTERNS

### Docker Support (Dockerfile)

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj files and restore dependencies
COPY ["YourProject.Web/YourProject.Web.csproj", "YourProject.Web/"]
COPY ["YourProject.Models/YourProject.Models.csproj", "YourProject.Models/"]
COPY ["YourProject.Services/YourProject.Services.csproj", "YourProject.Services/"]
COPY ["YourProject.DataAccess/YourProject.DataAccess.csproj", "YourProject.DataAccess/"]
COPY ["YourProject.Common/YourProject.Common.csproj", "YourProject.Common/"]
RUN dotnet restore "YourProject.Web/YourProject.Web.csproj"

# Copy everything else and build
COPY . .
WORKDIR "/src/YourProject.Web"
RUN dotnet build "YourProject.Web.csproj" -c Release -o /app/build

# Publish stage
FROM build AS publish
RUN dotnet publish "YourProject.Web.csproj" -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 80
EXPOSE 443

COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "YourProject.Web.dll"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: YourProject.Web/Dockerfile
    ports:
      - "5000:80"
      - "5001:443"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__DefaultConnection=Server=db;Database=YourProjectDB;User=sa;Password=Your_password123;TrustServerCertificate=True
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=Your_password123
      - MSSQL_PID=Developer
    ports:
      - "1433:1433"
    volumes:
      - sqldata:/var/opt/mssql
    networks:
      - app-network

volumes:
  sqldata:

networks:
  app-network:
    driver: bridge
```

---

## 🎓 BEST PRACTICES & CONVENTIONS

### 1. Naming Conventions

**C# Classes & Methods**:
- PascalCase for classes, methods, properties: `PatientService`, `GetByIdAsync()`
- camelCase for parameters, local variables: `patientId`, `userName`
- Async methods should end with `Async`: `GetAllAsync()`, `SaveAsync()`

**Database**:
- PascalCase for table names: `Patients`, `Appointments`
- PascalCase for column names: `FirstName`, `CreatedDate`
- Avoid abbreviations: Use `Identification` not `Id` (except primary keys)

**API Endpoints**:
- Plural nouns: `/api/v1/patients`, `/api/v1/appointments`
- Kebab-case for multi-word: `/api/v1/medical-records`
- RESTful verbs: GET, POST, PUT, DELETE, PATCH

### 2. Error Handling

**Always use try-catch in controllers**:
```csharp
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
    try
    {
        var result = await _service.GetByIdAsync(id);
        if (result == null)
            return NotFound();
        return Ok(result);
    }
    catch (NotFoundException ex)
    {
        _logger.LogWarning(ex, "Patient not found: {PatientId}", id);
        return NotFound(new { message = ex.Message });
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error retrieving patient: {PatientId}", id);
        return StatusCode(500, new { message = "An error occurred" });
    }
}
```

**Custom Exceptions**:
```csharp
public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message) { }
}

public class ValidationException : Exception
{
    public ValidationException(string message) : base(message) { }
}

public class UnauthorizedException : Exception
{
    public UnauthorizedException(string message) : base(message) { }
}
```

### 3. Logging Best Practices

**Use structured logging**:
```csharp
_logger.LogInformation("Patient {PatientId} retrieved by user {UserId}",
    patientId, userId);

_logger.LogError(exception, "Error processing payment {PaymentId} for order {OrderId}",
    paymentId, orderId);

_logger.LogWarning("Rate limit exceeded for IP {IpAddress}", ipAddress);
```

### 4. Performance Optimization

**Use async/await everywhere**:
```csharp
// ✅ Good
public async Task<IEnumerable<Patient>> GetAllAsync()
{
    return await _context.Patients.ToListAsync();
}

// ❌ Bad
public IEnumerable<Patient> GetAll()
{
    return _context.Patients.ToList();
}
```

**Use projection to avoid over-fetching**:
```csharp
// ✅ Good - only select needed fields
var patients = await _context.Patients
    .Where(p => !p.IsDeleted)
    .Select(p => new PatientListViewModel
    {
        Id = p.Id,
        FullName = p.FirstName + " " + p.LastName,
        Email = p.Email
    })
    .ToListAsync();

// ❌ Bad - fetches all fields
var patients = await _context.Patients
    .Where(p => !p.IsDeleted)
    .ToListAsync();
```

**Use caching for frequently accessed data**:
```csharp
public async Task<DashboardSummary> GetSummaryAsync()
{
    return await _cache.GetOrCreateAsync("dashboard_summary", async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
        return await CalculateSummaryAsync();
    });
}
```

### 5. Security Best Practices

**Never store plain text passwords**:
```csharp
// Hash password before saving
var hashedPassword = BCrypt.Net.BCrypt.HashPassword(plainTextPassword);
user.PasswordHash = hashedPassword;

// Verify password
var isValid = BCrypt.Net.BCrypt.Verify(plainTextPassword, user.PasswordHash);
```

**Use parameterized queries (EF Core does this automatically)**:
```csharp
// ✅ Good - EF Core parameterizes automatically
var patients = await _context.Patients
    .Where(p => p.LastName == lastName)
    .ToListAsync();

// ❌ Bad - SQL injection risk
var sql = $"SELECT * FROM Patients WHERE LastName = '{lastName}'";
```

**Sanitize user input**:
```csharp
[Required]
[StringLength(100, MinimumLength = 2)]
[RegularExpression(@"^[a-zA-Z\s]+$", ErrorMessage = "Only letters allowed")]
public string FirstName { get; set; }

[Required]
[EmailAddress]
public string Email { get; set; }
```

---

## 📚 COMMON SCENARIOS & SOLUTIONS

### Scenario 1: Many-to-Many Relationship

**Problem**: Products and Categories (many-to-many)

**Solution**:
```csharp
public class Product : BaseEntity
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public ICollection<ProductCategory> ProductCategories { get; set; }
}

public class Category : BaseEntity
{
    public string Name { get; set; }
    public ICollection<ProductCategory> ProductCategories { get; set; }
}

public class ProductCategory
{
    public int ProductId { get; set; }
    public Product Product { get; set; }

    public int CategoryId { get; set; }
    public Category Category { get; set; }
}

// In DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<ProductCategory>()
        .HasKey(pc => new { pc.ProductId, pc.CategoryId });

    modelBuilder.Entity<ProductCategory>()
        .HasOne(pc => pc.Product)
        .WithMany(p => p.ProductCategories)
        .HasForeignKey(pc => pc.ProductId);

    modelBuilder.Entity<ProductCategory>()
        .HasOne(pc => pc.Category)
        .WithMany(c => c.ProductCategories)
        .HasForeignKey(pc => pc.CategoryId);
}
```

### Scenario 2: File Upload & Storage

**Solution**:
```csharp
[HttpPost("upload")]
public async Task<IActionResult> UploadFile(IFormFile file)
{
    if (file == null || file.Length == 0)
        return BadRequest("No file uploaded");

    // Validate file type
    var allowedExtensions = new[] { ".pdf", ".jpg", ".png", ".docx" };
    var extension = Path.GetExtension(file.FileName).ToLowerInvariant();

    if (!allowedExtensions.Contains(extension))
        return BadRequest("Invalid file type");

    // Validate file size (10MB limit)
    if (file.Length > 10 * 1024 * 1024)
        return BadRequest("File too large (max 10MB)");

    // Generate unique filename
    var fileName = $"{Guid.NewGuid()}{extension}";
    var uploadPath = Path.Combine(_env.WebRootPath, "uploads");
    Directory.CreateDirectory(uploadPath);
    var filePath = Path.Combine(uploadPath, fileName);

    // Save file
    using (var stream = new FileStream(filePath, FileMode.Create))
    {
        await file.CopyToAsync(stream);
    }

    // Save to database
    var document = new Document
    {
        FileName = file.FileName,
        StoredFileName = fileName,
        FilePath = $"/uploads/{fileName}",
        FileSize = file.Length,
        ContentType = file.ContentType,
        UploadedBy = User.Identity.Name,
        UploadedDate = DateTime.UtcNow
    };

    await _documentRepository.AddAsync(document);

    return Ok(new {
        message = "File uploaded successfully",
        fileUrl = document.FilePath
    });
}
```

### Scenario 3: Pagination & Sorting

**Solution**:
```csharp
public class PaginatedResult<T>
{
    public IEnumerable<T> Items { get; set; }
    public int TotalCount { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPrevious => PageNumber > 1;
    public bool HasNext => PageNumber < TotalPages;
}

[HttpGet]
public async Task<IActionResult> GetAll(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    [FromQuery] string sortBy = "Id",
    [FromQuery] string sortOrder = "asc",
    [FromQuery] string search = "")
{
    var query = _context.Patients.Where(p => !p.IsDeleted);

    // Search
    if (!string.IsNullOrWhiteSpace(search))
    {
        query = query.Where(p =>
            p.FirstName.Contains(search) ||
            p.LastName.Contains(search) ||
            p.Email.Contains(search));
    }

    // Total count
    var totalCount = await query.CountAsync();

    // Sorting
    query = sortBy.ToLower() switch
    {
        "firstname" => sortOrder.ToLower() == "desc"
            ? query.OrderByDescending(p => p.FirstName)
            : query.OrderBy(p => p.FirstName),
        "lastname" => sortOrder.ToLower() == "desc"
            ? query.OrderByDescending(p => p.LastName)
            : query.OrderBy(p => p.LastName),
        "email" => sortOrder.ToLower() == "desc"
            ? query.OrderByDescending(p => p.Email)
            : query.OrderBy(p => p.Email),
        _ => sortOrder.ToLower() == "desc"
            ? query.OrderByDescending(p => p.Id)
            : query.OrderBy(p => p.Id)
    };

    // Pagination
    var items = await query
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(p => new PatientViewModel
        {
            Id = p.Id,
            FirstName = p.FirstName,
            LastName = p.LastName,
            Email = p.Email
        })
        .ToListAsync();

    var result = new PaginatedResult<PatientViewModel>
    {
        Items = items,
        TotalCount = totalCount,
        PageNumber = page,
        PageSize = pageSize
    };

    return Ok(result);
}
```

---

## 🎯 SKILL INVOCATION EXAMPLES

### Example 1: Create Healthcare Management System

**User Prompt**:
```
Create a complete healthcare management application using the RMMS Project Generator skill.

Project: MediCare System
Database: MediCare_DB

Core Modules:
1. Patient Management
2. Doctor Management
3. Appointment Scheduling
4. Medical Records
5. Prescription Management
6. Billing & Invoicing

Technical Requirements:
- ASP.NET Core 8 MVC
- SQL Server
- JWT Authentication
- RESTful API with Swagger
- PDF Reports
- Real-time notifications (SignalR)
- Mobile API support
- Dashboard with charts

Generate complete project structure.
```

**Claude Response**:
I'll generate the complete MediCare System using the RMMS Project Generator patterns...

[Generates complete project with all layers, models, services, repositories, controllers, views, API endpoints, authentication, etc.]

### Example 2: Add Feature to Existing Project

**User Prompt**:
```
Add a Laboratory Management module to my existing hospital system using RMMS patterns.

New Entities:
- LabTest (Id, TestName, Category, Price, Duration)
- LabOrder (Id, PatientId, DoctorId, Tests, OrderDate, Status)
- LabResult (Id, OrderId, TestId, Result, TechnicianId, ResultDate)

Features:
- Order lab tests
- Track test status
- Record results
- Generate lab reports (PDF)
- Dashboard with pending tests

Generate: Models, Repository, Service, Controller, API, Views
```

**Claude Response**:
I'll add the Laboratory Management module following RMMS patterns...

[Generates all components with repository pattern, service layer, API controllers, views, PDF report generation, etc.]

---

## 🚨 TROUBLESHOOTING GUIDE

### Issue 1: Database Connection Fails

**Symptoms**: "A network-related or instance-specific error"

**Solutions**:
1. Check connection string in appsettings.json
2. Verify SQL Server is running
3. Add `TrustServerCertificate=True` to connection string
4. Check firewall settings
5. Verify SQL Server authentication mode

### Issue 2: JWT Token Not Working

**Symptoms**: 401 Unauthorized

**Solutions**:
1. Verify secret key is at least 256 bits (32 characters)
2. Check token expiration
3. Verify Issuer and Audience match
4. Ensure [Authorize] attribute is present
5. Check if token is being sent in Authorization header

### Issue 3: CORS Errors

**Symptoms**: "Access-Control-Allow-Origin" error

**Solutions**:
1. Add CORS policy in Program.cs
2. Call `app.UseCors()` before `app.UseAuthorization()`
3. Verify allowed origins in appsettings.json
4. Use `AllowAnyOrigin()` for development only

### Issue 4: EF Core Migration Fails

**Symptoms**: "No migrations configuration type was found"

**Solutions**:
1. Ensure migrations assembly is specified in AddDbContext
2. Run from Web project directory
3. Verify connection string
4. Check if DbContext is registered in DI container
5. Use: `dotnet ef migrations add InitialCreate --project YourProject.DataAccess`

---

## 📖 DOCUMENTATION TEMPLATES

### README.md Template

```markdown
# Project Name

Brief description of your project.

## Prerequisites

- .NET 8 SDK
- SQL Server 2019+
- Visual Studio 2022 or VS Code

## Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2. Database Setup

```bash
# Update connection string in appsettings.json
# Run migrations
dotnet ef database update --project YourProject.DataAccess
```

### 3. Run Application

```bash
cd YourProject.Web
dotnet run
```

Navigate to: https://localhost:5001

### 4. API Documentation

Swagger UI: https://localhost:5001/api/docs

## Default Credentials

- **Admin**: admin@example.com / Admin@123
- **User**: user@example.com / User@123

## Project Structure

```
YourProject/
├── YourProject.Web       # ASP.NET Core MVC application
├── YourProject.Models    # Entity models, ViewModels, DTOs
├── YourProject.Services  # Business logic layer
├── YourProject.DataAccess # Database context, repositories
└── YourProject.Common    # Shared utilities, constants
```

## Features

- ✅ User Authentication & Authorization
- ✅ RESTful API with Swagger
- ✅ Entity Management (CRUD)
- ✅ Dashboard & Analytics
- ✅ PDF Report Generation
- ✅ Excel Export
- ✅ Real-time Notifications

## Technologies

- ASP.NET Core 8 MVC
- Entity Framework Core 8
- SQL Server
- JWT Authentication
- Swagger/OpenAPI
- Serilog
- QuestPDF
- ClosedXML

## License

MIT License
```

---

## 🎓 LEARNING RESOURCES

### Key Patterns Used

1. **Repository Pattern**: Abstracts data access logic
2. **Service Layer Pattern**: Encapsulates business logic
3. **Dependency Injection**: Loose coupling, testability
4. **Async/Await**: Non-blocking operations
5. **DTO Pattern**: Data transfer between layers
6. **Unit of Work**: Manages transactions

### Recommended Reading

- ASP.NET Core Documentation: https://docs.microsoft.com/aspnet/core
- Entity Framework Core: https://docs.microsoft.com/ef/core
- C# Best Practices: https://docs.microsoft.com/dotnet/csharp
- RESTful API Design: https://restfulapi.net

---

## 📝 SKILL METADATA

**Skill Name**: RMMS Project Generator
**Version**: 1.0
**Base Project**: RMMS.Web (Rice Mill Management System)
**Target Framework**: .NET 8
**Language**: C# 11
**Database**: SQL Server
**Architecture**: Clean Architecture / N-Tier
**Patterns**: Repository, Service Layer, DI, Async/Await

**Capabilities**:
- ✅ Full-stack ASP.NET Core 8 MVC applications
- ✅ RESTful Web APIs with versioning
- ✅ Authentication & Authorization (JWT, Cookies)
- ✅ Database design & Entity Framework Core
- ✅ Report generation (PDF, Excel)
- ✅ Real-time features (SignalR)
- ✅ Background jobs (Hangfire)
- ✅ Mobile API support
- ✅ Complete deployment setup

---

## 🎉 READY TO USE!

This skill is production-ready and based on battle-tested patterns from the RMMS.Web project.

**To use this skill, simply prompt Claude Code with**:

```
"Using the RMMS Project Generator skill, create a [domain] application with [features]..."
```

Claude will generate complete, production-ready code following all the patterns and best practices documented here.

**Happy Coding!** 🚀

---

*End of RMMS Project Generator Skill Documentation*
