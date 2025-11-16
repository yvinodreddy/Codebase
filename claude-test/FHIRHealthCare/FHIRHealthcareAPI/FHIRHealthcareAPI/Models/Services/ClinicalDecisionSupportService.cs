using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Hl7.Fhir.Model;
using FHIRHealthcareAPI.Models;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Provides clinical decision support by analyzing patient data
    /// and generating alerts, warnings, and recommendations
    /// </summary>
    public class ClinicalDecisionSupportService
    {
        private readonly MedicationService _medicationService;
        private readonly ObservationService _observationService;
        private readonly ConditionService _conditionService;

        // Drug interaction database (simplified - real systems use comprehensive databases)
        private readonly Dictionary<string, List<DrugInteraction>> _drugInteractions = new()
        {
            {
                "6809", // Metformin
                new List<DrugInteraction>
                {
                    new DrugInteraction
                    {
                        DrugCode = "8356", // Alcohol
                        Severity = "Major",
                        Description = "Metformin + alcohol increases risk of lactic acidosis"
                    },
                    new DrugInteraction
                    {
                        DrugCode = "161", // Acetaminophen (high dose)
                        Severity = "Moderate",
                        Description = "May affect glycemic control"
                    }
                }
            },
            {
                "29046", // Lisinopril
                new List<DrugInteraction>
                {
                    new DrugInteraction
                    {
                        DrugCode = "632", // Potassium supplements
                        Severity = "Major",
                        Description = "Risk of hyperkalemia (dangerous potassium levels)"
                    },
                    new DrugInteraction
                    {
                        DrugCode = "5521", // Ibuprofen
                        Severity = "Moderate",
                        Description = "NSAIDs may reduce effectiveness of ACE inhibitors"
                    }
                }
            },
            {
                "243670", // Aspirin
                new List<DrugInteraction>
                {
                    new DrugInteraction
                    {
                        DrugCode = "11289", // Warfarin
                        Severity = "Major",
                        Description = "Increased bleeding risk with dual anticoagulation"
                    },
                    new DrugInteraction
                    {
                        DrugCode = "5521", // Ibuprofen
                        Severity = "Major",
                        Description = "Multiple NSAIDs increase bleeding and ulcer risk"
                    }
                }
            },
            {
                "11289", // Warfarin
                new List<DrugInteraction>
                {
                    new DrugInteraction
                    {
                        DrugCode = "243670", // Aspirin
                        Severity = "Major",
                        Description = "Warfarin + Aspirin: Significantly increased bleeding risk. Monitor INR closely if combination necessary."
                    },
                    new DrugInteraction
                    {
                        DrugCode = "5521", // Ibuprofen
                        Severity = "Major",
                        Description = "Warfarin + NSAIDs: Increased bleeding risk and potential for dangerous INR elevation"
                    }
                }
            }
        };

        // Disease-medication contraindications
        private readonly Dictionary<string, List<string>> _contraindicatedConditions = new()
        {
            {
                "6809", // Metformin
                new List<string>
                {
                    "46271022", // Chronic kidney disease stage 4-5 (SNOMED code)
                    "59032002"  // Severe hepatic impairment
                }
            },
            {
                "5521", // Ibuprofen
                new List<string>
                {
                    "40733004", // Chronic kidney disease (any stage)
                    "25064002", // Peptic ulcer disease
                    "49601007"  // Cardiovascular disease (increases heart attack risk)
                }
            }
        };

        public ClinicalDecisionSupportService(
            MedicationService medicationService,
            ObservationService observationService,
            ConditionService conditionService)
        {
            _medicationService = medicationService;
            _observationService = observationService;
            _conditionService = conditionService;
        }

        /// <summary>
        /// Checks for drug-drug interactions before prescribing
        /// This could prevent dangerous medication combinations
        /// </summary>
        public async Task<DrugInteractionCheckResult> CheckDrugInteractions(
    string patientId,
    string newMedicationCode)
        {
            var result = new DrugInteractionCheckResult
            {
                MedicationCode = newMedicationCode,
                Interactions = new List<DrugInteraction>(),
                SafeToPrescribe = true
            };

            // Get patient's current medications - both prescriptions and statements
            var medicationSummary = await _medicationService.GetPatientMedicationSummary(patientId);

            // We need to check BOTH active prescriptions AND current medications
            var allCurrentMedications = new List<string>();

            // Extract codes from active prescriptions (MedicationRequest objects)
            foreach (var prescription in medicationSummary.ActivePrescriptions)
            {
                if (prescription.Medication is CodeableConcept concept)
                {
                    var rxNormCode = concept.Coding?
                        .FirstOrDefault(c => c.System?.Contains("rxnorm") == true)?.Code;
                    if (!string.IsNullOrEmpty(rxNormCode))
                    {
                        allCurrentMedications.Add(rxNormCode);
                    }
                }
            }

            // Extract codes from current medication statements
            foreach (var statement in medicationSummary.CurrentMedications)
            {
                if (statement.Medication is CodeableConcept concept)
                {
                    var rxNormCode = concept.Coding?
                        .FirstOrDefault(c => c.System?.Contains("rxnorm") == true)?.Code;
                    if (!string.IsNullOrEmpty(rxNormCode))
                    {
                        allCurrentMedications.Add(rxNormCode);
                    }
                }
            }

            // Now check for interactions with each current medication
            foreach (var currentMedCode in allCurrentMedications)
            {
                DrugInteraction interaction = null;

                // Check if the NEW medication has listed interactions with current meds
                if (_drugInteractions.ContainsKey(newMedicationCode))
                {
                    interaction = _drugInteractions[newMedicationCode]
                        .FirstOrDefault(i => i.DrugCode == currentMedCode);
                }

                // ALSO check if current medications have listed interactions with the new med
                // This is crucial for bidirectional checking
                if (interaction == null && _drugInteractions.ContainsKey(currentMedCode))
                {
                    var reverseInteraction = _drugInteractions[currentMedCode]
                        .FirstOrDefault(i => i.DrugCode == newMedicationCode);

                    if (reverseInteraction != null)
                    {
                        // Create the interaction from the reverse perspective
                        interaction = new DrugInteraction
                        {
                            DrugCode = currentMedCode,
                            Severity = reverseInteraction.Severity,
                            Description = reverseInteraction.Description
                        };
                    }
                }

                // Add the interaction if found
                if (interaction != null)
                {
                    result.Interactions.Add(interaction);

                    if (interaction.Severity == "Major")
                    {
                        result.SafeToPrescribe = false;
                    }
                }
            }

            // Generate detailed warning message
            if (result.Interactions.Any())
            {
                var majorCount = result.Interactions.Count(i => i.Severity == "Major");
                var moderateCount = result.Interactions.Count(i => i.Severity == "Moderate");

                result.WarningMessage = $"Found {result.Interactions.Count} drug interaction(s): " +
                    $"{majorCount} major, {moderateCount} moderate. ";

                // Add specific warnings for each interaction
                foreach (var interaction in result.Interactions)
                {
                    result.WarningMessage += $"\n- {interaction.Description}";
                }

                result.WarningMessage += result.SafeToPrescribe
                    ? "\nProceed with caution and monitor closely."
                    : "\nPrescription blocked due to major interactions.";
            }
            else
            {
                result.WarningMessage = "No drug interactions detected";
            }

            return result;
        }

        /// <summary>
        /// Checks if a medication is contraindicated based on patient's conditions
        /// </summary>
        public async Task<ContraindicationCheckResult> CheckContraindications(
            string patientId,
            string medicationCode)
        {
            var result = new ContraindicationCheckResult
            {
                MedicationCode = medicationCode,
                Contraindications = new List<string>(),
                SafeToPrescribe = true
            };

            // Get patient's active conditions
            var conditions = await _conditionService.GetActiveConditions(patientId);

            // Check if medication has any contraindications
            if (_contraindicatedConditions.ContainsKey(medicationCode))
            {
                var contraindicatedSnomedCodes = _contraindicatedConditions[medicationCode];

                foreach (var condition in conditions)
                {
                    // Extract SNOMED code from condition
                    var snomedCode = condition.Code?.Coding?
                        .FirstOrDefault(c => c.System?.Contains("snomed") == true)?.Code;

                    if (!string.IsNullOrEmpty(snomedCode) &&
                        contraindicatedSnomedCodes.Contains(snomedCode))
                    {
                        result.Contraindications.Add(
                            $"{condition.Code?.Text ?? "Unknown condition"} - " +
                            "This medication is contraindicated for this condition");
                        result.SafeToPrescribe = false;
                    }
                }
            }

            result.WarningMessage = result.SafeToPrescribe
                ? "No contraindications found"
                : $"Medication contraindicated due to {result.Contraindications.Count} condition(s)";

            return result;
        }

        /// <summary>
        /// Analyzes vital signs and lab results for critical values
        /// Returns alerts for values requiring immediate attention
        /// </summary>
        public async Task<List<ClinicalAlert>> CheckCriticalValues(string patientId)
        {
            var alerts = new List<ClinicalAlert>();

            // Get recent observations
            var observations = await _observationService.GetPatientObservations(patientId, null);

            foreach (var obs in observations)
            {
                var alert = CheckObservationForCriticalValue(obs);
                if (alert != null)
                {
                    alerts.Add(alert);
                }
            }

            return alerts;
        }

        /// <summary>
        /// Checks a single observation for critical values
        /// </summary>
        private ClinicalAlert CheckObservationForCriticalValue(Observation observation)
        {
            var loincCode = observation.Code?.Coding?
                .FirstOrDefault(c => c.System?.Contains("loinc") == true)?.Code;

            if (string.IsNullOrEmpty(loincCode))
                return null;

            // Extract the value from the observation
            if (observation.Value is Quantity quantity)
            {
                decimal value = quantity.Value ?? 0;

                switch (loincCode)
                {
                    case "1558-6": // Fasting glucose
                        if (value > 300)
                        {
                            return new ClinicalAlert
                            {
                                Severity = AlertSeverity.Critical,
                                Type = "Critical Lab Value",
                                Message = $"Critical glucose level: {value} mg/dL (>300)",
                                RequiresImmediateAction = true,
                                Recommendation = "Immediate medical intervention required for severe hyperglycemia"
                            };
                        }
                        else if (value < 50)
                        {
                            return new ClinicalAlert
                            {
                                Severity = AlertSeverity.Critical,
                                Type = "Critical Lab Value",
                                Message = $"Dangerously low glucose: {value} mg/dL (<50)",
                                RequiresImmediateAction = true,
                                Recommendation = "Immediate glucose administration required"
                            };
                        }
                        break;

                    case "4548-4": // HbA1c
                        if (value > 10)
                        {
                            return new ClinicalAlert
                            {
                                Severity = AlertSeverity.High,
                                Type = "Poor Disease Control",
                                Message = $"Very poor diabetes control: HbA1c {value}% (>10)",
                                RequiresImmediateAction = false,
                                Recommendation = "Urgent medication adjustment and specialist referral recommended"
                            };
                        }
                        break;
                }
            }

            // Check blood pressure (compound observation)
            if (loincCode == "85354-9" && observation.Component?.Any() == true)
            {
                var systolic = observation.Component
                    .FirstOrDefault(c => c.Code?.Coding?.Any(coding =>
                        coding.Code == "8480-6") == true)?.Value as Quantity;
                var diastolic = observation.Component
                    .FirstOrDefault(c => c.Code?.Coding?.Any(coding =>
                        coding.Code == "8462-4") == true)?.Value as Quantity;

                if (systolic?.Value > 180 || diastolic?.Value > 120)
                {
                    return new ClinicalAlert
                    {
                        Severity = AlertSeverity.Critical,
                        Type = "Hypertensive Crisis",
                        Message = $"Hypertensive emergency: {systolic?.Value}/{diastolic?.Value} mmHg",
                        RequiresImmediateAction = true,
                        Recommendation = "Immediate blood pressure reduction required - potential organ damage"
                    };
                }
            }

            return null;
        }

        /// <summary>
        /// Checks if the patient is already taking the same medication
        /// This prevents dangerous duplicate therapy
        /// </summary>
        public async Task<DuplicateTherapyCheckResult> CheckDuplicateTherapy(
            string patientId,
            string medicationCode,
            string medicationName)
        {
            var result = new DuplicateTherapyCheckResult
            {
                MedicationCode = medicationCode,
                IsDuplicate = false,
                ExistingMedications = new List<string>()
            };

            // Get patient's current medications
            var medicationSummary = await _medicationService.GetPatientMedicationSummary(patientId);

            // Check active prescriptions for duplicates
            foreach (var prescription in medicationSummary.ActivePrescriptions)
            {
                if (prescription.Medication is CodeableConcept concept)
                {
                    var existingCode = concept.Coding?
                        .FirstOrDefault(c => c.System?.Contains("rxnorm") == true)?.Code;

                    // Check for exact match (same medication code)
                    if (existingCode == medicationCode)
                    {
                        result.IsDuplicate = true;
                        result.ExistingMedications.Add($"Active prescription for {concept.Text ?? medicationName}");
                    }

                    // You could also check for same drug class here
                    // For example, multiple statins or multiple ACE inhibitors
                }
            }

            // Check current medication statements for duplicates
            foreach (var statement in medicationSummary.CurrentMedications)
            {
                if (statement.Medication is CodeableConcept concept)
                {
                    var existingCode = concept.Coding?
                        .FirstOrDefault(c => c.System?.Contains("rxnorm") == true)?.Code;

                    if (existingCode == medicationCode)
                    {
                        result.IsDuplicate = true;
                        result.ExistingMedications.Add($"Patient reports taking {concept.Text ?? medicationName}");
                    }
                }
            }

            // Generate appropriate warning message
            if (result.IsDuplicate)
            {
                result.WarningMessage = $"DUPLICATE THERAPY WARNING: Patient is already taking {medicationName}. ";
                result.WarningMessage += $"Found {result.ExistingMedications.Count} existing prescription(s)/statement(s). ";
                result.WarningMessage += "Prescribing again could lead to overdose. ";
                result.WarningMessage += "If dose adjustment is intended, discontinue existing prescription first.";
                result.SafeToPrescribe = false;
            }
            else
            {
                result.WarningMessage = "No duplicate therapy detected";
                result.SafeToPrescribe = true;
            }

            return result;
        }

        /// <summary>
        /// Generates care gap alerts for overdue preventive care
        /// </summary>
        public async Task<List<CareGapAlert>> IdentifyCareGaps(string patientId)
        {
            var careGaps = new List<CareGapAlert>();

            // Get patient's conditions to determine what monitoring they need
            var conditions = await _conditionService.GetActiveConditions(patientId);
            var observations = await _observationService.GetPatientObservations(patientId, null);

            // Check for diabetes-related care gaps
            var hasDiabetes = conditions.Any(c =>
                c.Code?.Coding?.Any(coding =>
                    coding.Code == "44054006") == true); // Type 2 diabetes SNOMED code

            if (hasDiabetes)
            {
                // Check for recent HbA1c
                var latestHbA1c = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (latestHbA1c == null || IsOverdue(latestHbA1c.Effective, 90))
                {
                    careGaps.Add(new CareGapAlert
                    {
                        Type = "Diabetes Monitoring",
                        Message = "HbA1c test overdue (recommended every 3 months)",
                        DaysSinceLastCompleted = latestHbA1c != null ?
                            GetDaysSince(latestHbA1c.Effective) : 999,
                        Priority = "High"
                    });
                }

                // In a complete system, we'd also check for:
                // - Annual eye exams
                // - Annual foot exams
                // - Kidney function tests
                // - Lipid panels
            }

            // Check for hypertension-related care gaps
            var hasHypertension = conditions.Any(c =>
                c.Code?.Coding?.Any(coding =>
                    coding.Code == "59621000") == true); // Essential hypertension SNOMED code

            if (hasHypertension)
            {
                var latestBP = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "85354-9") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (latestBP == null || IsOverdue(latestBP.Effective, 30))
                {
                    careGaps.Add(new CareGapAlert
                    {
                        Type = "Blood Pressure Monitoring",
                        Message = "Blood pressure check overdue (recommended monthly for hypertension)",
                        DaysSinceLastCompleted = latestBP != null ?
                            GetDaysSince(latestBP.Effective) : 999,
                        Priority = "Medium"
                    });
                }
            }

            return careGaps;
        }

        /// <summary>
        /// Helper method to extract medication code from a MedicationStatement
        /// </summary>
        private string ExtractMedicationCode(MedicationStatement statement)
        {
            if (statement.Medication is CodeableConcept concept)
            {
                return concept.Coding?.FirstOrDefault(c =>
                    c.System?.Contains("rxnorm") == true)?.Code;
            }
            return null;
        }

        /// <summary>
        /// Checks if a date is overdue by specified number of days
        /// </summary>
        private bool IsOverdue(DataType effectiveDate, int dayThreshold)
        {
            if (effectiveDate is FhirDateTime fhirDateTime &&
                DateTime.TryParse(fhirDateTime.Value, out DateTime date))
            {
                return (DateTime.Now - date).TotalDays > dayThreshold;
            }
            return true; // If we can't parse the date, assume it's overdue
        }

        /// <summary>
        /// Gets the number of days since a given date
        /// </summary>
        private int GetDaysSince(DataType effectiveDate)
        {
            if (effectiveDate is FhirDateTime fhirDateTime &&
                DateTime.TryParse(fhirDateTime.Value, out DateTime date))
            {
                return (int)(DateTime.Now - date).TotalDays;
            }
            return 999; // Return a high number if we can't parse
        }
    }

    // Supporting classes for decision support results

    // Add this class to your models
    public class DuplicateTherapyCheckResult
    {
        public string MedicationCode { get; set; }
        public bool IsDuplicate { get; set; }
        public List<string> ExistingMedications { get; set; }
        public bool SafeToPrescribe { get; set; }
        public string WarningMessage { get; set; }
    }
    public class DrugInteraction
    {
        public string DrugCode { get; set; }
        public string Severity { get; set; } // Major, Moderate, Minor
        public string Description { get; set; }
    }

    public class DrugInteractionCheckResult
    {
        public string MedicationCode { get; set; }
        public List<DrugInteraction> Interactions { get; set; }
        public bool SafeToPrescribe { get; set; }
        public string WarningMessage { get; set; }
    }

    public class ContraindicationCheckResult
    {
        public string MedicationCode { get; set; }
        public List<string> Contraindications { get; set; }
        public bool SafeToPrescribe { get; set; }
        public string WarningMessage { get; set; }
    }

    public class ClinicalAlert
    {
        public AlertSeverity Severity { get; set; }
        public string Type { get; set; }
        public string Message { get; set; }
        public bool RequiresImmediateAction { get; set; }
        public string Recommendation { get; set; }
    }

    public enum AlertSeverity
    {
        Low,
        Medium,
        High,
        Critical
    }

    public class CareGapAlert
    {
        public string Type { get; set; }
        public string Message { get; set; }
        public int DaysSinceLastCompleted { get; set; }
        public string Priority { get; set; }
    }
}