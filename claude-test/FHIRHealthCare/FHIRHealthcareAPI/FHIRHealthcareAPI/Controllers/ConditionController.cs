using FHIRHealthcareAPI.Services;
using Hl7.Fhir.Model;
using Hl7.Fhir.Serialization;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/fhir/[controller]")]
    [ApiController]
    public class ConditionController : ControllerBase
    {
        private readonly ConditionService _conditionService;
        private readonly FhirJsonSerializer _serializer;

        public ConditionController(ConditionService conditionService)
        {
            _conditionService = conditionService;
            _serializer = new FhirJsonSerializer(new SerializerSettings { Pretty = true });
        }

        /// <summary>
        /// POST: api/fhir/condition
        /// Records a new diagnosis for a patient
        /// </summary> 
        // Only doctors can make official diagnoses
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost]
        public async Task<IActionResult> RecordDiagnosis([FromBody] DiagnosisRequest request)
        {
            try
            {
                var condition = await _conditionService.RecordDiagnosis(
                    request.PatientId,
                    request.ConditionName,
                    request.SnomedCode,
                    request.Icd10Code,
                    request.OnsetDate,
                    request.ClinicalStatus ?? "active",
                    request.Severity,
                    request.SupportingObservationIds
                );

                var json = _serializer.SerializeToString(condition);
                return Created($"api/fhir/condition/{condition.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// POST: api/fhir/condition/diabetes
        /// Specialized endpoint for recording Type 2 Diabetes
        /// </summary> 
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost("diabetes")]
        public async Task<IActionResult> RecordDiabetes([FromBody] DiabetesRequest request)
        {
            try
            {
                var condition = await _conditionService.RecordType2Diabetes(
                    request.PatientId,
                    request.OnsetDate,
                    request.WithComplications,
                    request.SupportingObservationIds
                );

                var json = _serializer.SerializeToString(condition);
                return Created($"api/fhir/condition/{condition.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// POST: api/fhir/condition/hypertension
        /// Specialized endpoint for recording hypertension
        /// </summary> 
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost("hypertension")]
        public async Task<IActionResult> RecordHypertension([FromBody] HypertensionRequest request)
        {
            try
            {
                var condition = await _conditionService.RecordHypertension(
                    request.PatientId,
                    request.Stage,
                    request.OnsetDate,
                    request.SupportingObservationIds
                );

                var json = _serializer.SerializeToString(condition);
                return Created($"api/fhir/condition/{condition.Id}", json);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// GET: api/fhir/condition/patient/{patientId}/active
        /// Gets all active conditions for a patient
        /// </summary>
        [HttpGet("patient/{patientId}/active")]
        public async Task<IActionResult> GetActiveConditions(string patientId)
        {
            try
            {
                // Patients must only access their own diagnoses
                if (User.IsInRole("Patient"))
                {
                    var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                    if (userFhirPatientId != patientId)
                    {
                        return Forbid("You cannot view another patient's medical conditions");
                    }
                }

                // Medical staff need access for treatment decisions
                // Consider logging who accesses sensitive diagnoses
                if (User.IsInRole("Doctor") || User.IsInRole("Nurse"))
                {
                    var accessingUser = User.FindFirst(System.Security.Claims.ClaimTypes.Name)?.Value;
                    // In production: log that user X accessed patient Y's diagnoses
                    // This audit trail is crucial for investigating inappropriate access
                }

                var conditions = await _conditionService.GetActiveConditions(patientId);

                var results = conditions.Select(c => new
                {
                    id = c.Id,
                    condition = c.Code?.Text,
                    snomedCode = c.Code?.Coding?.FirstOrDefault(x => x.System.Contains("snomed"))?.Code,
                    icd10Code = c.Code?.Coding?.FirstOrDefault(x => x.System.Contains("icd-10"))?.Code,
                    onsetDate = c.Onset?.ToString(),
                    severity = c.Severity?.Coding?.FirstOrDefault()?.Display,
                    status = c.ClinicalStatus?.Coding?.FirstOrDefault()?.Display
                });

                return Ok(new
                {
                    patientId = patientId,
                    activeConditionCount = conditions.Count,
                    conditions = results
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// GET: api/fhir/condition/patient/{patientId}/history
        /// Gets complete medical history for a patient
        /// </summary>
        [HttpGet("patient/{patientId}/history")]
        public async Task<IActionResult> GetMedicalHistory(string patientId)
        {
            try
            {
                // Privacy check 
                if (User.IsInRole("Patient"))
                {
                    var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                    if (userFhirPatientId != patientId)
                    {
                        return Forbid("You cannot view another patient's medical history");
                    }
                }
                var history = await _conditionService.GetPatientMedicalHistory(patientId);

                return Ok(new
                {
                    patientId = history.PatientId,
                    hasChronicConditions = history.HasChronicConditions,
                    totalConditions = history.TotalConditions,
                    activeConditions = history.ActiveConditions.Select(c => new
                    {
                        id = c.Id,
                        name = c.Code?.Text,
                        onsetDate = c.Onset?.ToString()
                    }),
                    resolvedConditions = history.ResolvedConditions.Select(c => new
                    {
                        id = c.Id,
                        name = c.Code?.Text,
                        resolvedDate = c.Abatement?.ToString()
                    }),
                    chronicConditions = history.ChronicConditions.Select(c => new
                    {
                        id = c.Id,
                        name = c.Code?.Text,
                        duration = GetConditionDuration(c)
                    })
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        // Helper method to calculate how long a patient has had a condition
        private string GetConditionDuration(Condition condition)
        {
            if (condition.Onset is FhirDateTime onsetDateTime && DateTime.TryParse(onsetDateTime.Value, out DateTime onset))
            {
                var duration = DateTime.Now - onset;
                if (duration.TotalDays < 30)
                    return $"{(int)duration.TotalDays} days";
                else if (duration.TotalDays < 365)
                    return $"{(int)(duration.TotalDays / 30)} months";
                else
                    return $"{(int)(duration.TotalDays / 365)} years";
            }
            return "Unknown duration";
        }
    }

    // Request models
    public class DiagnosisRequest
    {
        public string PatientId { get; set; }
        public string ConditionName { get; set; }
        public string SnomedCode { get; set; }
        public string Icd10Code { get; set; }
        public DateTime? OnsetDate { get; set; }
        public string ClinicalStatus { get; set; }
        public string Severity { get; set; }
        public List<string> SupportingObservationIds { get; set; }
    }

    public class DiabetesRequest
    {
        public string PatientId { get; set; }
        public DateTime? OnsetDate { get; set; }
        public bool WithComplications { get; set; }
        public List<string> SupportingObservationIds { get; set; }
    }

    public class HypertensionRequest
    {
        public string PatientId { get; set; }
        public string Stage { get; set; } = "1";
        public DateTime? OnsetDate { get; set; }
        public List<string> SupportingObservationIds { get; set; }
    }
}