
"""
Transformation : nettoyage des données et enrichissement.
"""

import pandas as pd

from pipeline.utils import get_logger

logger = get_logger(__name__)


def sales_by_country(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("country", as_index=False)["total_price"]
        .sum()
        .sort_values(by="total_price", ascending=False)
        .reset_index(drop=True)
    )
