using System;
using System.Collections.Generic;
using RMMS.Models;

namespace RMMS.DataAccess.Repositories
{
    public interface IByProductSalesRepository
    {
        List<ByProductSales> GetAll(bool activeOnly = true);
        ByProductSales? GetById(int id);
        int Insert(ByProductSales model);
        bool Update(ByProductSales model);
        bool Delete(int id, string deletedBy);
        List<ByProductSales> GetByProductType(string productType);
        List<ByProductSales> GetByDateRange(DateTime startDate, DateTime endDate);
        List<ByProductSales> GetPendingPayments();
        decimal GetTotalSalesByProduct(string productType, DateTime startDate, DateTime endDate);
        string GenerateTransactionNumber();
    }
}