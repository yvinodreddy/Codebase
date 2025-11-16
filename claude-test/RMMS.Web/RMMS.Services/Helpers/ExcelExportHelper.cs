using ClosedXML.Excel;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace RMMS.Services.Helpers
{
    public static class ExcelExportHelper
    {
        public static byte[] ExportToExcel<T>(
            List<T> data,
            string sheetName,
            string reportTitle,
            Dictionary<string, Func<T, object>> columnMappings)
        {
            using (var workbook = new XLWorkbook())
            {
                var worksheet = workbook.Worksheets.Add(sheetName);

                // Add title
                worksheet.Cell(1, 1).Value = reportTitle;
                worksheet.Cell(1, 1).Style.Font.Bold = true;
                worksheet.Cell(1, 1).Style.Font.FontSize = 16;
                worksheet.Range(1, 1, 1, columnMappings.Count).Merge();
                worksheet.Range(1, 1, 1, columnMappings.Count).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;

                // Add generation date
                worksheet.Cell(2, 1).Value = $"Generated: {DateTime.Now:dd-MMM-yyyy HH:mm}";
                worksheet.Cell(2, 1).Style.Font.FontSize = 10;
                worksheet.Range(2, 1, 2, columnMappings.Count).Merge();

                // Add empty row
                int currentRow = 4;

                // Add headers
                int col = 1;
                foreach (var columnName in columnMappings.Keys)
                {
                    var cell = worksheet.Cell(currentRow, col);
                    cell.Value = columnName;
                    cell.Style.Font.Bold = true;
                    cell.Style.Fill.BackgroundColor = XLColor.LightGray;
                    cell.Style.Border.OutsideBorder = XLBorderStyleValues.Thin;
                    col++;
                }

                currentRow++;

                // Add data rows
                foreach (var item in data)
                {
                    col = 1;
                    foreach (var mapping in columnMappings.Values)
                    {
                        var value = mapping(item);
                        var cell = worksheet.Cell(currentRow, col);

                        if (value != null)
                        {
                            if (value is decimal decimalValue)
                            {
                                cell.Value = decimalValue;
                                cell.Style.NumberFormat.Format = "#,##0.00";
                            }
                            else if (value is DateTime dateValue)
                            {
                                cell.Value = dateValue;
                                cell.Style.DateFormat.Format = "dd-MMM-yyyy";
                            }
                            else if (value is int || value is long)
                            {
                                cell.Value = Convert.ToDouble(value);
                                cell.Style.NumberFormat.Format = "#,##0";
                            }
                            else
                            {
                                cell.Value = value.ToString();
                            }
                        }

                        cell.Style.Border.OutsideBorder = XLBorderStyleValues.Thin;
                        col++;
                    }
                    currentRow++;
                }

                // Auto-fit columns
                worksheet.Columns().AdjustToContents();

                // Save to memory stream
                using (var stream = new MemoryStream())
                {
                    workbook.SaveAs(stream);
                    return stream.ToArray();
                }
            }
        }

        public static byte[] ExportSalesToExcel(
            string reportTitle,
            List<(DateTime Date, string Customer, string Product, decimal Quantity, decimal Amount)> sales,
            DateTime? fromDate = null,
            DateTime? toDate = null)
        {
            using (var workbook = new XLWorkbook())
            {
                var worksheet = workbook.Worksheets.Add("Sales Report");

                // Add title
                worksheet.Cell(1, 1).Value = reportTitle;
                worksheet.Cell(1, 1).Style.Font.Bold = true;
                worksheet.Cell(1, 1).Style.Font.FontSize = 16;
                worksheet.Range(1, 1, 1, 5).Merge();
                worksheet.Range(1, 1, 1, 5).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;

                // Add period if provided
                if (fromDate.HasValue && toDate.HasValue)
                {
                    worksheet.Cell(2, 1).Value = $"Period: {fromDate:dd-MMM-yyyy} to {toDate:dd-MMM-yyyy}";
                    worksheet.Range(2, 1, 2, 5).Merge();
                }

                // Add generation date
                worksheet.Cell(3, 1).Value = $"Generated: {DateTime.Now:dd-MMM-yyyy HH:mm}";
                worksheet.Range(3, 1, 3, 5).Merge();

                int currentRow = 5;

                // Headers
                worksheet.Cell(currentRow, 1).Value = "Date";
                worksheet.Cell(currentRow, 2).Value = "Customer";
                worksheet.Cell(currentRow, 3).Value = "Product";
                worksheet.Cell(currentRow, 4).Value = "Quantity (kg)";
                worksheet.Cell(currentRow, 5).Value = "Amount (₹)";

                var headerRange = worksheet.Range(currentRow, 1, currentRow, 5);
                headerRange.Style.Font.Bold = true;
                headerRange.Style.Fill.BackgroundColor = XLColor.LightBlue;
                headerRange.Style.Border.OutsideBorder = XLBorderStyleValues.Medium;

                currentRow++;

                // Data rows
                decimal totalQuantity = 0;
                decimal totalAmount = 0;

                foreach (var sale in sales)
                {
                    worksheet.Cell(currentRow, 1).Value = sale.Date;
                    worksheet.Cell(currentRow, 1).Style.DateFormat.Format = "dd-MMM-yyyy";

                    worksheet.Cell(currentRow, 2).Value = sale.Customer;
                    worksheet.Cell(currentRow, 3).Value = sale.Product;

                    worksheet.Cell(currentRow, 4).Value = sale.Quantity;
                    worksheet.Cell(currentRow, 4).Style.NumberFormat.Format = "#,##0.00";

                    worksheet.Cell(currentRow, 5).Value = sale.Amount;
                    worksheet.Cell(currentRow, 5).Style.NumberFormat.Format = "#,##0.00";

                    totalQuantity += sale.Quantity;
                    totalAmount += sale.Amount;

                    currentRow++;
                }

                // Total row
                worksheet.Cell(currentRow, 1).Value = "TOTAL";
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Range(currentRow, 1, currentRow, 3).Merge();
                worksheet.Range(currentRow, 1, currentRow, 3).Style.Fill.BackgroundColor = XLColor.LightGray;

                worksheet.Cell(currentRow, 4).Value = totalQuantity;
                worksheet.Cell(currentRow, 4).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 4).Style.NumberFormat.Format = "#,##0.00";
                worksheet.Cell(currentRow, 4).Style.Fill.BackgroundColor = XLColor.LightGray;

                worksheet.Cell(currentRow, 5).Value = totalAmount;
                worksheet.Cell(currentRow, 5).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 5).Style.NumberFormat.Format = "#,##0.00";
                worksheet.Cell(currentRow, 5).Style.Fill.BackgroundColor = XLColor.LightGray;

                // Auto-fit columns
                worksheet.Columns().AdjustToContents();

                using (var stream = new MemoryStream())
                {
                    workbook.SaveAs(stream);
                    return stream.ToArray();
                }
            }
        }

        public static byte[] ExportProfitLossToExcel(
            decimal totalIncome,
            decimal totalExpenses,
            decimal netProfit,
            List<(string Category, decimal Amount)> incomeBreakdown,
            List<(string Category, decimal Amount)> expenseBreakdown,
            DateTime fromDate,
            DateTime toDate)
        {
            using (var workbook = new XLWorkbook())
            {
                var worksheet = workbook.Worksheets.Add("Profit & Loss");

                // Title
                worksheet.Cell(1, 1).Value = "PROFIT & LOSS STATEMENT";
                worksheet.Cell(1, 1).Style.Font.Bold = true;
                worksheet.Cell(1, 1).Style.Font.FontSize = 16;
                worksheet.Range(1, 1, 1, 2).Merge();
                worksheet.Range(1, 1, 1, 2).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;

                // Period
                worksheet.Cell(2, 1).Value = $"Period: {fromDate:dd-MMM-yyyy} to {toDate:dd-MMM-yyyy}";
                worksheet.Range(2, 1, 2, 2).Merge();

                int currentRow = 4;

                // Income Section
                worksheet.Cell(currentRow, 1).Value = "INCOME";
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 1).Style.Font.FontSize = 14;
                worksheet.Cell(currentRow, 1).Style.Font.FontColor = XLColor.Green;
                currentRow++;

                worksheet.Cell(currentRow, 1).Value = "Category";
                worksheet.Cell(currentRow, 2).Value = "Amount (₹)";
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Font.Bold = true;
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Fill.BackgroundColor = XLColor.LightGray;
                currentRow++;

                foreach (var item in incomeBreakdown)
                {
                    worksheet.Cell(currentRow, 1).Value = item.Category;
                    worksheet.Cell(currentRow, 2).Value = item.Amount;
                    worksheet.Cell(currentRow, 2).Style.NumberFormat.Format = "#,##0.00";
                    currentRow++;
                }

                worksheet.Cell(currentRow, 1).Value = "Total Income";
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 2).Value = totalIncome;
                worksheet.Cell(currentRow, 2).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 2).Style.NumberFormat.Format = "#,##0.00";
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Fill.BackgroundColor = XLColor.LightGreen;
                currentRow += 2;

                // Expenses Section
                worksheet.Cell(currentRow, 1).Value = "EXPENSES";
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 1).Style.Font.FontSize = 14;
                worksheet.Cell(currentRow, 1).Style.Font.FontColor = XLColor.Red;
                currentRow++;

                worksheet.Cell(currentRow, 1).Value = "Category";
                worksheet.Cell(currentRow, 2).Value = "Amount (₹)";
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Font.Bold = true;
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Fill.BackgroundColor = XLColor.LightGray;
                currentRow++;

                foreach (var item in expenseBreakdown)
                {
                    worksheet.Cell(currentRow, 1).Value = item.Category;
                    worksheet.Cell(currentRow, 2).Value = item.Amount;
                    worksheet.Cell(currentRow, 2).Style.NumberFormat.Format = "#,##0.00";
                    currentRow++;
                }

                worksheet.Cell(currentRow, 1).Value = "Total Expenses";
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 2).Value = totalExpenses;
                worksheet.Cell(currentRow, 2).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 2).Style.NumberFormat.Format = "#,##0.00";
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Fill.BackgroundColor = XLColor.LightPink;
                currentRow += 2;

                // Net Profit/Loss
                var profitLabel = netProfit >= 0 ? "NET PROFIT" : "NET LOSS";
                var bgColor = netProfit >= 0 ? XLColor.LightGreen : XLColor.LightPink;

                worksheet.Cell(currentRow, 1).Value = profitLabel;
                worksheet.Cell(currentRow, 1).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 1).Style.Font.FontSize = 14;
                worksheet.Cell(currentRow, 2).Value = Math.Abs(netProfit);
                worksheet.Cell(currentRow, 2).Style.Font.Bold = true;
                worksheet.Cell(currentRow, 2).Style.Font.FontSize = 14;
                worksheet.Cell(currentRow, 2).Style.NumberFormat.Format = "#,##0.00";
                worksheet.Range(currentRow, 1, currentRow, 2).Style.Fill.BackgroundColor = bgColor;

                worksheet.Columns().AdjustToContents();

                using (var stream = new MemoryStream())
                {
                    workbook.SaveAs(stream);
                    return stream.ToArray();
                }
            }
        }
    }
}
