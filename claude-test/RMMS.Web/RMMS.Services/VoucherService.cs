using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class VoucherService : IVoucherService
    {
        private readonly IVouchersRepository _repository;
        private static int _lastVoucherNumber = 1000;
        private static readonly object _lock = new object();

        public VoucherService(IVouchersRepository repository)
        {
            _repository = repository;
        }

        public List<Voucher> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderByDescending(v => v.VoucherDate).ToList();
        }

        public Voucher? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(Voucher model, string username)
        {
            model.CreatedBy = username;
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;

            if (string.IsNullOrEmpty(model.VoucherNumber))
            {
                model.VoucherNumber = GenerateVoucherNumber();
            }

            _repository.Insert(model);
        }

        public void Update(Voucher model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Voucher with ID {model.Id} not found.");
            }

            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var voucher = _repository.GetById(id);
            if (voucher == null)
            {
                throw new ArgumentException($"Voucher with ID {id} not found.");
            }

            _repository.Delete(id, username);
        }

        public string GenerateVoucherNumber()
        {
            lock (_lock)
            {
                _lastVoucherNumber++;
                return $"VCH-{DateTime.Now:yyyyMM}-{_lastVoucherNumber}";
            }
        }

        public List<Voucher> GetByVoucherType(string voucherType)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(v => v.VoucherType != null && v.VoucherType.Equals(voucherType, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }

        public List<Voucher> GetByDateRange(DateTime startDate, DateTime endDate)
        {
            return _repository.GetAll(activeOnly: true)
                .Where(v => v.VoucherDate >= startDate && v.VoucherDate <= endDate)
                .OrderBy(v => v.VoucherDate)
                .ToList();
        }
    }
}
