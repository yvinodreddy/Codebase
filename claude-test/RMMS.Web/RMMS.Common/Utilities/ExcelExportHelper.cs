//RMMS.Common / Utilities / ExcelExportHelper.cs
using System;
using System.Data;
using System.IO;
using ClosedXML.Excel;
using RMMS.Common.Utilities;

namespace RMMS.Common.Utilities
{
    public class ExcelExportHelper
    {
        public static byte[] ExportToExcel(DataTable dataTable, string worksheetName)
        {
            using (var workbook = new XLWorkbook())
            {
                var worksheet = workbook.Worksheets.Add(worksheetName);

                // Add headers
                for (int i = 0; i < dataTable.Columns.Count; i++)
                {
                    worksheet.Cell(1, i + 1).Value = dataTable.Columns[i].ColumnName;
                    worksheet.Cell(1, i + 1).Style.Font.Bold = true;
                    worksheet.Cell(1, i + 1).Style.Fill.BackgroundColor = XLColor.LightGray;
                }

                // Add data
                for (int row = 0; row < dataTable.Rows.Count; row++)
                {
                    for (int col = 0; col < dataTable.Columns.Count; col++)
                    {
                        worksheet.Cell(row + 2, col + 1).Value = dataTable.Rows[row][col].ToString();
                    }
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

        public static byte[] ExportMultipleSheets(Dictionary<string, DataTable> sheets)
        {
            using (var workbook = new XLWorkbook())
            {
                foreach (var sheet in sheets)
                {
                    var worksheet = workbook.Worksheets.Add(sheet.Key);
                    var dataTable = sheet.Value;

                    // Add headers with formatting
                    for (int i = 0; i < dataTable.Columns.Count; i++)
                    {
                        var cell = worksheet.Cell(1, i + 1);
                        cell.Value = dataTable.Columns[i].ColumnName;
                        cell.Style.Font.Bold = true;
                        cell.Style.Fill.BackgroundColor = XLColor.FromHtml("#2c3e50");
                        cell.Style.Font.FontColor = XLColor.White;
                        cell.Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;
                    }

                    // Add data with alternating row colors
                    for (int row = 0; row < dataTable.Rows.Count; row++)
                    {
                        for (int col = 0; col < dataTable.Columns.Count; col++)
                        {
                            var cell = worksheet.Cell(row + 2, col + 1);
                            var value = dataTable.Rows[row][col];

                            // Set value based on type
                            if (value != DBNull.Value)
                            {
                                if (value is DateTime)
                                    cell.Value = (DateTime)value;
                                else if (value is decimal || value is double || value is float)
                                    cell.Value = Convert.ToDouble(value);
                                else if (value is int || value is long)
                                    cell.Value = Convert.ToInt32(value);
                                else
                                    cell.Value = value.ToString();
                            }

                            // Alternate row coloring
                            if (row % 2 == 1)
                            {
                                cell.Style.Fill.BackgroundColor = XLColor.FromHtml("#f8f9fa");
                            }
                        }
                    }

                    // Format columns based on data type
                    for (int col = 0; col < dataTable.Columns.Count; col++)
                    {
                        var column = dataTable.Columns[col];
                        if (column.DataType == typeof(DateTime))
                        {
                            worksheet.Column(col + 1).Style.DateFormat.Format = "dd-MMM-yyyy";
                        }
                        else if (column.DataType == typeof(decimal) || column.DataType == typeof(double))
                        {
                            worksheet.Column(col + 1).Style.NumberFormat.Format = "#,##0.00";
                        }
                    }

                    // Auto-fit columns
                    worksheet.Columns().AdjustToContents();

                    // Add borders
                    var range = worksheet.Range(1, 1, dataTable.Rows.Count + 1, dataTable.Columns.Count);
                    range.Style.Border.OutsideBorder = XLBorderStyleValues.Thin;
                    range.Style.Border.InsideBorder = XLBorderStyleValues.Thin;
                }

                using (var stream = new MemoryStream())
                {
                    workbook.SaveAs(stream);
                    return stream.ToArray();
                }
            }
        }
    }
}