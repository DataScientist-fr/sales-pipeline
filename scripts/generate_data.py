"""
Script de génération de données fictives pour le projet sales-pipeline.
Utilise Faker pour produire des CSV réalistes avec quelques problèmes intentionnels.
"""

import random
from datetime import datetime, timedelta
import csv
import os

random.seed(42)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def random_date(start_year=2023, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Customers (50 lignes, propre)
# ---------------------------------------------------------------------------

COUNTRIES = ["France", "Germany", "Spain", "Italy", "Belgium", "Netherlands"]

CUSTOMERS = []
for i in range(1, 51):
    CUSTOMERS.append({
        "customer_id": f"C{i:03d}",
        "name": f"Customer {i}",
        "email": f"customer{i}@example.com",
        "country": random.choice(COUNTRIES),
    })


# ---------------------------------------------------------------------------
# Products (20 lignes, propre)
# ---------------------------------------------------------------------------

CATEGORIES = ["Electronics", "Office", "Furniture", "Software", "Accessories"]

PRODUCTS = []
for i in range(1, 21):
    PRODUCTS.append({
        "product_id": f"P{i:03d}",
        "product_name": f"Product {i}",
        "category": random.choice(CATEGORIES),
    })


# ---------------------------------------------------------------------------
# Orders (200 lignes + problèmes intentionnels)
# ---------------------------------------------------------------------------

STATUSES = ["completed", "pending", "cancelled", "refunded"]

orders = []
for i in range(1, 201):
    order = {
        "order_id": f"O{i:04d}",
        "customer_id": random.choice(CUSTOMERS)["customer_id"],
        "product_id": random.choice(PRODUCTS)["product_id"],
        "quantity": random.randint(1, 10),
        "unit_price": round(random.uniform(5.0, 500.0), 2),
        "order_date": random_date(),
        "status": random.choice(STATUSES),
    }
    orders.append(order)

# Problème 1 : 10 doublons (on réinsère des commandes existantes)
duplicates = random.sample(orders[:100], 10)
orders.extend(duplicates)

# Problème 2 : 8 valeurs manquantes sur status
for order in random.sample(orders, 8):
    order["status"] = ""

# Problème 3 : 5 prix négatifs
for order in random.sample(orders, 5):
    order["unit_price"] = round(-random.uniform(5.0, 100.0), 2)

# Mélanger pour que les problèmes ne soient pas tous à la fin
random.shuffle(orders)


# ---------------------------------------------------------------------------
# Écriture des CSV
# ---------------------------------------------------------------------------

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ {filename} généré ({len(rows)} lignes)")


write_csv("customers.csv", CUSTOMERS, ["customer_id", "name", "email", "country"])
write_csv("products.csv", PRODUCTS, ["product_id", "product_name", "category"])
write_csv(
    "orders.csv",
    orders,
    ["order_id", "customer_id", "product_id", "quantity", "unit_price", "order_date", "status"],
)

print("\nDonnées générées dans data/raw/")
