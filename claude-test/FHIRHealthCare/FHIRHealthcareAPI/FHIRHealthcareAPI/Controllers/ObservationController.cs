using FHIRHealthcareAPI.Services;
using Hl7.Fhir.Model;
using Hl7.Fhir.Serialization;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/fhir/[controller]")]
    [ApiController]
    public class ObservationController : ControllerBase
    {
        private readonly ObservationService _observationService;
        private readonly FhirJsonSerializer _serializer;

        public ObservationController(ObservationService observationService)
        {
            _observationService = observationService;  
            _serializer = new FhirJsonSerializer(new SerializerSettings { Pretty = true });
        }

        /// <summary>
        /// POST: api/fhir/observation/glucose
        /// Records a blood glucose reading for a patient
        /// </summary> 
        // Recording observations - nurses and doctors do this daily
        [Authorize(Roles = "Doctor,Nurse,Admin")]
        [HttpPost("glucose")]
        public async Task<IActionResult> RecordGlucose([FromBody] GlucoseRequest request)
        {
            try
            {
                var observation = await _observationService.RecordBloodGlucose(
                    request.PatientId,
                    request.GlucoseValue,
                    request.IsFasting,
                    request.MeasuredAt
                );

                var json = _serializer.SerializeToString(observation);

                // Include interpretation in response headers for quick reference
                var interpretation = observation.Interpretation?.FirstOrDefault()?.Coding?.FirstOrDefault()?.Display;
                if (!string.IsNullOrEmpty(interpretation))
                {
                    Response.Headers.Add("X-Interpretation", interpretation);
                }

                return Created($"api/fhir/observation/{observation.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// POST: api/fhir/observation/blood-pressure
        /// Records a blood pressure reading
        /// </summary> 
        [Authorize(Roles = "Doctor,Nurse,Admin")]
        [HttpPost("blood-pressure")]
        public async Task<IActionResult> RecordBloodPressure([FromBody] BloodPressureRequest request)
        {
            try
            {
                var observation = await _observationService.RecordBloodPressure(
                    request.PatientId,
                    request.Systolic,
                    request.Diastolic,
                    request.MeasuredAt
                );

                var json = _serializer.SerializeToString(observation);
                return Created($"api/fhir/observation/{observation.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// POST: api/fhir/observation/hba1c
        /// Records an HbA1c lab result
        /// </summary> 
        [Authorize(Roles = "Doctor,Nurse,Admin")]
        [HttpPost("hba1c")]
        public async Task<IActionResult> RecordHbA1c([FromBody] HbA1cRequest request)
        {
            try
            {
                var observation = await _observationService.RecordHbA1c(
                    request.PatientId,
                    request.HbA1cPercentage,
                    request.MeasuredAt
                );

                var json = _serializer.SerializeToString(observation);
                return Created($"api/fhir/observation/{observation.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// GET: api/fhir/observation/patient/{patientId}
        /// Gets all observations for a patient
        /// </summary>
        [HttpGet("patient/{patientId}")]
        public async Task<IActionResult> GetPatientObservations(
            string patientId,
            [FromQuery] string type = null)
        {
            try
            {
                // Critical privacy check - patients can only view their own observations
                if (User.IsInRole("Patient"))
                {
                    var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                    if (userFhirPatientId != patientId)
                    {
                        // Don't reveal whether the patient exists or has observations
                        // Always return the same error message for privacy
                        return Forbid("Patients can only view their own medical observations");
                    }
                }

                // Medical staff (doctors, nurses, admin) can proceed to view any patient's observations
                // In a production system, you might add audit logging here:
                if (User.IsInRole("Doctor") || User.IsInRole("Nurse"))
                {
                    var accessingUser = User.FindFirst(System.Security.Claims.ClaimTypes.Name)?.Value;
                    // Log: user X accessed patient Y's observations at time Z
                    // This creates an audit trail for HIPAA compliance
                }

                List<Observation> observations; // Declare the 'observations' variable here

                // Special handling for glucose to include both fasting and random
                if (type?.ToLower() == "glucose")
                {
                    // Get both fasting and random glucose observations
                    var fastingGlucose = await _observationService.GetPatientObservations(patientId, "1558-6");
                    var randomGlucose = await _observationService.GetPatientObservations(patientId, "2339-0");

                    // Combine the results
                    observations = new List<Observation>();
                    observations.AddRange(fastingGlucose);
                    observations.AddRange(randomGlucose);
                }
                else
                {
                    // For other types, use the original logic
                    string loincCode = type?.ToLower() switch
                    {
                        "bp" or "blood-pressure" => "85354-9",
                        "hba1c" => "4548-4",
                        _ => null
                    };

                    observations = await _observationService.GetPatientObservations(patientId, loincCode);
                }

                // Rest of your method remains the same...
                var results = observations.Select(o => new
                {
                    id = o.Id,
                    type = o.Code?.Text,
                    value = GetObservationValue(o),
                    interpretation = o.Interpretation?.FirstOrDefault()?.Coding?.FirstOrDefault()?.Display,
                    date = o.Effective?.ToString(),
                    status = o.Status?.ToString()
                });

                return Ok(new
                {
                    patientId = patientId,
                    observationCount = observations.Count,
                    observations = results
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        // Helper method to extract observation value in a readable format
        private string GetObservationValue(Observation obs)
        {
            // Simple value (like glucose or HbA1c)
            if (obs.Value is Quantity quantity)
            {
                return $"{quantity.Value} {quantity.Unit}";
            }

            // Compound value (like blood pressure)
            if (obs.Component != null && obs.Component.Any())
            {
                var values = obs.Component
                    .Select(c => $"{c.Code?.Coding?.FirstOrDefault()?.Display}: {(c.Value as Quantity)?.Value} {(c.Value as Quantity)?.Unit}")
                    .ToList();
                return string.Join(", ", values);
            }

            return "No value";
        }
    }

    // Request models
    public class GlucoseRequest
    {
        public string PatientId { get; set; }
        public decimal GlucoseValue { get; set; }
        public bool IsFasting { get; set; }
        public DateTime? MeasuredAt { get; set; }
    }

    public class BloodPressureRequest
    {
        public string PatientId { get; set; }
        public int Systolic { get; set; }
        public int Diastolic { get; set; }
        public DateTime? MeasuredAt { get; set; }
    }

    public class HbA1cRequest
    {
        public string PatientId { get; set; }
        public decimal HbA1cPercentage { get; set; }
        public DateTime? MeasuredAt { get; set; }
    }
}