"""
Ingestion : lecture et validation des fichiers CSV bruts.
"""

import os
import pandas as pd
from pipeline.utils import get_logger, get_data_path

logger = get_logger(__name__)

EXPECTED_COLUMNS = {
    "orders": ["order_id", "customer_id", "product_id", "quantity", "unit_price", "order_date", "status"],
    "customers": ["customer_id", "name", "email", "country"],
    "products": ["product_id", "product_name", "category"],
}


def load_csv(filename: str) -> pd.DataFrame:
    """Charge un fichier CSV depuis DATA_PATH et valide ses colonnes."""
    data_path = get_data_path()
    filepath = os.path.join(data_path, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    df = pd.read_csv(filepath)
    logger.info(f"{filename} chargé — {len(df)} lignes, {len(df.columns)} colonnes")

    # Validation des colonnes
    name = filename.replace(".csv", "")
    if name in EXPECTED_COLUMNS:
        missing = set(EXPECTED_COLUMNS[name]) - set(df.columns)
        if missing:
            raise ValueError(f"Colonnes manquantes dans {filename} : {missing}")

    return df


def load_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Charge les trois fichiers CSV et retourne les DataFrames."""
    logger.info("Démarrage de l'ingestion...")
    orders = load_csv("orders.csv")
    customers = load_csv("customers.csv")
    products = load_csv("products.csv")
    logger.info("Ingestion terminée.")
    return orders, customers, products
