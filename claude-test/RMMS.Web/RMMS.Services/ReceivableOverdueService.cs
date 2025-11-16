using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class ReceivableOverdueService : IReceivableOverdueService
    {
        private readonly IReceivablesOverdueRepository _repository;

        public ReceivableOverdueService(IReceivablesOverdueRepository repository)
        {
            _repository = repository;
        }

        public List<ReceivableOverdue> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderByDescending(r => r.DaysOverdue).ToList();
        }

        public ReceivableOverdue? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(ReceivableOverdue model, string username)
        {
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            model.BalanceDue = model.InvoiceAmount - model.AmountReceived;

            _repository.Insert(model);
        }

        public void Update(ReceivableOverdue model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Receivable overdue with ID {model.Id} not found.");
            }

            model.BalanceDue = model.InvoiceAmount - model.AmountReceived;
            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var receivable = _repository.GetById(id);
            if (receivable == null)
            {
                throw new ArgumentException($"Receivable overdue with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public void RecordReceipt(int id, decimal receiptAmount, string username)
        {
            // Validate receipt amount
            if (receiptAmount <= 0)
            {
                throw new ArgumentException("Receipt amount must be greater than zero.");
            }

            var receivable = _repository.GetById(id);
            if (receivable == null)
            {
                throw new ArgumentException($"Receivable overdue with ID {id} not found.");
            }

            // Validate receipt doesn't exceed balance due
            if (receiptAmount > receivable.BalanceDue)
            {
                throw new ArgumentException($"Receipt amount ({receiptAmount:C}) cannot exceed balance due ({receivable.BalanceDue:C}).");
            }

            receivable.AmountReceived += receiptAmount;
            receivable.BalanceDue = receivable.InvoiceAmount - receivable.AmountReceived;

            _repository.Update(receivable);
        }

        public List<ReceivableOverdue> GetOverdueReceivables()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(r => r.DaysOverdue > 0)
                .OrderByDescending(r => r.DaysOverdue)
                .ToList();
        }

        public decimal GetTotalOutstandingAmount()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(r => r.BalanceDue > 0)
                .Sum(r => r.BalanceDue);
        }

        public List<ReceivableOverdue> GetByCustomer(string customerName)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(r => r.CustomerName != null && r.CustomerName.Contains(customerName, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }
    }
}
