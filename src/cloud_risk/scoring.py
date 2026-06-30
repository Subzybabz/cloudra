"""
Cloud Migration Risk Scoring Algorithm
=======================================
Implements the three-dimensional risk scoring model specified in
Thesis Sections 3.5.1 – 3.5.3.

Formulas:
    O  = 0.30·N_D + 0.25·N_S + 0.30·N_A + 0.15·N_W
    F  = 0.45·N_C + 0.30·N_E + 0.25·N_T
    Cy = 0.35·N_Sens + 0.30·N_IAM + 0.20·N_Enc + 0.15·N_Comp
    C  = 0.35·O + 0.30·F + 0.35·Cy
"""

from __future__ import annotations

from .models import MigrationAssessmentInput, RiskAssessmentResult, RiskRecommendation


# ─── Cached Fallback Prices (hourly USD) ──────────────────────────────────────
# Used when the AWS Pricing API is unavailable.
# Prices: On-Demand, Linux, Shared Tenancy, US East (N. Virginia).
CACHED_FALLBACK_PRICES: dict[str, float] = {
    "EC2_SMALL": 0.0208,     # t3.small
    "EC2_MEDIUM": 0.0416,    # t3.medium
    "EC2_LARGE": 0.0832,     # t3.large
    "EC2_XLARGE": 0.1664,    # t3.xlarge
}

AVG_HOURS_PER_MONTH = 730


# ─── Utility Functions ────────────────────────────────────────────────────────

def clamp(value: float, lower: float = 0, upper: float = 100) -> float:
    """Clamp value to [lower, upper]."""
    return max(lower, min(upper, value))


def risk_tier(score: float) -> str:
    """Classify composite score into LOW / MEDIUM / HIGH (Section 3.5.2 Phase 4)."""
    if score < 40:
        return "LOW"
    if score < 70:
        return "MEDIUM"
    return "HIGH"


def get_cached_monthly_cost(resource_type: str) -> float:
    """Return a fallback monthly cost estimate for the given resource type."""
    hourly = CACHED_FALLBACK_PRICES.get(resource_type, 0.0416)
    return hourly * AVG_HOURS_PER_MONTH


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: PARAMETER NORMALISATION  (Section 3.5.2)
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Operational Parameters ───────────────────────────────────────────────────

def normalise_data_volume(data_volume_tb: float) -> float:
    """Piecewise linear: 3 segments at 10 TB, 50 TB inflection points."""
    if data_volume_tb < 10:
        nd = 10 + (data_volume_tb / 10) * 30           # range: 10–40
    elif data_volume_tb < 50:
        nd = 40 + ((data_volume_tb - 10) / 40) * 35    # range: 40–75
    else:
        nd = 75 + ((data_volume_tb - 50) / 50) * 25    # range: 75–100
    return clamp(nd)


def normalise_server_count(server_count: int) -> float:
    """Piecewise linear: 4 segments at 10, 50, 200 inflection points."""
    if server_count < 10:
        ns = (server_count / 10) * 25                       # range:  0–25
    elif server_count < 50:
        ns = 25 + ((server_count - 10) / 40) * 35          # range: 25–60
    elif server_count < 200:
        ns = 60 + ((server_count - 50) / 150) * 30         # range: 60–90
    else:
        ns = min(90 + (server_count - 200) / 100, 100)     # range: 90–100
    return clamp(ns)


APP_COMPLEXITY_LOOKUP: dict[str, float] = {
    "LOW": 20,
    "MEDIUM": 45,
    "HIGH": 70,
    "VERY_HIGH": 95,
}


def normalise_app_complexity(app_complexity: str) -> float:
    """Categorical lookup: LOW=20, MEDIUM=45, HIGH=70, VERY_HIGH=95."""
    return float(APP_COMPLEXITY_LOOKUP[app_complexity])


def normalise_migration_window(migration_window_hrs: int) -> float:
    """Inverse piecewise: shorter window → higher risk score."""
    if migration_window_hrs >= 72:
        nw = 10.0
    elif migration_window_hrs >= 24:
        nw = 10 + ((72 - migration_window_hrs) / 48) * 40      # range: 10–50
    elif migration_window_hrs >= 4:
        nw = 50 + ((24 - migration_window_hrs) / 20) * 40      # range: 50–90
    else:
        nw = min(90 + (4 - migration_window_hrs) * 2.5, 100)   # range: 90–100
    return clamp(nw)


# ─── Financial Parameters ─────────────────────────────────────────────────────

def normalise_monthly_cost(monthly_cost_usd: float) -> float:
    """Piecewise linear using 3 segments (Section 3.5.2 Phase 1B)."""
    if monthly_cost_usd < 500:
        nc = (monthly_cost_usd / 500) * 30                             # range:  0–30
    elif monthly_cost_usd < 5000:
        nc = 30 + ((monthly_cost_usd - 500) / 4500) * 40               # range: 30–70
    else:
        nc = min(70 + ((monthly_cost_usd - 5000) / 5000) * 30, 100)    # range: 70–100
    return clamp(nc)


def normalise_egress_volume(egress_volume_tb: float) -> float:
    """Linear: N_E = clamp((V / 10) × 80 + 10, 10, 100)."""
    return clamp((egress_volume_tb / 10) * 80 + 10, 10, 100)


def normalise_capex_opex_delta(monthly_cost_usd: float, capex_monthly_usd: float) -> float:
    """Relative cost delta: |cloud_cost − on_prem_cost| / max(on_prem_cost, 1) × 100."""
    delta = abs(monthly_cost_usd - capex_monthly_usd) / max(capex_monthly_usd, 1)
    return clamp(delta * 100)


# ─── Cybersecurity Parameters ─────────────────────────────────────────────────

DATA_SENSITIVITY_LOOKUP: dict[str, float] = {
    "PUBLIC": 10,
    "INTERNAL": 30,
    "CONFIDENTIAL": 65,
    "RESTRICTED": 95,
}

IAM_PERMISSIVENESS_LOOKUP: dict[str, float] = {
    "LEAST_PRIV": 10,
    "MODERATE": 35,
    "PERMISSIVE": 70,
    "WILDCARD": 98,
}

ENCRYPTION_POSTURE_LOOKUP: dict[str, float] = {
    "FULL": 5,
    "PARTIAL": 35,
    "TRANSIT_ONLY": 65,
    "NONE": 95,
}

COMPLIANCE_SCOPE_LOOKUP: dict[str, float] = {
    "NONE": 5,
    "SINGLE": 30,
    "MULTIPLE": 60,
    "CRITICAL": 90,
}


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: DIMENSIONAL SUB-SCORE COMPUTATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_operational_score(
    payload: MigrationAssessmentInput,
) -> tuple[float, dict[str, float]]:
    """O = 0.30·N_D + 0.25·N_S + 0.30·N_A + 0.15·N_W"""
    nd = normalise_data_volume(payload.data_volume_tb)
    ns = normalise_server_count(payload.server_count)
    na = normalise_app_complexity(payload.app_complexity)
    nw = normalise_migration_window(payload.migration_window_hrs)

    score = round(0.30 * nd + 0.25 * ns + 0.30 * na + 0.15 * nw, 2)
    params = {
        "Data Volume": nd,
        "Server Count": ns,
        "App Complexity": na,
        "Migration Window": nw,
    }
    return score, params


def calculate_financial_score(
    payload: MigrationAssessmentInput,
    monthly_cost_usd: float,
) -> tuple[float, dict[str, float]]:
    """F = 0.45·N_C + 0.30·N_E + 0.25·N_T"""
    nc = normalise_monthly_cost(monthly_cost_usd)
    ne = normalise_egress_volume(payload.egress_volume_tb)
    nt = normalise_capex_opex_delta(monthly_cost_usd, payload.capex_monthly_usd)

    score = round(0.45 * nc + 0.30 * ne + 0.25 * nt, 2)
    params = {
        "Monthly Cost": nc,
        "Data Egress": ne,
        "CapEx-OpEx Delta": nt,
    }
    return score, params


def calculate_cybersecurity_score(
    payload: MigrationAssessmentInput,
) -> tuple[float, dict[str, float]]:
    """Cy = 0.35·N_Sens + 0.30·N_IAM + 0.20·N_Enc + 0.15·N_Comp"""
    n_sens = float(DATA_SENSITIVITY_LOOKUP[payload.data_sensitivity])
    n_iam = float(IAM_PERMISSIVENESS_LOOKUP[payload.iam_permissiveness])
    n_enc = float(ENCRYPTION_POSTURE_LOOKUP[payload.encryption_posture])
    n_comp = float(COMPLIANCE_SCOPE_LOOKUP[payload.compliance_scope])

    score = round(0.35 * n_sens + 0.30 * n_iam + 0.20 * n_enc + 0.15 * n_comp, 2)
    params = {
        "Data Sensitivity": n_sens,
        "IAM Permissiveness": n_iam,
        "Encryption": n_enc,
        "Compliance Scope": n_comp,
    }
    return score, params


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: RECOMMENDATION ENGINE  (Section 3.5.2)
# ═══════════════════════════════════════════════════════════════════════════════

RECOMMENDATION_DETAILS: dict[str, str] = {
    "Data Volume": (
        "The data volume to migrate exceeds safe thresholds. Consider partitioning "
        "data into migration waves, implementing parallel transfer streams, and "
        "validating data integrity checksums at each stage."
    ),
    "Server Count": (
        "The number of servers to migrate introduces significant complexity. Map all "
        "inter-server dependencies, establish a phased migration schedule, and "
        "provision rollback capacity for each wave."
    ),
    "App Complexity": (
        "Application dependency complexity is elevated. Conduct a thorough dependency "
        "audit, refactor tightly coupled components where feasible, and perform "
        "integration testing in a staging environment before cutover."
    ),
    "Migration Window": (
        "The available maintenance window is restrictive. Negotiate extended downtime "
        "if possible, pre-stage data replication, and prepare automated rollback "
        "procedures to minimise cutover duration."
    ),
    "Monthly Cost": (
        "Projected monthly cloud costs are significant. Evaluate Reserved Instance or "
        "Savings Plan commitments, right-size instance selections, and implement cost "
        "anomaly alerts before migration."
    ),
    "Data Egress": (
        "Data egress volumes present material cost exposure. Architect workloads to "
        "minimise cross-region transfers, evaluate AWS Direct Connect for high-volume "
        "egress, and monitor egress billing closely."
    ),
    "CapEx-OpEx Delta": (
        "The transition from on-premise CapEx to cloud OpEx introduces significant "
        "budget variance. Model cloud costs against current on-premise expenditure "
        "over a 12-month horizon and secure budget approval for the projected delta."
    ),
    "Data Sensitivity": (
        "Data sensitivity classification warrants enhanced protection. Implement "
        "encryption at rest and in transit, enforce data loss prevention policies, "
        "and ensure compliance with applicable data residency requirements."
    ),
    "IAM Permissiveness": (
        "IAM policy permissiveness exceeds recommended thresholds. Apply the Principle "
        "of Least Privilege, eliminate wildcard permissions, and implement IAM Access "
        "Analyzer to detect overly broad policies."
    ),
    "Encryption": (
        "Encryption coverage is insufficient. Enable AWS KMS-managed encryption at "
        "rest for all storage services, enforce TLS 1.2+ for data in transit, and "
        "audit encryption configurations before migration."
    ),
    "Compliance Scope": (
        "The breadth of compliance obligations introduces governance risk. Map all "
        "applicable frameworks to AWS shared responsibility controls, prepare audit "
        "evidence documentation, and engage compliance stakeholders early."
    ),
}

PARAMETER_THRESHOLDS: dict[str, tuple[str, int]] = {
    "Data Volume":        ("Operational",    60),
    "Server Count":       ("Operational",    60),
    "App Complexity":     ("Operational",    60),
    "Migration Window":   ("Operational",    60),
    "Monthly Cost":       ("Financial",      55),
    "Data Egress":        ("Financial",      55),
    "CapEx-OpEx Delta":   ("Financial",      55),
    "Data Sensitivity":   ("Cybersecurity",  50),
    "IAM Permissiveness": ("Cybersecurity",  50),
    "Encryption":         ("Cybersecurity",  50),
    "Compliance Scope":   ("Cybersecurity",  50),
}

PRIORITY_ORDER = {"CRITICAL": 0, "IMPORTANT": 1, "ADVISORY": 2}


def build_recommendations(all_param_scores: dict[str, float]) -> list[RiskRecommendation]:
    """
    Generate recommendations for parameters exceeding their thresholds.

    Priority assignment (Section 3.5.2 Phase 5):
        score >= 80  →  CRITICAL
        score >= 60  →  IMPORTANT
        otherwise    →  ADVISORY

    Results are sorted by priority (desc) then score (desc), capped at 10.
    """
    recommendations: list[RiskRecommendation] = []

    for param_name, score in all_param_scores.items():
        dimension, thresh = PARAMETER_THRESHOLDS[param_name]
        if score > thresh:
            if score >= 80:
                priority = "CRITICAL"
            elif score >= 60:
                priority = "IMPORTANT"
            else:
                priority = "ADVISORY"

            recommendations.append(
                RiskRecommendation(
                    parameter=param_name,
                    dimension=dimension,
                    detail=RECOMMENDATION_DETAILS[param_name],
                    priority=priority,
                    score=round(score, 2),
                )
            )

    recommendations.sort(key=lambda r: (PRIORITY_ORDER[r.priority], -r.score))
    return recommendations[:10]


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_input(payload: MigrationAssessmentInput) -> None:
    """Validate all input constraints before scoring."""
    if payload.data_volume_tb < 0:
        raise ValueError("data_volume_tb cannot be negative")
    if payload.server_count < 0:
        raise ValueError("server_count cannot be negative")
    if payload.migration_window_hrs < 0:
        raise ValueError("migration_window_hrs cannot be negative")
    if payload.egress_volume_tb < 0:
        raise ValueError("egress_volume_tb cannot be negative")
    if payload.capex_monthly_usd < 0:
        raise ValueError("capex_monthly_usd cannot be negative")
    if payload.projected_users < 0:
        raise ValueError("projected_users cannot be negative")

    if payload.app_complexity not in APP_COMPLEXITY_LOOKUP:
        raise ValueError(f"Invalid app_complexity: {payload.app_complexity}")
    if payload.data_sensitivity not in DATA_SENSITIVITY_LOOKUP:
        raise ValueError(f"Invalid data_sensitivity: {payload.data_sensitivity}")
    if payload.iam_permissiveness not in IAM_PERMISSIVENESS_LOOKUP:
        raise ValueError(f"Invalid iam_permissiveness: {payload.iam_permissiveness}")
    if payload.encryption_posture not in ENCRYPTION_POSTURE_LOOKUP:
        raise ValueError(f"Invalid encryption_posture: {payload.encryption_posture}")
    if payload.compliance_scope not in COMPLIANCE_SCOPE_LOOKUP:
        raise ValueError(f"Invalid compliance_scope: {payload.compliance_scope}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ASSESSMENT FUNCTION  (Section 3.5.2 – Full Algorithm)
# ═══════════════════════════════════════════════════════════════════════════════

def assess_migration_risk(
    payload: MigrationAssessmentInput,
    monthly_cost_usd: float | None = None,
    live_price_used: bool = False,
) -> RiskAssessmentResult:
    """
    Execute the complete CloudMigrationRiskScoring algorithm.

    Parameters
    ----------
    payload : MigrationAssessmentInput
        The migration parameters P.
    monthly_cost_usd : float, optional
        The projected monthly cloud cost derived from pricing queries.
        If None, the cached fallback price is used.
    live_price_used : bool
        Whether the cost was obtained from a live AWS Pricing API call.
    """
    validate_input(payload)

    # If no external price provided, use cached fallback
    if monthly_cost_usd is None:
        monthly_cost_usd = get_cached_monthly_cost(payload.resource_type)
        live_price_used = False

    # Phase 2: Dimensional sub-scores
    operational_score, op_params = calculate_operational_score(payload)
    financial_score, fin_params = calculate_financial_score(payload, monthly_cost_usd)
    cybersec_score, cyber_params = calculate_cybersecurity_score(payload)

    # Phase 3: Composite score
    composite_score = round(
        0.35 * operational_score + 0.30 * financial_score + 0.35 * cybersec_score, 2
    )

    # Phase 4: Risk tier classification
    tier = risk_tier(composite_score)

    # Phase 5: Recommendation engine
    all_params = {**op_params, **fin_params, **cyber_params}
    recommendations = build_recommendations(all_params)

    return RiskAssessmentResult(
        project_name=payload.project_name,
        composite_score=composite_score,
        operational_score=operational_score,
        financial_score=financial_score,
        cybersec_score=cybersec_score,
        risk_tier=tier,
        live_price_used=live_price_used,
        monthly_est_usd=round(monthly_cost_usd, 2),
        recommendations=recommendations,
    )
