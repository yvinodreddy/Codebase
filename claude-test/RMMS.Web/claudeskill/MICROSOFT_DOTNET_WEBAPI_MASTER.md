# Microsoft .NET Web API Master - Production-Ready Claude Skill
## Comprehensive ASP.NET Core 8 Web API + MVC Application Generator

**Purpose**: Generate enterprise-grade, production-ready ASP.NET Core 8 applications with Web APIs, MVC, complete JavaScript ecosystem, and advanced integrations.

**Skill Version**: 2.0 (Ultra-Comprehensive)
**Last Updated**: 2025-10-23
**Base Projects**: RMMS.Web + FHIRHealthcareAPI
**Target Framework**: .NET 8.0 LTS

---

## 🎯 SKILL CAPABILITIES (COMPLETE STACK)

This skill generates production-ready applications with **EVERYTHING**:

### 🏗️ Backend Technologies (.NET 8)
- ✅ **ASP.NET Core 8 MVC** (Server-side rendering with Razor)
- ✅ **ASP.NET Core 8 Web API** (RESTful APIs)
- ✅ **Entity Framework Core 8** (ORM with SQL Server)
- ✅ **Clean Architecture** (Models, Services, DataAccess, Web)
- ✅ **Repository Pattern** with Unit of Work
- ✅ **Service Layer** with Business Logic
- ✅ **Dependency Injection** throughout

### 🔐 Authentication & Security
- ✅ **JWT Authentication** (with refresh tokens)
- ✅ **Cookie-Based Authentication** (ASP.NET Core Identity)
- ✅ **Role-Based Authorization** (RBAC)
- ✅ **API Key Authentication** (for external integrations)
- ✅ **OAuth2/OpenID Connect** support
- ✅ **BCrypt Password Hashing**
- ✅ **Rate Limiting** (AspNetCoreRateLimit)
- ✅ **CORS Configuration**
- ✅ **Security Headers** middleware

### 🌐 Frontend Technologies (Complete JavaScript Ecosystem)

**Core Libraries:**
- ✅ **Bootstrap 5.3** (responsive framework)
- ✅ **jQuery 3.7** (DOM manipulation)
- ✅ **jQuery Validation** (client-side validation)
- ✅ **jQuery Unobtrusive Validation**

**UI Components & Enhancement:**
- ✅ **DataTables** (advanced grids with sorting, filtering, export)
- ✅ **SweetAlert2** (professional alerts & confirmations)
- ✅ **Toastr** (toast notifications)
- ✅ **Select2** (advanced dropdowns with search)
- ✅ **AOS** (Animate On Scroll - smooth animations)
- ✅ **FullCalendar** (scheduling & calendar views)
- ✅ **Dropzone** (drag-drop file upload)
- ✅ **Chart.js** (data visualization)
- ✅ **D3.js** (advanced visualizations - optional)

**Icons & Fonts:**
- ✅ **Font Awesome 6.4** (icon library)
- ✅ **Bootstrap Icons 1.11**
- ✅ **Google Fonts** (Nunito Sans, etc.)

**PDF & Export:**
- ✅ **jsPDF** (client-side PDF generation)
- ✅ **html2canvas** (HTML to canvas conversion)
- ✅ **DataTables Buttons** (Excel, PDF, CSV export)
- ✅ **QuestPDF** (server-side C# PDF generation)
- ✅ **ClosedXML** (Excel generation)

### 📡 Real-Time & Communication
- ✅ **SignalR** (WebSocket real-time updates)
- ✅ **Server-Sent Events** (SSE)
- ✅ **WebSockets** (bidirectional communication)
- ✅ **Push Notifications** (Firebase FCM, APNS)

### 🗄️ Database & Data Access
- ✅ **SQL Server** (primary database)
- ✅ **Entity Framework Core** (Code-First & Database-First)
- ✅ **ADO.NET** (for stored procedures)
- ✅ **Dapper** (micro-ORM for performance)
- ✅ **Redis** (distributed caching)
- ✅ **Elasticsearch** (full-text search - optional)

### 🔄 Background Jobs & Scheduling
- ✅ **Hangfire** (background job processing)
- ✅ **Recurring Jobs** (cron-based scheduling)
- ✅ **Fire-and-Forget** jobs
- ✅ **Delayed** jobs
- ✅ **Dashboard** (/hangfire)

### 📊 Monitoring & Logging
- ✅ **Serilog** (structured logging)
- ✅ **File Logging** (rolling intervals)
- ✅ **Console Logging**
- ✅ **Health Checks** (ASP.NET Core Health Checks)
- ✅ **Health Checks UI** (/health-ui)
- ✅ **Custom Metrics** (Prometheus-ready - optional)

### 🚀 Advanced Integrations
- ✅ **GraphQL** (HotChocolate)
- ✅ **gRPC** (high-performance RPC)
- ✅ **RabbitMQ** (message queue)
- ✅ **Elasticsearch** (NEST client)
- ✅ **Polly** (resilience & retry policies)
- ✅ **RestSharp** (HTTP client)
- ✅ **Refit** (type-safe HTTP client)

### 📱 Mobile & API Support
- ✅ **RESTful API** design
- ✅ **API Versioning** (URL, header, query string)
- ✅ **Swagger/OpenAPI** documentation
- ✅ **API Rate Limiting**
- ✅ **API Analytics**
- ✅ **Webhook Management**
- ✅ **Mobile-First** responsive design

### 🧪 Testing & Quality
- ✅ **xUnit** (unit testing framework)
- ✅ **Moq** (mocking framework)
- ✅ **FluentAssertions** (assertion library)
- ✅ **Integration Tests**
- ✅ **API Tests** (Postman collections)

### 🐳 DevOps & Deployment
- ✅ **Docker** support
- ✅ **Docker Compose** (multi-container)
- ✅ **Kubernetes** manifests (optional)
- ✅ **Azure App Service** ready
- ✅ **IIS** deployment
- ✅ **GitHub Actions** CI/CD
- ✅ **Azure DevOps** Pipelines

---

## 📋 COMPLETE JAVASCRIPT LIBRARY MANIFEST

### Core Libraries (Foundation)

```html
<!-- jQuery 3.7.0 -->
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>

<!-- Bootstrap 5.3.0 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- jQuery Validation -->
<script src="~/lib/jquery-validation/dist/jquery.validate.min.js"></script>
<script src="~/lib/jquery-validation-unobtrusive/jquery.validate.unobtrusive.min.js"></script>
```

### Icon Libraries

```html
<!-- Font Awesome 6.4.0 -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" />

<!-- Bootstrap Icons 1.11.0 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet" />
```

### Data Tables & Grids

```html
<!-- DataTables with Bootstrap 5 integration -->
<link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet" />
<link href="https://cdn.datatables.net/responsive/2.5.0/css/responsive.bootstrap5.min.css" rel="stylesheet" />
<link href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.bootstrap5.min.css" rel="stylesheet" />

<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
<script src="https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js"></script>
<script src="https://cdn.datatables.net/responsive/2.5.0/js/responsive.bootstrap5.min.js"></script>

<!-- DataTables Buttons (Export functionality) -->
<script src="https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.bootstrap5.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.print.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.colVis.min.js"></script>
```

### UI Enhancements

```html
<!-- SweetAlert2 (Professional Alerts) -->
<link href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.0/dist/sweetalert2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.0/dist/sweetalert2.all.min.js"></script>

<!-- Toastr (Toast Notifications) -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>

<!-- Select2 (Advanced Dropdowns) -->
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

<!-- AOS (Animate On Scroll) -->
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet" />
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
```

### Specialized Components

```html
<!-- FullCalendar (Scheduling) -->
<link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.10/index.global.min.css' rel='stylesheet' />
<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.10/index.global.min.js'></script>

<!-- Dropzone (File Upload) -->
<link rel="stylesheet" href="https://unpkg.com/dropzone@5/dist/min/dropzone.min.css" type="text/css" />
<script src="https://unpkg.com/dropzone@5/dist/min/dropzone.min.js"></script>

<!-- Chart.js (Data Visualization) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>

<!-- jsPDF & html2canvas (PDF Generation) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

### Fonts

```html
<!-- Google Fonts - Nunito Sans (Professional) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
```

---

## 🏗️ COMPLETE PROJECT STRUCTURE

```
YourProject.sln
├── YourProject.Web (ASP.NET Core MVC + Web API)
│   ├── Controllers/
│   │   ├── Web/ (MVC Controllers)
│   │   │   ├── HomeController.cs
│   │   │   ├── AccountController.cs
│   │   │   ├── DashboardController.cs
│   │   │   └── [EntityName]Controller.cs
│   │   └── API/ (API Controllers)
│   │       ├── v1/
│   │       │   ├── AuthController.cs
│   │       │   ├── [EntityName]ApiController.cs
│   │       │   └── HealthController.cs
│   │       └── v2/ (Future versions)
│   ├── Views/
│   │   ├── Shared/
│   │   │   ├── _Layout.cshtml
│   │   │   ├── _LoginPartial.cshtml
│   │   │   └── Error.cshtml
│   │   ├── Home/
│   │   │   ├── Index.cshtml
│   │   │   └── Privacy.cshtml
│   │   └── [EntityName]/
│   │       ├── Index.cshtml
│   │       ├── Create.cshtml
│   │       ├── Edit.cshtml
│   │       ├── Details.cshtml
│   │       └── Delete.cshtml
│   ├── wwwroot/
│   │   ├── css/
│   │   │   ├── site.css
│   │   │   ├── microsoft-fluent.css
│   │   │   ├── responsive.css
│   │   │   └── custom.css
│   │   ├── js/
│   │   │   ├── site.js
│   │   │   ├── site-enhanced.js
│   │   │   ├── app-pro.js
│   │   │   └── modules/ (feature-specific JS)
│   │   ├── lib/ (local libraries)
│   │   │   ├── jquery/
│   │   │   ├── bootstrap/
│   │   │   └── jquery-validation/
│   │   ├── images/
│   │   └── uploads/ (user-uploaded files)
│   ├── Middleware/
│   │   ├── AuditMiddleware.cs
│   │   ├── ErrorHandlingMiddleware.cs
│   │   ├── RateLimitMiddleware.cs
│   │   └── SecurityHeadersMiddleware.cs
│   ├── Hubs/ (SignalR)
│   │   ├── NotificationHub.cs
│   │   ├── ChatHub.cs
│   │   └── MonitoringHub.cs
│   ├── HealthChecks/
│   │   ├── DatabaseHealthCheck.cs
│   │   ├── RedisHealthCheck.cs
│   │   └── ExternalApiHealthCheck.cs
│   ├── ViewModels/
│   │   ├── [EntityName]ViewModel.cs
│   │   └── DashboardViewModel.cs
│   ├── Program.cs
│   ├── appsettings.json
│   ├── appsettings.Development.json
│   ├── appsettings.Production.json
│   └── YourProject.Web.csproj
│
├── YourProject.Models (Class Library .NET 8)
│   ├── Entities/
│   │   ├── BaseEntity.cs
│   │   ├── [EntityName].cs
│   │   ├── User.cs
│   │   ├── Role.cs
│   │   └── AuditLog.cs
│   ├── ViewModels/
│   │   └── API/
│   │       ├── ApiResponse.cs
│   │       ├── PaginatedResult.cs
│   │       └── [EntityName]Dto.cs
│   ├── Enums/
│   │   └── [EnumName].cs
│   ├── Constants/
│   │   └── AppConstants.cs
│   └── YourProject.Models.csproj
│
├── YourProject.Services (Class Library .NET 8)
│   ├── Interfaces/
│   │   ├── IEntityService.cs
│   │   ├── I[EntityName]Service.cs
│   │   ├── IAuthService.cs
│   │   ├── IEmailService.cs
│   │   └── ICacheService.cs
│   ├── Implementations/
│   │   ├── BaseService.cs
│   │   ├── [EntityName]Service.cs
│   │   ├── AuthService.cs
│   │   ├── EmailService.cs
│   │   └── CacheService.cs
│   ├── Helpers/
│   │   ├── PasswordHasher.cs
│   │   ├── JwtTokenGenerator.cs
│   │   └── EmailTemplates.cs
│   ├── Validators/
│   │   └── [EntityName]Validator.cs
│   ├── BackgroundJobs/ (Hangfire)
│   │   ├── DataCleanupJob.cs
│   │   ├── EmailSenderJob.cs
│   │   └── ReportGenerationJob.cs
│   └── YourProject.Services.csproj
│
├── YourProject.DataAccess (Class Library .NET 8)
│   ├── Context/
│   │   └── ApplicationDbContext.cs
│   ├── Repositories/
│   │   ├── Interfaces/
│   │   │   ├── IRepository.cs
│   │   │   ├── IUnitOfWork.cs
│   │   │   └── I[EntityName]Repository.cs
│   │   └── Implementations/
│   │       ├── Repository.cs
│   │       ├── UnitOfWork.cs
│   │       └── [EntityName]Repository.cs
│   ├── Migrations/
│   │   └── (EF Core migrations)
│   ├── Seeding/
│   │   └── DataSeeder.cs
│   └── YourProject.DataAccess.csproj
│
├── YourProject.Common (Class Library .NET 8)
│   ├── Extensions/
│   │   ├── StringExtensions.cs
│   │   ├── DateTimeExtensions.cs
│   │   └── IEnumerableExtensions.cs
│   ├── Utilities/
│   │   ├── FileHelper.cs
│   │   ├── CryptoHelper.cs
│   │   └── ValidationHelper.cs
│   ├── Exceptions/
│   │   ├── NotFoundException.cs
│   │   ├── ValidationException.cs
│   │   └── UnauthorizedException.cs
│   └── YourProject.Common.csproj
│
├── YourProject.Tests (xUnit Test Project)
│   ├── Unit/
│   │   ├── Services/
│   │   └── Repositories/
│   ├── Integration/
│   │   ├── Controllers/
│   │   └── API/
│   └── YourProject.Tests.csproj
│
├── Infrastructure/ (DevOps & Deployment)
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── .dockerignore
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── scripts/
│   │   ├── deploy.sh
│   │   ├── backup.sh
│   │   └── seed-data.sh
│   └── ci-cd/
│       ├── azure-pipelines.yml
│       └── github-actions.yml
│
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── API.md
    └── DEPLOYMENT.md
```

---

## 🔧 COMPREHENSIVE .CSPROJ CONFIGURATION

### YourProject.Web.csproj (Complete)

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <NoWarn>NU1701</NoWarn>
  </PropertyGroup>

  <ItemGroup>
    <!-- ===================================================================
         CORE ASP.NET CORE PACKAGES
         =================================================================== -->
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.SignalR" Version="1.1.0" />
    <PackageReference Include="Microsoft.Data.SqlClient" Version="6.1.1" />

    <!-- ===================================================================
         ENTITY FRAMEWORK CORE
         =================================================================== -->
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>

    <!-- ===================================================================
         API FEATURES
         =================================================================== -->
    <PackageReference Include="Asp.Versioning.Mvc" Version="8.1.0" />
    <PackageReference Include="Asp.Versioning.Mvc.ApiExplorer" Version="8.1.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Swashbuckle.AspNetCore.Annotations" Version="6.5.0" />

    <!-- ===================================================================
         HEALTH CHECKS
         =================================================================== -->
    <PackageReference Include="AspNetCore.HealthChecks.SqlServer" Version="8.0.0" />
    <PackageReference Include="AspNetCore.HealthChecks.UI" Version="8.0.0" />
    <PackageReference Include="AspNetCore.HealthChecks.UI.Client" Version="8.0.0" />
    <PackageReference Include="AspNetCore.HealthChecks.UI.InMemory.Storage" Version="8.0.0" />

    <!-- ===================================================================
         SECURITY & AUTHENTICATION
         =================================================================== -->
    <PackageReference Include="AspNetCoreRateLimit" Version="5.0.0" />
    <PackageReference Include="BCrypt.Net-Next" Version="4.0.3" />
    <PackageReference Include="System.IdentityModel.Tokens.Jwt" Version="8.0.0" />

    <!-- ===================================================================
         BACKGROUND JOBS
         =================================================================== -->
    <PackageReference Include="Hangfire.AspNetCore" Version="1.8.17" />
    <PackageReference Include="Hangfire.Core" Version="1.8.17" />
    <PackageReference Include="Hangfire.SqlServer" Version="1.8.17" />

    <!-- ===================================================================
         LOGGING
         =================================================================== -->
    <PackageReference Include="Serilog.AspNetCore" Version="9.0.0" />
    <PackageReference Include="Serilog.Sinks.Console" Version="6.0.0" />
    <PackageReference Include="Serilog.Sinks.File" Version="7.0.0" />

    <!-- ===================================================================
         PDF & EXCEL GENERATION
         =================================================================== -->
    <PackageReference Include="QuestPDF" Version="2024.10.3" />
    <PackageReference Include="ClosedXML" Version="0.105.0" />

    <!-- ===================================================================
         CACHING & REDIS
         =================================================================== -->
    <PackageReference Include="Microsoft.Extensions.Caching.StackExchangeRedis" Version="8.0.0" />

    <!-- ===================================================================
         RESILIENCE & HTTP
         =================================================================== -->
    <PackageReference Include="Microsoft.Extensions.Http.Polly" Version="8.0.0" />
    <PackageReference Include="RestSharp" Version="110.2.0" />
    <PackageReference Include="Refit" Version="7.0.0" />

    <!-- ===================================================================
         MOBILE & PUSH NOTIFICATIONS
         =================================================================== -->
    <PackageReference Include="FirebaseAdmin" Version="3.0.0" />
    <PackageReference Include="Twilio" Version="7.0.0" />

    <!-- ===================================================================
         GRAPHQL (OPTIONAL)
         =================================================================== -->
    <PackageReference Include="HotChocolate.AspNetCore" Version="15.1.10" />

    <!-- ===================================================================
         ELASTICSEARCH (OPTIONAL)
         =================================================================== -->
    <PackageReference Include="NEST" Version="7.17.5" />

    <!-- ===================================================================
         MESSAGE QUEUE (OPTIONAL)
         =================================================================== -->
    <PackageReference Include="RabbitMQ.Client" Version="7.1.2" />

    <!-- ===================================================================
         ENVIRONMENT VARIABLES
         =================================================================== -->
    <PackageReference Include="DotNetEnv" Version="2.5.0" />

    <!-- ===================================================================
         FHIR/HEALTHCARE (IF APPLICABLE)
         =================================================================== -->
    <!-- <PackageReference Include="Hl7.Fhir.R4" Version="5.12.2" /> -->
    <!-- <PackageReference Include="Hl7.Fhir.Specification.Data.R4" Version="5.12.2" /> -->

    <!-- ===================================================================
         MACHINE LEARNING (OPTIONAL)
         =================================================================== -->
    <!-- <PackageReference Include="Microsoft.ML" Version="4.0.2" /> -->
    <!-- <PackageReference Include="Microsoft.ML.TimeSeries" Version="4.0.2" /> -->
    <!-- <PackageReference Include="Microsoft.ML.FastTree" Version="4.0.2" /> -->
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\YourProject.Common\YourProject.Common.csproj" />
    <ProjectReference Include="..\YourProject.Models\YourProject.Models.csproj" />
    <ProjectReference Include="..\YourProject.Services\YourProject.Services.csproj" />
    <ProjectReference Include="..\YourProject.DataAccess\YourProject.DataAccess.csproj" />
  </ItemGroup>
</Project>
```

---

## 📄 COMPLETE PROGRAM.CS TEMPLATE (PRODUCTION-READY)

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Serilog;
using Serilog.Events;
using System.Text;
using YourProject.DataAccess.Context;
using YourProject.DataAccess.Repositories;
using YourProject.Services.Implementations;
using YourProject.Services.Interfaces;
using Hangfire;
using Hangfire.SqlServer;
using AspNetCoreRateLimit;
using YourProject.Web.Middleware;
using YourProject.Web.Hubs;
using HealthChecks.UI.Client;
using Microsoft.AspNetCore.Http.Json;

// ============================================================
// SERILOG CONFIGURATION
// ============================================================
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .WriteTo.File("logs/app-.log",
        rollingInterval: RollingInterval.Day,
        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj}{NewLine}{Exception}")
    .CreateLogger();

try
{
    Log.Information("Starting YourProject application");

    var builder = WebApplication.CreateBuilder(args);

    // Load environment variables (.env file support)
    DotNetEnv.Env.Load();

    // ============================================================
    // CONFIGURATION
    // ============================================================
    builder.Configuration
        .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
        .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .AddEnvironmentVariables(prefix: "YOURPROJECT_");

    // Add Serilog
    builder.Host.UseSerilog();

    // ============================================================
    // SERVICES CONFIGURATION
    // ============================================================

    // MVC Controllers with Views
    builder.Services.AddControllersWithViews(options =>
    {
        // Add custom model binders if needed
        // options.ModelBinderProviders.Insert(0, new CustomModelBinderProvider());
    })
    .AddJsonOptions(options =>
    {
        // JSON serialization for API endpoints
        options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull;
        options.JsonSerializerOptions.WriteIndented = builder.Environment.IsDevelopment();
    });

    // ============================================================
    // DATABASE CONTEXT
    // ============================================================
    builder.Services.AddDbContext<ApplicationDbContext>(options =>
        options.UseSqlServer(
            builder.Configuration.GetConnectionString("DefaultConnection"),
            sqlOptions =>
            {
                sqlOptions.EnableRetryOnFailure(
                    maxRetryCount: 5,
                    maxRetryDelay: TimeSpan.FromSeconds(30),
                    errorNumbersToAdd: null);
                sqlOptions.CommandTimeout(180);
                sqlOptions.MigrationsAssembly("YourProject.DataAccess");
            }
        ));

    // ============================================================
    // API VERSIONING
    // ============================================================
    builder.Services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new Asp.Versioning.ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
        options.ApiVersionReader = Asp.Versioning.ApiVersionReader.Combine(
            new Asp.Versioning.UrlSegmentApiVersionReader(),
            new Asp.Versioning.HeaderApiVersionReader("X-Api-Version"),
            new Asp.Versioning.QueryStringApiVersionReader("api-version")
        );
    })
    .AddApiExplorer(options =>
    {
        options.GroupNameFormat = "'v'VVV";
        options.SubstituteApiVersionInUrl = true;
    });

    // ============================================================
    // CORS CONFIGURATION
    // ============================================================
    builder.Services.AddCors(options =>
    {
        options.AddPolicy("DefaultCorsPolicy", corsBuilder =>
        {
            var corsSettings = builder.Configuration.GetSection("CorsSettings");
            var allowedOrigins = corsSettings.GetSection("AllowedOrigins").Get<string[]>() ?? new[] { "*" };
            var allowedMethods = corsSettings.GetSection("AllowedMethods").Get<string[]>() ?? new[] { "GET", "POST", "PUT", "DELETE", "OPTIONS" };
            var allowedHeaders = corsSettings.GetSection("AllowedHeaders").Get<string[]>() ?? new[] { "*" };
            var allowCredentials = corsSettings.GetValue<bool>("AllowCredentials");

            if (allowedOrigins.Contains("*"))
                corsBuilder.AllowAnyOrigin();
            else
                corsBuilder.WithOrigins(allowedOrigins);

            if (allowedMethods.Contains("*"))
                corsBuilder.AllowAnyMethod();
            else
                corsBuilder.WithMethods(allowedMethods);

            if (allowedHeaders.Contains("*"))
                corsBuilder.AllowAnyHeader();
            else
                corsBuilder.WithHeaders(allowedHeaders);

            if (allowCredentials && !allowedOrigins.Contains("*"))
                corsBuilder.AllowCredentials();
        });
    });

    // ============================================================
    // JWT AUTHENTICATION
    // ============================================================
    var jwtSettings = builder.Configuration.GetSection("JwtSettings");
    var secretKey = Encoding.UTF8.GetBytes(jwtSettings["SecretKey"]!);

    builder.Services.AddAuthentication(options =>
    {
        options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
    })
    .AddJwtBearer(options =>
    {
        options.RequireHttpsMetadata = false; // Set to true in production
        options.SaveToken = true;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(secretKey),
            ValidateIssuer = true,
            ValidIssuer = jwtSettings["Issuer"],
            ValidateAudience = true,
            ValidAudience = jwtSettings["Audience"],
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };

        // SignalR support
        options.Events = new JwtBearerEvents
        {
            OnMessageReceived = context =>
            {
                var accessToken = context.Request.Query["access_token"];
                var path = context.HttpContext.Request.Path;
                if (!string.IsNullOrEmpty(accessToken) && path.StartsWithSegments("/hubs"))
                {
                    context.Token = accessToken;
                }
                return Task.CompletedTask;
            }
        };
    });

    // ============================================================
    // SWAGGER/OPENAPI
    // ============================================================
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen(c =>
    {
        c.SwaggerDoc("v1", new OpenApiInfo
        {
            Title = "YourProject API",
            Version = "v1",
            Description = "Production-Ready ASP.NET Core 8 Web API",
            Contact = new OpenApiContact
            {
                Name = "Your Name",
                Email = "your.email@example.com"
            }
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

        // XML Comments (optional)
        // var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
        // var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
        // c.IncludeXmlComments(xmlPath);
    });

    // ============================================================
    // RATE LIMITING
    // ============================================================
    builder.Services.AddMemoryCache();
    builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting"));
    builder.Services.Configure<IpRateLimitPolicies>(builder.Configuration.GetSection("IpRateLimitPolicies"));
    builder.Services.AddInMemoryRateLimiting();
    builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();

    // ============================================================
    // CACHING (REDIS)
    // ============================================================
    var redisConnection = builder.Configuration.GetConnectionString("RedisCache");
    if (!string.IsNullOrEmpty(redisConnection))
    {
        builder.Services.AddStackExchangeRedisCache(options =>
        {
            options.Configuration = redisConnection;
            options.InstanceName = "YourProject_";
        });
    }
    else
    {
        builder.Services.AddDistributedMemoryCache();
    }

    // ============================================================
    // HANGFIRE (BACKGROUND JOBS)
    // ============================================================
    builder.Services.AddHangfire(configuration => configuration
        .SetDataCompatibilityLevel(CompatibilityLevel.Version_180)
        .UseSimpleAssemblyNameTypeSerializer()
        .UseRecommendedSerializerSettings()
        .UseSqlServerStorage(builder.Configuration.GetConnectionString("DefaultConnection"), new SqlServerStorageOptions
        {
            CommandBatchMaxTimeout = TimeSpan.FromMinutes(5),
            SlidingInvisibilityTimeout = TimeSpan.FromMinutes(5),
            QueuePollInterval = TimeSpan.Zero,
            UseRecommendedIsolationLevel = true,
            DisableGlobalLocks = true
        }));

    builder.Services.AddHangfireServer();

    // ============================================================
    // SIGNALR
    // ============================================================
    builder.Services.AddSignalR(options =>
    {
        options.EnableDetailedErrors = builder.Environment.IsDevelopment();
        options.KeepAliveInterval = TimeSpan.FromSeconds(15);
        options.ClientTimeoutInterval = TimeSpan.FromSeconds(30);
    });

    // ============================================================
    // HEALTH CHECKS
    // ============================================================
    builder.Services.AddHealthChecks()
        .AddSqlServer(
            connectionString: builder.Configuration.GetConnectionString("DefaultConnection")!,
            name: "sql-server",
            tags: new[] { "db", "sql", "sqlserver" })
        .AddCheck<CustomHealthCheck>("custom-check");

    builder.Services.AddHealthChecksUI(options =>
    {
        options.SetEvaluationTimeInSeconds(60);
        options.MaximumHistoryEntriesPerEndpoint(50);
        options.AddHealthCheckEndpoint("API Health", "/health");
    }).AddInMemoryStorage();

    // ============================================================
    // DEPENDENCY INJECTION - REPOSITORIES
    // ============================================================
    builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
    builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
    // Add specific repositories
    // builder.Services.AddScoped<ICustomerRepository, CustomerRepository>();

    // ============================================================
    // DEPENDENCY INJECTION - SERVICES
    // ============================================================
    builder.Services.AddScoped<IAuthService, AuthService>();
    builder.Services.AddScoped<ICacheService, CacheService>();
    builder.Services.AddScoped<IEmailService, EmailService>();
    // Add specific services
    // builder.Services.AddScoped<ICustomerService, CustomerService>();

    // ============================================================
    // HTTP CLIENTS WITH POLLY (RESILIENCE)
    // ============================================================
    builder.Services.AddHttpClient("ExternalApi")
        .AddPolicyHandler(GetRetryPolicy())
        .AddPolicyHandler(GetCircuitBreakerPolicy());

    // ============================================================
    // BUILD APPLICATION
    // ============================================================
    var app = builder.Build();

    // ============================================================
    // MIDDLEWARE PIPELINE
    // ============================================================

    // Error Handling
    if (app.Environment.IsDevelopment())
    {
        app.UseDeveloperExceptionPage();
        app.UseSwagger();
        app.UseSwaggerUI(c =>
        {
            c.SwaggerEndpoint("/swagger/v1/swagger.json", "YourProject API v1");
            c.RoutePrefix = "api-docs";
        });
    }
    else
    {
        app.UseExceptionHandler("/Home/Error");
        app.UseHsts();
    }

    // Security Headers
    app.UseMiddleware<SecurityHeadersMiddleware>();

    // Request Logging
    app.UseSerilogRequestLogging();

    // HTTPS Redirection
    app.UseHttpsRedirection();

    // Static Files
    app.UseStaticFiles();

    // Routing
    app.UseRouting();

    // CORS
    app.UseCors("DefaultCorsPolicy");

    // Rate Limiting
    app.UseIpRateLimiting();

    // Authentication & Authorization
    app.UseAuthentication();
    app.UseAuthorization();

    // Health Checks
    app.MapHealthChecks("/health", new HealthCheckOptions
    {
        Predicate = _ => true,
        ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
    });

    app.MapHealthChecksUI(options =>
    {
        options.UIPath = "/health-ui";
        options.ApiPath = "/health-api";
    });

    // Hangfire Dashboard
    app.MapHangfireDashboard("/hangfire", new DashboardOptions
    {
        Authorization = new[] { new HangfireAuthorizationFilter() }
    });

    // SignalR Hubs
    app.MapHub<NotificationHub>("/hubs/notifications");
    app.MapHub<ChatHub>("/hubs/chat");

    // API Controllers
    app.MapControllers();

    // MVC Routes
    app.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");

    // ============================================================
    // RUN APPLICATION
    // ============================================================
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

// ============================================================
// HELPER METHODS
// ============================================================
static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3, retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
}

static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(5, TimeSpan.FromSeconds(30));
}
```

---

## 🎨 COMPLETE _LAYOUT.CSHTML TEMPLATE

(Due to length, see RMMS.Web _Layout.cshtml for complete professional template with all libraries)

**Key Features Included:**
- ✅ Professional sidebar navigation
- ✅ Responsive design
- ✅ All JavaScript libraries loaded
- ✅ Microsoft Fluent Design System styling
- ✅ Nunito Sans professional font
- ✅ Complete icon libraries
- ✅ Toast notifications
- ✅ Data tables integration
- ✅ SweetAlert2 for confirmations
- ✅ Select2 for dropdowns
- ✅ AOS animations
- ✅ FullCalendar support
- ✅ File upload (Dropzone)
- ✅ Chart.js for visualizations

---

## 🚀 API CONTROLLER TEMPLATES

### Base API Controller

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using YourProject.Models;

namespace YourProject.Web.Controllers.API.v1
{
    [ApiController]
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    [Produces("application/json")]
    [Authorize]
    public class BaseApiController : ControllerBase
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
                Data = data,
                Timestamp = DateTime.UtcNow
            });
        }

        protected IActionResult Created<T>(T data, string message = "Created successfully")
        {
            return StatusCode(201, new ApiResponse<T>
            {
                Success = true,
                Message = message,
                Data = data,
                Timestamp = DateTime.UtcNow
            });
        }

        protected IActionResult Error(string message, int statusCode = 400, object? errors = null)
        {
            return StatusCode(statusCode, new ApiResponse<object>
            {
                Success = false,
                Message = message,
                Data = null,
                Errors = errors,
                Timestamp = DateTime.UtcNow
            });
        }

        protected IActionResult NotFound(string message = "Resource not found")
        {
            return StatusCode(404, new ApiResponse<object>
            {
                Success = false,
                Message = message,
                Data = null,
                Timestamp = DateTime.UtcNow
            });
        }
    }
}
```

### Complete CRUD API Controller Example

```csharp
using Microsoft.AspNetCore.Mvc;
using YourProject.Models;
using YourProject.Services.Interfaces;

namespace YourProject.Web.Controllers.API.v1
{
    [ApiController]
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    public class CustomersController : BaseApiController
    {
        private readonly ICustomerService _customerService;

        public CustomersController(ICustomerService customerService, ILogger<CustomersController> logger)
            : base(logger)
        {
            _customerService = customerService;
        }

        /// <summary>
        /// Get all customers with pagination
        /// </summary>
        [HttpGet]
        [ProducesResponseType(typeof(ApiResponse<PaginatedResult<CustomerDto>>), 200)]
        public async Task<IActionResult> GetAll(
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 10,
            [FromQuery] string? search = null,
            [FromQuery] string? sortBy = "Id",
            [FromQuery] string? sortOrder = "asc")
        {
            try
            {
                var result = await _customerService.GetAllAsync(page, pageSize, search, sortBy, sortOrder);
                return Success(result, "Customers retrieved successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving customers");
                return Error("An error occurred while retrieving customers", 500);
            }
        }

        /// <summary>
        /// Get customer by ID
        /// </summary>
        [HttpGet("{id}")]
        [ProducesResponseType(typeof(ApiResponse<CustomerDto>), 200)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> GetById(int id)
        {
            try
            {
                var customer = await _customerService.GetByIdAsync(id);
                if (customer == null)
                    return NotFound($"Customer with ID {id} not found");

                return Success(customer, "Customer retrieved successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving customer {CustomerId}", id);
                return Error("An error occurred while retrieving the customer", 500);
            }
        }

        /// <summary>
        /// Create new customer
        /// </summary>
        [HttpPost]
        [ProducesResponseType(typeof(ApiResponse<CustomerDto>), 201)]
        [ProducesResponseType(400)]
        public async Task<IActionResult> Create([FromBody] CustomerCreateDto model)
        {
            if (!ModelState.IsValid)
                return Error("Validation failed", 400, ModelState);

            try
            {
                var customer = await _customerService.CreateAsync(model);
                return Created(customer, "Customer created successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating customer");
                return Error("An error occurred while creating the customer", 500);
            }
        }

        /// <summary>
        /// Update existing customer
        /// </summary>
        [HttpPut("{id}")]
        [ProducesResponseType(200)]
        [ProducesResponseType(400)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> Update(int id, [FromBody] CustomerUpdateDto model)
        {
            if (!ModelState.IsValid)
                return Error("Validation failed", 400, ModelState);

            try
            {
                await _customerService.UpdateAsync(id, model);
                return Success<object>(null, "Customer updated successfully");
            }
            catch (NotFoundException)
            {
                return NotFound($"Customer with ID {id} not found");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating customer {CustomerId}", id);
                return Error("An error occurred while updating the customer", 500);
            }
        }

        /// <summary>
        /// Delete customer (soft delete)
        /// </summary>
        [HttpDelete("{id}")]
        [ProducesResponseType(200)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                await _customerService.DeleteAsync(id);
                return Success<object>(null, "Customer deleted successfully");
            }
            catch (NotFoundException)
            {
                return NotFound($"Customer with ID {id} not found");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting customer {CustomerId}", id);
                return Error("An error occurred while deleting the customer", 500);
            }
        }
    }
}
```

---

*[Continued in next response due to length...]*
