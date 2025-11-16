using FHIRHealthcareAPI.Services;
using Hl7.Fhir.Model;
using Hl7.Fhir.Serialization;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/fhir/[controller]")]
    [ApiController]
    public class MedicationController : ControllerBase
    {
        private readonly MedicationService _medicationService;
        private readonly AllergyService _allergyService;
        private readonly FhirJsonSerializer _serializer;

        public MedicationController()
        {
            _medicationService = new MedicationService();
            _allergyService = new AllergyService();
            _serializer = new FhirJsonSerializer(new SerializerSettings { Pretty = true });
        }

        [HttpPost("prescribe-validated")]
        [Authorize(Roles = "Doctor,Admin")]
        public async Task<IActionResult> PrescribeValidated([FromBody] PrescriptionRequest request)
        {
            try
            {
                var prescription = await _medicationService.PrescribeMedicationValidated(
                    request.PatientId,
                    request.RxNormCode,
                    request.DosageInstructions,
                    request.Refills
                );

                return Ok(new
                {
                    success = true,
                    prescriptionId = prescription.Id,
                    message = "Prescription created with live validation"
                });
            }
            catch (ArgumentException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (InvalidOperationException ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// POST: api/fhir/medication/prescribe
        /// Creates a new prescription for a patient
        /// </summary> 
        // Only doctors can prescribe
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost("prescribe")]
        public async Task<IActionResult> PrescribeMedication([FromBody] PrescriptionRequest request)
        {
            // First, check for allergies - this is critical for patient safety
            var allergyCheck = await _allergyService.CheckMedicationAllergies(
                request.PatientId, 
                request.RxNormCode);
            
            if (!allergyCheck.SafeToPrescribe)
            {
                // Return a warning but don't block - doctor might override
                return BadRequest(new 
                { 
                    error = "Allergy Alert",
                    message = allergyCheck.WarningMessage,
                    allergies = allergyCheck.Allergies,
                    note = "Prescription blocked due to documented allergy. Consult with patient."
                });
            }
            
            // No allergies found, proceed with prescription
            var prescription = await _medicationService.PrescribeMedication(
                request.PatientId,
                request.MedicationName,
                request.RxNormCode,
                request.DosageInstructions,
                request.Refills);
            
            var json = _serializer.SerializeToString(prescription);
            return Created($"api/fhir/medication/{prescription.Id}", json);
        }

        /// <summary>
        /// GET: api/fhir/medication/patient/{patientId}
        /// Gets complete medication profile for a patient
        /// </summary>
        [HttpGet("patient/{patientId}")]
        public async Task<IActionResult> GetPatientMedications(string patientId)
        {
            // Add this privacy check at the very start
            if (User.IsInRole("Patient"))
            {
                var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                if (userFhirPatientId != patientId)
                {
                    return Forbid("Patients can only view their own medication records");
                }
            }

            var summary = await _medicationService.GetPatientMedicationSummary(patientId);

            // Create a comprehensive response
            return Ok(new
            {
                patientId = patientId,
                totalActiveMedications = summary.TotalActiveMedications,
                hasActivePrescriptions = summary.HasActivePrescriptions,
                activePrescriptions = summary.ActivePrescriptions.Select(p => new
                {
                    id = p.Id,
                    medication = (p.Medication as CodeableConcept)?.Text ?? (p.Medication as ResourceReference)?.Display,
                    status = p.Status.ToString(),
                    authoredOn = p.AuthoredOn,
                    dosage = p.DosageInstruction?.FirstOrDefault()?.Text
                }),
                currentMedications = summary.CurrentMedications.Select(m => new
                {
                    id = m.Id,
                    medication = (m.Medication as CodeableConcept)?.Text ?? (m.Medication as ResourceReference)?.Display,
                    status = m.Status.ToString(),
                    since = (m.Effective as Period)?.Start
                }),
                pastMedications = summary.PastMedications.Select(m => new
                {
                    id = m.Id,
                    medication = (m.Medication as CodeableConcept)?.Text ?? (m.Medication as ResourceReference)?.Display,
                    startDate = (m.Effective as Period)?.Start,
                    endDate = (m.Effective as Period)?.End
                })
            });
        }

        /// <summary>
        /// POST: api/fhir/medication/statement
        /// Records what medication a patient reports taking
        /// </summary> 
        [Authorize(Roles = "Doctor,Nurse,Admin")]
        [HttpPost("statement")]
        public async Task<IActionResult> RecordMedicationStatement([FromBody] MedicationStatementRequest request)
        {
            var statement = await _medicationService.RecordMedicationStatement(
                request.PatientId,
                request.MedicationName,
                request.RxNormCode,
                request.IsCurrentlyTaking);
            
            var json = _serializer.SerializeToString(statement);
            return Created($"api/fhir/medication/statement/{statement.Id}", json);
        }
    }

    // Request models for cleaner API design
    public class PrescriptionRequest
    {
        public string PatientId { get; set; }
        public string MedicationName { get; set; }
        public string RxNormCode { get; set; }
        public string DosageInstructions { get; set; }
        public int Refills { get; set; }
    }

    public class MedicationStatementRequest
    {
        public string PatientId { get; set; }
        public string MedicationName { get; set; }
        public string RxNormCode { get; set; }
        public bool IsCurrentlyTaking { get; set; }
    }
}