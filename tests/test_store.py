from unittest.mock import MagicMock, patch
from cloud_risk.store import AssessmentStore
from cloud_risk.models import MigrationAssessmentInput, RiskRecommendation, RiskAssessmentResult
from botocore.exceptions import ClientError
from decimal import Decimal


def make_dummy_assessment():
    input_payload = MigrationAssessmentInput(
        project_name="Test Project",
        data_volume_tb=5.0,
        server_count=10,
        app_complexity="LOW",
        migration_window_hrs=48,
        resource_type="EC2_SMALL",
        target_region="eu-west-1",
        egress_volume_tb=1.0,
        capex_monthly_usd=2000.0,
        projected_users=100,
        data_sensitivity="INTERNAL",
        iam_permissiveness="LEAST_PRIV",
        encryption_posture="FULL",
        compliance_scope="NONE",
    )
    result = RiskAssessmentResult(
        project_name="Test Project",
        composite_score=25.0,
        operational_score=20.0,
        financial_score=15.0,
        cybersec_score=30.0,
        risk_tier="LOW",
        live_price_used=False,
        monthly_est_usd=15.18,
        recommendations=[
            RiskRecommendation(
                parameter="Data Volume",
                dimension="Operational",
                detail="Test recommendation.",
                priority="ADVISORY",
                score=55.0,
            )
        ],
    )
    return input_payload, result


def test_store_lifecycle(tmp_path):
    db_file = tmp_path / "test_assessments.db"
    store = AssessmentStore(db_file)
    store.init_db()

    assert db_file.exists()
    assert len(store.list_assessments()) == 0

    input_payload, result = make_dummy_assessment()

    saved_result = store.save_assessment(input_payload, result)
    assert "id" in saved_result
    assert "created_at" in saved_result
    assert saved_result["project_name"] == "Test Project"
    assert saved_result["composite_score"] == 25.0

    history = store.list_assessments()
    assert len(history) == 1
    assert history[0]["id"] == saved_result["id"]

    fetched = store.get_assessment(saved_result["id"])
    assert fetched is not None
    assert fetched["input_data"]["data_volume_tb"] == 5.0
    assert fetched["result_data"]["composite_score"] == 25.0

    deleted = store.delete_assessment(saved_result["id"])
    assert deleted is True
    assert store.get_assessment(saved_result["id"]) is None
    assert len(store.list_assessments()) == 0


def test_get_nonexistent(tmp_path):
    store = AssessmentStore(tmp_path / "test.db")
    store.init_db()
    assert store.get_assessment("fake-id") is None
    assert store.delete_assessment("fake-id") is False


def test_schema_columns(tmp_path):
    db_file = tmp_path / "test_schema.db"
    store = AssessmentStore(db_file)
    store.init_db()

    expected_cols = {
        "AssessmentId", "Timestamp", "CompositeScore", "OperationalScore",
        "FinancialScore", "CybersecScore", "RiskTier", "InputParameters",
        "Recommendations", "LivePriceUsed", "MonthlyEstUSD"
    }

    with store._get_connection() as conn:
        cursor = conn.execute("PRAGMA table_info(assessments)")
        actual_cols = {row["name"] for row in cursor.fetchall()}

    assert actual_cols == expected_cols


@patch("cloud_risk.store.boto3.resource")
def test_dynamodb_lifecycle(mock_boto_resource, tmp_path):
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_boto_resource.return_value = mock_db
    mock_db.Table.return_value = mock_table

    # Scenario 1: Table exists
    store = AssessmentStore(tmp_path / "test.db", use_dynamodb=True)
    store.init_db()
    assert store.use_dynamodb is True
    mock_db.Table.assert_called_with("CloudRiskAssessments")

    # Scenario 2: Save assessment
    input_payload, result = make_dummy_assessment()
    saved = store.save_assessment(input_payload, result)
    assert "id" in saved
    mock_table.put_item.assert_called_once()
    saved_item = mock_table.put_item.call_args[1]["Item"]
    assert saved_item["AssessmentId"] == saved["id"]
    assert saved_item["CompositeScore"] == Decimal("25.0")
    assert saved_item["RiskTier"] == "LOW"

    # Scenario 3: List assessments
    mock_table.scan.return_value = {
        "Items": [
            {
                "AssessmentId": saved["id"],
                "Timestamp": saved["created_at"],
                "CompositeScore": Decimal("25.0"),
                "RiskTier": "LOW",
                "InputParameters": {
                    "project_name": "Test Project"
                }
            }
        ]
    }
    history = store.list_assessments()
    assert len(history) == 1
    assert history[0]["id"] == saved["id"]
    mock_table.scan.assert_called_once()

    # Scenario 4: Get assessment
    mock_table.get_item.return_value = {
        "Item": {
            "AssessmentId": saved["id"],
            "Timestamp": saved["created_at"],
            "CompositeScore": Decimal("25.0"),
            "OperationalScore": Decimal("20.0"),
            "FinancialScore": Decimal("15.0"),
            "CybersecScore": Decimal("30.0"),
            "RiskTier": "LOW",
            "LivePriceUsed": False,
            "MonthlyEstUSD": Decimal("15.18"),
            "InputParameters": {
                "project_name": "Test Project",
                "data_volume_tb": Decimal("5.0")
            },
            "Recommendations": []
        }
    }
    fetched = store.get_assessment(saved["id"])
    assert fetched is not None
    assert fetched["id"] == saved["id"]
    assert fetched["input_data"]["data_volume_tb"] == 5.0
    mock_table.get_item.assert_called_with(Key={"AssessmentId": saved["id"]})

    # Scenario 5: Delete assessment
    mock_table.get_item.return_value = {"Item": {}}  # return dummy for exists check
    mock_table.delete_item.return_value = {}
    deleted = store.delete_assessment(saved["id"])
    assert deleted is True
    mock_table.delete_item.assert_called_with(Key={"AssessmentId": saved["id"]})


@patch("cloud_risk.store.boto3.resource")
def test_dynamodb_creation_when_missing(mock_boto_resource, tmp_path):
    mock_db = MagicMock()
    mock_table = MagicMock()
    mock_boto_resource.return_value = mock_db
    mock_db.Table.return_value = mock_table

    # Simulate ResourceNotFoundException
    mock_table.table_status = MagicMock()
    error_response = {"Error": {"Code": "ResourceNotFoundException", "Message": "Not Found"}}
    type(mock_table).table_status = property(MagicMock(side_effect=ClientError(error_response, "DescribeTable")))

    mock_db.create_table.return_value = mock_table

    store = AssessmentStore(tmp_path / "test.db", use_dynamodb=True)
    store.init_db()

    mock_db.create_table.assert_called_once()
