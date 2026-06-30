from __future__ import annotations

import pytest
from cloud_risk.api import create_app


def make_payload(**overrides):
    payload = {
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
    payload.update(overrides)
    return payload


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test_api_assessments.db"
    app = create_app({"DATABASE_PATH": str(db_file), "TESTING": True})
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_landing_page_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CloudRA" in response.data
    assert b"Launch Assessment Dashboard" in response.data


def test_login_page_serves_html(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_login_with_valid_credentials(client):
    response = client.post("/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_login_with_invalid_credentials(client):
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 302
    assert "error=1" in response.headers["Location"]


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_create_assessment_returns_thesis_aligned_fields(client):
    response = client.post("/assessments", json=make_payload())
    data = response.get_json()

    assert response.status_code == 201
    assert data["project_name"] == "Test Migration"
    assert data["risk_tier"] == "LOW"
    assert "id" in data
    assert "created_at" in data
    assert "composite_score" in data
    assert "operational_score" in data
    assert "financial_score" in data
    assert "cybersec_score" in data
    assert "live_price_used" in data
    assert "monthly_est_usd" in data
    assert isinstance(data["recommendations"], list)

    # Verify history persistence
    list_response = client.get("/assessments")
    assert list_response.status_code == 200
    history = list_response.get_json()
    assert len(history) == 1
    assert history[0]["id"] == data["id"]

    # Verify detail retrieval
    detail_response = client.get(f"/assessments/{data['id']}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()
    assert detail["result_data"]["composite_score"] == data["composite_score"]


def test_create_assessment_rejects_missing_fields(client):
    payload = make_payload()
    del payload["data_volume_tb"]

    response = client.post("/assessments", json=payload)

    assert response.status_code == 400
    assert "data_volume_tb" in response.get_json()["error"]


def test_create_assessment_rejects_non_json_body(client):
    response = client.post("/assessments", data="not json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be JSON"


def test_list_assessments_empty_initially(client):
    response = client.get("/assessments")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_assessment_not_found(client):
    response = client.get("/assessments/nonexistent-id")
    assert response.status_code == 404


def test_delete_assessment(client):
    response = client.post("/assessments", json=make_payload())
    assessment_id = response.get_json()["id"]

    del_response = client.delete(f"/assessments/{assessment_id}")
    assert del_response.status_code == 200
    assert del_response.get_json()["status"] == "deleted"

    get_response = client.get(f"/assessments/{assessment_id}")
    assert get_response.status_code == 404


def test_delete_assessment_not_found(client):
    response = client.delete("/assessments/nonexistent-id")
    assert response.status_code == 404


def test_get_assessment_report(client):
    response = client.post("/assessments", json=make_payload())
    assessment_id = response.get_json()["id"]

    report_response = client.get(f"/assessments/{assessment_id}/report")
    assert report_response.status_code == 200
    assert report_response.content_type == "application/pdf"
    assert report_response.data.startswith(b"%PDF-")
    assert "Content-Disposition" in report_response.headers
    assert f"CloudRisk_Report_{assessment_id}.pdf" in report_response.headers["Content-Disposition"]


def test_get_assessment_report_not_found(client):
    response = client.get("/assessments/nonexistent-id/report")
    assert response.status_code == 404

