"""Starter functions for Lesson 10 — Spark and distributed DataFrames.

Run ``python3 -m pytest test_lesson10.py -v`` from this folder after installing
PySpark and a supported Java runtime. Each function receives Spark DataFrames
with the columns supplied by the course retail CSVs and returns a Spark
DataFrame. Do not call ``collect()`` or convert the result to pandas here: that
would pull distributed results back to the driver before the caller asks for it.
"""

from pyspark.sql import functions as F
from pyspark.sql.window import Window


def monthly_revenue_by_country(transactions, customers):
    """Return country/month revenue and line-item counts.

    Join transactions to customers on ``customer_id``. Revenue is
    ``quantity * unit_price`` and month must be a ``YYYY-MM`` string derived
    from ``transaction_date``. Return exactly these columns, in this order:
    ``country``, ``month``, ``revenue``, ``line_items``. Sort the result by
    country then month. The result stays a Spark DataFrame.
    """
    raise NotImplementedError("implement monthly_revenue_by_country")


def customer_revenue_rank(transactions, customers):
    """Return each customer's revenue rank within its country.

    Join, calculate revenue, aggregate it by ``country`` and ``customer_id``,
    then assign a dense rank in descending revenue order within each country.
    Return exactly ``country``, ``customer_id``, ``revenue``, and
    ``revenue_rank``, sorted by country and rank. The result stays a Spark
    DataFrame.
    """
    raise NotImplementedError("implement customer_revenue_rank")
