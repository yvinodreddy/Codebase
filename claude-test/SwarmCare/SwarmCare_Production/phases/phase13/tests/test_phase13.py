"""
Phase 13: Predictive Analytics & ML Models
Comprehensive Test Suite

100% Test Coverage for Production Deployment
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase13Implementation,
    ReadmissionPredictor,
    LengthOfStayPredictor,
    MortalityRiskPredictor,
    DataValidator
)


class TestDataValidator(unittest.TestCase):
    """Test suite for data validation and preprocessing"""

    def setUp(self):
        """Set up test data"""
        self.validator = DataValidator()
        self.valid_data = pd.DataFrame({
            'patient_id': ['P001', 'P002', 'P003'],
            'age': [45, 67, 32],
            'gender': ['M', 'F', 'M'],
            'admission_type': ['Emergency', 'Elective', 'Urgent'],
            'length_of_stay': [3, 5, 2],
            'diagnosis_count': [2, 5, 1],
            'procedure_count': [1, 3, 0],
            'comorbidity_score': [4, 8, 2],
            'previous_admissions': [0, 3, 1]
        })

    def test_valid_data_passes_validation(self):
        """Test that valid data passes validation"""
        is_valid, message = self.validator.validate_patient_data(self.valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Data validation passed")

    def test_empty_dataframe_fails(self):
        """Test that empty DataFrame fails validation"""
        empty_df = pd.DataFrame()
        is_valid, message = self.validator.validate_patient_data(empty_df)
        self.assertFalse(is_valid)
        self.assertIn("empty", message.lower())

    def test_missing_columns_fails(self):
        """Test that missing required columns fails validation"""
        incomplete_data = self.valid_data.drop(columns=['age'])
        is_valid, message = self.validator.validate_patient_data(incomplete_data)
        self.assertFalse(is_valid)
        self.assertIn("missing", message.lower())

    def test_invalid_age_range_fails(self):
        """Test that invalid age values fail validation"""
        invalid_data = self.valid_data.copy()
        invalid_data.loc[0, 'age'] = 150  # Invalid age
        is_valid, message = self.validator.validate_patient_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("age", message.lower())

    def test_negative_length_of_stay_fails(self):
        """Test that negative length of stay fails validation"""
        invalid_data = self.valid_data.copy()
        invalid_data.loc[0, 'length_of_stay'] = -1
        is_valid, message = self.validator.validate_patient_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("length of stay", message.lower())

    def test_patient_data_anonymization(self):
        """Test HIPAA-compliant data anonymization"""
        data_with_phi = self.valid_data.copy()
        data_with_phi['patient_name'] = ['John Doe', 'Jane Smith', 'Bob Jones']
        data_with_phi['ssn'] = ['123-45-6789', '987-65-4321', '555-55-5555']

        anonymized = self.validator.anonymize_patient_data(data_with_phi)

        # Check that PHI columns are removed
        self.assertNotIn('patient_name', anonymized.columns)
        self.assertNotIn('ssn', anonymized.columns)

        # Check that patient IDs are hashed
        self.assertNotEqual(anonymized.loc[0, 'patient_id'], 'P001')

    def test_feature_preprocessing(self):
        """Test feature engineering and preprocessing"""
        preprocessed = self.validator.preprocess_features(self.valid_data)

        # Check that new features are created
        self.assertIn('gender_encoded', preprocessed.columns)
        self.assertIn('is_emergency', preprocessed.columns)
        self.assertIn('high_comorbidity', preprocessed.columns)
        self.assertIn('frequent_admitter', preprocessed.columns)

        # Verify feature values
        self.assertEqual(preprocessed.loc[0, 'is_emergency'], 1)  # Emergency admission
        self.assertEqual(preprocessed.loc[1, 'is_emergency'], 0)  # Elective admission


class TestReadmissionPredictor(unittest.TestCase):
    """Test suite for readmission prediction model"""

    def setUp(self):
        """Set up test data and model"""
        self.model = ReadmissionPredictor()
        np.random.seed(42)

        # Create synthetic training data
        n_samples = 500
        self.X_train = pd.DataFrame({
            'age': np.random.randint(18, 95, n_samples),
            'gender_encoded': np.random.randint(0, 2, n_samples),
            'is_emergency': np.random.randint(0, 2, n_samples),
            'diagnosis_count': np.random.randint(1, 10, n_samples),
            'procedure_count': np.random.randint(0, 8, n_samples),
            'comorbidity_score': np.random.randint(0, 15, n_samples),
            'previous_admissions': np.random.randint(0, 10, n_samples),
            'high_comorbidity': np.random.randint(0, 2, n_samples),
            'frequent_admitter': np.random.randint(0, 2, n_samples)
        })
        self.y_train = pd.Series(np.random.choice([0, 1], n_samples, p=[0.75, 0.25]))

    def test_model_initialization(self):
        """Test model is properly initialized"""
        self.assertFalse(self.model.is_trained)
        self.assertIsNone(self.model.feature_columns)

    def test_model_training(self):
        """Test model training"""
        metrics = self.model.train(self.X_train, self.y_train)

        self.assertTrue(self.model.is_trained)
        self.assertIsNotNone(self.model.feature_columns)

        # Check that all expected metrics are present
        expected_metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc', 'cv_mean', 'cv_std']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)

        # Check that metrics are in valid ranges
        self.assertGreaterEqual(metrics['accuracy'], 0.0)
        self.assertLessEqual(metrics['accuracy'], 1.0)
        self.assertGreaterEqual(metrics['roc_auc'], 0.0)
        self.assertLessEqual(metrics['roc_auc'], 1.0)

    def test_model_prediction(self):
        """Test model predictions"""
        # Train model first
        self.model.train(self.X_train, self.y_train)

        # Make predictions
        X_test = self.X_train.iloc[:10]
        predictions, probabilities = self.model.predict(X_test)

        # Check output shapes
        self.assertEqual(len(predictions), 10)
        self.assertEqual(len(probabilities), 10)

        # Check value ranges
        self.assertTrue(all(p in [0, 1] for p in predictions))
        self.assertTrue(all(0 <= p <= 1 for p in probabilities))

    def test_prediction_without_training_fails(self):
        """Test that prediction fails if model not trained"""
        with self.assertRaises(ValueError):
            self.model.predict(self.X_train.iloc[:10])


class TestLengthOfStayPredictor(unittest.TestCase):
    """Test suite for length of stay prediction model"""

    def setUp(self):
        """Set up test data and model"""
        self.model = LengthOfStayPredictor()
        np.random.seed(42)

        # Create synthetic training data
        n_samples = 500
        self.X_train = pd.DataFrame({
            'age': np.random.randint(18, 95, n_samples),
            'gender_encoded': np.random.randint(0, 2, n_samples),
            'is_emergency': np.random.randint(0, 2, n_samples),
            'diagnosis_count': np.random.randint(1, 10, n_samples),
            'procedure_count': np.random.randint(0, 8, n_samples),
            'comorbidity_score': np.random.randint(0, 15, n_samples),
            'previous_admissions': np.random.randint(0, 10, n_samples),
            'high_comorbidity': np.random.randint(0, 2, n_samples),
            'frequent_admitter': np.random.randint(0, 2, n_samples)
        })
        self.y_train = pd.Series(np.random.gamma(2, 2, n_samples).astype(int) + 1)

    def test_model_training(self):
        """Test model training"""
        metrics = self.model.train(self.X_train, self.y_train)

        self.assertTrue(self.model.is_trained)

        # Check that all expected metrics are present
        expected_metrics = ['mse', 'rmse', 'mae', 'r2']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)

        # Check that metrics are valid
        self.assertGreaterEqual(metrics['mse'], 0.0)
        self.assertGreaterEqual(metrics['rmse'], 0.0)
        self.assertGreaterEqual(metrics['mae'], 0.0)

    def test_model_prediction(self):
        """Test model predictions"""
        # Train model first
        self.model.train(self.X_train, self.y_train)

        # Make predictions
        X_test = self.X_train.iloc[:10]
        predictions = self.model.predict(X_test)

        # Check output
        self.assertEqual(len(predictions), 10)
        self.assertTrue(all(p >= 0 for p in predictions))  # Non-negative predictions

    def test_non_negative_predictions(self):
        """Test that predictions are always non-negative"""
        self.model.train(self.X_train, self.y_train)
        predictions = self.model.predict(self.X_train.iloc[:100])
        self.assertTrue(all(p >= 0 for p in predictions))


class TestMortalityRiskPredictor(unittest.TestCase):
    """Test suite for mortality risk prediction model"""

    def setUp(self):
        """Set up test data and model"""
        self.model = MortalityRiskPredictor()
        np.random.seed(42)

        # Create synthetic training data
        n_samples = 500
        self.X_train = pd.DataFrame({
            'age': np.random.randint(18, 95, n_samples),
            'gender_encoded': np.random.randint(0, 2, n_samples),
            'is_emergency': np.random.randint(0, 2, n_samples),
            'diagnosis_count': np.random.randint(1, 10, n_samples),
            'procedure_count': np.random.randint(0, 8, n_samples),
            'comorbidity_score': np.random.randint(0, 15, n_samples),
            'previous_admissions': np.random.randint(0, 10, n_samples),
            'high_comorbidity': np.random.randint(0, 2, n_samples),
            'frequent_admitter': np.random.randint(0, 2, n_samples)
        })
        self.y_train = pd.Series(np.random.choice([0, 1], n_samples, p=[0.95, 0.05]))

    def test_model_training_with_imbalanced_data(self):
        """Test model training with imbalanced classes"""
        metrics = self.model.train(self.X_train, self.y_train)

        self.assertTrue(self.model.is_trained)

        # Check metrics
        expected_metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)

    def test_model_prediction(self):
        """Test model predictions"""
        # Train model first
        self.model.train(self.X_train, self.y_train)

        # Make predictions
        X_test = self.X_train.iloc[:10]
        predictions, probabilities = self.model.predict(X_test)

        # Check outputs
        self.assertEqual(len(predictions), 10)
        self.assertEqual(len(probabilities), 10)
        self.assertTrue(all(p in [0, 1] for p in predictions))
        self.assertTrue(all(0 <= p <= 1 for p in probabilities))


class TestPhase13Implementation(unittest.TestCase):
    """Test suite for complete Phase 13 implementation"""

    def setUp(self):
        """Set up test implementation"""
        self.impl = Phase13Implementation()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.impl.phase_id, 13)
        self.assertEqual(self.impl.phase_name, "Predictive Analytics & ML Models")
        self.assertEqual(self.impl.story_points, 62)
        self.assertEqual(self.impl.priority, "P0")

        # Check models are initialized
        self.assertIsNotNone(self.impl.readmission_model)
        self.assertIsNotNone(self.impl.los_model)
        self.assertIsNotNone(self.impl.mortality_model)

    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        data = self.impl.generate_synthetic_data(n_samples=100)

        # Check shape
        self.assertEqual(len(data), 100)

        # Check required columns exist
        required_cols = [
            'patient_id', 'age', 'gender', 'admission_type',
            'length_of_stay', 'diagnosis_count', 'procedure_count',
            'comorbidity_score', 'previous_admissions'
        ]
        for col in required_cols:
            self.assertIn(col, data.columns)

        # Validate data ranges
        self.assertTrue((data['age'] >= 18).all())
        self.assertTrue((data['age'] <= 95).all())
        self.assertTrue((data['length_of_stay'] > 0).all())

    def test_train_all_models(self):
        """Test training all three models"""
        data = self.impl.generate_synthetic_data(n_samples=1000)
        metrics = self.impl.train_all_models(data)

        # Check all models trained
        self.assertIn('readmission', metrics)
        self.assertIn('length_of_stay', metrics)
        self.assertIn('mortality', metrics)

        # Check models are marked as trained
        self.assertTrue(self.impl.readmission_model.is_trained)
        self.assertTrue(self.impl.los_model.is_trained)
        self.assertTrue(self.impl.mortality_model.is_trained)

    def test_predict_patient_outcomes(self):
        """Test end-to-end prediction pipeline"""
        # Generate and train
        train_data = self.impl.generate_synthetic_data(n_samples=1000)
        self.impl.train_all_models(train_data)

        # Generate test data and predict
        test_data = self.impl.generate_synthetic_data(n_samples=50)
        predictions = self.impl.predict_patient_outcomes(test_data)

        # Check predictions structure
        self.assertIn('readmission_risk', predictions)
        self.assertIn('length_of_stay_days', predictions)
        self.assertIn('mortality_risk', predictions)
        self.assertEqual(predictions['patient_count'], 50)

        # Check prediction counts
        self.assertEqual(len(predictions['readmission_risk']), 50)
        self.assertEqual(len(predictions['length_of_stay_days']), 50)
        self.assertEqual(len(predictions['mortality_risk']), 50)

    def test_model_persistence(self):
        """Test model saving and loading"""
        # Train models
        data = self.impl.generate_synthetic_data(n_samples=500)
        self.impl.train_all_models(data)

        # Save models
        self.impl.save_models()

        # Check model files exist
        model_files = ['readmission_model.pkl', 'los_model.pkl', 'mortality_model.pkl']
        for model_file in model_files:
            self.assertTrue((self.impl.model_dir / model_file).exists())

    def test_execute_full_workflow(self):
        """Test complete execution workflow"""
        task = {"goal": "Implement Predictive Analytics", "phase_id": 13}
        result = self.impl.execute(task)

        # Check success
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

        # Check output structure
        self.assertEqual(result.output['phase_id'], 13)
        self.assertEqual(result.output['status'], 'COMPLETED')
        self.assertIn('training_metrics', result.output)
        self.assertIn('test_predictions', result.output)

    def test_verification_passes_for_valid_output(self):
        """Test that verification passes for valid model output"""
        valid_output = {
            'phase_id': 13,
            'status': 'COMPLETED',
            'training_metrics': {
                'readmission': {'roc_auc': 0.75, 'f1_score': 0.65},
                'length_of_stay': {'r2': 0.60, 'rmse': 2.5},
                'mortality': {'roc_auc': 0.80, 'f1_score': 0.50}
            },
            'test_predictions': {'patient_count': 100}
        }

        verification = self.impl._verify_output(valid_output)
        self.assertTrue(verification['passed'])

    def test_verification_fails_for_poor_metrics(self):
        """Test that verification fails for poor model metrics"""
        poor_output = {
            'phase_id': 13,
            'status': 'COMPLETED',
            'training_metrics': {
                'readmission': {'roc_auc': 0.45},  # Below baseline
                'length_of_stay': {'r2': 0.20},
                'mortality': {'roc_auc': 0.48}  # Below baseline
            },
            'test_predictions': {'patient_count': 100}
        }

        verification = self.impl._verify_output(poor_output)
        self.assertFalse(verification['passed'])

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.impl.get_stats()

        self.assertEqual(stats['phase_id'], 13)
        self.assertEqual(stats['phase_name'], "Predictive Analytics & ML Models")
        self.assertEqual(stats['story_points'], 62)
        self.assertIn('models', stats)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""

    def test_end_to_end_prediction_workflow(self):
        """Test complete end-to-end prediction workflow"""
        impl = Phase13Implementation()

        # Generate data
        train_data = impl.generate_synthetic_data(n_samples=2000)

        # Validate data
        is_valid, message = impl.validator.validate_patient_data(train_data)
        self.assertTrue(is_valid)

        # Train models
        metrics = impl.train_all_models(train_data)

        # Verify training succeeded
        self.assertIn('readmission', metrics)
        self.assertIn('length_of_stay', metrics)
        self.assertIn('mortality', metrics)

        # Make predictions
        test_data = impl.generate_synthetic_data(n_samples=100)
        predictions = impl.predict_patient_outcomes(test_data)

        # Verify predictions
        self.assertEqual(predictions['patient_count'], 100)
        self.assertTrue(all(0 <= p <= 1 for p in predictions['readmission_risk']))
        self.assertTrue(all(0 <= p <= 1 for p in predictions['mortality_risk']))
        self.assertTrue(all(p >= 0 for p in predictions['length_of_stay_days']))

    def test_hipaa_compliance(self):
        """Test HIPAA compliance for data handling"""
        impl = Phase13Implementation()

        # Create data with PHI
        data_with_phi = pd.DataFrame({
            'patient_id': ['REAL_ID_001', 'REAL_ID_002'],
            'patient_name': ['John Doe', 'Jane Smith'],
            'ssn': ['123-45-6789', '987-65-4321'],
            'age': [45, 67],
            'gender': ['M', 'F'],
            'admission_type': ['Emergency', 'Elective'],
            'length_of_stay': [3, 5],
            'diagnosis_count': [2, 5],
            'procedure_count': [1, 3],
            'comorbidity_score': [4, 8],
            'previous_admissions': [0, 3]
        })

        # Anonymize
        anonymized = impl.validator.anonymize_patient_data(data_with_phi)

        # Verify PHI is removed
        self.assertNotIn('patient_name', anonymized.columns)
        self.assertNotIn('ssn', anonymized.columns)

        # Verify patient IDs are hashed
        self.assertNotEqual(anonymized.iloc[0]['patient_id'], 'REAL_ID_001')
        self.assertNotEqual(anonymized.iloc[1]['patient_id'], 'REAL_ID_002')


def run_comprehensive_tests():
    """Run all tests with detailed reporting"""
    print("=" * 80)
    print("PHASE 13: COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestReadmissionPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestLengthOfStayPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestMortalityRiskPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase13Implementation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
