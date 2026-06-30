from __future__ import annotations

import json
from unittest.mock import MagicMock, patch
import pytest
from botocore.exceptions import NoCredentialsError

from cloud_risk.pricing import get_instance_monthly_cost, RESOURCE_INSTANCE_MAP, REGION_LOCATION_MAP


def test_mappings_exist():
    assert RESOURCE_INSTANCE_MAP["EC2_SMALL"] == "t3.small"
    assert REGION_LOCATION_MAP["eu-west-1"] == "EU (Ireland)"


def test_invalid_parameters_fallback():
    # If invalid region/resource type is provided, it should fallback to cached prices
    cost, live_price = get_instance_monthly_cost("invalid-region", "EC2_SMALL")
    assert live_price is False
    assert cost > 0


@patch("boto3.client")
def test_boto3_success(mock_client_factory):
    # Mock successful response
    mock_client = MagicMock()
    mock_client_factory.return_value = mock_client

    dummy_payload = {
        "terms": {
            "OnDemand": {
                "sku.ratecode": {
                    "priceDimensions": {
                        "sku.ratecode.dimension": {
                            "pricePerUnit": {
                                "USD": "0.0832"  # EC2_LARGE fallback or mock rate
                            }
                        }
                    }
                }
            }
        }
    }

    mock_client.get_products.return_value = {
        "PriceList": [json.dumps(dummy_payload)]
    }

    cost, live_price = get_instance_monthly_cost("eu-west-1", "EC2_LARGE")
    
    # Assert get_products was called with correct parameters
    mock_client.get_products.assert_called_once()
    args, kwargs = mock_client.get_products.call_args
    assert kwargs["ServiceCode"] == "AmazonEC2"
    filters = kwargs["Filters"]
    assert {"Type": "TERM_MATCH", "Field": "instanceType", "Value": "t3.large"} in filters
    assert {"Type": "TERM_MATCH", "Field": "location", "Value": "EU (Ireland)"} in filters

    assert live_price is True
    # 0.0832 * 730 = 60.736
    assert cost == pytest.approx(60.736)


@patch("boto3.client")
def test_boto3_empty_response_fallback(mock_client_factory):
    mock_client = MagicMock()
    mock_client_factory.return_value = mock_client
    mock_client.get_products.return_value = {"PriceList": []}

    cost, live_price = get_instance_monthly_cost("eu-west-1", "EC2_MEDIUM")
    assert live_price is False
    # EC2_MEDIUM fallback: 0.0416 * 730 = 30.368
    assert cost == pytest.approx(30.368)


@patch("boto3.client")
def test_boto3_exception_fallback(mock_client_factory):
    mock_client = MagicMock()
    mock_client_factory.return_value = mock_client
    mock_client.get_products.side_effect = NoCredentialsError()

    cost, live_price = get_instance_monthly_cost("eu-west-1", "EC2_SMALL")
    assert live_price is False
    # EC2_SMALL fallback: 0.0208 * 730 = 15.184
    assert cost == pytest.approx(15.184)
