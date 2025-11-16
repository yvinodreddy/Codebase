using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IVoucherService
    {
        List<Voucher> GetAll();
        Voucher? GetById(int id);
        void Create(Voucher model, string username);
        void Update(Voucher model, string username);
        void Delete(int id, string username);
        string GenerateVoucherNumber();
        List<Voucher> GetByVoucherType(string voucherType);
        List<Voucher> GetByDateRange(DateTime startDate, DateTime endDate);
    }
}