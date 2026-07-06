import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def export_json(df, path):
    directory = os.path.dirname(path)
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        logger.info(f"[EXPORT] Création du dossier manquant : {directory}")
    df.to_json(path, orient="records", date_format="iso", indent=4)

    logger.info(f"[EXPORT] Données exportées avec succès au format JSON -> {path}")