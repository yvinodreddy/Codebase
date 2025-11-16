// TerminologyIntegrationConfig.cs
namespace FHIRHealthcareAPI.Services.Terminology
{
    public class TerminologyConfig
    {
        // UMLS API (requires registration at https://uts.nlm.nih.gov/uts/)
        public string UmlsApiKey { get; set; }
        public string UmlsBaseUrl { get; set; } = "https://uts-ws.nlm.nih.gov/rest";

        // SNOMED CT API (via UMLS or Snowstorm server)
        public string SnomedBaseUrl { get; set; } = "https://browser.ihtsdotools.org/snowstorm/snomed-ct";
        public string SnomedEdition { get; set; } = "MAIN/2024-03-01";

        // RxNorm API (NLM)
        public string RxNormBaseUrl { get; set; } = "https://rxnav.nlm.nih.gov/REST";

        // LOINC API (requires account at loinc.org)
        public string LoincApiKey { get; set; }
        public string LoincBaseUrl { get; set; } = "https://fhir.loinc.org";

        // ICD-10 API (CMS or WHO)
        public string Icd10BaseUrl { get; set; } = "http://id.who.int/icd/release/10";
    }
}