from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import MigrationAssessmentInput, RiskAssessmentResult


REQUIRED_FIELDS = {
    "project_name",
    "data_volume_tb",
    "server_count",
    "app_complexity",
    "migration_window_hrs",
    "resource_type",
    "target_region",
    "egress_volume_tb",
    "capex_monthly_usd",
    "projected_users",
    "data_sensitivity",
    "iam_permissiveness",
    "encryption_posture",
    "compliance_scope",
}


def input_from_dict(data: dict[str, Any]) -> MigrationAssessmentInput:
    """Convert an incoming JSON dict into a validated MigrationAssessmentInput."""
    missing_fields = sorted(REQUIRED_FIELDS - set(data))
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    return MigrationAssessmentInput(
        project_name=str(data["project_name"]).strip(),
        data_volume_tb=float(data["data_volume_tb"]),
        server_count=int(data["server_count"]),
        app_complexity=str(data["app_complexity"]).strip().upper(),
        migration_window_hrs=int(data["migration_window_hrs"]),
        resource_type=str(data["resource_type"]).strip().upper(),
        target_region=str(data["target_region"]).strip(),
        egress_volume_tb=float(data["egress_volume_tb"]),
        capex_monthly_usd=float(data["capex_monthly_usd"]),
        projected_users=int(data["projected_users"]),
        data_sensitivity=str(data["data_sensitivity"]).strip().upper(),
        iam_permissiveness=str(data["iam_permissiveness"]).strip().upper(),
        encryption_posture=str(data["encryption_posture"]).strip().upper(),
        compliance_scope=str(data["compliance_scope"]).strip().upper(),
    )


def result_to_dict(result: RiskAssessmentResult) -> dict[str, Any]:
    """Convert a RiskAssessmentResult to a JSON-serialisable dict."""
    return asdict(result)
