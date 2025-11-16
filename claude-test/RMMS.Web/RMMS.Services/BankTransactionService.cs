using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class BankTransactionService : IBankTransactionService
    {
        private readonly IBankTransactionsRepository _repository;

        public BankTransactionService(IBankTransactionsRepository repository)
        {
            _repository = repository;
        }

        public List<BankTransaction> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderBy(b => b.TransactionDate).ToList();
        }

        public BankTransaction? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(BankTransaction model, string username)
        {
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;

            // Calculate balance for this account
            var accountTransactions = _repository.GetAll(activeOnly: true)
                .Where(b => b.AccountNumber == (model.AccountNumber ?? string.Empty))
                .OrderBy(b => b.TransactionDate);
            decimal previousBalance = 0;
            foreach (var trans in accountTransactions)
            {
                previousBalance = previousBalance + trans.Deposits - trans.Withdrawals;
            }
            model.Balance = previousBalance + model.Deposits - model.Withdrawals;

            _repository.Insert(model);
        }

        public void Update(BankTransaction model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Bank transaction with ID {model.Id} not found.");
            }

            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var transaction = _repository.GetById(id);
            if (transaction == null)
            {
                throw new ArgumentException($"Bank transaction with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public List<BankTransaction> GetByBankAccount(string accountNumber)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(b => b.AccountNumber == accountNumber)
                .OrderBy(b => b.TransactionDate)
                .ToList();
        }

        public decimal GetAccountBalance(string accountNumber)
        {
            var transactions = _repository.GetAll(activeOnly: true)
                .Where(b => b.AccountNumber == accountNumber)
                .OrderBy(b => b.TransactionDate);
            decimal balance = 0;
            foreach (var trans in transactions)
            {
                balance = balance + trans.Deposits - trans.Withdrawals;
            }
            return balance;
        }

        public List<BankTransaction> GetTransactionsByDateRange(DateTime startDate, DateTime endDate)
        {
            // Retrieves all bank transactions within a date range
            // Critical for calculating total banking expenses and receipts
            return _repository.GetAll(activeOnly: true)
                .Where(b => b.TransactionDate >= startDate &&
                            b.TransactionDate <= endDate)
                .OrderBy(b => b.TransactionDate)
                .ToList();
        }
    }
}