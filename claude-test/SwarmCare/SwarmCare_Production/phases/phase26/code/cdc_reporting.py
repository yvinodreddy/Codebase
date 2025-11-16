"""
CDC Reporting Framework
Comprehensive CDC reporting with HL7, NEDSS, NNDSS formats

Features:
- HL7 message generation (ORU^R01, ADT^A01)
- NEDSS Base System (NBS) integration
- NNDSS (National Notifiable Diseases Surveillance System)
- Electronic Laboratory Reporting (ELR)
- Case reporting to CDC
- Automated transmission
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Tuple
import uuid
import json


class ReportType(Enum):
    """Type of report"""
    CASE_REPORT = "case_report"  # Individual case
    LAB_REPORT = "lab_report"  # Laboratory result
    OUTBREAK_REPORT = "outbreak_report"  # Outbreak summary
    SURVEILLANCE_SUMMARY = "surveillance_summary"  # Periodic summary


class ReportFormat(Enum):
    """Report format/standard"""
    HL7_V2 = "hl7_v2"  # HL7 Version 2.x messages
    HL7_FHIR = "hl7_fhir"  # HL7 FHIR resources
    NEDSS = "nedss"  # NEDSS Base System
    NNDSS = "nndss"  # National Notifiable Diseases
    CDC_CSV = "cdc_csv"  # CDC CSV format
    XML = "xml"  # Generic XML


class ReportStatus(Enum):
    """Report submission status"""
    DRAFT = "draft"
    READY = "ready"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"
    COMPLETED = "completed"


class JurisdictionLevel(Enum):
    """Reporting jurisdiction"""
    LOCAL = "local"  # County/city health department
    STATE = "state"  # State health department
    FEDERAL = "federal"  # CDC/federal agencies
    INTERNATIONAL = "international"  # WHO, etc.


@dataclass
class HL7Segment:
    """HL7 message segment"""
    segment_type: str  # MSH, PID, OBR, OBX, etc.
    fields: List[str]

    def to_string(self, field_separator: str = "|",
                  component_separator: str = "^",
                  repetition_separator: str = "~",
                  escape_char: str = "\\",
                  subcomponent_separator: str = "&") -> str:
        """Convert segment to HL7 string format"""

        if self.segment_type == "MSH":
            # MSH segment is special - field separator is field 1
            return f"MSH{field_separator}{component_separator}{repetition_separator}{escape_char}{subcomponent_separator}{field_separator}" + field_separator.join(self.fields)
        else:
            return f"{self.segment_type}{field_separator}" + field_separator.join(self.fields)


@dataclass
class HL7Message:
    """HL7 v2 message"""
    message_type: str  # ORU^R01, ADT^A01, etc.
    message_id: str
    segments: List[HL7Segment] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_string(self) -> str:
        """Convert entire message to HL7 format"""
        return "\r".join(segment.to_string() for segment in self.segments)


@dataclass
class NEDSSCaseReport:
    """NEDSS (National Electronic Disease Surveillance System) case report"""
    # Required fields first
    report_id: str
    case_id: str

    # Patient demographics (required)
    patient_id: str
    patient_first_name: str
    patient_last_name: str
    patient_date_of_birth: str
    patient_sex: str

    # Disease information (required)
    disease_code: str  # SNOMED or ICD-10
    disease_name: str

    # Patient demographics (optional)
    patient_race: Optional[str] = None
    patient_ethnicity: Optional[str] = None

    # Address (optional)
    patient_street_address: Optional[str] = None
    patient_city: Optional[str] = None
    patient_state: Optional[str] = None
    patient_zip: Optional[str] = None
    patient_county: Optional[str] = None

    # Disease information (optional)
    condition_code: Optional[str] = None  # CDC condition code

    # Dates
    date_of_onset: Optional[str] = None
    date_of_diagnosis: Optional[str] = None
    date_reported_to_phd: str = ""  # Public health department

    # Case classification
    case_status: str = "suspected"  # suspected, probable, confirmed
    imported_case: bool = False
    outbreak_associated: bool = False
    outbreak_name: Optional[str] = None

    # Clinical
    hospitalized: bool = False
    icu_admission: bool = False
    died: bool = False
    pregnant: bool = False

    # Reporting source
    reporting_source_type: str = ""  # hospital, clinic, lab, etc.
    reporting_facility: str = ""
    reporter_name: str = ""
    reporter_phone: str = ""

    # Jurisdiction
    jurisdiction: str = ""  # State/local jurisdiction code

    # Investigation
    investigator_name: Optional[str] = None
    investigation_start_date: Optional[str] = None
    investigation_status: str = "open"


@dataclass
class NNDSSReport:
    """NNDSS (National Notifiable Diseases Surveillance System) report"""
    report_id: str

    # MMWR (Morbidity and Mortality Weekly Report) information
    mmwr_year: int
    mmwr_week: int

    # Reporting area
    reporting_area: str  # State/territory
    reporting_area_code: str  # FIPS code

    # Disease
    condition: str  # NNDSS condition name
    condition_code: str  # NNDSS condition code

    # Case counts
    current_week_cases: int = 0
    current_week_flag: str = ""  # N (no cases), - (not reportable)
    cumulative_ytd_cases: int = 0

    # Comparison to previous years
    previous_52_weeks_median: Optional[int] = None
    previous_52_weeks_max: Optional[int] = None

    # Demographics (optional)
    age_group_counts: Dict[str, int] = field(default_factory=dict)
    sex_counts: Dict[str, int] = field(default_factory=dict)


@dataclass
class ElectronicLabReport:
    """Electronic Laboratory Reporting (ELR)"""
    # Required fields first
    report_id: str

    # Patient (required)
    patient_id: str
    patient_name: str
    patient_dob: str
    patient_sex: str

    # Specimen (required)
    specimen_id: str
    specimen_type: str
    specimen_collection_date: str

    # Test (required)
    test_type_code: str  # LOINC code
    test_type_name: str

    # Results (required)
    result: str  # Positive, Negative, Indeterminate
    performing_lab_name: str

    # Specimen (optional)
    specimen_received_date: str = ""

    # Test (optional)
    test_method: Optional[str] = None

    # Results (optional)
    result_status: str = "final"  # preliminary, final, corrected
    result_date: str = ""

    # Organism identification
    organism_code: Optional[str] = None  # SNOMED code
    organism_name: Optional[str] = None

    # Lab information
    ordering_facility: str = ""
    performing_lab_clia: str = ""  # CLIA number

    # Reporter
    ordering_provider_name: str = ""
    ordering_provider_npi: Optional[str] = None

    # Notifiable
    notifiable: bool = False
    condition_code: Optional[str] = None


@dataclass
class CDCTransmission:
    """Record of transmission to CDC"""
    transmission_id: str
    report_id: str
    report_type: ReportType
    report_format: ReportFormat

    # Transmission details
    destination: JurisdictionLevel
    destination_endpoint: str  # URL or system name
    transmission_date: str

    # Status
    status: ReportStatus
    acknowledgment_received: bool = False
    acknowledgment_date: Optional[str] = None
    acknowledgment_message: Optional[str] = None

    # Content
    message_content: str = ""  # HL7, XML, JSON, etc.
    message_size_bytes: int = 0

    # Retry information
    retry_count: int = 0
    last_error: Optional[str] = None


class CDCReportingSystem:
    """
    Comprehensive CDC reporting system

    Supports:
    - HL7 message generation
    - NEDSS case reporting
    - NNDSS surveillance reporting
    - Electronic lab reporting
    - Multi-format report generation
    - Transmission tracking
    """

    def __init__(self):
        self.reports: Dict[str, Dict] = {}  # All reports
        self.nedss_reports: Dict[str, NEDSSCaseReport] = {}
        self.nndss_reports: Dict[str, NNDSSReport] = {}
        self.lab_reports: Dict[str, ElectronicLabReport] = {}
        self.hl7_messages: Dict[str, HL7Message] = {}
        self.transmissions: Dict[str, CDCTransmission] = {}

        # CDC condition codes (NNDSS)
        self.nndss_conditions = self._initialize_nndss_conditions()

    def _initialize_nndss_conditions(self) -> Dict[str, str]:
        """Initialize NNDSS reportable conditions"""
        return {
            "10350": "Anthrax",
            "10054": "Botulism",
            "11065": "COVID-19",
            "10140": "Measles",
            "10210": "Tuberculosis",
            "11723": "Novel Influenza A",
            "10290": "Salmonellosis",
            "10110": "Hepatitis A",
            "10580": "West Nile Virus",
            "10490": "Legionellosis",
            "10520": "Lyme disease",
            "10450": "Hepatitis B",
            "10460": "Hepatitis C",
            "11550": "HIV infection",
            "10590": "Listeriosis",
            "10180": "Meningococcal disease",
            "10190": "Mumps",
            "10200": "Pertussis",
            "10410": "Rabies (animal)",
            "10250": "Rubella",
            "10370": "Shiga toxin-producing E. coli",
            "10380": "Shigellosis",
            "10680": "Varicella",
        }

    def create_nedss_case_report(self, case_id: str, patient_id: str,
                                 patient_first_name: str, patient_last_name: str,
                                 patient_dob: str, patient_sex: str,
                                 disease_code: str, disease_name: str,
                                 **kwargs) -> str:
        """Create NEDSS case report"""

        report_id = f"NEDSS-{uuid.uuid4().hex[:8].upper()}"

        # Get CDC condition code
        condition_code = None
        for code, name in self.nndss_conditions.items():
            if disease_name.lower() in name.lower():
                condition_code = code
                break

        report = NEDSSCaseReport(
            report_id=report_id,
            case_id=case_id,
            patient_id=patient_id,
            patient_first_name=patient_first_name,
            patient_last_name=patient_last_name,
            patient_date_of_birth=patient_dob,
            patient_sex=patient_sex,
            disease_code=disease_code,
            disease_name=disease_name,
            condition_code=condition_code,
            date_reported_to_phd=datetime.now().isoformat(),
            **kwargs
        )

        self.nedss_reports[report_id] = report
        self.reports[report_id] = {"type": ReportType.CASE_REPORT, "report": report}

        return report_id

    def create_nndss_weekly_report(self, reporting_area: str,
                                   reporting_area_code: str,
                                   condition: str, condition_code: str,
                                   mmwr_year: int, mmwr_week: int,
                                   current_week_cases: int,
                                   cumulative_ytd_cases: int,
                                   **kwargs) -> str:
        """Create NNDSS weekly surveillance report"""

        report_id = f"NNDSS-{uuid.uuid4().hex[:8].upper()}"

        report = NNDSSReport(
            report_id=report_id,
            mmwr_year=mmwr_year,
            mmwr_week=mmwr_week,
            reporting_area=reporting_area,
            reporting_area_code=reporting_area_code,
            condition=condition,
            condition_code=condition_code,
            current_week_cases=current_week_cases,
            cumulative_ytd_cases=cumulative_ytd_cases,
            **kwargs
        )

        self.nndss_reports[report_id] = report
        self.reports[report_id] = {"type": ReportType.SURVEILLANCE_SUMMARY, "report": report}

        return report_id

    def create_electronic_lab_report(self, patient_id: str, patient_name: str,
                                    patient_dob: str, patient_sex: str,
                                    specimen_id: str, specimen_type: str,
                                    specimen_collection_date: str,
                                    test_type_code: str, test_type_name: str,
                                    result: str, performing_lab_name: str,
                                    **kwargs) -> str:
        """Create electronic laboratory report"""

        report_id = f"ELR-{uuid.uuid4().hex[:8].upper()}"

        report = ElectronicLabReport(
            report_id=report_id,
            patient_id=patient_id,
            patient_name=patient_name,
            patient_dob=patient_dob,
            patient_sex=patient_sex,
            specimen_id=specimen_id,
            specimen_type=specimen_type,
            specimen_collection_date=specimen_collection_date,
            test_type_code=test_type_code,
            test_type_name=test_type_name,
            result=result,
            result_date=datetime.now().isoformat(),
            performing_lab_name=performing_lab_name,
            **kwargs
        )

        self.lab_reports[report_id] = report
        self.reports[report_id] = {"type": ReportType.LAB_REPORT, "report": report}

        return report_id

    def generate_hl7_oru_message(self, lab_report_id: str) -> str:
        """
        Generate HL7 ORU^R01 message for lab result
        (Unsolicited Observation Result)
        """

        if lab_report_id not in self.lab_reports:
            raise ValueError(f"Lab report {lab_report_id} not found")

        lab = self.lab_reports[lab_report_id]
        message_id = f"HL7-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        segments = []

        # MSH - Message Header
        msh = HL7Segment("MSH", [
            "",  # Encoding characters (added by to_string)
            lab.performing_lab_name,  # Sending application
            lab.performing_lab_clia,  # Sending facility
            "CDC",  # Receiving application
            "NEDSS",  # Receiving facility
            timestamp,  # Message datetime
            "",  # Security
            "ORU^R01",  # Message type
            message_id,  # Message control ID
            "P",  # Processing ID (P=Production, T=Test)
            "2.5.1"  # HL7 version
        ])
        segments.append(msh)

        # PID - Patient Identification
        pid = HL7Segment("PID", [
            "1",  # Set ID
            "",  # Patient ID (external)
            lab.patient_id,  # Patient ID (internal)
            "",  # Alternate patient ID
            lab.patient_name,  # Patient name
            "",  # Mother's maiden name
            lab.patient_dob,  # Date of birth
            lab.patient_sex,  # Sex
            "",  # Patient alias
            "",  # Race
            "",  # Patient address
            "",  # County code
            ""   # Phone number
        ])
        segments.append(pid)

        # OBR - Observation Request
        obr = HL7Segment("OBR", [
            "1",  # Set ID
            "",  # Placer order number
            lab.specimen_id,  # Filler order number
            f"{lab.test_type_code}^{lab.test_type_name}",  # Universal service ID
            "",  # Priority
            lab.specimen_collection_date,  # Observation date/time
            "",  # Observation end date/time
            "",  # Collection volume
            "",  # Collector identifier
            "",  # Specimen action code
            "",  # Danger code
            "",  # Relevant clinical info
            lab.specimen_collection_date,  # Specimen received date/time
            lab.specimen_type,  # Specimen source
            lab.ordering_provider_name,  # Ordering provider
            "",  # Order callback phone
            "",  # Placer field 1
            "",  # Placer field 2
            "",  # Filler field 1
            "",  # Filler field 2
            lab.result_date,  # Results date/time
            "",  # Charge to practice
            "",  # Diagnostic service section
            lab.result_status  # Result status
        ])
        segments.append(obr)

        # OBX - Observation Result
        obx = HL7Segment("OBX", [
            "1",  # Set ID
            "CE",  # Value type (CE=Coded Entry)
            f"{lab.test_type_code}^{lab.test_type_name}",  # Observation identifier
            "",  # Observation sub-ID
            lab.result,  # Observation value
            "",  # Units
            "",  # Reference range
            "",  # Abnormal flags
            "",  # Probability
            "",  # Nature of abnormal test
            lab.result_status,  # Observation result status
            "",  # Effective date
            "",  # User defined access checks
            lab.result_date  # Date/time of observation
        ])
        segments.append(obx)

        # If organism identified, add another OBX
        if lab.organism_name:
            obx_organism = HL7Segment("OBX", [
                "2",  # Set ID
                "CE",  # Value type
                "ORGANISM^Organism",  # Observation identifier
                "",  # Observation sub-ID
                f"{lab.organism_code or ''}^{lab.organism_name}",  # Organism
                "",  # Units
                "",  # Reference range
                "",  # Abnormal flags
                "",  # Probability
                "",  # Nature of abnormal test
                lab.result_status,  # Status
                "",  # Effective date
                "",  # Access checks
                lab.result_date  # Date/time
            ])
            segments.append(obx_organism)

        message = HL7Message(
            message_type="ORU^R01",
            message_id=message_id,
            segments=segments
        )

        self.hl7_messages[message_id] = message
        return message_id

    def transmit_report(self, report_id: str, report_format: ReportFormat,
                       destination: JurisdictionLevel,
                       destination_endpoint: str) -> str:
        """Transmit report to public health authorities"""

        if report_id not in self.reports:
            raise ValueError(f"Report {report_id} not found")

        report_info = self.reports[report_id]
        report_type = report_info["type"]
        report = report_info["report"]

        # Generate message content based on format
        if report_format == ReportFormat.HL7_V2:
            # For lab reports, generate HL7
            if report_type == ReportType.LAB_REPORT:
                hl7_id = self.generate_hl7_oru_message(report_id)
                message_content = self.hl7_messages[hl7_id].to_string()
            else:
                message_content = json.dumps(vars(report), default=str, indent=2)
        elif report_format == ReportFormat.NEDSS:
            message_content = json.dumps(vars(report), default=str, indent=2)
        elif report_format == ReportFormat.NNDSS:
            message_content = json.dumps(vars(report), default=str, indent=2)
        else:
            message_content = json.dumps(vars(report), default=str, indent=2)

        transmission_id = f"TX-{uuid.uuid4().hex[:8].upper()}"

        transmission = CDCTransmission(
            transmission_id=transmission_id,
            report_id=report_id,
            report_type=report_type,
            report_format=report_format,
            destination=destination,
            destination_endpoint=destination_endpoint,
            transmission_date=datetime.now().isoformat(),
            status=ReportStatus.SUBMITTED,
            message_content=message_content,
            message_size_bytes=len(message_content)
        )

        self.transmissions[transmission_id] = transmission
        return transmission_id

    def acknowledge_transmission(self, transmission_id: str,
                                acknowledgment_message: str = "") -> bool:
        """Record acknowledgment from receiving system"""

        if transmission_id not in self.transmissions:
            return False

        transmission = self.transmissions[transmission_id]
        transmission.acknowledgment_received = True
        transmission.acknowledgment_date = datetime.now().isoformat()
        transmission.acknowledgment_message = acknowledgment_message
        transmission.status = ReportStatus.ACKNOWLEDGED

        return True

    def get_pending_transmissions(self) -> List[CDCTransmission]:
        """Get transmissions awaiting acknowledgment"""
        return [
            tx for tx in self.transmissions.values()
            if tx.status == ReportStatus.SUBMITTED
            and not tx.acknowledgment_received
        ]

    def get_mmwr_week(self, date: datetime = None) -> Tuple[int, int]:
        """
        Get MMWR (Morbidity and Mortality Weekly Report) week
        Returns (year, week)

        MMWR week starts on Sunday
        """
        if date is None:
            date = datetime.now()

        # Find the first day of the year
        jan1 = datetime(date.year, 1, 1)

        # Find the first Sunday of the year (MMWR week 1 starts)
        days_to_sunday = (6 - jan1.weekday()) % 7
        first_sunday = jan1 + timedelta(days=days_to_sunday)

        # Calculate week number
        if date < first_sunday:
            # Belongs to last week of previous year
            return self.get_mmwr_week(datetime(date.year - 1, 12, 31))

        days_since_first = (date - first_sunday).days
        week = (days_since_first // 7) + 1

        return (date.year, week)

    def get_reporting_summary(self) -> Dict:
        """Get reporting system summary statistics"""

        total_reports = len(self.reports)
        nedss_count = len(self.nedss_reports)
        nndss_count = len(self.nndss_reports)
        lab_count = len(self.lab_reports)

        transmitted = len(self.transmissions)
        acknowledged = sum(
            1 for tx in self.transmissions.values()
            if tx.acknowledgment_received
        )
        pending = transmitted - acknowledged

        return {
            "total_reports": total_reports,
            "nedss_case_reports": nedss_count,
            "nndss_surveillance_reports": nndss_count,
            "electronic_lab_reports": lab_count,
            "hl7_messages": len(self.hl7_messages),
            "transmissions_sent": transmitted,
            "transmissions_acknowledged": acknowledged,
            "transmissions_pending": pending,
            "nndss_conditions": len(self.nndss_conditions)
        }
