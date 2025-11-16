using System.Net;
using System.Net.Mail;
using Microsoft.Extensions.Configuration;
using RMMS.Models.Sales;

namespace RMMS.Services.Services
{
    public interface IEmailNotificationService
    {
        Task<bool> SendQuotationEmail(int quotationId);
        Task<bool> SendOrderConfirmation(int salesOrderId);
        Task<bool> SendCreditLimitAlert(int customerId);
        Task<bool> SendPaymentReminder(int customerId, decimal amount, DateTime dueDate);
        Task<bool> SendInvoice(int invoiceId);
        Task<bool> SendCustomEmail(string to, string subject, string body);
        Task<bool> SendBulkEmail(List<string> recipients, string subject, string body);
        Task<bool> SendEmailWithAttachmentAsync(string to, string subject, string body, byte[] attachmentData, string attachmentFileName, string contentType);
    }

    public class EmailNotificationService : IEmailNotificationService
    {
        private readonly IConfiguration _configuration;
        private readonly string _smtpServer;
        private readonly int _smtpPort;
        private readonly string _smtpUsername;
        private readonly string _smtpPassword;
        private readonly string _fromEmail;
        private readonly string _fromName;
        private readonly bool _enableSsl;

        public EmailNotificationService(IConfiguration configuration)
        {
            _configuration = configuration;
            _smtpServer = _configuration["EmailSettings:SmtpServer"] ?? "smtp.gmail.com";
            _smtpPort = int.Parse(_configuration["EmailSettings:SmtpPort"] ?? "587");
            _smtpUsername = _configuration["EmailSettings:Username"] ?? "";
            _smtpPassword = _configuration["EmailSettings:Password"] ?? "";
            _fromEmail = _configuration["EmailSettings:FromEmail"] ?? "noreply@rmms.com";
            _fromName = _configuration["EmailSettings:FromName"] ?? "RMMS System";
            _enableSsl = bool.Parse(_configuration["EmailSettings:EnableSsl"] ?? "true");
        }

        public async Task<bool> SendQuotationEmail(int quotationId)
        {
            // Implementation would fetch quotation details and send email
            var subject = $"Quotation #{quotationId} - RMMS";
            var body = GenerateQuotationEmailBody(quotationId);

            // In production, fetch customer email from database
            var customerEmail = "customer@example.com"; // Placeholder

            return await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task<bool> SendOrderConfirmation(int salesOrderId)
        {
            var subject = $"Order Confirmation #{salesOrderId} - RMMS";
            var body = $@"
                <html>
                <body>
                    <h2>Order Confirmation</h2>
                    <p>Dear Customer,</p>
                    <p>Your order #{salesOrderId} has been confirmed.</p>
                    <p>Thank you for your business!</p>
                    <br/>
                    <p>Best Regards,<br/>RMMS Team</p>
                </body>
                </html>
            ";

            var customerEmail = "customer@example.com"; // Fetch from DB
            return await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task<bool> SendCreditLimitAlert(int customerId)
        {
            var subject = "Credit Limit Alert - RMMS";
            var body = $@"
                <html>
                <body>
                    <h2>Credit Limit Alert</h2>
                    <p>Dear Customer,</p>
                    <p>Your credit limit has been reached or exceeded.</p>
                    <p>Please clear your outstanding dues to continue business operations.</p>
                    <p>For queries, contact our accounts department.</p>
                    <br/>
                    <p>Best Regards,<br/>RMMS Accounts Team</p>
                </body>
                </html>
            ";

            var customerEmail = "customer@example.com"; // Fetch from DB
            return await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task<bool> SendPaymentReminder(int customerId, decimal amount, DateTime dueDate)
        {
            var subject = "Payment Reminder - RMMS";
            var body = $@"
                <html>
                <body>
                    <h2>Payment Reminder</h2>
                    <p>Dear Customer,</p>
                    <p>This is a friendly reminder that a payment of <strong>₹{amount:N2}</strong> is due on {dueDate:dd-MMM-yyyy}.</p>
                    <p>Please arrange for timely payment to avoid any service disruption.</p>
                    <br/>
                    <p>Best Regards,<br/>RMMS Accounts Team</p>
                </body>
                </html>
            ";

            var customerEmail = "customer@example.com"; // Fetch from DB
            return await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task<bool> SendInvoice(int invoiceId)
        {
            var subject = $"Invoice #{invoiceId} - RMMS";
            var body = $@"
                <html>
                <body>
                    <h2>Invoice</h2>
                    <p>Dear Customer,</p>
                    <p>Please find attached invoice #{invoiceId}.</p>
                    <p>Payment due within 30 days.</p>
                    <br/>
                    <p>Best Regards,<br/>RMMS Team</p>
                </body>
                </html>
            ";

            var customerEmail = "customer@example.com"; // Fetch from DB
            return await SendEmailAsync(customerEmail, subject, body);
        }

        public async Task<bool> SendCustomEmail(string to, string subject, string body)
        {
            return await SendEmailAsync(to, subject, body);
        }

        public async Task<bool> SendBulkEmail(List<string> recipients, string subject, string body)
        {
            var tasks = recipients.Select(email => SendEmailAsync(email, subject, body));
            var results = await Task.WhenAll(tasks);
            return results.All(r => r);
        }

        public async Task<bool> SendEmailWithAttachmentAsync(string to, string subject, string body, byte[] attachmentData, string attachmentFileName, string contentType)
        {
            try
            {
                using var mail = new MailMessage();
                mail.From = new MailAddress(_fromEmail, _fromName);
                mail.To.Add(to);
                mail.Subject = subject;
                mail.Body = body;
                mail.IsBodyHtml = true;

                // Add attachment
                if (attachmentData != null && attachmentData.Length > 0)
                {
                    using var stream = new MemoryStream(attachmentData);
                    var attachment = new Attachment(stream, attachmentFileName, contentType);
                    mail.Attachments.Add(attachment);

                    using var smtp = new SmtpClient(_smtpServer, _smtpPort);
                    smtp.Credentials = new NetworkCredential(_smtpUsername, _smtpPassword);
                    smtp.EnableSsl = _enableSsl;

                    await smtp.SendMailAsync(mail);
                }

                return true;
            }
            catch (Exception ex)
            {
                // Log exception
                Console.WriteLine($"Email with attachment send failed: {ex.Message}");
                return false;
            }
        }

        private async Task<bool> SendEmailAsync(string to, string subject, string body)
        {
            try
            {
                using var mail = new MailMessage();
                mail.From = new MailAddress(_fromEmail, _fromName);
                mail.To.Add(to);
                mail.Subject = subject;
                mail.Body = body;
                mail.IsBodyHtml = true;

                using var smtp = new SmtpClient(_smtpServer, _smtpPort);
                smtp.Credentials = new NetworkCredential(_smtpUsername, _smtpPassword);
                smtp.EnableSsl = _enableSsl;

                await smtp.SendMailAsync(mail);
                return true;
            }
            catch (Exception ex)
            {
                // Log exception (implement logging)
                Console.WriteLine($"Email send failed: {ex.Message}");
                return false;
            }
        }

        private string GenerateQuotationEmailBody(int quotationId)
        {
            return $@"
                <html>
                <body style='font-family: Arial, sans-serif;'>
                    <div style='max-width: 600px; margin: 0 auto; padding: 20px;'>
                        <h2 style='color: #333;'>Quotation #{quotationId}</h2>
                        <p>Dear Valued Customer,</p>
                        <p>Thank you for your inquiry. Please find below our quotation for your consideration.</p>

                        <div style='background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;'>
                            <h3>Quotation Details</h3>
                            <p><strong>Quote ID:</strong> {quotationId}</p>
                            <p><strong>Valid Until:</strong> [Expiry Date]</p>
                        </div>

                        <p>This quotation is valid for 15 days from the date of issue.</p>
                        <p>For any queries, please feel free to contact us.</p>

                        <br/>
                        <p>Best Regards,<br/>
                        <strong>RMMS Sales Team</strong><br/>
                        Email: sales@rmms.com<br/>
                        Phone: +91-XXXXXXXXXX</p>
                    </div>
                </body>
                </html>
            ";
        }
    }

    // Email Settings Model
    public class EmailSettings
    {
        public string SmtpServer { get; set; } = string.Empty;
        public int SmtpPort { get; set; }
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string FromEmail { get; set; } = string.Empty;
        public string FromName { get; set; } = string.Empty;
        public bool EnableSsl { get; set; } = true;
    }
}
