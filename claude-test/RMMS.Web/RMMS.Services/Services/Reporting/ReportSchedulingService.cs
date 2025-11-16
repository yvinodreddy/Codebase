using System;
using System.Data;
using System.Threading.Tasks;
using Hangfire;
using Microsoft.Extensions.Logging;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Report scheduling service using Hangfire with email delivery
    /// </summary>
    public class ReportSchedulingService : IReportSchedulingService
    {
        private readonly ILogger<ReportSchedulingService> _logger;
        private readonly IExcelExportService _excelService;
        private readonly IPdfExportService _pdfService;
        private readonly IEmailNotificationService _emailService;

        public ReportSchedulingService(
            ILogger<ReportSchedulingService> logger,
            IExcelExportService excelService,
            IPdfExportService pdfService,
            IEmailNotificationService emailService)
        {
            _logger = logger;
            _excelService = excelService;
            _pdfService = pdfService;
            _emailService = emailService;
        }

        public async Task<string> ScheduleRecurringReportAsync(string reportName, string cronExpression, string recipients)
        {
            try
            {
                _logger.LogInformation($"Scheduling recurring report: {reportName} with cron: {cronExpression}");

                var jobId = $"report-{reportName}";
                RecurringJob.AddOrUpdate(
                    jobId,
                    () => ExecuteScheduledReportAsync(reportName, recipients),
                    cronExpression
                );

                return await Task.FromResult(jobId);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error scheduling recurring report");
                throw;
            }
        }

        public async Task ExecuteScheduledReportAsync(string reportName, string recipients)
        {
            try
            {
                _logger.LogInformation($"Executing scheduled report: {reportName} for recipients: {recipients}");

                // Create sample data for demonstration
                var dataTable = new DataTable(reportName);
                dataTable.Columns.Add("ID", typeof(int));
                dataTable.Columns.Add("Date", typeof(DateTime));
                dataTable.Columns.Add("Description", typeof(string));
                dataTable.Columns.Add("Amount", typeof(decimal));

                for (int i = 1; i <= 10; i++)
                {
                    dataTable.Rows.Add(i, DateTime.Now.AddDays(-i), $"Entry {i}", 100.00m * i);
                }

                // Export to Excel
                var excelResult = await _excelService.ExportToExcelAsync(dataTable, reportName);

                if (excelResult.Success)
                {
                    _logger.LogInformation($"Scheduled report '{reportName}' generated successfully. Size: {excelResult.FileSizeBytes} bytes");

                    // Send email with Excel attachment
                    var emailSubject = $"Scheduled Report: {reportName} - {DateTime.Now:dd MMM yyyy}";
                    var emailBody = $@"
                        <h2>Automated Report: {reportName}</h2>
                        <p>This is your scheduled report generated on {DateTime.Now:dd MMM yyyy HH:mm}.</p>
                        <p><strong>Report Details:</strong></p>
                        <ul>
                            <li>Total Records: {excelResult.RowCount}</li>
                            <li>Columns: {excelResult.ColumnCount}</li>
                            <li>File Size: {excelResult.FileSizeBytes / 1024:N0} KB</li>
                        </ul>
                        <p>Please find the report attached.</p>
                        <p><i>This is an automated report. Please do not reply to this email.</i></p>
                    ";

                    var recipientList = recipients.Split(';', StringSplitOptions.RemoveEmptyEntries);

                    foreach (var recipient in recipientList)
                    {
                        await _emailService.SendEmailWithAttachmentAsync(
                            recipient.Trim(),
                            emailSubject,
                            emailBody,
                            excelResult.FileData,
                            excelResult.FileName,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        );
                    }

                    _logger.LogInformation($"Scheduled report '{reportName}' emailed successfully to {recipientList.Length} recipient(s)");
                }
                else
                {
                    _logger.LogError($"Failed to generate scheduled report '{reportName}': {excelResult.ErrorMessage}");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error executing scheduled report: {reportName}");
                throw;
            }
        }

        public async Task<bool> CancelScheduledReportAsync(string jobId)
        {
            try
            {
                _logger.LogInformation($"Cancelling scheduled report: {jobId}");
                RecurringJob.RemoveIfExists(jobId);
                return await Task.FromResult(true);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cancelling scheduled report");
                return false;
            }
        }
    }
}
