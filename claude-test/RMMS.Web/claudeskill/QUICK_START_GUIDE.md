# Quick Start Guide - Claude Skills
## Get Started in 5 Minutes

**Last Updated**: 2025-10-23
**Location**: `/home/user01/claude-test/RMMS.Web/claudeskill/`

---

## 🚀 ULTRA-FAST START

### Step 1: Choose Your Skill

**For most projects, use**: **Microsoft .NET Web API Master** ⭐ (Most comprehensive!)

| If you need... | Use this skill |
|----------------|----------------|
| Complete .NET app with JavaScript UI | **Microsoft .NET Web API Master** ⭐ |
| Healthcare/FHIR application | **Microsoft .NET Web API Master** |
| Real-time features (SignalR) | **Microsoft .NET Web API Master** |
| Background jobs (Hangfire) | **Microsoft .NET Web API Master** |
| Traditional MVC app | RMMS Project Generator |
| Healthcare management system | Microsoft .NET Web API Master |

---

### Step 2: Invoke the Skill

**Copy and customize this template:**

```
Using the Microsoft .NET Web API Master skill, create a [DOMAIN] management system:

Project Name: [YourProjectName]
Database: [YourProjectName]_DB

Core Features:
1. [Feature 1] - [Description]
2. [Feature 2] - [Description]
3. [Feature 3] - [Description]

Entities:
- [Entity1] (Id, Field1, Field2, Field3)
- [Entity2] (Id, Field1, Field2, FK to Entity1)
- [Entity3] (Id, Field1, Field2)

Technical Requirements:
- ASP.NET Core 8 MVC + Web API
- SQL Server database
- JWT authentication with roles (Admin, User, Manager)
- RESTful API with Swagger
- Bootstrap 5 + jQuery frontend
- DataTables for grids
- SweetAlert2 for confirmations
- Chart.js for dashboard visualizations
- SignalR for real-time notifications
- Hangfire for background jobs
- Redis caching
- Health checks + monitoring
- PDF reports (QuestPDF)
- Excel export (ClosedXML)
- Docker deployment

Generate complete production-ready project structure with all code.
```

---

### Step 3: Get Your Code

Claude will generate:
- ✅ Complete project structure (5 projects)
- ✅ All entity models
- ✅ Repository + Service layers
- ✅ MVC Controllers + Views
- ✅ Web API Controllers
- ✅ Authentication + Authorization
- ✅ Database migrations
- ✅ JavaScript integration
- ✅ Docker configuration
- ✅ Documentation

---

## 📋 EXAMPLE INVOCATIONS

### Example 1: E-Commerce Platform

```
Using the Microsoft .NET Web API Master skill, create an E-Commerce platform:

Project Name: ECommerceHub
Database: ECommerceHub_DB

Core Features:
1. Product Catalog - Browse, search, filter products
2. Shopping Cart - Add/remove items, calculate totals
3. Order Management - Create, track, fulfill orders
4. Customer Management - Registration, profiles, order history
5. Payment Processing - Multiple payment gateways
6. Real-time Inventory - SignalR updates when stock changes
7. Admin Dashboard - Sales analytics, charts, reports

Entities:
- Product (Id, Name, Description, Price, Stock, CategoryId, ImageUrl, SKU)
- Category (Id, Name, Description, ParentCategoryId)
- Customer (Id, Email, FirstName, LastName, Phone, Address, City, State, ZipCode)
- Order (Id, CustomerId, OrderDate, Status, TotalAmount, ShippingAddress)
- OrderItem (Id, OrderId, ProductId, Quantity, UnitPrice, Subtotal)
- ShoppingCart (Id, CustomerId, CreatedDate)
- CartItem (Id, CartId, ProductId, Quantity)
- Payment (Id, OrderId, PaymentMethod, Amount, TransactionId, Status, PaymentDate)

Technical Requirements:
- ASP.NET Core 8 MVC + Web API
- SQL Server with EF Core
- JWT authentication (Customer, Admin roles)
- Bootstrap 5 responsive UI
- DataTables for product/order grids
- Select2 for product/category dropdowns
- Chart.js dashboard (sales, revenue, top products)
- SignalR for real-time inventory updates
- Hangfire for order processing emails
- Redis caching for products/categories
- QuestPDF for invoices
- Swagger API documentation
- Docker + Docker Compose

Generate complete production-ready code.
```

---

### Example 2: Hospital Management System

```
Using the Microsoft .NET Web API Master skill, create a Hospital Management System:

Project Name: HealthCareHub
Database: HealthCareHub_DB

Core Features:
1. Patient Management - Registration, demographics, medical history
2. Appointment Scheduling - Calendar view with FullCalendar
3. Doctor Management - Specializations, schedules, availability
4. Medical Records - EHR, prescriptions, lab results
5. Billing & Insurance - Invoice generation, payment tracking
6. Real-time Notifications - Appointment reminders, test results
7. Dashboard & Analytics - Patient statistics, revenue charts

Entities:
- Patient (Id, FirstName, LastName, DOB, Gender, Phone, Email, Address, BloodType, Allergies)
- Doctor (Id, FirstName, LastName, Specialization, Phone, Email, LicenseNumber, DepartmentId)
- Appointment (Id, PatientId, DoctorId, AppointmentDate, Status, Reason, Notes)
- MedicalRecord (Id, PatientId, DoctorId, Diagnosis, Prescription, RecordDate, AttachmentUrl)
- Department (Id, Name, Description, Floor, Phone)
- Invoice (Id, PatientId, Amount, Status, DueDate, InvoiceDate, Items)
- LabTest (Id, PatientId, TestType, Result, TestDate, TechnicianId)

Technical Requirements:
- ASP.NET Core 8 MVC + Web API
- SQL Server with EF Core
- JWT authentication (Admin, Doctor, Nurse, Patient roles)
- Bootstrap 5 responsive UI
- DataTables for patient/appointment grids
- FullCalendar for appointment scheduling
- Select2 for doctor/patient search
- Chart.js for dashboard analytics
- SignalR for real-time appointment updates
- Hangfire for appointment reminder emails
- Redis caching for doctor schedules
- QuestPDF for medical reports
- Dropzone for file uploads (lab results, X-rays)
- SweetAlert2 for appointment confirmations
- Health checks + monitoring
- Docker deployment

Optional FHIR Integration:
- Add Hl7.Fhir.R4 for FHIR resource support
- FHIR Patient, Practitioner, Appointment resources

Generate complete production-ready code.
```

---

### Example 3: Manufacturing ERP

```
Using the Microsoft .NET Web API Master skill, create a Manufacturing ERP system:

Project Name: ManufactureERP
Database: ManufactureERP_DB

Core Features:
1. Production Management - Orders, batches, scheduling
2. Inventory Control - Raw materials, finished goods, warehouses
3. Machine Monitoring - Real-time status with SignalR
4. Quality Control - Inspections, defect tracking
5. Supply Chain - Vendor management, purchase orders
6. Shop Floor Dashboard - Production metrics, machine utilization
7. Reporting - Production reports, yield analysis

Entities:
- ProductionOrder (Id, OrderNumber, ProductId, Quantity, StartDate, DueDate, Status, Priority)
- ProductionBatch (Id, OrderId, BatchNumber, MachineId, StartTime, EndTime, ActualQuantity, Status)
- Machine (Id, Name, Type, Location, Status, LastMaintenanceDate, NextMaintenanceDate)
- Product (Id, Name, SKU, Description, UnitPrice, ProductionTime)
- RawMaterial (Id, Name, Description, Unit, ReorderLevel, CurrentStock)
- Warehouse (Id, Name, Location, Type, Capacity)
- Inventory (Id, WarehouseId, ItemType, ItemId, Quantity, LastUpdated)
- QualityInspection (Id, BatchId, InspectorId, InspectionDate, Result, DefectCount, Notes)
- Vendor (Id, Name, ContactPerson, Phone, Email, Address, Rating)
- PurchaseOrder (Id, VendorId, OrderDate, Status, TotalAmount)

Technical Requirements:
- ASP.NET Core 8 MVC + Web API
- SQL Server with EF Core
- JWT authentication (Admin, Manager, Operator, QC roles)
- Bootstrap 5 responsive UI
- DataTables for all grids
- FullCalendar for production scheduling
- Chart.js for real-time machine monitoring
- SignalR for live production updates
- Hangfire for maintenance reminders
- Redis caching for machine status
- QuestPDF for production reports
- Excel export with ClosedXML
- Health checks for machine connectivity
- Docker deployment

Generate complete production-ready code.
```

---

## 🎯 CUSTOMIZATION OPTIONS

### Adjust the Technology Stack

**Use different database?**
```
Replace SQL Server with PostgreSQL:
- Use Npgsql.EntityFrameworkCore.PostgreSQL package
- Update connection string
```

**Add Azure Services?**
```
Include in requirements:
- Azure Blob Storage for file uploads
- Azure Service Bus for messaging
- Azure App Insights for monitoring
```

**Add Identity?**
```
Include in requirements:
- ASP.NET Core Identity for user management
- Email confirmation
- Two-factor authentication
- External logins (Google, Microsoft, Facebook)
```

**Add More JavaScript Libraries?**
```
Include in requirements:
- Moment.js for date formatting
- lodash for utility functions
- axios for HTTP requests
- Vue.js or React components (specific areas)
```

---

## 📚 WHAT YOU GET

### Backend Code
```
✅ 5-layer clean architecture
✅ Generic repository pattern
✅ Service layer with business logic
✅ API versioning (v1, v2, etc.)
✅ JWT authentication + refresh tokens
✅ Role-based authorization
✅ Input validation (FluentValidation optional)
✅ Exception handling middleware
✅ Rate limiting
✅ CORS configuration
✅ Health checks
✅ Hangfire background jobs
✅ SignalR hubs
✅ Caching with Redis
```

### Frontend Code
```
✅ Responsive Bootstrap 5 layout
✅ Professional sidebar navigation
✅ DataTables with export buttons
✅ SweetAlert2 confirmations
✅ Toastr notifications
✅ Select2 dropdowns
✅ Chart.js visualizations
✅ FullCalendar scheduling
✅ Dropzone file uploads
✅ Form validation
✅ AJAX operations
✅ SignalR client integration
```

### DevOps & Deployment
```
✅ Dockerfile
✅ docker-compose.yml
✅ Kubernetes manifests (optional)
✅ GitHub Actions CI/CD
✅ Azure Pipelines (optional)
✅ Environment configurations
✅ Database migrations
✅ Seed data scripts
```

### Documentation
```
✅ README.md
✅ API documentation (Swagger)
✅ Architecture diagram
✅ Database schema
✅ Deployment guide
✅ Testing guide
```

---

## 🔧 COMMON MODIFICATIONS

### Add New Entity

**Prompt**:
```
Add a new Supplier entity to my project:

Supplier (Id, CompanyName, ContactPerson, Email, Phone, Address, Rating, IsActive)

Generate:
- Entity model
- Repository interface + implementation
- Service interface + implementation
- MVC Controller + Views (Index, Create, Edit, Details, Delete)
- API Controller with CRUD endpoints
- DataTables integration for listing
- Form validation
```

### Add Background Job

**Prompt**:
```
Add a Hangfire background job for sending daily sales reports:

Requirements:
- Run daily at 8:00 AM
- Generate PDF report with yesterday's sales
- Email report to admin@company.com
- Log execution in database

Generate:
- Hangfire job class
- Report generation logic
- Email service integration
- Hangfire configuration in Program.cs
```

### Add SignalR Feature

**Prompt**:
```
Add SignalR real-time stock updates:

Requirements:
- When inventory quantity changes, broadcast update to all connected clients
- Update UI automatically without page refresh
- Show notification toast

Generate:
- SignalR hub (StockHub)
- Server-side broadcast code (in InventoryService)
- Client-side JavaScript (connection + event handling)
- UI update logic
```

---

## 🎓 LEARNING RESOURCES

### After Generation

1. **Explore the code**: Start with `Program.cs` to understand configuration
2. **Run migrations**: `dotnet ef database update`
3. **Seed data**: Run the application, data will be seeded automatically
4. **Test APIs**: Open `/api-docs` (Swagger)
5. **Browse UI**: Navigate to `/` to see the MVC interface
6. **Check health**: Visit `/health-ui` for system health
7. **View jobs**: Access `/hangfire` for background jobs

### Key Files to Understand

```
Program.cs                  → Application configuration
ApplicationDbContext.cs     → Database context
Repository.cs               → Generic data access
BaseService.cs              → Service pattern
BaseApiController.cs        → API base controller
_Layout.cshtml              → Main UI layout
site.js                     → JavaScript utilities
```

---

## 💡 PRO TIPS

1. **Start simple**: Begin with basic CRUD, add advanced features incrementally
2. **Use Swagger**: Test APIs immediately with Swagger UI
3. **Check logs**: Serilog writes to `logs/` directory
4. **Monitor health**: `/health-ui` shows database, Redis, API status
5. **Test real-time**: Open two browser tabs to test SignalR
6. **Background jobs**: Check `/hangfire` dashboard for job status
7. **Export data**: DataTables has built-in export to Excel, PDF, CSV
8. **Responsive**: Test on mobile - Bootstrap 5 makes it responsive
9. **Security**: Change JWT secret key before deploying
10. **Performance**: Use Redis for caching frequently accessed data

---

## 🚨 TROUBLESHOOTING

**Database connection fails?**
- Check connection string in `appsettings.json`
- Ensure SQL Server is running
- Run migrations: `dotnet ef database update`

**JWT token not working?**
- Verify secret key is at least 256 bits (32 characters)
- Check token expiration time
- Ensure "Bearer " prefix in Authorization header

**SignalR not connecting?**
- Check browser console for errors
- Verify `/hubs/notifications` endpoint
- Ensure JWT token is passed in connection

**Hangfire dashboard not loading?**
- Check Hangfire authorization filter
- Verify database connection
- Check `/hangfire` route is registered

**DataTables not initializing?**
- Check jQuery is loaded before DataTables
- Verify `.datatable` class on table
- Check browser console for JavaScript errors

---

## 🎉 YOU'RE READY!

You now have everything to generate production-ready .NET applications!

**Need help?** Just ask Claude to:
- "Explain how [feature] works in my project"
- "Add [new feature] to my application"
- "Fix [specific issue] in my code"
- "Optimize [performance issue]"

**Happy Coding!** 🚀

---

*Quick Start Guide - Claude Skills*
*Version 1.0*
*Last Updated: 2025-10-23*
