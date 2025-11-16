using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public class InquiryRepository : IInquiryRepository
    {
        private readonly ApplicationDbContext _context;

        public InquiryRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Inquiry>> GetAllAsync(bool activeOnly = true)
        {
            var query = _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .AsQueryable();

            if (activeOnly)
            {
                query = query.Where(i => i.IsActive);
            }

            return await query
                .OrderByDescending(i => i.InquiryDate)
                .ToListAsync();
        }

        public async Task<Inquiry?> GetByIdAsync(int id)
        {
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .FirstOrDefaultAsync(i => i.Id == id);
        }

        public async Task<Inquiry?> GetByInquiryNumberAsync(string inquiryNumber)
        {
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .FirstOrDefaultAsync(i => i.InquiryNumber == inquiryNumber);
        }

        public async Task<IEnumerable<Inquiry>> GetByCustomerIdAsync(int customerId)
        {
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .Where(i => i.CustomerId == customerId && i.IsActive)
                .OrderByDescending(i => i.InquiryDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Inquiry>> GetByStatusAsync(string status)
        {
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .Where(i => i.Status == status && i.IsActive)
                .OrderByDescending(i => i.InquiryDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Inquiry>> GetPendingInquiriesAsync()
        {
            var pendingStatuses = new[] { "New", "In Progress" };
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .Where(i => pendingStatuses.Contains(i.Status) && i.IsActive)
                .OrderBy(i => i.InquiryDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Inquiry>> GetByDateRangeAsync(DateTime startDate, DateTime endDate)
        {
            return await _context.Inquiries
                .Include(i => i.Customer)
                .Include(i => i.AssignedToEmployee)
                .Where(i => i.InquiryDate >= startDate && i.InquiryDate <= endDate && i.IsActive)
                .OrderByDescending(i => i.InquiryDate)
                .ToListAsync();
        }

        public async Task<string> GenerateInquiryNumberAsync()
        {
            var today = DateTime.Now;
            var prefix = $"INQ{today:yyyyMM}";

            var lastInquiry = await _context.Inquiries
                .Where(i => i.InquiryNumber.StartsWith(prefix))
                .OrderByDescending(i => i.InquiryNumber)
                .FirstOrDefaultAsync();

            if (lastInquiry == null)
            {
                return $"{prefix}0001";
            }

            var lastNumber = int.Parse(lastInquiry.InquiryNumber.Substring(prefix.Length));
            var newNumber = lastNumber + 1;

            return $"{prefix}{newNumber:D4}";
        }

        public async Task<Inquiry> AddAsync(Inquiry inquiry)
        {
            if (string.IsNullOrEmpty(inquiry.InquiryNumber))
            {
                inquiry.InquiryNumber = await GenerateInquiryNumberAsync();
            }

            inquiry.CreatedDate = DateTime.Now;
            _context.Inquiries.Add(inquiry);
            await _context.SaveChangesAsync();
            return inquiry;
        }

        public async Task<Inquiry> UpdateAsync(Inquiry inquiry)
        {
            inquiry.ModifiedDate = DateTime.Now;
            _context.Entry(inquiry).State = EntityState.Modified;
            await _context.SaveChangesAsync();
            return inquiry;
        }

        public async Task<bool> DeleteAsync(int id)
        {
            var inquiry = await _context.Inquiries.FindAsync(id);
            if (inquiry == null) return false;

            inquiry.IsActive = false;
            inquiry.ModifiedDate = DateTime.Now;
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.Inquiries.AnyAsync(i => i.Id == id);
        }
    }
}
