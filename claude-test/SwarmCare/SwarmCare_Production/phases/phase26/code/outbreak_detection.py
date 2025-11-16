"""
Outbreak Detection System
Statistical outbreak detection, cluster analysis, and alert generation

Features:
- Spatial cluster detection
- Temporal cluster detection
- Spatio-temporal analysis
- Threshold-based alerts
- Statistical aberration detection
- Outbreak investigation workflows
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import uuid
import math


class ClusterType(Enum):
    """Type of cluster detected"""
    SPATIAL = "spatial"  # Geographic clustering
    TEMPORAL = "temporal"  # Time clustering
    SPATIOTEMPORAL = "spatiotemporal"  # Both space and time


class AlertLevel(Enum):
    """Alert severity levels"""
    INFORMATION = "information"
    ADVISORY = "advisory"
    WATCH = "watch"
    WARNING = "warning"
    CRITICAL = "critical"


class OutbreakStatus(Enum):
    """Outbreak investigation status"""
    POTENTIAL = "potential"
    CONFIRMED = "confirmed"
    UNDER_INVESTIGATION = "under_investigation"
    RULED_OUT = "ruled_out"
    CLOSED = "closed"


class DetectionMethod(Enum):
    """Detection algorithm used"""
    THRESHOLD = "threshold"  # Simple threshold
    MOVING_AVERAGE = "moving_average"  # Exceeds moving average
    CONTROL_CHART = "control_chart"  # Statistical process control
    SCAN_STATISTIC = "scan_statistic"  # Spatial scan statistic
    TEMPORAL_SCAN = "temporal_scan"  # Temporal scan
    SYNDROMIC = "syndromic"  # Syndromic surveillance


@dataclass
class GeoLocation:
    """Geographic location for spatial analysis"""
    location_id: str
    location_name: str
    latitude: float
    longitude: float
    population: int = 0
    zip_code: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None


@dataclass
class ClusterCase:
    """Case included in a cluster"""
    case_id: str
    patient_id: str
    disease_code: str
    onset_date: str
    location_id: str
    latitude: float
    longitude: float


@dataclass
class DetectedCluster:
    """Detected disease cluster"""
    cluster_id: str
    disease_code: str
    disease_name: str
    cluster_type: ClusterType

    # Cases in cluster
    case_ids: List[str]
    case_count: int

    # Spatial information
    center_latitude: Optional[float] = None
    center_longitude: Optional[float] = None
    radius_km: Optional[float] = None
    affected_locations: List[str] = field(default_factory=list)

    # Temporal information
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: Optional[int] = None

    # Statistical significance
    detection_method: DetectionMethod = DetectionMethod.THRESHOLD
    expected_cases: float = 0.0
    observed_cases: int = 0
    relative_risk: float = 1.0
    p_value: float = 1.0
    statistically_significant: bool = False

    # Metadata
    detected_date: str = field(default_factory=lambda: datetime.now().isoformat())
    alert_level: AlertLevel = AlertLevel.INFORMATION


@dataclass
class OutbreakAlert:
    """Alert for potential outbreak"""
    alert_id: str
    disease_code: str
    disease_name: str
    alert_level: AlertLevel

    # Alert details
    title: str
    description: str
    detected_method: DetectionMethod

    # Associated cluster (if any)
    cluster_id: Optional[str] = None

    # Cases
    case_count: int = 0
    case_ids: List[str] = field(default_factory=list)

    # Geographic scope
    affected_locations: List[str] = field(default_factory=list)
    affected_population: int = 0

    # Temporal scope
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    # Response
    investigation_required: bool = True
    response_actions: List[str] = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None


@dataclass
class OutbreakInvestigation:
    """Outbreak investigation record"""
    investigation_id: str
    outbreak_id: str
    disease_code: str
    disease_name: str

    # Investigation team
    lead_investigator_id: str
    lead_investigator_name: str
    team_members: List[str] = field(default_factory=list)

    # Status
    status: OutbreakStatus = OutbreakStatus.UNDER_INVESTIGATION

    # Findings
    confirmed_cases: int = 0
    probable_cases: int = 0
    suspected_cases: int = 0

    # Epidemiology
    attack_rate: Optional[float] = None
    population_at_risk: int = 0

    # Source identification
    suspected_source: Optional[str] = None
    source_confirmed: bool = False
    transmission_mode: Optional[str] = None

    # Response measures
    control_measures: List[str] = field(default_factory=list)
    public_communication: bool = False

    # Timeline
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    # Notes
    investigation_notes: str = ""


@dataclass
class BaselineData:
    """Historical baseline data for comparison"""
    disease_code: str
    location_id: str
    time_period: str  # "2024-01" for monthly, "2024-W01" for weekly
    case_count: int
    population: int
    incidence_rate: float  # Per 100,000 population


class OutbreakDetectionSystem:
    """
    Comprehensive outbreak detection and alert system

    Implements:
    - Spatial cluster detection
    - Temporal aberration detection
    - Threshold-based alerts
    - Statistical analysis
    - Outbreak investigation management
    """

    def __init__(self):
        self.locations: Dict[str, GeoLocation] = {}
        self.clusters: Dict[str, DetectedCluster] = {}
        self.alerts: Dict[str, OutbreakAlert] = {}
        self.investigations: Dict[str, OutbreakInvestigation] = {}
        self.baselines: List[BaselineData] = []

        # Alert thresholds (cases per 100,000 population)
        self.alert_thresholds = {
            "COVID-19": {"watch": 10, "warning": 50, "critical": 100},
            "Measles": {"watch": 1, "warning": 5, "critical": 10},
            "Salmonellosis": {"watch": 20, "warning": 50, "critical": 100},
            "default": {"watch": 10, "warning": 25, "critical": 50}
        }

    def register_location(self, location_id: str, location_name: str,
                         latitude: float, longitude: float, population: int,
                         **kwargs) -> str:
        """Register a geographic location for surveillance"""

        location = GeoLocation(
            location_id=location_id,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            population=population,
            **kwargs
        )

        self.locations[location_id] = location
        return location_id

    def add_baseline(self, disease_code: str, location_id: str,
                    time_period: str, case_count: int, population: int):
        """Add historical baseline data"""

        incidence_rate = (case_count / population) * 100000 if population > 0 else 0

        baseline = BaselineData(
            disease_code=disease_code,
            location_id=location_id,
            time_period=time_period,
            case_count=case_count,
            population=population,
            incidence_rate=incidence_rate
        )

        self.baselines.append(baseline)

    def calculate_distance_km(self, lat1: float, lon1: float,
                             lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""

        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def detect_spatial_clusters(self, cases: List[ClusterCase],
                               max_radius_km: float = 50,
                               min_cases: int = 3) -> List[DetectedCluster]:
        """
        Detect spatial clusters using a simplified scan statistic

        This is a simplified version of SaTScan spatial clustering
        """

        if len(cases) < min_cases:
            return []

        detected_clusters = []

        # Group cases by disease
        cases_by_disease = defaultdict(list)
        for case in cases:
            cases_by_disease[case.disease_code].append(case)

        for disease_code, disease_cases in cases_by_disease.items():
            if len(disease_cases) < min_cases:
                continue

            # Try each case as a potential cluster center
            for center_case in disease_cases:
                cluster_cases = []

                # Find all cases within radius
                for other_case in disease_cases:
                    distance = self.calculate_distance_km(
                        center_case.latitude, center_case.longitude,
                        other_case.latitude, other_case.longitude
                    )

                    if distance <= max_radius_km:
                        cluster_cases.append(other_case)

                # Check if this is a significant cluster
                if len(cluster_cases) >= min_cases:
                    # Calculate cluster statistics
                    avg_lat = sum(c.latitude for c in cluster_cases) / len(cluster_cases)
                    avg_lon = sum(c.longitude for c in cluster_cases) / len(cluster_cases)

                    # Calculate actual radius (distance from center to furthest case)
                    max_distance = max(
                        self.calculate_distance_km(avg_lat, avg_lon, c.latitude, c.longitude)
                        for c in cluster_cases
                    )

                    # Get disease name
                    disease_name = cluster_cases[0].disease_code  # Simplified

                    # Simple relative risk calculation
                    # (In real implementation, would use population at risk)
                    observed = len(cluster_cases)
                    expected = len(disease_cases) / max(len(self.locations), 1)
                    relative_risk = observed / expected if expected > 0 else observed

                    # Simple p-value (simplified - would use Poisson distribution in reality)
                    p_value = 1.0 / (relative_risk + 1)  # Simplified
                    significant = relative_risk > 2.0 and observed >= min_cases

                    cluster_id = f"CLUSTER-{uuid.uuid4().hex[:8].upper()}"

                    cluster = DetectedCluster(
                        cluster_id=cluster_id,
                        disease_code=disease_code,
                        disease_name=disease_name,
                        cluster_type=ClusterType.SPATIAL,
                        case_ids=[c.case_id for c in cluster_cases],
                        case_count=len(cluster_cases),
                        center_latitude=avg_lat,
                        center_longitude=avg_lon,
                        radius_km=max_distance,
                        affected_locations=list(set(c.location_id for c in cluster_cases)),
                        detection_method=DetectionMethod.SCAN_STATISTIC,
                        expected_cases=expected,
                        observed_cases=observed,
                        relative_risk=relative_risk,
                        p_value=p_value,
                        statistically_significant=significant,
                        alert_level=self._determine_alert_level(relative_risk, observed)
                    )

                    # Only add if not duplicate
                    if not self._is_duplicate_cluster(cluster, detected_clusters):
                        detected_clusters.append(cluster)
                        self.clusters[cluster_id] = cluster

        return detected_clusters

    def detect_temporal_clusters(self, cases: List[ClusterCase],
                                window_days: int = 7,
                                min_cases: int = 3) -> List[DetectedCluster]:
        """
        Detect temporal clusters (unusual increases over time)
        """

        if len(cases) < min_cases:
            return []

        detected_clusters = []

        # Group by disease
        cases_by_disease = defaultdict(list)
        for case in cases:
            cases_by_disease[case.disease_code].append(case)

        for disease_code, disease_cases in cases_by_disease.items():
            # Sort by onset date
            sorted_cases = sorted(disease_cases, key=lambda c: c.onset_date)

            # Sliding window
            for i in range(len(sorted_cases)):
                window_start = datetime.fromisoformat(sorted_cases[i].onset_date)
                window_end = window_start + timedelta(days=window_days)

                # Count cases in window
                window_cases = [
                    c for c in sorted_cases
                    if window_start <= datetime.fromisoformat(c.onset_date) < window_end
                ]

                if len(window_cases) >= min_cases:
                    # Calculate expected based on baseline
                    expected = self._get_expected_cases(disease_code, window_days)
                    observed = len(window_cases)
                    relative_risk = observed / expected if expected > 0 else observed

                    if relative_risk > 2.0:  # Threshold for significance
                        cluster_id = f"CLUSTER-{uuid.uuid4().hex[:8].upper()}"

                        cluster = DetectedCluster(
                            cluster_id=cluster_id,
                            disease_code=disease_code,
                            disease_name=disease_code,
                            cluster_type=ClusterType.TEMPORAL,
                            case_ids=[c.case_id for c in window_cases],
                            case_count=len(window_cases),
                            start_date=window_start.isoformat(),
                            end_date=window_end.isoformat(),
                            duration_days=window_days,
                            detection_method=DetectionMethod.TEMPORAL_SCAN,
                            expected_cases=expected,
                            observed_cases=observed,
                            relative_risk=relative_risk,
                            p_value=1.0 / (relative_risk + 1),  # Simplified
                            statistically_significant=True,
                            alert_level=self._determine_alert_level(relative_risk, observed)
                        )

                        if not self._is_duplicate_cluster(cluster, detected_clusters):
                            detected_clusters.append(cluster)
                            self.clusters[cluster_id] = cluster

        return detected_clusters

    def check_thresholds(self, disease_code: str, disease_name: str,
                        location_id: str, case_count: int) -> Optional[OutbreakAlert]:
        """Check if case count exceeds alert thresholds"""

        if location_id not in self.locations:
            return None

        location = self.locations[location_id]
        if location.population == 0:
            return None

        # Calculate incidence rate per 100,000
        incidence_rate = (case_count / location.population) * 100000

        # Get thresholds for this disease
        thresholds = self.alert_thresholds.get(
            disease_name,
            self.alert_thresholds["default"]
        )

        # Determine alert level
        alert_level = None
        if incidence_rate >= thresholds["critical"]:
            alert_level = AlertLevel.CRITICAL
        elif incidence_rate >= thresholds["warning"]:
            alert_level = AlertLevel.WARNING
        elif incidence_rate >= thresholds["watch"]:
            alert_level = AlertLevel.WATCH

        if alert_level:
            alert_id = f"ALERT-{uuid.uuid4().hex[:8].upper()}"

            alert = OutbreakAlert(
                alert_id=alert_id,
                disease_code=disease_code,
                disease_name=disease_name,
                alert_level=alert_level,
                title=f"{alert_level.value.upper()}: {disease_name} in {location.location_name}",
                description=f"{case_count} cases reported ({incidence_rate:.1f} per 100,000 population)",
                detected_method=DetectionMethod.THRESHOLD,
                case_count=case_count,
                affected_locations=[location_id],
                affected_population=location.population
            )

            self.alerts[alert_id] = alert
            return alert

        return None

    def create_alert_from_cluster(self, cluster: DetectedCluster) -> str:
        """Create an outbreak alert from a detected cluster"""

        alert_id = f"ALERT-{uuid.uuid4().hex[:8].upper()}"

        title = f"{cluster.alert_level.value.upper()}: {cluster.disease_name} cluster detected"
        description = (
            f"Detected {cluster.cluster_type.value} cluster with {cluster.case_count} cases. "
            f"Relative risk: {cluster.relative_risk:.2f}"
        )

        alert = OutbreakAlert(
            alert_id=alert_id,
            disease_code=cluster.disease_code,
            disease_name=cluster.disease_name,
            alert_level=cluster.alert_level,
            title=title,
            description=description,
            detected_method=cluster.detection_method,
            cluster_id=cluster.cluster_id,
            case_count=cluster.case_count,
            case_ids=cluster.case_ids,
            affected_locations=cluster.affected_locations,
            start_date=cluster.start_date,
            end_date=cluster.end_date,
            investigation_required=cluster.statistically_significant
        )

        self.alerts[alert_id] = alert
        return alert_id

    def initiate_investigation(self, outbreak_id: str, disease_code: str,
                              disease_name: str, lead_investigator_id: str,
                              lead_investigator_name: str,
                              population_at_risk: int = 0) -> str:
        """Initiate an outbreak investigation"""

        investigation_id = f"INV-{uuid.uuid4().hex[:8].upper()}"

        investigation = OutbreakInvestigation(
            investigation_id=investigation_id,
            outbreak_id=outbreak_id,
            disease_code=disease_code,
            disease_name=disease_name,
            lead_investigator_id=lead_investigator_id,
            lead_investigator_name=lead_investigator_name,
            population_at_risk=population_at_risk
        )

        self.investigations[investigation_id] = investigation
        return investigation_id

    def update_investigation(self, investigation_id: str,
                           confirmed_cases: int = None,
                           probable_cases: int = None,
                           suspected_cases: int = None,
                           status: OutbreakStatus = None,
                           **kwargs) -> bool:
        """Update outbreak investigation details"""

        if investigation_id not in self.investigations:
            return False

        investigation = self.investigations[investigation_id]

        if confirmed_cases is not None:
            investigation.confirmed_cases = confirmed_cases
        if probable_cases is not None:
            investigation.probable_cases = probable_cases
        if suspected_cases is not None:
            investigation.suspected_cases = suspected_cases
        if status is not None:
            investigation.status = status

        # Calculate attack rate
        total_cases = (investigation.confirmed_cases +
                      investigation.probable_cases +
                      investigation.suspected_cases)
        if investigation.population_at_risk > 0:
            investigation.attack_rate = (total_cases / investigation.population_at_risk) * 100

        for key, value in kwargs.items():
            if hasattr(investigation, key):
                setattr(investigation, key, value)

        return True

    def _determine_alert_level(self, relative_risk: float, case_count: int) -> AlertLevel:
        """Determine alert level based on risk and case count"""
        if relative_risk >= 5.0 or case_count >= 20:
            return AlertLevel.CRITICAL
        elif relative_risk >= 3.0 or case_count >= 10:
            return AlertLevel.WARNING
        elif relative_risk >= 2.0 or case_count >= 5:
            return AlertLevel.WATCH
        else:
            return AlertLevel.INFORMATION

    def _is_duplicate_cluster(self, new_cluster: DetectedCluster,
                             existing_clusters: List[DetectedCluster]) -> bool:
        """Check if cluster is duplicate (>80% overlap in cases)"""
        new_cases = set(new_cluster.case_ids)

        for existing in existing_clusters:
            existing_cases = set(existing.case_ids)
            overlap = len(new_cases.intersection(existing_cases))
            overlap_pct = overlap / len(new_cases) if len(new_cases) > 0 else 0

            if overlap_pct > 0.8:
                return True

        return False

    def _get_expected_cases(self, disease_code: str, days: int) -> float:
        """Get expected number of cases based on baseline (simplified)"""
        # In real implementation, would use historical data
        # For now, use simple average
        matching_baselines = [
            b for b in self.baselines
            if b.disease_code == disease_code
        ]

        if matching_baselines:
            avg_weekly = sum(b.case_count for b in matching_baselines) / len(matching_baselines)
            return (avg_weekly / 7) * days

        return 1.0  # Default baseline

    def get_active_alerts(self) -> List[OutbreakAlert]:
        """Get all unacknowledged alerts"""
        return [
            alert for alert in self.alerts.values()
            if not alert.acknowledged
        ]

    def get_critical_alerts(self) -> List[OutbreakAlert]:
        """Get critical level alerts"""
        return [
            alert for alert in self.alerts.values()
            if alert.alert_level == AlertLevel.CRITICAL
            and not alert.acknowledged
        ]

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        if alert_id not in self.alerts:
            return False

        alert = self.alerts[alert_id]
        alert.acknowledged = True
        alert.acknowledged_by = acknowledged_by
        return True

    def get_detection_summary(self) -> Dict:
        """Get outbreak detection summary statistics"""

        active_alerts = len(self.get_active_alerts())
        critical_alerts = len(self.get_critical_alerts())
        active_investigations = sum(
            1 for inv in self.investigations.values()
            if inv.status == OutbreakStatus.UNDER_INVESTIGATION
        )

        # Alerts by level
        alerts_by_level = defaultdict(int)
        for alert in self.alerts.values():
            alerts_by_level[alert.alert_level.value] += 1

        return {
            "total_clusters": len(self.clusters),
            "total_alerts": len(self.alerts),
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "active_investigations": active_investigations,
            "alerts_by_level": dict(alerts_by_level),
            "registered_locations": len(self.locations)
        }
