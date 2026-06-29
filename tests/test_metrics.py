"""
Tests unitaires pour pipeline/metrics.py
"""

import pandas as pd

from pipeline.metrics import sales_by_country


def test_sales_by_country():
    df = pd.DataFrame(
        {
            "country": [
                "France",
                "Canada",
                "France",
                "Belgique",
                "Canada",
                "France",
            ],
            "total_price": [
                100.0,
                50.0,
                25.0,
                80.0,
                150.0,
                75.0,
            ],
        }
    )

    result = sales_by_country(df)

    expected = pd.DataFrame(
        {
            "country": [
                "Canada",
                "France",
                "Belgique",
            ],
            "total_price": [
                200.0,
                200.0,
                80.0,
            ],
        }
    )

    pd.testing.assert_frame_equal(result, expected)