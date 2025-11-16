using System;
using System.Collections.Generic;

namespace HealthcareManagement.AI.Models
{
    /// <summary>
    /// AI Model classes for Healthcare Platform
    /// These models represent the AI-generated content that qualifies us as an AI startup
    /// </summary>

    #region Core AI Request/Response Models

    public class PatientSymptoms
    {
        public string PatientId { get; set; }
        public int Age { get; set; }
        public string Gender { get; set; }
        public double Weight { get; set; }
        public double Height { get; set; }
        public List<string> Symptoms { get; set; }
        public string Duration { get; set; }
        public string Severity { get; set; }
        public List<string> MedicalHistory { get; set; }
        public List<string> CurrentMedications { get; set; }
        public List<string> Allergies { get; set; }
        public VitalSigns VitalSigns { get; set; }
        public LabResults LabResults { get; set; }
    }

    public class VitalSigns
    {
        public string BloodPressure { get; set; }
        public int HeartRate { get; set; }
        public double Temperature { get; set; }
        public int RespiratoryRate { get; set; }
        public int OxygenSaturation { get; set; }
    }

    public class LabResults
    {
        public Dictionary<string, double> Values { get; set; }
        public DateTime CollectedDate { get; set; }
    }

    public class AIDiagnosisResult
    {
        public string DiagnosisId { get; set; }
        public DateTime GeneratedAt { get; set; }
        public string PatientId { get; set; }

        // Primary diagnosis
        public Diagnosis PrimaryDiagnosis { get; set; }
        public double ConfidenceScore { get; set; }

        // Differential diagnoses
        public List<DifferentialDiagnosis> DifferentialDiagnoses { get; set; }

        // Risk assessment
        public RiskAssessment RiskAssessment { get; set; }
        public string UrgencyLevel { get; set; }

        // Recommendations
        public List<string> RecommendedTests { get; set; }
        public TreatmentPlan TreatmentRecommendations { get; set; }

        // Clinical information
        public string ClinicalNotes { get; set; }
        public List<string> RedFlags { get; set; }
        public string FollowUpInstructions { get; set; }

        // AI metadata
        public string AIModelUsed { get; set; }
        public int ProcessingTimeMs { get; set; }
    }

    #endregion

    #region Diagnosis Models

    public class Diagnosis
    {
        public string Name { get; set; }
        public string ICD10Code { get; set; }
        public double Confidence { get; set; }
        public string Description { get; set; }
        public string ClinicalReasoning { get; set; }
    }

    public class DifferentialDiagnosis
    {
        public string Condition { get; set; }
        public double Probability { get; set; }
        public string ICD10Code { get; set; }
        public string[] DifferentiatingFactors { get; set; }
        public string[] RuleOutTests { get; set; }
    }

    public class GeminiDiagnosisResponse
    {
        public Diagnosis PrimaryDiagnosis { get; set; }
        public double ConfidenceScore { get; set; }
        public List<DifferentialDiagnosis> Differentials { get; set; }
        public List<string> RecommendedTests { get; set; }
        public List<TreatmentRecommendation> TreatmentRecommendations { get; set; }
        public string ClinicalNotes { get; set; }
        public List<string> RedFlags { get; set; }
    }

    public class VertexAIEnhancement
    {
        public double EnhancedConfidence { get; set; }
        public List<string> AdditionalFindings { get; set; }
        public string ModelVersion { get; set; }
    }

    #endregion

    #region Risk Assessment Models

    public class RiskAssessment
    {
        public double OverallRiskScore { get; set; }
        public string UrgencyLevel { get; set; }
        public List<string> RiskFactors { get; set; }
        public double MortalityRisk { get; set; }
        public double MorbidityRisk { get; set; }
        public bool RequiresEmergencyAction { get; set; }
        public Dictionary<string, double> OrganSystemRisks { get; set; }
    }

    public class HealthRiskProfile
    {
        public Dictionary<string, double> RiskScores { get; set; }
        public PreventionPlan PreventionPlan { get; set; }
        public HealthTrajectory HealthTrajectory { get; set; }
        public List<string> PersonalizedRecommendations { get; set; }
        public List<string> EarlyWarningIndicators { get; set; }
    }

    public class PreventionPlan
    {
        public List<PreventiveAction> Actions { get; set; }
        public string Priority { get; set; }
        public DateTime NextAssessmentDate { get; set; }
    }

    public class PreventiveAction
    {
        public string Action { get; set; }
        public string Rationale { get; set; }
        public string Frequency { get; set; }
        public double ExpectedRiskReduction { get; set; }
    }

    public class HealthTrajectory
    {
        public List<HealthDataPoint> PastData { get; set; }
        public List<HealthPrediction> FuturePredictions { get; set; }
        public double ConfidenceInterval { get; set; }
    }

    public class HealthDataPoint
    {
        public DateTime Date { get; set; }
        public double HealthScore { get; set; }
        public Dictionary<string, double> Metrics { get; set; }
    }

    public class HealthPrediction
    {
        public DateTime Date { get; set; }
        public double PredictedHealthScore { get; set; }
        public double UpperBound { get; set; }
        public double LowerBound { get; set; }
    }

    #endregion

    #region Treatment Models

    public class TreatmentPlan
    {
        public Treatment PrimaryTreatment { get; set; }
        public List<Medication> Medications { get; set; }
        public List<string> Procedures { get; set; }
        public List<string> LifestyleModifications { get; set; }
        public string FollowUpSchedule { get; set; }
        public string MonitoringPlan { get; set; }
        public Dictionary<string, string> PatientEducation { get; set; }
    }

    public class Treatment
    {
        public string Name { get; set; }
        public TreatmentType Type { get; set; }
        public string Duration { get; set; }
        public string Instructions { get; set; }
        public List<string> ExpectedOutcomes { get; set; }
        public List<string> PossibleSideEffects { get; set; }
    }

    public class TreatmentRecommendation
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public string Rationale { get; set; }
        public double EvidenceLevel { get; set; }
    }

    public class Medication
    {
        public string Name { get; set; }
        public string GenericName { get; set; }
        public string Dosage { get; set; }
        public string Frequency { get; set; }
        public string Route { get; set; }
        public string Duration { get; set; }
        public List<string> Interactions { get; set; }
        public List<string> Contraindications { get; set; }
        public MonitoringRequirement Monitoring { get; set; }
    }

    public class MonitoringRequirement
    {
        public string Parameter { get; set; }
        public string Frequency { get; set; }
        public string TargetRange { get; set; }
    }

    public enum TreatmentType
    {
        Pharmacological,
        Surgical,
        Procedural,
        Lifestyle,
        Supportive,
        Rehabilitative
    }

    #endregion

    #region Medical Image Analysis Models

    public class ImageAnalysisResult
    {
        public string AnalysisId { get; set; }
        public DateTime AnalyzedAt { get; set; }
        public List<Finding> Findings { get; set; }
        public List<Anomaly> AnomaliesDetected { get; set; }
        public double ConfidenceScore { get; set; }
        public byte[] AnnotatedImage { get; set; }
        public List<string> RecommendedActions { get; set; }
        public ComparativeAnalysis ComparativeAnalysis { get; set; }
    }

    public class Finding
    {
        public string Description { get; set; }
        public string Location { get; set; }
        public string Severity { get; set; }
        public double Confidence { get; set; }
        public BoundingBox BoundingBox { get; set; }
    }

    public class Anomaly
    {
        public string Type { get; set; }
        public string Description { get; set; }
        public double Probability { get; set; }
        public string ClinicalSignificance { get; set; }
    }

    public class BoundingBox
    {
        public int X { get; set; }
        public int Y { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
    }

    public class ComparativeAnalysis
    {
        public string ComparisonType { get; set; }
        public List<string> Changes { get; set; }
        public string Progression { get; set; }
        public double ChangeRate { get; set; }
    }

    public enum ImageType
    {
        XRay,
        MRI,
        CT,
        Ultrasound,
        PET,
        Mammogram,
        ECG,
        Other
    }

    #endregion

    #region Clinical Decision Support Models

    public class ClinicalScenario
    {
        public string Condition { get; set; }
        public PatientContext PatientContext { get; set; }
        public List<string> Symptoms { get; set; }
        public List<string> TestResults { get; set; }
        public List<string> CurrentTreatments { get; set; }
    }

    public class PatientContext
    {
        public int Age { get; set; }
        public string Gender { get; set; }
        public List<string> Comorbidities { get; set; }
        public List<string> Medications { get; set; }
        public List<string> Allergies { get; set; }
    }

    public class ClinicalDecision
    {
        public List<string> RecommendedActions { get; set; }
        public string EvidenceLevel { get; set; }
        public List<ClinicalGuideline> Guidelines { get; set; }
        public List<AlternativeApproach> Alternatives { get; set; }
        public RiskBenefitAnalysis RiskBenefitAnalysis { get; set; }
    }

    public class ClinicalGuideline
    {
        public string Source { get; set; }
        public string Title { get; set; }
        public string Recommendation { get; set; }
        public string EvidenceGrade { get; set; }
        public string URL { get; set; }
    }

    public class AlternativeApproach
    {
        public string Approach { get; set; }
        public string Rationale { get; set; }
        public double SuccessRate { get; set; }
        public List<string> Considerations { get; set; }
    }

    public class RiskBenefitAnalysis
    {
        public List<string> Benefits { get; set; }
        public List<string> Risks { get; set; }
        public double NetBenefit { get; set; }
        public string Recommendation { get; set; }
    }

    #endregion

    #region Chatbot Models

    public class ChatRequest
    {
        public string SessionId { get; set; }
        public string PatientId { get; set; }
        public string Message { get; set; }
        public string Language { get; set; }
        public bool EnableVoice { get; set; }
        public string PreferredVoice { get; set; }
        public Dictionary<string, object> Context { get; set; }
    }

    public class ChatResponse
    {
        public string Message { get; set; }
        public byte[] AudioResponse { get; set; }
        public List<string> SuggestedActions { get; set; }
        public List<Resource> Resources { get; set; }
        public bool EscalationNeeded { get; set; }
        public string Intent { get; set; }
        public double Confidence { get; set; }
    }

    public class Resource
    {
        public string Title { get; set; }
        public string Type { get; set; }
        public string URL { get; set; }
        public string Description { get; set; }
    }

    #endregion

    #region Prescription Models

    public class AIPrescription
    {
        public string PrescriptionId { get; set; }
        public DateTime GeneratedAt { get; set; }
        public List<Medication> Medications { get; set; }
        public Dictionary<string, string> Dosages { get; set; }
        public PersonalizedInstructions Instructions { get; set; }
        public MonitoringPlan MonitoringPlan { get; set; }
        public List<AlternativeMedication> AlternativeOptions { get; set; }
        public DrugInteractionAnalysis InteractionAnalysis { get; set; }
    }

    public class PersonalizedInstructions
    {
        public string Language { get; set; }
        public string ReadingLevel { get; set; }
        public List<string> Instructions { get; set; }
        public List<string> Warnings { get; set; }
        public Dictionary<string, string> VisualAids { get; set; }
    }

    public class MonitoringPlan
    {
        public List<MonitoringTask> Tasks { get; set; }
        public string Schedule { get; set; }
        public List<string> WarningSignals { get; set; }
    }

    public class MonitoringTask
    {
        public string Task { get; set; }
        public string Frequency { get; set; }
        public string Method { get; set; }
        public string TargetValue { get; set; }
    }

    public class AlternativeMedication
    {
        public string Name { get; set; }
        public string Reason { get; set; }
        public double Efficacy { get; set; }
        public double CostRatio { get; set; }
    }

    public class DrugInteractionAnalysis
    {
        public List<DrugInteraction> Interactions { get; set; }
        public string OverallRisk { get; set; }
        public List<string> Recommendations { get; set; }
    }

    public class DrugInteraction
    {
        public string Drug1 { get; set; }
        public string Drug2 { get; set; }
        public string InteractionType { get; set; }
        public string Severity { get; set; }
        public string ManagementStrategy { get; set; }
    }

    #endregion

    #region Analytics and Monitoring Models

    public class AIUsageLog
    {
        public DateTime Timestamp { get; set; }
        public string Service { get; set; }
        public string Model { get; set; }
        public int TokensUsed { get; set; }
        public int ResponseTime { get; set; }
        public double ConfidenceScore { get; set; }
        public string PatientId { get; set; }
        public string DiagnosisId { get; set; }
        public Dictionary<string, object> Metadata { get; set; }
    }

    public class AIPerformanceMetrics
    {
        public DateTime Date { get; set; }
        public int TotalRequests { get; set; }
        public double AverageConfidence { get; set; }
        public double AverageResponseTime { get; set; }
        public int TokensConsumed { get; set; }
        public decimal EstimatedCost { get; set; }
        public Dictionary<string, int> RequestsByService { get; set; }
        public Dictionary<string, double> AccuracyByService { get; set; }
    }

    #endregion

    #region Medical Report Models

    public class MedicalReport
    {
        public string ReportId { get; set; }
        public DateTime GeneratedAt { get; set; }
        public string PatientId { get; set; }
        public string ReportType { get; set; }

        public PatientInformation PatientInfo { get; set; }
        public ClinicalSummary ClinicalSummary { get; set; }
        public AssessmentAndPlan AssessmentPlan { get; set; }
        public List<DifferentialDiagnosis> Differentials { get; set; }
        public TreatmentRecommendations Treatments { get; set; }
        public FollowUpInstructions FollowUp { get; set; }
        public PatientEducation Education { get; set; }

        public string GeneratedBy { get; set; }
        public string AIModel { get; set; }
        public bool IsHL7Compliant { get; set; }
    }

    public class PatientInformation
    {
        public string Name { get; set; }
        public DateTime DateOfBirth { get; set; }
        public string MRN { get; set; }
        public string Gender { get; set; }
        public List<string> Allergies { get; set; }
        public List<string> CurrentMedications { get; set; }
    }

    public class ClinicalSummary
    {
        public string ChiefComplaint { get; set; }
        public string HistoryOfPresentIllness { get; set; }
        public string ReviewOfSystems { get; set; }
        public string PhysicalExamination { get; set; }
        public Dictionary<string, string> VitalSigns { get; set; }
        public Dictionary<string, string> LabResults { get; set; }
    }

    public class AssessmentAndPlan
    {
        public string Assessment { get; set; }
        public List<PlanItem> Plan { get; set; }
        public string Prognosis { get; set; }
    }

    public class PlanItem
    {
        public int Priority { get; set; }
        public string Problem { get; set; }
        public string Intervention { get; set; }
        public string Rationale { get; set; }
    }

    public class TreatmentRecommendations
    {
        public List<Medication> Medications { get; set; }
        public List<string> Procedures { get; set; }
        public List<string> Therapies { get; set; }
        public List<string> LifestyleChanges { get; set; }
    }

    public class FollowUpInstructions
    {
        public string NextAppointment { get; set; }
        public List<string> WarningSignals { get; set; }
        public string EmergencyInstructions { get; set; }
        public List<string> HomeMonitoring { get; set; }
    }

    public class PatientEducation
    {
        public string ConditionExplanation { get; set; }
        public List<string> KeyPoints { get; set; }
        public List<string> Resources { get; set; }
        public Dictionary<string, string> FAQs { get; set; }
    }

    #endregion
}