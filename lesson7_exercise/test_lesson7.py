"""Tests for the Lesson 7 database-design exercise.

These tests import from ``build_database.py`` -- the starter module you finish.
In its shipped state that module's two functions raise ``NotImplementedError``,
so every test below fails with that same instructive message until you implement
them. That is the intended starting point, not something you broke.

Run from inside lesson7_exercise/ :

    python3 -m pytest test_lesson7.py -v

The checker builds your database into a fresh temporary directory each run, so it
never leaves a file behind and never depends on a previous attempt.

Expected module contract (build_database.py):

    build_database(db_path, customers_csv, transactions_csv) -> sqlite3.Connection
        Create a brand-new SQLite database at ``db_path`` holding two tables and
        load the two CSVs into them. Return an OPEN connection that already has
        ``PRAGMA foreign_keys = ON`` set. The schema must declare:

          customers
            - customer_id : the PRIMARY KEY (unique, one row per customer)
            - country     : NOT NULL (a customer must have a country)

          transactions
            - transaction_id : the PRIMARY KEY
            - customer_id    : NOT NULL, and a FOREIGN KEY referencing
                               customers(customer_id)

        Keep every column the CSVs carry, so a whole row round-trips. Declare
        NOT NULL only where a property truly demands it (customers.country and
        transactions.customer_id); leave the descriptive columns nullable.
        After loading, customers has 10 rows and transactions has 60 rows -- the
        two course_data CSVs, unchanged.

    demonstrate_rejection(conn) -> str
        Attempt ONE insert that the schema must reject -- your choice of a
        duplicate primary key, a NULL in a NOT NULL column, or an orphan foreign
        key. Catch the sqlite3.IntegrityError and return ``str(err)``. Every
        SQLite integrity message contains the word "constraint". If no error is
        raised, the schema failed its job: raise AssertionError instead of
        returning.

The enforcement tests below copy one real row and break exactly one rule, then
insert it themselves -- so each test targets its own constraint no matter what
extra columns your schema carries.
"""

import sqlite3
from pathlib import Path

import pytest

from build_database import build_database, demonstrate_rejection

COURSE_DATA = Path(__file__).parent.parent / "course_data"
CUSTOMERS_CSV = COURSE_DATA / "lesson2_customers_base.csv"
TRANSACTIONS_CSV = COURSE_DATA / "lesson2_transactions_base.csv"

# A customer_id that is NOT in the customer table -- used for the orphan test.
ORPHAN_CUSTOMER_ID = "C00000"


@pytest.fixture
def conn(tmp_path):
    """A freshly built database, as an open connection, rebuilt for every test."""
    connection = build_database(
        db_path=str(tmp_path / "lesson7_exercise.sqlite"),
        customers_csv=str(CUSTOMERS_CSV),
        transactions_csv=str(TRANSACTIONS_CSV),
    )
    yield connection
    connection.close()


# ----------------------------------------------------------------- helpers

def columns(conn, table):
    """PRAGMA table_info as {name: {"notnull": int, "pk": int, "type": str}}."""
    info = {}
    for _cid, name, col_type, notnull, _default, pk in conn.execute(
        f"PRAGMA table_info({table})"
    ):
        info[name] = {"notnull": notnull, "pk": pk, "type": col_type}
    return info


def foreign_keys(conn, table):
    """PRAGMA foreign_key_list as a list of (from_column, ref_table, to_column)."""
    return [(row[3], row[2], row[4]) for row in conn.execute(f"PRAGMA foreign_key_list({table})")]


def one_row(conn, table):
    """Fetch one existing, valid row of ``table`` as a {column: value} dict."""
    names = list(columns(conn, table))
    values = conn.execute(f"SELECT {', '.join(names)} FROM {table} LIMIT 1").fetchone()
    return dict(zip(names, values))


def insert_row(conn, table, row):
    """Insert a {column: value} dict, naming every column explicitly."""
    names = list(row)
    placeholders = ", ".join("?" for _ in names)
    conn.execute(
        f"INSERT INTO {table} ({', '.join(names)}) VALUES ({placeholders})",
        tuple(row[name] for name in names),
    )


# --------------------------------------------------------------- schema: keys

def test_customers_customer_id_is_the_primary_key(conn):
    info = columns(conn, "customers")
    assert "customer_id" in info, "customers needs a customer_id column"
    assert info["customer_id"]["pk"] > 0, "customer_id must be the PRIMARY KEY"


def test_customers_country_is_not_null(conn):
    info = columns(conn, "customers")
    assert "country" in info, "customers needs a country column"
    assert info["country"]["notnull"] == 1, "country must be declared NOT NULL"


def test_transactions_transaction_id_is_the_primary_key(conn):
    info = columns(conn, "transactions")
    assert "transaction_id" in info, "transactions needs a transaction_id column"
    assert info["transaction_id"]["pk"] > 0, "transaction_id must be the PRIMARY KEY"


def test_transactions_customer_id_is_not_null(conn):
    info = columns(conn, "transactions")
    assert "customer_id" in info, "transactions needs a customer_id column"
    assert info["customer_id"]["notnull"] == 1, "transactions.customer_id must be NOT NULL"


def test_transactions_have_a_foreign_key_to_customers(conn):
    assert ("customer_id", "customers", "customer_id") in foreign_keys(conn, "transactions"), (
        "transactions.customer_id must be a FOREIGN KEY referencing customers(customer_id)"
    )


# --------------------------------------------------------------- row counts

def test_customers_row_count_is_10(conn):
    (count,) = conn.execute("SELECT COUNT(*) FROM customers").fetchone()
    assert count == 10


def test_transactions_row_count_is_60(conn):
    (count,) = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
    assert count == 60


# --------------------------------------------------- enforcement (checker acts)

def test_foreign_keys_are_enforced_on_the_connection(conn):
    # A real transaction row whose only defect is an orphan customer_id. It is
    # rejected only when the returned connection has PRAGMA foreign_keys = ON.
    row = one_row(conn, "transactions")
    row["transaction_id"] = "ORPHAN-1"          # unique -> no primary-key clash
    row["customer_id"] = ORPHAN_CUSTOMER_ID     # the one rule this row breaks
    with pytest.raises(sqlite3.IntegrityError) as caught:
        insert_row(conn, "transactions", row)
    conn.rollback()
    assert "foreign key" in str(caught.value).lower(), (
        "expected a FOREIGN KEY constraint failure; got: " + str(caught.value)
    )


def test_duplicate_primary_key_is_rejected(conn):
    # Re-insert a full, valid customer row: the only broken rule is the unique key.
    row = one_row(conn, "customers")
    with pytest.raises(sqlite3.IntegrityError) as caught:
        insert_row(conn, "customers", row)
    conn.rollback()
    assert "unique" in str(caught.value).lower()


def test_null_country_is_rejected(conn):
    # A real customer row with a fresh id but a blank country -> only NOT NULL breaks.
    row = one_row(conn, "customers")
    row["customer_id"] = "C99999"
    row["country"] = None
    with pytest.raises(sqlite3.IntegrityError) as caught:
        insert_row(conn, "customers", row)
    conn.rollback()
    assert "not null" in str(caught.value).lower()


# ------------------------------------------------ the student's own rejection

def test_demonstrate_rejection_reports_a_real_integrity_error(conn):
    before_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    before_transactions = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    message = demonstrate_rejection(conn)
    conn.rollback()  # clear any transaction the failed insert left open

    assert isinstance(message, str) and message, (
        "demonstrate_rejection must return the caught error message as a string"
    )
    assert "constraint" in message.lower(), (
        "the returned message should be a real sqlite3.IntegrityError "
        "(its text contains 'constraint'); got: " + message
    )
    # The rejected row must not have landed.
    assert conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == before_customers
    assert (
        conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] == before_transactions
    )
