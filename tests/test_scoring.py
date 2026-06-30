import pytest

from cloud_risk.models import MigrationAssessmentInput
from cloud_risk.scoring import (
    assess_migration_risk,
    risk_tier,
    normalise_data_volume,
    normalise_server_count,
    normalise_app_complexity,
    normalise_migration_window,
    normalise_monthly_cost,
    normalise_egress_volume,
    normalise_capex_opex_delta,
    clamp,
)


def make_payload(**overrides):
    """Low-risk default profile for testing."""
    defaults = {
        "project_name": "Test Migration",
        "data_volume_tb": 5.0,
        "server_count": 8,
        "app_complexity": "LOW",
        "migration_window_hrs": 48,
        "resource_type": "EC2_SMALL",
        "target_region": "eu-west-1",
        "egress_volume_tb": 1.0,
        "capex_monthly_usd": 2000.0,
        "projected_users": 100,
        "data_sensitivity": "INTERNAL",
        "iam_permissiveness": "LEAST_PRIV",
        "encryption_posture": "FULL",
        "compliance_scope": "NONE",
    }
    defaults.update(overrides)
    return MigrationAssessmentInput(**defaults)


# ─── End-to-End Scoring Tests ─────────────────────────────────────────────────

def test_low_risk_profile_scores_low():
    result = assess_migration_risk(make_payload())
    assert result.risk_tier == "LOW"
    assert result.composite_score < 40


def test_high_risk_profile_scores_high():
    result = assess_migration_risk(
        make_payload(
            data_volume_tb=80.0,
            server_count=250,
            app_complexity="VERY_HIGH",
            migration_window_hrs=2,
            egress_volume_tb=12.0,
            capex_monthly_usd=500.0,
            data_sensitivity="RESTRICTED",
            iam_permissiveness="WILDCARD",
            encryption_posture="NONE",
            compliance_scope="CRITICAL",
        ),
        monthly_cost_usd=8000.0,
    )
    assert result.risk_tier == "HIGH"
    assert result.composite_score >= 70
    dims = {r.dimension for r in result.recommendations}
    assert dims >= {"Operational", "Financial", "Cybersecurity"}


def test_result_includes_thesis_fields():
    result = assess_migration_risk(make_payload())
    assert hasattr(result, "cybersec_score")
    assert hasattr(result, "live_price_used")
    assert hasattr(result, "monthly_est_usd")
    assert result.live_price_used is False  # Phase 1: always cached


# ─── Risk Tier Boundaries ────────────────────────────────────────────────────

@pytest.mark.parametrize(
    ("score", "expected"),
    [(0, "LOW"), (39.99, "LOW"), (40, "MEDIUM"), (69.99, "MEDIUM"), (70, "HIGH")],
)
def test_risk_tier_boundaries(score, expected):
    assert risk_tier(score) == expected


# ─── Normalisation Unit Tests ─────────────────────────────────────────────────

def test_normalise_data_volume_segment_1():
    # 5 TB: 10 + (5/10)*30 = 25.0
    assert normalise_data_volume(5.0) == pytest.approx(25.0)


def test_normalise_data_volume_segment_2():
    # 30 TB: 40 + ((30-10)/40)*35 = 57.5
    assert normalise_data_volume(30.0) == pytest.approx(57.5)


def test_normalise_data_volume_segment_3():
    # 60 TB: 75 + ((60-50)/50)*25 = 80.0
    assert normalise_data_volume(60.0) == pytest.approx(80.0)


def test_normalise_server_count_segment_1():
    # 5 servers: (5/10)*25 = 12.5
    assert normalise_server_count(5) == pytest.approx(12.5)


def test_normalise_server_count_segment_2():
    # 30 servers: 25 + ((30-10)/40)*35 = 42.5
    assert normalise_server_count(30) == pytest.approx(42.5)


def test_normalise_server_count_segment_3():
    # 100 servers: 60 + ((100-50)/150)*30 = 70.0
    assert normalise_server_count(100) == pytest.approx(70.0)


def test_normalise_app_complexity_lookup():
    assert normalise_app_complexity("LOW") == 20
    assert normalise_app_complexity("MEDIUM") == 45
    assert normalise_app_complexity("HIGH") == 70
    assert normalise_app_complexity("VERY_HIGH") == 95


def test_normalise_migration_window_wide():
    assert normalise_migration_window(72) == pytest.approx(10.0)
    assert normalise_migration_window(100) == pytest.approx(10.0)


def test_normalise_migration_window_24hrs():
    # Exactly 24: 10 + ((72-24)/48)*40 = 10 + 40 = 50.0
    assert normalise_migration_window(24) == pytest.approx(50.0)


def test_normalise_migration_window_tight():
    # 4 hrs: 50 + ((24-4)/20)*40 = 90.0
    assert normalise_migration_window(4) == pytest.approx(90.0)


def test_normalise_monthly_cost_low():
    # $100: (100/500)*30 = 6.0
    assert normalise_monthly_cost(100.0) == pytest.approx(6.0)


def test_normalise_monthly_cost_mid():
    # $2750: 30 + ((2750-500)/4500)*40 = 50.0
    assert normalise_monthly_cost(2750.0) == pytest.approx(50.0)


def test_normalise_egress_volume():
    # 5 TB: (5/10)*80 + 10 = 50.0
    assert normalise_egress_volume(5.0) == pytest.approx(50.0)


def test_normalise_capex_opex_delta():
    # cloud=3000, capex=2000: |3000-2000|/2000 = 0.5 → 50
    assert normalise_capex_opex_delta(3000.0, 2000.0) == pytest.approx(50.0)


# ─── Recommendation Engine Tests ─────────────────────────────────────────────

def test_recommendations_sorted_by_priority():
    result = assess_migration_risk(
        make_payload(
            data_volume_tb=80.0,
            server_count=250,
            app_complexity="VERY_HIGH",
            migration_window_hrs=2,
            data_sensitivity="RESTRICTED",
            iam_permissiveness="WILDCARD",
            encryption_posture="NONE",
            compliance_scope="CRITICAL",
        ),
        monthly_cost_usd=8000.0,
    )
    priorities = [r.priority for r in result.recommendations]
    seen = set()
    for p in priorities:
        if p == "ADVISORY":
            seen.add("ADVISORY")
        elif p == "IMPORTANT":
            assert "ADVISORY" not in seen, "IMPORTANT must precede ADVISORY"
            seen.add("IMPORTANT")
        elif p == "CRITICAL":
            assert "IMPORTANT" not in seen and "ADVISORY" not in seen


def test_recommendations_capped_at_10():
    result = assess_migration_risk(
        make_payload(
            data_volume_tb=80.0,
            server_count=250,
            app_complexity="VERY_HIGH",
            migration_window_hrs=2,
            egress_volume_tb=12.0,
            capex_monthly_usd=500.0,
            data_sensitivity="RESTRICTED",
            iam_permissiveness="WILDCARD",
            encryption_posture="NONE",
            compliance_scope="CRITICAL",
        ),
        monthly_cost_usd=8000.0,
    )
    assert len(result.recommendations) <= 10


# ─── Validation Tests ─────────────────────────────────────────────────────────

def test_rejects_negative_data_volume():
    with pytest.raises(ValueError, match="data_volume_tb"):
        assess_migration_risk(make_payload(data_volume_tb=-1))


def test_rejects_negative_server_count():
    with pytest.raises(ValueError, match="server_count"):
        assess_migration_risk(make_payload(server_count=-1))


def test_rejects_invalid_app_complexity():
    with pytest.raises(ValueError, match="app_complexity"):
        assess_migration_risk(make_payload(app_complexity="INVALID"))
