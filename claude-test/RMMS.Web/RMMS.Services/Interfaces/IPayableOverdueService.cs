using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IPayableOverdueService
    {
        List<PayableOverdue> GetAll();
        PayableOverdue? GetById(int id);
        void Create(PayableOverdue model, string username);
        void Update(PayableOverdue model, string username);
        void Delete(int id, string username);
        void RecordPayment(int id, decimal paymentAmount, string username);
        List<PayableOverdue> GetOverduePayables();
        decimal GetTotalOutstandingAmount();
        List<PayableOverdue> GetBySupplier(string supplierName);
    }
}