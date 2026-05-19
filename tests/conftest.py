"""
Fixtures partagées pour les tests.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_orders() -> pd.DataFrame:
    """DataFrame de commandes avec des problèmes intentionnels."""
    return pd.DataFrame({
        "order_id":   ["O001", "O002", "O002", "O003", "O004", "O005"],
        "customer_id":["C001", "C002", "C002", "C003", "C001", "C002"],
        "product_id": ["P001", "P002", "P002", "P003", "P001", "P003"],
        "quantity":   [2,      1,      1,      3,      5,      2     ],
        "unit_price": [10.0,   -5.0,   -5.0,   20.0,   15.0,   8.0  ],
        "order_date": ["2024-01-01"] * 6,
        "status":     ["completed", "pending", "pending", "", None, "cancelled"],
    })


@pytest.fixture
def sample_customers() -> pd.DataFrame:
    return pd.DataFrame({
        "customer_id": ["C001", "C002", "C003"],
        "name":        ["Alice", "Bob", "Charlie"],
        "email":       ["alice@example.com", "bob@example.com", "charlie@example.com"],
        "country":     ["France", "Germany", "Spain"],
    })


@pytest.fixture
def sample_products() -> pd.DataFrame:
    return pd.DataFrame({
        "product_id":   ["P001", "P002", "P003"],
        "product_name": ["Widget A", "Widget B", "Widget C"],
        "category":     ["Electronics", "Office", "Furniture"],
    })
