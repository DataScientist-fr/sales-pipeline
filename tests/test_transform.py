"""
Tests unitaires pour pipeline/transform.py
"""

import pandas as pd

from pipeline.transform import (
    compute_total_price,
    enrich,
    fill_missing_status,
    normalize_emails,
    parse_order_dates,
    remove_duplicates,
    remove_invalid_quantity,
    remove_negative_prices,
    strip_whitespace,
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


def test_strip_whitespace(sample_customers):
    result = strip_whitespace(sample_customers, ["name"])
    for i in result["name"]:
        assert not i.startswith(" ")
        assert not i.endswith(" ")


def test_enrich_adds_product_columns(sample_orders, sample_customers, sample_products):
    result = enrich(sample_orders, sample_customers, sample_products)
    assert "product_name" in result.columns
    assert "category" in result.columns


def test_remove_invalid_quantity_keeps_only_positive_quantities():
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5],
            "quantity": [2, 0, -1, 5, -3],
            "unit_price": [10, 20, 30, 40, 50],
        }
    )

    result = remove_invalid_quantity(df)

    assert len(result) == 2
    assert result["quantity"].tolist() == [2, 5]
    assert (result["quantity"] > 0).all()


def test_normalize_emails():
    data = {"id": [1, 2], "email": ["ALI@test.com", "moha@Ex.ma"]}
    df = pd.DataFrame(data)
    result_df = normalize_emails(df)
    assert result_df.loc[0, "email"] == "ali@test.com"
    assert result_df.loc[1, "email"] == "moha@ex.ma"


def test_parse_order_dates():
    data = { "order_id": [1, 2, 3, 4], "order_date": ["2023-01-01", "2023-02-30", "invalid_date", None], }
    df = pd.DataFrame(data)
    result_df = parse_order_dates(df)
    # Vérifier que les dates valides sont converties correctement
    assert pd.notna(result_df.loc[0, "order_date"])
    assert result_df.loc[0, "order_date"] == pd.Timestamp("2023-01-01")

