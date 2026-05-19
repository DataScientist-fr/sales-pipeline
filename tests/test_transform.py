"""
Tests unitaires pour pipeline/transform.py
"""

import pandas as pd
import pytest
from pipeline.transform import (
    remove_duplicates,
    remove_negative_prices,
    fill_missing_status,
    compute_total_price,
    enrich,
)


def test_remove_duplicates(sample_orders):
    result = remove_duplicates(sample_orders)
    assert len(result) == 5  # O002 dupliqué → 1 supprimé
    assert result["order_id"].is_unique


def test_remove_negative_prices(sample_orders):
    result = remove_negative_prices(sample_orders)
    assert (result["unit_price"] > 0).all()


def test_fill_missing_status(sample_orders):
    result = fill_missing_status(sample_orders)
    assert result["status"].isna().sum() == 0
    assert (result["status"] != "").all()
    assert "unknown" in result["status"].values


def test_fill_missing_status_custom_default(sample_orders):
    result = fill_missing_status(sample_orders, default="n/a")
    assert "n/a" in result["status"].values


def test_compute_total_price(sample_orders):
    result = compute_total_price(sample_orders)
    assert "total_price" in result.columns
    expected = sample_orders["quantity"] * sample_orders["unit_price"]
    pd.testing.assert_series_equal(
        result["total_price"].round(2),
        expected.round(2),
        check_names=False,
    )


def test_enrich_adds_customer_columns(sample_orders, sample_customers, sample_products):
    result = enrich(sample_orders, sample_customers, sample_products)
    assert "name" in result.columns
    assert "country" in result.columns


def test_enrich_adds_product_columns(sample_orders, sample_customers, sample_products):
    result = enrich(sample_orders, sample_customers, sample_products)
    assert "product_name" in result.columns
    assert "category" in result.columns
