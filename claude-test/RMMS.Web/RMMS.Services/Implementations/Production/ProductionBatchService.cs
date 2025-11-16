using RMMS.DataAccess.Repositories.Production;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Production
{
    public class ProductionBatchService : IProductionBatchService
    {
        private readonly IProductionBatchRepository _batchRepository;

        public ProductionBatchService(IProductionBatchRepository batchRepository)
        {
            _batchRepository = batchRepository;
        }

        public List<ProductionBatch> GetAllBatches(bool activeOnly = true)
        {
            return _batchRepository.GetAllBatches(activeOnly);
        }

        public ProductionBatch? GetBatchById(int id)
        {
            return _batchRepository.GetBatchById(id);
        }

        public ProductionBatch? GetBatchByNumber(string batchNumber)
        {
            return _batchRepository.GetBatchByNumber(batchNumber);
        }

        public int CreateBatch(ProductionBatch batch, string createdBy)
        {
            // Generate batch number if not provided
            if (string.IsNullOrEmpty(batch.BatchNumber))
            {
                batch.BatchNumber = GenerateBatchNumber();
            }

            // Set audit fields
            batch.CreatedDate = DateTime.Now;
            batch.CreatedBy = createdBy;
            batch.IsActive = true;

            // Set default status if not provided
            if (string.IsNullOrEmpty(batch.Status))
            {
                batch.Status = "Planned";
            }

            return _batchRepository.CreateBatch(batch);
        }

        public bool UpdateBatch(ProductionBatch batch, string modifiedBy)
        {
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;
            return _batchRepository.UpdateBatch(batch);
        }

        public bool DeleteBatch(int id, string deletedBy)
        {
            var batch = _batchRepository.GetBatchById(id);
            if (batch == null) return false;

            // Only allow deletion if batch is in Planned status
            if (batch.Status != "Planned")
            {
                return false;
            }

            batch.IsActive = false;
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = deletedBy;
            return _batchRepository.UpdateBatch(batch);
        }

        public List<ProductionBatch> GetBatchesByStatus(string status)
        {
            return _batchRepository.GetBatchesByStatus(status);
        }

        public List<ProductionBatch> GetBatchesByShift(string shiftType)
        {
            return _batchRepository.GetBatchesByShift(shiftType);
        }

        public List<ProductionBatch> GetBatchesByProductionOrder(int productionOrderId)
        {
            return _batchRepository.GetBatchesByProductionOrder(productionOrderId);
        }

        public List<ProductionBatch> GetBatchesByDateRange(DateTime startDate, DateTime endDate)
        {
            return _batchRepository.GetBatchesByDateRange(startDate, endDate);
        }

        public List<ProductionBatch> GetBatchesByOperator(int operatorId)
        {
            return _batchRepository.GetBatchesByOperator(operatorId);
        }

        public List<ProductionBatch> GetBatchesBySupervisor(int supervisorId)
        {
            return _batchRepository.GetBatchesBySupervisor(supervisorId);
        }

        public List<ProductionBatch> GetInProgressBatches()
        {
            return _batchRepository.GetInProgressBatches();
        }

        public List<ProductionBatch> GetCompletedBatches()
        {
            return _batchRepository.GetCompletedBatches();
        }

        public List<ProductionBatch> GetPendingVerificationBatches()
        {
            return _batchRepository.GetPendingVerificationBatches();
        }

        public List<ProductionBatch> SearchBatches(string searchTerm)
        {
            return _batchRepository.SearchBatches(searchTerm);
        }

        public ProductionBatch? GetBatchWithDetails(int id)
        {
            return _batchRepository.GetBatchWithDetails(id);
        }

        public List<ProductionBatch> GetBatchesWithDetails(bool activeOnly = true)
        {
            return _batchRepository.GetBatchesWithDetails(activeOnly);
        }

        public bool StartBatch(int batchId, string modifiedBy)
        {
            var batch = _batchRepository.GetBatchById(batchId);
            if (batch == null) return false;

            // Only allow starting if batch is in Planned status
            if (batch.Status != "Planned")
            {
                return false;
            }

            batch.Status = "In Progress";
            batch.StartTime = DateTime.Now;
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;

            return _batchRepository.UpdateBatch(batch);
        }

        public bool CompleteBatch(int batchId, decimal qualityScore, string? qualityRemarks, string modifiedBy)
        {
            var batch = _batchRepository.GetBatchById(batchId);
            if (batch == null) return false;

            // Only allow completion if batch is In Progress
            if (batch.Status != "In Progress")
            {
                return false;
            }

            batch.Status = "Completed";
            batch.EndTime = DateTime.Now;
            batch.CompletionPercent = 100;
            batch.QualityScore = qualityScore;
            batch.QualityRemarks = qualityRemarks;
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;

            return _batchRepository.UpdateBatch(batch);
        }

        public bool VerifyBatch(int batchId, string modifiedBy)
        {
            var batch = _batchRepository.GetBatchWithDetails(batchId);
            if (batch == null) return false;

            // Only allow verification if batch is Completed
            if (batch.Status != "Completed")
            {
                return false;
            }

            // Verify that yield record exists and is verified
            if (batch.YieldRecord == null || !batch.YieldRecord.IsVerified)
            {
                return false;
            }

            batch.Status = "Verified";
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;

            return _batchRepository.UpdateBatch(batch);
        }

        public bool CancelBatch(int batchId, string reason, string modifiedBy)
        {
            var batch = _batchRepository.GetBatchById(batchId);
            if (batch == null) return false;

            // Can only cancel Planned or In Progress batches
            if (batch.Status != "Planned" && batch.Status != "In Progress")
            {
                return false;
            }

            batch.Status = "Cancelled";
            batch.Issues = reason;
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;

            return _batchRepository.UpdateBatch(batch);
        }

        public bool UpdateProgress(int batchId, decimal completionPercent, string modifiedBy)
        {
            var batch = _batchRepository.GetBatchById(batchId);
            if (batch == null) return false;

            // Only update progress if batch is In Progress
            if (batch.Status != "In Progress")
            {
                return false;
            }

            batch.CompletionPercent = completionPercent;
            batch.ModifiedDate = DateTime.Now;
            batch.ModifiedBy = modifiedBy;

            return _batchRepository.UpdateBatch(batch);
        }

        public bool AddBatchInput(int batchId, BatchInput input)
        {
            // This will be implemented with inventory integration
            // For now, just a placeholder
            return true;
        }

        public bool AddBatchOutput(int batchId, BatchOutput output)
        {
            // This will be implemented with inventory integration
            // For now, just a placeholder
            return true;
        }

        public List<BatchInput> GetBatchInputs(int batchId)
        {
            var batch = _batchRepository.GetBatchWithDetails(batchId);
            return batch?.Inputs.ToList() ?? new List<BatchInput>();
        }

        public List<BatchOutput> GetBatchOutputs(int batchId)
        {
            var batch = _batchRepository.GetBatchWithDetails(batchId);
            return batch?.Outputs.ToList() ?? new List<BatchOutput>();
        }

        public bool CalculateYield(int batchId, string calculatedBy)
        {
            var batch = _batchRepository.GetBatchWithDetails(batchId);
            if (batch == null) return false;

            // Can only calculate yield for Completed batches
            if (batch.Status != "Completed")
            {
                return false;
            }

            // Ensure we have inputs and outputs
            if (!batch.Inputs.Any() || !batch.Outputs.Any())
            {
                return false;
            }

            // Create yield record if it doesn't exist
            if (batch.YieldRecord == null)
            {
                batch.YieldRecord = new YieldRecord
                {
                    BatchId = batch.Id,
                    CalculatedDate = DateTime.Now,
                    CalculatedBy = calculatedBy
                };
            }

            // Calculate yield from batch data
            var totalInput = batch.Inputs.Sum(i => i.Quantity);
            var headRice = batch.Outputs.Where(o => o.OutputType == "Rice" && o.Grade != "Broken").Sum(o => o.Quantity);
            var brokenRice = batch.Outputs.Where(o => o.OutputType == "Rice" && o.Grade == "Broken").Sum(o => o.Quantity);
            var bran = batch.Outputs.Where(o => o.OutputType == "Bran").Sum(o => o.Quantity);
            var husk = batch.Outputs.Where(o => o.OutputType == "Husk").Sum(o => o.Quantity);

            batch.YieldRecord.InputPaddyQuantity = totalInput;
            batch.YieldRecord.OutputHeadRice = headRice;
            batch.YieldRecord.OutputBrokenRice = brokenRice;
            batch.YieldRecord.OutputBran = bran;
            batch.YieldRecord.OutputHusk = husk;

            // Calculate yields using the model's method
            batch.YieldRecord.CalculateYields();

            // Update batch
            return _batchRepository.UpdateBatch(batch);
        }

        public YieldRecord? GetBatchYield(int batchId)
        {
            var batch = _batchRepository.GetBatchWithDetails(batchId);
            return batch?.YieldRecord;
        }

        public string GenerateBatchNumber()
        {
            return _batchRepository.GenerateBatchNumber();
        }

        public int GetTotalBatchesCount()
        {
            return _batchRepository.GetTotalBatchesCount();
        }

        public int GetInProgressBatchesCount()
        {
            return _batchRepository.GetInProgressBatchesCount();
        }

        public int GetCompletedBatchesCount()
        {
            return _batchRepository.GetCompletedBatchesCount();
        }

        public int GetTodayBatchesCount()
        {
            return _batchRepository.GetTodayBatchesCount();
        }

        public decimal GetTotalInputQuantity(int batchId)
        {
            return _batchRepository.GetTotalInputQuantity(batchId);
        }

        public decimal GetTotalOutputQuantity(int batchId)
        {
            return _batchRepository.GetTotalOutputQuantity(batchId);
        }

        public decimal GetBatchEfficiency(int batchId)
        {
            var totalInput = GetTotalInputQuantity(batchId);
            var totalOutput = GetTotalOutputQuantity(batchId);

            if (totalInput == 0) return 0;

            return (totalOutput / totalInput) * 100;
        }
    }
}
