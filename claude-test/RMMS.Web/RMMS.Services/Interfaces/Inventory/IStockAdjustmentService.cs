using RMMS.Models.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Inventory
{
    public interface IStockAdjustmentService
    {
        List<StockAdjustment> GetAllAdjustments(bool activeOnly = true);
        StockAdjustment? GetAdjustmentById(int id);
        StockAdjustment? GetAdjustmentByCode(string code);
        List<StockAdjustment> GetAdjustmentsByProduct(int productId);
        List<StockAdjustment> GetAdjustmentsByWarehouse(int warehouseId);
        List<StockAdjustment> GetPendingApprovals();
        List<StockAdjustment> GetApprovedAdjustments();
        List<StockAdjustment> GetRejectedAdjustments();
        List<StockAdjustment> GetAdjustmentsByDateRange(DateTime startDate, DateTime endDate);
        int CreateAdjustment(StockAdjustment adjustment, string createdBy);
        bool UpdateAdjustment(StockAdjustment adjustment, string modifiedBy);
        bool DeleteAdjustment(int id, string deletedBy);
        bool ApproveAdjustment(int id, string approvedBy, string? remarks = null);
        bool RejectAdjustment(int id, string rejectedBy, string reason);
        List<StockAdjustment> SearchAdjustments(string searchTerm);
        string GenerateAdjustmentCode();
        (bool success, string message) ValidateAdjustment(StockAdjustment adjustment);
    }
}
