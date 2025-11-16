using RMMS.DataAccess.Repositories.Inventory;
using RMMS.Models.Inventory;
using RMMS.Services.Interfaces.Inventory;
using System;
using System.Collections.Generic;

namespace RMMS.Services.Implementations.Inventory
{
    public class StockMovementService : IStockMovementService
    {
        private readonly IStockMovementRepository _movementRepository;
        private readonly IInventoryLedgerRepository _ledgerRepository;

        public StockMovementService(
            IStockMovementRepository movementRepository,
            IInventoryLedgerRepository ledgerRepository)
        {
            _movementRepository = movementRepository;
            _ledgerRepository = ledgerRepository;
        }

        public List<StockMovement> GetAllMovements(bool activeOnly = true)
        {
            return _movementRepository.GetAll(activeOnly);
        }

        public StockMovement? GetMovementById(int id)
        {
            return _movementRepository.GetById(id);
        }

        public StockMovement? GetMovementByCode(string code)
        {
            return _movementRepository.GetByCode(code);
        }

        public List<StockMovement> GetMovementsByProduct(int productId)
        {
            return _movementRepository.GetByProduct(productId);
        }

        public List<StockMovement> GetMovementsByWarehouse(int warehouseId)
        {
            return _movementRepository.GetByWarehouse(warehouseId);
        }

        public List<StockMovement> GetMovementsByDateRange(DateTime startDate, DateTime endDate)
        {
            return _movementRepository.GetByDateRange(startDate, endDate);
        }

        public List<StockMovement> GetMovementsByType(string movementType)
        {
            return _movementRepository.GetByType(movementType);
        }

        public List<StockMovement> GetMovementsByCategory(string category)
        {
            return _movementRepository.GetByCategory(category);
        }

        public List<StockMovement> GetRecentMovements(int count = 10)
        {
            return _movementRepository.GetRecentMovements(count);
        }

        public int CreateMovement(StockMovement movement, string createdBy)
        {
            // Validate movement
            var validation = ValidateMovement(movement);
            if (!validation.success)
            {
                throw new InvalidOperationException(validation.message);
            }

            // Set audit fields
            movement.CreatedDate = DateTime.Now;
            movement.CreatedBy = createdBy;
            movement.IsActive = true;

            // Auto-generate code if not provided
            if (string.IsNullOrEmpty(movement.MovementCode))
            {
                movement.MovementCode = GenerateMovementCode();
            }

            // Calculate total cost
            movement.TotalCost = movement.Quantity * movement.UnitCost;

            // Create the movement
            var movementId = _movementRepository.Create(movement);

            // Update inventory ledger
            UpdateInventoryLedger(movement);

            return movementId;
        }

        public bool UpdateMovement(StockMovement movement, string modifiedBy)
        {
            movement.ModifiedDate = DateTime.Now;
            movement.ModifiedBy = modifiedBy;

            // Recalculate total cost
            movement.TotalCost = movement.Quantity * movement.UnitCost;

            return _movementRepository.Update(movement);
        }

        public bool DeleteMovement(int id, string deletedBy)
        {
            // Note: Deleting a movement should potentially reverse the ledger entry
            // For now, we'll just soft delete
            return _movementRepository.Delete(id);
        }

        public List<StockMovement> SearchMovements(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllMovements();

            return _movementRepository.Search(searchTerm);
        }

        public string GenerateMovementCode()
        {
            return _movementRepository.GenerateMovementCode();
        }

        public (bool success, string message) ValidateMovement(StockMovement movement)
        {
            // Check if product exists
            if (movement.ProductId <= 0)
                return (false, "Product is required");

            // Check if warehouse exists
            if (movement.WarehouseId <= 0)
                return (false, "Warehouse is required");

            // Check quantity
            if (movement.Quantity <= 0)
                return (false, "Quantity must be greater than zero");

            // For OUT movements, check if sufficient stock exists
            if (movement.MovementType == "OUT")
            {
                var ledger = _ledgerRepository.GetByProductAndWarehouse(
                    movement.ProductId,
                    movement.WarehouseId,
                    movement.ZoneId);

                if (ledger == null)
                {
                    return (false, "No inventory ledger entry found for this product/warehouse combination");
                }

                if (ledger.CurrentStock < movement.Quantity)
                {
                    return (false, $"Insufficient stock. Available: {ledger.CurrentStock}, Required: {movement.Quantity}");
                }
            }

            return (true, "Valid");
        }

        private void UpdateInventoryLedger(StockMovement movement)
        {
            // Get or create ledger entry
            var ledger = _ledgerRepository.GetByProductAndWarehouse(
                movement.ProductId,
                movement.WarehouseId,
                movement.ZoneId);

            if (ledger == null)
            {
                // Create new ledger entry for IN movements
                if (movement.MovementType == "IN")
                {
                    ledger = new InventoryLedger
                    {
                        ProductId = movement.ProductId,
                        WarehouseId = movement.WarehouseId,
                        ZoneId = movement.ZoneId,
                        CurrentStock = movement.Quantity,
                        MinimumLevel = 0,
                        MaximumLevel = 0,
                        ReorderLevel = 0,
                        UnitCost = movement.UnitCost,
                        TotalValue = movement.Quantity * movement.UnitCost,
                        LastMovementDate = movement.MovementDate,
                        CreatedDate = DateTime.Now,
                        IsActive = true
                    };
                    _ledgerRepository.Create(ledger);
                }
            }
            else
            {
                // Update existing ledger
                if (movement.MovementType == "IN")
                {
                    ledger.CurrentStock += movement.Quantity;
                }
                else if (movement.MovementType == "OUT")
                {
                    ledger.CurrentStock -= movement.Quantity;
                }

                // Update cost (weighted average)
                if (movement.MovementType == "IN" && ledger.CurrentStock > 0)
                {
                    ledger.UnitCost = ((ledger.TotalValue + movement.TotalCost) / ledger.CurrentStock);
                }

                ledger.TotalValue = ledger.CurrentStock * ledger.UnitCost;
                ledger.LastMovementDate = movement.MovementDate;
                ledger.LastUpdated = DateTime.Now;
                ledger.ModifiedDate = DateTime.Now;

                _ledgerRepository.Update(ledger);
            }
        }
    }
}
