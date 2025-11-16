using iTextSharp.text.pdf;
using iTextSharp.text;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RMMS.Services.Helpers
{
    public class PdfExportHelper
    {
        public static byte[] ExportToPdf(DataTable dataTable, string title, string? subtitle = null)
        {
            using (var memoryStream = new MemoryStream())
            {
                // Create document
                Document document = new Document(PageSize.A4.Rotate(), 25, 25, 30, 30);
                PdfWriter writer = PdfWriter.GetInstance(document, memoryStream);

                document.Open();

                // Add title
                Font titleFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 18);
                Paragraph titleParagraph = new Paragraph(title, titleFont);
                titleParagraph.Alignment = Element.ALIGN_CENTER;
                document.Add(titleParagraph);

                // Add subtitle if provided
                if (!string.IsNullOrEmpty(subtitle))
                {
                    Font subtitleFont = FontFactory.GetFont(FontFactory.HELVETICA, 12);
                    Paragraph subtitleParagraph = new Paragraph(subtitle, subtitleFont);
                    subtitleParagraph.Alignment = Element.ALIGN_CENTER;
                    document.Add(subtitleParagraph);
                }

                document.Add(new Paragraph(" ")); // Add space

                // Create table
                PdfPTable pdfTable = new PdfPTable(dataTable.Columns.Count);
                pdfTable.WidthPercentage = 100;

                // Add headers
                Font headerFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 10, BaseColor.WHITE);
                foreach (DataColumn column in dataTable.Columns)
                {
                    PdfPCell cell = new PdfPCell(new Phrase(column.ColumnName, headerFont));
                    cell.BackgroundColor = new BaseColor(44, 62, 80); // Dark blue
                    cell.HorizontalAlignment = Element.ALIGN_CENTER;
                    cell.Padding = 5;
                    pdfTable.AddCell(cell);
                }

                // Add data
                Font dataFont = FontFactory.GetFont(FontFactory.HELVETICA, 9);
                foreach (DataRow row in dataTable.Rows)
                {
                    foreach (var item in row.ItemArray)
                    {
                        PdfPCell cell = new PdfPCell(new Phrase(item?.ToString() ?? "", dataFont));
                        cell.Padding = 5;
                        pdfTable.AddCell(cell);
                    }
                }

                document.Add(pdfTable);

                // Add footer
                document.Add(new Paragraph(" "));
                Font footerFont = FontFactory.GetFont(FontFactory.HELVETICA, 8);
                Paragraph footer = new Paragraph($"Generated on: {DateTime.Now:dd-MMM-yyyy HH:mm}", footerFont);
                footer.Alignment = Element.ALIGN_RIGHT;
                document.Add(footer);

                document.Close();

                return memoryStream.ToArray();
            }
        }

        public static byte[] GenerateInvoicePdf(RiceSales invoice)
        {
            using (var memoryStream = new MemoryStream())
            {
                Document document = new Document(PageSize.A4, 25, 25, 30, 30);
                PdfWriter writer = PdfWriter.GetInstance(document, memoryStream);

                document.Open();

                // Company Header
                Font companyFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 20);
                Paragraph company = new Paragraph("RICE MILL MANAGEMENT SYSTEM", companyFont);
                company.Alignment = Element.ALIGN_CENTER;
                document.Add(company);

                Font addressFont = FontFactory.GetFont(FontFactory.HELVETICA, 10);
                Paragraph address = new Paragraph("Your Address Here\nPhone: +91-XXXXXXXXXX\nGSTIN: YOUR_GSTIN", addressFont);
                address.Alignment = Element.ALIGN_CENTER;
                document.Add(address);

                document.Add(new Paragraph(" "));

                // Invoice Title
                Font invoiceFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 16);
                Paragraph invoiceTitle = new Paragraph("TAX INVOICE", invoiceFont);
                invoiceTitle.Alignment = Element.ALIGN_CENTER;
                document.Add(invoiceTitle);

                document.Add(new Paragraph(" "));

                // Invoice Details Table
                PdfPTable detailsTable = new PdfPTable(2);
                detailsTable.WidthPercentage = 100;
                detailsTable.SetWidths(new float[] { 1, 1 });

                // Left side - Invoice details
                PdfPCell leftCell = new PdfPCell();
                leftCell.Border = Rectangle.NO_BORDER;
                leftCell.AddElement(new Phrase($"Invoice No: {invoice.InvoiceNumber}", addressFont));
                leftCell.AddElement(new Phrase($"Date: {invoice.SaleDate:dd-MMM-yyyy}", addressFont));
                leftCell.AddElement(new Phrase($"Payment Mode: {invoice.PaymentMode}", addressFont));
                detailsTable.AddCell(leftCell);

                // Right side - Buyer details
                PdfPCell rightCell = new PdfPCell();
                rightCell.Border = Rectangle.NO_BORDER;
                rightCell.AddElement(new Phrase("Bill To:", FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 10)));
                rightCell.AddElement(new Phrase(new Chunk(invoice.BuyerName, addressFont)));
                rightCell.AddElement(new Phrase(new Chunk(invoice.BuyerAddress ?? "", addressFont)));
                if (!string.IsNullOrEmpty(invoice.BuyerGSTIN))
                    rightCell.AddElement(new Phrase($"GSTIN: {invoice.BuyerGSTIN}", addressFont));
                detailsTable.AddCell(rightCell);

                document.Add(detailsTable);
                document.Add(new Paragraph(" "));

                // Product Table
                PdfPTable productTable = new PdfPTable(5);
                productTable.WidthPercentage = 100;
                productTable.SetWidths(new float[] { 3, 1, 1, 1, 1 });

                // Headers
                string[] headers = { "Description", "Quantity", "Rate", "Taxable Value", "Total" };
                foreach (string header in headers)
                {
                    PdfPCell cell = new PdfPCell(new Phrase(header, FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 10)));
                    cell.BackgroundColor = BaseColor.LIGHT_GRAY;
                    cell.HorizontalAlignment = Element.ALIGN_CENTER;
                    productTable.AddCell(cell);
                }

                // Product row
                // Fix for CS1503: Ensure the second argument is a Chunk, not a Font
                productTable.AddCell(new Phrase(new Chunk(invoice.RiceGrade, addressFont)));
                productTable.AddCell(new Phrase($"{invoice.Quantity:N2} Kg", addressFont));
                productTable.AddCell(new Phrase($"₹ {invoice.UnitPrice:N2}", addressFont));
                productTable.AddCell(new Phrase($"₹ {invoice.TaxableValue:N2}", addressFont));
                productTable.AddCell(new Phrase($"₹ {invoice.TotalInvoiceValue:N2}", addressFont));

                document.Add(productTable);
                document.Add(new Paragraph(" "));

                // Tax and Total Table
                PdfPTable totalTable = new PdfPTable(2);
                totalTable.WidthPercentage = 50;
                totalTable.HorizontalAlignment = Element.ALIGN_RIGHT;

                if (invoice.Discount > 0)
                {
                    totalTable.AddCell(new Phrase("Discount:", addressFont));
                    totalTable.AddCell(new Phrase($"₹ {invoice.Discount:N2}", addressFont));
                }

                if (invoice.CGSTAmount > 0)
                {
                    totalTable.AddCell(new Phrase("CGST (2.5%):", addressFont));
                    totalTable.AddCell(new Phrase($"₹ {invoice.CGSTAmount:N2}", addressFont));

                    totalTable.AddCell(new Phrase("SGST (2.5%):", addressFont));
                    totalTable.AddCell(new Phrase($"₹ {invoice.SGSTAmount:N2}", addressFont));
                }
                else if (invoice.IGSTAmount > 0)
                {
                    totalTable.AddCell(new Phrase("IGST (5%):", addressFont));
                    totalTable.AddCell(new Phrase($"₹ {invoice.IGSTAmount:N2}", addressFont));
                }

                if (invoice.FreightCharges > 0)
                {
                    totalTable.AddCell(new Phrase("Freight Charges:", addressFont));
                    totalTable.AddCell(new Phrase($"₹ {invoice.FreightCharges:N2}", addressFont));
                }

                // Grand Total
                PdfPCell totalLabelCell = new PdfPCell(new Phrase("GRAND TOTAL:", FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 12)));
                totalLabelCell.BackgroundColor = BaseColor.LIGHT_GRAY;
                totalTable.AddCell(totalLabelCell);

                PdfPCell totalValueCell = new PdfPCell(new Phrase($"₹ {invoice.GrossInvoiceAmount:N2}", FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 12)));
                totalValueCell.BackgroundColor = BaseColor.LIGHT_GRAY;
                totalTable.AddCell(totalValueCell);

                document.Add(totalTable);

                // Footer
                document.Add(new Paragraph(" "));
                document.Add(new Paragraph(" "));
                Paragraph footer = new Paragraph("This is a computer generated invoice", FontFactory.GetFont(FontFactory.HELVETICA, 8));
                footer.Alignment = Element.ALIGN_CENTER;
                document.Add(footer);

                document.Close();

                return memoryStream.ToArray();
            }
        }
    }
}