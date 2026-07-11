"""Your finance toolbox — THIS FILE IS YOURS TO EDIT.

Real projects keep reusable logic in .py modules, not notebook cells: modules can
be imported anywhere, tested automatically, and diffed in code review. The
notebook imports from this file, and the grader tests it on synthetic data with
known answers (`grader.check_finance_module()`).

Workflow: implement a function below, save the file, rerun the check cell in the
notebook. Thanks to `%autoreload`, you do NOT need to restart the kernel.

Each docstring fully specifies the behavior — including the formula and the NaN
handling — so there is exactly one right answer.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def daily_returns(close: pd.DataFrame) -> pd.DataFrame:
    """Simple daily returns for each column of a wide price table.

    Formula: ``close.pct_change()`` — each value is (today / yesterday) - 1.
    The first row is NaN, because the first day has no "yesterday".

    Parameters
    ----------
    close : pd.DataFrame
        Wide price table: one column per ticker, dates as the index.

    Returns
    -------
    pd.DataFrame
        Same shape as ``close``; first row all NaN.
    """
    raise NotImplementedError("your code here")


def cumulative_return(returns: pd.DataFrame | pd.Series) -> pd.Series | float:
    """Total compounded return over the whole sample.

    Formula: ``(1 + returns).prod() - 1``.
    NaNs are ignored (pandas treats them as 0-length periods), so the leading
    NaN produced by ``pct_change`` is harmless.

    Example: daily returns [0.10, -0.10, 0.2222...] compound to 0.21
    (100 -> 110 -> 99 -> 121, i.e. +21% overall — NOT the sum of the returns).

    Parameters
    ----------
    returns : pd.DataFrame or pd.Series
        Periodic simple returns (e.g. from ``daily_returns``).

    Returns
    -------
    pd.Series (one value per column) if given a DataFrame, float if given a Series.
    """
    raise NotImplementedError("your code here")


def annualized_volatility(
    returns: pd.DataFrame | pd.Series, periods_per_year: int = 252
) -> pd.Series | float:
    """Annualized volatility: standard deviation of returns, scaled to a year.

    Formula: ``returns.std() * sqrt(periods_per_year)``.
    Uses the pandas default standard deviation (ddof=1), which skips NaNs.
    There are ~252 trading days in a year, hence the default.

    Parameters
    ----------
    returns : pd.DataFrame or pd.Series
        Periodic simple returns.
    periods_per_year : int
        Number of return periods in a year (252 for daily, 12 for monthly).

    Returns
    -------
    pd.Series (one value per column) if given a DataFrame, float if given a Series.
    """
    raise NotImplementedError("your code here")


def sharpe_ratio(
    returns: pd.DataFrame | pd.Series,
    risk_free_rate: float,
    periods_per_year: int = 252,
) -> pd.Series | float:
    """Sharpe ratio: excess return earned per unit of risk taken.

    Formula:
        (returns.mean() * periods_per_year - risk_free_rate)
        / annualized_volatility(returns, periods_per_year)

    ``risk_free_rate`` is ANNUAL and a decimal (0.03 means 3%). The mean skips
    NaNs (pandas default). Reuse your ``annualized_volatility`` — that's the
    point of putting these in a module.

    Returns
    -------
    pd.Series (one value per column) if given a DataFrame, float if given a Series.
    """
    raise NotImplementedError("your code here")


def max_drawdown(prices: pd.Series) -> float:
    """Maximum drawdown: the worst peak-to-trough loss, as a negative fraction.

    Formula: the most negative value of ``prices / prices.cummax() - 1``.

    Example: prices [100, 120, 60, 90] -> the peak was 120, the trough after it
    was 60, so the max drawdown is 60/120 - 1 = -0.5.

    Parameters
    ----------
    prices : pd.Series
        A price series (not returns!), dates as the index.

    Returns
    -------
    float
        A value <= 0 (0.0 only if prices never fall below a previous peak).
    """
    raise NotImplementedError("your code here")
