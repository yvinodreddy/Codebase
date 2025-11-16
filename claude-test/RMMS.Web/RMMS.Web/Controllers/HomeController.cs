using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using RMMS.Services;
using RMMS.Web.Models;

namespace RMMS.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IDashboardService _dashboardService;

        public HomeController(ILogger<HomeController> logger, IDashboardService dashboardService)
        {
            _logger = logger;
            _dashboardService = dashboardService;
            _logger.LogInformation("HomeController instantiated with DashboardService");
        }

        public IActionResult Index()
        {
            try
            {
                _logger.LogInformation("Index action called - Loading dashboard data");

                // Get real dashboard data from the service
                var username = User.Identity?.Name ?? "admin";
                var model = _dashboardService.GetDashboardData(username);

                // Get chart data for the view
                ViewBag.MonthlySalesChart = _dashboardService.GetMonthlySalesChart(DateTime.Now.Year);
                ViewBag.StockByVarietyChart = _dashboardService.GetStockByVarietyChart();

                _logger.LogInformation($"Dashboard loaded successfully - Paddy Stock: {model.TotalPaddyStock}, Monthly Revenue: {model.MonthlyRevenue}");

                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading dashboard data");

                // Return safe default dashboard on error
                var model = new DashboardViewModel
                {
                    TotalPaddyStock = 0,
                    TotalRiceStock = 0,
                    MonthlyRevenue = 0,
                    PendingPayments = 0,
                    TotalCustomers = 0,
                    TotalSuppliers = 0,
                    RecentTransactions = new List<TransactionSummary>(),
                    Alerts = new List<SystemAlert>
                    {
                        new SystemAlert
                        {
                            Type = "Error",
                            Message = $"Unable to load dashboard data: {ex.Message}",
                            Severity = "High"
                        }
                    }
                };

                return View(model);
            }
        }

        public IActionResult Privacy()
        {
            return View();
        }

        /// <summary>
        /// Professional Features Demo Page - Phase 1 Implementation
        /// Showcases: SweetAlert2, Toastr, Professional Buttons, Forms, Cards
        /// </summary>
        public IActionResult ProfessionalDemo()
        {
            _logger.LogInformation("Professional Demo page accessed");
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel
            {
                RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier
            });
        }
    }
}