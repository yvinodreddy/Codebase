using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface ICashBookService
    {
        List<CashBook> GetAll();
        CashBook? GetById(int id);
        void Create(CashBook model, string username);
        void Update(CashBook model, string username);
        void Delete(int id, string username);
        decimal GetCurrentBalance();
        List<CashBook> GetTransactionsByDate(DateTime date);
        decimal GetTotalReceipts(DateTime startDate, DateTime endDate);
        decimal GetTotalPayments(DateTime startDate, DateTime endDate);
    }
}