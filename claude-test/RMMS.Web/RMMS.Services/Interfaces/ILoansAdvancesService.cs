using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface ILoansAdvancesService
    {
        List<LoanAdvance> GetAll();
        LoanAdvance? GetById(int id);
        void Create(LoanAdvance model, string username);
        void Update(LoanAdvance model, string username);
        void Delete(int id, string username);
        void RecordRepayment(int id, decimal repaymentAmount, DateTime repaymentDate, string username);
        List<LoanAdvance> GetOutstandingLoans();
        decimal GetTotalOutstandingAmount();
        List<LoanAdvance> GetByParty(string partyName);
    }
}