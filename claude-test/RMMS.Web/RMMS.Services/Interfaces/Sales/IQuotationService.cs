using RMMS.Models.Sales;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Interfaces.Sales
{
    public interface IQuotationService
    {
        Task<IEnumerable<Quotation>> GetAllQuotationsAsync();
        Task<Quotation?> GetQuotationByIdAsync(int id);
        Task<Quotation?> GetQuotationByNumberAsync(string quotationNumber);
        Task<IEnumerable<Quotation>> GetQuotationsByCustomerAsync(int customerId);
        Task<IEnumerable<Quotation>> GetQuotationsByInquiryAsync(int inquiryId);
        Task<IEnumerable<Quotation>> GetQuotationsByStatusAsync(string status);
        Task<IEnumerable<Quotation>> GetQuotationsByDateRangeAsync(DateTime fromDate, DateTime toDate);
        Task<IEnumerable<Quotation>> GetPendingQuotationsAsync();
        Task<IEnumerable<Quotation>> GetExpiredQuotationsAsync();
        Task<IEnumerable<Quotation>> SearchQuotationsAsync(string searchTerm);
        Task<Quotation> CreateQuotationAsync(Quotation quotation);
        Task UpdateQuotationAsync(Quotation quotation);
        Task DeleteQuotationAsync(int id);
        Task<Quotation> AddQuotationItemAsync(int quotationId, QuotationItem item);
        Task RemoveQuotationItemAsync(int quotationId, int itemId);
        Task RecalculateQuotationTotalsAsync(int quotationId);
        Task<bool> ApproveQuotationAsync(int quotationId, int approvedByEmployeeId);
        Task<bool> SendQuotationAsync(int quotationId);
        Task<bool> ConvertToSalesOrderAsync(int quotationId);
        Task<Dictionary<string, object>> GetQuotationStatisticsAsync();
    }
}
