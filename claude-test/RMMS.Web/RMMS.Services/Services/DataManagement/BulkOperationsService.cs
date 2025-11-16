using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using ClosedXML.Excel;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.DataManagement;
using RMMS.Models.Masters;

namespace RMMS.Services.Services.DataManagement
{
    public class BulkOperationsService : IBulkOperationsService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<BulkOperationsService> _logger;

        public BulkOperationsService(
            ApplicationDbContext context,
            ILogger<BulkOperationsService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<BulkImportResult> ImportProductsFromExcelAsync(Stream fileStream)
        {
            var result = new BulkImportResult();

            try
            {
                using var stream = fileStream;
                using var workbook = new XLWorkbook(stream);
                var worksheet = workbook.Worksheet(1);
                var rangeUsed = worksheet.RangeUsed();
                if (rangeUsed == null)
                {
                    result.Success = false;
                    result.Message = "Empty worksheet";
                    return result;
                }
                var rows = rangeUsed.RowsUsed().Skip(1); // Skip header

                foreach (var row in rows)
                {
                    result.TotalRecords++;

                    try
                    {
                        var product = new Product
                        {
                            ProductCode = row.Cell(1).GetString(),
                            ProductName = row.Cell(2).GetString(),
                            ProductCategory = row.Cell(3).GetString(),
                            ProductType = row.Cell(4).GetString(),
                            UnitOfMeasure = row.Cell(5).GetString(),
                            SellingPrice = row.Cell(6).TryGetValue(out decimal price) ? price : 0,
                            IsActive = true,
                            CreatedDate = DateTime.Now
                        };

                        _context.Products.Add(product);
                        result.SuccessCount++;
                    }
                    catch (Exception ex)
                    {
                        result.FailedCount++;
                        result.Errors.Add($"Row {result.TotalRecords}: {ex.Message}");
                    }
                }

                await _context.SaveChangesAsync();
                result.Success = result.FailedCount == 0;
                result.Message = $"Imported {result.SuccessCount} of {result.TotalRecords} products";
                _logger.LogInformation(result.Message);
            }
            catch (Exception ex)
            {
                result.Success = false;
                result.Message = $"Import failed: {ex.Message}";
                _logger.LogError(ex, "Bulk product import failed");
            }

            return result;
        }

        public async Task<BulkImportResult> ImportCustomersFromExcelAsync(Stream fileStream)
        {
            var result = new BulkImportResult { Success = true, Message = "Customer import not yet implemented" };
            await Task.CompletedTask;
            return result;
        }

        public async Task<byte[]> ExportProductsToExcelAsync()
        {
            var products = await _context.Products
                .Where(p => p.IsActive)
                .Select(p => new
                {
                    p.ProductCode,
                    p.ProductName,
                    p.ProductCategory,
                    p.ProductType,
                    p.UnitOfMeasure,
                    p.SellingPrice,
                    p.CreatedDate
                })
                .ToListAsync();

            using var workbook = new XLWorkbook();
            var worksheet = workbook.Worksheets.Add("Products");

            // Headers
            worksheet.Cell(1, 1).Value = "Code";
            worksheet.Cell(1, 2).Value = "Name";
            worksheet.Cell(1, 3).Value = "Category";
            worksheet.Cell(1, 4).Value = "Type";
            worksheet.Cell(1, 5).Value = "UOM";
            worksheet.Cell(1, 6).Value = "Price";
            worksheet.Cell(1, 7).Value = "Created Date";

            // Data
            int row = 2;
            foreach (var product in products)
            {
                worksheet.Cell(row, 1).Value = product.ProductCode;
                worksheet.Cell(row, 2).Value = product.ProductName;
                worksheet.Cell(row, 3).Value = product.ProductCategory;
                worksheet.Cell(row, 4).Value = product.ProductType;
                worksheet.Cell(row, 5).Value = product.UnitOfMeasure;
                worksheet.Cell(row, 6).Value = product.SellingPrice ?? 0;
                worksheet.Cell(row, 7).Value = product.CreatedDate;
                row++;
            }

            worksheet.Columns().AdjustToContents();

            using var stream = new MemoryStream();
            workbook.SaveAs(stream);
            return stream.ToArray();
        }

        public async Task<byte[]> ExportSalesToExcelAsync(BulkExportOptions options)
        {
            var sales = await _context.RiceSales
                .OrderByDescending(s => s.SaleDate)
                .Take(1000)
                .ToListAsync();

            using var workbook = new XLWorkbook();
            var worksheet = workbook.Worksheets.Add("Sales");

            worksheet.Cell(1, 1).Value = "Invoice #";
            worksheet.Cell(1, 2).Value = "Date";
            worksheet.Cell(1, 3).Value = "Customer";
            worksheet.Cell(1, 4).Value = "Product";
            worksheet.Cell(1, 5).Value = "Quantity";
            worksheet.Cell(1, 6).Value = "Amount";

            int row = 2;
            foreach (var sale in sales)
            {
                worksheet.Cell(row, 1).Value = sale.InvoiceNumber;
                worksheet.Cell(row, 2).Value = sale.SaleDate;
                worksheet.Cell(row, 3).Value = sale.BuyerName;
                worksheet.Cell(row, 4).Value = sale.RiceGrade;
                worksheet.Cell(row, 5).Value = sale.Quantity;
                worksheet.Cell(row, 6).Value = sale.TotalInvoiceValue;
                row++;
            }

            worksheet.Columns().AdjustToContents();

            using var stream = new MemoryStream();
            workbook.SaveAs(stream);
            return stream.ToArray();
        }

        public async Task<byte[]> ExportInventoryToExcelAsync()
        {
            var products = await _context.Products.Where(p => p.IsActive).ToListAsync();

            using var workbook = new XLWorkbook();
            var worksheet = workbook.Worksheets.Add("Inventory");

            worksheet.Cell(1, 1).Value = "Product";
            worksheet.Cell(1, 2).Value = "Category";
            worksheet.Cell(1, 3).Value = "UOM";
            worksheet.Cell(1, 4).Value = "Min Stock";

            int row = 2;
            foreach (var product in products)
            {
                worksheet.Cell(row, 1).Value = product.ProductName;
                worksheet.Cell(row, 2).Value = product.ProductCategory;
                worksheet.Cell(row, 3).Value = product.UnitOfMeasure;
                worksheet.Cell(row, 4).Value = product.MinimumStockLevel ?? 0;
                row++;
            }

            worksheet.Columns().AdjustToContents();

            using var stream = new MemoryStream();
            workbook.SaveAs(stream);
            return stream.ToArray();
        }
    }
}
