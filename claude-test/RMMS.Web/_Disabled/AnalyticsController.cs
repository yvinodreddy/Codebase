using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Analytics;

namespace RMMS.Web.Controllers
{
    [Authorize]
    public class AnalyticsController : Controller
    {
        private readonly IProductionAnalyticsService _productionAnalytics;
        private readonly IInventoryAnalyticsService _inventoryAnalytics;
        private readonly ISalesTrendAnalyticsService _salesTrendAnalytics;
        private readonly IProfitMarginAnalysisService _profitMarginAnalytics;
        private readonly ICustomerBehaviorAnalyticsService _customerBehaviorAnalytics;
        private readonly ISupplierPerformanceService _supplierPerformance;
        private readonly ICostAnalysisService _costAnalysis;
        private readonly IBusinessIntelligenceService _businessIntelligence;

        public AnalyticsController(
            IProductionAnalyticsService productionAnalytics,
            IInventoryAnalyticsService inventoryAnalytics,
            ISalesTrendAnalyticsService salesTrendAnalytics,
            IProfitMarginAnalysisService profitMarginAnalytics,
            ICustomerBehaviorAnalyticsService customerBehaviorAnalytics,
            ISupplierPerformanceService supplierPerformance,
            ICostAnalysisService costAnalysis,
            IBusinessIntelligenceService businessIntelligence)
        {
            _productionAnalytics = productionAnalytics;
            _inventoryAnalytics = inventoryAnalytics;
            _salesTrendAnalytics = salesTrendAnalytics;
            _profitMarginAnalytics = profitMarginAnalytics;
            _customerBehaviorAnalytics = customerBehaviorAnalytics;
            _supplierPerformance = supplierPerformance;
            _costAnalysis = costAnalysis;
            _businessIntelligence = businessIntelligence;
        }

        // =============================================================================
        // MAIN DASHBOARD
        // =============================================================================

        public async Task<IActionResult> Index()
        {
            try
            {
                var dashboard = await _businessIntelligence.GetExecutiveDashboard();
                return View(dashboard);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading analytics dashboard: {ex.Message}";
                return View(new Dictionary<string, object>());
            }
        }

        // =============================================================================
        // PRODUCTION ANALYTICS (TASKS 1, 7, 8, 9)
        // =============================================================================

        public async Task<IActionResult> Production(DateTime? date)
        {
            try
            {
                var dashboard = await _productionAnalytics.GetProductionDashboard(date);
                ViewBag.SelectedDate = date ?? DateTime.Today;
                return View(dashboard);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading production analytics: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> MachineEfficiency(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;
                var efficiencies = await _productionAnalytics.GetMachineEfficiencies(start, end);
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View(efficiencies);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading machine efficiency: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> ShiftPerformance(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-7);
                var end = endDate ?? DateTime.Today;
                var performance = await _productionAnalytics.GetShiftPerformance(start, end);
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View(performance);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading shift performance: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> MachineUtilization(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;
                var utilization = await _productionAnalytics.GetMachineUtilization(start, end);
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View(utilization);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading machine utilization: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> QualityAnalytics(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;
                var trends = await _productionAnalytics.GetQualityTrends(start, end);
                var defects = await _productionAnalytics.GetDefectAnalysis(start, end);
                var suggestions = await _productionAnalytics.GetYieldOptimizationSuggestions();

                ViewBag.QualityTrends = trends;
                ViewBag.DefectAnalysis = defects;
                ViewBag.YieldSuggestions = suggestions;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading quality analytics: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> WasteTracking(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;
                var wasteByProduct = await _productionAnalytics.GetWasteByProduct(start, end);
                var wasteByProcess = await _productionAnalytics.GetWasteByProcess(start, end);
                var wasteCost = await _productionAnalytics.CalculateTotalWasteCost(start, end);
                var targets = await _productionAnalytics.GetWasteReductionTargets();

                ViewBag.WasteByProduct = wasteByProduct;
                ViewBag.WasteByProcess = wasteByProcess;
                ViewBag.TotalWasteCost = wasteCost;
                ViewBag.ReductionTargets = targets;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading waste tracking: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // INVENTORY ANALYTICS (TASKS 2, 10)
        // =============================================================================

        public async Task<IActionResult> Inventory()
        {
            try
            {
                var dashboard = await _inventoryAnalytics.GetInventoryDashboard();
                return View(dashboard);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inventory analytics: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> StockAging()
        {
            try
            {
                var aging = await _inventoryAnalytics.GetStockAgingAnalysis();
                return View(aging);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading stock aging: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> ABCClassification(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddYears(-1);
                var end = endDate ?? DateTime.Today;
                var classification = await _inventoryAnalytics.GetABCClassification(start, end);
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View(classification);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading ABC classification: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> StockMovement(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-90);
                var end = endDate ?? DateTime.Today;
                var classification = await _inventoryAnalytics.GetStockMovementClassification(start, end);
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View(classification);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading stock movement: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> StockAlerts()
        {
            try
            {
                var alerts = await _inventoryAnalytics.GetStockAlerts();
                var reorderSuggestions = await _inventoryAnalytics.GenerateAutoReorderSuggestions();
                var stockoutRisk = await _inventoryAnalytics.PredictStockoutRisk(30);

                ViewBag.Alerts = alerts;
                ViewBag.ReorderSuggestions = reorderSuggestions;
                ViewBag.StockoutRisk = stockoutRisk;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading stock alerts: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> DemandForecast(int productId, int daysAhead = 30)
        {
            try
            {
                var forecast = await _inventoryAnalytics.GetDemandForecast(productId, daysAhead);
                return View(forecast);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading demand forecast: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // SALES & CUSTOMER ANALYTICS (TASKS 3, 5)
        // =============================================================================

        public async Task<IActionResult> Sales(DateTime? startDate, DateTime? endDate, string periodType = "Monthly")
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddYears(-1);
                var end = endDate ?? DateTime.Today;
                var trends = await _salesTrendAnalytics.GetSalesTrends(start, end, periodType);
                var seasonal = await _salesTrendAnalytics.GetSeasonalPatterns();
                var topProducts = await _salesTrendAnalytics.GetTopProducts(10);
                var productMix = await _salesTrendAnalytics.GetProductMixAnalysis(start, end);

                ViewBag.Trends = trends;
                ViewBag.SeasonalPatterns = seasonal;
                ViewBag.TopProducts = topProducts;
                ViewBag.ProductMix = productMix;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                ViewBag.PeriodType = periodType;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading sales analytics: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> CustomerBehavior()
        {
            try
            {
                var patterns = await _customerBehaviorAnalytics.GetPurchasePatterns();
                var rfmAnalysis = await _customerBehaviorAnalytics.PerformRFMAnalysis();
                var clv = await _customerBehaviorAnalytics.CalculateCustomerLifetimeValue();
                var churn = await _customerBehaviorAnalytics.PredictChurn();

                ViewBag.PurchasePatterns = patterns;
                ViewBag.RFMAnalysis = rfmAnalysis;
                ViewBag.CustomerLifetimeValue = clv;
                ViewBag.ChurnPrediction = churn;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading customer behavior: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> CustomerSegmentation()
        {
            try
            {
                var segments = await _salesTrendAnalytics.GetCustomerSegmentation();
                return View(segments);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading customer segmentation: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // FINANCIAL ANALYTICS (TASKS 4, 11)
        // =============================================================================

        public async Task<IActionResult> Financial(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddMonths(-6);
                var end = endDate ?? DateTime.Today;

                var productMargins = await _profitMarginAnalytics.GetProductMargins(start, end);
                var customerProfitability = await _profitMarginAnalytics.GetCustomerProfitability(start, end);
                var costAnalysis = await _profitMarginAnalytics.GetCostAnalysis(start, end);
                var revenueBreakdown = await _profitMarginAnalytics.GetRevenueBreakdown(start, end);

                ViewBag.ProductMargins = productMargins;
                ViewBag.CustomerProfitability = customerProfitability;
                ViewBag.CostAnalysis = costAnalysis;
                ViewBag.RevenueBreakdown = revenueBreakdown;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading financial analytics: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> CostAnalysis(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddMonths(-6);
                var end = endDate ?? DateTime.Today;

                var costBreakdown = await _costAnalysis.GetCostBreakdown(start, end);
                var costTrends = await _costAnalysis.GetCostPerUnitTrends(start, end);
                var budgetVariance = await _costAnalysis.GetBudgetVariance(DateTime.Today);

                ViewBag.CostBreakdown = costBreakdown;
                ViewBag.CostTrends = costTrends;
                ViewBag.BudgetVariance = budgetVariance;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading cost analysis: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // SUPPLIER PERFORMANCE (TASK 6)
        // =============================================================================

        public async Task<IActionResult> Suppliers(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddMonths(-6);
                var end = endDate ?? DateTime.Today;

                var performance = await _supplierPerformance.GetSupplierPerformance(start, end);
                var delivery = await _supplierPerformance.GetDeliveryPerformance(start, end);
                var quality = await _supplierPerformance.GetQualityScores(start, end);
                var pricing = await _supplierPerformance.GetPriceCompetitiveness();

                ViewBag.SupplierPerformance = performance;
                ViewBag.DeliveryPerformance = delivery;
                ViewBag.QualityScores = quality;
                ViewBag.PriceCompetitiveness = pricing;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading supplier performance: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // EXECUTIVE DASHBOARD (TASK 12)
        // =============================================================================

        public async Task<IActionResult> Executive()
        {
            try
            {
                var kpis = await _businessIntelligence.GetExecutiveKPIs();
                var scorecard = await _businessIntelligence.GetPerformanceScorecard();
                var dashboard = await _businessIntelligence.GetExecutiveDashboard();

                ViewBag.KPIs = kpis;
                ViewBag.Scorecard = scorecard;
                ViewBag.Dashboard = dashboard;

                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading executive dashboard: {ex.Message}";
                return View();
            }
        }

        [HttpGet]
        public async Task<IActionResult> PerformanceScorecard()
        {
            try
            {
                var scorecard = await _businessIntelligence.GetPerformanceScorecard();
                return View(scorecard);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading performance scorecard: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // API ENDPOINTS FOR AJAX/CHARTS
        // =============================================================================

        [HttpGet]
        public async Task<IActionResult> GetProductionDashboardData(DateTime? date)
        {
            try
            {
                var dashboard = await _productionAnalytics.GetProductionDashboard(date);
                return Json(dashboard);
            }
            catch (Exception ex)
            {
                return Json(new { error = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetInventoryDashboardData()
        {
            try
            {
                var dashboard = await _inventoryAnalytics.GetInventoryDashboard();
                return Json(dashboard);
            }
            catch (Exception ex)
            {
                return Json(new { error = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetSalesTrendsData(DateTime? startDate, DateTime? endDate, string periodType = "Monthly")
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddMonths(-12);
                var end = endDate ?? DateTime.Today;
                var trends = await _salesTrendAnalytics.GetSalesTrends(start, end, periodType);
                return Json(trends);
            }
            catch (Exception ex)
            {
                return Json(new { error = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetExecutiveKPIsData()
        {
            try
            {
                var kpis = await _businessIntelligence.GetExecutiveKPIs();
                return Json(kpis);
            }
            catch (Exception ex)
            {
                return Json(new { error = ex.Message });
            }
        }
    }
}
