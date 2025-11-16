using RMMS.Models.Production;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Production
{
    public interface IProductionBatchRepository
    {
        // Basic CRUD operations
        List<ProductionBatch> GetAllBatches(bool activeOnly = true);
        ProductionBatch? GetBatchById(int id);
        ProductionBatch? GetBatchByNumber(string batchNumber);
        int CreateBatch(ProductionBatch batch);
        bool UpdateBatch(ProductionBatch batch);
        bool DeleteBatch(int id);

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

        // Code generation
        string GenerateBatchNumber();

        // Statistics
        int GetTotalBatchesCount();
        int GetInProgressBatchesCount();
        int GetCompletedBatchesCount();
        int GetTodayBatchesCount();
        decimal GetTotalInputQuantity(int batchId);
        decimal GetTotalOutputQuantity(int batchId);

        // Yield Analysis
        List<ProductionBatch> GetBatchesWithYieldRecords();
    }
}
