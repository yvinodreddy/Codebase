// =====================================================
// SERVICE IMPLEMENTATIONS
// =====================================================

// RMMS.Services/RiceSalesService.cs
using System;
using System.Collections.Generic;
using RMMS.DataAccess.Repositories;
using RMMS.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Data.SqlClient;

namespace RMMS.Services
{
    public interface IRiceSalesService
    {
        // Existing methods from your original implementation
        List<RiceSales> GetAllSales(bool activeOnly = true);
        RiceSales? GetSaleById(int id);
        int CreateSale(RiceSales model, string username);
        bool UpdateSale(RiceSales model, string username);
        bool DeleteSale(int id, string username);
        List<RiceSales> SearchSalesByCustomer(string customerName);
        List<RiceSales> GetPendingPayments();
        decimal CalculateTaxableValue(decimal totalValue, decimal discount);
        decimal CalculateGrossAmount(RiceSales model);
        string GenerateNewInvoiceNumber();
        GSTCalculation CalculateGST(decimal taxableValue, string buyerState, string sellerState);

        // Methods that were missing and causing your errors
        public decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate) => 0m;
        public List<RiceSales> GetSalesByDateRange(DateTime startDate, DateTime endDate) => new List<RiceSales>();
    }

    public class RiceSalesService : IRiceSalesService
    {
        private readonly IRiceSalesRepository _repository;
        private readonly IConfiguration _configuration;
        private const decimal GST_RATE = 5; // 5% GST on rice

        public RiceSalesService(IConfiguration configuration)
        {
            _configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
            _repository = new RiceSalesRepository(configuration);
        }

        public List<RiceSales> GetAllSales(bool activeOnly = true)
        {
            try
            {
                return _repository.GetAll(activeOnly) ?? new List<RiceSales>();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving sales: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving sales: {ex.Message}", ex);
            }
        }

        public RiceSales? GetSaleById(int id)
        {
            try
            {
                return _repository.GetById(id);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving sale with ID {id}: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving sale with ID {id}: {ex.Message}", ex);
            }
        }

        public int CreateSale(RiceSales model, string username)
        {
            try
            {
                // Business validations
                if (model.Quantity <= 0)
                    throw new ArgumentException("Quantity must be greater than zero.");

                if (model.UnitPrice <= 0)
                    throw new ArgumentException("Unit price must be greater than zero.");

                // Calculate invoice values
                model.TotalInvoiceValue = model.Quantity * model.UnitPrice;
                model.TaxableValue = CalculateTaxableValue(model.TotalInvoiceValue, model.Discount);

                // Calculate GST based on interstate or intrastate
                string defaultState = _configuration["DefaultState"] ?? "YourState";
                var gstCalc = CalculateGST(model.TaxableValue, model.BuyerAddress ?? string.Empty, defaultState);
                model.CGSTAmount = gstCalc.CGST;
                model.SGSTAmount = gstCalc.SGST;
                model.IGSTAmount = gstCalc.IGST;
                model.TotalTaxAmount = gstCalc.TotalTax;

                // Calculate gross amount
                model.GrossInvoiceAmount = CalculateGrossAmount(model);

                // Generate invoice number if not provided
                if (string.IsNullOrEmpty(model.InvoiceNumber))
                {
                    model.InvoiceNumber = GenerateNewInvoiceNumber();
                }

                model.CreatedBy = username;
                model.CreatedDate = DateTime.Now;
                model.PaymentStatus = "Pending";
                model.IsActive = true;

                return _repository.Insert(model);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error creating sale: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error creating sale: {ex.Message}", ex);
            }
        }

        public bool UpdateSale(RiceSales model, string username)
        {
            try
            {
                var existing = _repository.GetById(model.Id);
                if (existing == null)
                    throw new ArgumentException($"Sale record with ID {model.Id} not found.");

                // Recalculate all values
                model.TotalInvoiceValue = model.Quantity * model.UnitPrice;
                model.TaxableValue = CalculateTaxableValue(model.TotalInvoiceValue, model.Discount);

                string defaultState = _configuration["DefaultState"] ?? "YourState";
                var gstCalc = CalculateGST(model.TaxableValue, model.BuyerAddress ?? string.Empty, defaultState);
                model.CGSTAmount = gstCalc.CGST;
                model.SGSTAmount = gstCalc.SGST;
                model.IGSTAmount = gstCalc.IGST;
                model.TotalTaxAmount = gstCalc.TotalTax;

                model.GrossInvoiceAmount = CalculateGrossAmount(model);
                model.ModifiedBy = username;
                model.ModifiedDate = DateTime.Now;

                return _repository.Update(model);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error updating sale with ID {model.Id}: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error updating sale with ID {model.Id}: {ex.Message}", ex);
            }
        }

        public bool DeleteSale(int id, string username)
        {
            try
            {
                var existing = _repository.GetById(id);
                if (existing == null)
                    throw new ArgumentException($"Sale record with ID {id} not found.");

                return _repository.Delete(id, username);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error deleting sale with ID {id}: {ex.Message}", ex);
            }
            catch (ArgumentException)
            {
                throw; // Re-throw validation exceptions as-is
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error deleting sale with ID {id}: {ex.Message}", ex);
            }
        }

        public List<RiceSales> SearchSalesByCustomer(string customerName)
        {
            try
            {
                return _repository.SearchByCustomer(customerName) ?? new List<RiceSales>();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error searching sales by customer '{customerName}': {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error searching sales by customer '{customerName}': {ex.Message}", ex);
            }
        }

        public List<RiceSales> GetPendingPayments()
        {
            try
            {
                return _repository.GetPendingPayments() ?? new List<RiceSales>();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving pending payments: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving pending payments: {ex.Message}", ex);
            }
        }

        public decimal CalculateTaxableValue(decimal totalValue, decimal discount)
        {
            return totalValue - discount;
        }

        public decimal CalculateGrossAmount(RiceSales model)
        {
            return model.TaxableValue + model.TotalTaxAmount + model.FreightCharges + model.OtherCharges;
        }

        public string GenerateNewInvoiceNumber()
        {
            try
            {
                return _repository.GenerateInvoiceNumber();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error generating invoice number: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error generating invoice number: {ex.Message}", ex);
            }
        }

        public decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate)
        {
            try
            {
                // This method calculates the total sales revenue for a given period
                // It's essential for your financial reports like Profit & Loss

                var sales = (_repository.GetAll(true) ?? new List<RiceSales>())
                    .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                    .ToList();

                // Sum up the gross invoice amounts for all sales in the period
                return sales.Sum(s => s.GrossInvoiceAmount);
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error calculating total sales amount: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error calculating total sales amount: {ex.Message}", ex);
            }
        }

        public List<RiceSales> GetSalesByDateRange(DateTime startDate, DateTime endDate)
        {
            try
            {
                // This retrieves all sales within a specific date range
                // Used extensively in your reports for filtering data by period

                return (_repository.GetAll(true) ?? new List<RiceSales>())
                    .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                    .OrderByDescending(s => s.SaleDate)
                    .ToList();
            }
            catch (SqlException ex)
            {
                throw new InvalidOperationException($"Database error retrieving sales by date range: {ex.Message}", ex);
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Error retrieving sales by date range: {ex.Message}", ex);
            }
        }

        public GSTCalculation CalculateGST(decimal taxableValue, string buyerState, string sellerState)
        {
            var result = new GSTCalculation();

            // Check if interstate or intrastate transaction
            bool isInterstate = !string.IsNullOrEmpty(buyerState) &&
                               !buyerState.Equals(sellerState, StringComparison.OrdinalIgnoreCase);

            if (isInterstate)
            {
                // Interstate - Apply IGST
                result.IGST = Math.Round(taxableValue * GST_RATE / 100, 2);
                result.CGST = 0;
                result.SGST = 0;
            }
            else
            {
                // Intrastate - Apply CGST + SGST
                result.CGST = Math.Round(taxableValue * (GST_RATE / 2) / 100, 2);
                result.SGST = Math.Round(taxableValue * (GST_RATE / 2) / 100, 2);
                result.IGST = 0;
            }

            result.TotalTax = result.CGST + result.SGST + result.IGST;
            return result;
        }
    }

    public class GSTCalculation
    {
        public decimal CGST { get; set; }
        public decimal SGST { get; set; }
        public decimal IGST { get; set; }
        public decimal TotalTax { get; set; }
    }
}