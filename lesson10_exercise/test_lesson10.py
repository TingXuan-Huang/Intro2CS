"""Offline checker for the Lesson 10 Spark exercise.

Run from ``lesson10_exercise/`` with ``python3 -m pytest test_lesson10.py -v``.
The test creates one local Spark session and reads only committed course CSVs;
it never contacts a cluster or the network.
"""

from pathlib import Path
import shutil

import pandas as pd
import pytest

if shutil.which("java") is None:
    pytest.exit(
        "Lesson 10 requires a local Java 17+ runtime. Install Java, then rerun this checker.",
        returncode=2,
    )

try:
    import pyspark  # noqa: F401
except ModuleNotFoundError:
    pytest.exit(
        "Lesson 10 requires pyspark. Run `pip install pyspark`, then rerun this checker.",
        returncode=2,
    )

import os
import sys

# Spark workers must run the same Python minor version as this driver; without
# this pin they spawn whatever `python3` is on PATH and fail on version skew.
os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

from pyspark.sql import SparkSession

from spark_queries import customer_revenue_rank, monthly_revenue_by_country

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("intro-cs-lesson10-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture
def retail_frames(spark):
    customers = pd.read_csv(ROOT / "course_data" / "lesson2_customers_base.csv")
    transactions = pd.read_csv(ROOT / "course_data" / "lesson2_transactions_base.csv")
    return spark.createDataFrame(transactions), spark.createDataFrame(customers)


def pandas_monthly_revenue_reference():
    customers = pd.read_csv(ROOT / "course_data" / "lesson2_customers_base.csv")
    transactions = pd.read_csv(
        ROOT / "course_data" / "lesson2_transactions_base.csv",
        parse_dates=["transaction_date"],
    )
    joined = transactions.merge(customers, on="customer_id")
    joined["month"] = joined["transaction_date"].dt.strftime("%Y-%m")
    joined["revenue"] = joined["quantity"] * joined["unit_price"]
    return (
        joined.groupby(["country", "month"], as_index=False)
        .agg(revenue=("revenue", "sum"), line_items=("transaction_id", "size"))
        .sort_values(["country", "month"])
        .reset_index(drop=True)
    )


def test_monthly_revenue_by_country_matches_pinned_values(retail_frames):
    transactions, customers = retail_frames
    actual = monthly_revenue_by_country(transactions, customers).toPandas()
    actual = actual.sort_values(["country", "month"]).reset_index(drop=True)
    expected = pd.DataFrame(
        [
            ("EIRE", "2010-12", 148.88, 6),
            ("Netherlands", "2010-12", 23.41, 6),
            ("United Kingdom", "2010-12", 1209.90, 36),
            ("United Kingdom", "2011-01", 17.06, 6),
            ("United Kingdom", "2011-08", 21.84, 6),
        ],
        columns=["country", "month", "revenue", "line_items"],
    )
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False, rtol=1e-9, atol=1e-9)
    pd.testing.assert_frame_equal(
        actual,
        pandas_monthly_revenue_reference(),
        check_dtype=False,
        rtol=1e-9,
        atol=1e-9,
    )


def test_customer_revenue_rank_matches_pinned_values(retail_frames):
    transactions, customers = retail_frames
    actual = customer_revenue_rank(transactions, customers).toPandas()
    actual = actual.sort_values(["country", "revenue_rank", "customer_id"]).reset_index(drop=True)
    expected = pd.DataFrame(
        [
            ("EIRE", "C14911", 148.88, 1),
            ("Netherlands", "C14646", 23.41, 1),
            ("United Kingdom", "C13089", 868.26, 1),
            ("United Kingdom", "C14298", 181.20, 2),
            ("United Kingdom", "C15311", 89.57, 3),
            ("United Kingdom", "C12748", 24.75, 4),
            ("United Kingdom", "C14606", 24.39, 5),
            ("United Kingdom", "C14096", 21.84, 6),
            ("United Kingdom", "C17841", 21.73, 7),
            ("United Kingdom", "C13263", 17.06, 8),
        ],
        columns=["country", "customer_id", "revenue", "revenue_rank"],
    )
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False, rtol=1e-9, atol=1e-9)


def test_queries_do_not_mutate_input_schemas(retail_frames):
    transactions, customers = retail_frames
    before_transactions = transactions.columns
    before_customers = customers.columns
    monthly_revenue_by_country(transactions, customers)
    customer_revenue_rank(transactions, customers)
    assert transactions.columns == before_transactions
    assert customers.columns == before_customers
