using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IReceivableOverdueService
    {
        List<ReceivableOverdue> GetAll();
        ReceivableOverdue? GetById(int id);
        void Create(ReceivableOverdue model, string username);
        void Update(ReceivableOverdue model, string username);
        void Delete(int id, string username);
        void RecordReceipt(int id, decimal receiptAmount, string username);
        List<ReceivableOverdue> GetOverdueReceivables();
        decimal GetTotalOutstandingAmount();
        List<ReceivableOverdue> GetByCustomer(string customerName);
    }
}