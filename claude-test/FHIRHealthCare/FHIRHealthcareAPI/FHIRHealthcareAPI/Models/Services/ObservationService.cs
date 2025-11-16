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
    /// Manages clinical observations - vital signs, lab results, and other measurements.
    /// Think of this as the clinical data recorder that captures all the numbers and
    /// measurements that help doctors understand a patient's health status.
    /// </summary>
    public class ObservationService
    {
        private readonly FhirClient _fhirClient;
        private readonly LoincService _loincService;   
        // LOINC is the universal coding system for laboratory and clinical observations
        // It's like a dictionary where every possible medical test has a unique code
        private const string LOINC_SYSTEM = "http://loinc.org";

        // Units of measure use the UCUM system - standardized units for medical measurements
        private const string UCUM_SYSTEM = "http://unitsofmeasure.org";

        // Update the constructor to include a parameter for LoincService and initialize it properly.
        public ObservationService(LoincService loincService)
        {
            _loincService = loincService;

            // Connect to your local FHIR server
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
        /// Generic method to record any lab observation with LOINC code
        /// </summary>
        public async Task<Observation> RecordObservation(
            string patientId,
            string testName,
            string loincCode,
            decimal value,
            string unit,
            string interpretation = null)
        {
            var observation = new Observation
            {
                Status = ObservationStatus.Final,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Effective = new FhirDateTime(DateTime.Now),

                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
            {
                new Coding
                {
                    System = LOINC_SYSTEM,
                    Code = loincCode,
                    Display = testName
                }
            },
                    Text = testName
                },

                Value = new Quantity
                {
                    Value = value,
                    Unit = unit,
                    System = UCUM_SYSTEM,
                    Code = unit
                }
            };

            // Add interpretation if provided
            if (!string.IsNullOrEmpty(interpretation))
            {
                observation.Interpretation = new List<CodeableConcept>
        {
            new CodeableConcept { Text = interpretation }
        };
            }

            var created = await _fhirClient.CreateAsync(observation);
            return created;
        }
 
        /// <summary>
        /// Create lab observation with LOINC validation
        /// </summary>
        public async Task<Observation> RecordValidatedLabResult(
            string patientId,
            string loincCode,
            decimal value,
            string unit,
            string interpretation = null)
                {
                    // Use fallback method instead
                    var labTest = await _loincService.GetLabTestByCodeWithFallback(loincCode);

                    if (!labTest.IsValid)
                    {
                        throw new ArgumentException($"Invalid LOINC code: {loincCode}");
                    }

                    return await RecordObservation(
                        patientId,
                        labTest.Display,
                        loincCode,
                        value,
                        unit,
                        interpretation
                    );
                }

        /// <summary>
        /// Records a blood glucose reading - one of the most common observations for diabetic patients.
        /// This demonstrates recording a simple numeric observation with interpretation.
        /// </summary>
        public async Task<Observation> RecordBloodGlucose(
            string patientId,
            decimal glucoseValue,
            bool isFasting,
            DateTime? measuredAt = null)
        {
            var observation = new Observation
            {
                // Status indicates this is a final result, not preliminary
                Status = ObservationStatus.Final,

                // Link to the patient this observation is about
                Subject = new ResourceReference($"Patient/{patientId}"),

                // When was this measured? Default to now if not specified
                Effective = new FhirDateTime(measuredAt ?? DateTime.Now),

                // What are we measuring? Use the appropriate LOINC code
                // LOINC has different codes for fasting vs random glucose
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = LOINC_SYSTEM,
                            Code = isFasting ? "1558-6" : "2339-0",
                            Display = isFasting ? "Fasting glucose [Mass/volume] in Serum or Plasma"
                                              : "Glucose [Mass/volume] in Blood"
                        }
                    },
                    Text = isFasting ? "Fasting Blood Glucose" : "Random Blood Glucose"
                },

                // The actual measurement value with units
                Value = new Quantity
                {
                    Value = glucoseValue,
                    Unit = "mg/dL",  // Standard US units for glucose
                    System = UCUM_SYSTEM,
                    Code = "mg/dL"
                }
            };

            // Add interpretation based on clinical ranges
            // This helps clinicians quickly identify abnormal values
            observation.Interpretation = new List<CodeableConcept> { InterpretGlucoseLevel(glucoseValue, isFasting) };

            // Add reference ranges so anyone viewing this knows what's normal
            observation.ReferenceRange = new List<Observation.ReferenceRangeComponent>
            {
                new Observation.ReferenceRangeComponent
                {
                    Low = new Quantity { Value = isFasting ? 70 : 80, Unit = "mg/dL" },
                    High = new Quantity { Value = isFasting ? 100 : 140, Unit = "mg/dL" },
                    Text = isFasting ? "Normal fasting glucose range" : "Normal random glucose range"
                }
            };

            var created = await _fhirClient.CreateAsync(observation);
            return created;
        }

        /// <summary>
        /// Records blood pressure - a compound observation with systolic and diastolic components.
        /// This demonstrates how FHIR handles observations with multiple related values.
        /// </summary>
        public async Task<Observation> RecordBloodPressure(
            string patientId,
            int systolic,
            int diastolic,
            DateTime? measuredAt = null)
        {
            var observation = new Observation
            {
                Status = ObservationStatus.Final,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Effective = new FhirDateTime(measuredAt ?? DateTime.Now),

                // Blood pressure is identified by LOINC code 85354-9
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = LOINC_SYSTEM,
                            Code = "85354-9",
                            Display = "Blood pressure panel with all children optional"
                        }
                    },
                    Text = "Blood Pressure"
                },

                // Blood pressure has two components rather than a single value
                Component = new List<Observation.ComponentComponent>
                {
                    new Observation.ComponentComponent
                    {
                        // Systolic component
                        Code = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding
                                {
                                    System = LOINC_SYSTEM,
                                    Code = "8480-6",
                                    Display = "Systolic blood pressure"
                                }
                            }
                        },
                        Value = new Quantity
                        {
                            Value = systolic,
                            Unit = "mmHg",
                            System = UCUM_SYSTEM,
                            Code = "mm[Hg]"
                        }
                    },
                    new Observation.ComponentComponent
                    {
                        // Diastolic component
                        Code = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding
                                {
                                    System = LOINC_SYSTEM,
                                    Code = "8462-4",
                                    Display = "Diastolic blood pressure"
                                }
                            }
                        },
                        Value = new Quantity
                        {
                            Value = diastolic,
                            Unit = "mmHg",
                            System = UCUM_SYSTEM,
                            Code = "mm[Hg]"
                        }
                    }
                }
            };

            // Interpret the blood pressure according to clinical guidelines
            observation.Interpretation = new List<CodeableConcept> { InterpretBloodPressure(systolic, diastolic) };

            var created = await _fhirClient.CreateAsync(observation);
            return created;
        }

        // <summary>
        /// Generic method to record any observation with LOINC code
        /// </summary>
        private async Task<Observation> RecordObservationGeneric(
            string patientId,
            string testName,
            string loincCode,
            decimal value,
            string unit,
            string interpretation = null)
        {
            var observation = new Observation
            {
                Status = ObservationStatus.Final,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Effective = new FhirDateTime(DateTime.Now),
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
            {
                new Coding
                {
                    System = LOINC_SYSTEM,
                    Code = loincCode,
                    Display = testName
                }
            },
                    Text = testName
                },
                Value = new Quantity
                {
                    Value = value,
                    Unit = unit,
                    System = UCUM_SYSTEM,
                    Code = unit
                }
            };

            if (!string.IsNullOrEmpty(interpretation))
            {
                observation.Interpretation = new List<CodeableConcept>
        {
            new CodeableConcept { Text = interpretation }
        };
            }

            var created = await _fhirClient.CreateAsync(observation);
            return created;
        }

        /// <summary>
        /// Records HbA1c - a key laboratory test for monitoring diabetes control.
        /// HbA1c reflects average blood glucose over the past 2-3 months.
        /// </summary>
        public async Task<Observation> RecordHbA1c(
            string patientId,
            decimal hba1cPercentage,
            DateTime? measuredAt = null)
        {
            var observation = new Observation
            {
                Status = ObservationStatus.Final,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Effective = new FhirDateTime(measuredAt ?? DateTime.Now),

                // HbA1c has a specific LOINC code
                Code = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = LOINC_SYSTEM,
                            Code = "4548-4",
                            Display = "Hemoglobin A1c/Hemoglobin.total in Blood"
                        }
                    },
                    Text = "HbA1c"
                },

                Value = new Quantity
                {
                    Value = hba1cPercentage,
                    Unit = "%",
                    System = UCUM_SYSTEM,
                    Code = "%"
                }
            };

            // Interpret based on diabetes control guidelines
            // <5.7% = Normal, 5.7-6.4% = Prediabetes, ≥6.5% = Diabetes
            observation.Interpretation = new List<CodeableConcept> { InterpretHbA1c(hba1cPercentage) };

            // Add reference range
            observation.ReferenceRange = new List<Observation.ReferenceRangeComponent>
            {
                new Observation.ReferenceRangeComponent
                {
                    Low = new Quantity { Value = 4.0m, Unit = "%" },
                    High = new Quantity { Value = 5.6m, Unit = "%" },
                    Text = "Normal HbA1c range for non-diabetic individuals"
                }
            };

            var created = await _fhirClient.CreateAsync(observation);
            return created;
        }

        /// <summary>
        /// Retrieves all observations for a patient, optionally filtered by type.
        /// This allows you to get all vital signs, or just glucose readings, etc.
        /// </summary>
        public async Task<List<Observation>> GetPatientObservations(
            string patientId,
            string loincCode = null)
        {
            var searchParams = new SearchParams()
                .Where($"patient={patientId}")
                .OrderBy("-date")  // Most recent first
                .LimitTo(100);

            // Add code filter if specified
            if (!string.IsNullOrEmpty(loincCode))
            {
                searchParams = searchParams.Where($"code={LOINC_SYSTEM}|{loincCode}");
            }

            var bundle = await _fhirClient.SearchAsync<Observation>(searchParams);

            return bundle.Entry
                .Select(e => e.Resource as Observation)
                .Where(o => o != null)
                .ToList();
        }

        // Helper method to interpret glucose levels based on clinical guidelines
        private CodeableConcept InterpretGlucoseLevel(decimal glucose, bool isFasting)
        {
            string code, display;

            if (isFasting)
            {
                // Fasting glucose interpretation
                if (glucose < 70) { code = "L"; display = "Low (Hypoglycemia)"; }
                else if (glucose <= 100) { code = "N"; display = "Normal"; }
                else if (glucose <= 125) { code = "H"; display = "High (Prediabetes)"; }
                else { code = "HH"; display = "Very High (Diabetes)"; }
            }
            else
            {
                // Random glucose interpretation
                if (glucose < 80) { code = "L"; display = "Low"; }
                else if (glucose <= 140) { code = "N"; display = "Normal"; }
                else if (glucose <= 199) { code = "H"; display = "High"; }
                else { code = "HH"; display = "Very High (Possible Diabetes)"; }
            }

            return new CodeableConcept
            {
                Coding = new List<Coding>
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        Code = code,
                        Display = display
                    }
                }
            };
        }

        // Helper method to interpret blood pressure based on AHA guidelines
        private CodeableConcept InterpretBloodPressure(int systolic, int diastolic)
        {
            string interpretation;

            if (systolic < 120 && diastolic < 80)
                interpretation = "Normal";
            else if (systolic < 130 && diastolic < 80)
                interpretation = "Elevated";
            else if (systolic < 140 || diastolic < 90)
                interpretation = "Stage 1 Hypertension";
            else
                interpretation = "Stage 2 Hypertension";

            return new CodeableConcept
            {
                Coding = new List<Coding>
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        Code = interpretation.Contains("Normal") ? "N" : "H",
                        Display = interpretation
                    }
                }
            };
        }

        // Helper method to interpret HbA1c based on diabetes guidelines
        private CodeableConcept InterpretHbA1c(decimal hba1c)
        {
            string code, display;

            if (hba1c < 5.7m) { code = "N"; display = "Normal"; }
            else if (hba1c < 6.5m) { code = "H"; display = "Prediabetes"; }
            else if (hba1c < 7.0m) { code = "H"; display = "Diabetes - Good Control"; }
            else if (hba1c < 8.0m) { code = "H"; display = "Diabetes - Moderate Control"; }
            else { code = "HH"; display = "Diabetes - Poor Control"; }

            return new CodeableConcept
            {
                Coding = new List<Coding>
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        Code = code,
                        Display = display
                    }
                }
            };
        }
    }
}