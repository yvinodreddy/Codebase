using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Sales;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public class QuotationRepository : IQuotationRepository
    {
        private readonly ApplicationDbContext _context;

        public QuotationRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Quotation>> GetAllAsync()
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.ApprovedByEmployee)
                .Include(q => q.QuotationItems)
                    .ThenInclude(qi => qi.Product)
                .Where(q => q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<Quotation?> GetByIdAsync(int id)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.ApprovedByEmployee)
                .Include(q => q.QuotationItems)
                    .ThenInclude(qi => qi.Product)
                .FirstOrDefaultAsync(q => q.Id == id && q.IsActive);
        }

        public async Task<Quotation?> GetByQuotationNumberAsync(string quotationNumber)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.ApprovedByEmployee)
                .Include(q => q.QuotationItems)
                    .ThenInclude(qi => qi.Product)
                .FirstOrDefaultAsync(q => q.QuotationNumber == quotationNumber && q.IsActive);
        }

        public async Task<IEnumerable<Quotation>> GetByCustomerIdAsync(int customerId)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => q.CustomerId == customerId && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Quotation>> GetByInquiryIdAsync(int inquiryId)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => q.InquiryId == inquiryId && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Quotation>> GetByStatusAsync(string status)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => q.Status == status && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Quotation>> GetByDateRangeAsync(DateTime fromDate, DateTime toDate)
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => q.QuotationDate >= fromDate && q.QuotationDate <= toDate && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Quotation>> GetPendingQuotationsAsync()
        {
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => (q.Status == "Draft" || q.Status == "Sent") && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<IEnumerable<Quotation>> GetExpiredQuotationsAsync()
        {
            var today = DateTime.Now.Date;
            return await _context.Quotations
                .Include(q => q.Customer)
                .Include(q => q.Inquiry)
                .Include(q => q.QuotationItems)
                .Where(q => q.ValidUntil < today && q.Status == "Sent" && q.IsActive)
                .OrderByDescending(q => q.QuotationDate)
                .ToListAsync();
        }

        public async Task<string> GenerateQuotationNumberAsync()
        {
            var yearMonth = DateTime.Now.ToString("yyyyMM");
            var prefix = $"QUO{yearMonth}";

            var lastQuotation = await _context.Quotations
                .Where(q => q.QuotationNumber.StartsWith(prefix))
                .OrderByDescending(q => q.QuotationNumber)
                .FirstOrDefaultAsync();

            if (lastQuotation == null)
            {
                return $"{prefix}0001";
            }

            var lastNumber = int.Parse(lastQuotation.QuotationNumber.Substring(prefix.Length));
            var newNumber = lastNumber + 1;
            return $"{prefix}{newNumber:D4}";
        }

        public async Task<Quotation> AddAsync(Quotation quotation)
        {
            if (string.IsNullOrEmpty(quotation.QuotationNumber))
            {
                quotation.QuotationNumber = await GenerateQuotationNumberAsync();
            }

            quotation.CreatedDate = DateTime.Now;
            quotation.IsActive = true;

            _context.Quotations.Add(quotation);
            await _context.SaveChangesAsync();
            return quotation;
        }

        public async Task UpdateAsync(Quotation quotation)
        {
            quotation.ModifiedDate = DateTime.Now;
            _context.Entry(quotation).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(int id)
        {
            var quotation = await _context.Quotations.FindAsync(id);
            if (quotation != null)
            {
                quotation.IsActive = false;
                quotation.ModifiedDate = DateTime.Now;
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.Quotations.AnyAsync(q => q.Id == id && q.IsActive);
        }
    }
}
