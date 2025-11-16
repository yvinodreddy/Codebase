using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class CashBookService : ICashBookService
    {
        private readonly ICashBookRepository _repository;

        public CashBookService(ICashBookRepository repository)
        {
            _repository = repository;
        }

        public List<CashBook> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderBy(c => c.TransactionDate).ToList();
        }

        public CashBook? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(CashBook model, string username)
        {
            model.CreatedBy = username;
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;

            // Calculate running balance
            var entries = _repository.GetAll(activeOnly: true);
            decimal previousBalance = 0;
            foreach (var entry in entries)
            {
                previousBalance = previousBalance + entry.Receipts - entry.Payments;
            }
            model.Balance = previousBalance + model.Receipts - model.Payments;

            _repository.Insert(model);
        }

        public void Update(CashBook model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Cash book entry with ID {model.Id} not found.");
            }

            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var entry = _repository.GetById(id);
            if (entry == null)
            {
                throw new ArgumentException($"Cash book entry with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public decimal GetCurrentBalance()
        {
            var entries = _repository.GetAll(activeOnly: true);
            decimal balance = 0;
            foreach (var entry in entries)
            {
                balance = balance + entry.Receipts - entry.Payments;
            }
            return balance;
        }

        public List<CashBook> GetTransactionsByDate(DateTime date)
        {
            // Retrieves all cash transactions for a specific date
            // Used in daily reports to show cash movement
            return _repository.GetAll(activeOnly: true)
                .Where(c => c.TransactionDate.Date == date.Date)
                .OrderBy(c => c.CreatedDate)
                .ToList();
        }

        public decimal GetTotalReceipts(DateTime startDate, DateTime endDate)
        {
            // Sums up all money received in cash during a period
            // Essential for cash flow analysis
            return _repository.GetAll(activeOnly: true)
                .Where(c => c.TransactionDate >= startDate &&
                            c.TransactionDate <= endDate)
                .Sum(c => c.Receipts);
        }

        public decimal GetTotalPayments(DateTime startDate, DateTime endDate)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(c => c.TransactionDate >= startDate && c.TransactionDate <= endDate)
                .Sum(c => c.Payments);
        }
    }
}
