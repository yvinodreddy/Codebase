using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Hl7.Fhir.Model;
using FHIRHealthcareAPI.Services;
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Clinical
{
    public class ClinicalDecisionSupportEngine
    {
        private readonly PatientService _patientService;
        private readonly ConditionService _conditionService;
        private readonly ObservationService _observationService;
        private readonly MedicationService _medicationService;
        private readonly ILogger<ClinicalDecisionSupportEngine> _logger;

        public ClinicalDecisionSupportEngine(
            PatientService patientService,
            ConditionService conditionService,
            ObservationService observationService,
            MedicationService medicationService,
            ILogger<ClinicalDecisionSupportEngine> logger)
        {
            _patientService = patientService;
            _conditionService = conditionService;
            _observationService = observationService;
            _medicationService = medicationService;
            _logger = logger;
        }

        /// <summary>
        /// Comprehensive clinical decision support analysis for a patient
        /// </summary>
        public async Task<ClinicalDecisionSupportReport> GenerateComprehensiveAnalysis(string patientId)
        {
            var report = new ClinicalDecisionSupportReport
            {
                PatientId = patientId,
                AnalysisDate = DateTime.UtcNow
            };

            try
            {
                // Gather patient data
                var conditions = await _conditionService.GetActiveConditions(patientId);
                var observations = await _observationService.GetPatientObservations(patientId);
                var medications = await _medicationService.GetPatientMedicationSummary(patientId);

                // Run clinical decision support rules
                report.Alerts = await GenerateClinicalAlerts(patientId, conditions, observations, medications);
                report.Recommendations = await GenerateEvidenceBasedRecommendations(conditions, observations);
                report.RiskAssessments = await PerformRiskAssessments(conditions, observations);
                report.CareGaps = await IdentifyCareGaps(patientId, conditions, observations);
                report.QualityMeasures = await CalculateQualityMeasures(conditions, observations, medications);

                _logger.LogInformation($"Generated comprehensive CDS analysis for patient {patientId}");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error generating CDS analysis for patient {patientId}");
                report.Errors = new List<string> { ex.Message };
            }

            return report;
        }

        /// <summary>
        /// Generates real-time clinical alerts based on current patient data
        /// </summary>
        private async Task<List<ClinicalAlert>> GenerateClinicalAlerts(
            string patientId,
            List<Condition> conditions,
            List<Observation> observations,
            MedicationSummary medications)
        {
            var alerts = new List<ClinicalAlert>();

            // Critical glucose alerts
            var glucoseObs = observations
                .Where(o => o.Code?.Coding?.Any(c => c.Code == "33747-0") == true)
                .OrderByDescending(o => o.Effective)
                .FirstOrDefault();

            if (glucoseObs?.Value is Quantity glucose)
            {
                if (glucose.Value < 70)
                {
                    alerts.Add(new ClinicalAlert
                    {
                        Severity = AlertSeverity.Critical,
                        Title = "Hypoglycemia Alert",
                        Message = $"Critical low glucose level: {glucose.Value} mg/dL",
                        ActionRequired = "Immediate intervention required - administer glucose",
                        EvidenceLevel = "A"
                    });
                }
                else if (glucose.Value > 400)
                {
                    alerts.Add(new ClinicalAlert
                    {
                        Severity = AlertSeverity.Critical,
                        Title = "Severe Hyperglycemia Alert",
                        Message = $"Dangerously high glucose level: {glucose.Value} mg/dL",
                        ActionRequired = "Consider DKA evaluation, immediate medical attention",
                        EvidenceLevel = "A"
                    });
                }
            }

            // Blood pressure alerts
            var bpObs = observations
                .Where(o => o.Code?.Coding?.Any(c => c.Code == "85354-9") == true)
                .OrderByDescending(o => o.Effective)
                .FirstOrDefault();

            if (bpObs?.Component != null && bpObs.Component.Count >= 2)
            {
                var systolic = bpObs.Component.FirstOrDefault(c => c.Code?.Coding?.Any(cd => cd.Code == "8480-6") == true)?.Value as Quantity;
                var diastolic = bpObs.Component.FirstOrDefault(c => c.Code?.Coding?.Any(cd => cd.Code == "8462-4") == true)?.Value as Quantity;

                if (systolic?.Value >= 180 || diastolic?.Value >= 120)
                {
                    alerts.Add(new ClinicalAlert
                    {
                        Severity = AlertSeverity.High,
                        Title = "Hypertensive Crisis Alert",
                        Message = $"BP: {systolic?.Value}/{diastolic?.Value} mmHg - Crisis level",
                        ActionRequired = "Immediate BP management required",
                        EvidenceLevel = "A"
                    });
                }
            }

            // HbA1c trending alerts for diabetics
            var isDiabetic = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true);
            if (isDiabetic)
            {
                var hba1cObs = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                    .OrderByDescending(o => o.Effective)
                    .Take(2)
                    .ToList();

                if (hba1cObs.Count >= 2)
                {
                    var current = hba1cObs[0].Value as Quantity;
                    var previous = hba1cObs[1].Value as Quantity;

                    if (current?.Value > previous?.Value + 1)
                    {
                        alerts.Add(new ClinicalAlert
                        {
                            Severity = AlertSeverity.Medium,
                            Title = "Worsening Diabetes Control",
                            Message = $"HbA1c increased from {previous?.Value}% to {current?.Value}%",
                            ActionRequired = "Review medication adherence and lifestyle factors",
                            EvidenceLevel = "B"
                        });
                    }
                }
            }

            return alerts;
        }

        /// <summary>
        /// Generates evidence-based treatment recommendations
        /// </summary>
        private async Task<List<ClinicalRecommendation>> GenerateEvidenceBasedRecommendations(
            List<Condition> conditions,
            List<Observation> observations)
        {
            var recommendations = new List<ClinicalRecommendation>();

            // Diabetes management recommendations
            var hasDiabetes = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true);
            if (hasDiabetes)
            {
                var latestHbA1c = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (latestHbA1c?.Value is Quantity hba1c && hba1c.Value > 7.0m)
                {
                    recommendations.Add(new ClinicalRecommendation
                    {
                        Title = "Diabetes Medication Intensification",
                        Description = $"HbA1c of {hba1c.Value}% above target of <7%. Consider medication adjustment.",
                        Rationale = "ADA guidelines recommend intensification when HbA1c >7% despite optimal therapy",
                        EvidenceLevel = "A",
                        GuidelineSource = "American Diabetes Association 2024",
                        Priority = RecommendationPriority.High,
                        SuggestedActions = new List<string>
                        {
                            "Consider adding SGLT2 inhibitor if cardiovascular disease present",
                            "Evaluate medication adherence",
                            "Refer to endocrinology if HbA1c >9%"
                        }
                    });
                }

                // Annual screening recommendations
                var lastEyeExam = await GetLastScreeningDate(observations, "eye-exam");
                if (lastEyeExam == null || lastEyeExam < DateTime.Now.AddMonths(-12))
                {
                    recommendations.Add(new ClinicalRecommendation
                    {
                        Title = "Diabetic Eye Exam Due",
                        Description = "Annual dilated eye examination recommended for diabetes management",
                        EvidenceLevel = "A",
                        Priority = RecommendationPriority.Medium,
                        SuggestedActions = new List<string> { "Schedule ophthalmology referral" }
                    });
                }
            }

            // Hypertension recommendations
            var hasHypertension = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "38341003") == true);
            if (hasHypertension)
            {
                var latestBP = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "85354-9") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (latestBP?.Component != null)
                {
                    var systolic = latestBP.Component.FirstOrDefault(c => c.Code?.Coding?.Any(cd => cd.Code == "8480-6") == true)?.Value as Quantity;

                    if (systolic?.Value > 140)
                    {
                        recommendations.Add(new ClinicalRecommendation
                        {
                            Title = "Hypertension Management",
                            Description = "Blood pressure above target (<130/80 for most patients)",
                            EvidenceLevel = "A",
                            Priority = RecommendationPriority.High,
                            SuggestedActions = new List<string>
                            {
                                "Consider ACE inhibitor or ARB if not contraindicated",
                                "Lifestyle counseling: sodium restriction, DASH diet",
                                "Home blood pressure monitoring"
                            }
                        });
                    }
                }
            }

            return recommendations;
        }

        /// <summary>
        /// Performs comprehensive risk assessments
        /// </summary>
        private async Task<List<RiskAssessment>> PerformRiskAssessments(
            List<Condition> conditions,
            List<Observation> observations)
        {
            var assessments = new List<RiskAssessment>();

            // Cardiovascular risk assessment
            var cvRisk = await CalculateCardiovascularRisk(conditions, observations);
            assessments.Add(cvRisk);

            // Diabetes complications risk
            var hasDiabetes = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true);
            if (hasDiabetes)
            {
                var diabetesRisk = await CalculateDiabetesComplicationsRisk(observations);
                assessments.Add(diabetesRisk);
            }

            return assessments;
        }

        private async Task<RiskAssessment> CalculateCardiovascularRisk(List<Condition> conditions, List<Observation> observations)
        {
            var riskFactors = new List<string>();
            var riskScore = 0;

            // Age factor (would get from patient demographics)
            // Smoking status
            // Diabetes
            if (conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true))
            {
                riskFactors.Add("Type 2 Diabetes");
                riskScore += 2;
            }

            // Hypertension
            if (conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "38341003") == true))
            {
                riskFactors.Add("Hypertension");
                riskScore += 1;
            }

            // High cholesterol
            var cholesterol = observations
                .Where(o => o.Code?.Coding?.Any(c => c.Code == "2085-9") == true)
                .OrderByDescending(o => o.Effective)
                .FirstOrDefault();

            if (cholesterol?.Value is Quantity chol && chol.Value > 200)
            {
                riskFactors.Add($"Elevated Total Cholesterol ({chol.Value} mg/dL)");
                riskScore += 1;
            }

            var riskLevel = riskScore switch
            {
                <= 1 => "Low",
                2 => "Moderate",
                >= 3 => "High"
            };

            return new RiskAssessment
            {
                Title = "10-Year Cardiovascular Disease Risk",
                RiskLevel = riskLevel,
                RiskFactors = riskFactors,
                Recommendations = riskLevel == "High"
                    ? new List<string> { "Consider statin therapy", "Aspirin prophylaxis evaluation", "Lifestyle intervention" }
                    : new List<string> { "Continue preventive measures" },
                CalculationMethod = "Simplified risk factor analysis",
                LastCalculated = DateTime.UtcNow
            };
        }

        private async Task<RiskAssessment> CalculateDiabetesComplicationsRisk(List<Observation> observations)
        {
            var riskFactors = new List<string>();
            var riskScore = 0;

            // Poor glycemic control
            var hba1c = observations
                .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                .OrderByDescending(o => o.Effective)
                .FirstOrDefault();

            if (hba1c?.Value is Quantity hba1cValue)
            {
                if (hba1cValue.Value > 9)
                {
                    riskFactors.Add($"Poor glycemic control (HbA1c {hba1cValue.Value}%)");
                    riskScore += 3;
                }
                else if (hba1cValue.Value > 7)
                {
                    riskFactors.Add($"Suboptimal glycemic control (HbA1c {hba1cValue.Value}%)");
                    riskScore += 1;
                }
            }

            var riskLevel = riskScore >= 2 ? "High" : "Moderate";

            return new RiskAssessment
            {
                Title = "Diabetes Complications Risk",
                RiskLevel = riskLevel,
                RiskFactors = riskFactors,
                Recommendations = new List<string>
                {
                    "Annual eye exam",
                    "Annual kidney function assessment",
                    "Foot care education"
                },
                LastCalculated = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Identifies gaps in evidence-based care
        /// </summary>
        private async Task<List<CareGap>> IdentifyCareGaps(
            string patientId,
            List<Condition> conditions,
            List<Observation> observations)
        {
            var careGaps = new List<CareGap>();

            // Diabetes care gaps
            var hasDiabetes = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true);
            if (hasDiabetes)
            {
                // HbA1c monitoring gap
                var lastHbA1c = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (lastHbA1c == null || DateTime.Parse(lastHbA1c.Effective.ToString()) < DateTime.Now.AddMonths(-6))
                {
                    careGaps.Add(new CareGap
                    {
                        Title = "HbA1c Monitoring Gap",
                        Description = "HbA1c should be checked every 3-6 months for diabetes management",
                        LastCompleted = lastHbA1c?.Effective?.ToString(),
                        DueDate = DateTime.Now,
                        Priority = CareGapPriority.High,
                        GuidelineSource = "ADA Standards of Medical Care"
                    });
                }
            }

            return careGaps;
        }

        private async Task<List<QualityMeasure>> CalculateQualityMeasures(
            List<Condition> conditions,
            List<Observation> observations,
            MedicationSummary medications)
        {
            var measures = new List<QualityMeasure>();

            // Diabetes quality measures
            var hasDiabetes = conditions.Any(c => c.Code?.Coding?.Any(cd => cd.Code == "44054006") == true);
            if (hasDiabetes)
            {
                // HbA1c control measure
                var latestHbA1c = observations
                    .Where(o => o.Code?.Coding?.Any(c => c.Code == "4548-4") == true)
                    .OrderByDescending(o => o.Effective)
                    .FirstOrDefault();

                if (latestHbA1c?.Value is Quantity hba1c)
                {
                    measures.Add(new QualityMeasure
                    {
                        Name = "Diabetes HbA1c Control",
                        Target = "HbA1c <7%",
                        CurrentValue = $"{hba1c.Value}%",
                        Met = hba1c.Value < 7,
                        MeasureSet = "HEDIS Diabetes Care"
                    });
                }
            }

            return measures;
        }

        private async Task<DateTime?> GetLastScreeningDate(List<Observation> observations, string screeningType)
        {
            // This would look for specific screening observations
            // Implementation depends on how screenings are coded
            return null;
        }
    }

    // Supporting data models
    public class ClinicalDecisionSupportReport
    {
        public string PatientId { get; set; }
        public DateTime AnalysisDate { get; set; }
        public List<ClinicalAlert> Alerts { get; set; } = new List<ClinicalAlert>();
        public List<ClinicalRecommendation> Recommendations { get; set; } = new List<ClinicalRecommendation>();
        public List<RiskAssessment> RiskAssessments { get; set; } = new List<RiskAssessment>();
        public List<CareGap> CareGaps { get; set; } = new List<CareGap>();
        public List<QualityMeasure> QualityMeasures { get; set; } = new List<QualityMeasure>();
        public List<string> Errors { get; set; } = new List<string>();
    }

    public class ClinicalAlert
    {
        public AlertSeverity Severity { get; set; }
        public string Title { get; set; }
        public string Message { get; set; }
        public string ActionRequired { get; set; }
        public string EvidenceLevel { get; set; }
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    public class ClinicalRecommendation
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public string Rationale { get; set; }
        public string EvidenceLevel { get; set; }
        public string GuidelineSource { get; set; }
        public RecommendationPriority Priority { get; set; }
        public List<string> SuggestedActions { get; set; } = new List<string>();
    }

    public class RiskAssessment
    {
        public string Title { get; set; }
        public string RiskLevel { get; set; }
        public List<string> RiskFactors { get; set; } = new List<string>();
        public List<string> Recommendations { get; set; } = new List<string>();
        public string CalculationMethod { get; set; }
        public DateTime LastCalculated { get; set; }
    }

    public class CareGap
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public string LastCompleted { get; set; }
        public DateTime DueDate { get; set; }
        public CareGapPriority Priority { get; set; }
        public string GuidelineSource { get; set; }
    }

    public class QualityMeasure
    {
        public string Name { get; set; }
        public string Target { get; set; }
        public string CurrentValue { get; set; }
        public bool Met { get; set; }
        public string MeasureSet { get; set; }
    }

    public enum AlertSeverity { Low, Medium, High, Critical }
    public enum RecommendationPriority { Low, Medium, High }
    public enum CareGapPriority { Low, Medium, High, Critical }
}