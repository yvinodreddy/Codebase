using RMMS.Models.Sales;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.DataAccess.Repositories.Sales
{
    public interface IQuotationRepository
    {
        Task<IEnumerable<Quotation>> GetAllAsync();
        Task<Quotation?> GetByIdAsync(int id);
        Task<Quotation?> GetByQuotationNumberAsync(string quotationNumber);
        Task<IEnumerable<Quotation>> GetByCustomerIdAsync(int customerId);
        Task<IEnumerable<Quotation>> GetByInquiryIdAsync(int inquiryId);
        Task<IEnumerable<Quotation>> GetByStatusAsync(string status);
        Task<IEnumerable<Quotation>> GetByDateRangeAsync(DateTime fromDate, DateTime toDate);
        Task<IEnumerable<Quotation>> GetPendingQuotationsAsync();
        Task<IEnumerable<Quotation>> GetExpiredQuotationsAsync();
        Task<string> GenerateQuotationNumberAsync();
        Task<Quotation> AddAsync(Quotation quotation);
        Task UpdateAsync(Quotation quotation);
        Task DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
    }
}
