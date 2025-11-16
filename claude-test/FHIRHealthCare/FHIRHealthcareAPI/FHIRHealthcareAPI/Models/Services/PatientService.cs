using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using Hl7.Fhir.Serialization;

namespace FHIRHealthcareAPI.Services
{
    /// <summary>
    /// This service handles all FHIR Patient operations
    /// Think of it as a specialized librarian who knows how to 
    /// create, read, update, and delete patient records
    /// </summary>
    public class PatientService
    {
        private readonly FhirClient _fhirClient;
        private readonly FhirJsonSerializer _serializer;

        public PatientService()
        {
            // Connect to a public test FHIR server
            // This is like connecting to a library's database
            //_fhirClient = new FhirClient("http://hapi.fhir.org/baseR4");
            _fhirClient = new FhirClient("http://localhost:8080/fhir"); 

            // Set the preferred format for the FHIR client
            _fhirClient.Settings.PreferredFormat = ResourceFormat.Json;

            // Wait up to 30 seconds for responses (healthcare servers can be slow)
            _fhirClient.Settings.Timeout = 30000;

            // This serializer converts FHIR objects to/from JSON
            _serializer = new FhirJsonSerializer(new SerializerSettings
            {
                Pretty = true  // Makes the JSON human-readable
            });
        }

        /// <summary>
        /// Creates a simple test patient to verify everything works
        /// </summary>
        public async Task<Patient> CreateTestPatient()
        {
            // Step 1: Create a new patient object
            var patient = new Patient();

            // Step 2: Add an identifier (like a medical record number)
            // In real hospitals, this would be their MRN
            var identifier = new Identifier
            {
                System = "http://myhospital.org/mrn",  // Which system issued this ID
                Value = $"TEST-{DateTime.Now.Ticks}"   // Unique ID using timestamp
            };
            patient.Identifier.Add(identifier);

            // Step 3: Add the patient's name
            var name = new HumanName
            {
                Family = "TestPatient",                // Last name
                Given = new[] { "FHIR", "Demo" },     // First and middle names
                Use = HumanName.NameUse.Official      // This is their legal name
            };
            patient.Name.Add(name);

            // Step 4: Add demographics
            patient.Gender = AdministrativeGender.Male;
            patient.BirthDate = "1980-01-01";
            patient.Active = true;  // Patient record is active

            // Step 5: Add contact information
            var contact = new ContactPoint
            {
                System = ContactPoint.ContactPointSystem.Phone,
                Value = "555-0123",
                Use = ContactPoint.ContactPointUse.Mobile
            };
            patient.Telecom.Add(contact);

            // Step 6: Send to the FHIR server and get back the created patient
            try
            {
                var createdPatient = await _fhirClient.CreateAsync(patient);
                return createdPatient;
            }
            catch (Exception ex)
            {
                // If something goes wrong, we'll see what happened
                throw new Exception($"Failed to create patient: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Searches for patients by name
        /// </summary>
        public async Task<Bundle> SearchPatientsByName(string name)
        {
            try
            {
                // Add a date filter to avoid older, potentially corrupted data
                var searchParams = new SearchParams()
                    .Where($"name={name}")
                    .Where($"_lastUpdated=ge{DateTime.Now.AddDays(-1):yyyy-MM-dd}")  // Only get patients updated in last day
                    .LimitTo(10);

                var bundle = await _fhirClient.SearchAsync<Patient>(searchParams);
                return bundle;
            }
            catch (FhirOperationException ex) when (ex.Status == System.Net.HttpStatusCode.BadRequest)
            {
                // If we still get a bad request, return an empty bundle
                Console.WriteLine($"Search failed due to server data issues: {ex.Message}");
                return new Bundle
                {
                    Type = Bundle.BundleType.Searchset,
                    Entry = new List<Bundle.EntryComponent>()
                };
            }
        }

        /// <summary>
        /// Gets a specific patient by their ID
        /// </summary>
        public async Task<Patient> GetPatientById(string id)
        {
            try
            {
                // Read a specific patient from the server
                var patient = await _fhirClient.ReadAsync<Patient>($"Patient/{id}");
                return patient;
            }
            catch (FhirOperationException ex)
            {
                // Handle cases where patient doesn't exist
                if (ex.Status == System.Net.HttpStatusCode.NotFound)
                {
                    return null;  // Patient not found
                }
                throw;  // Re-throw other errors
            }
        }
    }
}