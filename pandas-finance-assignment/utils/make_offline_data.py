"""Capture real dated snapshots for the offline assignment bundle.

The snapshots are captured from the same FRED and yfinance sources used by the
normal acquisition path, then saved locally so students can complete every task
without a network connection. The cleaning defects remain deterministic teaching
fixtures applied to a real market-data snapshot.

Run from the repo root:

    python utils/make_offline_data.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

if __package__ in (None, ""):  # allow `python utils/make_offline_data.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.data_setup import (
    download_fred_csv,
    download_fred_excel,
    download_stocks_parquet,
    inject_chaos,
    write_portfolio_json,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main(out_dir: str | Path = "data_offline") -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    download_fred_csv(out=out_dir / "DGS10.csv")
    write_portfolio_json(out_dir / "portfolio.json")
    download_fred_excel(out=out_dir / "fred_macro.xlsx")
    stock_path = download_stocks_parquet(out=out_dir / "stock_market.parquet")
    stocks = pd.read_parquet(stock_path)
    inject_chaos(stocks).to_parquet(stock_path, index=False, engine="pyarrow")

    files = ["DGS10.csv", "portfolio.json", "fred_macro.xlsx", "stock_market.parquet"]
    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "captured_at_utc": datetime.now(timezone.utc).isoformat(),
                "fred_series": ["DGS10", "CPIAUCSL", "UNRATE"],
                "market_source": "Yahoo Finance via yfinance",
                "market_terms": "Private educational-course snapshot; do not redistribute.",
                "tickers": ["AAPL", "MSFT", "SPY"],
                "stock_start": "2021-01-01",
                "files": [
                    {"path": name, "sha256": sha256(out_dir / name)}
                    for name in files
                ],
            },
            indent=2,
        )
        + "\n"
    )
    print("Captured dated real-data snapshots in data_offline/.")


if __name__ == "__main__":
    main()
