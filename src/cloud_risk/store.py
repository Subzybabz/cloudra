from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import sqlite3
from typing import Any
import uuid

import boto3
from botocore.exceptions import ClientError

from .models import MigrationAssessmentInput, RiskAssessmentResult
from .serialization import result_to_dict


def float_to_decimal(obj: Any) -> Any:
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: float_to_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [float_to_decimal(x) for x in obj]
    return obj


def decimal_to_float(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decimal_to_float(x) for x in obj]
    return obj


class AssessmentStore:
    """Hybrid persistence store supporting SQLite and AWS DynamoDB.

    Column/Attribute layout mirrors the DynamoDB schema described in Section 3.5.2
    Phase 6, with automated table provisioning and offline fallback capability.
    """

    def __init__(self, db_path: str | Path, use_dynamodb: bool = False) -> None:
        self.db_path = Path(db_path)
        self.use_dynamodb = use_dynamodb
        self.dynamodb = None
        self.table = None

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Create or migrate the database table."""
        if self.use_dynamodb:
            try:
                self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
                self.table = self.dynamodb.Table("CloudRiskAssessments")
                # Try accessing table details to see if it exists
                self.table.table_status
            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    # Create the table dynamically
                    self.table = self.dynamodb.create_table(
                        TableName="CloudRiskAssessments",
                        KeySchema=[
                            {"AttributeName": "AssessmentId", "KeyType": "HASH"}
                        ],
                        AttributeDefinitions=[
                            {"AttributeName": "AssessmentId", "AttributeType": "S"}
                        ],
                        BillingMode="PAY_PER_REQUEST"
                    )
                    # Wait for table creation
                    self.table.meta.client.get_waiter("table_exists").wait(
                        TableName="CloudRiskAssessments"
                    )
                else:
                    raise e
            return

        # SQLite mode fallback
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as conn:
            # Detect old schema and recreate if necessary
            cursor = conn.execute("PRAGMA table_info(assessments)")
            columns = {row["name"] for row in cursor.fetchall()}

            # If there's an old schema (e.g. using 'id' instead of 'AssessmentId'), drop it
            if columns and "AssessmentId" not in columns:
                conn.execute("DROP TABLE assessments")

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS assessments (
                    AssessmentId TEXT PRIMARY KEY,
                    Timestamp TEXT NOT NULL,
                    CompositeScore REAL NOT NULL,
                    OperationalScore REAL NOT NULL,
                    FinancialScore REAL NOT NULL,
                    CybersecScore REAL NOT NULL,
                    RiskTier TEXT NOT NULL,
                    InputParameters TEXT NOT NULL,
                    Recommendations TEXT NOT NULL,
                    LivePriceUsed INTEGER NOT NULL,
                    MonthlyEstUSD REAL NOT NULL
                )
                """
            )
            conn.commit()

    def save_assessment(
        self, input_payload: MigrationAssessmentInput, result: RiskAssessmentResult
    ) -> dict[str, Any]:
        assessment_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        input_dict = asdict(input_payload)
        recs_dict = [asdict(r) for r in result.recommendations]

        # Prepare the final JSON result structure that the frontend expects
        result_dict = result_to_dict(result)
        result_dict["id"] = assessment_id
        result_dict["created_at"] = timestamp

        if self.use_dynamodb:
            item = {
                "AssessmentId": assessment_id,
                "Timestamp": timestamp,
                "CompositeScore": float_to_decimal(result.composite_score),
                "OperationalScore": float_to_decimal(result.operational_score),
                "FinancialScore": float_to_decimal(result.financial_score),
                "CybersecScore": float_to_decimal(result.cybersec_score),
                "RiskTier": result.risk_tier,
                "InputParameters": float_to_decimal(input_dict),
                "Recommendations": float_to_decimal(recs_dict),
                "LivePriceUsed": result.live_price_used,
                "MonthlyEstUSD": float_to_decimal(result.monthly_est_usd),
            }
            self.table.put_item(Item=item)
            return result_dict

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO assessments (
                    AssessmentId, Timestamp, CompositeScore, OperationalScore,
                    FinancialScore, CybersecScore, RiskTier, InputParameters,
                    Recommendations, LivePriceUsed, MonthlyEstUSD
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assessment_id,
                    timestamp,
                    result.composite_score,
                    result.operational_score,
                    result.financial_score,
                    result.cybersec_score,
                    result.risk_tier,
                    json.dumps(input_dict),
                    json.dumps(recs_dict),
                    1 if result.live_price_used else 0,
                    result.monthly_est_usd,
                ),
            )
            conn.commit()

        return result_dict

    def list_assessments(self) -> list[dict[str, Any]]:
        """Return a list of assessment summaries, mapped to frontend-expected key names."""
        if self.use_dynamodb:
            response = self.table.scan(
                ProjectionExpression="AssessmentId, #ts, CompositeScore, RiskTier, InputParameters",
                ExpressionAttributeNames={"#ts": "Timestamp"}
            )
            items = response.get("Items", [])
            results = []
            for item in items:
                item_data = decimal_to_float(item)
                results.append({
                    "id": item_data["AssessmentId"],
                    "project_name": item_data["InputParameters"].get("project_name", "Unknown Project"),
                    "created_at": item_data["Timestamp"],
                    "composite_score": item_data["CompositeScore"],
                    "risk_tier": item_data["RiskTier"],
                })
            # Sort by Timestamp DESC
            results.sort(key=lambda x: x["created_at"], reverse=True)
            return results

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT AssessmentId, Timestamp, CompositeScore, RiskTier, InputParameters
                FROM assessments
                ORDER BY Timestamp DESC
                """
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                input_data = json.loads(row["InputParameters"])
                results.append({
                    "id": row["AssessmentId"],
                    "project_name": input_data.get("project_name", "Unknown Project"),
                    "created_at": row["Timestamp"],
                    "composite_score": row["CompositeScore"],
                    "risk_tier": row["RiskTier"],
                })
            return results

    def get_assessment(self, assessment_id: str) -> dict[str, Any] | None:
        """Fetch and construct a complete assessment profile matching the frontend API schema."""
        if self.use_dynamodb:
            response = self.table.get_item(Key={"AssessmentId": assessment_id})
            item = response.get("Item")
            if not item:
                return None

            item_data = decimal_to_float(item)
            input_data = item_data["InputParameters"]
            recs_data = item_data["Recommendations"]

            result_data = {
                "project_name": input_data.get("project_name", ""),
                "composite_score": item_data["CompositeScore"],
                "operational_score": item_data["OperationalScore"],
                "financial_score": item_data["FinancialScore"],
                "cybersec_score": item_data["CybersecScore"],
                "risk_tier": item_data["RiskTier"],
                "live_price_used": bool(item_data["LivePriceUsed"]),
                "monthly_est_usd": item_data["MonthlyEstUSD"],
                "recommendations": recs_data,
                "id": item_data["AssessmentId"],
                "created_at": item_data["Timestamp"],
            }

            return {
                "id": item_data["AssessmentId"],
                "project_name": input_data.get("project_name", ""),
                "created_at": item_data["Timestamp"],
                "composite_score": item_data["CompositeScore"],
                "risk_tier": item_data["RiskTier"],
                "live_price_used": bool(item_data["LivePriceUsed"]),
                "monthly_est_usd": item_data["MonthlyEstUSD"],
                "input_data": input_data,
                "result_data": result_data,
            }

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT AssessmentId, Timestamp, CompositeScore, OperationalScore,
                       FinancialScore, CybersecScore, RiskTier, InputParameters,
                       Recommendations, LivePriceUsed, MonthlyEstUSD
                FROM assessments
                WHERE AssessmentId = ?
                """,
                (assessment_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            input_data = json.loads(row["InputParameters"])
            recs_data = json.loads(row["Recommendations"])

            result_data = {
                "project_name": input_data.get("project_name", ""),
                "composite_score": row["CompositeScore"],
                "operational_score": row["OperationalScore"],
                "financial_score": row["FinancialScore"],
                "cybersec_score": row["CybersecScore"],
                "risk_tier": row["RiskTier"],
                "live_price_used": bool(row["LivePriceUsed"]),
                "monthly_est_usd": row["MonthlyEstUSD"],
                "recommendations": recs_data,
                "id": row["AssessmentId"],
                "created_at": row["Timestamp"],
            }

            return {
                "id": row["AssessmentId"],
                "project_name": input_data.get("project_name", ""),
                "created_at": row["Timestamp"],
                "composite_score": row["CompositeScore"],
                "risk_tier": row["RiskTier"],
                "live_price_used": bool(row["LivePriceUsed"]),
                "monthly_est_usd": row["MonthlyEstUSD"],
                "input_data": input_data,
                "result_data": result_data,
            }

    def delete_assessment(self, assessment_id: str) -> bool:
        if self.use_dynamodb:
            try:
                # Check if item exists first to match SQLite behavior of returning false if not found
                response = self.table.get_item(Key={"AssessmentId": assessment_id})
                if "Item" not in response:
                    return False
                self.table.delete_item(Key={"AssessmentId": assessment_id})
                return True
            except ClientError:
                return False

        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM assessments WHERE AssessmentId = ?", (assessment_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
