using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;

namespace RMMS.Web.Controllers
{
    [Authorize]
    public class AnalyticsController : Controller
    {
        private readonly ApplicationDbContext _context;

        public AnalyticsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // =============================================================================
        // MAIN ANALYTICS DASHBOARD (Executive)
        // =============================================================================
        public async Task<IActionResult> Index()
        {
            try
            {
                var data = new
                {
                    TotalCustomers = await _context.Customers.CountAsync(c => c.IsActive),
                    TotalProducts = await _context.Products.CountAsync(p => p.IsActive),
                    TotalEmployees = await _context.Employees.CountAsync(e => e.IsActive),
                    TotalWarehouses = await _context.Warehouses.CountAsync(w => w.IsActive),
                    TotalMachines = await _context.Machines.CountAsync(m => m.IsActive),
                    TotalSalesOrders = await _context.SalesOrders.CountAsync(s => s.IsActive),
                    TotalQuotations = await _context.Quotations.CountAsync(q => q.IsActive),
                    TotalProductionBatches = await _context.ProductionBatches.CountAsync(p => p.IsActive)
                };

                ViewBag.Data = data;
                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading analytics dashboard: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // EXECUTIVE DASHBOARD (Alias for Index)
        // =============================================================================
        public Task<IActionResult> Executive()
        {
            return Index();
        }

        // =============================================================================
        // PRODUCTION ANALYTICS
        // =============================================================================
        public async Task<IActionResult> Production(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;

                var batches = await _context.ProductionBatches
                    .Where(b => b.IsActive && b.BatchDate >= start && b.BatchDate <= end)
                    .Include(b => b.ProductionOrder)
                    .AsNoTracking().ToListAsync();

                var machines = await _context.Machines
                    .Where(m => m.IsActive)
                    .AsNoTracking().ToListAsync();

                var data = new
                {
                    TotalBatches = batches.Count,
                    CompletedBatches = batches.Count(b => b.Status == "Completed"),
                    InProgressBatches = batches.Count(b => b.Status == "In Progress"),
                    PlannedBatches = batches.Count(b => b.Status == "Planned"),
                    TotalMachines = machines.Count,
                    ActiveMachines = machines.Count(m => m.Status == "Active"),
                    TotalInputQty = batches.Sum(b => b.TotalInputQuantity),
                    TotalOutputQty = batches.Sum(b => b.TotalOutputQuantity),
                    Batches = batches.OrderByDescending(b => b.BatchDate).Take(10).ToList(),
                    Machines = machines
                };

                ViewBag.Data = data;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading production analytics: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // INVENTORY ANALYTICS
        // =============================================================================
        public async Task<IActionResult> Inventory()
        {
            try
            {
                var products = await _context.Products
                    .Where(p => p.IsActive)
                    .AsNoTracking().ToListAsync();

                var warehouses = await _context.Warehouses
                    .Where(w => w.IsActive)
                    .AsNoTracking().ToListAsync();

                var stockMovements = await _context.StockMovements
                    .Where(m => m.IsActive && m.MovementDate >= DateTime.Today.AddDays(-30))
                    .OrderByDescending(m => m.MovementDate)
                    .Take(20)
                    .Include(m => m.Product)
                    .Include(m => m.Warehouse)
                    .AsNoTracking().ToListAsync();

                var stockAdjustments = await _context.StockAdjustments
                    .Where(a => a.IsActive && a.AdjustmentDate >= DateTime.Today.AddDays(-30))
                    .OrderByDescending(a => a.AdjustmentDate)
                    .Take(20)
                    .Include(a => a.Product)
                    .Include(a => a.Warehouse)
                    .AsNoTracking().ToListAsync();

                var data = new
                {
                    TotalProducts = products.Count,
                    TotalWarehouses = warehouses.Count,
                    RecentMovements = stockMovements.Count,
                    RecentAdjustments = stockAdjustments.Count,
                    Products = products,
                    Warehouses = warehouses,
                    StockMovements = stockMovements,
                    StockAdjustments = stockAdjustments
                };

                ViewBag.Data = data;
                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inventory analytics: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // SALES ANALYTICS
        // =============================================================================
        public async Task<IActionResult> Sales(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;

                var salesOrders = await _context.SalesOrders
                    .Where(s => s.IsActive && s.OrderDate >= start && s.OrderDate <= end)
                    .Include(s => s.Customer)
                    .OrderByDescending(s => s.OrderDate)
                    .AsNoTracking().ToListAsync();

                var quotations = await _context.Quotations
                    .Where(q => q.IsActive && q.QuotationDate >= start && q.QuotationDate <= end)
                    .Include(q => q.Customer)
                    .OrderByDescending(q => q.QuotationDate)
                    .AsNoTracking().ToListAsync();

                var inquiries = await _context.Inquiries
                    .Where(i => i.IsActive && i.InquiryDate >= start && i.InquiryDate <= end)
                    .Include(i => i.Customer)
                    .OrderByDescending(i => i.InquiryDate)
                    .AsNoTracking().ToListAsync();

                var data = new
                {
                    TotalSalesOrders = salesOrders.Count,
                    TotalSalesAmount = salesOrders.Sum(s => s.TotalAmount),
                    PendingSalesOrders = salesOrders.Count(s => s.Status == "Pending"),
                    CompletedSalesOrders = salesOrders.Count(s => s.Status == "Completed"),
                    TotalQuotations = quotations.Count,
                    TotalQuotationAmount = quotations.Sum(q => q.TotalAmount),
                    TotalInquiries = inquiries.Count,
                    SalesOrders = salesOrders.Take(10).ToList(),
                    Quotations = quotations.Take(10).ToList(),
                    Inquiries = inquiries.Take(10).ToList()
                };

                ViewBag.Data = data;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading sales analytics: {ex.Message}";
                return View();
            }
        }

        // =============================================================================
        // FINANCIAL ANALYTICS
        // =============================================================================
        public async Task<IActionResult> Financial(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;

                var cashBook = await _context.CashBooks
                    .Where(c => c.IsActive && c.TransactionDate >= start && c.TransactionDate <= end)
                    .OrderByDescending(c => c.TransactionDate)
                    .AsNoTracking().ToListAsync();

                var bankTransactions = await _context.BankTransactions
                    .Where(b => b.IsActive && b.TransactionDate >= start && b.TransactionDate <= end)
                    .OrderByDescending(b => b.TransactionDate)
                    .AsNoTracking().ToListAsync();

                var vouchers = await _context.Vouchers
                    .Where(v => v.IsActive && v.VoucherDate >= start && v.VoucherDate <= end)
                    .OrderByDescending(v => v.VoucherDate)
                    .AsNoTracking().ToListAsync();

                var data = new
                {
                    TotalCashReceipts = cashBook.Sum(c => c.Receipts),
                    TotalCashPayments = cashBook.Sum(c => c.Payments),
                    CashBalance = cashBook.OrderByDescending(c => c.TransactionDate).FirstOrDefault()?.Balance ?? 0,
                    TotalBankDeposits = bankTransactions.Sum(b => b.Deposits),
                    TotalBankWithdrawals = bankTransactions.Sum(b => b.Withdrawals),
                    BankBalance = bankTransactions.OrderByDescending(b => b.TransactionDate).FirstOrDefault()?.Balance ?? 0,
                    TotalVouchers = vouchers.Count,
                    TotalVoucherAmount = vouchers.Sum(v => v.Amount),
                    CashTransactions = cashBook.Take(10).ToList(),
                    BankTransactions = bankTransactions.Take(10).ToList(),
                    Vouchers = vouchers.Take(10).ToList()
                };

                ViewBag.Data = data;
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

        // =============================================================================
        // SUPPLIERS ANALYTICS
        // =============================================================================
        public async Task<IActionResult> Suppliers(DateTime? startDate, DateTime? endDate)
        {
            try
            {
                var start = startDate ?? DateTime.Today.AddDays(-30);
                var end = endDate ?? DateTime.Today;

                var vendors = await _context.Vendors
                    .Where(v => v.IsActive)
                    .Include(v => v.Contacts)
                    .AsNoTracking().ToListAsync();

                var paddyProcurements = await _context.PaddyProcurements
                    .Where(p => p.IsActive && p.ReceiptDate >= start && p.ReceiptDate <= end)
                    .OrderByDescending(p => p.ReceiptDate)
                    .AsNoTracking().ToListAsync();

                var data = new
                {
                    TotalVendors = vendors.Count,
                    ActiveVendors = vendors.Count(v => v.Status == "Active"),
                    TotalProcurements = paddyProcurements.Count,
                    TotalProcurementQty = paddyProcurements.Sum(p => p.QuantityReceived),
                    TotalProcurementValue = paddyProcurements.Sum(p => p.TotalNetWeight), // Using TotalNetWeight as proxy for value
                    Vendors = vendors.Take(10).ToList(),
                    RecentProcurements = paddyProcurements.Take(10).ToList()
                };

                ViewBag.Data = data;
                ViewBag.StartDate = start;
                ViewBag.EndDate = end;
                return View();
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading suppliers analytics: {ex.Message}";
                return View();
            }
        }
    }
}
