"""Grading checks for "One Analysis, Two Engines".

Import in the notebook as:

    from utils import test as grader

Run the matching check cell after each task; call ``grader.summary()`` at the
end for your score. Design rules (same house style as Assignment 1's grader):

* Every business question is answered TWICE — once in SQL (via ``pd.read_sql``)
  and once in pandas. Each check verifies BOTH engines against a pinned
  reference AND against each other. Two engines that disagree is itself a bug.
* A check never raises — a failed check prints a ❌ message and lets the notebook
  keep running. Re-running a check overwrites its previous result.
* Messages point at the problem, never at the answer. When stuck: hints.md.

(Do not import this as a bare top-level ``import test`` — always go through the
``utils`` package.)
"""
from __future__ import annotations

import functools
from pathlib import Path

import pandas as pd

_RESULTS: dict[str, bool] = {}

# Registry: id -> label shown in summary(). Order defines the summary table.
_ALL_CHECKS: dict[str, str] = {
    "0": "Database built (3 tables)",
    "1": "De-duplicated working set",
    "Q1": "Revenue by country (INNER JOIN)",
    "Q2": "Customers with no transactions (LEFT JOIN + IS NULL)",
    "Q3": "Customer count by spend band (CASE WHEN)",
    "Q4": "Top 3 customers by spend",
    "Q5": "Monthly revenue",
    "Q6": "Top customer per country (window)",
    "Q7": "Country revenue share (window)",
    "B": "Benchmark — filtered SQL vs load-everything",
    "D1": "Drill — 2nd highest customer",
    "D2": "Drill — find the duplicate transactions",
    "D3": "Drill — month-over-month revenue change",
    "D4": "Drill — longest gap between purchases",
}

# ---------------------------------------------------------------------------
# Pinned reference answers (canonical, sorted). Computed once, by hand-checked
# query, on the de-duplicated data (60 distinct transactions, 12 customers).
# ---------------------------------------------------------------------------
_REF = {
    "Q1": [("EIRE", 148.88), ("Netherlands", 23.41), ("United Kingdom", 1248.80)],
    "Q2": [("C99001",), ("C99002",)],
    "Q3": [("high", 1), ("low", 7), ("mid", 2)],
    "Q4": [("C13089", 868.26), ("C14298", 181.20), ("C14911", 148.88)],
    "Q5": [("2010-12", 1382.19), ("2011-01", 17.06), ("2011-08", 21.84)],
    "Q6": [
        ("EIRE", "C14911", 148.88),
        ("Netherlands", "C14646", 23.41),
        ("United Kingdom", "C13089", 868.26),
    ],
    "Q7": [
        ("EIRE", 148.88, 10.48),
        ("Netherlands", 23.41, 1.65),
        ("United Kingdom", 1248.80, 87.88),
    ],
    "D1": [("C14298", 181.20)],
    "D2": [("536381-01",)],
    "D3": [
        ("2010-12", 1382.19, None),
        ("2011-01", 17.06, -1365.13),
        ("2011-08", 21.84, 4.78),
    ],
    "D4": [("C12748", 3.0), ("C13089", 1.0)],
}

# Per-task output contract: required columns and which of them are floats.
_COLS = {
    "Q1": (["country", "revenue"], {"revenue"}),
    "Q2": (["customer_id"], set()),
    "Q3": (["band", "n_customers"], set()),
    "Q4": (["customer_id", "total"], {"total"}),
    "Q5": (["month", "revenue"], {"revenue"}),
    "Q6": (["country", "customer_id", "total"], {"total"}),
    "Q7": (["country", "revenue", "pct_of_total"], {"revenue", "pct_of_total"}),
    "D1": (["customer_id", "total"], {"total"}),
    "D2": (["transaction_id"], set()),
    "D3": (["month", "revenue", "mom_change"], {"revenue", "mom_change"}),
    "D4": (["customer_id", "longest_gap_days"], {"longest_gap_days"}),
}

_EXPECTED_TABLES = {"customers", "transactions", "transactions_big"}
_BENCHMARK_ROWS = 6000  # EIRE lines in transactions_big at the default n_big=1000


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
                print(f"   (Stuck? hints.md → {task_id})")
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
        "pd.read_sql returns a DataFrame, and your pandas answer should too."
    )


def _canon(df: pd.DataFrame, cols: list[str], float_cols: set[str]) -> list[tuple]:
    """Turn a result frame into a canonical, sorted list of tuples.

    String cells are stripped; float cells are rounded to 2 dp; NaN -> None.
    This makes a SQL frame and a pandas frame comparable regardless of row order,
    index, or int-vs-float dtype quibbles.
    """
    missing = [c for c in cols if c not in df.columns]
    assert not missing, (
        f"missing column(s) {missing} — the contract asks for exactly {cols}. "
        f"You returned {list(df.columns)}; rename with .rename(columns=...) "
        "(pandas) or AS aliases (SQL)."
    )
    rows: list[tuple] = []
    for _, r in df[cols].iterrows():
        row = []
        for c in cols:
            v = r[c]
            if c in float_cols:
                v = None if pd.isna(v) else round(float(v), 2)
            elif isinstance(v, str):
                v = v.strip()
            elif pd.isna(v):
                v = None
            row.append(v)
        rows.append(tuple(row))
    return sorted(rows, key=lambda t: tuple((x is None, x) for x in t))


def _rows_close(a: list[tuple], b: list[tuple], tol: float = 0.02) -> bool:
    if len(a) != len(b):
        return False
    for ra, rb in zip(a, b):
        if len(ra) != len(rb):
            return False
        for x, y in zip(ra, rb):
            if isinstance(x, float) or isinstance(y, float):
                if x is None or y is None:
                    if x is not y:
                        return False
                elif abs(float(x) - float(y)) > tol:
                    return False
            elif x != y:
                return False
    return True


def _two_engines(task_id: str, sql_df, pandas_df) -> None:
    """Shared verification: both frames match the reference and each other."""
    cols, float_cols = _COLS[task_id]
    reference = sorted(_REF[task_id], key=lambda t: tuple((x is None, x) for x in t))
    _is_dataframe(sql_df, f"{task_id}_sql")
    _is_dataframe(pandas_df, f"{task_id}_pandas")
    sql_rows = _canon(sql_df, cols, float_cols)
    pandas_rows = _canon(pandas_df, cols, float_cols)
    sql_ok = _rows_close(sql_rows, reference)
    pandas_ok = _rows_close(pandas_rows, reference)
    assert sql_ok, (
        f"the SQL answer ({len(sql_rows)} rows) doesn't match the reference "
        f"({len(reference)} rows). Check the query — did you de-duplicate, join, "
        "and aggregate exactly as the task asks?"
    )
    assert pandas_ok, (
        f"the pandas answer ({len(pandas_rows)} rows) doesn't match the reference "
        f"({len(reference)} rows). Your SQL may be right — make the pandas pipeline "
        "produce the SAME table."
    )
    assert _rows_close(sql_rows, pandas_rows), (
        "each engine is close to the reference but they disagree with EACH OTHER — "
        "usually a rounding or a de-duplication difference between the two."
    )


# ---------------------------------------------------------------------------
# Part 0 / Part 1
# ---------------------------------------------------------------------------

@_register("0")
def check_0_database(con) -> str:
    try:
        names = set(
            pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con)["name"]
        )
    except Exception as exc:  # noqa: BLE001
        raise AssertionError(
            f"couldn't query the database — is `con` an open sqlite3 connection? ({exc})"
        )
    missing = _EXPECTED_TABLES - names
    assert not missing, (
        f"missing table(s) {sorted(missing)} — run the build_database() cell in Part 0."
    )
    counts = {
        t: int(pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", con)["n"].iloc[0])
        for t in ("customers", "transactions")
    }
    assert counts["customers"] == 12, (
        f"customers has {counts['customers']} rows — expected 12 "
        "(10 real + 2 authored no-order fixtures)."
    )
    assert counts["transactions"] == 61, (
        f"transactions has {counts['transactions']} rows — expected 61 "
        "(60 real + 1 authored duplicate)."
    )
    return f"three tables present; customers=12, transactions=61 (as designed)."


@_register("1")
def check_1_dedup(tx) -> str:
    _is_dataframe(tx, "tx")
    needed = {"transaction_id", "customer_id", "quantity", "unit_price"}
    assert needed <= set(tx.columns), (
        f"tx is missing columns {sorted(needed - set(tx.columns))} — keep every "
        "column, just drop the duplicate ROW."
    )
    assert len(tx) == 60, (
        f"tx has {len(tx)} rows — expected 60. The raw table has 61 rows with one "
        "exact duplicate; de-duplicate it (SELECT DISTINCT / drop_duplicates())."
    )
    assert tx["transaction_id"].nunique() == 60, (
        "tx still has a repeated transaction_id — 60 rows but not 60 distinct ids."
    )
    return "working set is 60 distinct transactions — the duplicate is gone."


# ---------------------------------------------------------------------------
# Part 2 — business questions, two engines each
# ---------------------------------------------------------------------------

@_register("Q1")
def check_q1(q1_sql, q1_pandas) -> str:
    _two_engines("Q1", q1_sql, q1_pandas)
    return "revenue by country agrees across SQL and pandas (UK leads at 1248.80)."


@_register("Q2")
def check_q2(q2_sql, q2_pandas) -> str:
    _two_engines("Q2", q2_sql, q2_pandas)
    return "both engines find the 2 customers a LEFT JOIN keeps but INNER would drop."


@_register("Q3")
def check_q3(q3_sql, q3_pandas) -> str:
    _two_engines("Q3", q3_sql, q3_pandas)
    return "spend-band counts match (7 low, 2 mid, 1 high) in both engines."


@_register("Q4")
def check_q4(q4_sql, q4_pandas) -> str:
    _two_engines("Q4", q4_sql, q4_pandas)
    return "top-3 customers agree (C13089 far ahead at 868.26)."


@_register("Q5")
def check_q5(q5_sql, q5_pandas) -> str:
    _two_engines("Q5", q5_sql, q5_pandas)
    return "monthly revenue agrees across engines (Dec 2010 dominates)."


@_register("Q6")
def check_q6(q6_sql, q6_pandas) -> str:
    _two_engines("Q6", q6_sql, q6_pandas)
    return "top customer per country matches — the window kept one row per country."


@_register("Q7")
def check_q7(q7_sql, q7_pandas) -> str:
    _two_engines("Q7", q7_sql, q7_pandas)
    return "revenue shares agree and sum to ~100% (UK ≈ 87.9%)."


# ---------------------------------------------------------------------------
# Part 3 — benchmark
# ---------------------------------------------------------------------------

@_register("B")
def check_benchmark(results_df) -> str:
    _is_dataframe(results_df, "results_df")
    required = {"approach", "rows_returned", "seconds"}
    assert required <= set(results_df.columns), (
        f"missing columns: {sorted(required - set(results_df.columns))} — expected "
        "approach, rows_returned, seconds."
    )
    approaches = set(results_df["approach"])
    assert approaches == {"sql_filter", "pandas_filter"}, (
        f"approaches are {sorted(approaches)} — expected exactly "
        "'sql_filter' and 'pandas_filter'."
    )
    res = results_df.set_index("approach")
    for name in ("sql_filter", "pandas_filter"):
        rows = int(res.loc[name, "rows_returned"])
        assert rows == _BENCHMARK_ROWS, (
            f"{name} returned {rows} rows — expected {_BENCHMARK_ROWS} EIRE rows. "
            "Both approaches must end up with the SAME filtered result."
        )
        secs = float(res.loc[name, "seconds"])
        assert secs > 0, (
            f"{name} seconds = {secs} — time the call with time.perf_counter()."
        )
    sql_s = float(res.loc["sql_filter", "seconds"])
    pandas_s = float(res.loc["pandas_filter", "seconds"])
    ratio = pandas_s / sql_s if sql_s else float("nan")
    return (
        f"both approaches returned {_BENCHMARK_ROWS} rows; filtered SQL read was "
        f"~{ratio:.1f}x faster than load-everything-then-filter (your numbers vary)."
    )


# ---------------------------------------------------------------------------
# Part 4 — drills
# ---------------------------------------------------------------------------

@_register("D1")
def check_d1(d1_sql, d1_pandas) -> str:
    _two_engines("D1", d1_sql, d1_pandas)
    return "the 2nd-highest customer is C14298 (181.20) in both engines."


@_register("D2")
def check_d2(d2_sql, d2_pandas) -> str:
    _two_engines("D2", d2_sql, d2_pandas)
    return "both engines flag transaction 536381-01 as the duplicate."


@_register("D3")
def check_d3(d3_sql, d3_pandas) -> str:
    _two_engines("D3", d3_sql, d3_pandas)
    return "month-over-month change agrees (first month is NULL/NaN, as it must be)."


@_register("D4")
def check_d4(d4_sql, d4_pandas) -> str:
    _two_engines("D4", d4_sql, d4_pandas)
    return "longest purchase gaps agree (C12748: 3 days, C13089: 1 day)."


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def summary() -> None:
    """Print the full check registry with ✅ / ❌ / – and the final score."""
    width = max(len(label) for label in _ALL_CHECKS.values()) + 2
    print("=" * (width + 18))
    print(" One Analysis, Two Engines — score summary")
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
        print(f" {check_id:<5} {label:<{width}} {icon}")
    print("-" * (width + 18))
    print(f" Score: {passed}/{len(_ALL_CHECKS)} checks passed")
    if passed < len(_ALL_CHECKS):
        print(" Rerun any failed task's cell and its ✅ cell — results update in place.")
    else:
        print(" 🏆 Full marks — the same truth, proven twice, in two languages.")
