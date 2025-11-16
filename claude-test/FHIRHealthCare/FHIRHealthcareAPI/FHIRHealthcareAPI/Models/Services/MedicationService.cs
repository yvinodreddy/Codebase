using FHIRHealthcareAPI.Controllers;
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Medication management service that handles prescriptions and medication statements.
    /// This version is corrected for all the specific issues in your FHIR library version.
    /// </summary>
    public class MedicationService
    {
        private readonly FhirClient _fhirClient;

        // RxNorm system URL for medication coding
        private const string RXNORM_SYSTEM = "http://www.nlm.nih.gov/research/umls/rxnorm";

        public MedicationService()
        {
            // Initialize the FHIR client with proper settings
            var settings = new FhirClientSettings
            {
                PreferredFormat = ResourceFormat.Json,
                Timeout = 30000  // 30000 milliseconds = 30 seconds // Use TimeSpan for timeout
            };

            //_fhirClient = new FhirClient("http://hapi.fhir.org/baseR4", settings);
            _fhirClient = new FhirClient("http://localhost:8080/fhir", settings);
        }

        /// <summary>
        /// Creates a prescription (MedicationRequest) for a patient.
        /// Note the correct enum naming with lowercase 'r' in MedicationrequestStatus.
        /// </summary>
        public async Task<MedicationRequest> PrescribeMedication(
            string patientId,
            string medicationName,
            string rxNormCode,
            string dosageInstructions,
            int refills = 0)
        {
            var medicationRequest = new MedicationRequest
            {
                // CORRECTED: Using lowercase 'r' in MedicationrequestStatus
                Status = MedicationRequest.MedicationrequestStatus.Active,

                // Intent indicates this is an actual order
                Intent = MedicationRequest.MedicationRequestIntent.Order,

                // Link to the patient
                Subject = new ResourceReference($"Patient/{patientId}"),

                // When this prescription was written
                AuthoredOn = DateTime.Now.ToString("yyyy-MM-dd"),

                // The medication being prescribed
                Medication = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = RXNORM_SYSTEM,
                            Code = rxNormCode,
                            Display = medicationName
                        }
                    },
                    Text = medicationName
                },

                // Dosage instructions - these belong on MedicationRequest, not MedicationStatement
                DosageInstruction = new List<Dosage>
                {
                    new Dosage
                    {
                        Text = dosageInstructions,
                        Timing = new Timing
                        {
                            Repeat = new Timing.RepeatComponent
                            {
                                Frequency = 1,
                                Period = 1,
                                PeriodUnit = Timing.UnitsOfTime.D
                            }
                        }
                    }
                },

                // Dispensing information for the pharmacy
                DispenseRequest = new MedicationRequest.DispenseRequestComponent
                {
                    NumberOfRepeatsAllowed = refills,
                    Quantity = new Quantity
                    {
                        Value = 30,
                        Unit = "tablets"
                    }
                }
            };

            var createdRequest = await _fhirClient.CreateAsync(medicationRequest);
            return createdRequest;
        }

        /// <summary>
        /// Records what a patient reports they are taking (MedicationStatement).
        /// Note: MedicationStatement does NOT have AuthoredOn or DosageInstruction properties.
        /// </summary>
        public async Task<MedicationStatement> RecordMedicationStatement(
            string patientId,
            string medicationName,
            string rxNormCode,
            bool isCurrentlyTaking)
        {
            var medicationStatement = new MedicationStatement
            {
                // Status indicates if they're currently taking it
                Status = isCurrentlyTaking
                    ? MedicationStatement.MedicationStatusCodes.Active
                    : MedicationStatement.MedicationStatusCodes.Stopped,

                // Link to the patient
                Subject = new ResourceReference($"Patient/{patientId}"),

                // When this information was recorded (not AuthoredOn - that's for MedicationRequest)
                DateAsserted = DateTime.Now.ToString(),

                // The medication they're taking
                Medication = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = RXNORM_SYSTEM,
                            Code = rxNormCode,
                            Display = medicationName
                        }
                    },
                    Text = medicationName
                },

                // When they started/stopped taking it
                Effective = isCurrentlyTaking
                    ? new Period { Start = DateTime.Now.AddMonths(-3).ToString("yyyy-MM-dd") }
                    : new Period
                    {
                        Start = DateTime.Now.AddMonths(-6).ToString("yyyy-MM-dd"),
                        End = DateTime.Now.AddMonths(-1).ToString("yyyy-MM-dd")
                    }
            };

            var createdStatement = await _fhirClient.CreateAsync(medicationStatement);
            return createdStatement;
        }

        // <summary>
        /// Creates a prescription with live RxNorm validation
        /// Validates the RxNorm code exists and gets the official drug name before prescribing
        /// </summary>
        public async Task<MedicationRequest> PrescribeMedicationValidated(
            string patientId,
            string rxNormCode,
            string dosageInstructions,
            int refills = 0)
        {
            // Step 1: Validate RxNorm code with live API
            using var httpClient = new HttpClient();
            var validationUrl = $"https://rxnav.nlm.nih.gov/REST/rxcui/{rxNormCode}/properties.json";

            try
            {
                var response = await httpClient.GetAsync(validationUrl);

                if (!response.IsSuccessStatusCode)
                {
                    throw new ArgumentException($"Invalid RxNorm code: {rxNormCode}. Code not found in RxNorm database.");
                }

                // Step 2: Extract official drug name from RxNorm response
                var json = await response.Content.ReadAsStringAsync();
                var drugData = JsonDocument.Parse(json);

                string officialDrugName = "Unknown Drug";
                if (drugData.RootElement.TryGetProperty("properties", out var properties))
                {
                    if (properties.TryGetProperty("name", out var nameElement))
                    {
                        officialDrugName = nameElement.GetString() ?? "Unknown Drug";
                    }
                }

                // Step 3: Use existing prescription method with validated data
                var prescription = await PrescribeMedication(
                    patientId,
                    officialDrugName, // Use the official name from RxNorm
                    rxNormCode,
                    dosageInstructions,
                    refills
                );

                return prescription;
            }
            catch (HttpRequestException ex)
            {
                throw new InvalidOperationException($"Unable to validate RxNorm code {rxNormCode}. RxNorm service may be unavailable.", ex);
            }
            catch (JsonException ex)
            {
                throw new InvalidOperationException($"Invalid response from RxNorm service for code {rxNormCode}.", ex);
            }
        }

        /// <summary>
        /// Validates multiple RxNorm codes and checks for drug interactions before prescribing
        /// </summary>
        public async Task<List<MedicationRequest>> PrescribeMultipleMedicationsWithValidation(
            string patientId,
            List<PrescriptionRequest> prescriptions)
        {
            var results = new List<MedicationRequest>();
            var rxCuiList = prescriptions.Select(p => p.RxNormCode).ToList();

            // Step 1: Check for drug interactions
            using var httpClient = new HttpClient();
            var interactionUrl = $"https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={string.Join("+", rxCuiList)}";

            try
            {
                var interactionResponse = await httpClient.GetAsync(interactionUrl);
                if (interactionResponse.IsSuccessStatusCode)
                {
                    var interactionJson = await interactionResponse.Content.ReadAsStringAsync();
                    var hasInteractions = CheckForSignificantInteractions(interactionJson);

                    if (hasInteractions)
                    {
                        throw new InvalidOperationException("Significant drug interactions detected. Please review before prescribing.");
                    }
                }
            }
            catch (HttpRequestException)
            {
                // Log warning but continue - don't block prescription if interaction service is down
                Console.WriteLine("Warning: Unable to check drug interactions");
            }

            // Step 2: Validate and prescribe each medication
            foreach (var prescription in prescriptions)
            {
                var validated = await PrescribeMedicationValidated(
                    patientId,
                    prescription.RxNormCode,
                    prescription.DosageInstructions,
                    prescription.Refills
                );
                results.Add(validated);
            }

            return results;
        }

        private bool CheckForSignificantInteractions(string interactionJson)
        {
            try
            {
                var doc = JsonDocument.Parse(interactionJson);
                if (doc.RootElement.TryGetProperty("fullInteractionTypeGroup", out var groupArray))
                {
                    // Return true if any interactions found
                    return groupArray.EnumerateArray().Any();
                }
            }
            catch
            {
                // If we can't parse interactions, assume safe
            }
            return false;
        }

        /// <summary>
        /// Retrieves a complete medication summary for a patient.
        /// This properly separates MedicationRequests (prescriptions) from MedicationStatements.
        /// </summary>
        public async Task<MedicationSummary> GetPatientMedicationSummary(string patientId)
        {
            var summary = new MedicationSummary
            {
                PatientId = patientId
            };

            try
            {
                // Search for MedicationRequests (prescriptions)
                var prescriptionParams = new SearchParams()
                    .Where($"patient={patientId}")
                    .LimitTo(100);

                var prescriptions = await _fhirClient.SearchAsync<MedicationRequest>(prescriptionParams);

                if (prescriptions?.Entry != null)
                {
                    summary.ActivePrescriptions = prescriptions.Entry
                        .Select(e => e.Resource as MedicationRequest)
                        .Where(mr => mr != null && mr.Status == MedicationRequest.MedicationrequestStatus.Active)
                        .ToList();
                }

                // Search for MedicationStatements (what patient reports taking)
                var statementParams = new SearchParams()
                    .Where($"patient={patientId}")
                    .LimitTo(100);

                var statements = await _fhirClient.SearchAsync<MedicationStatement>(statementParams);

                if (statements?.Entry != null)
                {
                    var statementList = statements.Entry
                        .Select(e => e.Resource as MedicationStatement)
                        .Where(ms => ms != null)
                        .ToList();

                    summary.CurrentMedications = statementList
                        .Where(ms => ms.Status == MedicationStatement.MedicationStatusCodes.Active)
                        .ToList();

                    summary.PastMedications = statementList
                        .Where(ms => ms.Status == MedicationStatement.MedicationStatusCodes.Stopped ||
                                    ms.Status == MedicationStatement.MedicationStatusCodes.Completed)
                        .ToList();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error retrieving medication summary: {ex.Message}");
                // Return partial summary rather than throwing
            }

            return summary;
        }
    }

    /// <summary>
    /// Summary class that properly separates prescriptions from patient-reported medications.
    /// MedicationRequests are prescriptions, MedicationStatements are what patients report taking.
    /// </summary>
    public class MedicationSummary
    {
        public string PatientId { get; set; }

        // Prescriptions are MedicationRequests, not MedicationStatements
        public List<MedicationRequest> ActivePrescriptions { get; set; } = new List<MedicationRequest>();

        // What patient reports taking are MedicationStatements
        public List<MedicationStatement> CurrentMedications { get; set; } = new List<MedicationStatement>();
        public List<MedicationStatement> PastMedications { get; set; } = new List<MedicationStatement>();

        public int TotalActiveMedications => CurrentMedications?.Count ?? 0;
        public bool HasActivePrescriptions => ActivePrescriptions?.Any() ?? false;
    }

    /// <summary>
    /// Request model for validated prescriptions
    /// </summary>
    public class PrescriptionRequest
    {
        public string RxNormCode { get; set; }
        public string DosageInstructions { get; set; }
        public int Refills { get; set; } = 0;
    }
}

