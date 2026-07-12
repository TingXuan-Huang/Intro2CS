"""Tests for the Lesson 8 SQL exercise.

These tests import the two functions YOU complete in ``queries.py`` and check
that your SQL report and your pandas report agree with each other and with a set
of reference numbers computed from the real data.

In the shipped starter, both functions ``raise NotImplementedError``, so every
test below ERRORS with that message until you implement them. That is the
intended starting state, not something you broke.

Run from inside lesson8_exercise/ :

    python3 -m pytest test_lesson8.py -v

What the tests need:

    * ``../course_data/lesson2_transactions_base.csv`` -- the 60 real rows.
      This checker builds its own SQLite database from that CSV, under
      ``lesson8_exercise/data/`` (gitignored), every run. You do not build it.

Expected contract (queries.py):

    monthly_revenue_by_country_sql() -> str
        A SQL query string. Run against a ``transactions`` table it returns
        columns [month, country, revenue]: month = strftime('%Y-%m',
        transaction_date), country = source_country, revenue =
        ROUND(SUM(quantity*unit_price), 2). One row per (month, country),
        ordered by month then country.

    monthly_revenue_by_country_pandas(transactions_df) -> pandas.DataFrame
        The SAME report from a DataFrame: columns [month, country, revenue],
        month as a 'YYYY-MM' string, revenue rounded to 2 decimals, one row per
        (month, country), sorted by month then country, index reset to 0..n-1.
        Must not mutate the input frame.

The reference numbers below were computed from the real 60-row extract and are
pinned on purpose. Decide what the report SHOULD be by reading the contract, not
by tweaking numbers until the test passes.
"""

import sqlite3
from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from queries import (
    monthly_revenue_by_country_pandas,
    monthly_revenue_by_country_sql,
)

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE.parent / "course_data" / "lesson2_transactions_base.csv"
DB_PATH = HERE / "data" / "lesson8_retail.sqlite"

# ---- Pinned reference values (computed from the real 60-row extract) --------
EXPECTED_ROWS = 5
EXPECTED_GRAND_TOTAL = 1421.09
EXPECTED_CELL = ("2010-12", "United Kingdom", 1209.90)
EXPECTED_COLUMNS = ["month", "country", "revenue"]


@pytest.fixture(scope="module")
def transactions_df():
    """The transactions table as a DataFrame (input to the pandas function)."""
    return pd.read_csv(CSV_PATH)


@pytest.fixture(scope="module")
def connection():
    """A SQLite connection whose ``transactions`` table is the real 60 rows.

    The database is rebuilt fresh under lesson8_exercise/data/ each run.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    pd.read_csv(CSV_PATH).to_sql("transactions", con, index=False, if_exists="replace")
    yield con
    con.close()


@pytest.fixture(scope="module")
def sql_result(connection):
    """The student's SQL report, run through pd.read_sql."""
    return pd.read_sql(monthly_revenue_by_country_sql(), connection)


@pytest.fixture(scope="module")
def pandas_result(transactions_df):
    """The student's pandas report."""
    return monthly_revenue_by_country_pandas(transactions_df)


# ---------------------------------------------------------- shape / columns

def test_sql_has_the_contracted_columns(sql_result):
    assert list(sql_result.columns) == EXPECTED_COLUMNS


def test_pandas_has_the_contracted_columns(pandas_result):
    assert list(pandas_result.columns) == EXPECTED_COLUMNS


def test_row_count(sql_result):
    assert len(sql_result) == EXPECTED_ROWS


# --------------------------------------------------- the two reports agree

def test_sql_and_pandas_agree(sql_result, pandas_result):
    # The whole point of the exercise: same report, two engines, identical frame.
    assert_frame_equal(sql_result, pandas_result)


# ---------------------------------------------------------- pinned numbers

def test_grand_total_revenue(sql_result):
    assert sql_result["revenue"].sum() == pytest.approx(EXPECTED_GRAND_TOTAL)


def test_one_specific_month_country_cell(sql_result):
    month, country, revenue = EXPECTED_CELL
    row = sql_result[(sql_result["month"] == month) & (sql_result["country"] == country)]
    assert len(row) == 1
    assert row["revenue"].iloc[0] == pytest.approx(revenue)


# ------------------------------------------------------------- properties

def test_month_is_a_yyyy_dash_mm_string(sql_result):
    first_month = sql_result["month"].iloc[0]
    assert isinstance(first_month, str)
    assert len(first_month) == 7 and first_month[4] == "-"


def test_sorted_by_month_then_country(pandas_result):
    ordered = pandas_result.sort_values(["month", "country"]).reset_index(drop=True)
    assert_frame_equal(pandas_result, ordered)


def test_pandas_index_is_reset(pandas_result):
    assert list(pandas_result.index) == list(range(len(pandas_result)))


def test_pandas_does_not_mutate_its_input(transactions_df):
    before = transactions_df.copy()
    monthly_revenue_by_country_pandas(transactions_df)
    assert_frame_equal(transactions_df, before)
