using System;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// PDF export service using QuestPDF
    /// </summary>
    public class PdfExportService : IPdfExportService
    {
        private readonly ILogger<PdfExportService> _logger;

        public PdfExportService(ILogger<PdfExportService> logger)
        {
            _logger = logger;
            QuestPDF.Settings.License = LicenseType.Community;
        }

        public async Task<byte[]> GenerateSimplePdfAsync(DataTable data, string title)
        {
            var options = new PdfReportOptions { Title = title };
            return await GeneratePdfReportAsync(data, options);
        }

        public async Task<byte[]> GeneratePdfReportAsync(DataTable data, PdfReportOptions options)
        {
            try
            {
                _logger.LogInformation($"Generating PDF report: {data.Rows.Count} rows");

                var document = Document.Create(container =>
                {
                    container.Page(page =>
                    {
                        page.Size(PageSizes.A4);
                        page.Margin(1.5f, Unit.Centimetre);
                        page.PageColor(Colors.White);
                        page.DefaultTextStyle(x => x.FontSize(9));

                        page.Header().Element(c => ComposeHeader(c, options));
                        page.Content().Element(c => ComposeContent(c, data, options));
                        page.Footer().Element(c => ComposeFooter(c, options));
                    });
                });

                var pdfBytes = document.GeneratePdf();
                _logger.LogInformation($"PDF generated successfully. Size: {pdfBytes.Length} bytes");

                return await Task.FromResult(pdfBytes);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating PDF report");
                throw;
            }
        }

        private void ComposeHeader(IContainer container, PdfReportOptions options)
        {
            container.Column(column =>
            {
                // Company name
                column.Item().AlignCenter().Text(options.CompanyName)
                    .FontSize(10).Bold().FontColor(Colors.Blue.Medium);

                // Title
                column.Item().AlignCenter().Text(options.Title)
                    .FontSize(16).Bold().FontColor(Colors.Black);

                // Subtitle
                if (!string.IsNullOrEmpty(options.Subtitle))
                {
                    column.Item().AlignCenter().Text(options.Subtitle)
                        .FontSize(11).Italic().FontColor(Colors.Grey.Darken2);
                }

                // Generated date
                if (options.IncludeGeneratedDate)
                {
                    column.Item().AlignCenter().Text($"Generated: {DateTime.Now:dd-MMM-yyyy HH:mm}")
                        .FontSize(8).FontColor(Colors.Grey.Medium);
                }

                // Separator line
                column.Item().PaddingTop(10).BorderBottom(1).BorderColor(Colors.Blue.Medium);
            });
        }

        private void ComposeContent(IContainer container, DataTable data, PdfReportOptions options)
        {
            container.PaddingTop(15).Column(column =>
            {
                // Add watermark if requested
                if (options.IncludeWatermark)
                {
                    column.Item().AlignCenter().Text(options.WatermarkText)
                        .FontSize(40).Bold().FontColor(Colors.Grey.Lighten3);
                }

                // Data table
                column.Item().Table(table =>
                {
                    // Define columns
                    table.ColumnsDefinition(columns =>
                    {
                        foreach (DataColumn col in data.Columns)
                        {
                            columns.RelativeColumn();
                        }
                    });

                    // Header row
                    table.Header(header =>
                    {
                        foreach (DataColumn col in data.Columns)
                        {
                            header.Cell().Element(CellStyle)
                                .Background(Colors.Blue.Medium)
                                .Padding(5)
                                .Text(col.ColumnName)
                                .FontColor(Colors.White)
                                .FontSize(9)
                                .Bold();
                        }
                    });

                    // Data rows
                    int rowIndex = 0;
                    foreach (DataRow row in data.Rows)
                    {
                        var isAlternate = rowIndex % 2 == 0;
                        foreach (var item in row.ItemArray)
                        {
                            var cell = table.Cell().Element(CellStyle).Padding(5);

                            if (isAlternate)
                            {
                                cell.Background(Colors.Grey.Lighten4);
                            }

                            cell.Text(FormatCellValue(item)).FontSize(8);
                        }
                        rowIndex++;
                    }
                });

                // Summary
                column.Item().PaddingTop(10).Text($"Total Records: {data.Rows.Count}")
                    .FontSize(9).Bold();
            });
        }

        private void ComposeFooter(IContainer container, PdfReportOptions options)
        {
            container.AlignCenter().Row(row =>
            {
                row.RelativeItem().Column(column =>
                {
                    if (options.IncludePageNumbers)
                    {
                        column.Item().AlignCenter().DefaultTextStyle(x => x.FontSize(8).FontColor(Colors.Grey.Medium)).Text(text =>
                        {
                            text.Span("Page ");
                            text.CurrentPageNumber();
                            text.Span(" of ");
                            text.TotalPages();
                        });
                    }
                });
            });
        }

        private IContainer CellStyle(IContainer container)
        {
            return container
                .Border(0.5f)
                .BorderColor(Colors.Grey.Lighten2);
        }

        private string FormatCellValue(object? value)
        {
            if (value == null || value == DBNull.Value)
                return "-";

            if (value is DateTime dateTime)
                return dateTime.ToString("dd-MMM-yyyy");

            if (value is decimal || value is double || value is float)
            {
                var numValue = Convert.ToDecimal(value);
                return numValue.ToString("N2");
            }

            return value.ToString() ?? "-";
        }
    }
}
