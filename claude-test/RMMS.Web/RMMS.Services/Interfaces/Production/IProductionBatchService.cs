using RMMS.Models.Production;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Production
{
    public interface IProductionBatchService
    {
        // Basic CRUD operations
        List<ProductionBatch> GetAllBatches(bool activeOnly = true);
        ProductionBatch? GetBatchById(int id);
        ProductionBatch? GetBatchByNumber(string batchNumber);
        int CreateBatch(ProductionBatch batch, string createdBy);
        bool UpdateBatch(ProductionBatch batch, string modifiedBy);
        bool DeleteBatch(int id, string deletedBy);

        // Query operations
        List<ProductionBatch> GetBatchesByStatus(string status);
        List<ProductionBatch> GetBatchesByShift(string shiftType);
        List<ProductionBatch> GetBatchesByProductionOrder(int productionOrderId);
        List<ProductionBatch> GetBatchesByDateRange(DateTime startDate, DateTime endDate);
        List<ProductionBatch> GetBatchesByOperator(int operatorId);
        List<ProductionBatch> GetBatchesBySupervisor(int supervisorId);
        List<ProductionBatch> GetInProgressBatches();
        List<ProductionBatch> GetCompletedBatches();
        List<ProductionBatch> GetPendingVerificationBatches();
        List<ProductionBatch> SearchBatches(string searchTerm);

        // Batch with details
        ProductionBatch? GetBatchWithDetails(int id);
        List<ProductionBatch> GetBatchesWithDetails(bool activeOnly = true);

        // Batch workflow operations
        bool StartBatch(int batchId, string modifiedBy);
        bool CompleteBatch(int batchId, decimal qualityScore, string? qualityRemarks, string modifiedBy);
        bool VerifyBatch(int batchId, string modifiedBy);
        bool CancelBatch(int batchId, string reason, string modifiedBy);
        bool UpdateProgress(int batchId, decimal completionPercent, string modifiedBy);

        // Batch inputs/outputs management
        bool AddBatchInput(int batchId, BatchInput input);
        bool AddBatchOutput(int batchId, BatchOutput output);
        List<BatchInput> GetBatchInputs(int batchId);
        List<BatchOutput> GetBatchOutputs(int batchId);

        // Yield operations
        bool CalculateYield(int batchId, string calculatedBy);
        YieldRecord? GetBatchYield(int batchId);

        // Code generation
        string GenerateBatchNumber();

        // Statistics
        int GetTotalBatchesCount();
        int GetInProgressBatchesCount();
        int GetCompletedBatchesCount();
        int GetTodayBatchesCount();
        decimal GetTotalInputQuantity(int batchId);
        decimal GetTotalOutputQuantity(int batchId);
        decimal GetBatchEfficiency(int batchId);
    }
}
