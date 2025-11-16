using System;
using System.Linq;
using System.Threading.Tasks;
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Terminology
{
    public class LoincService
    {
        private readonly FhirClient _fhirClient;
        private readonly ILogger<LoincService> _logger;

        public LoincService(ILogger<LoincService> logger)
        {
            _logger = logger;
            _fhirClient = new FhirClient("https://r4.ontoserver.csiro.au/fhir")
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json,
                    Timeout = 30000
                }
            };
        }

        public async Task<LoincCode> GetLabTestByCode(string loincCode)
        {
            try
            {
                var parameters = new Parameters();
                parameters.Add("system", new FhirUri("http://loinc.org"));
                parameters.Add("code", new Code(loincCode));

                var result = await _fhirClient.OperationAsync(
                    new Uri("CodeSystem/$lookup", UriKind.Relative),
                    parameters);

                if (result is Parameters responseParams)
                {
                    return new LoincCode
                    {
                        Code = loincCode,
                        Display = GetParameterValue(responseParams, "display"),
                        IsValid = true
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error looking up LOINC code {loincCode}");
            }

            return new LoincCode { Code = loincCode, IsValid = false };
        }

        public async Task<LoincCode> GetLabTestByCodeWithFallback(string loincCode)
        {
            try
            {
                // Try the FHIR server first
                var result = await GetLabTestByCode(loincCode);

                // If FHIR server says it's invalid, check our known codes
                if (!result.IsValid)
                {
                    var knownCodes = new Dictionary<string, string>
            {
                {"4548-4", "Hemoglobin A1c/Hemoglobin.total in Blood"},
                {"33747-0", "Glucose [Mass/volume] in Blood"},
                {"2085-9", "Cholesterol [Mass/volume] in Serum or Plasma"},
                {"718-7", "Hemoglobin [Mass/volume] in Blood"},
                {"6690-2", "Leukocytes [#/volume] in Blood by Automated count"},
                {"2160-0", "Creatinine [Mass/volume] in Serum or Plasma"}
            };

                    if (knownCodes.ContainsKey(loincCode))
                    {
                        return new LoincCode
                        {
                            Code = loincCode,
                            Display = knownCodes[loincCode],
                            IsValid = true
                        };
                    }
                }

                return result;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $"FHIR server failed for LOINC {loincCode}, using fallback");
                return new LoincCode { Code = loincCode, IsValid = false };
            }
        }

        /// <summary>
        /// Get detailed lab test information including normal ranges and units
        /// </summary>
        public async Task<DetailedLoincCode> GetDetailedLabTest(string loincCode)
        {
            try
            {
                var parameters = new Parameters();
                parameters.Add("system", new FhirUri("http://loinc.org"));
                parameters.Add("code", new Code(loincCode));
                parameters.Add("property", new Code("COMPONENT"));
                parameters.Add("property", new Code("PROPERTY"));
                parameters.Add("property", new Code("SCALE_TYP"));
                parameters.Add("property", new Code("METHOD_TYP"));

                var result = await _fhirClient.OperationAsync(
                    new Uri("CodeSystem/$lookup", UriKind.Relative),
                    parameters);

                if (result is Parameters responseParams)
                {
                    return new DetailedLoincCode
                    {
                        Code = loincCode,
                        Display = GetParameterValue(responseParams, "display"),
                        Component = GetPropertyValue(responseParams, "COMPONENT"),
                        Property = GetPropertyValue(responseParams, "PROPERTY"),
                        Scale = GetPropertyValue(responseParams, "SCALE_TYP"),
                        Method = GetPropertyValue(responseParams, "METHOD_TYP"),
                        IsValid = true
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting detailed LOINC info for {loincCode}");
            }

            return new DetailedLoincCode { Code = loincCode, IsValid = false };
        }

        private string GetPropertyValue(Parameters parameters, string propertyName)
        {
            var properties = parameters.Parameter?
                .Where(p => p.Name == "property")
                .SelectMany(p => p.Part ?? new List<Parameters.ParameterComponent>());

            foreach (var part in properties ?? Enumerable.Empty<Parameters.ParameterComponent>())
            {
                var codePart = part.Part?.FirstOrDefault(pp => pp.Name == "code");
                var valuePart = part.Part?.FirstOrDefault(pp => pp.Name == "value");

                if (codePart?.Value is Code code && code.Value == propertyName)
                {
                    return valuePart?.Value?.ToString();
                }
            }
            return null;
        }
        public async Task<bool> ValidateLoincCode(string loincCode)
        {
            var labTest = await GetLabTestByCode(loincCode);
            return labTest.IsValid;
        }

        private string GetParameterValue(Parameters parameters, string name)
        {
            var param = parameters.Parameter?.FirstOrDefault(p => p.Name == name);

            if (param?.Value != null)
            {
                switch (param.Value)
                {
                    case FhirString fs:
                        return fs.Value;
                    case Code c:
                        return c.Value;
                    case FhirUri fu:
                        return fu.Value;
                    default:
                        return param.Value.ToString();
                }
            }

            return null;
        }
    }
    public class DetailedLoincCode : LoincCode
    {
        public string Component { get; set; }  // What is measured (e.g., "Glucose")
        public string Property { get; set; }   // Type of property (e.g., "MCnc" for mass concentration)
        public string Scale { get; set; }      // Scale type (e.g., "Qn" for quantitative)
        public string Method { get; set; }     // Method used (e.g., "Enzymatic")
    }
    public class LoincCode
    {
        public string Code { get; set; }
        public string Display { get; set; }
        public bool IsValid { get; set; }
    } 

}