"""
Tests unitaires pour pipeline/ingest.py
"""

import os
import pytest
import pandas as pd
from unittest.mock import patch
from pipeline.ingest import load_csv


def test_load_csv_file_not_found():
    with patch("pipeline.ingest.get_data_path", return_value="/nonexistent"):
        with pytest.raises(FileNotFoundError):
            load_csv("orders.csv")


def test_load_csv_missing_columns(tmp_path):
    # Crée un CSV avec des colonnes incorrectes
    bad_csv = tmp_path / "orders.csv"
    bad_csv.write_text("wrong_col1,wrong_col2\n1,2\n")

    with patch("pipeline.ingest.get_data_path", return_value=str(tmp_path)):
        with pytest.raises(ValueError, match="Colonnes manquantes"):
            load_csv("orders.csv")


def test_load_csv_valid(tmp_path):
    valid_csv = tmp_path / "customers.csv"
    valid_csv.write_text("customer_id,name,email,country\nC001,Alice,a@b.com,France\n")

    with patch("pipeline.ingest.get_data_path", return_value=str(tmp_path)):
        df = load_csv("customers.csv")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
