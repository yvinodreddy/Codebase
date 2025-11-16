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
    public class CarePlanManagementService
    {
        private readonly FhirClient _fhirClient;
        private readonly SnomedService _snomedService;
        private readonly LoincService _loincService;
        private readonly ILogger<CarePlanManagementService> _logger;

        public CarePlanManagementService(
            FhirClient fhirClient,
            SnomedService snomedService,
            LoincService loincService,
            ILogger<CarePlanManagementService> logger)
        {
            _fhirClient = fhirClient;
            _snomedService = snomedService;
            _loincService = loincService;
            _logger = logger;
        }

        /// <summary>
        /// Creates a comprehensive diabetes care plan with evidence-based activities
        /// </summary>
        public async Task<CarePlan> CreateDiabetesCarePlan(string patientId, string conditionId, string practitionerId)
        {
            var carePlan = new CarePlan
            {
                Status = RequestStatus.Active,
                Intent = CarePlan.CarePlanIntent.Plan,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Title = "Type 2 Diabetes Management Plan",
                Description = "Evidence-based comprehensive care plan for Type 2 Diabetes management",
                Author = new ResourceReference($"Practitioner/{practitionerId}"),
                Created = DateTime.Now.ToString("yyyy-MM-dd"),

                Category = new List<CodeableConcept>
                {
                    new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "182840001",
                                Display = "Drug treatment"
                            }
                        }
                    }
                },

                Period = new Period
                {
                    Start = DateTime.Now.ToString("yyyy-MM-dd"),
                    End = DateTime.Now.AddYears(1).ToString("yyyy-MM-dd")
                },

                Addresses = new List<ResourceReference>
                {
                    new ResourceReference($"Condition/{conditionId}")
                },

                Activity = await BuildDiabetesActivities()
            };

            var created = await _fhirClient.CreateAsync(carePlan);
            _logger.LogInformation($"Created diabetes care plan {created.Id} for patient {patientId}");
            return created;
        }

        /// <summary>
        /// Creates a hypertension care plan with monitoring and lifestyle interventions
        /// </summary>
        public async Task<CarePlan> CreateHypertensionCarePlan(string patientId, string conditionId, string practitionerId, int currentSystolic, int currentDiastolic)
        {
            var carePlan = new CarePlan
            {
                Status = RequestStatus.Active,
                Intent = CarePlan.CarePlanIntent.Plan,
                Subject = new ResourceReference($"Patient/{patientId}"),
                Title = "Hypertension Management Plan",
                Description = $"Personalized hypertension management plan - Current BP: {currentSystolic}/{currentDiastolic}",
                Author = new ResourceReference($"Practitioner/{practitionerId}"),
                Created = DateTime.Now.ToString("yyyy-MM-dd"),

                Activity = await BuildHypertensionActivities(currentSystolic, currentDiastolic)
            };

            var created = await _fhirClient.CreateAsync(carePlan);
            return created;
        }

        private async Task<List<CarePlan.ActivityComponent>> BuildDiabetesActivities()
        {
            var activities = new List<CarePlan.ActivityComponent>();

            // Blood glucose monitoring
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "33747003",
                                Display = "Blood glucose monitoring"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "Monitor blood glucose levels before meals and at bedtime",
                    Scheduled = new Timing
                    {
                        Repeat = new Timing.RepeatComponent
                        {
                            Frequency = 4,
                            Period = 1,
                            PeriodUnit = Timing.UnitsOfTime.D
                        }
                    }
                }
            });

            // HbA1c monitoring
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://loinc.org",
                                Code = "4548-4",
                                Display = "Hemoglobin A1c measurement"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "Quarterly HbA1c testing to monitor long-term glucose control",
                    Scheduled = new Timing
                    {
                        Repeat = new Timing.RepeatComponent
                        {
                            Frequency = 1,
                            Period = 3,
                            PeriodUnit = Timing.UnitsOfTime.Mo
                        }
                    }
                }
            });

            // Dietary counseling
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "11816003",
                                Display = "Diet education"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "Diabetes-specific dietary counseling focusing on carbohydrate counting and portion control"
                }
            });

            // Exercise therapy
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "229065009",
                                Display = "Exercise therapy"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "150 minutes of moderate-intensity aerobic exercise per week",
                    Scheduled = new Timing
                    {
                        Repeat = new Timing.RepeatComponent
                        {
                            Frequency = 5,
                            Period = 1,
                            PeriodUnit = Timing.UnitsOfTime.Wk
                        }
                    }
                }
            });

            // Medication adherence monitoring
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "182840001",
                                Display = "Drug treatment"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "Monitor medication adherence and adjust dosing as needed"
                }
            });

            return activities;
        }

        private async Task<List<CarePlan.ActivityComponent>> BuildHypertensionActivities(int systolic, int diastolic)
        {
            var activities = new List<CarePlan.ActivityComponent>();
            var isStage2 = systolic >= 140 || diastolic >= 90;

            // Blood pressure monitoring frequency based on current readings
            var monitoringFrequency = isStage2 ? 2 : 1; // Daily if stage 2, weekly if stage 1

            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "182744004",
                                Display = "Blood pressure monitoring"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = $"Monitor blood pressure {(isStage2 ? "daily" : "weekly")} - Target: <130/80 mmHg",
                    Scheduled = new Timing
                    {
                        Repeat = new Timing.RepeatComponent
                        {
                            Frequency = monitoringFrequency,
                            Period = 1,
                            PeriodUnit = isStage2 ? Timing.UnitsOfTime.D : Timing.UnitsOfTime.Wk
                        }
                    }
                }
            });

            // Sodium restriction
            activities.Add(new CarePlan.ActivityComponent
            {
                Detail = new CarePlan.DetailComponent
                {
                    Code = new CodeableConcept
                    {
                        Coding = new List<Coding>
                        {
                            new Coding
                            {
                                System = "http://snomed.info/sct",
                                Code = "88480006",
                                Display = "Low sodium diet"
                            }
                        }
                    },
                    Status = CarePlan.CarePlanActivityStatus.NotStarted,
                    Description = "Limit sodium intake to less than 2300mg per day (ideally 1500mg)"
                }
            });

            return activities;
        }

        /// <summary>
        /// Updates activity status and tracks care plan progress
        /// </summary>
        public async Task<CarePlan> UpdateActivityStatus(string carePlanId, int activityIndex, CarePlan.CarePlanActivityStatus newStatus, string notes = null)
        {
            var carePlan = await _fhirClient.ReadAsync<CarePlan>($"CarePlan/{carePlanId}");

            if (activityIndex < carePlan.Activity.Count)
            {
                carePlan.Activity[activityIndex].Detail.Status = newStatus;

                if (!string.IsNullOrEmpty(notes))
                {
                    carePlan.Activity[activityIndex].Progress = new List<Annotation>
                    {
                        new Annotation
                        {
                            Text = notes,
                            Time = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss")
                        }
                    };
                }
            }

            var updated = await _fhirClient.UpdateAsync(carePlan);
            _logger.LogInformation($"Updated activity {activityIndex} status to {newStatus} for care plan {carePlanId}");
            return updated;
        }

        /// <summary>
        /// Generates care plan progress report
        /// </summary>
        public async Task<CarePlanProgressReport> GenerateProgressReport(string carePlanId)
        {
            var carePlan = await _fhirClient.ReadAsync<CarePlan>($"CarePlan/{carePlanId}");

            var report = new CarePlanProgressReport
            {
                CarePlanId = carePlanId,
                PatientId = carePlan.Subject.Reference.Split('/').Last(),
                Title = carePlan.Title,
                CreatedDate = DateTime.Parse(carePlan.Created),
                TotalActivities = carePlan.Activity.Count,
                CompletedActivities = carePlan.Activity.Count(a => a.Detail.Status == CarePlan.CarePlanActivityStatus.Completed),
                InProgressActivities = carePlan.Activity.Count(a => a.Detail.Status == CarePlan.CarePlanActivityStatus.InProgress),
                NotStartedActivities = carePlan.Activity.Count(a => a.Detail.Status == CarePlan.CarePlanActivityStatus.NotStarted),
                OnHoldActivities = carePlan.Activity.Count(a => a.Detail.Status == CarePlan.CarePlanActivityStatus.OnHold)
            };

            report.CompletionPercentage = report.TotalActivities > 0
                ? (double)report.CompletedActivities / report.TotalActivities * 100
                : 0;

            return report;
        }
    }

    public class CarePlanProgressReport
    {
        public string CarePlanId { get; set; }
        public string PatientId { get; set; }
        public string Title { get; set; }
        public DateTime CreatedDate { get; set; }
        public int TotalActivities { get; set; }
        public int CompletedActivities { get; set; }
        public int InProgressActivities { get; set; }
        public int NotStartedActivities { get; set; }
        public int OnHoldActivities { get; set; }
        public double CompletionPercentage { get; set; }
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;
    }
}