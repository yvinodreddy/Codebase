using System;
using System.Threading;
using System.Threading.Tasks;
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace FHIRHealthcareAPI.HealthChecks
{
    public class TerminologyHealthCheck : IHealthCheck
    {
        private readonly SimplifiedRxNormService _rxNormService;

        public TerminologyHealthCheck(SimplifiedRxNormService rxNormService)
        {
            _rxNormService = rxNormService;
        }

        public async Task<HealthCheckResult> CheckHealthAsync(
            HealthCheckContext context,
            CancellationToken cancellationToken = default)
        {
            try
            {
                var testDrug = await _rxNormService.GetDrugInfo("6809");

                if (testDrug.IsValid)
                {
                    return HealthCheckResult.Healthy("RxNorm API is accessible");
                }

                return HealthCheckResult.Degraded("RxNorm API returned unexpected result");
            }
            catch (Exception ex)
            {
                return HealthCheckResult.Unhealthy("RxNorm API is not accessible", ex);
            }
        }
    }
}