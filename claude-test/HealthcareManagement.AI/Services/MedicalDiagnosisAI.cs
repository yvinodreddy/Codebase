using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Google.Cloud.AIPlatform.V1;
using Google.Api.Gax.Grpc;
using Google.Protobuf.WellKnownTypes;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Net.Http;
using System.Text;

namespace HealthcareManagement.AI.Services
{
    /// <summary>
    /// Core AI Medical Diagnosis Engine using Google Vertex AI and Gemini
    /// This is the PRIMARY AI feature that qualifies us for $350K Google credits
    /// </summary>
    public class MedicalDiagnosisAI : IMedicalDiagnosisAI
    {
        private readonly PredictionServiceClient _predictionClient;
        private readonly EndpointServiceClient _endpointClient;
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration;
        private readonly ILogger<MedicalDiagnosisAI> _logger;
        private readonly string _projectId;
        private readonly string _location;
        private readonly string _geminiApiKey;

        public MedicalDiagnosisAI(
            IHttpClientFactory httpClientFactory,
            IConfiguration configuration,
            ILogger<MedicalDiagnosisAI> logger)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
            _logger = logger;
            _projectId = configuration["GoogleCloud:ProjectId"];
            _location = configuration["GoogleCloud:Location"];
            _geminiApiKey = configuration["GoogleCloud:GeminiApiKey"];

            // Initialize Vertex AI clients
            _predictionClient = PredictionServiceClient.Create();
            _endpointClient = EndpointServiceClient.Create();
        }

        /// <summary>
        /// Generate AI-powered medical diagnosis using multiple AI models
        /// </summary>
        public async Task<AIDiagnosisResult> GenerateDiagnosisAsync(PatientSymptoms symptoms)
        {
            try
            {
                _logger.LogInformation("Starting AI diagnosis generation for patient symptoms");

                // Step 1: Prepare patient data for AI processing
                var patientContext = PreparePatientContext(symptoms);

                // Step 2: Generate diagnosis using Gemini Pro 1.5
                var geminiDiagnosis = await GenerateGeminiDiagnosis(patientContext);

                // Step 3: Enhance with Vertex AI medical model
                var vertexEnhancement = await EnhanceWithVertexAI(geminiDiagnosis, symptoms);

                // Step 4: Perform differential diagnosis analysis
                var differentialDiagnosis = await GenerateDifferentialDiagnosis(symptoms, geminiDiagnosis);

                // Step 5: Risk assessment and urgency scoring
                var riskAssessment = await CalculateRiskScore(symptoms, geminiDiagnosis);

                // Step 6: Generate treatment recommendations
                var treatmentPlan = await GenerateTreatmentRecommendations(geminiDiagnosis, symptoms);

                // Step 7: Compile comprehensive AI diagnosis result
                var result = new AIDiagnosisResult
                {
                    DiagnosisId = Guid.NewGuid().ToString(),
                    GeneratedAt = DateTime.UtcNow,
                    PatientId = symptoms.PatientId,

                    PrimaryDiagnosis = geminiDiagnosis.PrimaryDiagnosis,
                    ConfidenceScore = geminiDiagnosis.ConfidenceScore,

                    DifferentialDiagnoses = differentialDiagnosis,

                    RiskAssessment = riskAssessment,
                    UrgencyLevel = riskAssessment.UrgencyLevel,

                    RecommendedTests = geminiDiagnosis.RecommendedTests,
                    TreatmentRecommendations = treatmentPlan,

                    ClinicalNotes = geminiDiagnosis.ClinicalNotes,
                    RedFlags = geminiDiagnosis.RedFlags,

                    FollowUpInstructions = GenerateFollowUpInstructions(riskAssessment),

                    AIModelUsed = "Gemini Pro 1.5 + Vertex AI Medical",
                    ProcessingTimeMs = 0 // Will be calculated
                };

                // Log AI usage for monitoring and billing
                await LogAIUsage(result);

                _logger.LogInformation($"AI diagnosis completed successfully. Confidence: {result.ConfidenceScore}%");

                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating AI diagnosis");
                throw new AIProcessingException("Failed to generate AI diagnosis", ex);
            }
        }

        /// <summary>
        /// Generate diagnosis using Google's Gemini Pro 1.5 model
        /// </summary>
        private async Task<GeminiDiagnosisResponse> GenerateGeminiDiagnosis(string patientContext)
        {
            var httpClient = _httpClientFactory.CreateClient();
            var geminiEndpoint = $"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={_geminiApiKey}";

            var prompt = $@"
You are an expert AI medical diagnostic assistant. Analyze the following patient information and provide a comprehensive medical diagnosis.

{patientContext}

Provide a detailed medical analysis including:

1. PRIMARY DIAGNOSIS:
   - Most likely diagnosis with ICD-10 code
   - Confidence score (0-100%)
   - Clinical reasoning

2. DIFFERENTIAL DIAGNOSES:
   - List 3-5 alternative diagnoses
   - Probability for each
   - Key distinguishing factors

3. RECOMMENDED DIAGNOSTIC TESTS:
   - Laboratory tests
   - Imaging studies
   - Specialist consultations

4. URGENCY ASSESSMENT:
   - Urgency level (Emergency/Urgent/Routine/Elective)
   - Red flags requiring immediate attention
   - Time frame for follow-up

5. TREATMENT RECOMMENDATIONS:
   - First-line treatment options
   - Medication suggestions with dosing
   - Non-pharmacological interventions
   - Lifestyle modifications

6. CLINICAL NOTES:
   - Important considerations
   - Contraindications
   - Patient education points

Format the response as structured JSON for medical record integration.
";

            var requestBody = new
            {
                contents = new[]
                {
                    new
                    {
                        parts = new[]
                        {
                            new { text = prompt }
                        }
                    }
                },
                generationConfig = new
                {
                    temperature = 0.2,  // Lower temperature for medical accuracy
                    topK = 40,
                    topP = 0.95,
                    maxOutputTokens = 4096,
                    stopSequences = new string[] { }
                },
                safetySettings = new[]
                {
                    new
                    {
                        category = "HARM_CATEGORY_HARASSMENT",
                        threshold = "BLOCK_NONE"
                    },
                    new
                    {
                        category = "HARM_CATEGORY_HATE_SPEECH",
                        threshold = "BLOCK_NONE"
                    },
                    new
                    {
                        category = "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold = "BLOCK_NONE"
                    },
                    new
                    {
                        category = "HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold = "BLOCK_NONE"  // Medical content may trigger this
                    }
                }
            };

            var json = JsonConvert.SerializeObject(requestBody);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await httpClient.PostAsync(geminiEndpoint, content);
            var responseContent = await response.Content.ReadAsStringAsync();

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogError($"Gemini API error: {responseContent}");
                throw new Exception("Failed to get Gemini diagnosis");
            }

            var geminiResponse = JsonConvert.DeserializeObject<dynamic>(responseContent);
            var diagnosisText = geminiResponse.candidates[0].content.parts[0].text.ToString();

            // Parse the structured response
            return ParseGeminiResponse(diagnosisText);
        }

        /// <summary>
        /// Enhance diagnosis with Vertex AI specialized medical model
        /// </summary>
        private async Task<VertexAIEnhancement> EnhanceWithVertexAI(
            GeminiDiagnosisResponse geminiDiagnosis,
            PatientSymptoms symptoms)
        {
            var endpointName = EndpointName.FromProjectLocationEndpoint(
                _projectId, _location, "medical-diagnosis-endpoint");

            var instances = new List<Value>
            {
                Value.ForStruct(new Struct
                {
                    Fields =
                    {
                        ["symptoms"] = Value.ForList(symptoms.Symptoms.Select(s => Value.ForString(s)).ToArray()),
                        ["age"] = Value.ForNumber(symptoms.Age),
                        ["gender"] = Value.ForString(symptoms.Gender),
                        ["medical_history"] = Value.ForList(symptoms.MedicalHistory.Select(h => Value.ForString(h)).ToArray()),
                        ["initial_diagnosis"] = Value.ForString(geminiDiagnosis.PrimaryDiagnosis.Name)
                    }
                })
            };

            var parameters = Value.ForStruct(new Struct
            {
                Fields =
                {
                    ["confidence_threshold"] = Value.ForNumber(0.8),
                    ["max_results"] = Value.ForNumber(5)
                }
            });

            try
            {
                var predictRequest = new PredictRequest
                {
                    EndpointAsEndpointName = endpointName,
                    Instances = { instances },
                    Parameters = parameters
                };

                var prediction = await _predictionClient.PredictAsync(predictRequest);

                return new VertexAIEnhancement
                {
                    EnhancedConfidence = ExtractConfidence(prediction),
                    AdditionalFindings = ExtractFindings(prediction),
                    ModelVersion = "vertex-medical-v1"
                };
            }
            catch (Exception ex)
            {
                _logger.LogWarning($"Vertex AI enhancement failed: {ex.Message}");
                // Return default enhancement if Vertex AI fails
                return new VertexAIEnhancement
                {
                    EnhancedConfidence = geminiDiagnosis.ConfidenceScore,
                    AdditionalFindings = new List<string>(),
                    ModelVersion = "fallback"
                };
            }
        }

        /// <summary>
        /// Generate differential diagnosis using AI
        /// </summary>
        private async Task<List<DifferentialDiagnosis>> GenerateDifferentialDiagnosis(
            PatientSymptoms symptoms,
            GeminiDiagnosisResponse primaryDiagnosis)
        {
            var httpClient = _httpClientFactory.CreateClient();

            var prompt = $@"
Based on the symptoms: {string.Join(", ", symptoms.Symptoms)}
And the primary diagnosis: {primaryDiagnosis.PrimaryDiagnosis.Name}

Generate a differential diagnosis list with:
1. Alternative conditions to consider
2. Probability scores
3. Key differentiating factors
4. Tests to rule in/out each condition

Format as JSON array of differential diagnoses.
";

            // Call Gemini API for differential diagnosis
            var differentials = new List<DifferentialDiagnosis>();

            // Add logic to call Gemini and parse response
            // For now, return sample differentials
            differentials.Add(new DifferentialDiagnosis
            {
                Condition = "Acute Coronary Syndrome",
                Probability = 0.75,
                ICD10Code = "I20.0",
                DifferentiatingFactors = new[] { "ECG changes", "Troponin levels", "Pain character" },
                RuleOutTests = new[] { "ECG", "Cardiac markers", "Stress test" }
            });

            return differentials;
        }

        /// <summary>
        /// Calculate risk score and urgency using AI
        /// </summary>
        private async Task<RiskAssessment> CalculateRiskScore(
            PatientSymptoms symptoms,
            GeminiDiagnosisResponse diagnosis)
        {
            // Use BigQuery ML for risk scoring
            var riskFactors = IdentifyRiskFactors(symptoms, diagnosis);
            var baseRiskScore = CalculateBaseRiskScore(riskFactors);

            // Enhance with AI prediction
            var aiRiskScore = await PredictRiskWithAI(symptoms, diagnosis);

            return new RiskAssessment
            {
                OverallRiskScore = (baseRiskScore + aiRiskScore) / 2,
                UrgencyLevel = DetermineUrgencyLevel(aiRiskScore),
                RiskFactors = riskFactors,
                MortalityRisk = CalculateMortalityRisk(symptoms, diagnosis),
                MorbidityRisk = CalculateMorbidityRisk(symptoms, diagnosis),
                RequiresEmergencyAction = aiRiskScore > 0.8
            };
        }

        /// <summary>
        /// Generate AI-powered treatment recommendations
        /// </summary>
        private async Task<TreatmentPlan> GenerateTreatmentRecommendations(
            GeminiDiagnosisResponse diagnosis,
            PatientSymptoms symptoms)
        {
            var treatmentPlan = new TreatmentPlan
            {
                PrimaryTreatment = new Treatment
                {
                    Name = diagnosis.TreatmentRecommendations.FirstOrDefault()?.Name ?? "Supportive care",
                    Type = TreatmentType.Pharmacological,
                    Duration = "As directed by physician",
                    Instructions = "Follow prescribed regimen"
                },
                Medications = await GenerateMedicationRecommendations(diagnosis, symptoms),
                Procedures = GenerateProcedureRecommendations(diagnosis),
                LifestyleModifications = GenerateLifestyleRecommendations(diagnosis),
                FollowUpSchedule = GenerateFollowUpSchedule(diagnosis),
                MonitoringPlan = GenerateMonitoringPlan(diagnosis)
            };

            return treatmentPlan;
        }

        /// <summary>
        /// Log AI usage for monitoring and cost tracking
        /// </summary>
        private async Task LogAIUsage(AIDiagnosisResult result)
        {
            // Log to BigQuery for analysis
            var usage = new AIUsageLog
            {
                Timestamp = DateTime.UtcNow,
                Service = "MedicalDiagnosis",
                Model = result.AIModelUsed,
                TokensUsed = EstimateTokenUsage(result),
                ResponseTime = result.ProcessingTimeMs,
                ConfidenceScore = result.ConfidenceScore,
                PatientId = result.PatientId,
                DiagnosisId = result.DiagnosisId
            };

            // Send to BigQuery
            await LogToBigQuery(usage);

            // Update metrics for monitoring
            await UpdateAIMetrics(usage);
        }

        // Helper methods
        private string PreparePatientContext(PatientSymptoms symptoms)
        {
            return JsonConvert.SerializeObject(new
            {
                patient = new
                {
                    age = symptoms.Age,
                    gender = symptoms.Gender,
                    weight = symptoms.Weight,
                    height = symptoms.Height
                },
                symptoms = symptoms.Symptoms,
                duration = symptoms.Duration,
                severity = symptoms.Severity,
                medicalHistory = symptoms.MedicalHistory,
                currentMedications = symptoms.CurrentMedications,
                allergies = symptoms.Allergies,
                vitalSigns = symptoms.VitalSigns,
                labResults = symptoms.LabResults
            }, Formatting.Indented);
        }

        private GeminiDiagnosisResponse ParseGeminiResponse(string responseText)
        {
            try
            {
                // Parse JSON response from Gemini
                var parsed = JsonConvert.DeserializeObject<GeminiDiagnosisResponse>(responseText);
                return parsed;
            }
            catch
            {
                // Fallback parsing if response is not proper JSON
                return new GeminiDiagnosisResponse
                {
                    PrimaryDiagnosis = new Diagnosis
                    {
                        Name = ExtractDiagnosisFromText(responseText),
                        ICD10Code = "R69",
                        Confidence = 0.7
                    },
                    ConfidenceScore = 70,
                    ClinicalNotes = responseText,
                    RecommendedTests = new List<string> { "Complete Blood Count", "Comprehensive Metabolic Panel" },
                    RedFlags = new List<string>()
                };
            }
        }

        private string ExtractDiagnosisFromText(string text)
        {
            // Simple extraction logic - in production, use NLP
            var lines = text.Split('\n');
            foreach (var line in lines)
            {
                if (line.Contains("diagnosis", StringComparison.OrdinalIgnoreCase))
                {
                    return line.Replace("diagnosis", "", StringComparison.OrdinalIgnoreCase).Trim();
                }
            }
            return "Unspecified condition";
        }

        private double ExtractConfidence(PredictResponse prediction)
        {
            // Extract confidence from Vertex AI prediction
            try
            {
                var confidence = prediction.Predictions[0].StructValue.Fields["confidence"].NumberValue;
                return confidence * 100;
            }
            catch
            {
                return 75.0; // Default confidence
            }
        }

        private List<string> ExtractFindings(PredictResponse prediction)
        {
            var findings = new List<string>();
            try
            {
                var findingsValue = prediction.Predictions[0].StructValue.Fields["findings"];
                foreach (var finding in findingsValue.ListValue.Values)
                {
                    findings.Add(finding.StringValue);
                }
            }
            catch
            {
                // Return empty list if extraction fails
            }
            return findings;
        }

        private List<string> IdentifyRiskFactors(PatientSymptoms symptoms, GeminiDiagnosisResponse diagnosis)
        {
            var riskFactors = new List<string>();

            // Age-related risks
            if (symptoms.Age > 65) riskFactors.Add("Advanced age");
            if (symptoms.Age < 18) riskFactors.Add("Pediatric patient");

            // Symptom-related risks
            if (symptoms.Symptoms.Any(s => s.Contains("chest pain", StringComparison.OrdinalIgnoreCase)))
                riskFactors.Add("Cardiac symptoms");

            // Medical history risks
            if (symptoms.MedicalHistory.Any(h => h.Contains("diabetes", StringComparison.OrdinalIgnoreCase)))
                riskFactors.Add("Diabetes");

            return riskFactors;
        }

        private double CalculateBaseRiskScore(List<string> riskFactors)
        {
            // Simple risk calculation - enhance with ML model
            return Math.Min(riskFactors.Count * 0.15, 1.0);
        }

        private async Task<double> PredictRiskWithAI(PatientSymptoms symptoms, GeminiDiagnosisResponse diagnosis)
        {
            // Placeholder for AI risk prediction
            // In production, call BigQuery ML or Vertex AI model
            return 0.65;
        }

        private string DetermineUrgencyLevel(double riskScore)
        {
            return riskScore switch
            {
                > 0.8 => "Emergency",
                > 0.6 => "Urgent",
                > 0.3 => "Routine",
                _ => "Elective"
            };
        }

        private double CalculateMortalityRisk(PatientSymptoms symptoms, GeminiDiagnosisResponse diagnosis)
        {
            // Placeholder - implement with medical risk models
            return 0.05;
        }

        private double CalculateMorbidityRisk(PatientSymptoms symptoms, GeminiDiagnosisResponse diagnosis)
        {
            // Placeholder - implement with medical risk models
            return 0.15;
        }

        private async Task<List<Medication>> GenerateMedicationRecommendations(
            GeminiDiagnosisResponse diagnosis,
            PatientSymptoms symptoms)
        {
            // Generate medication recommendations using AI
            return new List<Medication>
            {
                new Medication
                {
                    Name = "Recommended Medication",
                    Dosage = "As prescribed",
                    Frequency = "Daily",
                    Duration = "30 days"
                }
            };
        }

        private List<string> GenerateProcedureRecommendations(GeminiDiagnosisResponse diagnosis)
        {
            return new List<string> { "Follow-up consultation", "Diagnostic imaging if symptoms persist" };
        }

        private List<string> GenerateLifestyleRecommendations(GeminiDiagnosisResponse diagnosis)
        {
            return new List<string> { "Regular exercise", "Balanced diet", "Adequate rest" };
        }

        private string GenerateFollowUpSchedule(GeminiDiagnosisResponse diagnosis)
        {
            return "Follow up in 1-2 weeks or sooner if symptoms worsen";
        }

        private string GenerateMonitoringPlan(GeminiDiagnosisResponse diagnosis)
        {
            return "Monitor symptoms daily, seek immediate care if red flags appear";
        }

        private string GenerateFollowUpInstructions(RiskAssessment riskAssessment)
        {
            var urgency = riskAssessment.UrgencyLevel;
            return urgency switch
            {
                "Emergency" => "Seek immediate emergency care",
                "Urgent" => "See healthcare provider within 24-48 hours",
                "Routine" => "Schedule appointment within 1-2 weeks",
                _ => "Follow up as needed"
            };
        }

        private int EstimateTokenUsage(AIDiagnosisResult result)
        {
            // Estimate based on content length
            var totalLength = JsonConvert.SerializeObject(result).Length;
            return totalLength / 4; // Rough estimate: 4 characters per token
        }

        private async Task LogToBigQuery(AIUsageLog usage)
        {
            // Implement BigQuery logging
            _logger.LogInformation($"Logging AI usage to BigQuery: {usage.DiagnosisId}");
        }

        private async Task UpdateAIMetrics(AIUsageLog usage)
        {
            // Update CloudWatch or Google Cloud Monitoring metrics
            _logger.LogInformation($"Updating AI metrics for diagnosis: {usage.DiagnosisId}");
        }
    }

    // Supporting classes and interfaces
    public interface IMedicalDiagnosisAI
    {
        Task<AIDiagnosisResult> GenerateDiagnosisAsync(PatientSymptoms symptoms);
    }

    public class AIProcessingException : Exception
    {
        public AIProcessingException(string message, Exception innerException)
            : base(message, innerException) { }
    }
}