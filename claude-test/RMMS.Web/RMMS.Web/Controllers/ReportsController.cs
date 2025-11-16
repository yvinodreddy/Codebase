using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Models.ViewModels;
using RMMS.Models.Production;
using RMMS.Services;
using RMMS.Services.Interfaces.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Web.Controllers
{
    public class ReportsController : Controller
    {
        private readonly ILogger<ReportsController> _logger;
        private readonly IRiceSalesService _riceSalesService;
        private readonly IByProductSalesService _byProductService;
        private readonly ICashBookService _cashBookService;
        private readonly IBankTransactionService _bankService;
        private readonly IPayableOverdueService _payableService;
        private readonly IReceivableOverdueService _receivableService;
        private readonly IFixedAssetService _fixedAssetService;
        private readonly ILoansAdvancesService _loansService;
        private readonly IVoucherService _voucherService;
        private readonly IReportService _reportService;
        private readonly IPaddyProcurementService _paddyProcurementService;
        private readonly IProductionBatchService _productionBatchService;
        private readonly IProductionOrderService _productionOrderService;
        private readonly IMachineService _machineService;

        public ReportsController(
            ILogger<ReportsController> logger,
            IRiceSalesService riceSalesService,
            IByProductSalesService byProductService,
            ICashBookService cashBookService,
            IBankTransactionService bankService,
            IPayableOverdueService payableService,
            IReceivableOverdueService receivableService,
            IFixedAssetService fixedAssetService,
            ILoansAdvancesService loansService,
            IVoucherService voucherService,
            IReportService reportService,
            IPaddyProcurementService paddyProcurementService,
            IProductionBatchService productionBatchService,
            IProductionOrderService productionOrderService,
            IMachineService machineService)
        {
            _logger = logger;
            _riceSalesService = riceSalesService;
            _byProductService = byProductService;
            _cashBookService = cashBookService;
            _bankService = bankService;
            _payableService = payableService;
            _receivableService = receivableService;
            _fixedAssetService = fixedAssetService;
            _loansService = loansService;
            _voucherService = voucherService;
            _reportService = reportService;
            _paddyProcurementService = paddyProcurementService;
            _productionBatchService = productionBatchService;
            _productionOrderService = productionOrderService;
            _machineService = machineService;
        }

        public IActionResult Index()
        {
            try
            {
                ViewBag.CurrentMonth = DateTime.Now.ToString("MMMM yyyy");
                ViewBag.CurrentYear = DateTime.Now.Year;

                // Get quick stats for dashboard
                var today = DateTime.Today;
                var monthStart = new DateTime(today.Year, today.Month, 1);

                ViewBag.TodaysSales = _riceSalesService.GetTotalSalesAmount(today, today);
                ViewBag.MonthSales = _riceSalesService.GetTotalSalesAmount(monthStart, today);
                ViewBag.PendingPayments = _riceSalesService.GetPendingPayments().Count;
                ViewBag.TotalReceivables = _receivableService.GetTotalOutstandingAmount();

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading reports dashboard");
                TempData["Error"] = "Unable to load reports dashboard.";
                return RedirectToAction("Index", "Home");
            }
        }

        public IActionResult DailySales(DateTime? date = null)
        {
            try
            {
                var reportDate = date ?? DateTime.Today;

                // Get actual sales data from service
                var salesData = _riceSalesService.GetAllSales(true)
                    .Where(s => s.SaleDate.Date == reportDate.Date)
                    .ToList();

                var byProductSales = _byProductService.GetAllSales()
                    .Where(s => s.SaleDate.Date == reportDate.Date)
                    .ToList();

                ViewBag.ReportDate = reportDate.ToString("dd-MMM-yyyy");
                ViewBag.DayName = reportDate.ToString("dddd");
                ViewBag.RiceSales = salesData;
                ViewBag.ByProductSales = byProductSales;

                // Calculate totals
                ViewBag.TotalRiceSales = salesData.Sum(s => s.GrossInvoiceAmount);
                ViewBag.TotalByProductSales = byProductSales.Sum(s => s.TotalAmount);
                ViewBag.GrandTotal = ViewBag.TotalRiceSales + ViewBag.TotalByProductSales;
                ViewBag.TotalQuantity = salesData.Sum(s => s.Quantity) + byProductSales.Sum(s => s.Quantity);
                ViewBag.NumberOfInvoices = salesData.Count + byProductSales.Count;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating daily sales report");
                TempData["Error"] = "Unable to generate daily sales report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult MonthlySales(int? month = null, int? year = null)
        {
            try
            {
                var reportMonth = month ?? DateTime.Now.Month;
                var reportYear = year ?? DateTime.Now.Year;

                var startDate = new DateTime(reportYear, reportMonth, 1);
                var endDate = startDate.AddMonths(1).AddDays(-1);

                // Get data from services
                var riceSales = _riceSalesService.GetAllSales(true)
                    .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                    .ToList();

                var byProductSales = _byProductService.GetSalesByDateRange(startDate, endDate);

                // Prepare daily breakdown
                var dailyBreakdown = new Dictionary<int, decimal>();
                for (int day = 1; day <= endDate.Day; day++)
                {
                    var dayDate = new DateTime(reportYear, reportMonth, day);
                    var daySales = riceSales.Where(s => s.SaleDate.Date == dayDate).Sum(s => s.GrossInvoiceAmount);
                    var dayByProduct = byProductSales.Where(s => s.SaleDate.Date == dayDate).Sum(s => s.TotalAmount);
                    dailyBreakdown[day] = daySales + dayByProduct;
                }

                ViewBag.Month = reportMonth;
                ViewBag.Year = reportYear;
                ViewBag.MonthName = startDate.ToString("MMMM");
                ViewBag.DaysInMonth = DateTime.DaysInMonth(reportYear, reportMonth);
                ViewBag.RiceSales = riceSales;
                ViewBag.ByProductSales = byProductSales;
                ViewBag.DailyBreakdown = dailyBreakdown;

                ViewBag.TotalMonthlySales = riceSales.Sum(s => s.GrossInvoiceAmount) + byProductSales.Sum(s => s.TotalAmount);
                ViewBag.AverageDailySales = ViewBag.TotalMonthlySales / endDate.Day;
                ViewBag.BestSellingDay = dailyBreakdown.Any() ?
                    dailyBreakdown.OrderByDescending(d => d.Value).First().Key.ToString() : "N/A";

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating monthly sales report");
                TempData["Error"] = "Unable to generate monthly sales report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult CustomerWiseSales(string? customerName = null)
        {
            try
            {
                List<RiceSales> salesData;

                if (!string.IsNullOrEmpty(customerName))
                {
                    salesData = _riceSalesService.SearchSalesByCustomer(customerName);
                }
                else
                {
                    salesData = _riceSalesService.GetAllSales(true);
                }

                // Group by customer
                var customerGroups = salesData.GroupBy(s => s.BuyerName)
                    .Select(g => new
                    {
                        CustomerName = g.Key,
                        TotalSales = g.Sum(s => s.GrossInvoiceAmount),
                        TotalQuantity = g.Sum(s => s.Quantity),
                        NumberOfOrders = g.Count(),
                        AverageOrderValue = g.Average(s => s.GrossInvoiceAmount),
                        LastOrderDate = g.Max(s => s.SaleDate)
                    })
                    .OrderByDescending(c => c.TotalSales)
                    .ToList();

                ViewBag.CustomerFilter = customerName;
                ViewBag.ReportGeneratedAt = DateTime.Now;
                ViewBag.CustomerGroups = customerGroups;
                ViewBag.TotalCustomers = customerGroups.Count;
                ViewBag.TotalRevenue = customerGroups.Sum(c => c.TotalSales);

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating customer-wise sales report");
                TempData["Error"] = "Unable to generate customer report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult ProductWiseSales(string? productType = null)
        {
            var viewModel = new ProductWiseSalesViewModel();
            try
            {
                // Get rice sales grouped by grade
                var riceSales = _riceSalesService.GetAllSales(true);
                var riceGroups = riceSales.GroupBy(s => s.RiceGrade)
                    .Select(g => new
                    {
                        ProductName = g.Key,
                        ProductCategory = "Rice",
                        TotalQuantity = g.Sum(s => s.Quantity),
                        TotalSales = g.Sum(s => s.GrossInvoiceAmount),
                        NumberOfSales = g.Count(),
                        AveragePrice = g.Average(s => s.UnitPrice)
                    }).ToList();

                // Get by-product sales grouped by type
                var byProducts = _byProductService.GetAllSales();
                var byProductGroups = byProducts.GroupBy(s => s.ProductType)
                    .Select(g => new
                    {
                        ProductName = g.Key,
                        ProductCategory = "By-Product",
                        TotalQuantity = g.Sum(s => s.Quantity),
                        TotalSales = g.Sum(s => s.TotalAmount),
                        NumberOfSales = g.Count(),
                        AveragePrice = g.Average(s => s.Rate)
                    }).ToList();

                // Combine all products
                var allProducts = riceGroups.Concat(byProductGroups).ToList();

                if (!string.IsNullOrEmpty(productType))
                {
                    allProducts = allProducts.Where(p => p.ProductName != null && p.ProductName.Contains(productType, StringComparison.OrdinalIgnoreCase)).ToList();
                }

                // Map to the strongly-typed model
                foreach (var item in allProducts)
                {
                    viewModel.ProductGroups.Add(new ProductSalesGroup
                    {
                        ProductName = item.ProductName,
                        ProductCategory = item.ProductCategory,
                        TotalQuantity = item.TotalQuantity,
                        TotalSales = item.TotalSales,
                        NumberOfSales = item.NumberOfSales,
                        AveragePrice = item.AveragePrice
                    });
                }

                viewModel.ProductFilter = productType;
                viewModel.TotalProducts = viewModel.ProductGroups.Count;
                viewModel.GrandTotalSales = viewModel.ProductGroups.Sum(p => p.TotalSales);
                viewModel.TotalQuantitySold = viewModel.ProductGroups.Sum(p => p.TotalQuantity);

                return View(viewModel);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating product-wise sales report");
                TempData["Error"] = "Unable to generate product report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult ProfitLoss(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1);
                var end = endDate ?? DateTime.Now;

                // Calculate revenue
                var riceSalesRevenue = _riceSalesService.GetTotalSalesAmount(start, end);
                var byProductRevenue = _byProductService.GetTotalSalesAmount(start, end);
                var totalRevenue = riceSalesRevenue + byProductRevenue;

                // Calculate expenses (from cash book and bank transactions)
                var cashPayments = _cashBookService.GetTotalPayments(start, end);
                var bankPayments = _bankService.GetTransactionsByDateRange(start, end)
                    .Sum(t => t.Withdrawals);
                var totalExpenses = cashPayments + bankPayments;

                // Calculate pending amounts
                var pendingReceivables = _receivableService.GetTotalOutstandingAmount();
                var pendingPayables = _payableService.GetTotalOutstandingAmount();

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.ReportPeriod = $"{start:dd-MMM-yyyy} to {end:dd-MMM-yyyy}";

                ViewBag.RiceSalesRevenue = riceSalesRevenue;
                ViewBag.ByProductRevenue = byProductRevenue;
                ViewBag.TotalRevenue = totalRevenue;
                ViewBag.CashExpenses = cashPayments;
                ViewBag.BankExpenses = bankPayments;
                ViewBag.TotalExpenses = totalExpenses;
                ViewBag.GrossProfit = totalRevenue - totalExpenses;
                ViewBag.NetProfit = ViewBag.GrossProfit;
                ViewBag.PendingReceivables = pendingReceivables;
                ViewBag.PendingPayables = pendingPayables;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating profit & loss report");
                TempData["Error"] = "Unable to generate P&L report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult CashFlow(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? DateTime.Now.AddDays(-30);
                var end = endDate ?? DateTime.Now;

                // Get cash transactions
                var cashTransactions = _cashBookService.GetAll()
                    .Where(c => c.TransactionDate >= start && c.TransactionDate <= end)
                    .OrderBy(c => c.TransactionDate)
                    .ToList();

                // Get bank transactions
                var bankTransactions = _bankService.GetTransactionsByDateRange(start, end);

                // Calculate opening balance (transactions before start date)
                var openingCashBalance = _cashBookService.GetAll()
                    .Where(c => c.TransactionDate < start)
                    .Sum(c => c.Receipts - c.Payments);

                var openingBankBalance = _bankService.GetAll()
                    .Where(b => b.TransactionDate < start)
                    .Sum(b => b.Deposits - b.Withdrawals);

                var totalReceipts = cashTransactions.Sum(c => c.Receipts) +
                                   bankTransactions.Sum(b => b.Deposits);
                var totalPayments = cashTransactions.Sum(c => c.Payments) +
                                   bankTransactions.Sum(b => b.Withdrawals);

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.CashTransactions = cashTransactions;
                ViewBag.BankTransactions = bankTransactions;
                ViewBag.OpeningBalance = openingCashBalance + openingBankBalance;
                ViewBag.TotalReceipts = totalReceipts;
                ViewBag.TotalPayments = totalPayments;
                ViewBag.NetCashFlow = totalReceipts - totalPayments;
                ViewBag.ClosingBalance = ViewBag.OpeningBalance + ViewBag.NetCashFlow;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating cash flow report");
                TempData["Error"] = "Unable to generate cash flow report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult OutstandingPayments()
        {
            try
            {
                var payables = _payableService.GetAll();
                var overduePayables = _payableService.GetOverduePayables();

                var receivables = _receivableService.GetAll();
                var overdueReceivables = _receivableService.GetOverdueReceivables();

                ViewBag.Payables = payables;
                ViewBag.OverduePayables = overduePayables;
                ViewBag.Receivables = receivables;
                ViewBag.OverdueReceivables = overdueReceivables;

                ViewBag.TotalPayables = payables.Sum(p => p.BalancePayable);
                ViewBag.TotalReceivables = receivables.Sum(r => r.BalanceDue);
                ViewBag.OverduePayableAmount = overduePayables.Sum(p => p.BalancePayable);
                ViewBag.OverdueReceivableAmount = overdueReceivables.Sum(r => r.BalanceDue);

                ViewBag.NumberOfVendors = payables.Select(p => p.SupplierName).Distinct().Count();
                ViewBag.NumberOfCustomers = receivables.Select(r => r.CustomerName).Distinct().Count();

                // Find oldest overdue
                ViewBag.OldestPayableDays = overduePayables.Any() ? overduePayables.Max(p => p.DaysOverdue) : 0;
                ViewBag.OldestReceivableDays = overdueReceivables.Any() ? overdueReceivables.Max(r => r.DaysOverdue) : 0;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating outstanding payments report");
                TempData["Error"] = "Unable to generate outstanding payments report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult GSTReport(int? month = null, int? year = null)
        {
            try
            {
                var reportMonth = month ?? DateTime.Now.Month;
                var reportYear = year ?? DateTime.Now.Year;

                var startDate = new DateTime(reportYear, reportMonth, 1);
                var endDate = startDate.AddMonths(1).AddDays(-1);

                var sales = _riceSalesService.GetAllSales(true)
                    .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                    .ToList();

                ViewBag.Month = reportMonth;
                ViewBag.Year = reportYear;
                ViewBag.MonthName = startDate.ToString("MMMM");
                ViewBag.ReportPeriod = $"{startDate:dd-MMM-yyyy} to {endDate:dd-MMM-yyyy}";

                ViewBag.Sales = sales;
                ViewBag.TotalSalesValue = sales.Sum(s => s.TotalInvoiceValue);
                ViewBag.TotalTaxableValue = sales.Sum(s => s.TaxableValue);
                ViewBag.TotalCGST = sales.Sum(s => s.CGSTAmount);
                ViewBag.TotalSGST = sales.Sum(s => s.SGSTAmount);
                ViewBag.TotalIGST = sales.Sum(s => s.IGSTAmount);
                ViewBag.TotalGST = ViewBag.TotalCGST + ViewBag.TotalSGST + ViewBag.TotalIGST;

                // Group by GST type
                var intrastateCount = sales.Where(s => s.IGSTAmount == 0).Count();
                var interstateCount = sales.Where(s => s.IGSTAmount > 0).Count();

                ViewBag.IntrastateCount = intrastateCount;
                ViewBag.InterstateCount = interstateCount;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating GST report");
                TempData["Error"] = "Unable to generate GST report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult StockSummary()
        {
            try
            {
                // Get stock data from report service
                var stockData = _reportService.GetStockSummaryReport();

                ViewBag.StockData = stockData;
                ViewBag.LastUpdated = DateTime.Now;
                ViewBag.GeneratedBy = User.Identity?.Name ?? "System";

                // You can add more specific stock calculations here
                ViewBag.TotalStockValue = stockData.ContainsKey("TotalStockValue") ?
                    stockData["TotalStockValue"] : 0m;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating stock summary report");
                TempData["Error"] = "Unable to generate stock summary.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult PaddyStock()
        {
            try
            {
                // Get actual paddy procurement data
                var procurements = _paddyProcurementService.GetAllProcurements(true);

                // Group by variety to show stock by variety
                var stockByVariety = procurements
                    .GroupBy(p => p.PaddyVariety ?? "Unknown")
                    .Select(g => new
                    {
                        Variety = g.Key,
                        TotalStock = g.Sum(p => p.ClosingStock ?? 0)
                    })
                    .ToDictionary(x => x.Variety, x => x.TotalStock);

                ViewBag.ReportDate = DateTime.Now;
                ViewBag.TotalPaddyStock = stockByVariety.Sum(s => s.Value);
                ViewBag.StockByVariety = stockByVariety;
                ViewBag.ProcurementRecords = procurements;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating paddy stock report");
                TempData["Error"] = "Unable to generate paddy stock report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult RiceStock()
        {
            try
            {
                // Group rice by grade from sales data
                var riceSales = _riceSalesService.GetAllSales(true);
                var stockByGrade = riceSales.GroupBy(s => s.RiceGrade)
                    .Select(g => new
                    {
                        Grade = g.Key,
                        TotalQuantity = g.Sum(s => s.Quantity)
                    })
                    .ToList();

                ViewBag.ReportDate = DateTime.Now;
                ViewBag.StockByGrade = stockByGrade;
                ViewBag.TotalRiceStock = stockByGrade.Sum(s => s.TotalQuantity);

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating rice stock report");
                TempData["Error"] = "Unable to generate rice stock report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult StockMovement(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? DateTime.Now.AddDays(-30);
                var end = endDate ?? DateTime.Now;

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.ReportPeriod = $"{start:dd-MMM-yyyy} to {end:dd-MMM-yyyy}";

                // Calculate inward movements (procurement)
                var procurements = _paddyProcurementService.GetAllProcurements(true)
                    .Where(p => p.ReceiptDate >= start && p.ReceiptDate <= end);
                var totalInward = procurements.Sum(p => p.QuantityReceived);

                // Calculate outward movements (rice sales)
                var riceSales = _riceSalesService.GetSalesByDateRange(start, end);
                var totalOutward = riceSales.Sum(s => s.Quantity);

                ViewBag.TotalInward = totalInward;
                ViewBag.TotalOutward = totalOutward;
                ViewBag.NetMovement = totalInward - totalOutward;

                // Prepare movement list for table
                var movements = new List<dynamic>();

                // Add procurements (inward)
                foreach (var proc in procurements.OrderBy(p => p.ReceiptDate))
                {
                    movements.Add(new
                    {
                        Date = proc.ReceiptDate,
                        Type = "Procurement",
                        Item = proc.PaddyVariety ?? "Paddy",
                        Reference = $"PRC-{proc.Id}",
                        Inward = proc.QuantityReceived,
                        Outward = 0m,
                        Remarks = proc.SupplierName
                    });
                }

                // Add sales (outward)
                foreach (var sale in riceSales.OrderBy(s => s.SaleDate))
                {
                    movements.Add(new
                    {
                        Date = sale.SaleDate,
                        Type = "Sale",
                        Item = sale.RiceGrade ?? "Rice",
                        Reference = $"SAL-{sale.Id}",
                        Inward = 0m,
                        Outward = sale.Quantity,
                        Remarks = sale.BuyerName
                    });
                }

                ViewBag.Movements = movements.OrderBy(m => m.Date).ToList();

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating stock movement report");
                TempData["Error"] = "Unable to generate stock movement report.";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public IActionResult CustomReport(string? reportType, DateTime? fromDate, DateTime? toDate)
        {
            try
            {
                ViewBag.ReportType = reportType;
                ViewBag.FromDate = fromDate?.ToString("dd-MMM-yyyy") ?? "N/A";
                ViewBag.ToDate = toDate?.ToString("dd-MMM-yyyy") ?? "N/A";

                if (!string.IsNullOrEmpty(reportType) && fromDate.HasValue && toDate.HasValue)
                {
                    switch (reportType.ToLower())
                    {
                        case "sales":
                            ViewBag.ReportTitle = "Sales Analysis Report";
                            var salesData = _riceSalesService.GetAllSales(true)
                                .Where(s => s.SaleDate >= fromDate && s.SaleDate <= toDate)
                                .ToList();
                            ViewBag.ReportData = salesData;
                            ViewBag.TotalAmount = salesData.Sum(s => s.GrossInvoiceAmount);
                            break;

                        case "procurement":
                            ViewBag.ReportTitle = "Procurement Analysis Report";
                            // Add procurement data when available
                            break;

                        case "financial":
                            ViewBag.ReportTitle = "Financial Summary Report";
                            var revenue = _riceSalesService.GetTotalSalesAmount(fromDate.Value, toDate.Value);
                            var expenses = _cashBookService.GetTotalPayments(fromDate.Value, toDate.Value);
                            ViewBag.Revenue = revenue;
                            ViewBag.Expenses = expenses;
                            ViewBag.NetIncome = revenue - expenses;
                            break;

                        default:
                            ViewBag.ReportTitle = "Custom Report";
                            break;
                    }
                }
                else
                {
                    ViewBag.ReportTitle = "Custom Report - Select Parameters";
                }

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating custom report");
                TempData["Error"] = "Unable to generate custom report.";
                return RedirectToAction(nameof(Index));
            }
        }

        #region Export Actions

        [HttpGet]
        public IActionResult ExportProfitLossPdf(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1);
                var end = endDate ?? DateTime.Now;

                // Calculate revenue
                var riceSalesRevenue = _riceSalesService.GetTotalSalesAmount(start, end);
                var byProductRevenue = _byProductService.GetTotalSalesAmount(start, end);
                var totalRevenue = riceSalesRevenue + byProductRevenue;

                // Calculate expenses
                var cashPayments = _cashBookService.GetTotalPayments(start, end);
                var bankPayments = _bankService.GetTransactionsByDateRange(start, end)
                    .Sum(t => t.Withdrawals);
                var totalExpenses = cashPayments + bankPayments;

                var netProfit = totalRevenue - totalExpenses;

                // Prepare income breakdown
                var incomeBreakdown = new List<(string Category, decimal Amount)>
                {
                    ("Rice Sales", riceSalesRevenue),
                    ("By-Product Sales", byProductRevenue)
                };

                // Prepare expense breakdown
                var expenseBreakdown = new List<(string Category, decimal Amount)>
                {
                    ("Cash Payments", cashPayments),
                    ("Bank Payments", bankPayments)
                };

                // Generate PDF using PdfExportHelper (would need to implement this)
                // For now, using a simple approach with iTextSharp if available
                var pdfBytes = Services.Helpers.ExcelExportHelper.ExportProfitLossToExcel(
                    totalRevenue, totalExpenses, netProfit,
                    incomeBreakdown, expenseBreakdown, start, end);

                return File(pdfBytes, "application/pdf", $"ProfitLoss_{start:yyyyMMdd}_to_{end:yyyyMMdd}.pdf");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting P&L to PDF");
                TempData["Error"] = "Unable to export P&L report to PDF.";
                return RedirectToAction(nameof(ProfitLoss));
            }
        }

        [HttpGet]
        public IActionResult ExportProfitLossExcel(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1);
                var end = endDate ?? DateTime.Now;

                // Calculate revenue
                var riceSalesRevenue = _riceSalesService.GetTotalSalesAmount(start, end);
                var byProductRevenue = _byProductService.GetTotalSalesAmount(start, end);
                var totalRevenue = riceSalesRevenue + byProductRevenue;

                // Calculate expenses
                var cashPayments = _cashBookService.GetTotalPayments(start, end);
                var bankPayments = _bankService.GetTransactionsByDateRange(start, end)
                    .Sum(t => t.Withdrawals);
                var totalExpenses = cashPayments + bankPayments;

                var netProfit = totalRevenue - totalExpenses;

                // Prepare income breakdown
                var incomeBreakdown = new List<(string Category, decimal Amount)>
                {
                    ("Rice Sales", riceSalesRevenue),
                    ("By-Product Sales", byProductRevenue)
                };

                // Prepare expense breakdown
                var expenseBreakdown = new List<(string Category, decimal Amount)>
                {
                    ("Cash Payments", cashPayments),
                    ("Bank Payments", bankPayments)
                };

                var excelBytes = Services.Helpers.ExcelExportHelper.ExportProfitLossToExcel(
                    totalRevenue, totalExpenses, netProfit,
                    incomeBreakdown, expenseBreakdown, start, end);

                return File(excelBytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    $"ProfitLoss_{start:yyyyMMdd}_to_{end:yyyyMMdd}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting P&L to Excel");
                TempData["Error"] = "Unable to export P&L report to Excel.";
                return RedirectToAction(nameof(ProfitLoss));
            }
        }

        [HttpGet]
        public IActionResult ExportCustomReportExcel(string? reportType, DateTime? fromDate, DateTime? toDate)
        {
            try
            {
                var start = fromDate ?? DateTime.Now.AddMonths(-1);
                var end = toDate ?? DateTime.Now;

                List<(DateTime Date, string Customer, string Product, decimal Quantity, decimal Amount)> salesData;

                if (reportType == "sales")
                {
                    var riceSales = _riceSalesService.GetAllSales(true)
                        .Where(s => s.SaleDate >= start && s.SaleDate <= end)
                        .Select(s => (s.SaleDate, s.BuyerName ?? "", s.RiceGrade ?? "", s.Quantity, s.GrossInvoiceAmount))
                        .ToList();

                    salesData = riceSales;
                }
                else if (reportType == "byproduct")
                {
                    var byProductSales = _byProductService.GetAllSales()
                        .Where(s => s.SaleDate >= start && s.SaleDate <= end)
                        .Select(s => (s.SaleDate, s.BuyerName ?? "", s.ProductType ?? "", s.Quantity, s.TotalAmount))
                        .ToList();

                    salesData = byProductSales;
                }
                else
                {
                    // Combined report
                    var riceSales = _riceSalesService.GetAllSales(true)
                        .Where(s => s.SaleDate >= start && s.SaleDate <= end)
                        .Select(s => (s.SaleDate, s.BuyerName ?? "", s.RiceGrade ?? "", s.Quantity, s.GrossInvoiceAmount));

                    var byProductSales = _byProductService.GetAllSales()
                        .Where(s => s.SaleDate >= start && s.SaleDate <= end)
                        .Select(s => (s.SaleDate, s.BuyerName ?? "", s.ProductType ?? "", s.Quantity, s.TotalAmount));

                    salesData = riceSales.Concat(byProductSales).OrderBy(s => s.SaleDate).ToList();
                }

                var reportTitle = reportType == "sales" ? "Rice Sales Report" :
                                  reportType == "byproduct" ? "By-Product Sales Report" :
                                  "Combined Sales Report";

                var excelBytes = Services.Helpers.ExcelExportHelper.ExportSalesToExcel(
                    reportTitle, salesData, start, end);

                return File(excelBytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    $"{reportType ?? "Combined"}SalesReport_{start:yyyyMMdd}_to_{end:yyyyMMdd}.xlsx");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting custom report to Excel");
                TempData["Error"] = "Unable to export custom report to Excel.";
                return RedirectToAction(nameof(CustomReport));
            }
        }

        [HttpGet]
        public IActionResult ExportGSTR1Json(int? month = null, int? year = null)
        {
            try
            {
                var reportMonth = month ?? DateTime.Now.Month;
                var reportYear = year ?? DateTime.Now.Year;
                var startDate = new DateTime(reportYear, reportMonth, 1);
                var endDate = startDate.AddMonths(1).AddDays(-1);

                var sales = _riceSalesService.GetAllSales(true)
                    .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                    .ToList();

                // Create GSTR-1 format JSON
                var gstr1Data = new
                {
                    gstin = "YOUR_GSTIN_HERE",
                    ret_period = $"{reportMonth:D2}{reportYear}",
                    b2b = sales.Where(s => !string.IsNullOrEmpty(s.BuyerGSTIN)).Select(s => new
                    {
                        ctin = s.BuyerGSTIN,
                        inv = new[]
                        {
                            new
                            {
                                inum = s.InvoiceNumber,
                                idt = s.SaleDate.ToString("dd-MM-yyyy"),
                                val = s.GrossInvoiceAmount,
                                pos = "19", // State code - TN for demo
                                rchrg = "N",
                                inv_typ = "R",
                                itms = new[]
                                {
                                    new
                                    {
                                        num = 1,
                                        itm_det = new
                                        {
                                            rt = 5.0m, // GST rate
                                            txval = s.TaxableValue,
                                            iamt = s.IGSTAmount,
                                            camt = s.CGSTAmount,
                                            samt = s.SGSTAmount,
                                            csamt = 0
                                        }
                                    }
                                }
                            }
                        }
                    }).ToList(),
                    b2cl = sales.Where(s => string.IsNullOrEmpty(s.BuyerGSTIN) && s.GrossInvoiceAmount > 250000).Select(s => new
                    {
                        pos = "19",
                        inv = new[]
                        {
                            new
                            {
                                inum = s.InvoiceNumber,
                                idt = s.SaleDate.ToString("dd-MM-yyyy"),
                                val = s.GrossInvoiceAmount,
                                itms = new[]
                                {
                                    new
                                    {
                                        num = 1,
                                        itm_det = new
                                        {
                                            rt = 5.0m,
                                            txval = s.TaxableValue,
                                            iamt = s.IGSTAmount,
                                            camt = s.CGSTAmount,
                                            samt = s.SGSTAmount,
                                            csamt = 0
                                        }
                                    }
                                }
                            }
                        }
                    }).ToList()
                };

                var jsonString = System.Text.Json.JsonSerializer.Serialize(gstr1Data,
                    new System.Text.Json.JsonSerializerOptions { WriteIndented = true });

                var jsonBytes = System.Text.Encoding.UTF8.GetBytes(jsonString);

                return File(jsonBytes, "application/json", $"GSTR1_{reportMonth:D2}_{reportYear}.json");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting GSTR-1 JSON");
                TempData["Error"] = "Unable to export GSTR-1 JSON.";
                return RedirectToAction(nameof(GSTReport));
            }
        }

        #endregion

        #region Production Reports

        public IActionResult ProductionSummary(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? DateTime.Now.AddDays(-30);
                var end = endDate ?? DateTime.Now;

                var batches = _productionBatchService.GetBatchesByDateRange(start, end)
                    .Where(b => b.Status == "Completed")
                    .ToList();

                // Calculate statistics
                var totalBatches = batches.Count;
                var totalInput = batches.Sum(b => _productionBatchService.GetTotalInputQuantity(b.Id));
                var totalOutput = batches.Sum(b => _productionBatchService.GetTotalOutputQuantity(b.Id));
                var avgQualityScore = batches.Any() ? batches.Average(b => b.QualityScore ?? 0) : 0;

                // Group by shift
                var shiftBreakdown = batches.GroupBy(b => b.ShiftType)
                    .Select(g => new {
                        Shift = g.Key,
                        Count = g.Count(),
                        TotalInput = g.Sum(b => _productionBatchService.GetTotalInputQuantity(b.Id)),
                        TotalOutput = g.Sum(b => _productionBatchService.GetTotalOutputQuantity(b.Id))
                    })
                    .ToList();

                // Daily breakdown
                var dailyProduction = batches.GroupBy(b => b.BatchDate.Date)
                    .Select(g => new {
                        Date = g.Key,
                        Count = g.Count(),
                        TotalInput = g.Sum(b => _productionBatchService.GetTotalInputQuantity(b.Id)),
                        TotalOutput = g.Sum(b => _productionBatchService.GetTotalOutputQuantity(b.Id))
                    })
                    .OrderBy(d => d.Date)
                    .ToList();

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.TotalBatches = totalBatches;
                ViewBag.TotalInput = totalInput;
                ViewBag.TotalOutput = totalOutput;
                ViewBag.AvgQualityScore = avgQualityScore;
                ViewBag.ShiftBreakdown = shiftBreakdown;
                ViewBag.DailyProduction = dailyProduction;
                ViewBag.Batches = batches;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating production summary report");
                TempData["Error"] = "Unable to generate production summary.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult DailyProduction(DateTime? date = null)
        {
            try
            {
                var reportDate = date ?? DateTime.Today;

                var batches = _productionBatchService.GetBatchesByDateRange(reportDate, reportDate)
                    .ToList();

                var orders = batches.Where(b => b.ProductionOrderId.HasValue)
                    .Select(b => b.ProductionOrder)
                    .Where(o => o != null)
                    .Distinct()
                    .ToList();

                ViewBag.ReportDate = reportDate.ToString("dd-MMM-yyyy");
                ViewBag.DayName = reportDate.ToString("dddd");
                ViewBag.Batches = batches;
                ViewBag.Orders = orders;
                ViewBag.TotalBatches = batches.Count;
                ViewBag.CompletedBatches = batches.Count(b => b.Status == "Completed");
                ViewBag.InProgressBatches = batches.Count(b => b.Status == "In Progress");
                ViewBag.TotalInput = batches.Sum(b => _productionBatchService.GetTotalInputQuantity(b.Id));
                ViewBag.TotalOutput = batches.Sum(b => _productionBatchService.GetTotalOutputQuantity(b.Id));
                ViewBag.AvgQuality = batches.Any() ? batches.Average(b => b.QualityScore ?? 0) : 0;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating daily production report");
                TempData["Error"] = "Unable to generate daily production report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult MachineUtilization(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? DateTime.Now.AddDays(-30);
                var end = endDate ?? DateTime.Now;

                var machines = _machineService.GetAllMachines();
                var batches = _productionBatchService.GetBatchesByDateRange(start, end)
                    .Where(b => b.Status == "Completed")
                    .ToList();

                var machineStats = machines.Select(m => {
                    var machineBatches = batches.Where(b =>
                        b.ProductionOrder?.AssignedMachineId == m.Id).ToList();

                    var totalHours = machineBatches.Sum(b => b.DurationHours ?? 0);
                    var avgQuality = machineBatches.Any() ? machineBatches.Average(b => b.QualityScore ?? 0) : 0;
                    var totalInput = machineBatches.Sum(b => _productionBatchService.GetTotalInputQuantity(b.Id));
                    var totalOutput = machineBatches.Sum(b => _productionBatchService.GetTotalOutputQuantity(b.Id));

                    return new {
                        Machine = m,
                        BatchCount = machineBatches.Count,
                        TotalHours = totalHours,
                        TotalInput = totalInput,
                        TotalOutput = totalOutput,
                        AvgQuality = avgQuality,
                        Utilization = totalHours > 0 ? (double)(totalHours / ((decimal)(end - start).TotalDays * 24) * 100) : 0
                    };
                }).OrderByDescending(s => s.BatchCount).ToList();

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.MachineStats = machineStats;
                ViewBag.TotalMachines = machines.Count();
                ViewBag.ActiveMachines = machineStats.Count(s => s.BatchCount > 0);

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating machine utilization report");
                TempData["Error"] = "Unable to generate machine utilization report.";
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult ProductionEfficiency(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var start = startDate ?? DateTime.Now.AddDays(-30);
                var end = endDate ?? DateTime.Now;

                var batches = _productionBatchService.GetBatchesByDateRange(start, end)
                    .Where(b => b.Status == "Completed")
                    .ToList();

                var orders = _productionOrderService.GetProductionOrdersByDateRange(start, end)
                    .Where(o => o.Status == "Completed" && o.ActualCompletionDate.HasValue &&
                                o.ActualCompletionDate.Value >= start && o.ActualCompletionDate.Value <= end)
                    .ToList();

                // Efficiency metrics
                var totalPlannedQty = orders.Sum(o => o.TargetQuantity ?? 0);
                var totalActualQty = orders.Sum(o => o.ActualQuantityProduced ?? 0);
                var efficiencyRate = totalPlannedQty > 0 ? (totalActualQty / totalPlannedQty * 100) : 0;

                var onTimeOrders = orders.Count(o => o.ActualCompletionDate <= o.ScheduledDate);
                var onTimeRate = orders.Any() ? (decimal)onTimeOrders / orders.Count * 100 : 0;

                var avgCycleTime = batches.Any() ? batches.Average(b => b.DurationHours ?? 0) : 0;

                // Top performers
                var topBatches = batches.OrderByDescending(b => b.QualityScore).Take(5).ToList();
                var lowBatches = batches.OrderBy(b => b.QualityScore).Take(5).ToList();

                ViewBag.StartDate = start.ToString("dd-MMM-yyyy");
                ViewBag.EndDate = end.ToString("dd-MMM-yyyy");
                ViewBag.TotalOrders = orders.Count;
                ViewBag.TotalBatches = batches.Count;
                ViewBag.PlannedQuantity = totalPlannedQty;
                ViewBag.ActualQuantity = totalActualQty;
                ViewBag.EfficiencyRate = efficiencyRate;
                ViewBag.OnTimeOrders = onTimeOrders;
                ViewBag.OnTimeRate = onTimeRate;
                ViewBag.AvgCycleTime = avgCycleTime;
                ViewBag.TopBatches = topBatches;
                ViewBag.LowBatches = lowBatches;
                ViewBag.Orders = orders;

                return View();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating production efficiency report");
                TempData["Error"] = "Unable to generate production efficiency report.";
                return RedirectToAction(nameof(Index));
            }
        }

        #endregion
    }
}