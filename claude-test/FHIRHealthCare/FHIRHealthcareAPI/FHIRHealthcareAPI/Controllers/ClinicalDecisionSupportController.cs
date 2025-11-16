using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using FHIRHealthcareAPI.Services.Clinical;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/clinical-decision-support")]
    [ApiController]
    public class ClinicalDecisionSupportController : ControllerBase
    {
        private readonly ClinicalDecisionSupportEngine _cdsEngine;

        public ClinicalDecisionSupportController(ClinicalDecisionSupportEngine cdsEngine)
        {
            _cdsEngine = cdsEngine;
        }

        /// <summary>
        /// Generates comprehensive clinical decision support analysis for a patient
        /// This is the "smart" feature that analyzes all patient data and provides recommendations
        /// </summary>
        [HttpGet("analysis/{patientId}")]
        public async Task<IActionResult> GetComprehensiveAnalysis(string patientId)
        {
            try
            {
                // Privacy check for patients
                if (User.IsInRole("Patient"))
                {
                    var userFhirPatientId = User.FindFirst("FhirPatientId")?.Value;
                    if (userFhirPatientId != patientId)
                    {
                        return Forbid("Patients can only view their own clinical analysis");
                    }
                }

                var analysis = await _cdsEngine.GenerateComprehensiveAnalysis(patientId);

                return Ok(new
                {
                    patientId = analysis.PatientId,
                    analysisDate = analysis.AnalysisDate,
                    summary = new
                    {
                        totalAlerts = analysis.Alerts.Count,
                        criticalAlerts = analysis.Alerts.Count(a => a.Severity == AlertSeverity.Critical),
                        highPriorityRecommendations = analysis.Recommendations.Count(r => r.Priority == RecommendationPriority.High),
                        careGaps = analysis.CareGaps.Count,
                        qualityMeasuresMet = analysis.QualityMeasures.Count(q => q.Met)
                    },
                    alerts = analysis.Alerts.Select(a => new
                    {
                        severity = a.Severity.ToString(),
                        title = a.Title,
                        message = a.Message,
                        action = a.ActionRequired,
                        evidenceLevel = a.EvidenceLevel
                    }),
                    recommendations = analysis.Recommendations.Select(r => new
                    {
                        title = r.Title,
                        description = r.Description,
                        priority = r.Priority.ToString(),
                        evidenceLevel = r.EvidenceLevel,
                        source = r.GuidelineSource,
                        actions = r.SuggestedActions
                    }),
                    riskAssessments = analysis.RiskAssessments.Select(r => new
                    {
                        title = r.Title,
                        riskLevel = r.RiskLevel,
                        factors = r.RiskFactors,
                        recommendations = r.Recommendations
                    }),
                    careGaps = analysis.CareGaps.Select(c => new
                    {
                        title = c.Title,
                        description = c.Description,
                        priority = c.Priority.ToString(),
                        dueDate = c.DueDate,
                        source = c.GuidelineSource
                    }),
                    qualityMeasures = analysis.QualityMeasures.Select(q => new
                    {
                        name = q.Name,
                        target = q.Target,
                        current = q.CurrentValue,
                        met = q.Met,
                        measureSet = q.MeasureSet
                    }),
                    errors = analysis.Errors
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Gets quick clinical alerts for emergency situations
        /// </summary>
        [HttpGet("alerts/{patientId}")]
        public async Task<IActionResult> GetCriticalAlerts(string patientId)
        {
            try
            {
                var analysis = await _cdsEngine.GenerateComprehensiveAnalysis(patientId);
                var criticalAlerts = analysis.Alerts
                    .Where(a => a.Severity == AlertSeverity.Critical || a.Severity == AlertSeverity.High)
                    .OrderByDescending(a => a.Severity)
                    .Take(5)
                    .ToList();

                return Ok(new
                {
                    patientId = patientId,
                    hasCriticalAlerts = criticalAlerts.Any(a => a.Severity == AlertSeverity.Critical),
                    criticalAlertsCount = criticalAlerts.Count(a => a.Severity == AlertSeverity.Critical),
                    alerts = criticalAlerts.Select(a => new
                    {
                        severity = a.Severity.ToString(),
                        title = a.Title,
                        message = a.Message,
                        actionRequired = a.ActionRequired,
                        timestamp = a.Timestamp
                    }),
                    checkedAt = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}