using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Inventory
{
    public interface IStockAdjustmentRepository
    {
        List<StockAdjustment> GetAll(bool activeOnly = true);
        StockAdjustment? GetById(int id);
        StockAdjustment? GetByCode(string code);
        List<StockAdjustment> GetByProduct(int productId);
        List<StockAdjustment> GetByWarehouse(int warehouseId);
        List<StockAdjustment> GetPendingApprovals();
        List<StockAdjustment> GetApproved();
        List<StockAdjustment> GetRejected();
        List<StockAdjustment> GetByDateRange(DateTime startDate, DateTime endDate);
        int Create(StockAdjustment adjustment);
        bool Update(StockAdjustment adjustment);
        bool Delete(int id);
        List<StockAdjustment> Search(string searchTerm);
        string GenerateAdjustmentCode();
    }
}
