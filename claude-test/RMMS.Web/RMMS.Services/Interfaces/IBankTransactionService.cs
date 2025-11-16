using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IBankTransactionService
    {
        List<BankTransaction> GetAll();
        BankTransaction? GetById(int id);
        void Create(BankTransaction model, string username);
        void Update(BankTransaction model, string username);
        void Delete(int id, string username);
        List<BankTransaction> GetByBankAccount(string accountNumber);
        decimal GetAccountBalance(string accountNumber);
        List<BankTransaction> GetTransactionsByDateRange(DateTime startDate, DateTime endDate);
    }
}