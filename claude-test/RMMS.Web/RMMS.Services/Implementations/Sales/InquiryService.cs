using RMMS.DataAccess.Repositories.Sales;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Services.Implementations.Sales
{
    public class InquiryService : IInquiryService
    {
        private readonly IInquiryRepository _inquiryRepository;

        public InquiryService(IInquiryRepository inquiryRepository)
        {
            _inquiryRepository = inquiryRepository;
        }

        public async Task<IEnumerable<Inquiry>> GetAllInquiriesAsync(bool activeOnly = true)
        {
            return await _inquiryRepository.GetAllAsync(activeOnly);
        }

        public async Task<Inquiry?> GetInquiryByIdAsync(int id)
        {
            return await _inquiryRepository.GetByIdAsync(id);
        }

        public async Task<Inquiry?> GetInquiryByNumberAsync(string inquiryNumber)
        {
            return await _inquiryRepository.GetByInquiryNumberAsync(inquiryNumber);
        }

        public async Task<IEnumerable<Inquiry>> GetInquiriesByCustomerAsync(int customerId)
        {
            return await _inquiryRepository.GetByCustomerIdAsync(customerId);
        }

        public async Task<IEnumerable<Inquiry>> GetInquiriesByStatusAsync(string status)
        {
            return await _inquiryRepository.GetByStatusAsync(status);
        }

        public async Task<IEnumerable<Inquiry>> GetPendingInquiriesAsync()
        {
            return await _inquiryRepository.GetPendingInquiriesAsync();
        }

        public async Task<IEnumerable<Inquiry>> GetInquiriesByDateRangeAsync(DateTime startDate, DateTime endDate)
        {
            return await _inquiryRepository.GetByDateRangeAsync(startDate, endDate);
        }

        public async Task<IEnumerable<Inquiry>> GetFollowUpDueInquiriesAsync()
        {
            var allInquiries = await _inquiryRepository.GetAllAsync(true);
            var today = DateTime.Now.Date;

            return allInquiries
                .Where(i => i.FollowUpDate.HasValue &&
                           i.FollowUpDate.Value.Date <= today &&
                           (i.Status == "New" || i.Status == "In Progress"))
                .OrderBy(i => i.FollowUpDate);
        }

        public async Task<IEnumerable<Inquiry>> SearchInquiriesAsync(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return await GetAllInquiriesAsync();

            var allInquiries = await _inquiryRepository.GetAllAsync(true);
            searchTerm = searchTerm.ToLower();

            return allInquiries.Where(i =>
                i.InquiryNumber.ToLower().Contains(searchTerm) ||
                (i.Customer?.CustomerName?.ToLower().Contains(searchTerm) ?? false) ||
                (i.ProductType?.ToLower().Contains(searchTerm) ?? false) ||
                (i.CustomerRequirements?.ToLower().Contains(searchTerm) ?? false)
            );
        }

        public async Task<Inquiry> CreateInquiryAsync(Inquiry inquiry, string createdBy)
        {
            // Set audit fields
            inquiry.CreatedDate = DateTime.Now;
            inquiry.CreatedBy = createdBy;
            inquiry.IsActive = true;

            // Set default status if not provided
            if (string.IsNullOrEmpty(inquiry.Status))
            {
                inquiry.Status = "New";
            }

            // Set default priority if not provided
            if (string.IsNullOrEmpty(inquiry.Priority))
            {
                inquiry.Priority = "Normal";
            }

            return await _inquiryRepository.AddAsync(inquiry);
        }

        public async Task<Inquiry> UpdateInquiryAsync(Inquiry inquiry, string modifiedBy)
        {
            inquiry.ModifiedDate = DateTime.Now;
            inquiry.ModifiedBy = modifiedBy;

            return await _inquiryRepository.UpdateAsync(inquiry);
        }

        public async Task<bool> DeleteInquiryAsync(int id, string deletedBy)
        {
            var inquiry = await _inquiryRepository.GetByIdAsync(id);
            if (inquiry == null) return false;

            inquiry.ModifiedBy = deletedBy;
            return await _inquiryRepository.DeleteAsync(id);
        }

        public async Task<bool> ConvertToQuotationAsync(int inquiryId, string convertedBy)
        {
            var inquiry = await _inquiryRepository.GetByIdAsync(inquiryId);
            if (inquiry == null) return false;

            inquiry.Status = "Quoted";
            inquiry.ModifiedDate = DateTime.Now;
            inquiry.ModifiedBy = convertedBy;

            await _inquiryRepository.UpdateAsync(inquiry);
            return true;
        }

        public async Task<bool> MarkAsLostAsync(int inquiryId, string lostReason, string modifiedBy)
        {
            var inquiry = await _inquiryRepository.GetByIdAsync(inquiryId);
            if (inquiry == null) return false;

            inquiry.Status = "Lost";
            inquiry.LostReason = lostReason;
            inquiry.ModifiedDate = DateTime.Now;
            inquiry.ModifiedBy = modifiedBy;

            await _inquiryRepository.UpdateAsync(inquiry);
            return true;
        }

        public async Task<bool> AssignInquiryAsync(int inquiryId, int employeeId, string modifiedBy)
        {
            var inquiry = await _inquiryRepository.GetByIdAsync(inquiryId);
            if (inquiry == null) return false;

            inquiry.AssignedToEmployeeId = employeeId;
            inquiry.ModifiedDate = DateTime.Now;
            inquiry.ModifiedBy = modifiedBy;

            // Update status to "In Progress" if currently "New"
            if (inquiry.Status == "New")
            {
                inquiry.Status = "In Progress";
            }

            await _inquiryRepository.UpdateAsync(inquiry);
            return true;
        }

        public async Task<bool> UpdateFollowUpDateAsync(int inquiryId, DateTime followUpDate, string modifiedBy)
        {
            var inquiry = await _inquiryRepository.GetByIdAsync(inquiryId);
            if (inquiry == null) return false;

            inquiry.FollowUpDate = followUpDate;
            inquiry.ModifiedDate = DateTime.Now;
            inquiry.ModifiedBy = modifiedBy;

            await _inquiryRepository.UpdateAsync(inquiry);
            return true;
        }

        public async Task<Dictionary<string, int>> GetInquiryStatisticsAsync()
        {
            var allInquiries = await _inquiryRepository.GetAllAsync(true);

            var stats = new Dictionary<string, int>
            {
                { "Total", allInquiries.Count() },
                { "New", allInquiries.Count(i => i.Status == "New") },
                { "InProgress", allInquiries.Count(i => i.Status == "In Progress") },
                { "Quoted", allInquiries.Count(i => i.Status == "Quoted") },
                { "Converted", allInquiries.Count(i => i.Status == "Converted") },
                { "Lost", allInquiries.Count(i => i.Status == "Lost") },
                { "Closed", allInquiries.Count(i => i.Status == "Closed") },
                { "FollowUpDue", allInquiries.Count(i => i.FollowUpDate.HasValue && i.FollowUpDate.Value.Date <= DateTime.Now.Date && (i.Status == "New" || i.Status == "In Progress")) }
            };

            return stats;
        }
    }
}
