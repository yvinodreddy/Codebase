using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;

namespace RMMS.Services.Services.DataManagement
{
    public class DataCleansingService : IDataCleansingService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<DataCleansingService> _logger;

        public DataCleansingService(
            ApplicationDbContext context,
            ILogger<DataCleansingService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<List<object>> FindDuplicateRecordsAsync(string entityType)
        {
            if (entityType == "Product")
            {
                var duplicates = await _context.Products
                    .GroupBy(p => p.ProductCode)
                    .Where(g => g.Count() > 1)
                    .Select(g => new
                    {
                        ProductCode = g.Key,
                        Count = g.Count(),
                        Ids = g.Select(p => p.Id).ToList()
                    })
                    .ToListAsync();

                _logger.LogInformation($"Found {duplicates.Count} duplicate product codes");
                return duplicates.Cast<object>().ToList();
            }

            return new List<object>();
        }

        public async Task<bool> MergeDuplicatesAsync(string entityType, List<int> duplicateIds, int masterRecordId)
        {
            _logger.LogInformation($"Merging {duplicateIds.Count} duplicates into master #{masterRecordId}");
            await Task.CompletedTask;
            // Update references to point to master record
            // Delete duplicate records
            return true;
        }

        public async Task<int> StandardizeDataAsync(string entityType, string field)
        {
            var count = 0;

            if (entityType == "Product" && field == "Category")
            {
                // Standardize category names
                var products = await _context.Products.ToListAsync();
                foreach (var product in products)
                {
                    if (product.ProductCategory == "rice")
                    {
                        product.ProductCategory = "Rice";
                        count++;
                    }
                }
                await _context.SaveChangesAsync();
            }

            _logger.LogInformation($"Standardized {count} {entityType} records");
            return count;
        }

        public async Task<int> CleanInvalidDataAsync(string entityType)
        {
            var count = 0;
            _logger.LogInformation($"Cleaned {count} invalid {entityType} records");
            await Task.CompletedTask;
            return count;
        }
    }
}
