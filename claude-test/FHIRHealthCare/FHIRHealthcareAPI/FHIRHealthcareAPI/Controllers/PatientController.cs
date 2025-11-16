using FHIRHealthcareAPI.Services;
using Hl7.Fhir.Model;
using Hl7.Fhir.Serialization;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FHIRHealthcareAPI.Controllers
{
    /// <summary>
    /// This controller handles HTTP requests for FHIR Patient resources
    /// Think of it as the reception desk that directs patient-related requests
    /// </summary> 
    [Authorize]
    [Route("api/fhir/[controller]")]
    [ApiController]
    public class PatientController : ControllerBase
    {
        private readonly PatientService _patientService;
        private readonly FhirJsonSerializer _serializer;

        public PatientController()
        {
            _patientService = new PatientService();
            _serializer = new FhirJsonSerializer(new SerializerSettings { Pretty = true });
        }

        /// <summary>
        /// GET: api/fhir/patient/test-create
        /// Creates a test patient to verify the system works
        /// </summary> 
        [Authorize(Roles = "Doctor,Nurse,Admin")]  // Add this role restriction
        [HttpGet("test-create")]
        public async Task<IActionResult> CreateTestPatient()
        {
            try
            {
                // Call our service to create a test patient
                var patient = await _patientService.CreateTestPatient();

                // Convert to JSON for the response
                var json = _serializer.SerializeToString(patient);

                // Return the created patient with a 201 Created status
                return Created($"api/fhir/patient/{patient.Id}", json);
            }
            catch (Exception ex)
            {
                // If something goes wrong, return an error
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// GET: api/fhir/patient/search?name=Smith
        /// Searches for patients by name
        /// </summary>
        [Authorize(Roles = "Doctor,Nurse,Admin")]  // Restrict searching to medical staff
        [HttpGet("search")]
        public async Task<IActionResult> SearchPatients([FromQuery] string name)
        {
            if (string.IsNullOrEmpty(name))
            {
                return BadRequest(new { error = "Please provide a name to search" });
            }

            try
            {
                var bundle = await _patientService.SearchPatientsByName(name);

                // Convert the bundle to JSON
                var json = _serializer.SerializeToString(bundle);

                // Return the search results
                return Ok(json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// GET: api/fhir/patient/{id}
        /// Gets a specific patient by ID
        /// </summary> 
        [Authorize]
        [HttpGet("{id}")]
        public async Task<IActionResult> GetPatient(string id)
        {
            try
            {
                // Critical privacy check for patient users
                if (User.IsInRole("Patient"))
                {
                    var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;

                    // Patients can only view their own record
                    if (userFhirPatientId != id)
                    {
                        // Don't reveal whether the patient ID exists or not
                        return Forbid("You can only access your own patient record");
                    }
                }

                // For medical staff, you might want to add audit logging here
                if (User.IsInRole("Doctor") || User.IsInRole("Nurse"))
                {
                    // In production, you'd log: who accessed which patient record when
                    var accessingUser = User.FindFirst(System.Security.Claims.ClaimTypes.Name)?.Value;
                    var userRole = User.FindFirst(System.Security.Claims.ClaimTypes.Role)?.Value;

                    // You could add logging here:
                    // _auditService.LogAccess(accessingUser, userRole, id, "PatientRecord", DateTime.UtcNow);
                } 

                var patient = await _patientService.GetPatientById(id);

                if (patient == null)
                {
                    return NotFound(new { error = $"Patient with ID {id} not found" });
                }

                var json = _serializer.SerializeToString(patient);
                return Ok(json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}