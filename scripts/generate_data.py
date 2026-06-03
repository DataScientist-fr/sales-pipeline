"""
Script de génération de données fictives pour le projet sales-pipeline.
Utilise Faker pour produire des CSV réalistes avec quelques problèmes intentionnels.
"""

import csv
import os
import random
from collections import Counter
from datetime import datetime, timedelta

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
    CUSTOMERS.append(
        {
            "customer_id": f"C{i:03d}",
            "name": f"Customer {i}",
            "email": f"customer{i}@example.com",
            "country": random.choice(COUNTRIES),
        }
    )


# ---------------------------------------------------------------------------
# Products (20 lignes, propre)
# ---------------------------------------------------------------------------

CATEGORIES = ["Electronics", "Office", "Furniture", "Software", "Accessories"]

PRODUCTS = []
for i in range(1, 21):
    PRODUCTS.append(
        {
            "product_id": f"P{i:03d}",
            "product_name": f"Product {i}",
            "category": random.choice(CATEGORIES),
        }
    )


# ---------------------------------------------------------------------------
# Orders (200 lignes + problèmes intentionnels existants)
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

# Problème existant 1 : 10 doublons (on réinsère des commandes existantes)
duplicates = random.sample(orders[:100], 10)
orders.extend(duplicates)

# Problème existant 2 : 8 valeurs manquantes sur status
for order in random.sample(orders, 8):
    order["status"] = ""

# Problème existant 3 : 5 prix négatifs
for order in random.sample(orders, 5):
    order["unit_price"] = round(-random.uniform(5.0, 100.0), 2)

# Mélanger pour que les problèmes ne soient pas tous à la fin
random.shuffle(orders)

# ---------------------------------------------------------------------------
# Nouveaux défauts sur orders — indices strictement disjoints (tâches 3, 4, 6, 7)
# ---------------------------------------------------------------------------

# Indices portant déjà un défaut existant (doublons, statut vide, prix négatif)
_id_counts = Counter(o["order_id"] for o in orders)
_dup_ids = {oid for oid, cnt in _id_counts.items() if cnt > 1}

_used = set()
for _idx, _o in enumerate(orders):
    if _o["order_id"] in _dup_ids or _o["status"] == "" or _o["unit_price"] <= 0:
        _used.add(_idx)

# Tâche 3 – quantity ≤ 0 : 5 lignes
_avail = sorted(set(range(len(orders))) - _used)
_idx_t3 = random.sample(_avail, 5)
_used.update(_idx_t3)
_BAD_QTY = [0, -1, 0, -2, -3]
for _i, _idx in enumerate(sorted(_idx_t3)):
    orders[_idx]["quantity"] = _BAD_QTY[_i]

# Tâche 4 – order_date invalide : 5 lignes
_avail = sorted(set(range(len(orders))) - _used)
_idx_t4 = random.sample(_avail, 5)
_used.update(_idx_t4)
_BAD_DATES = ["2024-13-01", "31/02/2024", "not_a_date", "2024-00-10", "99/99/9999"]
for _i, _idx in enumerate(sorted(_idx_t4)):
    orders[_idx]["order_date"] = _BAD_DATES[_i]

# Tâche 6 – status casse mixte : 6 lignes (distinctes des status vides)
_avail = sorted(set(range(len(orders))) - _used)
_idx_t6 = random.sample(_avail, 6)
_used.update(_idx_t6)
_MIXED_STATUS = ["Completed", "PENDING", "Cancelled", "Refunded", "COMPLETED", "Pending"]
for _i, _idx in enumerate(sorted(_idx_t6)):
    orders[_idx]["status"] = _MIXED_STATUS[_i]

# Tâche 7 – orphelins customer_id inexistant "C999" : 3 lignes
_avail = sorted(set(range(len(orders))) - _used)
_idx_t7c = random.sample(_avail, 3)
_used.update(_idx_t7c)
for _idx in _idx_t7c:
    orders[_idx]["customer_id"] = "C999"

# Tâche 7 – orphelins product_id inexistant "P999" : 2 lignes
_avail = sorted(set(range(len(orders))) - _used)
_idx_t7p = random.sample(_avail, 2)
_used.update(_idx_t7p)
for _idx in _idx_t7p:
    orders[_idx]["product_id"] = "P999"

# ---------------------------------------------------------------------------
# Nouveaux défauts sur customers — colonnes distinctes (tâches 1 et 2)
# ---------------------------------------------------------------------------

# Tâche 1 – espaces en début/fin sur customers.name : 8 valeurs
_cust_idx_spaces = random.sample(range(len(CUSTOMERS)), 8)
for _i, _idx in enumerate(_cust_idx_spaces):
    _name = CUSTOMERS[_idx]["name"]
    # Alternance : 4 espaces en début, 4 en fin
    CUSTOMERS[_idx]["name"] = ("  " + _name) if _i % 2 == 0 else (_name + "  ")

# Tâche 2 – email casse mixte : 8 valeurs, indices distincts de la tâche 1
_cust_remaining = [i for i in range(len(CUSTOMERS)) if i not in set(_cust_idx_spaces)]
_cust_idx_email = random.sample(_cust_remaining, 8)
for _i, _idx in enumerate(_cust_idx_email):
    _email = CUSTOMERS[_idx]["email"]
    if _i % 2 == 0:
        # Local + domaine en majuscules : "CUSTOMER5@EXAMPLE.COM"
        CUSTOMERS[_idx]["email"] = _email.upper()
    else:
        # Local en titre, domaine inchangé : "Customer2@example.com"
        _local, _domain = _email.split("@")
        CUSTOMERS[_idx]["email"] = _local.capitalize() + "@" + _domain

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
