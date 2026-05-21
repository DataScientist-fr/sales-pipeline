"""
Fonctions utilitaires partagées : logging et lecture des variables d'environnement.
"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()


def get_logger(name: str) -> logging.Logger:
    """Retourne un logger configuré avec le niveau défini dans LOG_LEVEL."""
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
        level=getattr(logging, level, logging.INFO),
    )
    return logging.getLogger(name)


def get_data_path() -> str:
    """Retourne le chemin vers les données brutes depuis DATA_PATH."""
    return os.getenv("DATA_PATH", "data/raw")


def get_output_path() -> str:
    """Retourne le chemin de sortie depuis OUTPUT_PATH."""
    path = os.getenv("OUTPUT_PATH", "data/processed")
    os.makedirs(path, exist_ok=True)
    return path
