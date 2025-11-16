using RMMS.Models.Sales;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Interfaces.Sales
{
    public interface IInquiryService
    {
        Task<IEnumerable<Inquiry>> GetAllInquiriesAsync(bool activeOnly = true);
        Task<Inquiry?> GetInquiryByIdAsync(int id);
        Task<Inquiry?> GetInquiryByNumberAsync(string inquiryNumber);
        Task<IEnumerable<Inquiry>> GetInquiriesByCustomerAsync(int customerId);
        Task<IEnumerable<Inquiry>> GetInquiriesByStatusAsync(string status);
        Task<IEnumerable<Inquiry>> GetPendingInquiriesAsync();
        Task<IEnumerable<Inquiry>> GetInquiriesByDateRangeAsync(DateTime startDate, DateTime endDate);
        Task<IEnumerable<Inquiry>> GetFollowUpDueInquiriesAsync();
        Task<IEnumerable<Inquiry>> SearchInquiriesAsync(string searchTerm);
        Task<Inquiry> CreateInquiryAsync(Inquiry inquiry, string createdBy);
        Task<Inquiry> UpdateInquiryAsync(Inquiry inquiry, string modifiedBy);
        Task<bool> DeleteInquiryAsync(int id, string deletedBy);
        Task<bool> ConvertToQuotationAsync(int inquiryId, string convertedBy);
        Task<bool> MarkAsLostAsync(int inquiryId, string lostReason, string modifiedBy);
        Task<bool> AssignInquiryAsync(int inquiryId, int employeeId, string modifiedBy);
        Task<bool> UpdateFollowUpDateAsync(int inquiryId, DateTime followUpDate, string modifiedBy);
        Task<Dictionary<string, int>> GetInquiryStatisticsAsync();
    }
}
