using FHIRHealthcareAPI.Services.Terminology;
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Manages clinical conditions (diagnoses) for patients.
    /// This service handles the "why" behind treatments - documenting what health
    /// problems a patient has and tracking their progression over time.
    /// </summary>
    public class ConditionService
    {
        private readonly FhirClient _fhirClient;

        // SNOMED CT is the comprehensive clinical terminology for conditions
        private const string SNOMED_SYSTEM = "http://snomed.info/sct";

        // ICD-10 is used for billing and statistical reporting
        private const string ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10";

        private readonly SnomedService _snomedService;

        public ConditionService(SnomedService snomedService)
        {
            _snomedService = snomedService;
            _fhirClient = new FhirClient("http://localhost:8080/fhir")
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json,
                    Timeout = 30000
                }
            };
        }

        public async Task<Condition> RecordValidatedCondition(
     string patientId,
     string snomedCode,
     string severity = "moderate")
        {
            // Validate SNOMED code first
            var concept = await _snomedService.ValidateConditionCode(snomedCode);

            if (!concept.IsValid)
            {
                throw new ArgumentException($"Invalid SNOMED code: {snomedCode}");
            }

            // Call RecordDiagnosis directly instead of RecordCondition
            return await RecordDiagnosis(
                patientId,
                concept.PreferredTerm, // Official term from SNOMED
                snomedCode,
                null, // No ICD-10 code
                DateTime.Now, // Default onset
                "active", // Default status
                severity,
                null // No supporting observations
            );
        }

        // Add this to your ConditionService class:
        /// <summary>
        /// Generic method to record a condition with basic information
        /// </summary>
        public async Task<Condition> RecordCondition(
            string patientId,
            string conditionName,
            string snomedCode,
            string severity = "moderate")
        {
            // Use the existing RecordDiagnosis method with defaults
            return await RecordDiagnosis(
                patientId,
                conditionName,
                snomedCode,
                null, // No ICD-10 code for generic method
                DateTime.Now, // Default to now
                "active",
                severity,
                null // No supporting observations
            );
        }

        /// <summary>
        /// Records a new diagnosis for a patient.
        /// This creates a Condition resource with proper clinical coding.
        /// </summary>
        public async Task<Condition> RecordDiagnosis(
            string patientId,
            string conditionName,
            string snomedCode,
            string icd10Code,
            DateTime? onsetDate = null,
            string clinicalStatus = "active",
            string severity = null,
            List<string> supportingObservationIds = null)
        {
            var condition = new Condition
            {
                // Link to the patient who has this condition
                Subject = new ResourceReference($"Patient/{patientId}"),

                // When was this condition recorded in the system?
                RecordedDate = DateTime.Now.ToString("yyyy-MM-dd"),

                // Clinical status - is this condition currently active?
                ClinicalStatus = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            Code = clinicalStatus,  // active, recurrence, inactive, remission, resolved
                            Display = char.ToUpper(clinicalStatus[0]) + clinicalStatus.Substring(1)
                        }
                    }
                },

                // Verification status - how certain are we about this diagnosis?
                VerificationStatus = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            Code = "confirmed",
                            Display = "Confirmed"
                        }
                    }
                },

                // The actual diagnosis with multiple coding systems
                // This allows different systems to understand the same condition
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = SNOMED_SYSTEM,
                            Code = snomedCode,
                            Display = conditionName
                        },
                        new Coding
                        {
                            System = ICD10_SYSTEM,
                            Code = icd10Code,
                            Display = conditionName
                        }
                    },
                    Text = conditionName
                },

                // When did this condition start?
                Onset = onsetDate.HasValue
                    ? new FhirDateTime(onsetDate.Value)
                    : new FhirDateTime(DateTime.Now)
            };

            // Add severity if specified
            if (!string.IsNullOrEmpty(severity))
            {
                condition.Severity = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = "http://snomed.info/sct",
                            Code = severity switch
                            {
                                "mild" => "255604002",
                                "moderate" => "6736007",
                                "severe" => "24484000",
                                _ => "255604002"
                            },
                            Display = char.ToUpper(severity[0]) + severity.Substring(1)
                        }
                    }
                };
            }

            // Link to supporting observations (like high glucose supporting diabetes diagnosis)
            if (supportingObservationIds != null && supportingObservationIds.Any())
            {
                condition.Evidence = supportingObservationIds
                    .Select(id => new Condition.EvidenceComponent
                    {
                        Detail = new List<ResourceReference>
                        {
                            new ResourceReference($"Observation/{id}")
                        }
                    })
                    .ToList();
            }

            var created = await _fhirClient.CreateAsync(condition);
            return created;
        }

        /// <summary>
        /// Records Type 2 Diabetes diagnosis with proper coding and classification.
        /// This is a specialized method for one of the most common chronic conditions.
        /// </summary>
        public async Task<Condition> RecordType2Diabetes(
            string patientId,
            DateTime? onsetDate = null,
            bool withComplications = false,
            List<string> supportingObservationIds = null)
        {
            // Type 2 Diabetes has specific codes depending on complications
            string snomedCode = withComplications ? "44054006" : "44054006";  // Same base code
            string icd10Code = withComplications ? "E11.9" : "E11.9";  // .9 = without complications
            string conditionName = withComplications
                ? "Type 2 diabetes mellitus with complications"
                : "Type 2 diabetes mellitus without complications";

            return await RecordDiagnosis(
                patientId,
                conditionName,
                snomedCode,
                icd10Code,
                onsetDate,
                "active",
                "moderate",  // Diabetes is typically considered moderate severity
                supportingObservationIds
            );
        }

        /// <summary>
        /// Records hypertension diagnosis.
        /// Another very common condition that often accompanies diabetes.
        /// </summary>
        public async Task<Condition> RecordHypertension(
            string patientId,
            string stage = "1",  // Stage 1, 2, or 3
            DateTime? onsetDate = null,
            List<string> supportingObservationIds = null)
        {
            string snomedCode = stage switch
            {
                "1" => "59621000",  // Essential hypertension
                "2" => "59621000",  // Same code, different severity
                _ => "38341003"     // Hypertensive disorder
            };

            string icd10Code = stage switch
            {
                "1" => "I10",  // Essential (primary) hypertension
                "2" => "I10",
                _ => "I10"
            };

            return await RecordDiagnosis(
                patientId,
                $"Essential hypertension (Stage {stage})",
                snomedCode,
                icd10Code,
                onsetDate,
                "active",
                stage == "2" ? "severe" : "moderate",
                supportingObservationIds
            );
        }

        /// <summary>
        /// Updates the status of an existing condition.
        /// Used when conditions resolve, go into remission, or recur.
        /// </summary>
        public async Task<Condition> UpdateConditionStatus(
            string conditionId,
            string newStatus,
            DateTime? abatementDate = null)
        {
            // Retrieve the existing condition
            var condition = await _fhirClient.ReadAsync<Condition>($"Condition/{conditionId}");

            // Update the clinical status
            condition.ClinicalStatus = new CodeableConcept
            {
                Coding = new List<Coding>
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        Code = newStatus,
                        Display = char.ToUpper(newStatus[0]) + newStatus.Substring(1)
                    }
                }
            };

            // If the condition has resolved or gone into remission, record when
            if ((newStatus == "resolved" || newStatus == "remission") && abatementDate.HasValue)
            {
                condition.Abatement = new FhirDateTime(abatementDate.Value);
            }

            // Update the condition on the server
            var updated = await _fhirClient.UpdateAsync(condition);
            return updated;
        }

        /// <summary>
        /// Retrieves all active conditions for a patient.
        /// This gives you the patient's current problem list.
        /// </summary>
        public async Task<List<Condition>> GetActiveConditions(string patientId)
        {
            var searchParams = new SearchParams()
                .Where($"patient={patientId}")
                .Where("clinical-status=active")
                .OrderBy("-onset-date")
                .LimitTo(100);

            var bundle = await _fhirClient.SearchAsync<Condition>(searchParams);

            return bundle.Entry
                .Select(e => e.Resource as Condition)
                .Where(c => c != null)
                .ToList();
        }

        /// <summary>
        /// Gets a patient's complete medical history including resolved conditions.
        /// This provides the full picture of what the patient has experienced.
        /// </summary>
        public async Task<PatientMedicalHistory> GetPatientMedicalHistory(string patientId)
        {
            // Get all conditions for the patient
            var searchParams = new SearchParams()
                .Where($"patient={patientId}")
                .OrderBy("-onset-date")
                .LimitTo(100);

            var bundle = await _fhirClient.SearchAsync<Condition>(searchParams);

            var allConditions = bundle.Entry
                .Select(e => e.Resource as Condition)
                .Where(c => c != null)
                .ToList();

            // Organize by status
            return new PatientMedicalHistory
            {
                PatientId = patientId,
                ActiveConditions = allConditions.Where(c =>
                    c.ClinicalStatus?.Coding?.FirstOrDefault()?.Code == "active").ToList(),
                ResolvedConditions = allConditions.Where(c =>
                    c.ClinicalStatus?.Coding?.FirstOrDefault()?.Code == "resolved").ToList(),
                ChronicConditions = allConditions.Where(c =>
                    IsChronicCondition(c.Code?.Coding?.FirstOrDefault()?.Code)).ToList()
            };
        }

        // Helper method to identify chronic conditions
        private bool IsChronicCondition(string snomedCode)
        {
            // Common chronic condition SNOMED codes
            var chronicCodes = new HashSet<string>
            {
                "44054006",  // Type 2 diabetes
                "46635009",  // Type 1 diabetes
                "38341003",  // Hypertension
                "13645005",  // COPD
                "195967001", // Asthma
                "53741008",  // Coronary artery disease
                "49601007",  // Cardiovascular disorder
                "73211009",  // Chronic kidney disease
            };

            return chronicCodes.Contains(snomedCode);
        }
    }

    /// <summary>
    /// Represents a patient's complete medical history organized by condition status
    /// </summary>
    public class PatientMedicalHistory
    {
        public string PatientId { get; set; }
        public List<Condition> ActiveConditions { get; set; } = new List<Condition>();
        public List<Condition> ResolvedConditions { get; set; } = new List<Condition>();
        public List<Condition> ChronicConditions { get; set; } = new List<Condition>();

        public bool HasChronicConditions => ChronicConditions.Any();
        public int TotalConditions => ActiveConditions.Count + ResolvedConditions.Count;
    }
}