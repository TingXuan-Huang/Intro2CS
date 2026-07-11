"""Grading checks for "Four Formats, One Analysis".

Import in the notebook as:

    from utils import test as grader

Run the matching check cell after each task; call ``grader.summary()`` at the
end for your score. Design rules:

* Checks on downloaded data are structural/property-based (live data changes
  daily); checks on your ``utils/finance.py`` functions use tiny synthetic
  fixtures with known answers.
* A check never raises — a failed check prints a ❌ message and lets the
  notebook keep running. Re-running a check overwrites its previous result.
* Messages point at the problem, never at the solution. When stuck: hints.md.

(Do not import this as a bare top-level ``import test`` — always go through the
``utils`` package.)
"""
from __future__ import annotations

import functools
import importlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

_RESULTS: dict[str, bool] = {}

# Registry: id -> label shown in summary(). Order defines the summary table.
_ALL_CHECKS: dict[str, str] = {
    "0": "Part 0 — data files downloaded",
    "1.1": "Load CSV (DGS10)",
    "1.2": "Load JSON (portfolio -> flat trades)",
    "1.3": "Load Excel (macro, metadata skipped)",
    "1.4": "Load Parquet (stocks)",
    "2.1": "Clean stocks",
    "2.2": "Clean rates & macro",
    "3.1": "Pivot + returns warm-up",
    "3.2 module": "utils/finance.py functions",
    "3.3": "Volatility & Sharpe",
    "3.4": "Max drawdown",
    "3.5": "Portfolio valuation (JSON ⋈ Parquet)",
    "3.6": "Macro correlation (Excel ⋈ Parquet)",
    "4": "Format benchmark",
}

_EXPECTED_TICKERS = {"AAPL", "MSFT", "SPY"}


def _register(task_id: str):
    """Wrap a check: print ✅/❌, record the result, never raise."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                message = fn(*args, **kwargs)
            except AssertionError as exc:
                _RESULTS[task_id] = False
                print(f"❌ {task_id}: {exc}")
                print(f"   (Stuck? hints.md → {task_id.split()[0]})")
            except NotImplementedError:
                _RESULTS[task_id] = False
                print(
                    f"❌ {task_id}: a function in utils/finance.py is not implemented "
                    "yet — open the file, replace the NotImplementedError, save, rerun."
                )
            except Exception as exc:  # Ellipsis placeholders, undefined vars, etc.
                _RESULTS[task_id] = False
                print(
                    f"❌ {task_id}: looks like this task isn't attempted yet, or an "
                    f"earlier step went wrong ({type(exc).__name__}: {exc})."
                )
            else:
                _RESULTS[task_id] = True
                print(f"✅ {task_id} passed — {message}")

        return wrapper

    return decorator


def _is_dataframe(obj, name: str) -> None:
    assert isinstance(obj, pd.DataFrame), (
        f"`{name}` should be a DataFrame, got {type(obj).__name__} — "
        "did you complete the TODO above?"
    )


# ---------------------------------------------------------------------------
# Part 0
# ---------------------------------------------------------------------------

@_register("0")
def check_0_data_files():
    data = Path("data")
    # portfolio.json is a small fixed file by design; the others carry years of data.
    for name, min_bytes in (
        ("DGS10.csv", 1024),
        ("portfolio.json", 200),
        ("fred_macro.xlsx", 1024),
        ("stock_market.parquet", 1024),
    ):
        path = data / name
        assert path.exists(), (
            f"data/{name} is missing. Run the download cells above — or, if downloads "
            "fail, uncomment the use_offline_data() cell."
        )
        assert path.stat().st_size > min_bytes, (
            f"data/{name} is under 1 KB — the download probably failed halfway. "
            "Delete it and re-run the download cell (or switch to offline data)."
        )
    first_line = (data / "DGS10.csv").read_text().splitlines()[0]
    assert "DATE" in first_line.upper(), (
        "data/DGS10.csv doesn't start with the expected header — re-run download_fred_csv()."
    )
    payload = json.loads((data / "portfolio.json").read_text())
    assert "holdings" in payload, (
        "data/portfolio.json parsed, but has no 'holdings' key — re-run write_portfolio_json()."
    )
    return "all four files are in data/ and look plausible."


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------

@_register("1.1")
def check_1_1(rates):
    _is_dataframe(rates, "rates")
    df = rates
    if "DATE" not in df.columns and df.index.name == "DATE":
        df = df.reset_index()  # accept DATE as index too
    assert {"DATE", "DGS10"} <= set(df.columns), (
        f"expected columns DATE and DGS10, found {list(df.columns)} — "
        "reload data/DGS10.csv without renaming anything."
    )
    assert pd.api.types.is_datetime64_any_dtype(df["DATE"]), (
        "DATE is not a datetime yet — read_csv can parse dates for you at load "
        "time (check its arguments)."
    )
    assert pd.api.types.is_float_dtype(df["DGS10"]), (
        f"DGS10 is dtype '{df['DGS10'].dtype}', not float. Something in the raw file "
        "is preventing numeric parsing — open data/DGS10.csv in a text editor and "
        "look at the value column closely."
    )
    assert len(df) >= 500, (
        f"only {len(df)} rows — that's fewer than expected. Don't drop rows at load "
        "time; missing values should become NaN, not disappear."
    )
    n_missing = int(df["DGS10"].isna().sum())
    assert n_missing > 0, (
        "DGS10 has zero missing values, but FRED marks market holidays with a "
        "special non-numeric marker. If pandas saw none of them, they weren't "
        "handled at load time — look at the raw file again."
    )
    values = df["DGS10"].dropna()
    assert ((values > 0) & (values < 20)).all(), (
        "some DGS10 values are outside the plausible (0, 20)% range — the file may "
        "have been parsed incorrectly."
    )
    return f"DGS10 is float64 with {n_missing} missing values correctly detected."


@_register("1.2")
def check_1_2(trades):
    _is_dataframe(trades, "trades")
    assert len(trades) >= 4, (
        f"only {len(trades)} rows — there are 4 trades in the file. record_path "
        "should give one row per TRADE, not per holding."
    )
    ticker_col = next(
        (c for c in ("ticker", "holding_ticker") if c in trades.columns), None
    )
    assert ticker_col is not None, (
        f"couldn't find a ticker column in {list(trades.columns)} — pass the "
        "holding-level fields to json_normalize's meta= argument."
    )
    assert {"date", "shares", "price"} <= set(trades.columns), (
        f"expected trade-level columns date/shares/price, found {list(trades.columns)}."
    )
    assert set(trades[ticker_col].unique()) == _EXPECTED_TICKERS, (
        f"tickers are {sorted(trades[ticker_col].unique())} — expected exactly "
        f"{sorted(_EXPECTED_TICKERS)}."
    )
    total = int(pd.to_numeric(trades["shares"]).sum())
    assert total == 115, (
        f"trade shares sum to {total}, expected 115 — check that each row is one "
        "trade and no rows are duplicated or lost."
    )
    for col in trades.columns:
        assert not trades[col].map(lambda v: isinstance(v, (dict, list))).any(), (
            f"column '{col}' still contains nested dicts/lists — the table isn't "
            "flat yet. json_normalize's record_path= should unpack the trades."
        )
    return "the nested JSON became a flat table: one row per trade, holding info carried along."


@_register("1.3")
def check_1_3(macro):
    _is_dataframe(macro, "macro")
    assert pd.api.types.is_datetime64_any_dtype(macro.index), (
        "the index is not datetime — parse observation_date and set it as the index."
    )
    assert not macro.index.isna().any(), (
        "the index contains NaT — metadata rows probably leaked into the data. "
        "Look at what the first few rows of the sheet actually contain."
    )
    assert macro.index.is_monotonic_increasing, "the date index is not sorted ascending."
    gaps = macro.index.to_series().diff().dropna().dt.days
    assert gaps.between(25, 35).all(), (
        "the index doesn't step month-by-month — some non-data rows may have "
        "slipped in."
    )
    assert {"CPIAUCSL", "UNRATE"} <= set(macro.columns), (
        f"expected columns CPIAUCSL and UNRATE, found {list(macro.columns)} — if "
        "you see metadata text as column names, the header row was misidentified."
    )
    assert not any("FRED" in str(c).upper() for c in macro.columns), (
        "a column name contains metadata text — skip the decorative rows so the "
        "real header (row 5) is used."
    )
    assert len(macro) >= 48, f"only {len(macro)} rows — expected at least 48 months."
    for col, lo, hi in (("CPIAUCSL", 200, 500), ("UNRATE", 2, 15)):
        assert pd.api.types.is_numeric_dtype(macro[col]), (
            f"{col} is not numeric — metadata junk is probably mixed into the column."
        )
        vals = macro[col].dropna()
        assert ((vals > lo) & (vals < hi)).all(), (
            f"some {col} values fall outside the plausible ({lo}, {hi}) range — "
            "check what got parsed into that column."
        )
    return f"macro is a clean monthly table ({len(macro)} months), metadata rows gone."


@_register("1.4")
def check_1_4(stocks):
    _is_dataframe(stocks, "stocks")
    expected = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    assert set(stocks.columns) == set(expected) and len(stocks.columns) == 7, (
        f"columns are {list(stocks.columns)} — expected exactly {expected}."
    )
    assert pd.api.types.is_datetime64_any_dtype(stocks["Date"]), (
        "Date is not datetime — interesting, Parquet should have preserved that. "
        "Did you load data/stock_market.parquet with read_parquet?"
    )
    upper = set(stocks["Ticker"].str.upper().unique())
    assert _EXPECTED_TICKERS <= upper, (
        f"expected tickers {sorted(_EXPECTED_TICKERS)}, found {sorted(upper)}."
    )
    ok_rows = stocks.dropna(subset=["High", "Low"])
    assert (ok_rows["High"] >= ok_rows["Low"]).all(), (
        "some rows have High < Low — that file did not load correctly."
    )
    assert len(stocks) >= 2000, f"only {len(stocks)} rows — expected at least 2000."
    return f"stocks loaded with {len(stocks)} rows and dtypes intact (no arguments needed)."


# ---------------------------------------------------------------------------
# Part 2
# ---------------------------------------------------------------------------

@_register("2.1")
def check_2_1(stocks_clean):
    _is_dataframe(stocks_clean, "stocks_clean")
    for col in ("Date", "Ticker", "Close"):
        assert col in stocks_clean.columns, f"column '{col}' is missing from stocks_clean."
    assert not stocks_clean.duplicated(subset=["Ticker", "Date"]).any(), (
        "there are still duplicate (Ticker, Date) rows — each ticker should have "
        "at most one row per day."
    )
    assert stocks_clean["Ticker"].str.isupper().all(), (
        "some tickers are still lowercase — 'aapl' and 'AAPL' are the same company "
        "but pandas doesn't know that."
    )
    assert set(stocks_clean["Ticker"].unique()) == _EXPECTED_TICKERS, (
        f"tickers are {sorted(stocks_clean['Ticker'].unique())} — expected exactly "
        f"{sorted(_EXPECTED_TICKERS)}."
    )
    assert stocks_clean["Close"].notna().all(), (
        "Close still contains NaN — after removing the outlier, fill the gaps "
        "with each ticker's previous price (careful: per ticker, not globally!)."
    )
    counts = stocks_clean.groupby("Ticker").size()
    assert counts.nunique() == 1, (
        f"row counts per ticker differ ({counts.to_dict()}) — cleaning should fix "
        "values, not drop different numbers of rows per ticker."
    )
    key = stocks_clean[["Ticker", "Date"]].reset_index(drop=True)
    assert key.equals(key.sort_values(["Ticker", "Date"]).reset_index(drop=True)), (
        "rows are not sorted by Ticker then Date — time-series logic (shift, "
        "ffill) silently breaks on unsorted data."
    )
    for ticker, grp in stocks_clean.groupby("Ticker"):
        closes = grp.sort_values("Date")["Close"]
        ratio = (closes / closes.shift()).dropna()
        assert ratio.max() < 3 and ratio.min() > 1 / 3, (
            f"{ticker} still has a day where Close jumps ×{ratio.max():.1f} (or "
            f"drops to ×{ratio.min():.2f}) versus the day before — a fat-finger "
            "price is still in there."
        )
    note = ""
    try:
        on_disk = pd.read_parquet("data/stock_market.parquet", columns=["Ticker"])
        if on_disk["Ticker"].str.isupper().all():
            note = (
                " ℹ️ The file on disk shows no injected chaos — if you skipped the "
                "chaos cell, the duplicate/casing parts of this check passed "
                "vacuously (structure was still verified)."
            )
    except Exception:
        pass
    return f"stocks_clean is deduplicated, consistently cased, gap-free and outlier-free.{note}"


@_register("2.2")
def check_2_2(rates_clean, macro_clean):
    rc = rates_clean
    if isinstance(rc, pd.Series):
        rc = rc.to_frame("DGS10")
    _is_dataframe(rc, "rates_clean")
    assert pd.api.types.is_datetime64_any_dtype(rc.index), (
        "rates_clean should be indexed by date."
    )
    assert rc.index.is_monotonic_increasing, "rates_clean is not sorted by date."
    assert "DGS10" in rc.columns, f"expected a DGS10 column, found {list(rc.columns)}."
    assert pd.api.types.is_float_dtype(rc["DGS10"]), "DGS10 should be float."
    assert rc["DGS10"].notna().all(), (
        "DGS10 still has NaN — markets were closed those days, so carry the "
        "previous value forward."
    )
    _is_dataframe(macro_clean, "macro_clean")
    assert "UNRATE" in macro_clean.columns, "macro_clean should still have UNRATE."
    assert macro_clean["UNRATE"].notna().all(), (
        "UNRATE still has NaN — interpolate() can estimate the gaps from the "
        "neighboring months."
    )
    assert len(macro_clean) >= 48, (
        f"macro_clean has {len(macro_clean)} rows — nothing should have been "
        "dropped, only filled."
    )
    return "rates forward-filled and UNRATE interpolated — nothing was dropped."


# ---------------------------------------------------------------------------
# Part 3
# ---------------------------------------------------------------------------

@_register("3.1")
def check_3_1(close, daily_ret, cum_ret):
    _is_dataframe(close, "close")
    assert set(close.columns) == _EXPECTED_TICKERS, (
        f"close should have one column per ticker {sorted(_EXPECTED_TICKERS)}, "
        f"found {list(close.columns)} — pivot with columns='Ticker'."
    )
    assert pd.api.types.is_datetime64_any_dtype(close.index), (
        "close should be indexed by Date (pivot with index='Date')."
    )
    assert close.notna().all().all(), (
        "close contains NaN — did you pivot the *cleaned* table (stocks_clean)?"
    )
    _is_dataframe(daily_ret, "daily_ret")
    assert daily_ret.shape == close.shape, (
        f"daily_ret has shape {daily_ret.shape}, expected {close.shape} — one "
        "return per price."
    )
    assert daily_ret.iloc[0].isna().all(), (
        "the first row of daily_ret should be all NaN (no previous day to compare to)."
    )
    body = daily_ret.iloc[1:]
    assert ((body > -0.5) & (body < 0.5)).all().all(), (
        "some daily returns exceed ±50% — real large-caps don't do that; check "
        "the cleaning steps."
    )
    assert isinstance(cum_ret, pd.Series) and len(cum_ret) == 3, (
        "cum_ret should be a Series with one value per ticker."
    )
    for ticker in _EXPECTED_TICKERS:
        expected = close[ticker].iloc[-1] / close[ticker].iloc[0] - 1
        assert np.isclose(cum_ret[ticker], expected, rtol=1e-6), (
            f"cum_ret['{ticker}'] = {cum_ret[ticker]:.4f} doesn't match the "
            f"compounded price path ({expected:.4f}) — returns must be "
            "compounded (multiplied), not summed."
        )
    winner = cum_ret.idxmax()
    return f"prices pivoted and returns compound correctly (best performer: {winner})."


def _module_subtest(name: str, fn) -> bool:
    """Run one synthetic-fixture test; print an indented per-function line."""
    try:
        fn()
    except NotImplementedError:
        print(f"   ⏳ {name}: not implemented yet")
        return False
    except AssertionError as exc:
        print(f"   ❌ {name}: {exc}")
        return False
    except Exception as exc:
        print(f"   ❌ {name}: raised {type(exc).__name__}: {exc}")
        return False
    print(f"   ✅ {name}")
    return True


@_register("3.2 module")
def check_finance_module():
    import utils.finance as finance

    importlib.reload(finance)

    # Synthetic fixtures with hand-computed answers.
    prices = pd.Series([100.0, 110.0, 99.0, 121.0])
    expected_returns = pd.Series([np.nan, 0.10, -0.10, 22.0 / 99.0])
    dd_prices = pd.Series([100.0, 120.0, 60.0, 90.0])

    def t_daily_returns():
        out = finance.daily_returns(pd.DataFrame({"X": prices, "Y": prices * 2}))
        assert isinstance(out, pd.DataFrame), "should return a DataFrame"
        pd.testing.assert_series_equal(
            out["X"], expected_returns, rtol=1e-6, check_names=False
        )
        pd.testing.assert_series_equal(
            out["Y"], expected_returns, rtol=1e-6, check_names=False
        )

    def t_cumulative_return():
        got = finance.cumulative_return(expected_returns)
        assert np.isclose(got, 0.21, rtol=1e-6), (
            f"prices 100→110→99→121 mean +21% overall, got {got:.4f} "
            "(compound the returns, don't sum them; the leading NaN must not break it)"
        )
        as_df = finance.cumulative_return(pd.DataFrame({"X": expected_returns}))
        assert isinstance(as_df, pd.Series) and np.isclose(as_df["X"], 0.21, rtol=1e-6), (
            "a DataFrame input should give a Series of per-column results"
        )

    def t_annualized_volatility():
        expected = float(np.nanstd(expected_returns.to_numpy(), ddof=1) * np.sqrt(252))
        got = finance.annualized_volatility(expected_returns)
        assert np.isclose(got, expected, rtol=1e-6), (
            f"expected {expected:.4f}, got {got:.4f} — use the sample std (pandas "
            "default) and scale by sqrt(periods_per_year)"
        )
        monthly = finance.annualized_volatility(expected_returns, periods_per_year=12)
        assert np.isclose(
            monthly, float(np.nanstd(expected_returns.to_numpy(), ddof=1) * np.sqrt(12)),
            rtol=1e-6,
        ), "periods_per_year must not be hardcoded to 252"

    def t_sharpe_ratio():
        vol = float(np.nanstd(expected_returns.to_numpy(), ddof=1) * np.sqrt(252))
        expected = (float(np.nanmean(expected_returns.to_numpy())) * 252 - 0.03) / vol
        got = finance.sharpe_ratio(expected_returns, risk_free_rate=0.03)
        assert np.isclose(got, expected, rtol=1e-6), (
            f"expected {expected:.4f}, got {got:.4f} — annualize the mean return "
            "(×periods_per_year), subtract the annual risk-free rate, divide by "
            "annualized volatility"
        )

    def t_max_drawdown():
        got = finance.max_drawdown(dd_prices)
        assert np.isclose(got, -0.5, rtol=1e-6), (
            f"prices [100, 120, 60, 90]: peak 120 → trough 60 is a -50% drawdown, "
            f"got {got:.4f}"
        )
        assert finance.max_drawdown(pd.Series([1.0, 2.0, 3.0])) <= 0, (
            "a monotonically rising series has drawdown 0.0"
        )

    print("Testing utils/finance.py on synthetic data with known answers:")
    results = [
        _module_subtest("daily_returns", t_daily_returns),
        _module_subtest("cumulative_return", t_cumulative_return),
        _module_subtest("annualized_volatility", t_annualized_volatility),
        _module_subtest("sharpe_ratio", t_sharpe_ratio),
        _module_subtest("max_drawdown", t_max_drawdown),
    ]
    n_ok = sum(results)
    assert n_ok == len(results), (
        f"{n_ok}/{len(results)} functions correct so far — fix the ones flagged "
        "above, save the file, and rerun this cell (autoreload picks it up)."
    )
    return "all 5 functions in utils/finance.py behave correctly on known answers."


@_register("3.3")
def check_3_3(vol, sharpe, rf):
    assert isinstance(rf, float), (
        f"rf should be a plain annual rate as a float, got {type(rf).__name__}."
    )
    assert 0 < rf < 0.15, (
        f"rf = {rf:.4f} is not a plausible annual risk-free rate — remember DGS10 "
        "is quoted in percent (3.5 means 3.5%), your functions want a decimal."
    )
    for name, series, lo, hi in (("vol", vol, 0.05, 1.0), ("sharpe", sharpe, -3, 5)):
        assert isinstance(series, pd.Series) and len(series) == 3, (
            f"{name} should be a Series with one value per ticker."
        )
        assert ((series > lo) & (series < hi)).all(), (
            f"some {name} values are outside the plausible ({lo}, {hi}) range: "
            f"{series.round(3).to_dict()}."
        )
    implied_mean = sharpe * vol + rf  # annualized mean return each ticker implies
    assert ((implied_mean > -0.5) & (implied_mean < 1.0)).all(), (
        "vol, sharpe and rf are individually plausible but mutually inconsistent — "
        "check that all three use ANNUAL units."
    )
    return "volatility and Sharpe ratios are plausible and mutually consistent."


@_register("3.4")
def check_3_4(mdd, close=None):
    assert isinstance(mdd, pd.Series) and len(mdd) == 3, (
        "mdd should be a Series with one value per ticker."
    )
    assert ((mdd >= -1) & (mdd < 0)).all(), (
        f"drawdowns must be in [-1, 0): {mdd.round(3).to_dict()} — a drawdown is a "
        "negative fraction (and every real asset has at least one down day)."
    )
    if close is not None:
        ticker = sorted(close.columns)[0]
        direct = float((close[ticker] / close[ticker].cummax() - 1).min())
        assert np.isclose(mdd[ticker], direct, rtol=1e-6), (
            f"mdd['{ticker}'] = {mdd[ticker]:.4f} but the price path implies "
            f"{direct:.4f} — apply your max_drawdown to each column of close."
        )
    return f"max drawdowns look right (worst: {mdd.idxmin()} at {mdd.min():.1%})."


@_register("3.5")
def check_3_5(portfolio_df, close):
    _is_dataframe(portfolio_df, "portfolio_df")
    required = {"ticker", "shares", "cost_basis", "market_value", "pnl", "pnl_pct"}
    assert required <= set(portfolio_df.columns), (
        f"missing columns: {sorted(required - set(portfolio_df.columns))}."
    )
    assert len(portfolio_df) == 3, (
        f"{len(portfolio_df)} rows — expected one per holding (3)."
    )
    pf = portfolio_df.set_index("ticker")
    assert set(pf.index) == _EXPECTED_TICKERS, (
        f"tickers are {sorted(pf.index)} — expected {sorted(_EXPECTED_TICKERS)}."
    )
    expected_shares = {"AAPL": 50, "MSFT": 25, "SPY": 40}
    expected_basis = {"AAPL": 6599.70, "MSFT": 5810.50, "SPY": 14751.60}
    latest = close.iloc[-1]
    for ticker in sorted(_EXPECTED_TICKERS):
        row = pf.loc[ticker]
        assert int(row["shares"]) == expected_shares[ticker], (
            f"{ticker}: shares = {row['shares']}, expected {expected_shares[ticker]} "
            "(the holding-level share count)."
        )
        assert np.isclose(row["cost_basis"], expected_basis[ticker], rtol=1e-4), (
            f"{ticker}: cost_basis = {row['cost_basis']:.2f}, expected "
            f"{expected_basis[ticker]:.2f} — the cost basis lives in the TRADES: "
            "sum shares × price over each holding's trades."
        )
        expected_mv = expected_shares[ticker] * float(latest[ticker])
        assert np.isclose(row["market_value"], expected_mv, rtol=1e-4), (
            f"{ticker}: market_value = {row['market_value']:.2f}, expected shares × "
            f"latest close = {expected_mv:.2f} — use the LAST row of close."
        )
        assert np.isclose(row["pnl"], row["market_value"] - row["cost_basis"], rtol=1e-6), (
            f"{ticker}: pnl should be market_value − cost_basis."
        )
        assert np.isclose(
            row["pnl_pct"], row["pnl"] / row["cost_basis"], rtol=1e-4
        ) or np.isclose(row["pnl_pct"], 100 * row["pnl"] / row["cost_basis"], rtol=1e-4), (
            f"{ticker}: pnl_pct should be pnl relative to cost basis."
        )
    total_pnl = float(portfolio_df["pnl"].sum())
    return f"portfolio valued correctly (total unrealized P&L: {total_pnl:,.2f})."


@_register("3.6")
def check_3_6(corr):
    assert isinstance(corr, float), (
        f"corr should be a single float, got {type(corr).__name__} — .corr() "
        "between two aligned Series gives one number."
    )
    assert not np.isnan(corr), (
        "corr is NaN — the two series probably didn't align on the same dates. "
        "Compare their indexes before correlating."
    )
    assert -1 <= corr <= 1, f"corr = {corr} is not a valid correlation."
    return f"correlation computed: {corr:.3f} (interpret it — and its limits — in the markdown)."


# ---------------------------------------------------------------------------
# Part 4
# ---------------------------------------------------------------------------

@_register("4")
def check_4(results_df):
    _is_dataframe(results_df, "results_df")
    required = {"format", "write_s", "read_s", "size_kb", "date_dtype_survives"}
    assert required <= set(results_df.columns), (
        f"missing columns: {sorted(required - set(results_df.columns))}."
    )
    assert len(results_df) == 4, f"{len(results_df)} rows — expected one per format (4)."
    fmts = set(results_df["format"])
    assert fmts == {"csv", "json", "xlsx", "parquet"}, (
        f"formats are {sorted(fmts)} — expected csv, json, xlsx, parquet."
    )
    res = results_df.set_index("format")
    for col in ("write_s", "read_s"):
        vals = pd.to_numeric(res[col], errors="coerce")
        assert vals.notna().all() and (vals >= 0).all(), (
            f"{col} contains non-numeric or negative values — time with "
            "time.perf_counter() around the call."
        )
    sizes = pd.to_numeric(res["size_kb"], errors="coerce")
    assert sizes.notna().all() and (sizes > 0).all(), (
        "size_kb must be positive numbers — os.path.getsize gives bytes; convert."
    )
    surv = res["date_dtype_survives"]
    assert surv.map(lambda v: isinstance(v, (bool, np.bool_))).all(), (
        "date_dtype_survives should be True/False — use "
        "pd.api.types.is_datetime64_any_dtype on the reloaded Date column."
    )
    assert bool(surv["parquet"]), (
        "parquet should preserve the datetime dtype — reload and check again."
    )
    # Excel stores real date cells, so the dtype survives the round trip — verified
    # stable on pandas 2.3 and 3.0. A nuance the simple theory table misses!
    assert bool(surv["xlsx"]), (
        "xlsx reports the Date dtype did NOT survive — pandas writes real date "
        "cells to Excel, so it should. Reload it exactly as the scaffold does."
    )
    for fmt in ("csv", "json"):
        assert not bool(surv[fmt]), (
            f"{fmt} reports the Date dtype survived — but {fmt} stores no type "
            "metadata. Reload it exactly as the scaffold does and re-check."
        )
    assert float(sizes["parquet"]) < float(sizes["json"]), (
        "parquet should be smaller than json (json repeats every key on every row)."
    )
    return "benchmark table is complete — now compare it with the theory table above."


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def summary() -> None:
    """Print the full check registry with ✅ / ❌ / – and the final score."""
    width = max(len(label) for label in _ALL_CHECKS.values()) + 2
    print("=" * (width + 18))
    print(" Four Formats, One Analysis — score summary")
    print("=" * (width + 18))
    passed = 0
    for check_id, label in _ALL_CHECKS.items():
        state = _RESULTS.get(check_id)
        if state is True:
            icon, passed = "✅", passed + 1
        elif state is False:
            icon = "❌"
        else:
            icon = "–  (not run)"
        print(f" {check_id:<12} {label:<{width}} {icon}")
    print("-" * (width + 18))
    print(f" Score: {passed}/{len(_ALL_CHECKS)} checks passed")
    if passed < len(_ALL_CHECKS):
        print(" Rerun any failed task's cell and its ✅ cell — results update in place.")
    else:
        print(" 🏆 Full marks — every format bent to your will.")
