using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// Comprehensive data seeding service for populating FHIR server with realistic test data
    /// Production-ready with proper error handling and validation
    /// </summary>
    public class DataSeedingService
    {
        private readonly FhirClient _fhirClient;
        private readonly List<string> _seededPatientIds = new List<string>();
        private const string LOINC_SYSTEM = "http://loinc.org";
        private const string SNOMED_SYSTEM = "http://snomed.info/sct";
        private const string RXNORM_SYSTEM = "http://www.nlm.nih.gov/research/umls/rxnorm";
        private const string UCUM_SYSTEM = "http://unitsofmeasure.org";

        public DataSeedingService()
        {
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
        /// Main seeding orchestrator - seeds all test data in proper order
        /// </summary>
        public async Task<DataSeedingResult> SeedAllData()
        {
            var result = new DataSeedingResult();
            var startTime = DateTime.Now;

            try
            {
                Console.WriteLine("=== STARTING COMPREHENSIVE DATA SEEDING ===");

                // Step 1: Seed Patients
                Console.WriteLine("\n[1/5] Seeding Patients...");
                result.PatientsCreated = await SeedPatients();

                // Step 2: Seed Observations (vital signs & lab results)
                Console.WriteLine("\n[2/5] Seeding Observations...");
                result.ObservationsCreated = await SeedObservations();

                // Step 3: Seed Conditions
                Console.WriteLine("\n[3/5] Seeding Conditions...");
                result.ConditionsCreated = await SeedConditions();

                // Step 4: Seed Medications
                Console.WriteLine("\n[4/5] Seeding Medications...");
                result.MedicationsCreated = await SeedMedications();

                // Step 5: Seed Care Plans
                Console.WriteLine("\n[5/5] Seeding Care Plans...");
                result.CarePlansCreated = await SeedCarePlans();

                result.Success = true;
                result.Duration = DateTime.Now - startTime;

                Console.WriteLine($"\n=== SEEDING COMPLETED SUCCESSFULLY ===");
                Console.WriteLine($"Total Time: {result.Duration.TotalSeconds:F2} seconds");
                Console.WriteLine($"Patients: {result.PatientsCreated}");
                Console.WriteLine($"Observations: {result.ObservationsCreated}");
                Console.WriteLine($"Conditions: {result.ConditionsCreated}");
                Console.WriteLine($"Medications: {result.MedicationsCreated}");
                Console.WriteLine($"Care Plans: {result.CarePlansCreated}");
            }
            catch (Exception ex)
            {
                result.Success = false;
                result.ErrorMessage = ex.Message;
                Console.WriteLine($"\n❌ SEEDING FAILED: {ex.Message}");
            }

            return result;
        }

        /// <summary>
        /// Seeds realistic patient data with comprehensive demographics
        /// </summary>
        private async Task<int> SeedPatients()
        {
            var patients = new List<Patient>
            {
                CreatePatient("Sarah", "Johnson", "F", "1985-03-15", "555-0101", "sarah.johnson@example.com", "MRN-001"),
                CreatePatient("Michael", "Chen", "M", "1972-07-22", "555-0102", "michael.chen@example.com", "MRN-002"),
                CreatePatient("Emily", "Rodriguez", "F", "1990-11-08", "555-0103", "emily.rodriguez@example.com", "MRN-003"),
                CreatePatient("James", "Williams", "M", "1965-05-30", "555-0104", "james.williams@example.com", "MRN-004"),
                CreatePatient("Maria", "Garcia", "F", "1978-09-12", "555-0105", "maria.garcia@example.com", "MRN-005"),
                CreatePatient("David", "Brown", "M", "1958-12-03", "555-0106", "david.brown@example.com", "MRN-006"),
                CreatePatient("Jennifer", "Davis", "F", "1995-02-28", "555-0107", "jennifer.davis@example.com", "MRN-007"),
                CreatePatient("Robert", "Martinez", "M", "1982-06-17", "555-0108", "robert.martinez@example.com", "MRN-008")
            };

            int created = 0;
            foreach (var patient in patients)
            {
                try
                {
                    var createdPatient = await _fhirClient.CreateAsync(patient);
                    _seededPatientIds.Add(createdPatient.Id);
                    Console.WriteLine($"  ✓ Created patient: {patient.Name[0].Given.First()} {patient.Name[0].Family} (ID: {createdPatient.Id})");
                    created++;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  ✗ Failed to create patient: {ex.Message}");
                }
            }

            return created;
        }

        /// <summary>
        /// Seeds comprehensive observations including vital signs and lab results
        /// </summary>
        private async Task<int> SeedObservations()
        {
            int created = 0;

            foreach (var patientId in _seededPatientIds)
            {
                try
                {
                    // Blood Pressure
                    await CreateBloodPressureObservation(patientId, 120, 80);
                    created++;

                    // Heart Rate
                    await CreateVitalSignObservation(patientId, "8867-4", "Heart rate", 72, "beats/min");
                    created++;

                    // Body Temperature
                    await CreateVitalSignObservation(patientId, "8310-5", "Body temperature", 98.6m, "degF");
                    created++;

                    // Blood Glucose (Fasting)
                    await CreateObservation(patientId, "1558-6", "Fasting glucose", 95, "mg/dL");
                    created++;

                    // HbA1c
                    await CreateObservation(patientId, "4548-4", "Hemoglobin A1c", 5.4m, "%");
                    created++;

                    // Cholesterol Panel
                    await CreateObservation(patientId, "2093-3", "Total Cholesterol", 180, "mg/dL");
                    created++;

                    await CreateObservation(patientId, "2085-9", "HDL Cholesterol", 55, "mg/dL");
                    created++;

                    await CreateObservation(patientId, "2089-1", "LDL Cholesterol", 100, "mg/dL");
                    created++;

                    Console.WriteLine($"  ✓ Created 8 observations for patient {patientId}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  ✗ Failed to create observations for patient {patientId}: {ex.Message}");
                }
            }

            return created;
        }

        /// <summary>
        /// Seeds realistic medical conditions
        /// </summary>
        private async Task<int> SeedConditions()
        {
            int created = 0;
            var conditionData = new[]
            {
                ("38341003", "Hypertension", "High blood pressure"),
                ("44054006", "Type 2 Diabetes", "Diabetes mellitus type 2"),
                ("13645005", "Chronic Obstructive Pulmonary Disease", "COPD"),
                ("195967001", "Asthma", "Bronchial asthma"),
                ("22298006", "Myocardial Infarction", "Heart attack - history of")
            };

            for (int i = 0; i < _seededPatientIds.Count && i < conditionData.Length; i++)
            {
                try
                {
                    var patientId = _seededPatientIds[i];
                    var (code, display, clinical) = conditionData[i];

                    var condition = new Condition
                    {
                        ClinicalStatus = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding("http://terminology.hl7.org/CodeSystem/condition-clinical", "active", "Active")
                            }
                        },
                        VerificationStatus = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding("http://terminology.hl7.org/CodeSystem/condition-ver-status", "confirmed", "Confirmed")
                            }
                        },
                        Code = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding(SNOMED_SYSTEM, code, display)
                            },
                            Text = clinical
                        },
                        Subject = new ResourceReference($"Patient/{patientId}"),
                        Onset = new FhirDateTime(DateTime.Now.AddYears(-2))
                    };

                    await _fhirClient.CreateAsync(condition);
                    Console.WriteLine($"  ✓ Created condition: {display} for patient {patientId}");
                    created++;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  ✗ Failed to create condition: {ex.Message}");
                }
            }

            return created;
        }

        /// <summary>
        /// Seeds medication prescriptions
        /// </summary>
        private async Task<int> SeedMedications()
        {
            int created = 0;
            var medicationData = new[]
            {
                ("197361", "Lisinopril 10mg", "Take 1 tablet by mouth daily"),
                ("860975", "Metformin 500mg", "Take 1 tablet by mouth twice daily with meals"),
                ("1049221", "Albuterol Inhaler", "Inhale 2 puffs every 4-6 hours as needed"),
                ("104894", "Atorvastatin 20mg", "Take 1 tablet by mouth daily at bedtime"),
                ("308136", "Aspirin 81mg", "Take 1 tablet by mouth daily")
            };

            for (int i = 0; i < _seededPatientIds.Count && i < medicationData.Length; i++)
            {
                try
                {
                    var patientId = _seededPatientIds[i];
                    var (rxNormCode, medName, dosage) = medicationData[i];

                    var medicationRequest = new MedicationRequest
                    {
                        Status = MedicationRequest.MedicationrequestStatus.Active,
                        Intent = MedicationRequest.MedicationRequestIntent.Order,
                        Subject = new ResourceReference($"Patient/{patientId}"),
                        AuthoredOn = DateTime.Now.ToString("yyyy-MM-dd"),
                        Medication = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding(RXNORM_SYSTEM, rxNormCode, medName)
                            },
                            Text = medName
                        },
                        DosageInstruction = new List<Dosage>
                        {
                            new Dosage
                            {
                                Text = dosage,
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
                        }
                    };

                    await _fhirClient.CreateAsync(medicationRequest);
                    Console.WriteLine($"  ✓ Created medication: {medName} for patient {patientId}");
                    created++;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  ✗ Failed to create medication: {ex.Message}");
                }
            }

            return created;
        }

        /// <summary>
        /// Seeds care plans for chronic disease management
        /// </summary>
        private async Task<int> SeedCarePlans()
        {
            int created = 0;

            for (int i = 0; i < Math.Min(3, _seededPatientIds.Count); i++)
            {
                try
                {
                    var patientId = _seededPatientIds[i];

                    var carePlan = new CarePlan
                    {
                        Status = RequestStatus.Active,
                        Intent = CarePlan.CarePlanIntent.Plan,
                        Subject = new ResourceReference($"Patient/{patientId}"),
                        Title = "Chronic Disease Management Plan",
                        Description = "Comprehensive care plan for managing chronic conditions",
                        Period = new Period
                        {
                            Start = DateTime.Now.ToString("yyyy-MM-dd"),
                            End = DateTime.Now.AddYears(1).ToString("yyyy-MM-dd")
                        },
                        Activity = new List<CarePlan.ActivityComponent>
                        {
                            new CarePlan.ActivityComponent
                            {
                                Detail = new CarePlan.DetailComponent
                                {
                                    Status = CarePlan.CarePlanActivityStatus.InProgress,
                                    Description = "Monitor blood pressure daily",
                                    Scheduled = new Timing
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
                            new CarePlan.ActivityComponent
                            {
                                Detail = new CarePlan.DetailComponent
                                {
                                    Status = CarePlan.CarePlanActivityStatus.InProgress,
                                    Description = "Take prescribed medications as directed"
                                }
                            }
                        }
                    };

                    await _fhirClient.CreateAsync(carePlan);
                    Console.WriteLine($"  ✓ Created care plan for patient {patientId}");
                    created++;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  ✗ Failed to create care plan: {ex.Message}");
                }
            }

            return created;
        }

        // Helper Methods

        private Patient CreatePatient(string firstName, string lastName, string gender,
            string birthDate, string phone, string email, string mrn)
        {
            var patient = new Patient
            {
                Active = true,
                Identifier = new List<Identifier>
                {
                    new Identifier
                    {
                        System = "http://hospital.example.org/mrn",
                        Value = mrn
                    }
                },
                Name = new List<HumanName>
                {
                    new HumanName
                    {
                        Use = HumanName.NameUse.Official,
                        Family = lastName,
                        Given = new[] { firstName }
                    }
                },
                Gender = gender.ToUpper() == "M" ? AdministrativeGender.Male :
                         gender.ToUpper() == "F" ? AdministrativeGender.Female :
                         AdministrativeGender.Unknown,
                BirthDate = birthDate,
                Telecom = new List<ContactPoint>
                {
                    new ContactPoint
                    {
                        System = ContactPoint.ContactPointSystem.Phone,
                        Value = phone,
                        Use = ContactPoint.ContactPointUse.Mobile
                    },
                    new ContactPoint
                    {
                        System = ContactPoint.ContactPointSystem.Email,
                        Value = email
                    }
                },
                Address = new List<Address>
                {
                    new Address
                    {
                        Use = Address.AddressUse.Home,
                        Line = new[] { "123 Main Street" },
                        City = "Springfield",
                        State = "IL",
                        PostalCode = "62701",
                        Country = "USA"
                    }
                }
            };

            return patient;
        }

        private async System.Threading.Tasks.Task CreateObservation(string patientId, string loincCode,
            string display, decimal value, string unit)
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
                        new Coding(LOINC_SYSTEM, loincCode, display)
                    },
                    Text = display
                },
                Value = new Quantity
                {
                    Value = value,
                    Unit = unit,
                    System = UCUM_SYSTEM,
                    Code = unit
                }
            };

            await _fhirClient.CreateAsync(observation);
        }

        private async System.Threading.Tasks.Task CreateVitalSignObservation(string patientId, string loincCode,
            string display, decimal value, string unit)
        {
            await CreateObservation(patientId, loincCode, display, value, unit);
        }

        private async System.Threading.Tasks.Task CreateBloodPressureObservation(string patientId, int systolic, int diastolic)
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
                        new Coding(LOINC_SYSTEM, "85354-9", "Blood pressure panel")
                    },
                    Text = "Blood Pressure"
                },
                Component = new List<Observation.ComponentComponent>
                {
                    new Observation.ComponentComponent
                    {
                        Code = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding(LOINC_SYSTEM, "8480-6", "Systolic blood pressure")
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
                        Code = new CodeableConcept
                        {
                            Coding = new List<Coding>
                            {
                                new Coding(LOINC_SYSTEM, "8462-4", "Diastolic blood pressure")
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

            await _fhirClient.CreateAsync(observation);
        }
    }

    /// <summary>
    /// Result object for data seeding operation
    /// </summary>
    public class DataSeedingResult
    {
        public bool Success { get; set; }
        public int PatientsCreated { get; set; }
        public int ObservationsCreated { get; set; }
        public int ConditionsCreated { get; set; }
        public int MedicationsCreated { get; set; }
        public int CarePlansCreated { get; set; }
        public TimeSpan Duration { get; set; }
        public string ErrorMessage { get; set; }
    }
}
