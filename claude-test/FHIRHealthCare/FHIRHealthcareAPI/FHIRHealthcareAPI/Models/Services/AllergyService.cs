using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Manages allergy and intolerance information for patients.
    /// This is critical for patient safety - allergies can be life-threatening.
    /// </summary>
    public class AllergyService
    {
        private readonly FhirClient _fhirClient;
        // Define the RXNORM_SYSTEM constant at the class level
        private const string RXNORM_SYSTEM = "http://www.nlm.nih.gov/research/umls/rxnorm"; // RxNorm system URL

        public AllergyService()
        {
            //_fhirClient = new FhirClient("http://hapi.fhir.org/baseR4") 
            _fhirClient = new FhirClient("http://localhost:8080/fhir")
            {
                Settings = new FhirClientSettings
                {
                    PreferredFormat = ResourceFormat.Json,
                    Timeout = 30000
                }
            };
        }

        /// <summary>
        /// Records an allergy or intolerance for a patient.
        /// This is one of the most important safety features in healthcare IT.
        /// </summary>
        public async Task<AllergyIntolerance> RecordAllergy(
            string patientId,
            string allergen,
            string allergenCode,
            string reaction,
            AllergyIntolerance.AllergyIntoleranceSeverity severity)
        {
            // An AllergyIntolerance resource captures:
            // - What the patient is allergic to
            // - How severe the allergy is
            // - What reactions they've had
            // - When it was identified

            var allergy = new AllergyIntolerance
            {
                // Clinical status - is this allergy currently relevant?
                ClinicalStatus = new CodeableConcept
                {
                    Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                                Code = "active",
                                Display = "Active"
                            }
                        }
                },

                // Verification status - how confident are we about this allergy?
                VerificationStatus = new CodeableConcept
                {
                    Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                                Code = "confirmed",
                                Display = "Confirmed"
                            }
                        }
                },

                // Type - is this an allergy or intolerance?
                Type = AllergyIntolerance.AllergyIntoleranceType.Allergy,

                // Category - what type of allergen is this?
                Category = new List<AllergyIntolerance.AllergyIntoleranceCategory?>
                    {
                        AllergyIntolerance.AllergyIntoleranceCategory.Medication
                    },

                // Criticality - could this kill the patient?
                Criticality = severity == AllergyIntolerance.AllergyIntoleranceSeverity.Severe
                    ? AllergyIntolerance.AllergyIntoleranceCriticality.High
                    : AllergyIntolerance.AllergyIntoleranceCriticality.Low,

                // The allergen itself
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = RXNORM_SYSTEM,  // Using RxNorm for medication allergies
                                Code = allergenCode,
                                Display = allergen
                            }
                        },
                    Text = allergen
                },

                // Link to the patient
                Patient = new ResourceReference($"Patient/{patientId}"),

                // When was this recorded?
                RecordedDate = DateTime.Now.ToString(),

                // Document the reaction details
                Reaction = new List<AllergyIntolerance.ReactionComponent>
                    {
                        new AllergyIntolerance.ReactionComponent
                        {
                            // What happens when exposed to the allergen?
                            Manifestation = new List<CodeableConcept>
                            {
                                new CodeableConcept
                                {
                                    Text = reaction  // e.g., "Hives and difficulty breathing"
                                }
                            },
                            
                            // How bad was the reaction?
                            Severity = severity,
                            
                            // Additional notes about the reaction
                            Description = $"Patient experienced {reaction} when exposed to {allergen}"
                        }
                    }
            };

            var createdAllergy = await _fhirClient.CreateAsync(allergy);
            return createdAllergy;
        }

        /// <summary>
        /// Checks if a patient has any allergies to a specific medication
        /// This would be called before prescribing to ensure safety
        /// </summary>
        public async Task<AllergyCheckResult> CheckMedicationAllergies(
            string patientId,
            string medicationCode)
        {
            // Search for all active allergies for this patient
            var searchParams = new SearchParams()
                .Where($"patient={patientId}")
                .Where("clinical-status=active")
                .LimitTo(100);

            var allergies = await _fhirClient.SearchAsync<AllergyIntolerance>(searchParams);

            // Check if any allergies match the medication
            // In a real system, this would check drug families and cross-reactions
            var matchingAllergies = new List<AllergyIntolerance>();

            foreach (var entry in allergies.Entry)
            {
                if (entry.Resource is AllergyIntolerance allergyResource)
                {
                    // Check if this allergy is related to the medication
                    // This is simplified - real systems would check drug families
                    foreach (var coding in allergyResource.Code?.Coding ?? new List<Coding>())
                    {
                        if (coding.Code == medicationCode)
                        {
                            matchingAllergies.Add(allergyResource);
                        }
                    }
                }
            }

            return new AllergyCheckResult
            {
                PatientId = patientId,
                MedicationCode = medicationCode,
                HasAllergy = matchingAllergies.Any(),
                Allergies = matchingAllergies,
                SafeToPrescribe = !matchingAllergies.Any(),
                WarningMessage = matchingAllergies.Any()
                    ? $"WARNING: Patient has {matchingAllergies.Count} documented allergies to this medication"
                    : "No known allergies to this medication"
            };
        }
    }

    /// <summary>
    /// Result of checking for medication allergies
    /// </summary>
    public class AllergyCheckResult
    {
        public string PatientId { get; set; }
        public string MedicationCode { get; set; }
        public bool HasAllergy { get; set; }
        public List<AllergyIntolerance> Allergies { get; set; }
        public bool SafeToPrescribe { get; set; }
        public string WarningMessage { get; set; }
    }
}