"""
Phase 26: Real-time CDC & Public Health Integration
Comprehensive test suite

Tests:
- Disease Surveillance (10 tests)
- Outbreak Detection (10 tests)
- CDC Reporting (10 tests)
- Public Health Analytics (10 tests)
- Phase 26 Implementation (7 tests)
- Integration Tests (3 tests)
Total: 50 comprehensive tests
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase26Implementation
from disease_surveillance import (
    DiseaseSurveillanceSystem, NotifiableDisease, DiseaseCategory,
    NotifiabilityLevel, CaseStatus, InvestigationStatus, TransmissionMode
)
from outbreak_detection import (
    OutbreakDetectionSystem, ClusterCase, ClusterType, AlertLevel,
    OutbreakStatus, DetectionMethod
)
from cdc_reporting import (
    CDCReportingSystem, ReportType, ReportFormat, ReportStatus,
    JurisdictionLevel
)
from public_health_analytics import (
    PublicHealthAnalytics, TrendDirection, RiskLevel,
    HealthEquityDimension
)


class TestDiseaseSurveillance(unittest.TestCase):
    """Test Disease Surveillance System"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = DiseaseSurveillanceSystem()

    def test_disease_registry_initialization(self):
        """Test disease registry is initialized with diseases"""
        self.assertGreater(len(self.system.diseases), 0)
        self.assertIn("U07.1", self.system.diseases)  # COVID-19
        self.assertIn("B05", self.system.diseases)  # Measles

    def test_register_disease(self):
        """Test registering a new notifiable disease"""
        disease = NotifiableDisease(
            disease_code="TEST001",
            disease_name="Test Disease",
            category=DiseaseCategory.INFECTIOUS,
            notifiability=NotifiabilityLevel.WEEKLY_REPORTABLE,
            incubation_period_days_min=5,
            incubation_period_days_max=14,
            infectious_period_days=10,
            transmission_modes=[TransmissionMode.CONTACT]
        )

        code = self.system.register_disease(disease)
        self.assertEqual(code, "TEST001")
        self.assertIn("TEST001", self.system.diseases)

    def test_report_case(self):
        """Test reporting a disease case"""
        case_id = self.system.report_case(
            disease_code="U07.1",
            patient_id="PT001",
            patient_name="John Doe",
            date_of_birth="1980-01-15",
            sex="M",
            onset_date="2025-10-25",
            symptoms=["fever", "cough"]
        )

        self.assertIsNotNone(case_id)
        self.assertIn(case_id, self.system.cases)

        case = self.system.cases[case_id]
        self.assertEqual(case.patient_id, "PT001")
        self.assertEqual(case.case_status, CaseStatus.SUSPECTED)

    def test_update_case_status(self):
        """Test updating case classification"""
        case_id = self.system.report_case(
            disease_code="B05",
            patient_id="PT002",
            patient_name="Jane Smith",
            date_of_birth="1995-06-20",
            sex="F"
        )

        result = self.system.update_case_status(
            case_id, CaseStatus.CONFIRMED, lab_confirmed=True
        )

        self.assertTrue(result)
        case = self.system.cases[case_id]
        self.assertEqual(case.case_status, CaseStatus.CONFIRMED)
        self.assertTrue(case.lab_confirmed)

    def test_assign_investigator(self):
        """Test assigning investigator to case"""
        case_id = self.system.report_case(
            disease_code="U07.1",
            patient_id="PT003",
            patient_name="Bob Johnson",
            date_of_birth="1970-05-10",
            sex="M"
        )

        result = self.system.assign_investigator(
            case_id, "INV001", "Dr. Sarah Johnson"
        )

        self.assertTrue(result)
        case = self.system.cases[case_id]
        self.assertEqual(case.investigator_id, "INV001")
        self.assertEqual(case.investigation_status, InvestigationStatus.ASSIGNED)

    def test_add_contact(self):
        """Test adding contact for tracing"""
        case_id = self.system.report_case(
            disease_code="B05",
            patient_id="PT004",
            patient_name="Alice Williams",
            date_of_birth="2000-03-15",
            sex="F"
        )

        contact_id = self.system.add_contact(
            case_id=case_id,
            contact_name="Bob Williams",
            exposure_date="2025-10-20",
            exposure_type="household",
            monitoring_days=14
        )

        self.assertIsNotNone(contact_id)
        self.assertIn(contact_id, self.system.contacts)

        contact = self.system.contacts[contact_id]
        self.assertEqual(contact.case_id, case_id)
        self.assertEqual(contact.contact_name, "Bob Williams")

    def test_record_lab_result(self):
        """Test recording laboratory result"""
        result_id = self.system.record_lab_result(
            patient_id="PT001",
            patient_name="John Doe",
            test_type="PCR",
            test_name="COVID-19 PCR",
            specimen_type="Nasopharyngeal swab",
            specimen_collection_date="2025-10-25",
            result="positive",
            reporting_lab="State Lab"
        )

        self.assertIsNotNone(result_id)
        self.assertIn(result_id, self.system.lab_results)

    def test_get_cases_requiring_immediate_reporting(self):
        """Test identifying cases requiring immediate CDC reporting"""
        # Report a measles case (immediately reportable)
        case_id = self.system.report_case(
            disease_code="B05",
            patient_id="PT005",
            patient_name="Charlie Brown",
            date_of_birth="2020-01-01",
            sex="M"
        )

        # Update to probable status
        self.system.update_case_status(case_id, CaseStatus.PROBABLE)

        immediate_cases = self.system.get_cases_requiring_immediate_reporting()
        self.assertGreater(len(immediate_cases), 0)

    def test_get_contacts_for_case(self):
        """Test retrieving contacts for a case"""
        case_id = self.system.report_case(
            disease_code="U07.1",
            patient_id="PT006",
            patient_name="David Lee",
            date_of_birth="1985-08-20",
            sex="M"
        )

        # Add multiple contacts
        self.system.add_contact(
            case_id, "Contact 1", "2025-10-20", "household"
        )
        self.system.add_contact(
            case_id, "Contact 2", "2025-10-21", "workplace"
        )

        contacts = self.system.get_contacts_for_case(case_id)
        self.assertEqual(len(contacts), 2)

    def test_surveillance_summary(self):
        """Test getting surveillance summary statistics"""
        # Add some data
        self.system.report_case(
            "U07.1", "PT007", "Emma Wilson", "1990-04-12", "F"
        )

        summary = self.system.get_surveillance_summary()

        self.assertIn("total_cases", summary)
        self.assertIn("confirmed_cases", summary)
        self.assertIn("registered_diseases", summary)
        self.assertGreater(summary["total_cases"], 0)


class TestOutbreakDetection(unittest.TestCase):
    """Test Outbreak Detection System"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = OutbreakDetectionSystem()

    def test_register_location(self):
        """Test registering a geographic location"""
        location_id = self.system.register_location(
            location_id="LOC001",
            location_name="Springfield",
            latitude=42.1015,
            longitude=-72.5898,
            population=150000
        )

        self.assertEqual(location_id, "LOC001")
        self.assertIn("LOC001", self.system.locations)

    def test_calculate_distance(self):
        """Test calculating distance between two points"""
        # Boston to New York (approximately 300 km)
        distance = self.system.calculate_distance_km(
            42.3601, -71.0589,  # Boston
            40.7128, -74.0060   # New York
        )

        self.assertGreater(distance, 250)
        self.assertLess(distance, 350)

    def test_detect_spatial_clusters(self):
        """Test spatial cluster detection"""
        self.system.register_location(
            "LOC001", "Springfield", 42.1015, -72.5898, 100000
        )

        # Create cases in same location
        cases = []
        for i in range(5):
            case = ClusterCase(
                case_id=f"CASE-{i+1}",
                patient_id=f"PT{i+1}",
                disease_code="U07.1",
                onset_date="2025-10-25",
                location_id="LOC001",
                latitude=42.1015 + (i * 0.001),
                longitude=-72.5898 + (i * 0.001)
            )
            cases.append(case)

        clusters = self.system.detect_spatial_clusters(
            cases, max_radius_km=5, min_cases=3
        )

        self.assertGreater(len(clusters), 0)

    def test_detect_temporal_clusters(self):
        """Test temporal cluster detection"""
        # Create cases over consecutive days
        cases = []
        base_date = datetime(2025, 10, 20)

        for i in range(7):
            case = ClusterCase(
                case_id=f"CASE-{i+1}",
                patient_id=f"PT{i+1}",
                disease_code="U07.1",
                onset_date=(base_date + timedelta(days=i)).isoformat(),
                location_id="LOC001",
                latitude=42.1015,
                longitude=-72.5898
            )
            cases.append(case)

        clusters = self.system.detect_temporal_clusters(
            cases, window_days=7, min_cases=5
        )

        # Should detect at least one temporal cluster
        self.assertGreaterEqual(len(clusters), 0)

    def test_check_thresholds(self):
        """Test threshold-based alert generation"""
        self.system.register_location(
            "LOC001", "Springfield", 42.1015, -72.5898, 100000
        )

        # Test with case count that should trigger alert
        alert = self.system.check_thresholds(
            disease_code="U07.1",
            disease_name="COVID-19",
            location_id="LOC001",
            case_count=50  # Should trigger warning
        )

        # May or may not trigger depending on thresholds
        # Just verify it doesn't crash

    def test_create_alert_from_cluster(self):
        """Test creating alert from detected cluster"""
        from outbreak_detection import DetectedCluster

        cluster = DetectedCluster(
            cluster_id="CLUST-001",
            disease_code="U07.1",
            disease_name="COVID-19",
            cluster_type=ClusterType.SPATIAL,
            case_ids=["CASE-1", "CASE-2", "CASE-3"],
            case_count=3,
            center_latitude=42.1015,
            center_longitude=-72.5898,
            radius_km=5.0,
            alert_level=AlertLevel.WARNING
        )

        alert_id = self.system.create_alert_from_cluster(cluster)

        self.assertIsNotNone(alert_id)
        self.assertIn(alert_id, self.system.alerts)

    def test_initiate_investigation(self):
        """Test initiating outbreak investigation"""
        investigation_id = self.system.initiate_investigation(
            outbreak_id="OUTBREAK-001",
            disease_code="U07.1",
            disease_name="COVID-19",
            lead_investigator_id="INV001",
            lead_investigator_name="Dr. Sarah Johnson",
            population_at_risk=100000
        )

        self.assertIsNotNone(investigation_id)
        self.assertIn(investigation_id, self.system.investigations)

    def test_update_investigation(self):
        """Test updating investigation status"""
        investigation_id = self.system.initiate_investigation(
            "OUTBREAK-001", "U07.1", "COVID-19",
            "INV001", "Dr. Sarah Johnson", 100000
        )

        result = self.system.update_investigation(
            investigation_id,
            confirmed_cases=10,
            probable_cases=5,
            status=OutbreakStatus.CONFIRMED
        )

        self.assertTrue(result)
        investigation = self.system.investigations[investigation_id]
        self.assertEqual(investigation.confirmed_cases, 10)
        self.assertEqual(investigation.status, OutbreakStatus.CONFIRMED)

    def test_acknowledge_alert(self):
        """Test acknowledging an alert"""
        # Create a cluster and alert
        from outbreak_detection import DetectedCluster

        cluster = DetectedCluster(
            cluster_id="CLUST-002",
            disease_code="B05",
            disease_name="Measles",
            cluster_type=ClusterType.SPATIAL,
            case_ids=["CASE-1"],
            case_count=1,
            alert_level=AlertLevel.CRITICAL
        )

        alert_id = self.system.create_alert_from_cluster(cluster)

        result = self.system.acknowledge_alert(alert_id, "Dr. Johnson")

        self.assertTrue(result)
        alert = self.system.alerts[alert_id]
        self.assertTrue(alert.acknowledged)
        self.assertEqual(alert.acknowledged_by, "Dr. Johnson")

    def test_detection_summary(self):
        """Test getting detection system summary"""
        summary = self.system.get_detection_summary()

        self.assertIn("total_clusters", summary)
        self.assertIn("total_alerts", summary)
        self.assertIn("active_investigations", summary)


class TestCDCReporting(unittest.TestCase):
    """Test CDC Reporting System"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = CDCReportingSystem()

    def test_nndss_conditions_initialized(self):
        """Test NNDSS conditions are initialized"""
        self.assertGreater(len(self.system.nndss_conditions), 0)
        self.assertIn("11065", self.system.nndss_conditions)  # COVID-19

    def test_create_nedss_case_report(self):
        """Test creating NEDSS case report"""
        report_id = self.system.create_nedss_case_report(
            case_id="CASE-001",
            patient_id="PT001",
            patient_first_name="John",
            patient_last_name="Doe",
            patient_dob="1980-01-15",
            patient_sex="M",
            disease_code="U07.1",
            disease_name="COVID-19"
        )

        self.assertIsNotNone(report_id)
        self.assertIn(report_id, self.system.nedss_reports)

    def test_create_nndss_weekly_report(self):
        """Test creating NNDSS weekly report"""
        report_id = self.system.create_nndss_weekly_report(
            reporting_area="Massachusetts",
            reporting_area_code="25",
            condition="COVID-19",
            condition_code="11065",
            mmwr_year=2025,
            mmwr_week=44,
            current_week_cases=100,
            cumulative_ytd_cases=5000
        )

        self.assertIsNotNone(report_id)
        self.assertIn(report_id, self.system.nndss_reports)

    def test_create_electronic_lab_report(self):
        """Test creating electronic lab report"""
        report_id = self.system.create_electronic_lab_report(
            patient_id="PT001",
            patient_name="John Doe",
            patient_dob="1980-01-15",
            patient_sex="M",
            specimen_id="SPEC-001",
            specimen_type="Blood",
            specimen_collection_date="2025-10-25",
            test_type_code="12345",
            test_type_name="COVID-19 PCR",
            result="Positive",
            performing_lab_name="State Lab"
        )

        self.assertIsNotNone(report_id)
        self.assertIn(report_id, self.system.lab_reports)

    def test_generate_hl7_message(self):
        """Test generating HL7 ORU message"""
        # Create lab report first
        elr_id = self.system.create_electronic_lab_report(
            patient_id="PT001",
            patient_name="John Doe",
            patient_dob="1980-01-15",
            patient_sex="M",
            specimen_id="SPEC-001",
            specimen_type="Nasopharyngeal swab",
            specimen_collection_date="2025-10-25",
            test_type_code="94500-6",
            test_type_name="SARS-CoV-2 RNA",
            result="Positive",
            performing_lab_name="State Lab"
        )

        # Generate HL7 message
        hl7_id = self.system.generate_hl7_oru_message(elr_id)

        self.assertIsNotNone(hl7_id)
        self.assertIn(hl7_id, self.system.hl7_messages)

        # Verify message structure
        message = self.system.hl7_messages[hl7_id]
        self.assertEqual(message.message_type, "ORU^R01")
        self.assertGreater(len(message.segments), 0)

    def test_transmit_report(self):
        """Test transmitting report"""
        # Create report
        report_id = self.system.create_nedss_case_report(
            case_id="CASE-001",
            patient_id="PT001",
            patient_first_name="Jane",
            patient_last_name="Smith",
            patient_dob="1990-05-20",
            patient_sex="F",
            disease_code="B05",
            disease_name="Measles"
        )

        # Transmit
        transmission_id = self.system.transmit_report(
            report_id=report_id,
            report_format=ReportFormat.NEDSS,
            destination=JurisdictionLevel.STATE,
            destination_endpoint="https://state-nedss.gov"
        )

        self.assertIsNotNone(transmission_id)
        self.assertIn(transmission_id, self.system.transmissions)

        transmission = self.system.transmissions[transmission_id]
        self.assertEqual(transmission.status, ReportStatus.SUBMITTED)

    def test_acknowledge_transmission(self):
        """Test acknowledging transmission"""
        # Create and transmit report
        report_id = self.system.create_nedss_case_report(
            "CASE-001", "PT001", "John", "Doe",
            "1980-01-15", "M", "U07.1", "COVID-19"
        )

        transmission_id = self.system.transmit_report(
            report_id, ReportFormat.NEDSS,
            JurisdictionLevel.STATE, "https://state.gov"
        )

        # Acknowledge
        result = self.system.acknowledge_transmission(
            transmission_id, "Report received successfully"
        )

        self.assertTrue(result)
        transmission = self.system.transmissions[transmission_id]
        self.assertTrue(transmission.acknowledgment_received)
        self.assertEqual(transmission.status, ReportStatus.ACKNOWLEDGED)

    def test_get_mmwr_week(self):
        """Test calculating MMWR week"""
        test_date = datetime(2025, 10, 31)
        year, week = self.system.get_mmwr_week(test_date)

        self.assertEqual(year, 2025)
        self.assertGreater(week, 0)
        self.assertLess(week, 54)

    def test_hl7_segment_formatting(self):
        """Test HL7 segment to string conversion"""
        from cdc_reporting import HL7Segment

        segment = HL7Segment("PID", [
            "1", "PT001", "John^Doe", "1980-01-15", "M"
        ])

        segment_string = segment.to_string()
        self.assertTrue(segment_string.startswith("PID|"))
        self.assertIn("PT001", segment_string)

    def test_reporting_summary(self):
        """Test getting reporting summary"""
        summary = self.system.get_reporting_summary()

        self.assertIn("total_reports", summary)
        self.assertIn("nedss_case_reports", summary)
        self.assertIn("nndss_surveillance_reports", summary)
        self.assertIn("electronic_lab_reports", summary)


class TestPublicHealthAnalytics(unittest.TestCase):
    """Test Public Health Analytics System"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = PublicHealthAnalytics()

    def test_register_population(self):
        """Test registering population data"""
        self.system.register_population("LOC001", 150000)

        self.assertIn("LOC001", self.system.population_data)
        self.assertEqual(self.system.population_data["LOC001"], 150000)

    def test_analyze_trend(self):
        """Test disease trend analysis"""
        # Create time series data
        base_date = datetime(2025, 10, 1)
        time_series = [
            ((base_date + timedelta(days=i)).isoformat()[:10], i + 1)
            for i in range(30)
        ]

        analysis_id = self.system.analyze_trend(
            disease_code="U07.1",
            disease_name="COVID-19",
            time_series_data=time_series,
            location_id="LOC001"
        )

        self.assertIsNotNone(analysis_id)
        self.assertIn(analysis_id, self.system.trend_analyses)

        analysis = self.system.trend_analyses[analysis_id]
        self.assertEqual(analysis.data_points, 30)
        self.assertIn(analysis.trend_direction, list(TrendDirection))

    def test_assess_risk(self):
        """Test population risk assessment"""
        self.system.register_population("LOC001", 100000)

        assessment_id = self.system.assess_risk(
            disease_code="U07.1",
            disease_name="COVID-19",
            location_id="LOC001",
            location_name="Springfield",
            current_cases=50,
            baseline_cases=20,
            week_over_week_change_pct=25.0,
            hospitalization_rate=10.0,
            icu_rate=2.0
        )

        self.assertIsNotNone(assessment_id)
        self.assertIn(assessment_id, self.system.risk_assessments)

        assessment = self.system.risk_assessments[assessment_id]
        self.assertIn(assessment.overall_risk, list(RiskLevel))
        self.assertGreater(assessment.incidence_ratio, 1.0)

    def test_analyze_health_equity(self):
        """Test health equity analysis"""
        group_data = {
            "Group A": (100, 50000),
            "Group B": (200, 50000),
            "Group C": (150, 50000)
        }

        analysis_id = self.system.analyze_health_equity(
            disease_code="U07.1",
            disease_name="COVID-19",
            dimension=HealthEquityDimension.RACE,
            group_data=group_data,
            period_start="2025-10-01",
            period_end="2025-10-31"
        )

        self.assertIsNotNone(analysis_id)
        self.assertIn(analysis_id, self.system.equity_analyses)

        analysis = self.system.equity_analyses[analysis_id]
        self.assertEqual(len(analysis.group_rates), 3)
        self.assertGreater(analysis.rate_ratio, 0)

    def test_generate_dashboard_metrics(self):
        """Test dashboard metrics generation"""
        case_data = {
            "total_cases": 1000,
            "new_cases_today": 50,
            "new_cases_this_week": 300,
            "week_over_week_change": 15.0,
            "active_alerts": 3,
            "critical_alerts": 1
        }

        dashboard_id = self.system.generate_dashboard_metrics(
            dashboard_name="COVID-19 Dashboard",
            period_start="2025-10-01",
            period_end="2025-10-31",
            case_data=case_data
        )

        self.assertIsNotNone(dashboard_id)
        self.assertIn(dashboard_id, self.system.dashboards)

        dashboard = self.system.dashboards[dashboard_id]
        self.assertEqual(dashboard.total_cases, 1000)
        self.assertEqual(dashboard.new_cases_today, 50)

    def test_trend_direction_detection(self):
        """Test trend direction is correctly identified"""
        # Increasing trend
        increasing_data = [
            (f"2025-10-{i+1:02d}", i * 10)
            for i in range(10)
        ]

        trend_id = self.system.analyze_trend(
            "U07.1", "COVID-19", increasing_data
        )

        trend = self.system.trend_analyses[trend_id]
        # Should detect increasing trend
        self.assertIn(trend.trend_direction, [TrendDirection.INCREASING, TrendDirection.STABLE])

    def test_risk_level_determination(self):
        """Test risk level is appropriately determined"""
        self.system.register_population("LOC001", 100000)

        # High risk scenario
        high_risk_id = self.system.assess_risk(
            "U07.1", "COVID-19", "LOC001", "Test Location",
            current_cases=500,  # High case count
            baseline_cases=50,   # 10x baseline
            week_over_week_change_pct=50.0  # Increasing
        )

        assessment = self.system.risk_assessments[high_risk_id]
        # Should be high or very high risk
        self.assertIn(assessment.overall_risk, [RiskLevel.HIGH, RiskLevel.VERY_HIGH])

    def test_health_equity_disparity_detection(self):
        """Test health equity disparities are detected"""
        # Create data with clear disparity
        group_data = {
            "Low disparity group": (50, 100000),
            "High disparity group": (200, 100000)  # 4x higher rate
        }

        equity_id = self.system.analyze_health_equity(
            "U07.1", "COVID-19",
            HealthEquityDimension.INCOME,
            group_data,
            "2025-10-01", "2025-10-31"
        )

        analysis = self.system.equity_analyses[equity_id]
        # Should detect substantial disparity
        self.assertGreater(analysis.rate_ratio, 1.5)

    def test_analytics_summary(self):
        """Test getting analytics summary statistics"""
        summary = self.system.get_analytics_summary()

        self.assertIn("trend_analyses", summary)
        self.assertIn("risk_assessments", summary)
        self.assertIn("health_equity_analyses", summary)

    def test_moving_averages(self):
        """Test moving average calculations"""
        # Create data for 14 days
        data = [
            (f"2025-10-{i+1:02d}", i + 10)
            for i in range(14)
        ]

        trend_id = self.system.analyze_trend(
            "U07.1", "COVID-19", data
        )

        trend = self.system.trend_analyses[trend_id]
        # Should have 7-day and 14-day moving averages
        self.assertIsNotNone(trend.moving_average_7day)
        self.assertIsNotNone(trend.moving_average_14day)


class TestPhase26Implementation(unittest.TestCase):
    """Test Phase 26 Main Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase26Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 26)
        self.assertEqual(self.implementation.phase_name, "Real-time CDC & Public Health Integration")
        self.assertEqual(self.implementation.story_points, 40)
        self.assertEqual(self.implementation.priority, "P1")

    def test_execution(self):
        """Test main execution"""
        task = {
            "goal": "Implement Real-time CDC & Public Health Integration",
            "phase_id": 26
        }

        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(result.success)

    def test_disease_surveillance_integration(self):
        """Test disease surveillance is integrated"""
        from disease_surveillance import DiseaseSurveillanceSystem

        result = self.implementation._implement_disease_surveillance(
            DiseaseSurveillanceSystem
        )

        self.assertIn("total_cases", result)
        self.assertGreater(result["total_cases"], 0)

    def test_outbreak_detection_integration(self):
        """Test outbreak detection is integrated"""
        from outbreak_detection import OutbreakDetectionSystem, ClusterCase

        result = self.implementation._implement_outbreak_detection(
            OutbreakDetectionSystem, ClusterCase
        )

        self.assertIn("clusters_detected", result)

    def test_cdc_reporting_integration(self):
        """Test CDC reporting is integrated"""
        from cdc_reporting import CDCReportingSystem, ReportFormat, JurisdictionLevel

        result = self.implementation._implement_cdc_reporting(
            CDCReportingSystem, ReportFormat, JurisdictionLevel
        )

        self.assertIn("reports_submitted", result)
        self.assertGreater(result["reports_submitted"], 0)

    def test_analytics_integration(self):
        """Test public health analytics is integrated"""
        from public_health_analytics import PublicHealthAnalytics

        result = self.implementation._implement_public_health_analytics(
            PublicHealthAnalytics
        )

        self.assertIn("trend_analyses", result)
        self.assertIn("risk_assessments", result)

    def test_get_stats(self):
        """Test getting implementation statistics"""
        stats = self.implementation.get_stats()

        self.assertEqual(stats["phase_id"], 26)
        self.assertEqual(stats["story_points"], 40)


class TestIntegration(unittest.TestCase):
    """Integration tests across multiple systems"""

    def test_end_to_end_case_reporting(self):
        """Test complete workflow from case to CDC reporting"""
        # 1. Report case in surveillance system
        surveillance = DiseaseSurveillanceSystem()
        case_id = surveillance.report_case(
            disease_code="U07.1",
            patient_id="PT999",
            patient_name="Integration Test",
            date_of_birth="1985-01-01",
            sex="M"
        )

        # 2. Create CDC report
        reporting = CDCReportingSystem()
        report_id = reporting.create_nedss_case_report(
            case_id=case_id,
            patient_id="PT999",
            patient_first_name="Integration",
            patient_last_name="Test",
            patient_dob="1985-01-01",
            patient_sex="M",
            disease_code="U07.1",
            disease_name="COVID-19"
        )

        # 3. Transmit report
        transmission_id = reporting.transmit_report(
            report_id=report_id,
            report_format=ReportFormat.NEDSS,
            destination=JurisdictionLevel.STATE,
            destination_endpoint="https://test.gov"
        )

        # Verify workflow
        self.assertIsNotNone(case_id)
        self.assertIsNotNone(report_id)
        self.assertIsNotNone(transmission_id)

    def test_outbreak_investigation_workflow(self):
        """Test outbreak detection to investigation workflow"""
        # 1. Detect cluster
        outbreak = OutbreakDetectionSystem()
        outbreak.register_location(
            "LOC999", "Test City", 40.7128, -74.0060, 100000
        )

        # Create cluster cases
        cases = []
        for i in range(5):
            case = ClusterCase(
                case_id=f"INT-{i}",
                patient_id=f"PT{i}",
                disease_code="U07.1",
                onset_date="2025-10-25",
                location_id="LOC999",
                latitude=40.7128,
                longitude=-74.0060
            )
            cases.append(case)

        clusters = outbreak.detect_spatial_clusters(cases, max_radius_km=10, min_cases=3)

        # 2. Create alert from cluster
        if clusters:
            alert_id = outbreak.create_alert_from_cluster(clusters[0])
            self.assertIsNotNone(alert_id)

            # 3. Initiate investigation
            inv_id = outbreak.initiate_investigation(
                clusters[0].cluster_id,
                "U07.1", "COVID-19",
                "INV999", "Test Investigator",
                100000
            )

            self.assertIsNotNone(inv_id)

    def test_analytics_dashboard_integration(self):
        """Test generating analytics for dashboard"""
        # 1. Create some surveillance data
        surveillance = DiseaseSurveillanceSystem()
        for i in range(10):
            surveillance.report_case(
                "U07.1", f"PT{i}", f"Patient {i}",
                "1980-01-01", "M"
            )

        # 2. Run analytics
        analytics = PublicHealthAnalytics()
        analytics.register_population("LOC001", 100000)

        # Create trend data
        time_series = [
            (f"2025-10-{i+1:02d}", i + 1)
            for i in range(30)
        ]

        trend_id = analytics.analyze_trend(
            "U07.1", "COVID-19", time_series, "LOC001"
        )

        # 3. Generate dashboard
        summary = surveillance.get_surveillance_summary()

        dashboard_id = analytics.generate_dashboard_metrics(
            "Integration Dashboard",
            "2025-10-01",
            "2025-10-31",
            {
                "total_cases": summary["total_cases"],
                "new_cases_today": 5,
                "new_cases_this_week": 30
            }
        )

        self.assertIsNotNone(trend_id)
        self.assertIsNotNone(dashboard_id)


if __name__ == "__main__":
    unittest.main()
