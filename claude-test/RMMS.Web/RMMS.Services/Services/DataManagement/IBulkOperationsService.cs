using System.IO;
using System.Threading.Tasks;
using RMMS.Models.DataManagement;

namespace RMMS.Services.Services.DataManagement
{
    public interface IBulkOperationsService
    {
        Task<BulkImportResult> ImportProductsFromExcelAsync(Stream fileStream);
        Task<BulkImportResult> ImportCustomersFromExcelAsync(Stream fileStream);
        Task<byte[]> ExportProductsToExcelAsync();
        Task<byte[]> ExportSalesToExcelAsync(BulkExportOptions options);
        Task<byte[]> ExportInventoryToExcelAsync();
    }
}
