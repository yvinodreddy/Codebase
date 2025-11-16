using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using ClosedXML.Excel;
using Microsoft.Extensions.Logging;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Excel export service using ClosedXML with professional formatting
    /// </summary>
    public class ExcelExportService : IExcelExportService
    {
        private readonly ILogger<ExcelExportService> _logger;

        public ExcelExportService(ILogger<ExcelExportService> logger)
        {
            _logger = logger;
        }

        public Task<ExcelExportResult> ExportToExcelAsync(DataTable data, string sheetName)
        {
            var options = new ExcelExportOptions { SheetName = sheetName };
            return ExportToExcelWithFormattingAsync(data, options);
        }

        public Task<ExcelExportResult> ExportToExcelWithFormattingAsync(DataTable data, ExcelExportOptions options)
        {
            return Task.Run(() =>
            {
                try
                {
                    _logger.LogInformation($"Starting Excel export: {data.Rows.Count} rows, {data.Columns.Count} columns");

                using var workbook = new XLWorkbook();
                var worksheet = workbook.Worksheets.Add(options.SheetName);

                // Load data starting at A1
                var table = worksheet.Cell(1, 1).InsertTable(data);
                table.Theme = XLTableTheme.TableStyleMedium2;

                // Apply header formatting
                if (options.ApplyHeaderFormatting)
                {
                    var headerRow = worksheet.Row(1);
                    headerRow.Style.Font.Bold = true;
                    headerRow.Style.Font.FontSize = 11;
                    headerRow.Style.Fill.BackgroundColor = XLColor.FromHtml("#0070C0");
                    headerRow.Style.Font.FontColor = XLColor.White;
                    headerRow.Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;
                    headerRow.Style.Alignment.Vertical = XLAlignmentVerticalValues.Center;
                }

                // Apply alternate row colors
                if (options.ApplyAlternateRowColors)
                {
                    for (int row = 2; row <= data.Rows.Count + 1; row++)
                    {
                        if (row % 2 == 0)
                        {
                            worksheet.Row(row).Style.Fill.BackgroundColor = XLColor.FromHtml("#F2F2F2");
                        }
                    }
                }

                // Apply column-specific formatting
                foreach (var format in options.ColumnFormats)
                {
                    var columnIndex = GetColumnIndex(data, format.ColumnName);
                    if (columnIndex > 0)
                    {
                        var column = worksheet.Column(columnIndex);

                        if (!string.IsNullOrEmpty(format.NumberFormat))
                        {
                            var dataRange = worksheet.Range(2, columnIndex, data.Rows.Count + 1, columnIndex);
                            dataRange.Style.NumberFormat.Format = format.NumberFormat;
                        }

                        if (format.IsBold)
                        {
                            column.Style.Font.Bold = true;
                        }

                        if (!string.IsNullOrEmpty(format.BackgroundColor))
                        {
                            var dataRange = worksheet.Range(2, columnIndex, data.Rows.Count + 1, columnIndex);
                            dataRange.Style.Fill.BackgroundColor = XLColor.FromHtml(format.BackgroundColor);
                        }

                        if (format.ColumnWidth.HasValue)
                        {
                            column.Width = format.ColumnWidth.Value;
                        }
                    }
                }

                // Auto-fit columns
                if (options.AutoFitColumns)
                {
                    worksheet.Columns().AdjustToContents(1, data.Rows.Count + 1);
                    // Set maximum width to prevent extremely wide columns
                    foreach (var column in worksheet.ColumnsUsed())
                    {
                        if (column.Width > 50)
                            column.Width = 50;
                    }
                }

                // Freeze header row
                if (options.FreezePanes)
                {
                    worksheet.SheetView.FreezeRows(1);
                }

                // Apply auto-filter
                if (options.ApplyFilters)
                {
                    table.SetShowAutoFilter(true);
                }

                // Add summary row if requested
                if (options.IncludeSummaryRow)
                {
                    AddSummaryRow(worksheet, data);
                }

                // Add borders to all cells
                var dataRangeWithHeaders = worksheet.Range(1, 1, data.Rows.Count + 1, data.Columns.Count);
                dataRangeWithHeaders.Style.Border.OutsideBorder = XLBorderStyleValues.Thin;
                dataRangeWithHeaders.Style.Border.InsideBorder = XLBorderStyleValues.Thin;

                // Generate file
                using var stream = new MemoryStream();
                workbook.SaveAs(stream);
                var fileData = stream.ToArray();

                    _logger.LogInformation($"Excel export completed successfully. File size: {fileData.Length} bytes");

                    return new ExcelExportResult
                    {
                        Success = true,
                        FileData = fileData,
                        FileName = $"{options.SheetName}_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx",
                        FileSizeBytes = fileData.Length,
                        RowCount = data.Rows.Count,
                        ColumnCount = data.Columns.Count
                    };
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error during Excel export");
                    return new ExcelExportResult
                    {
                        Success = false,
                        ErrorMessage = ex.Message
                    };
                }
            });
        }

        public Task<ExcelExportResult> ExportMultipleSheetsAsync(Dictionary<string, DataTable> sheets)
        {
            return Task.Run(() =>
            {
                try
                {
                    _logger.LogInformation($"Starting multi-sheet Excel export: {sheets.Count} sheets");

                using var workbook = new XLWorkbook();

                foreach (var sheet in sheets)
                {
                    var worksheet = workbook.Worksheets.Add(sheet.Key);
                    var table = worksheet.Cell(1, 1).InsertTable(sheet.Value);
                    table.Theme = XLTableTheme.TableStyleMedium2;

                    // Basic formatting for each sheet
                    worksheet.Row(1).Style.Font.Bold = true;
                    worksheet.Row(1).Style.Fill.BackgroundColor = XLColor.FromHtml("#0070C0");
                    worksheet.Row(1).Style.Font.FontColor = XLColor.White;
                    worksheet.Columns().AdjustToContents();
                    worksheet.SheetView.FreezeRows(1);
                }

                using var stream = new MemoryStream();
                workbook.SaveAs(stream);
                var fileData = stream.ToArray();

                _logger.LogInformation($"Multi-sheet Excel export completed. File size: {fileData.Length} bytes");

                    return new ExcelExportResult
                    {
                        Success = true,
                        FileData = fileData,
                        FileName = $"Report_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx",
                        FileSizeBytes = fileData.Length,
                        RowCount = sheets.Sum(s => s.Value.Rows.Count),
                        ColumnCount = sheets.First().Value.Columns.Count
                    };
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error during multi-sheet Excel export");
                    return new ExcelExportResult
                    {
                        Success = false,
                        ErrorMessage = ex.Message
                    };
                }
            });
        }

        public Task<ExcelExportResult> ExportWithStylingAsync(DataTable data, ExcelExportOptions options)
        {
            // This method provides the same functionality as ExportToExcelWithFormattingAsync
            return ExportToExcelWithFormattingAsync(data, options);
        }

        public async Task<ExcelExportResult> ExportListToExcelAsync<T>(List<T> data, string sheetName) where T : class
        {
            try
            {
                var dataTable = ConvertListToDataTable(data);
                return await ExportToExcelAsync(dataTable, sheetName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error converting list to Excel");
                return new ExcelExportResult
                {
                    Success = false,
                    ErrorMessage = ex.Message
                };
            }
        }

        #region Private Helper Methods

        private int GetColumnIndex(DataTable data, string columnName)
        {
            for (int i = 0; i < data.Columns.Count; i++)
            {
                if (data.Columns[i].ColumnName.Equals(columnName, StringComparison.OrdinalIgnoreCase))
                {
                    return i + 1; // ClosedXML uses 1-based indexing
                }
            }
            return -1;
        }

        private void AddSummaryRow(IXLWorksheet worksheet, DataTable data)
        {
            int summaryRow = data.Rows.Count + 2;
            worksheet.Cell(summaryRow, 1).Value = "TOTAL";
            worksheet.Cell(summaryRow, 1).Style.Font.Bold = true;
            worksheet.Cell(summaryRow, 1).Style.Fill.BackgroundColor = XLColor.FromHtml("#FFD700");

            // Add sum formulas for numeric columns
            for (int col = 1; col <= data.Columns.Count; col++)
            {
                var columnType = data.Columns[col - 1].DataType;
                if (columnType == typeof(int) || columnType == typeof(decimal) ||
                    columnType == typeof(double) || columnType == typeof(float))
                {
                    var cellAddress = worksheet.Cell(summaryRow, col);
                    cellAddress.FormulaA1 = $"SUM({worksheet.Cell(2, col).Address}:{worksheet.Cell(data.Rows.Count + 1, col).Address})";
                    cellAddress.Style.Font.Bold = true;
                    cellAddress.Style.Fill.BackgroundColor = XLColor.FromHtml("#FFD700");
                }
            }
        }

        private DataTable ConvertListToDataTable<T>(List<T> data) where T : class
        {
            var dataTable = new DataTable();
            var properties = typeof(T).GetProperties();

            // Create columns
            foreach (var prop in properties)
            {
                dataTable.Columns.Add(prop.Name, Nullable.GetUnderlyingType(prop.PropertyType) ?? prop.PropertyType);
            }

            // Add rows
            foreach (var item in data)
            {
                var row = dataTable.NewRow();
                foreach (var prop in properties)
                {
                    row[prop.Name] = prop.GetValue(item) ?? DBNull.Value;
                }
                dataTable.Rows.Add(row);
            }

            return dataTable;
        }

        #endregion
    }
}
