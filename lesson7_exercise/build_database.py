"""Lesson 7 exercise -- design a schema, load it, and prove it rejects bad data.

You will build a two-table SQLite database for the retail extract you have used
all through the course, and then make the database refuse one bad row on purpose.
This is Unit 2 in your own hands: a schema is Lesson 1's property checklist, and
here you are the one writing it down so the software can enforce it.

Fill in the two functions below. The checker (test_lesson7.py) describes the exact
contract; this file repeats it next to each TODO. Run the checker with:

    python3 -m pytest test_lesson7.py -v

and run THIS file directly to see your own rejection message:

    python3 build_database.py

The course data lives one directory up, in course_data/ :
    lesson2_customers_base.csv    -> 10 customers
    lesson2_transactions_base.csv -> 60 transactions
"""

import sqlite3
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
COURSE_DATA = HERE.parent / "course_data"
DEFAULT_DB = HERE / "data" / "lesson7_exercise.sqlite"


def build_database(db_path, customers_csv, transactions_csv):
    """Create the database, load both CSVs, and return an OPEN connection.

    Requirements the checker enforces:

      * The connection you return must already have foreign keys switched on:
            conn.execute("PRAGMA foreign_keys = ON")
        (SQLite leaves this OFF by default, per connection -- see Unit 2.)

      * customers table
            customer_id  -> PRIMARY KEY   (unique label, one row per customer)
            country      -> NOT NULL      (a customer must have a country)
            keep the other CSV columns (customer_label, first_purchase_date) too,
            left nullable.

      * transactions table
            transaction_id -> PRIMARY KEY
            customer_id    -> NOT NULL and a FOREIGN KEY to customers(customer_id)
            keep the other CSV columns (transaction_date, product, quantity,
            unit_price, source_country) too, left nullable.

      * Load all 10 customers and all 60 transactions. Load customers FIRST, so
        that every transaction's customer_id already exists when the foreign key
        is checked.

    Returns:
        sqlite3.Connection -- open, foreign keys ON, both tables populated.

    Hints:
      * Start fresh: if db_path already exists, delete it, so a re-run is clean.
      * pandas.read_csv(...) reads a CSV into a DataFrame.
      * After you CREATE TABLE with your schema, df.to_sql(name, conn,
        if_exists="append", index=False) inserts the rows WITHOUT replacing the
        schema you just declared. (Plain to_sql without a pre-made table would
        invent its own schema with no keys -- exactly what Unit 3 warned about.)
    """
    # TODO: implement per the docstring above, then delete this line.
    raise NotImplementedError(
        "build_database is not implemented yet -- create the two tables with "
        "NOT NULL / PRIMARY KEY / FOREIGN KEY, load both CSVs, and return the "
        "open connection with PRAGMA foreign_keys = ON."
    )


def demonstrate_rejection(conn):
    """Attempt ONE insert the schema must reject, and return the error message.

    Pick any single violation you like:
      * a duplicate primary key (an id that already exists), or
      * a NULL in a NOT NULL column (e.g. a customer with no country), or
      * an orphan foreign key (a transaction for a customer that does not exist).

    Wrap the insert in try/except sqlite3.IntegrityError, and return str(err) --
    the caught message. Every SQLite integrity message contains the word
    "constraint" (for example "FOREIGN KEY constraint failed"), which is how the
    checker recognises a genuine rejection.

    If the insert unexpectedly SUCCEEDS, the schema has failed its one job:
    raise AssertionError rather than returning a message.

    Returns:
        str -- the caught sqlite3.IntegrityError message.
    """
    # TODO: implement per the docstring above, then delete this line.
    raise NotImplementedError(
        "demonstrate_rejection is not implemented yet -- attempt one bad insert, "
        "catch sqlite3.IntegrityError, and return its message as a string."
    )


if __name__ == "__main__":
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    connection = build_database(
        db_path=str(DEFAULT_DB),
        customers_csv=str(COURSE_DATA / "lesson2_customers_base.csv"),
        transactions_csv=str(COURSE_DATA / "lesson2_transactions_base.csv"),
    )
    customers = connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    transactions = connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print(f"loaded {customers} customers and {transactions} transactions into {DEFAULT_DB}")
    print("the database rejected a bad row:")
    print("  ", demonstrate_rejection(connection))
    connection.close()
