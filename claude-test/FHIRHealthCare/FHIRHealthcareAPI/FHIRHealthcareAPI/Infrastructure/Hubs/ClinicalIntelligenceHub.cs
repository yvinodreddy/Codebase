using Microsoft.AspNetCore.SignalR;
using Microsoft.AspNetCore.Authorization;

namespace FHIRHealthcareAPI.Infrastructure.Hubs
{
    [Authorize]
    public class ClinicalIntelligenceHub : Hub
    {
        private readonly ILogger<ClinicalIntelligenceHub> _logger;

        public ClinicalIntelligenceHub(ILogger<ClinicalIntelligenceHub> logger)
        {
            _logger = logger;
        }

        public override async Task OnConnectedAsync()
        {
            var userId = Context.User?.Identity?.Name;
            _logger.LogInformation($"User {userId} connected to Clinical Intelligence Hub");

            // Add user to their patient group if they're a patient
            if (Context.User.IsInRole("Patient"))
            {
                var patientId = Context.User.FindFirst("FhirPatientId")?.Value;
                if (!string.IsNullOrEmpty(patientId))
                {
                    await Groups.AddToGroupAsync(Context.ConnectionId, $"patient-{patientId}");
                }
            }

            // Add medical staff to provider group
            if (Context.User.IsInRole("Doctor") || Context.User.IsInRole("Nurse"))
            {
                await Groups.AddToGroupAsync(Context.ConnectionId, "providers");
            }

            await base.OnConnectedAsync();
        }

        public async Task SubscribeToPatient(string patientId)
        {
            // Check authorization
            if (Context.User.IsInRole("Doctor") || Context.User.IsInRole("Nurse"))
            {
                await Groups.AddToGroupAsync(Context.ConnectionId, $"patient-{patientId}");
                await Clients.Caller.SendAsync("Subscribed", $"Monitoring patient {patientId}");
            }
        }

        public async Task BroadcastCriticalAlert(CriticalAlert alert)
        {
            // Send to specific patient group
            await Clients.Group($"patient-{alert.PatientId}").SendAsync("CriticalAlert", alert);

            // Also send to all providers
            await Clients.Group("providers").SendAsync("CriticalAlert", alert);

            _logger.LogWarning($"Critical alert for patient {alert.PatientId}: {alert.Message}");
        }

        public async Task NotifyKnowledgeGraphUpdate(string patientId, string updateType)
        {
            await Clients.Group($"patient-{patientId}").SendAsync("KnowledgeGraphUpdated", new
            {
                patientId,
                updateType,
                timestamp = DateTime.UtcNow
            });
        }
    }

    public class CriticalAlert
    {
        public string PatientId { get; set; }
        public string Severity { get; set; }
        public string Message { get; set; }
        public DateTime Timestamp { get; set; }
        public Dictionary<string, object> Data { get; set; }
    }
}