"""
Tests unitaires pour pipeline/transform.py
"""

import pandas as pd

from pipeline.transform import remove_invalid_quantity


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