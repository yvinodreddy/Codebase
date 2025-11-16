using RMMS.DataAccess.Repositories.Inventory;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Implementations.Inventory
{
    public class StockAdjustmentService : IStockAdjustmentService
    {
        private readonly IStockAdjustmentRepository _adjustmentRepository;
        private readonly IInventoryLedgerRepository _ledgerRepository;

        public StockAdjustmentService(
            IStockAdjustmentRepository adjustmentRepository,
            IInventoryLedgerRepository ledgerRepository)
        {
            _adjustmentRepository = adjustmentRepository;
            _ledgerRepository = ledgerRepository;
        }

        public List<StockAdjustment> GetAllAdjustments(bool activeOnly = true)
        {
            return _adjustmentRepository.GetAll(activeOnly);
        }

        public StockAdjustment? GetAdjustmentById(int id)
        {
            return _adjustmentRepository.GetById(id);
        }

        public StockAdjustment? GetAdjustmentByCode(string code)
        {
            return _adjustmentRepository.GetByCode(code);
        }

        public List<StockAdjustment> GetAdjustmentsByProduct(int productId)
        {
            return _adjustmentRepository.GetByProduct(productId);
        }

        public List<StockAdjustment> GetAdjustmentsByWarehouse(int warehouseId)
        {
            return _adjustmentRepository.GetByWarehouse(warehouseId);
        }

        public List<StockAdjustment> GetPendingApprovals()
        {
            return _adjustmentRepository.GetPendingApprovals();
        }

        public List<StockAdjustment> GetApprovedAdjustments()
        {
            return _adjustmentRepository.GetApproved();
        }

        public List<StockAdjustment> GetRejectedAdjustments()
        {
            return _adjustmentRepository.GetRejected();
        }

        public List<StockAdjustment> GetAdjustmentsByDateRange(DateTime startDate, DateTime endDate)
        {
            return _adjustmentRepository.GetByDateRange(startDate, endDate);
        }

        public int CreateAdjustment(StockAdjustment adjustment, string createdBy)
        {
            // Validate adjustment
            var validation = ValidateAdjustment(adjustment);
            if (!validation.success)
            {
                throw new InvalidOperationException(validation.message);
            }

            // Get current stock from ledger
            var ledger = _ledgerRepository.GetByProductAndWarehouse(
                adjustment.ProductId,
                adjustment.WarehouseId,
                adjustment.ZoneId);

            if (ledger == null)
            {
                throw new InvalidOperationException("No inventory ledger entry found for this product/warehouse combination");
            }

            // Set before quantity
            adjustment.BeforeQuantity = ledger.CurrentStock;

            // Calculate after quantity based on adjustment type
            switch (adjustment.AdjustmentType)
            {
                case "Increase":
                    adjustment.AfterQuantity = adjustment.BeforeQuantity + adjustment.Quantity;
                    break;
                case "Decrease":
                    adjustment.AfterQuantity = adjustment.BeforeQuantity - adjustment.Quantity;
                    if (adjustment.AfterQuantity < 0)
                    {
                        throw new InvalidOperationException("Adjustment would result in negative stock");
                    }
                    break;
                case "Transfer":
                    adjustment.AfterQuantity = adjustment.Quantity;
                    break;
                default:
                    throw new InvalidOperationException("Invalid adjustment type");
            }

            // Set audit fields
            adjustment.CreatedDate = DateTime.Now;
            adjustment.CreatedBy = createdBy;
            adjustment.IsActive = true;

            // Auto-generate code if not provided
            if (string.IsNullOrEmpty(adjustment.AdjustmentCode))
            {
                adjustment.AdjustmentCode = GenerateAdjustmentCode();
            }

            // If doesn't require approval, auto-approve and update ledger
            if (!adjustment.RequiresApproval)
            {
                adjustment.IsApproved = true;
                adjustment.ApprovedBy = createdBy;
                adjustment.ApprovalDate = DateTime.Now;

                var adjustmentId = _adjustmentRepository.Create(adjustment);
                UpdateInventoryLedger(adjustment);
                return adjustmentId;
            }

            // Otherwise, just create the adjustment (pending approval)
            return _adjustmentRepository.Create(adjustment);
        }

        public bool UpdateAdjustment(StockAdjustment adjustment, string modifiedBy)
        {
            adjustment.ModifiedDate = DateTime.Now;
            adjustment.ModifiedBy = modifiedBy;
            return _adjustmentRepository.Update(adjustment);
        }

        public bool DeleteAdjustment(int id, string deletedBy)
        {
            var adjustment = _adjustmentRepository.GetById(id);
            if (adjustment == null)
                return false;

            // Don't allow deletion of approved adjustments
            if (adjustment.IsApproved)
            {
                throw new InvalidOperationException("Cannot delete an approved adjustment");
            }

            return _adjustmentRepository.Delete(id);
        }

        public bool ApproveAdjustment(int id, string approvedBy, string? remarks = null)
        {
            var adjustment = _adjustmentRepository.GetById(id);
            if (adjustment == null)
                return false;

            if (adjustment.IsApproved)
            {
                throw new InvalidOperationException("Adjustment is already approved");
            }

            if (adjustment.IsRejected)
            {
                throw new InvalidOperationException("Cannot approve a rejected adjustment");
            }

            // Approve the adjustment
            adjustment.IsApproved = true;
            adjustment.ApprovedBy = approvedBy;
            adjustment.ApprovalDate = DateTime.Now;
            adjustment.ApprovalRemarks = remarks;
            adjustment.ModifiedDate = DateTime.Now;
            adjustment.ModifiedBy = approvedBy;

            var success = _adjustmentRepository.Update(adjustment);

            if (success)
            {
                // Update inventory ledger
                UpdateInventoryLedger(adjustment);
            }

            return success;
        }

        public bool RejectAdjustment(int id, string rejectedBy, string reason)
        {
            var adjustment = _adjustmentRepository.GetById(id);
            if (adjustment == null)
                return false;

            if (adjustment.IsApproved)
            {
                throw new InvalidOperationException("Cannot reject an approved adjustment");
            }

            adjustment.IsRejected = true;
            adjustment.RejectionReason = reason;
            adjustment.ModifiedDate = DateTime.Now;
            adjustment.ModifiedBy = rejectedBy;

            return _adjustmentRepository.Update(adjustment);
        }

        public List<StockAdjustment> SearchAdjustments(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllAdjustments();

            return _adjustmentRepository.Search(searchTerm);
        }

        public string GenerateAdjustmentCode()
        {
            return _adjustmentRepository.GenerateAdjustmentCode();
        }

        public (bool success, string message) ValidateAdjustment(StockAdjustment adjustment)
        {
            // Check if product exists
            if (adjustment.ProductId <= 0)
                return (false, "Product is required");

            // Check if warehouse exists
            if (adjustment.WarehouseId <= 0)
                return (false, "Warehouse is required");

            // Check quantity
            if (adjustment.Quantity <= 0)
                return (false, "Quantity must be greater than zero");

            // Check adjustment type
            if (string.IsNullOrWhiteSpace(adjustment.AdjustmentType))
                return (false, "Adjustment type is required");

            // Check reason
            if (string.IsNullOrWhiteSpace(adjustment.Reason))
                return (false, "Reason is required");

            return (true, "Valid");
        }

        private void UpdateInventoryLedger(StockAdjustment adjustment)
        {
            var ledger = _ledgerRepository.GetByProductAndWarehouse(
                adjustment.ProductId,
                adjustment.WarehouseId,
                adjustment.ZoneId);

            if (ledger != null)
            {
                ledger.CurrentStock = adjustment.AfterQuantity;
                ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;
                ledger.LastUpdated = DateTime.Now;
                ledger.ModifiedDate = DateTime.Now;

                _ledgerRepository.Update(ledger);
            }
        }
    }
}
