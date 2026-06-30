from __future__ import annotations

from cloud_risk.report import generate_pdf_report


def test_generate_pdf_report_success():
    dummy_assessment = {
        "project_name": "Test PDF Report Project",
        "created_at": "2026-06-27T20:00:00Z",
        "id": "12345678-abcd-1234-abcd-1234567890ab",
        "input_data": {
            "data_volume_tb": 15.0,
            "target_region": "eu-west-1",
            "server_count": 30,
            "resource_type": "EC2_MEDIUM",
            "app_complexity": "MEDIUM",
            "egress_volume_tb": 2.0,
            "migration_window_hrs": 24,
            "capex_monthly_usd": 3000.0,
            "data_sensitivity": "CONFIDENTIAL",
            "projected_users": 500,
            "iam_permissiveness": "MODERATE",
            "encryption_posture": "FULL",
            "compliance_scope": "SINGLE",
        },
        "result_data": {
            "composite_score": 45.2,
            "operational_score": 40.5,
            "financial_score": 35.0,
            "cybersec_score": 60.0,
            "risk_tier": "MEDIUM",
            "live_price_used": False,
            "monthly_est_usd": 30.37,
            "recommendations": [
                {
                    "parameter": "Data Sensitivity",
                    "dimension": "Cybersecurity",
                    "detail": "Data sensitivity classification warrants enhanced protection...",
                    "priority": "IMPORTANT",
                    "score": 65.0,
                }
            ],
        },
    }

    pdf_bytes = generate_pdf_report(dummy_assessment)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF files start with the magic header bytes: %PDF-
    assert pdf_bytes.startswith(b"%PDF-")


def test_generate_pdf_report_no_recommendations():
    dummy_assessment = {
        "project_name": "Test Empty Recs",
        "created_at": "2026-06-27T20:00:00Z",
        "id": "empty-uuid",
        "input_data": {},
        "result_data": {
            "composite_score": 20.0,
            "operational_score": 20.0,
            "financial_score": 20.0,
            "cybersec_score": 20.0,
            "risk_tier": "LOW",
            "live_price_used": False,
            "monthly_est_usd": 15.18,
            "recommendations": [],
        },
    }

    pdf_bytes = generate_pdf_report(dummy_assessment)
    assert pdf_bytes.startswith(b"%PDF-")
