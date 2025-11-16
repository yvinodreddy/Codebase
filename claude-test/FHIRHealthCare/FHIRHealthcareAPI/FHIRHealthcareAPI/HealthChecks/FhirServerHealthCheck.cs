using System;
using System.Threading;
using System.Threading.Tasks;
using Hl7.Fhir.Rest;
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace FHIRHealthcareAPI.HealthChecks
{
    public class FhirServerHealthCheck : IHealthCheck
    {
        private readonly FhirClient _fhirClient;

        public FhirServerHealthCheck()
        {
            _fhirClient = new FhirClient("http://localhost:8080/fhir")
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json,
                    Timeout = 5000
                }
            };
        }

        public async Task<HealthCheckResult> CheckHealthAsync(
            HealthCheckContext context,
            CancellationToken cancellationToken = default)
        {
            try
            {
                var metadata = await _fhirClient.CapabilityStatementAsync();

                if (metadata != null)
                {
                    return HealthCheckResult.Healthy("FHIR server is accessible");
                }

                return HealthCheckResult.Unhealthy("FHIR server metadata unavailable");
            }
            catch (Exception ex)
            {
                return HealthCheckResult.Unhealthy("FHIR server is not accessible", ex);
            }
        }
    }
}