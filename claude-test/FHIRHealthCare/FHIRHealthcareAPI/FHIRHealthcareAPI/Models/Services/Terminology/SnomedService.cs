using System;
using System.Threading.Tasks;
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Terminology
{
    public class SnomedService
    {
        private readonly FhirClient _fhirClient;
        private readonly ILogger<SnomedService> _logger;

        public SnomedService(ILogger<SnomedService> logger)
        {
            _logger = logger;
            // Using Snowstorm SNOMED server
            _fhirClient = new FhirClient("https://snowstorm.ihtsdotools.org/fhir")
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json,
                    Timeout = 30000
                }
            };
        }

        public async Task<SnomedConcept> ValidateConditionCode(string snomedCode)
        {
            try
            {
                var parameters = new Parameters();
                parameters.Add("system", new FhirUri("http://snomed.info/sct"));
                parameters.Add("code", new Code(snomedCode));

                var result = await _fhirClient.OperationAsync(
                    new Uri("CodeSystem/$lookup", UriKind.Relative),
                    parameters);

                if (result is Parameters responseParams)
                {
                    return new SnomedConcept
                    {
                        ConceptId = snomedCode,
                        PreferredTerm = GetParameterValue(responseParams, "display"),
                        IsValid = true
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error validating SNOMED code {snomedCode}");
            }

            return new SnomedConcept { ConceptId = snomedCode, IsValid = false };
        }

        private string GetParameterValue(Parameters parameters, string name)
        {
            var param = parameters.Parameter?.FirstOrDefault(p => p.Name == name);
            return param?.Value?.ToString();
        }
    }

    public class SnomedConcept
    {
        public string ConceptId { get; set; }
        public string PreferredTerm { get; set; }
        public bool IsValid { get; set; }
    }
}