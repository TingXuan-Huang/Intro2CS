"""Tests for the Lesson 5 refactoring exercise.

These tests import from ``analysis.py`` -- the module YOU create by
extracting functions out of ``messy_analysis.py``. Until analysis.py
exists, this whole file fails to collect with a ModuleNotFoundError:
that is the intended starting state, not something you broke.

Run from inside lesson5_exercise/ :

    python3 -m pytest test_lesson5.py -v

Expected module contract (analysis.py):

    load_transactions(path) -> pandas.DataFrame
        Read the CSV at ``path``; tidy the Description text the way the
        script does; add the same revenue column the script adds.

    clean_prices(transactions) -> pandas.DataFrame
        Return a NEW frame, keeping the rows the script's price rule
        keeps. Must not modify the frame passed in.

    revenue_by_country(transactions) -> dict
        {country: total revenue, rounded to 2 decimal places}

    top_customers(transactions, n=3) -> list of (customer_id, total) pairs
        Sorted by total descending; a tie goes to the SMALLER customer id
        (the script's selection loop already encodes this rule); totals
        rounded to 2 decimal places; fewer than n customers -> return all.

Some tests below pin down edge cases the script itself never meets
(empty tables, ties). They are still part of the contract: decide what
the script WOULD do by reading its logic, not by running it.
"""

from pathlib import Path

import pandas as pd
import pytest

from analysis import (
    clean_prices,
    load_transactions,
    revenue_by_country,
    top_customers,
)

DATA_PATH = Path(__file__).parent.parent / "course_data" / "online_retail_sample.csv"


def edge_frame(customer_ids, revenues):
    """A minimal hand-made table for edge-case tests (no file needed)."""
    return pd.DataFrame(
        {
            "source_customer_id": customer_ids,
            "Country": ["United Kingdom"] * len(customer_ids),
            "revenue": revenues,
        }
    )


# ---------------------------------------------------------------- load

def test_load_transactions_returns_every_row():
    transactions = load_transactions(DATA_PATH)
    assert len(transactions) == 60          # the script prints this count


def test_load_transactions_adds_a_revenue_column():
    transactions = load_transactions(DATA_PATH)
    assert "revenue" in transactions.columns
    expected = transactions["Quantity"] * transactions["UnitPrice"]
    assert (transactions["revenue"] == expected).all()


def test_load_transactions_tidies_description_text():
    descriptions = load_transactions(DATA_PATH)["Description"]
    assert (descriptions == descriptions.str.strip()).all()


# --------------------------------------------------------------- clean

def test_clean_prices_keeps_the_rows_the_script_keeps():
    cleaned = clean_prices(load_transactions(DATA_PATH))
    assert len(cleaned) == 51               # the script prints this count


def test_clean_prices_does_not_mutate_its_input():
    transactions = load_transactions(DATA_PATH)
    rows_before = len(transactions)
    clean_prices(transactions)
    assert len(transactions) == rows_before


def test_clean_prices_on_an_empty_frame():
    empty = load_transactions(DATA_PATH).head(0)
    assert len(clean_prices(empty)) == 0


# ------------------------------------------------------------- country

def test_revenue_by_country_totals():
    cleaned = clean_prices(load_transactions(DATA_PATH))
    totals = revenue_by_country(cleaned)
    assert set(totals) == {"United Kingdom", "EIRE", "Netherlands"}
    assert totals["United Kingdom"] == pytest.approx(1220.07)
    assert sum(totals.values()) == pytest.approx(1385.40)


def test_revenue_by_country_on_an_empty_frame():
    empty = clean_prices(load_transactions(DATA_PATH)).head(0)
    assert revenue_by_country(empty) == {}


# ----------------------------------------------------------- customers

def test_top_customers_ranking():
    cleaned = clean_prices(load_transactions(DATA_PATH))
    top = top_customers(cleaned, 3)
    assert len(top) == 3
    totals = [total for _, total in top]
    assert totals == sorted(totals, reverse=True)
    first_id, first_total = top[0]
    assert first_id == 13089                # the script prints this ranking
    assert first_total == pytest.approx(868.26)


def test_top_customers_breaks_ties_by_smaller_id():
    # 999 spends 40 + 10 = 50, so all three customers tie at 50.0 exactly.
    frame = edge_frame([999, 999, 111, 555], [40.0, 10.0, 50.0, 50.0])
    top = top_customers(frame, 3)
    assert [customer_id for customer_id, _ in top] == [111, 555, 999]
    assert all(total == pytest.approx(50.0) for _, total in top)


def test_top_customers_when_n_exceeds_customer_count():
    frame = edge_frame([1, 2], [5.0, 7.0])
    top = top_customers(frame, 10)
    assert [customer_id for customer_id, _ in top] == [2, 1]


def test_top_customers_single_row():
    top = top_customers(edge_frame([42], [9.99]), 3)
    assert len(top) == 1
    customer_id, total = top[0]
    assert customer_id == 42
    assert total == pytest.approx(9.99)
