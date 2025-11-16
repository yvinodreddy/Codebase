using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class PayableOverdueService : IPayableOverdueService
    {
        private readonly IPayablesOverdueRepository _repository;

        public PayableOverdueService(IPayablesOverdueRepository repository)
        {
            _repository = repository;
        }

        public List<PayableOverdue> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderByDescending(p => p.DaysOverdue).ToList();
        }

        public PayableOverdue? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(PayableOverdue model, string username)
        {
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            model.BalancePayable = model.InvoiceAmount - model.AmountPaid;

            _repository.Insert(model);
        }

        public void Update(PayableOverdue model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Payable overdue with ID {model.Id} not found.");
            }

            model.BalancePayable = model.InvoiceAmount - model.AmountPaid;
            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var payable = _repository.GetById(id);
            if (payable == null)
            {
                throw new ArgumentException($"Payable overdue with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public void RecordPayment(int id, decimal paymentAmount, string username)
        {
            // Validate payment amount
            if (paymentAmount <= 0)
            {
                throw new ArgumentException("Payment amount must be greater than zero.");
            }

            var payable = _repository.GetById(id);
            if (payable == null)
            {
                throw new ArgumentException($"Payable overdue with ID {id} not found.");
            }

            // Validate payment doesn't exceed balance
            if (paymentAmount > payable.BalancePayable)
            {
                throw new ArgumentException($"Payment amount ({paymentAmount:C}) cannot exceed balance payable ({payable.BalancePayable:C}).");
            }

            payable.AmountPaid += paymentAmount;
            payable.BalancePayable = payable.InvoiceAmount - payable.AmountPaid;

            _repository.Update(payable);
        }

        public List<PayableOverdue> GetOverduePayables()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(p => p.DaysOverdue > 0)
                .OrderByDescending(p => p.DaysOverdue)
                .ToList();
        }

        public decimal GetTotalOutstandingAmount()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(p => p.BalancePayable > 0)
                .Sum(p => p.BalancePayable);
        }

        public List<PayableOverdue> GetBySupplier(string supplierName)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(p => p.SupplierName != null && p.SupplierName.Contains(supplierName, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }
    }
}
