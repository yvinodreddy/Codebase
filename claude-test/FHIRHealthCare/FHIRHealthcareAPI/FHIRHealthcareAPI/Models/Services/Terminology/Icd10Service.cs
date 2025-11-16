using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Terminology
{
    public class Icd10Service
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<Icd10Service> _logger;

        public Icd10Service(HttpClient httpClient, ILogger<Icd10Service> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
        }

        /// <summary>
        /// Validate ICD-10 code using WHO ICD API
        /// Common codes: E11.9 (Type 2 diabetes), I10 (Hypertension), J45.9 (Asthma)
        /// </summary>
        public async Task<Icd10Code> ValidateIcd10Code(string icd10Code)
        {
            try
            {
                // WHO provides free ICD-10 API access
                var url = $"https://id.who.int/icd/entity/{icd10Code}";
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    return ParseIcd10Response(json, icd10Code);
                }

                // Fallback to known codes if WHO API is unavailable
                return GetKnownIcd10Code(icd10Code);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error validating ICD-10 code: {icd10Code}");
                return GetKnownIcd10Code(icd10Code);
            }
        }

        /// <summary>
        /// Map SNOMED codes to ICD-10 for billing purposes
        /// </summary>
        public async Task<string> MapSnomedToIcd10(string snomedCode)
        {
            var mappings = new Dictionary<string, string>
            {
                {"44054006", "E11.9"},    // Type 2 diabetes → E11.9
                {"38341003", "I10"},      // Hypertension → I10
                {"195967001", "J45.9"},   // Asthma → J45.9
                {"73211009", "E11.9"},    // Diabetes mellitus → E11.9
                {"22298006", "I21.9"},    // MI → I21.9
                {"53741008", "I25.9"}     // CAD → I25.9
            };

            return mappings.TryGetValue(snomedCode, out var icd10Code) ? icd10Code : null;
        }

        private Icd10Code ParseIcd10Response(string json, string code)
        {
            try
            {
                var doc = JsonDocument.Parse(json);
                var root = doc.RootElement;

                return new Icd10Code
                {
                    Code = code,
                    Title = ExtractJsonProperty(root, "title", "en") ?? "Unknown condition",
                    Description = ExtractJsonProperty(root, "definition", "en"),
                    Category = ExtractCategory(code),
                    IsValid = true
                };
            }
            catch
            {
                return new Icd10Code { Code = code, IsValid = false };
            }
        }

        private Icd10Code GetKnownIcd10Code(string code)
        {
            var knownCodes = new Dictionary<string, (string title, string category)>
            {
                {"E11.9", ("Type 2 diabetes mellitus without complications", "Endocrine")},
                {"I10", ("Essential (primary) hypertension", "Circulatory")},
                {"J45.9", ("Asthma, unspecified", "Respiratory")},
                {"I21.9", ("Acute myocardial infarction, unspecified", "Circulatory")},
                {"I25.9", ("Chronic ischemic heart disease, unspecified", "Circulatory")},
                {"N18.6", ("End stage renal disease", "Genitourinary")},
                {"F32.9", ("Major depressive disorder, single episode, unspecified", "Mental")},
                {"M79.3", ("Panniculitis, unspecified", "Musculoskeletal")}
            };

            if (knownCodes.TryGetValue(code, out var known))
            {
                return new Icd10Code
                {
                    Code = code,
                    Title = known.title,
                    Category = known.category,
                    IsValid = true
                };
            }

            return new Icd10Code { Code = code, IsValid = false };
        }

        private string ExtractJsonProperty(JsonElement element, string property, string language = "en")
        {
            try
            {
                if (element.TryGetProperty(property, out var prop))
                {
                    if (prop.ValueKind == JsonValueKind.Object && prop.TryGetProperty(language, out var langProp))
                    {
                        return langProp.GetString();
                    }
                    return prop.GetString();
                }
            }
            catch { }
            return null;
        }

        private string ExtractCategory(string icd10Code)
        {
            return icd10Code.Substring(0, 1) switch
            {
                "A" or "B" => "Infectious and parasitic diseases",
                "C" or "D" => "Neoplasms",
                "E" => "Endocrine, nutritional and metabolic diseases",
                "F" => "Mental and behavioural disorders",
                "G" => "Diseases of the nervous system",
                "H" => "Diseases of the eye and ear",
                "I" => "Diseases of the circulatory system",
                "J" => "Diseases of the respiratory system",
                "K" => "Diseases of the digestive system",
                "L" => "Diseases of the skin",
                "M" => "Diseases of the musculoskeletal system",
                "N" => "Diseases of the genitourinary system",
                "O" => "Pregnancy, childbirth and the puerperium",
                "P" => "Conditions originating in the perinatal period",
                "Q" => "Congenital malformations",
                "R" => "Abnormal clinical and laboratory findings",
                "S" or "T" => "Injury, poisoning",
                "V" or "W" or "X" or "Y" => "External causes of morbidity",
                "Z" => "Factors influencing health status",
                _ => "Unknown"
            };
        }
    }

    public class Icd10Code
    {
        public string Code { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public string Category { get; set; }
        public bool IsValid { get; set; }
    }
}