using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using RMMS.Models.Masters;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RMMS.Services.Services
{
    // ================================================================
    // TASK 5: AUTOMATED INVOICE GENERATION
    // ================================================================
    public interface IInvoiceGenerationService
    {
        Task<Invoice> GenerateInvoiceFromSalesOrder(int salesOrderId);
        Task<Invoice?> GetInvoice(int invoiceId);
        Task<List<Invoice>> GetCustomerInvoices(int customerId);
        Task<byte[]> GenerateInvoicePDF(int invoiceId);
        Task<bool> SendInvoiceEmail(int invoiceId);
        Task<InvoiceStats> GetInvoiceStatistics();
    }

    public class InvoiceGenerationService : IInvoiceGenerationService
    {
        private readonly ApplicationDbContext _context;
        private readonly IEmailNotificationService _emailService;

        public InvoiceGenerationService(
            ApplicationDbContext context,
            IEmailNotificationService emailService)
        {
            _context = context;
            _emailService = emailService;
        }

        public async Task<Invoice> GenerateInvoiceFromSalesOrder(int salesOrderId)
        {
            var salesOrder = await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .FirstOrDefaultAsync(so => so.Id == salesOrderId);

            if (salesOrder == null)
                throw new Exception("Sales order not found");

            // Generate invoice number
            var lastInvoice = await _context.Invoices
                .OrderByDescending(i => i.Id)
                .FirstOrDefaultAsync();

            var invoiceNumber = $"INV-{DateTime.Now:yyyy}-{(lastInvoice?.Id ?? 0) + 1:D5}";

            var invoice = new Invoice
            {
                InvoiceNumber = invoiceNumber,
                InvoiceDate = DateTime.Now,
                SalesOrderId = salesOrderId,
                CustomerId = salesOrder.CustomerId,
                SubtotalAmount = salesOrder.TotalAmount ?? 0,
                TaxAmount = (salesOrder.TotalAmount ?? 0) * 0.18m, // 18% GST
                TotalAmount = (salesOrder.TotalAmount ?? 0) * 1.18m,
                DueDate = DateTime.Now.AddDays(30),
                Status = "Generated",
                CreatedDate = DateTime.Now
            };

            _context.Invoices.Add(invoice);
            await _context.SaveChangesAsync();

            // Update sales order
            salesOrder.Status = "Invoiced";
            await _context.SaveChangesAsync();

            return invoice;
        }

        public async Task<Invoice?> GetInvoice(int invoiceId)
        {
            return await _context.Invoices
                .Include(i => i.Customer)
                .Include(i => i.SalesOrder)
                .FirstOrDefaultAsync(i => i.Id == invoiceId);
        }

        public async Task<List<Invoice>> GetCustomerInvoices(int customerId)
        {
            return await _context.Invoices
                .Where(i => i.CustomerId == customerId)
                .OrderByDescending(i => i.InvoiceDate)
                .ToListAsync();
        }

        public async Task<byte[]> GenerateInvoicePDF(int invoiceId)
        {
            // TODO: Implement PDF generation using library like iTextSharp or DinkToPdf
            // Placeholder implementation
            return Array.Empty<byte>();
        }

        public async Task<bool> SendInvoiceEmail(int invoiceId)
        {
            var invoice = await GetInvoice(invoiceId);
            if (invoice == null) return false;

            return await _emailService.SendInvoice(invoiceId);
        }

        public async Task<InvoiceStats> GetInvoiceStatistics()
        {
            var today = DateTime.Today;
            var thisMonth = new DateTime(today.Year, today.Month, 1);

            return new InvoiceStats
            {
                TotalInvoices = await _context.Invoices.CountAsync(),
                ThisMonthInvoices = await _context.Invoices.CountAsync(i => i.InvoiceDate >= thisMonth),
                TotalValue = await _context.Invoices.SumAsync(i => i.TotalAmount),
                PendingPayments = await _context.Invoices.CountAsync(i => i.Status != "Paid"),
                OverdueInvoices = await _context.Invoices.CountAsync(i => i.DueDate < today && i.Status != "Paid")
            };
        }
    }

    // ================================================================
    // TASK 7: SALES PERFORMANCE ANALYTICS
    // ================================================================
    public interface ISalesAnalyticsService
    {
        Task<SalespersonPerformance> GetSalespersonPerformance(int employeeId, DateTime startDate, DateTime endDate);
        Task<List<SalespersonPerformance>> GetTeamPerformance(DateTime startDate, DateTime endDate);
        Task<SalesTargetAnalysis> GetTargetAnalysis(int employeeId);
        Task<List<TopProduct>> GetTopSellingProducts(DateTime startDate, DateTime endDate, int top = 10);
        Task<List<TopCustomer>> GetTopCustomers(DateTime startDate, DateTime endDate, int top = 10);
    }

    public class SalesAnalyticsService : ISalesAnalyticsService
    {
        private readonly ApplicationDbContext _context;

        public SalesAnalyticsService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<SalespersonPerformance> GetSalespersonPerformance(
            int employeeId, DateTime startDate, DateTime endDate)
        {
            var riceSales = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .ToListAsync();

            var totalSales = riceSales.Sum(rs => rs.GrossInvoiceAmount);
            var totalOrders = riceSales.Count;

            return new SalespersonPerformance
            {
                EmployeeId = employeeId,
                TotalSales = totalSales,
                TotalOrders = totalOrders,
                AverageOrderValue = totalOrders > 0 ? totalSales / totalOrders : 0,
                StartDate = startDate,
                EndDate = endDate
            };
        }

        public async Task<List<SalespersonPerformance>> GetTeamPerformance(
            DateTime startDate, DateTime endDate)
        {
            var employees = await _context.Employees
                .Where(e => e.IsActive && e.Department == "Sales")
                .ToListAsync();

            var performances = new List<SalespersonPerformance>();
            foreach (var emp in employees)
            {
                var perf = await GetSalespersonPerformance(emp.Id, startDate, endDate);
                performances.Add(perf);
            }

            return performances.OrderByDescending(p => p.TotalSales).ToList();
        }

        public async Task<SalesTargetAnalysis> GetTargetAnalysis(int employeeId)
        {
            var thisMonth = new DateTime(DateTime.Today.Year, DateTime.Today.Month, 1);
            var performance = await GetSalespersonPerformance(employeeId, thisMonth, DateTime.Today);

            // Get target (placeholder - should come from SalesTarget table)
            var monthlyTarget = 500000m;

            return new SalesTargetAnalysis
            {
                EmployeeId = employeeId,
                Target = monthlyTarget,
                Achievement = performance.TotalSales,
                AchievementPercentage = (performance.TotalSales / monthlyTarget) * 100,
                Shortfall = monthlyTarget - performance.TotalSales,
                Status = performance.TotalSales >= monthlyTarget ? "Achieved" : "In Progress"
            };
        }

        public async Task<List<TopProduct>> GetTopSellingProducts(
            DateTime startDate, DateTime endDate, int top = 10)
        {
            var products = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .GroupBy(rs => rs.RiceGrade)
                .Select(g => new TopProduct
                {
                    ProductName = g.Key,
                    TotalQuantity = g.Sum(rs => rs.Quantity),
                    TotalValue = g.Sum(rs => rs.GrossInvoiceAmount),
                    OrderCount = g.Count()
                })
                .OrderByDescending(p => p.TotalValue)
                .Take(top)
                .ToListAsync();

            return products;
        }

        public async Task<List<TopCustomer>> GetTopCustomers(
            DateTime startDate, DateTime endDate, int top = 10)
        {
            var customers = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .GroupBy(rs => rs.CustomerId)
                .Select(g => new TopCustomer
                {
                    CustomerId = g.Key,
                    TotalPurchases = g.Sum(rs => rs.GrossInvoiceAmount),
                    OrderCount = g.Count(),
                    AverageOrderValue = g.Average(rs => rs.GrossInvoiceAmount)
                })
                .OrderByDescending(c => c.TotalPurchases)
                .Take(top)
                .ToListAsync();

            return customers;
        }
    }

    // ================================================================
    // TASK 8: COMMISSION CALCULATION
    // ================================================================
    public interface ICommissionCalculationService
    {
        Task<decimal> CalculateCommission(int employeeId, DateTime month);
        Task<List<CommissionDetail>> GetCommissionDetails(int employeeId, DateTime startDate, DateTime endDate);
        Task<CommissionStructure?> GetCommissionStructure(int employeeId);
        Task<bool> UpdateCommissionStructure(CommissionStructure structure);
    }

    public class CommissionCalculationService : ICommissionCalculationService
    {
        private readonly ApplicationDbContext _context;

        public CommissionCalculationService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<decimal> CalculateCommission(int employeeId, DateTime month)
        {
            var startDate = new DateTime(month.Year, month.Month, 1);
            var endDate = startDate.AddMonths(1).AddDays(-1);

            var structure = await GetCommissionStructure(employeeId);
            if (structure == null) return 0;

            var sales = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .SumAsync(rs => rs.GrossInvoiceAmount);

            decimal commission = 0;

            if (structure.CalculationType == "Percentage")
            {
                commission = sales * (structure.CommissionRate / 100);
            }
            else if (structure.CalculationType == "Flat")
            {
                commission = structure.FlatAmount ?? 0;
            }
            else if (structure.CalculationType == "Tiered")
            {
                // Tiered calculation
                if (sales >= 1000000) commission = sales * 0.05m; // 5% above 10 lakh
                else if (sales >= 500000) commission = sales * 0.03m; // 3% above 5 lakh
                else commission = sales * 0.02m; // 2% below 5 lakh
            }

            return commission;
        }

        public async Task<List<CommissionDetail>> GetCommissionDetails(
            int employeeId, DateTime startDate, DateTime endDate)
        {
            var sales = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .ToListAsync();

            var structure = await GetCommissionStructure(employeeId);
            var commissionRate = structure?.CommissionRate ?? 0;

            return sales.Select(s => new CommissionDetail
            {
                SaleId = s.Id,
                SaleDate = s.SaleDate,
                SaleAmount = s.GrossInvoiceAmount,
                CommissionRate = commissionRate,
                CommissionAmount = s.GrossInvoiceAmount * (commissionRate / 100)
            }).ToList();
        }

        public async Task<CommissionStructure?> GetCommissionStructure(int employeeId)
        {
            return await _context.CommissionStructures
                .FirstOrDefaultAsync(cs => cs.EmployeeId == employeeId);
        }

        public async Task<bool> UpdateCommissionStructure(CommissionStructure structure)
        {
            _context.CommissionStructures.Update(structure);
            await _context.SaveChangesAsync();
            return true;
        }
    }

    // ================================================================
    // TASK 9: SALES TARGET TRACKING
    // ================================================================
    public interface ISalesTargetService
    {
        Task<bool> SetTarget(SalesTarget target);
        Task<SalesTarget?> GetTarget(int employeeId, DateTime month);
        Task<List<SalesTarget>> GetTeamTargets(DateTime month);
        Task<TargetAchievement> GetAchievement(int employeeId, DateTime month);
        Task<List<TargetAchievement>> GetTeamAchievements(DateTime month);
    }

    public class SalesTargetService : ISalesTargetService
    {
        private readonly ApplicationDbContext _context;

        public SalesTargetService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<bool> SetTarget(SalesTarget target)
        {
            _context.SalesTargets.Add(target);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<SalesTarget?> GetTarget(int employeeId, DateTime month)
        {
            var startDate = new DateTime(month.Year, month.Month, 1);
            return await _context.SalesTargets
                .FirstOrDefaultAsync(st => st.EmployeeId == employeeId &&
                                         st.TargetMonth == startDate);
        }

        public async Task<List<SalesTarget>> GetTeamTargets(DateTime month)
        {
            var startDate = new DateTime(month.Year, month.Month, 1);
            return await _context.SalesTargets
                .Where(st => st.TargetMonth == startDate)
                .ToListAsync();
        }

        public async Task<TargetAchievement> GetAchievement(int employeeId, DateTime month)
        {
            var target = await GetTarget(employeeId, month);
            if (target == null)
                return new TargetAchievement { EmployeeId = employeeId };

            var startDate = new DateTime(month.Year, month.Month, 1);
            var endDate = startDate.AddMonths(1).AddDays(-1);

            var actualSales = await _context.RiceSales
                .Where(rs => rs.IsActive &&
                           rs.SaleDate >= startDate &&
                           rs.SaleDate <= endDate)
                .SumAsync(rs => rs.GrossInvoiceAmount);

            return new TargetAchievement
            {
                EmployeeId = employeeId,
                TargetAmount = target.TargetAmount,
                AchievedAmount = actualSales,
                AchievementPercentage = (actualSales / target.TargetAmount) * 100,
                Status = actualSales >= target.TargetAmount ? "Achieved" : "In Progress"
            };
        }

        public async Task<List<TargetAchievement>> GetTeamAchievements(DateTime month)
        {
            var targets = await GetTeamTargets(month);
            var achievements = new List<TargetAchievement>();

            foreach (var target in targets)
            {
                var achievement = await GetAchievement(target.EmployeeId, month);
                achievements.Add(achievement);
            }

            return achievements.OrderByDescending(a => a.AchievementPercentage).ToList();
        }
    }

    // ================================================================
    // TASK 10: MULTI-CURRENCY SUPPORT
    // ================================================================
    public interface IMultiCurrencyService
    {
        Task<decimal> ConvertAmount(decimal amount, string fromCurrency, string toCurrency);
        Task<ExchangeRate?> GetExchangeRate(string fromCurrency, string toCurrency);
        Task<bool> UpdateExchangeRate(ExchangeRate rate);
        Task<List<Currency>> GetSupportedCurrencies();
    }

    public class MultiCurrencyService : IMultiCurrencyService
    {
        private readonly ApplicationDbContext _context;

        public MultiCurrencyService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<decimal> ConvertAmount(decimal amount, string fromCurrency, string toCurrency)
        {
            if (fromCurrency == toCurrency)
                return amount;

            var rate = await GetExchangeRate(fromCurrency, toCurrency);
            if (rate == null)
                throw new Exception($"Exchange rate not found for {fromCurrency} to {toCurrency}");

            return amount * rate.Rate;
        }

        public async Task<ExchangeRate?> GetExchangeRate(string fromCurrency, string toCurrency)
        {
            return await _context.ExchangeRates
                .FirstOrDefaultAsync(er => er.FromCurrency == fromCurrency &&
                                         er.ToCurrency == toCurrency &&
                                         er.IsActive);
        }

        public async Task<bool> UpdateExchangeRate(ExchangeRate rate)
        {
            _context.ExchangeRates.Update(rate);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<List<Currency>> GetSupportedCurrencies()
        {
            return await _context.Currencies
                .Where(c => c.IsActive)
                .ToListAsync();
        }
    }

    // ================================================================
    // SUPPORTING MODELS
    // ================================================================

    [Table("Invoices")]
    public class Invoice
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(20)]
        public string InvoiceNumber { get; set; } = string.Empty;

        [Required]
        public DateTime InvoiceDate { get; set; }

        public int SalesOrderId { get; set; }
        public int CustomerId { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal SubtotalAmount { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal TaxAmount { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal TotalAmount { get; set; }

        public DateTime DueDate { get; set; }

        [StringLength(20)]
        public string Status { get; set; } = "Generated"; // Generated, Sent, Paid, Overdue

        public SalesOrder? SalesOrder { get; set; }
        public Customer? Customer { get; set; }

        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }

    [Table("CommissionStructures")]
    public class CommissionStructure
    {
        [Key]
        public int Id { get; set; }
        public int EmployeeId { get; set; }

        [StringLength(20)]
        public string CalculationType { get; set; } = "Percentage"; // Percentage, Flat, Tiered

        [Column(TypeName = "decimal(5,2)")]
        public decimal CommissionRate { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal? FlatAmount { get; set; }

        public bool IsActive { get; set; } = true;
    }

    [Table("SalesTargets")]
    public class SalesTarget
    {
        [Key]
        public int Id { get; set; }
        public int EmployeeId { get; set; }
        public DateTime TargetMonth { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal TargetAmount { get; set; }

        public DateTime CreatedDate { get; set; } = DateTime.Now;
    }

    [Table("Currencies")]
    public class Currency
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(3)]
        public string CurrencyCode { get; set; } = string.Empty; // INR, USD, EUR

        [Required]
        [StringLength(50)]
        public string CurrencyName { get; set; } = string.Empty;

        [StringLength(5)]
        public string Symbol { get; set; } = string.Empty; // ₹, $, €

        public bool IsActive { get; set; } = true;
    }

    [Table("ExchangeRates")]
    public class ExchangeRate
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(3)]
        public string FromCurrency { get; set; } = string.Empty;

        [Required]
        [StringLength(3)]
        public string ToCurrency { get; set; } = string.Empty;

        [Column(TypeName = "decimal(18,6)")]
        public decimal Rate { get; set; }

        public DateTime EffectiveDate { get; set; } = DateTime.Now;
        public bool IsActive { get; set; } = true;
    }

    // DTOs and Response Models
    public class InvoiceStats
    {
        public int TotalInvoices { get; set; }
        public int ThisMonthInvoices { get; set; }
        public decimal TotalValue { get; set; }
        public int PendingPayments { get; set; }
        public int OverdueInvoices { get; set; }
    }

    public class SalespersonPerformance
    {
        public int EmployeeId { get; set; }
        public decimal TotalSales { get; set; }
        public int TotalOrders { get; set; }
        public decimal AverageOrderValue { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
    }

    public class SalesTargetAnalysis
    {
        public int EmployeeId { get; set; }
        public decimal Target { get; set; }
        public decimal Achievement { get; set; }
        public decimal AchievementPercentage { get; set; }
        public decimal Shortfall { get; set; }
        public string Status { get; set; } = string.Empty;
    }

    public class TopProduct
    {
        public string ProductName { get; set; } = string.Empty;
        public decimal TotalQuantity { get; set; }
        public decimal TotalValue { get; set; }
        public int OrderCount { get; set; }
    }

    public class TopCustomer
    {
        public int CustomerId { get; set; }
        public decimal TotalPurchases { get; set; }
        public int OrderCount { get; set; }
        public decimal AverageOrderValue { get; set; }
    }

    public class CommissionDetail
    {
        public int SaleId { get; set; }
        public DateTime SaleDate { get; set; }
        public decimal SaleAmount { get; set; }
        public decimal CommissionRate { get; set; }
        public decimal CommissionAmount { get; set; }
    }

    public class TargetAchievement
    {
        public int EmployeeId { get; set; }
        public decimal TargetAmount { get; set; }
        public decimal AchievedAmount { get; set; }
        public decimal AchievementPercentage { get; set; }
        public string Status { get; set; } = string.Empty;
    }
}
