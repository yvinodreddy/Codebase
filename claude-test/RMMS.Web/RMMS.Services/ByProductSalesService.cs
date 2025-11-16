using Microsoft.Extensions.Configuration;
using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class ByProductSalesService : IByProductSalesService
    {
        private readonly IByProductSalesRepository _repository;

        public ByProductSalesService(IByProductSalesRepository repository)
        {
            _repository = repository;
        }

        public List<ByProductSales> GetAllSales()
        {
            return _repository.GetAll(activeOnly: true);
        }

        public ByProductSales? GetSaleById(int id)
        {
            return _repository.GetById(id);
        }

        public int CreateSale(ByProductSales model, string username)
        {
            try
            {
                // Validate the model
                ValidateSale(model);

                // Calculate total amount
                model.TotalAmount = Math.Round(model.Quantity * model.Rate, 2);

                // Set audit fields
                model.CreatedBy = username;
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;

                // Set default payment status based on payment mode
                if (string.IsNullOrEmpty(model.PaymentStatus))
                {
                    model.PaymentStatus = model.PaymentMode == "Cash" ? "Paid" : "Pending";
                }

                // Insert and return the new ID
                return _repository.Insert(model);
            }
            catch (Exception ex)
            {
                throw new ApplicationException($"Error creating by-product sale: {ex.Message}", ex);
            }
        }

        public bool UpdateSale(ByProductSales model, string username)
        {
            // Validate the model
            ValidateSale(model);

            // Recalculate total amount
            model.TotalAmount = Math.Round(model.Quantity * model.Rate, 2);

            // Update audit fields
            model.ModifiedBy = username;
            model.ModifiedDate = DateTime.Now;

            return _repository.Update(model);
        }

        public bool DeleteSale(int id, string username)
        {
            return _repository.Delete(id, username);
        }

        public List<ByProductSales> GetSalesByProductType(string productType)
        {
            if (string.IsNullOrWhiteSpace(productType))
            {
                return new List<ByProductSales>();
            }

            return _repository.GetByProductType(productType);
        }

        public List<ByProductSales> GetPendingPayments()
        {
            return _repository.GetPendingPayments();
        }

        public decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate)
        {
            var sales = GetSalesByDateRange(startDate, endDate);
            return sales.Sum(s => s.TotalAmount);
        }

        public List<ByProductSales> GetSalesByDateRange(DateTime startDate, DateTime endDate)
        {
            if (startDate > endDate)
            {
                throw new ArgumentException("Start date cannot be greater than end date.");
            }

            return _repository.GetByDateRange(startDate, endDate);
        }

        private void ValidateSale(ByProductSales model)
        {
            var errors = new List<string>();

            if (model == null)
            {
                throw new ArgumentNullException(nameof(model), "Sale model cannot be null.");
            }

            if (string.IsNullOrWhiteSpace(model.ProductType))
            {
                errors.Add("Product type is required.");
            }

            if (string.IsNullOrWhiteSpace(model.BuyerName))
            {
                errors.Add("Buyer name is required.");
            }

            if (model.Quantity <= 0)
            {
                errors.Add("Quantity must be greater than zero.");
            }

            if (model.Rate <= 0)
            {
                errors.Add("Rate must be greater than zero.");
            }

            if (model.SaleDate > DateTime.Now.Date)
            {
                errors.Add("Sale date cannot be in the future.");
            }

            if (!string.IsNullOrEmpty(model.PaymentMode))
            {
                var validPaymentModes = new[] { "Cash", "Online", "Bank Transfer", "Cheque", "Credit" };
                if (!validPaymentModes.Contains(model.PaymentMode))
                {
                    errors.Add($"Invalid payment mode. Valid modes are: {string.Join(", ", validPaymentModes)}");
                }
            }

            if (errors.Any())
            {
                throw new ArgumentException(string.Join(" ", errors));
            }
        }
    }
}
