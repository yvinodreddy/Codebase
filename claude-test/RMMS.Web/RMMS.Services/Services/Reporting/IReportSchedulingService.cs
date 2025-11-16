using System.Threading.Tasks;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Service for scheduling automated reports using Hangfire
    /// </summary>
    public interface IReportSchedulingService
    {
        /// <summary>
        /// Schedule a recurring report
        /// </summary>
        Task<string> ScheduleRecurringReportAsync(string reportName, string cronExpression, string recipients);

        /// <summary>
        /// Execute scheduled report immediately
        /// </summary>
        Task ExecuteScheduledReportAsync(string reportName, string recipients);

        /// <summary>
        /// Cancel scheduled report
        /// </summary>
        Task<bool> CancelScheduledReportAsync(string jobId);
    }
}
