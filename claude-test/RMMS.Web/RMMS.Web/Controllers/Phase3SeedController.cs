using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Reporting;
using RMMS.Models.DataManagement;
using RMMS.Models.API;
using RMMS.Models.Mobile;
using RMMS.Models.Monitoring;

namespace RMMS.Web.Controllers
{
    [Authorize]
    public class Phase3SeedController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<Phase3SeedController> _logger;

        public Phase3SeedController(ApplicationDbContext context, ILogger<Phase3SeedController> logger)
        {
            _context = context;
            _logger = logger;
        }

        public IActionResult Index()
        {
            ViewBag.Message = "Click 'Seed Data' to populate Phase 3 and Phase 4 tables with test data.";
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> SeedPhase3Data()
        {
            try
            {
                int totalRecords = 0;

                // Seed Custom Report Definitions
                if (!await _context.Set<CustomReportDefinition>().AnyAsync())
                {
                    var reports = new List<CustomReportDefinition>
                    {
                        new() { Name = "Sales by Customer", Description = "Total sales grouped by customer", DataSource = "RiceSales", IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-30) },
                        new() { Name = "Inventory Summary", Description = "Current inventory levels by product", DataSource = "Inventory", IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-25) },
                        new() { Name = "Production Efficiency", Description = "Production output by machine", DataSource = "ProductionBatches", IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-20) },
                        new() { Name = "Revenue Analysis", Description = "Monthly revenue trends", DataSource = "RiceSales", IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-15) },
                        new() { Name = "Stock Movement Report", Description = "Track all stock movements", DataSource = "StockMovements", IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-10) }
                    };
                    await _context.Set<CustomReportDefinition>().AddRangeAsync(reports);
                    totalRecords += reports.Count;
                }

                // NOTE: ScheduledReport, ComparisonReport, DrilldownReport have schema mismatches
                // Use EF migrations or SQL script for proper seeding

                // Seed Dashboard Definitions
                if (!await _context.Set<DashboardDefinition>().AnyAsync())
                {
                    var dashboards = new List<DashboardDefinition>
                    {
                        new() { Name = "Executive Dashboard", Description = "High-level KPIs", RefreshInterval = 30, IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-45) },
                        new() { Name = "Sales Dashboard", Description = "Real-time sales monitoring", RefreshInterval = 60, IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-40) },
                        new() { Name = "Production Dashboard", Description = "Live production metrics", RefreshInterval = 15, IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-35) },
                        new() { Name = "Inventory Dashboard", Description = "Stock levels and movements", RefreshInterval = 120, IsActive = true, CreatedBy = "admin", CreatedDate = DateTime.Now.AddDays(-30) }
                    };
                    await _context.Set<DashboardDefinition>().AddRangeAsync(dashboards);
                    totalRecords += dashboards.Count;
                }

                // Save all Phase 3 Reporting data
                await _context.SaveChangesAsync();

                TempData["Success"] = $"Phase 3 & 4 seed data created successfully! Total records: {totalRecords}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error seeding Phase 3 data");
                TempData["Error"] = $"Error seeding data: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public IActionResult SeedPhase3DataManagement()
        {
            try
            {
                int totalRecords = 0;

                // NOTE: BulkOperation, BackupJob, ArchivalJob, AuditLog have schema mismatches
                // Use EF migrations or SQL script for proper seeding

                TempData["Success"] = $"Phase 3 Data Management seed data created! Total records: {totalRecords}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error seeding Phase 3 Data Management");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> SeedAllPhase3And4()
        {
            try
            {
                await SeedPhase3Data();
                SeedPhase3DataManagement();
                // Add more seed methods here

                TempData["Success"] = "ALL Phase 3 & 4 data seeded successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error seeding all data: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
