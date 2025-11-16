"""
Public Health Analytics
Advanced analytics, trend analysis, and risk assessment

Features:
- Disease trend analysis
- Risk assessment and stratification
- Population health metrics
- Health equity analysis
- Predictive analytics
- Dashboard and visualization data
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import uuid
import statistics


class TrendDirection(Enum):
    """Trend direction"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    UNKNOWN = "unknown"


class RiskLevel(Enum):
    """Population risk level"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AgeGroup(Enum):
    """Standard age groups for analysis"""
    INFANT = "0-1"  # 0-1 years
    TODDLER = "1-4"  # 1-4 years
    CHILD = "5-14"  # 5-14 years
    YOUNG_ADULT = "15-24"  # 15-24 years
    ADULT = "25-44"  # 25-44 years
    MIDDLE_AGE = "45-64"  # 45-64 years
    SENIOR = "65+"  # 65+ years


class HealthEquityDimension(Enum):
    """Dimensions for health equity analysis"""
    RACE = "race"
    ETHNICITY = "ethnicity"
    INCOME = "income"
    EDUCATION = "education"
    GEOGRAPHY = "geography"  # urban/rural
    LANGUAGE = "language"
    INSURANCE_STATUS = "insurance_status"


@dataclass
class TimeSeriesDataPoint:
    """Single data point in time series"""
    date: str
    value: float
    count: int = 0
    denominator: int = 0  # For rate calculations


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    analysis_id: str
    disease_code: str
    disease_name: str
    location_id: Optional[str] = None

    # Time period
    start_date: str = ""
    end_date: str = ""
    data_points: int = 0

    # Trend
    trend_direction: TrendDirection = TrendDirection.UNKNOWN
    percent_change: float = 0.0
    average_daily_cases: float = 0.0
    peak_date: Optional[str] = None
    peak_value: float = 0.0

    # Statistical
    moving_average_7day: Optional[float] = None
    moving_average_14day: Optional[float] = None
    doubling_time_days: Optional[float] = None  # For exponential growth

    # Time series data
    time_series: List[TimeSeriesDataPoint] = field(default_factory=list)

    # Analysis date
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RiskAssessment:
    """Population risk assessment"""
    assessment_id: str
    disease_code: str
    disease_name: str
    location_id: str
    location_name: str

    # Risk level
    overall_risk: RiskLevel = RiskLevel.LOW

    # Risk factors
    current_incidence_rate: float = 0.0  # per 100,000
    baseline_incidence_rate: float = 0.0
    incidence_ratio: float = 1.0  # current / baseline

    # Trends
    trend_direction: TrendDirection = TrendDirection.STABLE
    week_over_week_change: float = 0.0

    # Population impact
    population_at_risk: int = 0
    estimated_cases_next_week: int = 0

    # Healthcare capacity
    hospitalization_rate: float = 0.0  # % of cases
    estimated_hospitalizations: int = 0
    icu_rate: float = 0.0
    estimated_icu_admissions: int = 0

    # Vulnerability factors
    vulnerable_populations: List[str] = field(default_factory=list)
    comorbidity_prevalence: float = 0.0

    # Recommendations
    risk_factors: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)

    # Assessment date
    assessed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PopulationHealthMetric:
    """Population health metric"""
    metric_id: str
    metric_name: str
    metric_type: str  # incidence, prevalence, mortality, etc.

    # Geographic scope
    location_id: str
    location_name: str
    population: int

    # Time period
    period_start: str
    period_end: str

    # Metric values
    numerator: int  # Cases, deaths, etc.
    denominator: int  # Population at risk
    rate: float = 0.0  # Per 100,000 or other base
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None

    # Comparisons
    state_rate: Optional[float] = None
    national_rate: Optional[float] = None
    compared_to_state: Optional[str] = None  # "higher", "similar", "lower"
    compared_to_national: Optional[str] = None

    # Stratification
    stratified_by: Optional[str] = None  # age, race, etc.
    stratified_values: Dict[str, float] = field(default_factory=dict)


@dataclass
class HealthEquityAnalysis:
    """Health equity analysis"""
    analysis_id: str
    disease_code: str
    disease_name: str
    dimension: HealthEquityDimension

    # Time period
    period_start: str
    period_end: str

    # Group comparisons
    group_rates: Dict[str, float] = field(default_factory=dict)  # Group -> rate per 100K
    group_counts: Dict[str, int] = field(default_factory=dict)  # Group -> case count

    # Disparity measures
    highest_rate_group: str = ""
    lowest_rate_group: str = ""
    rate_ratio: float = 1.0  # highest / lowest
    rate_difference: float = 0.0  # highest - lowest

    # Statistical significance
    statistically_significant: bool = False
    p_value: Optional[float] = None

    # Interpretation
    disparity_level: str = "none"  # none, minimal, moderate, substantial
    affected_groups: List[str] = field(default_factory=list)
    priority_populations: List[str] = field(default_factory=list)

    # Analyzed date
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DashboardMetrics:
    """Dashboard summary metrics"""
    dashboard_id: str
    dashboard_name: str

    # Time period
    period_start: str
    period_end: str

    # Overall statistics
    total_cases: int = 0
    new_cases_today: int = 0
    new_cases_this_week: int = 0

    # Trends
    week_over_week_change: float = 0.0
    trend_direction: TrendDirection = TrendDirection.STABLE

    # Top diseases
    top_diseases: List[Dict[str, any]] = field(default_factory=list)

    # Geographic distribution
    top_locations: List[Dict[str, any]] = field(default_factory=list)

    # Alerts and outbreaks
    active_alerts: int = 0
    critical_alerts: int = 0
    active_outbreaks: int = 0

    # Healthcare impact
    total_hospitalizations: int = 0
    total_deaths: int = 0

    # System metrics
    investigations_active: int = 0
    investigations_completed: int = 0
    reports_submitted_this_week: int = 0

    # Updated timestamp
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class PublicHealthAnalytics:
    """
    Comprehensive public health analytics system

    Provides:
    - Disease trend analysis
    - Population risk assessment
    - Health equity analysis
    - Population health metrics
    - Dashboard data generation
    """

    def __init__(self):
        self.trend_analyses: Dict[str, TrendAnalysis] = {}
        self.risk_assessments: Dict[str, RiskAssessment] = {}
        self.health_metrics: Dict[str, PopulationHealthMetric] = {}
        self.equity_analyses: Dict[str, HealthEquityAnalysis] = {}
        self.dashboards: Dict[str, DashboardMetrics] = {}

        # Population data (would come from census in real system)
        self.population_data: Dict[str, int] = {}

        # Baseline rates
        self.baseline_rates: Dict[Tuple[str, str], float] = {}  # (disease, location) -> rate

    def register_population(self, location_id: str, population: int):
        """Register population for a location"""
        self.population_data[location_id] = population

    def set_baseline_rate(self, disease_code: str, location_id: str, rate: float):
        """Set baseline incidence rate for comparison"""
        self.baseline_rates[(disease_code, location_id)] = rate

    def analyze_trend(self, disease_code: str, disease_name: str,
                     time_series_data: List[Tuple[str, int]],
                     location_id: Optional[str] = None) -> str:
        """
        Analyze disease trends over time

        Args:
            disease_code: Disease code
            disease_name: Disease name
            time_series_data: List of (date, case_count) tuples
            location_id: Optional location identifier

        Returns:
            analysis_id
        """

        analysis_id = f"TREND-{uuid.uuid4().hex[:8].upper()}"

        if not time_series_data:
            return analysis_id

        # Convert to TimeSeriesDataPoint objects
        data_points = [
            TimeSeriesDataPoint(date=date, value=count, count=count)
            for date, count in time_series_data
        ]

        # Sort by date
        data_points.sort(key=lambda d: d.date)

        # Calculate statistics
        values = [d.value for d in data_points]
        dates = [d.date for d in data_points]

        # Find peak
        peak_value = max(values) if values else 0
        peak_index = values.index(peak_value) if values else 0
        peak_date = dates[peak_index] if dates else None

        # Average daily cases
        avg_daily = statistics.mean(values) if values else 0

        # Trend direction (compare first half to second half)
        mid_point = len(values) // 2
        if mid_point > 0:
            first_half_avg = statistics.mean(values[:mid_point])
            second_half_avg = statistics.mean(values[mid_point:])

            if second_half_avg > first_half_avg * 1.1:
                trend_direction = TrendDirection.INCREASING
            elif second_half_avg < first_half_avg * 0.9:
                trend_direction = TrendDirection.DECREASING
            else:
                trend_direction = TrendDirection.STABLE

            percent_change = ((second_half_avg - first_half_avg) / first_half_avg * 100
                            if first_half_avg > 0 else 0)
        else:
            trend_direction = TrendDirection.UNKNOWN
            percent_change = 0.0

        # Calculate moving averages
        ma_7day = None
        ma_14day = None

        if len(values) >= 7:
            ma_7day = statistics.mean(values[-7:])

        if len(values) >= 14:
            ma_14day = statistics.mean(values[-14:])

        # Estimate doubling time (for exponential growth)
        doubling_time = None
        if trend_direction == TrendDirection.INCREASING and len(values) >= 7:
            recent_growth = (values[-1] / values[-7]) if values[-7] > 0 else 0
            if recent_growth > 1:
                daily_growth_rate = recent_growth ** (1/7)
                if daily_growth_rate > 1:
                    doubling_time = 1 / (daily_growth_rate - 1) if daily_growth_rate > 1 else None

        analysis = TrendAnalysis(
            analysis_id=analysis_id,
            disease_code=disease_code,
            disease_name=disease_name,
            location_id=location_id,
            start_date=dates[0] if dates else "",
            end_date=dates[-1] if dates else "",
            data_points=len(data_points),
            trend_direction=trend_direction,
            percent_change=percent_change,
            average_daily_cases=avg_daily,
            peak_date=peak_date,
            peak_value=peak_value,
            moving_average_7day=ma_7day,
            moving_average_14day=ma_14day,
            doubling_time_days=doubling_time,
            time_series=data_points
        )

        self.trend_analyses[analysis_id] = analysis
        return analysis_id

    def assess_risk(self, disease_code: str, disease_name: str,
                   location_id: str, location_name: str,
                   current_cases: int, baseline_cases: int,
                   week_over_week_change_pct: float = 0.0,
                   hospitalization_rate: float = 0.0,
                   icu_rate: float = 0.0,
                   **kwargs) -> str:
        """
        Assess population risk level

        Args:
            disease_code: Disease code
            disease_name: Disease name
            location_id: Location identifier
            location_name: Location name
            current_cases: Current case count
            baseline_cases: Baseline/expected case count
            week_over_week_change_pct: Week-over-week percent change
            hospitalization_rate: Percent of cases hospitalized
            icu_rate: Percent of cases requiring ICU

        Returns:
            assessment_id
        """

        assessment_id = f"RISK-{uuid.uuid4().hex[:8].upper()}"

        # Get population
        population = self.population_data.get(location_id, 100000)

        # Calculate rates
        current_rate = (current_cases / population) * 100000
        baseline_rate = (baseline_cases / population) * 100000
        incidence_ratio = current_rate / baseline_rate if baseline_rate > 0 else 1.0

        # Determine trend
        if week_over_week_change_pct > 10:
            trend_direction = TrendDirection.INCREASING
        elif week_over_week_change_pct < -10:
            trend_direction = TrendDirection.DECREASING
        else:
            trend_direction = TrendDirection.STABLE

        # Determine overall risk level
        risk_score = 0

        # Factor 1: Incidence ratio
        if incidence_ratio >= 3.0:
            risk_score += 3
        elif incidence_ratio >= 2.0:
            risk_score += 2
        elif incidence_ratio >= 1.5:
            risk_score += 1

        # Factor 2: Trend
        if trend_direction == TrendDirection.INCREASING:
            risk_score += 2
        elif trend_direction == TrendDirection.STABLE:
            risk_score += 1

        # Factor 3: Case count
        if current_cases >= 100:
            risk_score += 2
        elif current_cases >= 50:
            risk_score += 1

        # Determine risk level
        if risk_score >= 6:
            overall_risk = RiskLevel.VERY_HIGH
        elif risk_score >= 4:
            overall_risk = RiskLevel.HIGH
        elif risk_score >= 2:
            overall_risk = RiskLevel.MODERATE
        else:
            overall_risk = RiskLevel.LOW

        # Estimate next week cases (simple projection)
        growth_factor = 1 + (week_over_week_change_pct / 100)
        estimated_next_week = int(current_cases * growth_factor)

        # Estimate healthcare impact
        estimated_hospitalizations = int(current_cases * (hospitalization_rate / 100))
        estimated_icu = int(current_cases * (icu_rate / 100))

        # Generate recommendations
        recommended_actions = []
        risk_factors = []

        if overall_risk in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]:
            recommended_actions.append("Increase surveillance activities")
            recommended_actions.append("Consider public health advisory")
            risk_factors.append("High incidence rate")

        if trend_direction == TrendDirection.INCREASING:
            recommended_actions.append("Monitor trend closely")
            recommended_actions.append("Prepare outbreak response")
            risk_factors.append("Increasing trend")

        if estimated_hospitalizations > 10:
            recommended_actions.append("Alert healthcare facilities")
            risk_factors.append("Significant healthcare burden")

        assessment = RiskAssessment(
            assessment_id=assessment_id,
            disease_code=disease_code,
            disease_name=disease_name,
            location_id=location_id,
            location_name=location_name,
            overall_risk=overall_risk,
            current_incidence_rate=current_rate,
            baseline_incidence_rate=baseline_rate,
            incidence_ratio=incidence_ratio,
            trend_direction=trend_direction,
            week_over_week_change=week_over_week_change_pct,
            population_at_risk=population,
            estimated_cases_next_week=estimated_next_week,
            hospitalization_rate=hospitalization_rate,
            estimated_hospitalizations=estimated_hospitalizations,
            icu_rate=icu_rate,
            estimated_icu_admissions=estimated_icu,
            risk_factors=risk_factors,
            recommended_actions=recommended_actions,
            **kwargs
        )

        self.risk_assessments[assessment_id] = assessment
        return assessment_id

    def analyze_health_equity(self, disease_code: str, disease_name: str,
                             dimension: HealthEquityDimension,
                             group_data: Dict[str, Tuple[int, int]],
                             period_start: str, period_end: str) -> str:
        """
        Analyze health equity across population groups

        Args:
            disease_code: Disease code
            disease_name: Disease name
            dimension: Equity dimension (race, income, etc.)
            group_data: Dict of group_name -> (case_count, population)
            period_start: Period start date
            period_end: Period end date

        Returns:
            analysis_id
        """

        analysis_id = f"EQUITY-{uuid.uuid4().hex[:8].upper()}"

        # Calculate rates per 100,000 for each group
        group_rates = {}
        group_counts = {}

        for group_name, (cases, population) in group_data.items():
            if population > 0:
                rate = (cases / population) * 100000
                group_rates[group_name] = rate
                group_counts[group_name] = cases

        if not group_rates:
            return analysis_id

        # Find highest and lowest
        highest_rate_group = max(group_rates, key=group_rates.get)
        lowest_rate_group = min(group_rates, key=group_rates.get)

        highest_rate = group_rates[highest_rate_group]
        lowest_rate = group_rates[lowest_rate_group]

        # Calculate disparity measures
        rate_ratio = highest_rate / lowest_rate if lowest_rate > 0 else 0
        rate_difference = highest_rate - lowest_rate

        # Determine disparity level
        if rate_ratio >= 3.0:
            disparity_level = "substantial"
        elif rate_ratio >= 2.0:
            disparity_level = "moderate"
        elif rate_ratio >= 1.5:
            disparity_level = "minimal"
        else:
            disparity_level = "none"

        # Identify affected groups (those above average)
        avg_rate = statistics.mean(group_rates.values())
        affected_groups = [
            group for group, rate in group_rates.items()
            if rate > avg_rate
        ]

        # Priority populations (highest rates)
        sorted_groups = sorted(group_rates.items(), key=lambda x: x[1], reverse=True)
        priority_populations = [g[0] for g in sorted_groups[:3]]  # Top 3

        # Simple significance test (would use chi-square in real implementation)
        statistically_significant = rate_ratio >= 2.0

        analysis = HealthEquityAnalysis(
            analysis_id=analysis_id,
            disease_code=disease_code,
            disease_name=disease_name,
            dimension=dimension,
            period_start=period_start,
            period_end=period_end,
            group_rates=group_rates,
            group_counts=group_counts,
            highest_rate_group=highest_rate_group,
            lowest_rate_group=lowest_rate_group,
            rate_ratio=rate_ratio,
            rate_difference=rate_difference,
            statistically_significant=statistically_significant,
            disparity_level=disparity_level,
            affected_groups=affected_groups,
            priority_populations=priority_populations
        )

        self.equity_analyses[analysis_id] = analysis
        return analysis_id

    def generate_dashboard_metrics(self, dashboard_name: str,
                                   period_start: str, period_end: str,
                                   case_data: Dict[str, int],
                                   **kwargs) -> str:
        """
        Generate dashboard summary metrics

        Args:
            dashboard_name: Dashboard name
            period_start: Period start date
            period_end: Period end date
            case_data: Dict with case statistics

        Returns:
            dashboard_id
        """

        dashboard_id = f"DASH-{uuid.uuid4().hex[:8].upper()}"

        dashboard = DashboardMetrics(
            dashboard_id=dashboard_id,
            dashboard_name=dashboard_name,
            period_start=period_start,
            period_end=period_end,
            total_cases=case_data.get("total_cases", 0),
            new_cases_today=case_data.get("new_cases_today", 0),
            new_cases_this_week=case_data.get("new_cases_this_week", 0),
            week_over_week_change=case_data.get("week_over_week_change", 0.0),
            trend_direction=case_data.get("trend_direction", TrendDirection.STABLE),
            active_alerts=case_data.get("active_alerts", 0),
            critical_alerts=case_data.get("critical_alerts", 0),
            active_outbreaks=case_data.get("active_outbreaks", 0),
            total_hospitalizations=case_data.get("total_hospitalizations", 0),
            total_deaths=case_data.get("total_deaths", 0),
            investigations_active=case_data.get("investigations_active", 0),
            investigations_completed=case_data.get("investigations_completed", 0),
            reports_submitted_this_week=case_data.get("reports_submitted_this_week", 0),
            **{k: v for k, v in kwargs.items() if k not in case_data}
        )

        self.dashboards[dashboard_id] = dashboard
        return dashboard_id

    def get_analytics_summary(self) -> Dict:
        """Get analytics system summary statistics"""

        high_risk_assessments = sum(
            1 for assessment in self.risk_assessments.values()
            if assessment.overall_risk in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]
        )

        substantial_disparities = sum(
            1 for analysis in self.equity_analyses.values()
            if analysis.disparity_level == "substantial"
        )

        increasing_trends = sum(
            1 for trend in self.trend_analyses.values()
            if trend.trend_direction == TrendDirection.INCREASING
        )

        return {
            "trend_analyses": len(self.trend_analyses),
            "risk_assessments": len(self.risk_assessments),
            "high_risk_areas": high_risk_assessments,
            "health_equity_analyses": len(self.equity_analyses),
            "substantial_disparities": substantial_disparities,
            "population_health_metrics": len(self.health_metrics),
            "dashboards": len(self.dashboards),
            "increasing_trends": increasing_trends,
            "registered_populations": len(self.population_data)
        }
