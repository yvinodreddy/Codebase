using FHIRHealthcareAPI.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using static FHIRHealthcareAPI.Services.ClinicalDecisionSupportService;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/fhir/decision-support")]
    [ApiController]
    public class DecisionSupportController : ControllerBase
    {
        private readonly ClinicalDecisionSupportService _decisionService;

        public DecisionSupportController(ClinicalDecisionSupportService decisionService)
        {
            _decisionService = decisionService;
        }

        /// <summary>
        /// POST: api/fhir/decision-support/check-interactions
        /// Checks for drug interactions before prescribing
        /// </summary>
        [HttpPost("check-interactions")]
        [Authorize(Roles = "Doctor,Admin")]
        public async Task<IActionResult> CheckDrugInteractions([FromBody] InteractionCheckRequest request)
        {
            var result = await _decisionService.CheckDrugInteractions(
                request.PatientId,
                request.MedicationCode);

            // Return appropriate status based on safety
            if (!result.SafeToPrescribe)
            {
                return BadRequest(new
                {
                    alert = "Drug Interaction Warning",
                    severity = "Major",
                    interactions = result.Interactions,
                    message = result.WarningMessage,
                    safeToPrescribe = false
                });
            }

            return Ok(new
            {
                message = result.WarningMessage,
                interactions = result.Interactions,
                safeToPrescribe = true
            });
        }

        /// <summary>
        /// POST: api/fhir/decision-support/check-duplicate
        /// Checks if patient is already taking the same medication
        /// </summary>
        [HttpPost("check-duplicate")]
        [Authorize(Roles = "Doctor,Admin")]
        public async Task<IActionResult> CheckDuplicateTherapy([FromBody] DuplicateCheckRequest request)
        {
            var result = await _decisionService.CheckDuplicateTherapy(
                request.PatientId,
                request.MedicationCode,
                request.MedicationName);

            if (result.IsDuplicate)
            {
                return BadRequest(new
                {
                    alert = "Duplicate Therapy Warning",
                    severity = "High",
                    existingMedications = result.ExistingMedications,
                    message = result.WarningMessage,
                    safeToPrescribe = false
                });
            }

            return Ok(new
            {
                message = result.WarningMessage,
                safeToPrescribe = true
            });
        }

        /// <summary>
        /// POST: api/fhir/decision-support/check-contraindications
        /// Checks if medication is contraindicated based on patient conditions
        /// </summary>
        [HttpPost("check-contraindications")]
        [Authorize(Roles = "Doctor,Admin")]
        public async Task<IActionResult> CheckContraindications([FromBody] ContraindicationCheckRequest request)
        {
            var result = await _decisionService.CheckContraindications(
                request.PatientId,
                request.MedicationCode);

            if (!result.SafeToPrescribe)
            {
                return BadRequest(new
                {
                    alert = "Contraindication Alert",
                    contraindications = result.Contraindications,
                    message = result.WarningMessage,
                    safeToPrescribe = false
                });
            }

            return Ok(new
            {
                message = result.WarningMessage,
                safeToPrescribe = true
            });
        }

        /// <summary>
        /// GET: api/fhir/decision-support/critical-values/{patientId}
        /// Gets all critical value alerts for a patient
        /// </summary>
        [HttpGet("critical-values/{patientId}")]
        public async Task<IActionResult> GetCriticalValues(string patientId)
        {
            // Check patient privacy for patient users
            if (User.IsInRole("Patient"))
            {
                var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                if (userFhirPatientId != patientId)
                {
                    return Forbid("Patients can only view their own alerts");
                }
            }

            var alerts = await _decisionService.CheckCriticalValues(patientId);

            // Categorize alerts by severity
            var criticalAlerts = alerts.Where(a => a.Severity == AlertSeverity.Critical).ToList();
            var highAlerts = alerts.Where(a => a.Severity == AlertSeverity.High).ToList();
            var otherAlerts = alerts.Where(a =>
                a.Severity != AlertSeverity.Critical &&
                a.Severity != AlertSeverity.High).ToList();

            return Ok(new
            {
                patientId = patientId,
                hasCriticalAlerts = criticalAlerts.Any(),
                alertCount = alerts.Count,
                criticalAlerts = criticalAlerts,
                highPriorityAlerts = highAlerts,
                otherAlerts = otherAlerts,
                checkedAt = DateTime.UtcNow
            });
        }

        /// <summary>
        /// GET: api/fhir/decision-support/care-gaps/{patientId}
        /// Identifies missing preventive care for a patient
        /// </summary>
        [HttpGet("care-gaps/{patientId}")]
        public async Task<IActionResult> GetCareGaps(string patientId)
        {
            // Check patient privacy
            if (User.IsInRole("Patient"))
            {
                var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                if (userFhirPatientId != patientId)
                {
                    return Forbid("Patients can only view their own care gaps");
                }
            }

            var careGaps = await _decisionService.IdentifyCareGaps(patientId);

            return Ok(new
            {
                patientId = patientId,
                totalGaps = careGaps.Count,
                hasCareGaps = careGaps.Any(),
                careGaps = careGaps.OrderBy(g => g.Priority).ToList(),
                recommendation = careGaps.Any()
                    ? "Schedule appointment to address overdue preventive care"
                    : "All preventive care is up to date"
            });
        }

        /// <summary>
        /// POST: api/fhir/decision-support/comprehensive-check
        /// Performs all safety checks before prescribing
        /// </summary>
        [HttpPost("comprehensive-check")]
        [Authorize(Roles = "Doctor,Admin")]
        public async Task<IActionResult> ComprehensivePrescriptionCheck([FromBody] PrescriptionCheckRequest request)
        {
            // Run all checks in parallel for efficiency
            var interactionTask = _decisionService.CheckDrugInteractions(
                request.PatientId, request.MedicationCode);
            var contraindicationTask = _decisionService.CheckContraindications(
                request.PatientId, request.MedicationCode);
            var duplicateTask = _decisionService.CheckDuplicateTherapy(
                request.PatientId, request.MedicationCode, request.MedicationName);

            await Task.WhenAll(interactionTask, contraindicationTask, duplicateTask);

            var interactionResult = interactionTask.Result;
            var contraindicationResult = contraindicationTask.Result;
            var duplicateResult = duplicateTask.Result;

            var overallSafe = interactionResult.SafeToPrescribe &&
                             contraindicationResult.SafeToPrescribe &&
                             duplicateResult.SafeToPrescribe;

            return Ok(new
            {
                medicationCode = request.MedicationCode,
                patientId = request.PatientId,
                overallSafety = overallSafe ? "Safe" : "Unsafe",
                canPrescribe = overallSafe,
                duplicateTherapy = new
                {
                    isDuplicate = duplicateResult.IsDuplicate,
                    existingMedications = duplicateResult.ExistingMedications,
                    warning = duplicateResult.WarningMessage
                },
                drugInteractions = new
                {
                    found = interactionResult.Interactions.Any(),
                    count = interactionResult.Interactions.Count,
                    details = interactionResult.Interactions
                },
                contraindications = new
                {
                    found = contraindicationResult.Contraindications.Any(),
                    count = contraindicationResult.Contraindications.Count,
                    details = contraindicationResult.Contraindications
                },
                recommendation = overallSafe
                    ? "Safe to prescribe with standard monitoring"
                    : "Do not prescribe - " + GetSpecificRecommendation(duplicateResult, interactionResult, contraindicationResult)
            });
        }

        private string GetSpecificRecommendation(
            DuplicateTherapyCheckResult duplicate,
            DrugInteractionCheckResult interaction,
            ContraindicationCheckResult contraindication)
        {
            if (duplicate.IsDuplicate)
                return "Patient already taking this medication. Adjust existing prescription if dose change needed.";
            if (!contraindication.SafeToPrescribe)
                return "Medication contraindicated for patient's conditions. Choose alternative therapy.";
            if (!interaction.SafeToPrescribe)
                return "Dangerous drug interaction detected. Consider alternative medication.";
            return "Review warnings and proceed with caution.";
        }
    }

    // Request models
    public class InteractionCheckRequest
    {
        public string PatientId { get; set; }
        public string MedicationCode { get; set; }
    }

    public class ContraindicationCheckRequest
    {
        public string PatientId { get; set; }
        public string MedicationCode { get; set; }
    }

    public class PrescriptionCheckRequest
    {
        public string PatientId { get; set; }
        public string MedicationCode { get; set; }
        public string MedicationName { get; set; }
    }

    // Add this request model
    public class DuplicateCheckRequest
    {
        public string PatientId { get; set; }
        public string MedicationCode { get; set; }
        public string MedicationName { get; set; }
    }
}