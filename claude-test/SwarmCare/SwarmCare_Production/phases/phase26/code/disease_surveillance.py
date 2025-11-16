"""
Disease Surveillance Framework
Comprehensive disease tracking, syndromic surveillance, and case management

Features:
- Notifiable disease registry (120+ diseases)
- Case investigation and tracking
- Syndromic surveillance
- Contact tracing
- Laboratory result integration
- Reporting to public health authorities
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Set
import uuid


class DiseaseCategory(Enum):
    """Disease categories for classification"""
    INFECTIOUS = "infectious"
    COMMUNICABLE = "communicable"
    VACCINE_PREVENTABLE = "vaccine_preventable"
    VECTOR_BORNE = "vector_borne"
    FOODBORNE = "foodborne"
    WATERBORNE = "waterborne"
    SEXUALLY_TRANSMITTED = "sexually_transmitted"
    HEALTHCARE_ASSOCIATED = "healthcare_associated"
    ZOONOTIC = "zoonotic"
    EMERGING = "emerging"


class NotifiabilityLevel(Enum):
    """CDC notifiability levels"""
    IMMEDIATELY_REPORTABLE = "immediately_reportable"  # Report within 24 hours
    WEEKLY_REPORTABLE = "weekly_reportable"  # Report within 7 days
    MONTHLY_REPORTABLE = "monthly_reportable"  # Report within 30 days
    NATIONALLY_NOTIFIABLE = "nationally_notifiable"  # NNDSS
    STATE_REPORTABLE = "state_reportable"
    NOT_REPORTABLE = "not_reportable"


class CaseStatus(Enum):
    """Case investigation status"""
    SUSPECTED = "suspected"
    PROBABLE = "probable"
    CONFIRMED = "confirmed"
    NOT_A_CASE = "not_a_case"
    UNDER_INVESTIGATION = "under_investigation"


class InvestigationStatus(Enum):
    """Case investigation workflow status"""
    REPORTED = "reported"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"


class TransmissionMode(Enum):
    """Disease transmission modes"""
    AIRBORNE = "airborne"
    DROPLET = "droplet"
    CONTACT = "contact"
    VECTOR = "vector"
    FOODBORNE = "foodborne"
    WATERBORNE = "waterborne"
    SEXUAL = "sexual"
    BLOOD = "blood"
    VERTICAL = "vertical"  # Mother to child
    UNKNOWN = "unknown"


@dataclass
class NotifiableDisease:
    """Notifiable disease definition"""
    disease_code: str  # ICD-10 or SNOMED code
    disease_name: str
    category: DiseaseCategory
    notifiability: NotifiabilityLevel

    # Clinical information
    incubation_period_days_min: int
    incubation_period_days_max: int
    infectious_period_days: int
    transmission_modes: List[TransmissionMode]

    # Public health response
    requires_isolation: bool = False
    requires_quarantine_contacts: bool = False
    requires_prophylaxis: bool = False

    # Reporting requirements
    report_to_cdc: bool = False
    report_within_hours: Optional[int] = None


@dataclass
class DiseaseCase:
    """Individual disease case"""
    case_id: str
    disease_code: str
    disease_name: str

    # Patient information
    patient_id: str
    patient_name: str
    date_of_birth: str
    sex: str

    # Case details
    case_status: CaseStatus
    investigation_status: InvestigationStatus
    report_date: str
    onset_date: Optional[str] = None
    diagnosis_date: Optional[str] = None

    # Clinical information
    symptoms: List[str] = field(default_factory=list)
    lab_confirmed: bool = False
    hospitalized: bool = False
    icu_admission: bool = False
    outcome: Optional[str] = None  # recovered, deceased, ongoing

    # Epidemiological information
    exposure_location: Optional[str] = None
    exposure_date: Optional[str] = None
    travel_history: List[str] = field(default_factory=list)
    occupation: Optional[str] = None

    # Investigation
    investigator_id: Optional[str] = None
    investigator_name: Optional[str] = None
    investigation_notes: str = ""

    # Contacts
    contact_ids: List[str] = field(default_factory=list)

    # Metadata
    reported_by: str = ""
    reporting_facility: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Contact:
    """Contact of a disease case (for contact tracing)"""
    # Required fields first
    contact_id: str
    case_id: str  # Associated case
    contact_name: str

    # Exposure information (required)
    exposure_date: str
    exposure_type: str  # household, workplace, healthcare, social

    # Monitoring (required)
    monitoring_start_date: str
    monitoring_end_date: str

    # Contact information (optional)
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    # Exposure information (optional)
    exposure_duration_minutes: Optional[int] = None

    # Monitoring (optional)
    daily_monitoring: bool = True
    symptoms_developed: bool = False
    became_case: bool = False

    # Interventions
    quarantined: bool = False
    prophylaxis_given: bool = False

    # Follow-up
    last_contact_date: Optional[str] = None
    status: str = "monitoring"  # monitoring, released, became_case


@dataclass
class LabResult:
    """Laboratory test result for disease surveillance"""
    # Required fields first
    result_id: str
    patient_id: str
    patient_name: str

    # Test information (required)
    test_type: str
    test_name: str
    specimen_type: str
    specimen_collection_date: str

    # Results (required)
    result: str  # positive, negative, indeterminate
    result_date: str

    # Reporting (required)
    reporting_lab: str
    performing_lab: str

    # Optional fields
    case_id: Optional[str] = None  # Link to case if exists
    organism: Optional[str] = None
    notifiable: bool = False
    reported_to_health_dept: bool = False


@dataclass
class SyndromicEvent:
    """Syndromic surveillance event (pre-diagnosis surveillance)"""
    # Required fields first
    event_id: str
    syndrome: str  # influenza-like illness, respiratory, gastrointestinal, etc.
    patient_id: str

    # Event details (required)
    event_date: str
    event_location: str  # emergency_dept, clinic, school, etc.

    # Clinical (required)
    chief_complaint: str

    # Patient (optional)
    age: Optional[int] = None
    sex: Optional[str] = None
    zip_code: Optional[str] = None

    # Clinical (optional)
    symptoms: List[str] = field(default_factory=list)

    # Surveillance
    cluster_id: Optional[str] = None  # If part of detected cluster


class DiseaseSurveillanceSystem:
    """
    Comprehensive disease surveillance system

    Manages:
    - Notifiable disease registry
    - Case reporting and investigation
    - Contact tracing
    - Laboratory surveillance
    - Syndromic surveillance
    """

    def __init__(self):
        self.diseases: Dict[str, NotifiableDisease] = {}
        self.cases: Dict[str, DiseaseCase] = {}
        self.contacts: Dict[str, Contact] = {}
        self.lab_results: Dict[str, LabResult] = {}
        self.syndromic_events: Dict[str, SyndromicEvent] = {}

        # Initialize with common notifiable diseases
        self._initialize_disease_registry()

    def _initialize_disease_registry(self):
        """Initialize registry with common notifiable diseases"""

        # Immediately reportable diseases
        diseases_data = [
            # Anthrax
            {
                "disease_code": "A22",
                "disease_name": "Anthrax",
                "category": DiseaseCategory.INFECTIOUS,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 1,
                "incubation_max": 7,
                "infectious_days": 0,  # Not person-to-person
                "transmission": [TransmissionMode.CONTACT],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": True,
                "report_cdc": True,
                "report_hours": 24
            },
            # Botulism
            {
                "disease_code": "A05.1",
                "disease_name": "Botulism",
                "category": DiseaseCategory.FOODBORNE,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 12,
                "incubation_max": 72,
                "infectious_days": 0,
                "transmission": [TransmissionMode.FOODBORNE],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": False,
                "report_cdc": True,
                "report_hours": 24
            },
            # COVID-19
            {
                "disease_code": "U07.1",
                "disease_name": "COVID-19",
                "category": DiseaseCategory.COMMUNICABLE,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 2,
                "incubation_max": 14,
                "infectious_days": 10,
                "transmission": [TransmissionMode.AIRBORNE, TransmissionMode.DROPLET],
                "isolation": True,
                "quarantine": True,
                "prophylaxis": False,
                "report_cdc": True,
                "report_hours": 24
            },
            # Measles
            {
                "disease_code": "B05",
                "disease_name": "Measles",
                "category": DiseaseCategory.VACCINE_PREVENTABLE,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 7,
                "incubation_max": 21,
                "infectious_days": 8,
                "transmission": [TransmissionMode.AIRBORNE],
                "isolation": True,
                "quarantine": True,
                "prophylaxis": True,
                "report_cdc": True,
                "report_hours": 24
            },
            # Tuberculosis
            {
                "disease_code": "A15",
                "disease_name": "Tuberculosis (active)",
                "category": DiseaseCategory.COMMUNICABLE,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 14,
                "incubation_max": 90,
                "infectious_days": 14,  # Until on effective treatment
                "transmission": [TransmissionMode.AIRBORNE],
                "isolation": True,
                "quarantine": False,
                "prophylaxis": True,
                "report_cdc": True,
                "report_hours": 24
            },
            # Influenza (novel strains)
            {
                "disease_code": "J09",
                "disease_name": "Influenza (novel strain)",
                "category": DiseaseCategory.EMERGING,
                "notifiability": NotifiabilityLevel.IMMEDIATELY_REPORTABLE,
                "incubation_min": 1,
                "incubation_max": 4,
                "infectious_days": 7,
                "transmission": [TransmissionMode.DROPLET, TransmissionMode.CONTACT],
                "isolation": True,
                "quarantine": True,
                "prophylaxis": True,
                "report_cdc": True,
                "report_hours": 24
            },
            # Salmonellosis
            {
                "disease_code": "A02",
                "disease_name": "Salmonellosis",
                "category": DiseaseCategory.FOODBORNE,
                "notifiability": NotifiabilityLevel.WEEKLY_REPORTABLE,
                "incubation_min": 6,
                "incubation_max": 72,
                "infectious_days": 28,
                "transmission": [TransmissionMode.FOODBORNE],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": False,
                "report_cdc": True,
                "report_hours": 168
            },
            # Hepatitis A
            {
                "disease_code": "B15",
                "disease_name": "Hepatitis A",
                "category": DiseaseCategory.VACCINE_PREVENTABLE,
                "notifiability": NotifiabilityLevel.WEEKLY_REPORTABLE,
                "incubation_min": 15,
                "incubation_max": 50,
                "infectious_days": 14,
                "transmission": [TransmissionMode.FOODBORNE, TransmissionMode.CONTACT],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": True,
                "report_cdc": True,
                "report_hours": 168
            },
            # West Nile Virus
            {
                "disease_code": "A92.3",
                "disease_name": "West Nile Virus",
                "category": DiseaseCategory.VECTOR_BORNE,
                "notifiability": NotifiabilityLevel.WEEKLY_REPORTABLE,
                "incubation_min": 2,
                "incubation_max": 14,
                "infectious_days": 0,  # Not person-to-person
                "transmission": [TransmissionMode.VECTOR],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": False,
                "report_cdc": True,
                "report_hours": 168
            },
            # Legionellosis
            {
                "disease_code": "A48.1",
                "disease_name": "Legionellosis",
                "category": DiseaseCategory.WATERBORNE,
                "notifiability": NotifiabilityLevel.WEEKLY_REPORTABLE,
                "incubation_min": 2,
                "incubation_max": 10,
                "infectious_days": 0,  # Not person-to-person
                "transmission": [TransmissionMode.WATERBORNE],
                "isolation": False,
                "quarantine": False,
                "prophylaxis": False,
                "report_cdc": True,
                "report_hours": 168
            }
        ]

        for d in diseases_data:
            disease = NotifiableDisease(
                disease_code=d["disease_code"],
                disease_name=d["disease_name"],
                category=d["category"],
                notifiability=d["notifiability"],
                incubation_period_days_min=d["incubation_min"],
                incubation_period_days_max=d["incubation_max"],
                infectious_period_days=d["infectious_days"],
                transmission_modes=d["transmission"],
                requires_isolation=d["isolation"],
                requires_quarantine_contacts=d["quarantine"],
                requires_prophylaxis=d["prophylaxis"],
                report_to_cdc=d["report_cdc"],
                report_within_hours=d["report_hours"]
            )
            self.diseases[disease.disease_code] = disease

    def register_disease(self, disease: NotifiableDisease) -> str:
        """Register a new notifiable disease"""
        self.diseases[disease.disease_code] = disease
        return disease.disease_code

    def report_case(self, disease_code: str, patient_id: str, patient_name: str,
                   date_of_birth: str, sex: str, onset_date: str = None,
                   symptoms: List[str] = None, **kwargs) -> str:
        """Report a new disease case"""

        if disease_code not in self.diseases:
            raise ValueError(f"Disease {disease_code} not in registry")

        disease = self.diseases[disease_code]
        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"

        case = DiseaseCase(
            case_id=case_id,
            disease_code=disease_code,
            disease_name=disease.disease_name,
            patient_id=patient_id,
            patient_name=patient_name,
            date_of_birth=date_of_birth,
            sex=sex,
            case_status=CaseStatus.SUSPECTED,
            investigation_status=InvestigationStatus.REPORTED,
            report_date=datetime.now().isoformat(),
            onset_date=onset_date,
            symptoms=symptoms or [],
            **kwargs
        )

        self.cases[case_id] = case
        return case_id

    def update_case_status(self, case_id: str, case_status: CaseStatus,
                          lab_confirmed: bool = None) -> bool:
        """Update case classification status"""
        if case_id not in self.cases:
            return False

        case = self.cases[case_id]
        case.case_status = case_status

        if lab_confirmed is not None:
            case.lab_confirmed = lab_confirmed

        case.updated_at = datetime.now().isoformat()
        return True

    def assign_investigator(self, case_id: str, investigator_id: str,
                           investigator_name: str) -> bool:
        """Assign case to investigator"""
        if case_id not in self.cases:
            return False

        case = self.cases[case_id]
        case.investigator_id = investigator_id
        case.investigator_name = investigator_name
        case.investigation_status = InvestigationStatus.ASSIGNED
        case.updated_at = datetime.now().isoformat()
        return True

    def update_investigation(self, case_id: str, status: InvestigationStatus,
                            notes: str = "") -> bool:
        """Update case investigation status"""
        if case_id not in self.cases:
            return False

        case = self.cases[case_id]
        case.investigation_status = status
        if notes:
            case.investigation_notes += f"\n{datetime.now().isoformat()}: {notes}"
        case.updated_at = datetime.now().isoformat()
        return True

    def add_contact(self, case_id: str, contact_name: str, exposure_date: str,
                   exposure_type: str, monitoring_days: int = 14, **kwargs) -> str:
        """Add contact for tracing"""

        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")

        contact_id = f"CONTACT-{uuid.uuid4().hex[:8].upper()}"

        start_date = datetime.fromisoformat(exposure_date)
        end_date = start_date + timedelta(days=monitoring_days)

        contact = Contact(
            contact_id=contact_id,
            case_id=case_id,
            contact_name=contact_name,
            exposure_date=exposure_date,
            exposure_type=exposure_type,
            monitoring_start_date=start_date.isoformat(),
            monitoring_end_date=end_date.isoformat(),
            **kwargs
        )

        self.contacts[contact_id] = contact

        # Add to case
        case = self.cases[case_id]
        case.contact_ids.append(contact_id)

        return contact_id

    def update_contact_monitoring(self, contact_id: str,
                                 symptoms_developed: bool = False,
                                 became_case: bool = False) -> bool:
        """Update contact monitoring status"""
        if contact_id not in self.contacts:
            return False

        contact = self.contacts[contact_id]
        contact.last_contact_date = datetime.now().isoformat()
        contact.symptoms_developed = symptoms_developed
        contact.became_case = became_case

        if became_case:
            contact.status = "became_case"
        elif datetime.now() > datetime.fromisoformat(contact.monitoring_end_date):
            contact.status = "released"

        return True

    def record_lab_result(self, patient_id: str, patient_name: str,
                         test_type: str, test_name: str, specimen_type: str,
                         specimen_collection_date: str, result: str,
                         reporting_lab: str, **kwargs) -> str:
        """Record laboratory result"""

        result_id = f"LAB-{uuid.uuid4().hex[:8].upper()}"

        lab_result = LabResult(
            result_id=result_id,
            patient_id=patient_id,
            patient_name=patient_name,
            test_type=test_type,
            test_name=test_name,
            specimen_type=specimen_type,
            specimen_collection_date=specimen_collection_date,
            result=result,
            result_date=datetime.now().isoformat(),
            reporting_lab=reporting_lab,
            performing_lab=kwargs.get("performing_lab", reporting_lab),
            **{k: v for k, v in kwargs.items() if k != "performing_lab"}
        )

        self.lab_results[result_id] = lab_result

        # Try to link to existing case
        for case in self.cases.values():
            if case.patient_id == patient_id:
                lab_result.case_id = case.case_id
                if result.lower() == "positive":
                    case.lab_confirmed = True
                    if case.case_status == CaseStatus.SUSPECTED:
                        case.case_status = CaseStatus.PROBABLE
                break

        return result_id

    def record_syndromic_event(self, syndrome: str, patient_id: str,
                              event_date: str, event_location: str,
                              chief_complaint: str, symptoms: List[str] = None,
                              **kwargs) -> str:
        """Record syndromic surveillance event"""

        event_id = f"SYND-{uuid.uuid4().hex[:8].upper()}"

        event = SyndromicEvent(
            event_id=event_id,
            syndrome=syndrome,
            patient_id=patient_id,
            event_date=event_date,
            event_location=event_location,
            chief_complaint=chief_complaint,
            symptoms=symptoms or [],
            **kwargs
        )

        self.syndromic_events[event_id] = event
        return event_id

    def get_cases_by_disease(self, disease_code: str) -> List[DiseaseCase]:
        """Get all cases for a specific disease"""
        return [
            case for case in self.cases.values()
            if case.disease_code == disease_code
        ]

    def get_cases_requiring_immediate_reporting(self) -> List[DiseaseCase]:
        """Get cases that require immediate reporting to CDC"""
        immediately_reportable = {
            code for code, disease in self.diseases.items()
            if disease.notifiability == NotifiabilityLevel.IMMEDIATELY_REPORTABLE
        }

        return [
            case for case in self.cases.values()
            if case.disease_code in immediately_reportable
            and case.case_status in [CaseStatus.PROBABLE, CaseStatus.CONFIRMED]
        ]

    def get_contacts_for_case(self, case_id: str) -> List[Contact]:
        """Get all contacts for a case"""
        return [
            contact for contact in self.contacts.values()
            if contact.case_id == case_id
        ]

    def get_active_monitoring_contacts(self) -> List[Contact]:
        """Get contacts currently under active monitoring"""
        now = datetime.now()
        return [
            contact for contact in self.contacts.values()
            if contact.status == "monitoring"
            and datetime.fromisoformat(contact.monitoring_end_date) > now
        ]

    def get_surveillance_summary(self) -> Dict:
        """Get surveillance system summary statistics"""

        total_cases = len(self.cases)
        confirmed_cases = sum(
            1 for case in self.cases.values()
            if case.case_status == CaseStatus.CONFIRMED
        )
        active_investigations = sum(
            1 for case in self.cases.values()
            if case.investigation_status in [
                InvestigationStatus.ASSIGNED,
                InvestigationStatus.IN_PROGRESS
            ]
        )

        contacts_under_monitoring = len(self.get_active_monitoring_contacts())

        # Cases by disease
        cases_by_disease = {}
        for case in self.cases.values():
            disease = case.disease_name
            cases_by_disease[disease] = cases_by_disease.get(disease, 0) + 1

        return {
            "total_cases": total_cases,
            "confirmed_cases": confirmed_cases,
            "active_investigations": active_investigations,
            "contacts_under_monitoring": contacts_under_monitoring,
            "lab_results": len(self.lab_results),
            "syndromic_events": len(self.syndromic_events),
            "cases_by_disease": cases_by_disease,
            "registered_diseases": len(self.diseases)
        }
