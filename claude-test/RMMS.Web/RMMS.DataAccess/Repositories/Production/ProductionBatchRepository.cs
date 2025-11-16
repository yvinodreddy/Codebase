using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Production
{
    public class ProductionBatchRepository : IProductionBatchRepository
    {
        private readonly ApplicationDbContext _context;

        public ProductionBatchRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<ProductionBatch> GetAllBatches(bool activeOnly = true)
        {
            var query = _context.ProductionBatches.AsQueryable();

            if (activeOnly)
            {
                query = query.Where(b => b.IsActive);
            }

            return query
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ThenBy(b => b.BatchNumber)
                .ToList();
        }

        public ProductionBatch? GetBatchById(int id)
        {
            return _context.ProductionBatches
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .FirstOrDefault(b => b.Id == id);
        }

        public ProductionBatch? GetBatchByNumber(string batchNumber)
        {
            return _context.ProductionBatches
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .FirstOrDefault(b => b.BatchNumber == batchNumber);
        }

        public int CreateBatch(ProductionBatch batch)
        {
            _context.ProductionBatches.Add(batch);
            _context.SaveChanges();
            return batch.Id;
        }

        public bool UpdateBatch(ProductionBatch batch)
        {
            _context.ProductionBatches.Update(batch);
            return _context.SaveChanges() > 0;
        }

        public bool DeleteBatch(int id)
        {
            var batch = GetBatchById(id);
            if (batch == null) return false;

            batch.IsActive = false;
            batch.ModifiedDate = DateTime.Now;
            return UpdateBatch(batch);
        }

        public List<ProductionBatch> GetBatchesByStatus(string status)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive && b.Status == status)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetBatchesByShift(string shiftType)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive && b.ShiftType == shiftType)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetBatchesByProductionOrder(int productionOrderId)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive && b.ProductionOrderId == productionOrderId)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderBy(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetBatchesByDateRange(DateTime startDate, DateTime endDate)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive &&
                           b.BatchDate >= startDate &&
                           b.BatchDate <= endDate)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetBatchesByOperator(int operatorId)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive && b.OperatorId == operatorId)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetBatchesBySupervisor(int supervisorId)
        {
            return _context.ProductionBatches
                .Where(b => b.IsActive && b.SupervisorId == supervisorId)
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public List<ProductionBatch> GetInProgressBatches()
        {
            return GetBatchesByStatus("In Progress");
        }

        public List<ProductionBatch> GetCompletedBatches()
        {
            return GetBatchesByStatus("Completed");
        }

        public List<ProductionBatch> GetPendingVerificationBatches()
        {
            return GetBatchesByStatus("Completed")
                .Where(b => b.YieldRecord == null || !b.YieldRecord.IsVerified)
                .ToList();
        }

        public List<ProductionBatch> SearchBatches(string searchTerm)
        {
            var lowerSearchTerm = searchTerm.ToLower();
            return _context.ProductionBatches
                .Where(b => b.IsActive &&
                           (b.BatchNumber.ToLower().Contains(lowerSearchTerm) ||
                            (b.ProductionOrder != null && b.ProductionOrder.OrderNumber.ToLower().Contains(lowerSearchTerm)) ||
                            (b.Operator != null && b.Operator.EmployeeName.ToLower().Contains(lowerSearchTerm)) ||
                            (b.Supervisor != null && b.Supervisor.EmployeeName.ToLower().Contains(lowerSearchTerm))))
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public ProductionBatch? GetBatchWithDetails(int id)
        {
            return _context.ProductionBatches
                .Include(b => b.ProductionOrder)
                    .ThenInclude(po => po!.PaddyProduct)
                .Include(b => b.ProductionOrder)
                    .ThenInclude(po => po!.TargetRiceProduct)
                .Include(b => b.ProductionOrder)
                    .ThenInclude(po => po!.AssignedMachine)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .Include(b => b.Inputs)
                    .ThenInclude(i => i.Product)
                .Include(b => b.Inputs)
                    .ThenInclude(i => i.Warehouse)
                .Include(b => b.Outputs)
                    .ThenInclude(o => o.Product)
                .Include(b => b.Outputs)
                    .ThenInclude(o => o.Warehouse)
                .Include(b => b.YieldRecord)
                .FirstOrDefault(b => b.Id == id);
        }

        public List<ProductionBatch> GetBatchesWithDetails(bool activeOnly = true)
        {
            var query = _context.ProductionBatches.AsQueryable();

            if (activeOnly)
            {
                query = query.Where(b => b.IsActive);
            }

            return query
                .Include(b => b.ProductionOrder)
                .Include(b => b.Operator)
                .Include(b => b.Supervisor)
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Include(b => b.YieldRecord)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }

        public string GenerateBatchNumber()
        {
            var lastBatch = _context.ProductionBatches
                .OrderByDescending(b => b.Id)
                .FirstOrDefault();

            if (lastBatch == null)
            {
                return "BATCH0001";
            }

            // Extract number from last code (e.g., BATCH0001 -> 0001)
            var lastCode = lastBatch.BatchNumber;
            var numberPart = lastCode.Substring(5); // Skip "BATCH"

            if (int.TryParse(numberPart, out int lastNumber))
            {
                var newNumber = lastNumber + 1;
                return $"BATCH{newNumber:D4}";
            }

            return "BATCH0001";
        }

        public int GetTotalBatchesCount()
        {
            return _context.ProductionBatches.Count(b => b.IsActive);
        }

        public int GetInProgressBatchesCount()
        {
            return _context.ProductionBatches.Count(b => b.IsActive && b.Status == "In Progress");
        }

        public int GetCompletedBatchesCount()
        {
            return _context.ProductionBatches.Count(b => b.IsActive && b.Status == "Completed");
        }

        public int GetTodayBatchesCount()
        {
            var today = DateTime.Today;
            return _context.ProductionBatches.Count(b => b.IsActive && b.BatchDate.Date == today);
        }

        public decimal GetTotalInputQuantity(int batchId)
        {
            return _context.BatchInputs
                .Where(i => i.BatchId == batchId)
                .Sum(i => i.Quantity);
        }

        public decimal GetTotalOutputQuantity(int batchId)
        {
            return _context.BatchOutputs
                .Where(o => o.BatchId == batchId)
                .Sum(o => o.Quantity);
        }

        public List<ProductionBatch> GetBatchesWithYieldRecords()
        {
            return _context.ProductionBatches
                .Include(b => b.YieldRecord)
                .Include(b => b.ProductionOrder)
                    .ThenInclude(po => po!.AssignedMachine)
                .Where(b => b.YieldRecord != null)
                .OrderByDescending(b => b.BatchDate)
                .ToList();
        }
    }
}
