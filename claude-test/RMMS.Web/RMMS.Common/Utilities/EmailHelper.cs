//RMMS.Common / Utilities / EmailHelper.cs
using RMMS.Common.Utilities;
using System.Net.Mail;
using System.Net;
using System;
using System.Threading.Tasks;

namespace RMMS.Common.Utilities
{
    public class EmailHelper
    {
        private readonly string _smtpHost;
        private readonly int _smtpPort;
        private readonly string _smtpUsername;
        private readonly string _smtpPassword;
        private readonly string _fromEmail;

        public EmailHelper(string smtpHost, int smtpPort, string username, string password, string fromEmail)
        {
            _smtpHost = smtpHost;
            _smtpPort = smtpPort;
            _smtpUsername = username;
            _smtpPassword = password;
            _fromEmail = fromEmail;
        }

        public async Task SendEmailAsync(string toEmail, string subject, string body, bool isHtml = true)
        {
            using (var client = new SmtpClient(_smtpHost, _smtpPort))
            {
                client.EnableSsl = true;
                client.Credentials = new NetworkCredential(_smtpUsername, _smtpPassword);

                var mailMessage = new MailMessage
                {
                    From = new MailAddress(_fromEmail),
                    Subject = subject,
                    Body = body,
                    IsBodyHtml = isHtml
                };

                mailMessage.To.Add(toEmail);

                await client.SendMailAsync(mailMessage);
            }
        }

        public async Task SendInvoiceEmailAsync(string toEmail, string customerName, string invoiceNumber, byte[] pdfAttachment)
        {
            string subject = $"Invoice {invoiceNumber} - Rice Mill Management System";
            string body = $@"
                <html>
                <body>
                    <h2>Dear {customerName},</h2>
                    <p>Please find attached invoice number <strong>{invoiceNumber}</strong> for your recent purchase.</p>
                    <p>If you have any questions, please don't hesitate to contact us.</p>
                    <br>
                    <p>Best regards,<br>
                    Rice Mill Management System<br>
                    Email: support@rmms.com<br>
                    Phone: +91-XXXXXXXXXX</p>
                </body>
                </html>";

            using (var client = new SmtpClient(_smtpHost, _smtpPort))
            {
                client.EnableSsl = true;
                client.Credentials = new NetworkCredential(_smtpUsername, _smtpPassword);

                var mailMessage = new MailMessage
                {
                    From = new MailAddress(_fromEmail),
                    Subject = subject,
                    Body = body,
                    IsBodyHtml = true
                };

                mailMessage.To.Add(toEmail);

                // Add PDF attachment
                var attachment = new Attachment(new MemoryStream(pdfAttachment), $"Invoice_{invoiceNumber}.pdf", "application/pdf");
                mailMessage.Attachments.Add(attachment);

                await client.SendMailAsync(mailMessage);
            }
        }
    }
}