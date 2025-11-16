using Microsoft.ML;
using Microsoft.ML.Data;
using Microsoft.ML.Trainers.FastTree;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Modules.MachineLearning.Services
{
    public class PredictiveHealthService
    {
        private readonly MLContext _mlContext;
        private readonly ILogger<PredictiveHealthService> _logger;
        private ITransformer _readmissionModel;
        private ITransformer _diabetesProgressionModel;

        public PredictiveHealthService(ILogger<PredictiveHealthService> logger)
        {
            _logger = logger;
            _mlContext = new MLContext(seed: 0);

            // Load pre-trained models
            LoadModels();
        }

        private void LoadModels()
        {
            try
            {
                // Load readmission model if exists
                if (File.Exists("Models/readmission_model.zip"))
                {
                    _readmissionModel = _mlContext.Model.Load("Models/readmission_model.zip", out _);
                }
                else
                {
                    // Train a simple model for demo
                    TrainReadmissionModel();
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading ML models");
            }
        }

        /// <summary>
        /// Train readmission prediction model
        /// </summary>
        private void TrainReadmissionModel()
        {
            // Create sample training data
            var sampleData = new List<PatientReadmissionData>
            {
                new PatientReadmissionData { Age = 65, DiabetesScore = 8.5f, PreviousAdmissions = 2, ComorbidityCount = 3, Readmitted = true },
                new PatientReadmissionData { Age = 45, DiabetesScore = 6.5f, PreviousAdmissions = 0, ComorbidityCount = 1, Readmitted = false },
                new PatientReadmissionData { Age = 72, DiabetesScore = 9.2f, PreviousAdmissions = 3, ComorbidityCount = 4, Readmitted = true },
                new PatientReadmissionData { Age = 55, DiabetesScore = 7.0f, PreviousAdmissions = 1, ComorbidityCount = 2, Readmitted = false },
                // Add more training data...
            };

            var trainingData = _mlContext.Data.LoadFromEnumerable(sampleData);

            // Build training pipeline
            var pipeline = _mlContext.Transforms.Concatenate("Features",
                    nameof(PatientReadmissionData.Age),
                    nameof(PatientReadmissionData.DiabetesScore),
                    nameof(PatientReadmissionData.PreviousAdmissions),
                    nameof(PatientReadmissionData.ComorbidityCount))
                .Append(_mlContext.BinaryClassification.Trainers.FastTree(
                    labelColumnName: nameof(PatientReadmissionData.Readmitted),
                    numberOfLeaves: 20,
                    minimumExampleCountPerLeaf: 10,
                    learningRate: 0.2));

            // Train the model
            _readmissionModel = pipeline.Fit(trainingData);

            // Save the model
            Directory.CreateDirectory("Models");
            _mlContext.Model.Save(_readmissionModel, trainingData.Schema, "Models/readmission_model.zip");

            _logger.LogInformation("Readmission model trained and saved");
        }

        /// <summary>
        /// Predict readmission risk for a patient
        /// </summary>
        public async Task<ReadmissionPrediction> PredictReadmissionRisk(string patientId)
        {
            // Get patient features from FHIR data
            var patientFeatures = await BuildPatientFeatures(patientId);

            // Create prediction engine
            var predictionEngine = _mlContext.Model.CreatePredictionEngine<PatientReadmissionData, ReadmissionPredictionResult>(_readmissionModel);

            // Make prediction
            var prediction = predictionEngine.Predict(patientFeatures);

            return new ReadmissionPrediction
            {
                PatientId = patientId,
                RiskScore = prediction.Probability,
                RiskLevel = DetermineRiskLevel(prediction.Probability),
                Confidence = prediction.Score,
                PredictedReadmission = prediction.PredictedLabel,
                Factors = IdentifyRiskFactors(patientFeatures),
                Recommendations = GenerateRecommendations(prediction.Probability)
            };
        }

        private async Task<PatientReadmissionData> BuildPatientFeatures(string patientId)
        {
            // In real implementation, fetch from FHIR server
            // This is mock data for demo
            return new PatientReadmissionData
            {
                Age = 60,
                DiabetesScore = 7.8f,
                PreviousAdmissions = 2,
                ComorbidityCount = 3
            };
        }

        private string DetermineRiskLevel(float probability)
        {
            if (probability < 0.3) return "Low";
            if (probability < 0.6) return "Medium";
            if (probability < 0.8) return "High";
            return "Critical";
        }

        private List<string> IdentifyRiskFactors(PatientReadmissionData features)
        {
            var factors = new List<string>();

            if (features.Age > 65)
                factors.Add("Advanced age (>65)");
            if (features.DiabetesScore > 7)
                factors.Add($"Poor diabetes control (HbA1c: {features.DiabetesScore})");
            if (features.PreviousAdmissions > 1)
                factors.Add($"Multiple previous admissions ({features.PreviousAdmissions})");
            if (features.ComorbidityCount > 2)
                factors.Add($"Multiple comorbidities ({features.ComorbidityCount})");

            return factors;
        }

        private List<string> GenerateRecommendations(float riskScore)
        {
            var recommendations = new List<string>();

            if (riskScore > 0.7)
            {
                recommendations.Add("Schedule follow-up within 48 hours of discharge");
                recommendations.Add("Initiate intensive care management program");
                recommendations.Add("Consider home health services");
                recommendations.Add("Review and optimize medication regimen");
            }
            else if (riskScore > 0.4)
            {
                recommendations.Add("Schedule follow-up within 7 days");
                recommendations.Add("Provide detailed discharge instructions");
                recommendations.Add("Ensure medication reconciliation");
            }
            else
            {
                recommendations.Add("Standard follow-up care");
                recommendations.Add("Patient education on warning signs");
            }

            return recommendations;
        }
    }

    // ML Data Models
    public class PatientReadmissionData
    {
        public float Age { get; set; }
        public float DiabetesScore { get; set; }
        public float PreviousAdmissions { get; set; }
        public float ComorbidityCount { get; set; }

        [ColumnName("Label")]
        public bool Readmitted { get; set; }
    }

    public class ReadmissionPredictionResult
    {
        [ColumnName("PredictedLabel")]
        public bool PredictedLabel { get; set; }

        [ColumnName("Probability")]
        public float Probability { get; set; }

        [ColumnName("Score")]
        public float Score { get; set; }
    }

    public class ReadmissionPrediction
    {
        public string PatientId { get; set; }
        public float RiskScore { get; set; }
        public string RiskLevel { get; set; }
        public float Confidence { get; set; }
        public bool PredictedReadmission { get; set; }
        public List<string> Factors { get; set; }
        public List<string> Recommendations { get; set; }
    }
}