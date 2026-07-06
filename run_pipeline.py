"""
Orchestrateur du pipeline : ingestion → transformation → export.
"""

import os

from pipeline import ingest, transform
from pipeline.export import export_json
from pipeline.utils import get_logger, get_output_path

logger = get_logger("run_pipeline")


def run() -> str:
    """Exécute le pipeline complet et retourne le chemin du fichier de sortie."""
    logger.info("=== Démarrage du pipeline ===")

    # Ingestion
    orders, customers, products = ingest.load_all()

    # Transformation
    df_clean = transform.run(orders, customers, products)

    # Export
    output_path = get_output_path()
    output_file = os.path.join(output_path, "orders_clean.csv")
    df_clean.to_csv(output_file, index=False)
    logger.info(f"Fichier de sortie écrit : {output_file}")

    logger.info("Lancement de la phase d'exportation...")
    
    json_output_path = "data/output/cleaned_orders.json"
    
    export_json(df_clean, json_output_path)

    logger.info("=== Pipeline terminé ===")
    return output_file


if __name__ == "__main__":
    run()
