using RMMS.Models.Sales;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public interface IInquiryRepository
    {
        Task<IEnumerable<Inquiry>> GetAllAsync(bool activeOnly = true);
        Task<Inquiry?> GetByIdAsync(int id);
        Task<Inquiry?> GetByInquiryNumberAsync(string inquiryNumber);
        Task<IEnumerable<Inquiry>> GetByCustomerIdAsync(int customerId);
        Task<IEnumerable<Inquiry>> GetByStatusAsync(string status);
        Task<IEnumerable<Inquiry>> GetPendingInquiriesAsync();
        Task<IEnumerable<Inquiry>> GetByDateRangeAsync(DateTime startDate, DateTime endDate);
        Task<string> GenerateInquiryNumberAsync();
        Task<Inquiry> AddAsync(Inquiry inquiry);
        Task<Inquiry> UpdateAsync(Inquiry inquiry);
        Task<bool> DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
    }
}
