using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Services.Services
{
    // TASK 4: SALES ORDER APPROVAL WORKFLOW
    public interface IApprovalWorkflowService
    {
        Task<List<SalesOrder>> GetPendingApprovals(string approverRole = "Manager");
        Task<bool> ApproveSalesOrder(int salesOrderId, string approvedBy, string comments);
        Task<bool> RejectSalesOrder(int salesOrderId, string rejectedBy, string reason);
        Task<ApprovalSummary> GetApprovalSummary(string approverRole);
        Task<bool> RequiresApproval(decimal orderAmount);
        Task<List<ApprovalHistory>> GetApprovalHistory(int salesOrderId);
    }

    public class ApprovalWorkflowService : IApprovalWorkflowService
    {
        private readonly ApplicationDbContext _context;
        private readonly IEmailNotificationService _emailService;
        private readonly decimal _approvalThreshold = 100000; // Orders above 1 lakh require approval

        public ApprovalWorkflowService(
            ApplicationDbContext context,
            IEmailNotificationService emailService)
        {
            _context = context;
            _emailService = emailService;
        }

        public async Task<List<SalesOrder>> GetPendingApprovals(string approverRole = "Manager")
        {
            return await _context.SalesOrders
                .Include(so => so.Customer)
                .Include(so => so.SalesOrderItems)
                .Where(so => so.IsActive &&
                           so.Status == "Pending Approval" &&
                           (so.TotalAmount ?? 0) >= _approvalThreshold)
                .OrderBy(so => so.OrderDate)
                .ToListAsync();
        }

        public async Task<bool> ApproveSalesOrder(int salesOrderId, string approvedBy, string comments)
        {
            var salesOrder = await _context.SalesOrders.FindAsync(salesOrderId);
            if (salesOrder == null || salesOrder.Status != "Pending Approval")
                return false;

            salesOrder.Status = "Approved";
            salesOrder.ModifiedDate = DateTime.Now;
            salesOrder.ModifiedBy = approvedBy;

            // Create approval history
            var history = new ApprovalHistory
            {
                EntityType = "SalesOrder",
                EntityId = salesOrderId,
                Action = "Approved",
                ApprovedBy = approvedBy,
                ApprovalDate = DateTime.Now,
                Comments = comments
            };

            _context.ApprovalHistories.Add(history);
            await _context.SaveChangesAsync();

            // Send email notification
            await _emailService.SendCustomEmail(
                "customer@example.com",
                $"Sales Order {salesOrder.OrderNumber} Approved",
                $"Your sales order has been approved and is now in progress."
            );

            return true;
        }

        public async Task<bool> RejectSalesOrder(int salesOrderId, string rejectedBy, string reason)
        {
            var salesOrder = await _context.SalesOrders.FindAsync(salesOrderId);
            if (salesOrder == null || salesOrder.Status != "Pending Approval")
                return false;

            salesOrder.Status = "Rejected";
            salesOrder.ModifiedDate = DateTime.Now;
            salesOrder.ModifiedBy = rejectedBy;

            var history = new ApprovalHistory
            {
                EntityType = "SalesOrder",
                EntityId = salesOrderId,
                Action = "Rejected",
                ApprovedBy = rejectedBy,
                ApprovalDate = DateTime.Now,
                Comments = reason
            };

            _context.ApprovalHistories.Add(history);
            await _context.SaveChangesAsync();

            return true;
        }

        public async Task<ApprovalSummary> GetApprovalSummary(string approverRole)
        {
            var pending = await GetPendingApprovals(approverRole);

            return new ApprovalSummary
            {
                TotalPending = pending.Count,
                TotalValue = pending.Sum(so => so.TotalAmount ?? 0),
                CriticalCount = pending.Count(so => (DateTime.Now - so.OrderDate).Days > 2),
                AverageAge = pending.Any() ? pending.Average(so => (DateTime.Now - so.OrderDate).Days) : 0
            };
        }

        public async Task<bool> RequiresApproval(decimal orderAmount)
        {
            return orderAmount >= _approvalThreshold;
        }

        public async Task<List<ApprovalHistory>> GetApprovalHistory(int salesOrderId)
        {
            return await _context.ApprovalHistories
                .Where(ah => ah.EntityType == "SalesOrder" && ah.EntityId == salesOrderId)
                .OrderByDescending(ah => ah.ApprovalDate)
                .ToListAsync();
        }
    }

    public class ApprovalSummary
    {
        public int TotalPending { get; set; }
        public decimal TotalValue { get; set; }
        public int CriticalCount { get; set; }
        public double AverageAge { get; set; }
    }

    public class ApprovalHistory
    {
        public int Id { get; set; }
        public string EntityType { get; set; } = string.Empty;
        public int EntityId { get; set; }
        public string Action { get; set; } = string.Empty; // Approved, Rejected
        public string ApprovedBy { get; set; } = string.Empty;
        public DateTime ApprovalDate { get; set; }
        public string? Comments { get; set; }
    }
}
