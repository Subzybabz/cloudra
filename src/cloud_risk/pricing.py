from __future__ import annotations

import json
import logging
import boto3
import botocore.config
import botocore.exceptions

from .scoring import get_cached_monthly_cost, AVG_HOURS_PER_MONTH

logger = logging.getLogger(__name__)

# ─── Mappings for AWS Pricing API (Section 3.5.2) ─────────────────────────────

REGION_LOCATION_MAP: dict[str, str] = {
    "us-east-1": "US East (N. Virginia)",
    "us-west-2": "US West (Oregon)",
    "eu-west-1": "EU (Ireland)",
    "eu-west-2": "EU (London)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
}

RESOURCE_INSTANCE_MAP: dict[str, str] = {
    "EC2_SMALL": "t3.small",
    "EC2_MEDIUM": "t3.medium",
    "EC2_LARGE": "t3.large",
    "EC2_XLARGE": "t3.xlarge",
}


def get_instance_monthly_cost(region_code: str, resource_type: str) -> tuple[float, bool]:
    """
    Query the AWS Pricing API for the hourly rate of the specified resource type,
    returning the monthly cost estimate. Falls back to local cached prices
    on any network/credential failure or timeout.

    Returns
    -------
    (monthly_cost_usd, live_price_used)
    """
    instance_type = RESOURCE_INSTANCE_MAP.get(resource_type)
    location_name = REGION_LOCATION_MAP.get(region_code)

    if not instance_type or not location_name:
        logger.warning(
            f"Invalid parameters for pricing query: region={region_code}, resource={resource_type}. "
            "Falling back to cache."
        )
        return get_cached_monthly_cost(resource_type), False

    # Config timeout strictly to 1.5 seconds per connection/read attempt
    config = botocore.config.Config(
        connect_timeout=1.5,
        read_timeout=1.5,
        retries={"max_attempts": 0}
    )

    try:
        # AWS Pricing service is globally available via endpoint in us-east-1
        client = boto3.client("pricing", region_name="us-east-1", config=config)

        filters = [
            {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
            {"Type": "TERM_MATCH", "Field": "location", "Value": location_name},
            {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
            {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
            {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
            {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
        ]

        response = client.get_products(
            ServiceCode="AmazonEC2",
            Filters=filters,
            MaxResults=1
        )

        price_list = response.get("PriceList", [])
        if not price_list:
            logger.warning(f"No pricing match found for {instance_type} in {location_name}. Using cache.")
            return get_cached_monthly_cost(resource_type), False

        product_data = json.loads(price_list[0])
        terms = product_data.get("terms", {})
        on_demand = terms.get("OnDemand", {})

        for term_val in on_demand.values():
            price_dimensions = term_val.get("priceDimensions", {})
            for price_dim in price_dimensions.values():
                price_per_unit = price_dim.get("pricePerUnit", {})
                usd_price = price_per_unit.get("USD")
                if usd_price is not None:
                    hourly_rate = float(usd_price)
                    monthly_cost = hourly_rate * AVG_HOURS_PER_MONTH
                    logger.info(
                        f"Successfully queried live AWS Pricing for {instance_type} in {location_name}: "
                        f"${hourly_rate}/hr (${monthly_cost:.2f}/mo)"
                    )
                    return monthly_cost, True

        logger.warning(f"Could not parse pricing terms for {instance_type} in {location_name}. Using cache.")
        return get_cached_monthly_cost(resource_type), False

    except Exception as exc:
        logger.warning(
            f"AWS Pricing query failed ({type(exc).__name__}: {exc}). "
            f"Falling back to offline cache."
        )
        return get_cached_monthly_cost(resource_type), False
