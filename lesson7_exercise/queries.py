"""Lesson 7 exercise -- monthly revenue by country, twice.

You will compute ONE report two ways: once in SQL, once in pandas. The point of
the exercise is that they must agree exactly -- ``test_lesson7.py`` proves it with
``pandas.testing.assert_frame_equal``.

Fill in the two functions below. Do not change their names or signatures. See
README.md for the full contract and the exact commands to run.

The report -- "monthly revenue by country":
    * revenue of one line  = quantity * unit_price
    * month                = the 'YYYY-MM' part of transaction_date  (e.g. '2010-12')
    * one row per (month, country) pair
    * revenue rounded to 2 decimal places
    * sorted by month ascending, then country ascending

Both functions must return the SAME three columns, in this order, with these
names and types:
    month    : str   ('YYYY-MM')
    country  : str
    revenue  : float (rounded to 2 decimals)
"""

import pandas as pd  # noqa: F401  (you will need it in the pandas function)


def monthly_revenue_by_country_sql():
    """Return a SQL query STRING (do not run it here -- just return the text).

    The query runs against a table named ``transactions`` with columns:
        transaction_id, customer_id, transaction_date (TEXT 'YYYY-MM-DD'),
        product, quantity (INTEGER), unit_price (REAL), source_country (TEXT)

    It must produce exactly three output columns, named and ordered:
        month, country, revenue
    where ``month`` is the 'YYYY-MM' string, ``country`` is source_country, and
    ``revenue`` is SUM(quantity * unit_price) rounded to 2 decimals. One row per
    (month, country), sorted by month then country ascending.

    Hints (all from the lesson): strftime('%Y-%m', ...) for the month,
    ROUND(..., 2) for the revenue, GROUP BY the month and the country, ORDER BY
    month then country.
    """
    raise NotImplementedError(
        "Fill in monthly_revenue_by_country_sql(): return the SQL string. See README.md"
    )


def monthly_revenue_by_country_pandas(df):
    """Return the SAME report as a DataFrame, computed with pandas.

    ``df`` is the transactions table as a DataFrame (the columns listed above).
    Return a DataFrame with columns [month, country, revenue]:
        * month   -- the 'YYYY-MM' string cut from transaction_date
        * country -- source_country
        * revenue -- summed quantity * unit_price, rounded to 2 decimals
    one row per (month, country), sorted by month then country ascending, with a
    fresh 0..n-1 index (use reset_index(drop=True)). Do not mutate ``df``.
    """
    raise NotImplementedError(
        "Fill in monthly_revenue_by_country_pandas(): return the DataFrame. See README.md"
    )
