using RMMS.Models.Masters;
using RMMS.Models.Sales;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Services.Services
{
    public interface ICreditManagementService
    {
        Task<decimal> GetCustomerCreditUtilization(int customerId);
        Task<decimal> GetAvailableCredit(int customerId);
        Task<bool> CheckCreditLimitExceeded(int customerId, decimal orderAmount);
        Task<CreditStatus> GetCustomerCreditStatus(int customerId);
        Task<List<Customer>> GetCustomersExceedingCreditLimit();
        Task<bool> ValidateOrderAgainstCreditLimit(int customerId, decimal orderAmount);
        Task<CreditLimitAlert> GenerateCreditAlert(int customerId);
    }

    public class CreditManagementService : ICreditManagementService
    {
        private readonly ApplicationDbContext _context;

        public CreditManagementService(ApplicationDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// Get total outstanding amount for a customer
        /// </summary>
        public async Task<decimal> GetCustomerCreditUtilization(int customerId)
        {
            // Get outstanding from Rice Sales
            var riceSalesOutstanding = await _context.RiceSales
                .Where(r => r.CustomerId == customerId &&
                           r.IsActive &&
                           r.PaymentStatus != "Paid" &&
                           r.PaymentStatus != "Completed")
                .SumAsync(r => r.GrossInvoiceAmount - (r.AmountPaid ?? 0));

            // Get outstanding from By-Product Sales
            var byProductOutstanding = await _context.ByProductSales
                .Where(b => b.CustomerId == customerId &&
                           b.IsActive &&
                           b.PaymentStatus != "Paid" &&
                           b.PaymentStatus != "Completed")
                .SumAsync(b => b.TotalAmount - (b.AmountPaid ?? 0));

            // Get outstanding from External Rice Sales
            var externalSalesOutstanding = await _context.ExternalRiceSales
                .Where(e => e.CustomerId == customerId &&
                           e.IsActive &&
                           e.PaymentStatus != "Paid" &&
                           e.PaymentStatus != "Completed")
                .SumAsync(e => e.TotalAmount - (e.AmountPaid ?? 0));

            // Get pending Sales Orders
            var salesOrdersPending = await _context.SalesOrders
                .Where(s => s.CustomerId == customerId &&
                           s.IsActive &&
                           s.Status != "Completed" &&
                           s.Status != "Cancelled")
                .SumAsync(s => s.TotalAmount ?? 0);

            return riceSalesOutstanding + byProductOutstanding +
                   externalSalesOutstanding + salesOrdersPending;
        }

        /// <summary>
        /// Calculate available credit for a customer
        /// </summary>
        public async Task<decimal> GetAvailableCredit(int customerId)
        {
            var customer = await _context.Customers.FindAsync(customerId);

            if (customer == null || customer.CreditLimit == null || customer.CreditLimit == 0)
            {
                return 0; // No credit facility
            }

            var utilized = await GetCustomerCreditUtilization(customerId);
            var available = customer.CreditLimit.Value - utilized;

            return available > 0 ? available : 0;
        }

        /// <summary>
        /// Check if credit limit will be exceeded with new order
        /// </summary>
        public async Task<bool> CheckCreditLimitExceeded(int customerId, decimal orderAmount)
        {
            var customer = await _context.Customers.FindAsync(customerId);

            if (customer == null || customer.CreditLimit == null || customer.CreditLimit == 0)
            {
                return false; // No credit limit set, allow transaction
            }

            var currentUtilization = await GetCustomerCreditUtilization(customerId);
            var newTotal = currentUtilization + orderAmount;

            return newTotal > customer.CreditLimit.Value;
        }

        /// <summary>
        /// Get comprehensive credit status for a customer
        /// </summary>
        public async Task<CreditStatus> GetCustomerCreditStatus(int customerId)
        {
            var customer = await _context.Customers
                .Include(c => c.Contacts)
                .FirstOrDefaultAsync(c => c.Id == customerId);

            if (customer == null)
            {
                return new CreditStatus { CustomerName = "Unknown", Status = "Not Found" };
            }

            var utilized = await GetCustomerCreditUtilization(customerId);
            var available = await GetAvailableCredit(customerId);
            var creditLimit = customer.CreditLimit ?? 0;

            var utilizationPercentage = creditLimit > 0 ? (utilized / creditLimit) * 100 : 0;

            string status = "Good";
            if (utilizationPercentage >= 100)
                status = "Exceeded";
            else if (utilizationPercentage >= 90)
                status = "Critical";
            else if (utilizationPercentage >= 75)
                status = "Warning";

            return new CreditStatus
            {
                CustomerId = customer.Id,
                CustomerCode = customer.CustomerCode,
                CustomerName = customer.CustomerName,
                CreditLimit = creditLimit,
                CreditUtilized = utilized,
                AvailableCredit = available,
                UtilizationPercentage = utilizationPercentage,
                Status = status,
                CreditDays = customer.CreditDays ?? 0,
                CustomerStatus = customer.Status,
                PrimaryContact = customer.Contacts?.FirstOrDefault(c => c.IsPrimary)?.ContactPerson ?? "N/A",
                PrimaryEmail = customer.Contacts?.FirstOrDefault(c => c.IsPrimary)?.Email ?? "N/A"
            };
        }

        /// <summary>
        /// Get list of customers exceeding credit limit
        /// </summary>
        public async Task<List<Customer>> GetCustomersExceedingCreditLimit()
        {
            var customersWithCredit = await _context.Customers
                .Where(c => c.IsActive && c.CreditLimit != null && c.CreditLimit > 0)
                .ToListAsync();

            var exceedingCustomers = new List<Customer>();

            foreach (var customer in customersWithCredit)
            {
                var utilized = await GetCustomerCreditUtilization(customer.Id);
                if (utilized > customer.CreditLimit.Value)
                {
                    exceedingCustomers.Add(customer);
                }
            }

            return exceedingCustomers;
        }

        /// <summary>
        /// Validate order amount against customer credit limit
        /// </summary>
        public async Task<bool> ValidateOrderAgainstCreditLimit(int customerId, decimal orderAmount)
        {
            var customer = await _context.Customers.FindAsync(customerId);

            // If no credit limit set, allow the transaction
            if (customer == null || customer.CreditLimit == null || customer.CreditLimit == 0)
            {
                return true;
            }

            // If customer is blocked, don't allow
            if (customer.Status == "Blocked")
            {
                return false;
            }

            var willExceed = await CheckCreditLimitExceeded(customerId, orderAmount);
            return !willExceed;
        }

        /// <summary>
        /// Generate credit limit alert for a customer
        /// </summary>
        public async Task<CreditLimitAlert> GenerateCreditAlert(int customerId)
        {
            var status = await GetCustomerCreditStatus(customerId);

            var alert = new CreditLimitAlert
            {
                CustomerId = status.CustomerId,
                CustomerCode = status.CustomerCode,
                CustomerName = status.CustomerName,
                AlertType = status.Status == "Exceeded" ? "Limit Exceeded" :
                           status.Status == "Critical" ? "Near Limit" :
                           status.Status == "Warning" ? "Warning" : "Normal",
                CreditLimit = status.CreditLimit,
                CreditUtilized = status.CreditUtilized,
                AvailableCredit = status.AvailableCredit,
                UtilizationPercentage = status.UtilizationPercentage,
                AlertDate = DateTime.Now,
                RequiresAction = status.Status == "Exceeded" || status.Status == "Critical",
                RecommendedAction = GetRecommendedAction(status),
                PrimaryContact = status.PrimaryContact,
                PrimaryEmail = status.PrimaryEmail
            };

            return alert;
        }

        private string GetRecommendedAction(CreditStatus status)
        {
            if (status.Status == "Exceeded")
                return "Block further orders until payment received. Contact customer immediately.";
            else if (status.Status == "Critical")
                return "Notify customer to clear outstanding dues. Consider payment before next order.";
            else if (status.Status == "Warning")
                return "Send reminder for upcoming payment. Monitor closely.";
            else
                return "No action required. Continue normal operations.";
        }
    }

    // Supporting classes
    public class CreditStatus
    {
        public int CustomerId { get; set; }
        public string CustomerCode { get; set; } = string.Empty;
        public string CustomerName { get; set; } = string.Empty;
        public decimal CreditLimit { get; set; }
        public decimal CreditUtilized { get; set; }
        public decimal AvailableCredit { get; set; }
        public decimal UtilizationPercentage { get; set; }
        public string Status { get; set; } = string.Empty; // Good, Warning, Critical, Exceeded
        public int CreditDays { get; set; }
        public string CustomerStatus { get; set; } = string.Empty;
        public string PrimaryContact { get; set; } = string.Empty;
        public string PrimaryEmail { get; set; } = string.Empty;
    }

    public class CreditLimitAlert
    {
        public int CustomerId { get; set; }
        public string CustomerCode { get; set; } = string.Empty;
        public string CustomerName { get; set; } = string.Empty;
        public string AlertType { get; set; } = string.Empty;
        public decimal CreditLimit { get; set; }
        public decimal CreditUtilized { get; set; }
        public decimal AvailableCredit { get; set; }
        public decimal UtilizationPercentage { get; set; }
        public DateTime AlertDate { get; set; }
        public bool RequiresAction { get; set; }
        public string RecommendedAction { get; set; } = string.Empty;
        public string PrimaryContact { get; set; } = string.Empty;
        public string PrimaryEmail { get; set; } = string.Empty;
    }
}
