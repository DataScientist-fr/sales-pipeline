"""
Interface Streamlit du pipeline sales.
Permet de lancer le pipeline et visualiser le résultat.
"""

import io
import logging
import os
import sys
import pandas as pd
import streamlit as st

# Ajouter la racine du projet au path pour les imports
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Sales Pipeline",
    page_icon="🔄",
    layout="wide",
)

st.title("🔄 Sales Pipeline")
st.caption("Nettoyage et transformation des données de ventes")

st.divider()

col1, col2, col3 = st.columns(3)

# Affichage des variables d'environnement actives
with col1:
    st.metric("Environnement", os.getenv("ENV", "development"))
with col2:
    st.metric("Source", os.getenv("DATA_PATH", "data/raw"))
with col3:
    st.metric("Sortie", os.getenv("OUTPUT_PATH", "data/processed"))

st.divider()

if st.button("▶️ Lancer le pipeline", type="primary", use_container_width=True):

    log_output = st.empty()
    log_lines = []

    # Intercepter les logs pour les afficher dans l'interface
    class StreamlitHandler(logging.Handler):
        def emit(self, record):
            log_lines.append(self.format(record))
            log_output.code("\n".join(log_lines), language=None)

    handler = StreamlitHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s", datefmt="%H:%M:%S"))

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    try:
        from run_pipeline import run
        output_file = run()
        st.success(f"✅ Pipeline terminé — {output_file}")

        # Aperçu du fichier de sortie
        if os.path.exists(output_file):
            st.divider()
            st.subheader("Aperçu des données nettoyées")
            df = pd.read_csv(output_file)
            st.caption(f"{len(df)} commandes · {len(df.columns)} colonnes")
            st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")
    finally:
        root_logger.removeHandler(handler)

else:
    st.info("Cliquez sur **Lancer le pipeline** pour démarrer le traitement.")

    # Aperçu des données brutes si disponibles
    raw_path = os.path.join(os.getenv("DATA_PATH", "data/raw"), "orders.csv")
    if os.path.exists(raw_path):
        st.divider()
        st.subheader("Aperçu des données brutes")
        df_raw = pd.read_csv(raw_path)
        st.caption(f"{len(df_raw)} lignes · {len(df_raw.columns)} colonnes")
        st.dataframe(df_raw.head(10), use_container_width=True)
