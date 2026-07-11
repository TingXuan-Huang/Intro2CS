"""Deterministic builder for the assignment's SQLite database.

The whole assignment runs against one small SQLite file. This module builds it
from the pinned source extracts in ``data_source/`` plus a short, explicit list
of teaching fixtures, so the database is byte-for-byte reproducible on any
machine with no network access.

Public function:

    build_database(db_path="data/retail.sqlite", n_big=1000) -> Path
        (Re)create the database at ``db_path``. Overwrites any existing file so a
        rerun always yields the same three tables.

Tables it creates
-----------------
customers          12 rows.  10 real customers from the UCI Online Retail
                   extract, PLUS two authored teaching fixtures (C99001,
                   C99002) who have NO transactions — so a LEFT JOIN + IS NULL
                   has real rows to find. customer_id is the PRIMARY KEY.

transactions       61 rows.  60 real transaction lines from the same extract,
                   PLUS one authored teaching fixture: an EXACT duplicate of the
                   first line (transaction_id '536381-01') — so ROW_NUMBER()
                   de-duplication has something to bite on. transaction_id is
                   deliberately NOT unique here: raw staging data has duplicates,
                   and pretending otherwise is how double-counting bugs are born.

transactions_big   60 * n_big rows.  The 60 real lines replicated with unique
                   ids, used ONLY by the Part 3 benchmark (filtered SQL read vs
                   load-everything-into-pandas). Nothing else reads it.

Provenance and honest labelling of the fixtures live in ``manifest.json``.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

# transaction lines whose transaction_id is duplicated in the raw data (the
# authored fixture). The assignment's drill D2 rediscovers this from scratch.
DUPLICATE_TRANSACTION_ID = "536381-01"

# The two authored "customer with no orders" fixtures.
NO_ORDER_CUSTOMERS = [
    {
        "customer_id": "C99001",
        "customer_label": "Customer 99001",
        "country": "United Kingdom",
        "first_purchase_date": "2011-02-01",
    },
    {
        "customer_id": "C99002",
        "customer_label": "Customer 99002",
        "country": "EIRE",
        "first_purchase_date": "2011-03-15",
    },
]

_CUSTOMERS_DDL = """
CREATE TABLE customers (
    customer_id         TEXT PRIMARY KEY,
    customer_label      TEXT,
    country             TEXT,
    first_purchase_date TEXT
)
"""

# Note: NO primary key on transaction_id — the raw data contains one duplicate,
# and a PRIMARY KEY would reject it. Modelling raw data honestly is the point.
_TRANSACTIONS_DDL = """
CREATE TABLE {name} (
    transaction_id   TEXT,
    customer_id      TEXT,
    transaction_date TEXT,
    product          TEXT,
    quantity         INTEGER,
    unit_price       REAL,
    source_country   TEXT
)
"""

_TX_COLUMNS = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "product",
    "quantity",
    "unit_price",
    "source_country",
]

_CUST_COLUMNS = ["customer_id", "customer_label", "country", "first_purchase_date"]


def _source_dir() -> Path:
    """Locate the pinned CSV extracts, wherever this package was copied to."""
    return Path(__file__).resolve().parent.parent / "data_source"


def _load_sources() -> tuple[pd.DataFrame, pd.DataFrame]:
    src = _source_dir()
    customers = pd.read_csv(src / "customers_base.csv", dtype=str)
    transactions = pd.read_csv(
        src / "transactions_base.csv",
        dtype={
            "transaction_id": str,
            "customer_id": str,
            "transaction_date": str,
            "product": str,
            "source_country": str,
        },
    )
    transactions["quantity"] = transactions["quantity"].astype(int)
    transactions["unit_price"] = transactions["unit_price"].astype(float)
    return customers, transactions


def build_database(db_path: str | Path = "data/retail.sqlite", n_big: int = 1000) -> Path:
    """Build the assignment database deterministically. Overwrites if present."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    customers_base, transactions_base = _load_sources()

    # customers = real + two authored no-order fixtures
    customers = pd.concat(
        [customers_base[_CUST_COLUMNS], pd.DataFrame(NO_ORDER_CUSTOMERS)[_CUST_COLUMNS]],
        ignore_index=True,
    )

    # transactions = real + one authored exact-duplicate line
    dup = transactions_base[
        transactions_base["transaction_id"] == DUPLICATE_TRANSACTION_ID
    ]
    transactions = pd.concat(
        [transactions_base[_TX_COLUMNS], dup[_TX_COLUMNS]], ignore_index=True
    )

    # transactions_big = benchmark fuel: n_big unique-id copies of the 60 lines
    big_frames = []
    for i in range(n_big):
        chunk = transactions_base[_TX_COLUMNS].copy()
        chunk["transaction_id"] = chunk["transaction_id"] + f"-{i:04d}"
        big_frames.append(chunk)
    transactions_big = pd.concat(big_frames, ignore_index=True)

    con = sqlite3.connect(db_path)
    try:
        con.execute(_CUSTOMERS_DDL)
        con.execute(_TRANSACTIONS_DDL.format(name="transactions"))
        con.execute(_TRANSACTIONS_DDL.format(name="transactions_big"))
        con.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?)",
            customers[_CUST_COLUMNS].itertuples(index=False, name=None),
        )
        con.executemany(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)",
            transactions[_TX_COLUMNS].itertuples(index=False, name=None),
        )
        con.executemany(
            "INSERT INTO transactions_big VALUES (?, ?, ?, ?, ?, ?, ?)",
            transactions_big[_TX_COLUMNS].itertuples(index=False, name=None),
        )
        con.commit()
    finally:
        con.close()

    print(
        f"Built {db_path} — customers: {len(customers)} rows, "
        f"transactions: {len(transactions)} rows "
        f"({transactions['transaction_id'].nunique()} distinct ids, "
        "1 authored duplicate), "
        f"transactions_big: {len(transactions_big)} rows (benchmark only)."
    )
    return db_path


if __name__ == "__main__":
    build_database()
