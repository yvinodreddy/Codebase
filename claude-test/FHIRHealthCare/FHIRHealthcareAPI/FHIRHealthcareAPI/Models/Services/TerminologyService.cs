using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System.Collections.Generic;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// This service handles medical terminology and coding systems
    /// It's like a medical dictionary that can translate between different coding systems
    /// </summary>
    public class TerminologyService
    {
        private readonly FhirClient _fhirClient;

        public TerminologyService()
        {
            // Replace the PreferredFormat property with the correct serializer configuration
            //_fhirClient = new FhirClient("http://hapi.fhir.org/baseR4")
            _fhirClient = new FhirClient("http://localhost:8080/fhir") 
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json, // Correctly set the preferred format in the settings
                    Timeout = 30000 // Set the timeout in the FhirClientSettings object
                }
            };
        }
    }
}