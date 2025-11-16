using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IByProductSalesService
    {
        List<ByProductSales> GetAllSales();
        ByProductSales? GetSaleById(int id);
        int CreateSale(ByProductSales model, string username);
        bool UpdateSale(ByProductSales model, string username);
        bool DeleteSale(int id, string username);
        List<ByProductSales> GetSalesByProductType(string productType);
        List<ByProductSales> GetPendingPayments();

        // Methods that were missing from the interface
        public List<ByProductSales> GetSalesByDateRange(DateTime startDate, DateTime endDate) => new List<ByProductSales>();
        public decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate) => 0m;
    }
}