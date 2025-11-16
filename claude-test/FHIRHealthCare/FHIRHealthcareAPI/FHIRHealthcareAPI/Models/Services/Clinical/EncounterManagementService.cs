using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Clinical
{
    public class EncounterManagementService
    {
        private readonly FhirClient _fhirClient;
        private readonly SnomedService _snomedService;
        private readonly ILogger<EncounterManagementService> _logger;

        public EncounterManagementService(
            FhirClient fhirClient,
            SnomedService snomedService,
            ILogger<EncounterManagementService> logger)
        {
            _fhirClient = fhirClient;
            _snomedService = snomedService;
            _logger = logger;
        }

        /// <summary>
        /// Creates a new clinical encounter with comprehensive metadata
        /// </summary>
        public async Task<Encounter> CreateEncounter(EncounterRequest request)
        {
            // Validate reason code if provided
            if (!string.IsNullOrEmpty(request.ReasonSnomedCode))
            {
                var concept = await _snomedService.ValidateConditionCode(request.ReasonSnomedCode);
                if (!concept.IsValid)
                {
                    throw new ArgumentException($"Invalid SNOMED code for encounter reason: {request.ReasonSnomedCode}");
                }
            }

            var encounter = new Encounter
            {
                Status = Encounter.EncounterStatus.InProgress,

                // Encounter classification
                Class = new Coding
                {
                    System = "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    Code = request.EncounterType switch
                    {
                        EncounterType.Emergency => "EMER",
                        EncounterType.Inpatient => "IMP",
                        EncounterType.Outpatient => "AMB",
                        EncounterType.Virtual => "VR",
                        EncounterType.HomeHealth => "HH",
                        _ => "AMB"
                    },
                    Display = request.EncounterType.ToString()
                },

                // Patient reference
                Subject = new ResourceReference($"Patient/{request.PatientId}"),

                // Encounter period
                Period = new Period
                {
                    Start = (request.StartTime ?? DateTime.Now).ToString("yyyy-MM-ddTHH:mm:ss")
                },

                // Primary practitioner
                Participant = new List<Encounter.ParticipantComponent>
                {
                    new Encounter.ParticipantComponent
                    {
                        Type = new List<CodeableConcept>
                        {
                            new CodeableConcept
                            {
                                Coding = new List<Coding>
                                {
                                    new Coding
                                    {
                                        System = "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                        Code = "PPRF",
                                        Display = "Primary performer"
                                    }
                                }
                            }
                        },
                        Individual = new ResourceReference($"Practitioner/{request.PractitionerId}")
                    }
                },

                // Encounter reason
                ReasonCode = !string.IsNullOrEmpty(request.ReasonSnomedCode)
                    ? new List<CodeableConcept>
                    {
                        new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding
                                {
                                    System = "http://snomed.info/sct",
                                    Code = request.ReasonSnomedCode,
                                    Display = request.ReasonDescription
                                }
                            }
                        }
                    }
                    : null,

                // Service type
                ServiceType = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = "http://snomed.info/sct",
                            Code = request.ServiceTypeSnomedCode ?? "11429006",
                            Display = request.ServiceTypeDescription ?? "Consultation"
                        }
                    }
                },

                // Priority
                Priority = new CodeableConcept
                {
                    Coding = new List<Coding>
                    {
                        new Coding
                        {
                            System = "http://terminology.hl7.org/ValueSet/v3-ActPriority",
                            Code = request.Priority switch
                            {
                                EncounterPriority.Emergency => "EM",
                                EncounterPriority.Urgent => "UR",
                                EncounterPriority.Routine => "R",
                                _ => "R"
                            },
                            Display = request.Priority.ToString()
                        }
                    }
                }
            };

            // Add location if provided
            if (!string.IsNullOrEmpty(request.LocationId))
            {
                encounter.Location = new List<Encounter.LocationComponent>
                {
                    new Encounter.LocationComponent
                    {
                        Location = new ResourceReference($"Location/{request.LocationId}"),
                        Status = Encounter.EncounterLocationStatus.Active
                    }
                };
            }

            var created = await _fhirClient.CreateAsync(encounter);
            _logger.LogInformation($"Created encounter {created.Id} for patient {request.PatientId}");
            return created;
        }

        /// <summary>
        /// Completes an encounter and calculates duration
        /// </summary>
        public async Task<Encounter> CompleteEncounter(string encounterId, EncounterCompletionRequest completion)
        {
            var encounter = await _fhirClient.ReadAsync<Encounter>($"Encounter/{encounterId}");

            encounter.Status = Encounter.EncounterStatus.Finished;
            encounter.Period.End = (completion.EndTime ?? DateTime.Now).ToString("yyyy-MM-ddTHH:mm:ss");

            // Add discharge disposition if provided
            if (!string.IsNullOrEmpty(completion.DischargeDisposition))
            {
                encounter.Hospitalization = new Encounter.HospitalizationComponent
                {
                    DischargeDisposition = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                                Code = completion.DischargeDisposition,
                                Display = completion.DischargeDispositionDescription
                            }
                        }
                    }
                };
            }

            // Add diagnosis if provided
            if (completion.Diagnoses != null && completion.Diagnoses.Any())
            {
                encounter.Diagnosis = completion.Diagnoses.Select(d => new Encounter.DiagnosisComponent
                {
                    Condition = new ResourceReference($"Condition/{d.ConditionId}"),
                    Use = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://terminology.hl7.org/CodeSystem/diagnosis-role",
                                Code = d.Role,
                                Display = d.Role == "AD" ? "Admission diagnosis" : "Discharge diagnosis"
                            }
                        }
                    },
                    Rank = d.Rank
                }).ToList();
            }

            var updated = await _fhirClient.UpdateAsync(encounter);
            _logger.LogInformation($"Completed encounter {encounterId}");
            return updated;
        }

        /// <summary>
        /// Gets comprehensive encounter summary with linked resources
        /// </summary>
        public async Task<EncounterSummary> GetEncounterSummary(string encounterId)
        {
            var encounter = await _fhirClient.ReadAsync<Encounter>($"Encounter/{encounterId}");
            var patientId = encounter.Subject.Reference.Split('/').Last();

            var summary = new EncounterSummary
            {
                EncounterId = encounterId,
                PatientId = patientId,
                Status = encounter.Status?.ToString(),
                Type = encounter.Class?.Display,
                StartTime = DateTime.Parse(encounter.Period?.Start ?? DateTime.Now.ToString()),
                EndTime = encounter.Period?.End != null ? DateTime.Parse(encounter.Period.End) : null,
                PrimaryPractitioner = encounter.Participant?.FirstOrDefault()?.Individual?.Reference,
                ReasonForVisit = encounter.ReasonCode?.FirstOrDefault()?.Coding?.FirstOrDefault()?.Display
            };

            // Calculate duration if completed
            if (summary.EndTime.HasValue)
            {
                summary.Duration = summary.EndTime.Value - summary.StartTime;
            }

            // Get related observations
            summary.Observations = await GetEncounterObservations(encounterId);

            // Get procedures performed
            summary.Procedures = await GetEncounterProcedures(encounterId);

            // Get medications prescribed/administered
            summary.Medications = await GetEncounterMedications(encounterId);

            // Get diagnoses
            if (encounter.Diagnosis != null)
            {
                summary.Diagnoses = encounter.Diagnosis.Select(d => new EncounterDiagnosis
                {
                    ConditionId = d.Condition.Reference.Split('/').Last(),
                    Role = d.Use?.Coding?.FirstOrDefault()?.Code ?? "unknown",
                    Rank = d.Rank ?? 1
                }).ToList();
            }

            return summary;
        }

        private async Task<List<ObservationSummary>> GetEncounterObservations(string encounterId)
        {
            try
            {
                var searchParams = new SearchParams()
                    .Where($"encounter={encounterId}")
                    .LimitTo(50);

                var bundle = await _fhirClient.SearchAsync<Observation>(searchParams);

                return bundle.Entry
                    .Select(e => e.Resource as Observation)
                    .Where(o => o != null)
                    .Select(o => new ObservationSummary
                    {
                        Id = o.Id,
                        Type = o.Code?.Text ?? o.Code?.Coding?.FirstOrDefault()?.Display ?? "Unknown",
                        Value = GetObservationValueString(o),
                        Date = o.Effective?.ToString(),
                        Status = o.Status?.ToString()
                    })
                    .ToList();
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $"Error retrieving observations for encounter {encounterId}");
                return new List<ObservationSummary>();
            }
        }

        private async Task<List<ProcedureSummary>> GetEncounterProcedures(string encounterId)
        {
            try
            {
                var searchParams = new SearchParams()
                    .Where($"encounter={encounterId}")
                    .LimitTo(50);

                var bundle = await _fhirClient.SearchAsync<Procedure>(searchParams);

                return bundle.Entry
                    .Select(e => e.Resource as Procedure)
                    .Where(p => p != null)
                    .Select(p => new ProcedureSummary
                    {
                        Id = p.Id,
                        Name = p.Code?.Text ?? p.Code?.Coding?.FirstOrDefault()?.Display ?? "Unknown procedure",
                        Status = p.Status?.ToString(),
                        Date = p.Performed?.ToString()
                    })
                    .ToList();
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $"Error retrieving procedures for encounter {encounterId}");
                return new List<ProcedureSummary>();
            }
        }

        private async Task<List<EncounterMedicationSummary>> GetEncounterMedications(string encounterId)
        {
            // This would search for MedicationAdministration, MedicationDispense, or MedicationRequest
            // resources associated with this encounter
            return new List<EncounterMedicationSummary>();
        }

        private string GetObservationValueString(Observation observation)
        {
            if (observation.Value is Quantity quantity)
                return $"{quantity.Value} {quantity.Unit}";

            if (observation.Value is FhirString str)
                return str.Value;

            if (observation.Component != null && observation.Component.Any())
            {
                var components = observation.Component
                    .Select(c => $"{c.Code?.Coding?.FirstOrDefault()?.Display}: {(c.Value as Quantity)?.Value} {(c.Value as Quantity)?.Unit}")
                    .Where(s => !string.IsNullOrEmpty(s));
                return string.Join(", ", components);
            }

            return "No value recorded";
        }

        /// <summary>
        /// Gets encounter statistics and analytics
        /// </summary>
        public async Task<EncounterAnalytics> GetEncounterAnalytics(string patientId, DateTime startDate, DateTime endDate)
        {
            var searchParams = new SearchParams()
                .Where($"patient={patientId}")
                .Where($"date=ge{startDate:yyyy-MM-dd}")
                .Where($"date=le{endDate:yyyy-MM-dd}")
                .LimitTo(100);

            var bundle = await _fhirClient.SearchAsync<Encounter>(searchParams);
            var encounters = bundle.Entry
                .Select(e => e.Resource as Encounter)
                .Where(e => e != null)
                .ToList();

            var analytics = new EncounterAnalytics
            {
                PatientId = patientId,
                DateRange = $"{startDate:yyyy-MM-dd} to {endDate:yyyy-MM-dd}",
                TotalEncounters = encounters.Count,
                CompletedEncounters = encounters.Count(e => e.Status == Encounter.EncounterStatus.Finished),
                EmergencyEncounters = encounters.Count(e => e.Class?.Code == "EMER"),
                OutpatientEncounters = encounters.Count(e => e.Class?.Code == "AMB"),
                InpatientEncounters = encounters.Count(e => e.Class?.Code == "IMP"),
                VirtualEncounters = encounters.Count(e => e.Class?.Code == "VR")
            };

            // Calculate average duration for completed encounters
            var completedWithDuration = encounters
                .Where(e => e.Status == Encounter.EncounterStatus.Finished &&
                           !string.IsNullOrEmpty(e.Period?.End))
                .ToList();

            if (completedWithDuration.Any())
            {
                var durations = completedWithDuration
                    .Select(e => DateTime.Parse(e.Period.End) - DateTime.Parse(e.Period.Start))
                    .ToList();

                analytics.AverageDuration = TimeSpan.FromTicks((long)durations.Average(d => d.Ticks));
            }

            return analytics;
        }
    }

    // Request and response models
    public class EncounterRequest
    {
        public string PatientId { get; set; }
        public string PractitionerId { get; set; }
        public string LocationId { get; set; }
        public EncounterType EncounterType { get; set; }
        public EncounterPriority Priority { get; set; } = EncounterPriority.Routine;
        public string ReasonSnomedCode { get; set; }
        public string ReasonDescription { get; set; }
        public string ServiceTypeSnomedCode { get; set; }
        public string ServiceTypeDescription { get; set; }
        public DateTime? StartTime { get; set; }
    }

    public class EncounterCompletionRequest
    {
        public DateTime? EndTime { get; set; }
        public string DischargeDisposition { get; set; }
        public string DischargeDispositionDescription { get; set; }
        public List<EncounterDiagnosis> Diagnoses { get; set; } = new List<EncounterDiagnosis>();
    }

    public class EncounterSummary
    {
        public string EncounterId { get; set; }
        public string PatientId { get; set; }
        public string Status { get; set; }
        public string Type { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime? EndTime { get; set; }
        public TimeSpan? Duration { get; set; }
        public string PrimaryPractitioner { get; set; }
        public string ReasonForVisit { get; set; }
        public List<ObservationSummary> Observations { get; set; } = new List<ObservationSummary>();
        public List<ProcedureSummary> Procedures { get; set; } = new List<ProcedureSummary>();
        public List<EncounterMedicationSummary> Medications { get; set; } = new List<EncounterMedicationSummary>();
        public List<EncounterDiagnosis> Diagnoses { get; set; } = new List<EncounterDiagnosis>();
    }

    public class EncounterAnalytics
    {
        public string PatientId { get; set; }
        public string DateRange { get; set; }
        public int TotalEncounters { get; set; }
        public int CompletedEncounters { get; set; }
        public int EmergencyEncounters { get; set; }
        public int OutpatientEncounters { get; set; }
        public int InpatientEncounters { get; set; }
        public int VirtualEncounters { get; set; }
        public TimeSpan? AverageDuration { get; set; }
    }

    public class ObservationSummary
    {
        public string Id { get; set; }
        public string Type { get; set; }
        public string Value { get; set; }
        public string Date { get; set; }
        public string Status { get; set; }
    }

    public class ProcedureSummary
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Status { get; set; }
        public string Date { get; set; }
    }

    public class EncounterMedicationSummary
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Status { get; set; }
        public string Date { get; set; }
    }

    public class EncounterDiagnosis
    {
        public string ConditionId { get; set; }
        public string Role { get; set; }
        public int Rank { get; set; }
    }

    public enum EncounterType
    {
        Emergency,
        Inpatient,
        Outpatient,
        Virtual,
        HomeHealth
    }

    public enum EncounterPriority
    {
        Emergency,
        Urgent,
        Routine
    }
}