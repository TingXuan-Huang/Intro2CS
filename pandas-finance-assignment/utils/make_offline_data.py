"""Regenerate data_offline/ deterministically (seed=42).

The offline files are SIMULATED but schema-identical to the live downloads, so
every task and every grading check behaves the same without a network.

Run from the repo root:

    python utils/make_offline_data.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

if __package__ in (None, ""):  # allow `python utils/make_offline_data.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.data_setup import _write_fred_style_xlsx, inject_chaos, write_portfolio_json

SEED = 42
START = "2021-01-04"
END = "2025-12-31"


def make_dgs10_csv(out: Path, seed: int = SEED) -> Path:
    """Business-day 10y yield path from ~1% to ~4.5%, with FRED's '.' markers."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(START, END)
    t = np.linspace(0.0, 1.0, len(dates))
    trend = 0.95 + 3.55 / (1.0 + np.exp(-8.0 * (t - 0.5)))  # smooth 1% -> 4.5%
    noise = np.zeros(len(dates))
    for i in range(1, len(dates)):  # mean-reverting wiggle around the trend
        noise[i] = 0.985 * noise[i - 1] + rng.normal(0, 0.035)
    yields = np.clip(trend + noise, 0.4, 6.0).round(2)

    missing = rng.random(len(dates)) < 0.02  # ~2% market holidays
    missing[0] = False  # a leading gap would survive a forward-fill — keep it winnable
    lines = ["DATE,DGS10"]
    for date, value, is_missing in zip(dates, yields, missing):
        lines.append(f"{date:%Y-%m-%d},{'.' if is_missing else f'{value:.2f}'}")
    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out} — {len(dates)} rows, {int(missing.sum())} '.' markers.")
    return out


def make_macro_xlsx(out: Path, seed: int = SEED) -> Path:
    """60 monthly rows: hot-then-cooling CPI, falling UNRATE with 2 NaN cells."""
    rng = np.random.default_rng(seed)
    months = pd.date_range("2021-01-01", periods=60, freq="MS")
    m = np.arange(60)

    # Monthly inflation: ~0.35% baseline plus a 2021-22 hump peaking near month 15.
    monthly_inflation = 0.0025 + 0.006 * np.exp(-(((m - 15) / 10.0) ** 2))
    monthly_inflation += rng.normal(0, 0.0006, 60)
    cpi = 261.6 * np.cumprod(1 + monthly_inflation)

    unrate = 6.3 - 2.6 / (1.0 + np.exp(-0.25 * (m - 10))) + rng.normal(0, 0.08, 60)
    unrate = np.clip(unrate, 3.4, 6.5).round(1)
    unrate_values = unrate.astype(object)
    for idx in rng.choice(np.arange(10, 58), size=2, replace=False):
        unrate_values[idx] = np.nan  # the Task 2.2 interpolation exercise

    df = pd.DataFrame(
        {
            "observation_date": months,
            "CPIAUCSL": cpi.round(3),
            "UNRATE": unrate_values,
        }
    )
    _write_fred_style_xlsx(df, out)
    print(f"Wrote {out} — 60 monthly rows, 2 NaN UNRATE cells, 2 sheets.")
    return out


def make_stocks_parquet(out: Path, seed: int = SEED) -> Path:
    """GBM-simulated OHLCV for AAPL/MSFT/SPY, then passed through inject_chaos."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(START, END)
    n = len(dates)
    params = {  # start price ~= first portfolio trade; annual drift; annual vol
        "AAPL": (129.41, 0.18, 0.28),
        "MSFT": (232.42, 0.16, 0.25),
        "SPY": (368.79, 0.11, 0.17),
    }

    frames = []
    for ticker, (start_price, mu, sigma) in params.items():
        z = np.clip(rng.standard_normal(n), -4, 4)
        log_returns = (mu - 0.5 * sigma**2) / 252 + sigma / np.sqrt(252) * z
        close = start_price * np.exp(np.cumsum(log_returns))

        prev_close = np.concatenate([[start_price], close[:-1]])
        open_ = prev_close * (1 + rng.normal(0, 0.004, n))
        spread = np.abs(rng.normal(0, 0.008, n))  # guarantees High/Low envelope
        high = np.maximum(open_, close) * (1 + spread)
        low = np.minimum(open_, close) * (1 - spread)
        volume = rng.lognormal(mean=16.0, sigma=0.35, size=n).astype("int64")

        frames.append(
            pd.DataFrame(
                {
                    "Date": dates,
                    "Ticker": ticker,
                    "Open": open_.round(4),
                    "High": high.round(4),
                    "Low": low.round(4),
                    "Close": close.round(4),
                    "Volume": volume,
                }
            )
        )

    stocks = pd.concat(frames, ignore_index=True)
    # Pre-chaos the offline file so students who skip the chaos cell (as offline
    # instructions say to) still get the full cleaning exercise.
    stocks = inject_chaos(stocks, seed=seed)
    stocks.to_parquet(out, index=False, engine="pyarrow")
    print(f"Wrote {out} — {len(stocks)} rows (chaos included).")
    return out


def main(out_dir: str | Path = "data_offline") -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    make_dgs10_csv(out_dir / "DGS10.csv")
    write_portfolio_json(out_dir / "portfolio.json")
    make_macro_xlsx(out_dir / "fred_macro.xlsx")
    make_stocks_parquet(out_dir / "stock_market.parquet")
    print("data_offline/ regenerated (seed=42).")


if __name__ == "__main__":
    main()
