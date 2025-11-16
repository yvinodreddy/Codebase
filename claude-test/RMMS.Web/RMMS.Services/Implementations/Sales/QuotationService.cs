using RMMS.DataAccess.Repositories.Sales;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Services.Implementations.Sales
{
    public class QuotationService : IQuotationService
    {
        private readonly IQuotationRepository _quotationRepository;
        private readonly IInquiryRepository _inquiryRepository;

        public QuotationService(IQuotationRepository quotationRepository, IInquiryRepository inquiryRepository)
        {
            _quotationRepository = quotationRepository;
            _inquiryRepository = inquiryRepository;
        }

        public async Task<IEnumerable<Quotation>> GetAllQuotationsAsync()
        {
            return await _quotationRepository.GetAllAsync();
        }

        public async Task<Quotation?> GetQuotationByIdAsync(int id)
        {
            return await _quotationRepository.GetByIdAsync(id);
        }

        public async Task<Quotation?> GetQuotationByNumberAsync(string quotationNumber)
        {
            return await _quotationRepository.GetByQuotationNumberAsync(quotationNumber);
        }

        public async Task<IEnumerable<Quotation>> GetQuotationsByCustomerAsync(int customerId)
        {
            return await _quotationRepository.GetByCustomerIdAsync(customerId);
        }

        public async Task<IEnumerable<Quotation>> GetQuotationsByInquiryAsync(int inquiryId)
        {
            return await _quotationRepository.GetByInquiryIdAsync(inquiryId);
        }

        public async Task<IEnumerable<Quotation>> GetQuotationsByStatusAsync(string status)
        {
            return await _quotationRepository.GetByStatusAsync(status);
        }

        public async Task<IEnumerable<Quotation>> GetQuotationsByDateRangeAsync(DateTime fromDate, DateTime toDate)
        {
            return await _quotationRepository.GetByDateRangeAsync(fromDate, toDate);
        }

        public async Task<IEnumerable<Quotation>> GetPendingQuotationsAsync()
        {
            return await _quotationRepository.GetPendingQuotationsAsync();
        }

        public async Task<IEnumerable<Quotation>> GetExpiredQuotationsAsync()
        {
            return await _quotationRepository.GetExpiredQuotationsAsync();
        }

        public async Task<IEnumerable<Quotation>> SearchQuotationsAsync(string searchTerm)
        {
            var allQuotations = await _quotationRepository.GetAllAsync();

            if (string.IsNullOrWhiteSpace(searchTerm))
                return allQuotations;

            searchTerm = searchTerm.ToLower();
            return allQuotations.Where(q =>
                q.QuotationNumber.ToLower().Contains(searchTerm) ||
                (q.Customer != null && q.Customer.CustomerName.ToLower().Contains(searchTerm)) ||
                (q.Customer != null && q.Customer.CustomerCode.ToLower().Contains(searchTerm)) ||
                (q.Remarks != null && q.Remarks.ToLower().Contains(searchTerm))
            );
        }

        public async Task<Quotation> CreateQuotationAsync(Quotation quotation)
        {
            // Set default values
            quotation.Status = "Draft";
            quotation.CreatedDate = DateTime.Now;

            // If created from inquiry, update inquiry status
            if (quotation.InquiryId.HasValue)
            {
                var inquiry = await _inquiryRepository.GetByIdAsync(quotation.InquiryId.Value);
                if (inquiry != null)
                {
                    inquiry.Status = "Quoted";
                    inquiry.ConvertedToQuotationId = quotation.Id;
                    await _inquiryRepository.UpdateAsync(inquiry);
                }
            }

            return await _quotationRepository.AddAsync(quotation);
        }

        public async Task UpdateQuotationAsync(Quotation quotation)
        {
            quotation.ModifiedDate = DateTime.Now;
            await _quotationRepository.UpdateAsync(quotation);
        }

        public async Task DeleteQuotationAsync(int id)
        {
            await _quotationRepository.DeleteAsync(id);
        }

        public async Task<Quotation> AddQuotationItemAsync(int quotationId, QuotationItem item)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                throw new Exception("Quotation not found");

            quotation.QuotationItems.Add(item);
            await RecalculateQuotationTotalsAsync(quotationId);

            return quotation;
        }

        public async Task RemoveQuotationItemAsync(int quotationId, int itemId)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                throw new Exception("Quotation not found");

            var item = quotation.QuotationItems.FirstOrDefault(i => i.Id == itemId);
            if (item != null)
            {
                quotation.QuotationItems.Remove(item);
                await RecalculateQuotationTotalsAsync(quotationId);
            }
        }

        public async Task RecalculateQuotationTotalsAsync(int quotationId)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                return;

            // Calculate subtotal from items
            quotation.SubtotalAmount = quotation.QuotationItems.Sum(i => i.LineTotal);

            // Apply discount
            if (quotation.DiscountPercent.HasValue && quotation.DiscountPercent.Value > 0)
            {
                quotation.DiscountAmount = quotation.SubtotalAmount * (quotation.DiscountPercent.Value / 100);
            }

            // Calculate total (subtotal - discount + tax)
            var amountAfterDiscount = quotation.SubtotalAmount - (quotation.DiscountAmount ?? 0);
            quotation.TotalAmount = amountAfterDiscount + quotation.TaxAmount;

            await _quotationRepository.UpdateAsync(quotation);
        }

        public async Task<bool> ApproveQuotationAsync(int quotationId, int approvedByEmployeeId)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                return false;

            if (quotation.Status != "Draft")
                return false;

            quotation.ApprovedByEmployeeId = approvedByEmployeeId;
            quotation.ApprovalDate = DateTime.Now;
            quotation.Status = "Sent";
            quotation.ModifiedDate = DateTime.Now;

            await _quotationRepository.UpdateAsync(quotation);
            return true;
        }

        public async Task<bool> SendQuotationAsync(int quotationId)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                return false;

            if (quotation.Status != "Draft" && quotation.Status != "Sent")
                return false;

            quotation.Status = "Sent";
            quotation.ModifiedDate = DateTime.Now;

            await _quotationRepository.UpdateAsync(quotation);
            return true;
        }

        public async Task<bool> ConvertToSalesOrderAsync(int quotationId)
        {
            var quotation = await _quotationRepository.GetByIdAsync(quotationId);
            if (quotation == null)
                return false;

            if (quotation.Status != "Accepted")
                return false;

            quotation.Status = "Converted";
            quotation.ModifiedDate = DateTime.Now;

            await _quotationRepository.UpdateAsync(quotation);
            return true;
        }

        public async Task<Dictionary<string, object>> GetQuotationStatisticsAsync()
        {
            var allQuotations = await _quotationRepository.GetAllAsync();

            return new Dictionary<string, object>
            {
                { "TotalQuotations", allQuotations.Count() },
                { "DraftCount", allQuotations.Count(q => q.Status == "Draft") },
                { "SentCount", allQuotations.Count(q => q.Status == "Sent") },
                { "AcceptedCount", allQuotations.Count(q => q.Status == "Accepted") },
                { "RejectedCount", allQuotations.Count(q => q.Status == "Rejected") },
                { "ExpiredCount", allQuotations.Count(q => q.Status == "Expired") },
                { "ConvertedCount", allQuotations.Count(q => q.Status == "Converted") },
                { "TotalValue", allQuotations.Sum(q => q.TotalAmount) },
                { "AverageValue", allQuotations.Any() ? allQuotations.Average(q => q.TotalAmount) : 0 }
            };
        }
    }
}
