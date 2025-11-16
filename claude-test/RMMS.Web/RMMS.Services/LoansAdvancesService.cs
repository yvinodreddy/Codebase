using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class LoansAdvancesService : ILoansAdvancesService
    {
        private readonly ILoansAdvancesRepository _repository;

        public LoansAdvancesService(ILoansAdvancesRepository repository)
        {
            _repository = repository;
        }

        public List<LoanAdvance> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderByDescending(l => l.Date).ToList();
        }

        public LoanAdvance? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(LoanAdvance model, string username)
        {
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            model.Balance = model.AmountGiven - model.Repayment;

            _repository.Insert(model);
        }

        public void Update(LoanAdvance model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Loan/Advance with ID {model.Id} not found.");
            }

            model.Balance = model.AmountGiven - model.Repayment;
            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var loan = _repository.GetById(id);
            if (loan == null)
            {
                throw new ArgumentException($"Loan/Advance with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public void RecordRepayment(int id, decimal repaymentAmount, DateTime repaymentDate, string username)
        {
            // Validate repayment amount
            if (repaymentAmount <= 0)
            {
                throw new ArgumentException("Repayment amount must be greater than zero.");
            }

            var loan = _repository.GetById(id);
            if (loan == null)
            {
                throw new ArgumentException($"Loan/Advance with ID {id} not found.");
            }

            // Validate repayment doesn't exceed balance
            if (repaymentAmount > loan.Balance)
            {
                throw new ArgumentException($"Repayment amount ({repaymentAmount:C}) cannot exceed loan balance ({loan.Balance:C}).");
            }

            loan.Repayment += repaymentAmount;
            loan.RepaymentDate = repaymentDate;
            loan.Balance = loan.AmountGiven - loan.Repayment;

            _repository.Update(loan);
        }

        public List<LoanAdvance> GetOutstandingLoans()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(l => l.Balance > 0)
                .OrderByDescending(l => l.Balance)
                .ToList();
        }

        public decimal GetTotalOutstandingAmount()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(l => l.Balance > 0)
                .Sum(l => l.Balance);
        }

        public List<LoanAdvance> GetByParty(string partyName)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(l => l.PartyName != null && l.PartyName.Contains(partyName, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }
    }
}
