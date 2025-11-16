// RMMS.Services/PaddyProcurementService.cs
using System;
using System.Collections.Generic;
using System.Data;
using RMMS.DataAccess.Repositories;
using RMMS.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Data.SqlClient;

namespace RMMS.Services
{
    public interface IPaddyProcurementService
    {
        List<PaddyProcurement> GetAllProcurements(bool activeOnly = true);
        PaddyProcurement? GetProcurementById(int id);
        int CreateProcurement(PaddyProcurement model, string username);
        bool UpdateProcurement(PaddyProcurement model, string username);
        bool DeleteProcurement(int id, string username);
        List<PaddyProcurement> SearchProcurements(string supplierName, string variety, DateTime? startDate, DateTime? endDate, string voucherNumber);
        DataTable GetStockSummaryReport();
        string GenerateNewVoucherNumber();
        decimal CalculateClosingStock(decimal? openingStock, decimal quantityReceived, decimal? issues);
        decimal? CalculateLossShrinkage(decimal? closingStock, decimal? weightPerBag, decimal totalNetWeight);
    }

    public class PaddyProcurementService : IPaddyProcurementService
    {
        private readonly IPaddyProcurementRepository _repository;

        public PaddyProcurementService(IConfiguration configuration)
        {
            _repository = new PaddyProcurementRepository(configuration);
        }

        public List<PaddyProcurement> GetAllProcurements(bool activeOnly = true)
        {
            try
            {
                return _repository.GetAll(activeOnly) ?? new List<PaddyProcurement>();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving procurements: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving procurements: {ex.Message}", ex);
            }
        }

        public PaddyProcurement? GetProcurementById(int id)
        {
            try
            {
                return _repository.GetById(id);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving procurement with ID {id}: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving procurement with ID {id}: {ex.Message}", ex);
            }
        }

        public int CreateProcurement(PaddyProcurement model, string username)
        {
            try
            {
                // Business logic validations
                if (model.QuantityReceived <= 0)
                {
                    throw new ArgumentException("Quantity received must be greater than zero.");
                }

                if (model.TotalNetWeight <= 0)
                {
                    throw new ArgumentException("Total net weight must be greater than zero.");
                }

                // Auto-generate voucher number if not provided
                if (string.IsNullOrEmpty(model.VoucherNumber))
                {
                    model.VoucherNumber = GenerateNewVoucherNumber();
                }

                // Calculate closing stock if not provided
                if (model.ClosingStock == null)
                {
                    model.ClosingStock = CalculateClosingStock(model.OpeningStock, model.QuantityReceived, model.Issues);
                }

                // Calculate loss/shrinkage if applicable
                if (model.LossShrinkage == null)
                {
                    model.LossShrinkage = CalculateLossShrinkage(model.ClosingStock, model.WeightPerBag, model.TotalNetWeight);
                }

                model.CreatedBy = username;
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;

                return _repository.Insert(model);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error creating procurement: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error creating procurement: {ex.Message}", ex);
            }
        }

        public bool UpdateProcurement(PaddyProcurement model, string username)
        {
            try
            {
                // Validate that the record exists
                var existing = _repository.GetById(model.Id);
                if (existing == null)
                {
                    throw new ArgumentException($"Procurement record with ID {model.Id} not found.");
                }

                // Business logic validations
                if (model.QuantityReceived <= 0)
                {
                    throw new ArgumentException("Quantity received must be greater than zero.");
                }

                // Recalculate closing stock
                model.ClosingStock = CalculateClosingStock(model.OpeningStock, model.QuantityReceived, model.Issues);

                // Recalculate loss/shrinkage
                model.LossShrinkage = CalculateLossShrinkage(model.ClosingStock, model.WeightPerBag, model.TotalNetWeight);

                model.ModifiedBy = username;
                model.ModifiedDate = DateTime.Now;

                return _repository.Update(model);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error updating procurement with ID {model.Id}: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error updating procurement with ID {model.Id}: {ex.Message}", ex);
            }
        }

        public bool DeleteProcurement(int id, string username)
        {
            try
            {
                // Validate that the record exists
                var existing = _repository.GetById(id);
                if (existing == null)
                {
                    throw new ArgumentException($"Procurement record with ID {id} not found.");
                }

                // Additional business logic checks before deletion
                // For example, check if this procurement has related transactions

                return _repository.Delete(id, username);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error deleting procurement with ID {id}: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error deleting procurement with ID {id}: {ex.Message}", ex);
            }
        }

        public List<PaddyProcurement> SearchProcurements(string supplierName, string variety, DateTime? startDate, DateTime? endDate, string voucherNumber)
        {
            try
            {
                return _repository.Search(supplierName, variety, startDate, endDate, voucherNumber) ?? new List<PaddyProcurement>();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error searching procurements: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error searching procurements: {ex.Message}", ex);
            }
        }

        public DataTable GetStockSummaryReport()
        {
            try
            {
                return _repository.GetStockSummary();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving stock summary report: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving stock summary report: {ex.Message}", ex);
            }
        }

        public string GenerateNewVoucherNumber()
        {
            try
            {
                return _repository.GenerateVoucherNumber();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error generating voucher number: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error generating voucher number: {ex.Message}", ex);
            }
        }

        public decimal CalculateClosingStock(decimal? openingStock, decimal quantityReceived, decimal? issues)
        {
            decimal opening = openingStock ?? 0;
            decimal issued = issues ?? 0;
            return opening + quantityReceived - issued;
        }

        public decimal? CalculateLossShrinkage(decimal? closingStock, decimal? weightPerBag, decimal totalNetWeight)
        {
            if (closingStock.HasValue && weightPerBag.HasValue && weightPerBag.Value > 0)
            {
                decimal expectedWeight = closingStock.Value * weightPerBag.Value;
                return expectedWeight - totalNetWeight;
            }
            return null;
        }
    }
}