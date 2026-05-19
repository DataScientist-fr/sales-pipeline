# Sales Pipeline

Projet fil rouge du cours **VS Code pour Data Engineers**.

Pipeline de traitement de données de ventes : ingestion de fichiers CSV bruts → nettoyage → transformation → export. Une interface Streamlit permet de lancer le pipeline et visualiser les résultats.

---

## Structure du projet

```
sales-pipeline/
├── data/
│   ├── raw/                  # Données brutes (CSV)
│   └── processed/            # Données nettoyées (gitignored)
├── pipeline/
│   ├── ingest.py             # Lecture et validation des CSV
│   ├── transform.py          # Nettoyage et transformation
│   └── utils.py              # Logging et helpers
├── tests/
│   ├── conftest.py           # Fixtures partagées
│   ├── test_ingest.py
│   └── test_transform.py
├── notebooks/
│   └── exploration.ipynb     # Analyse exploratoire
├── scripts/
│   └── generate_data.py      # Génération des données fictives
├── app.py                    # Interface Streamlit
├── run_pipeline.py           # Orchestrateur
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Prérequis

- Python 3.11+
- Docker Desktop

---

## Installation

```bash
# Cloner le repo
git clone <url-du-repo>
cd sales-pipeline

# Créer et activer le venv
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env
```

---

## Utilisation

### Générer les données

```bash
python scripts/generate_data.py
```

### Lancer le pipeline en local

```bash
python run_pipeline.py
```

### Lancer l'interface Streamlit en local

```bash
streamlit run app.py
```

### Lancer avec Docker

```bash
docker compose up --build
```

L'interface est accessible sur [http://localhost:8501](http://localhost:8501).

### Lancer les tests

```bash
pytest
```

---

## Données

Les données sont générées par `scripts/generate_data.py`. Elles simulent des exports de ventes avec des problèmes intentionnels :

| Fichier | Lignes | Problèmes |
|---|---|---|
| `orders.csv` | ~210 | Doublons, prix négatifs, statuts manquants |
| `customers.csv` | 50 | Aucun |
| `products.csv` | 20 | Aucun |
