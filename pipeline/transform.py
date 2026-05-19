"""
Transformation : nettoyage des données et enrichissement.
"""

import pandas as pd
from pipeline.utils import get_logger

logger = get_logger(__name__)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les lignes dupliquées sur order_id."""
    before = len(df)
    df = df.drop_duplicates(subset=["order_id"])
    removed = before - len(df)
    logger.info(f"Doublons supprimés : {removed}")
    return df


def remove_negative_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les lignes avec un unit_price négatif ou nul."""
    before = len(df)
    df = df[df["unit_price"] > 0]
    removed = before - len(df)
    logger.info(f"Lignes avec prix invalide supprimées : {removed}")
    return df


def fill_missing_status(df: pd.DataFrame, default: str = "unknown") -> pd.DataFrame:
    """Remplace les valeurs manquantes dans status par une valeur par défaut."""
    missing = df["status"].isna() | (df["status"] == "")
    count = missing.sum()
    df.loc[missing, "status"] = default
    logger.info(f"Statuts manquants remplacés par '{default}' : {count}")
    return df


def compute_total_price(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule la colonne total_price = quantity × unit_price."""
    df["total_price"] = df["quantity"] * df["unit_price"]
    df["total_price"] = df["total_price"].round(2)
    logger.info("Colonne total_price calculée.")
    return df


def enrich(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Enrichit les commandes avec les informations clients et produits."""
    df = orders.merge(customers, on="customer_id", how="left")
    df = df.merge(products, on="product_id", how="left")
    logger.info("Enrichissement avec customers et products effectué.")
    return df


def run(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Exécute toutes les étapes de transformation dans l'ordre."""
    logger.info("Démarrage des transformations...")
    df = remove_duplicates(orders)
    df = remove_negative_prices(df)
    df = fill_missing_status(df)
    df = compute_total_price(df)
    df = enrich(df, customers, products)
    logger.info(f"Transformations terminées — {len(df)} lignes en sortie.")
    return df
