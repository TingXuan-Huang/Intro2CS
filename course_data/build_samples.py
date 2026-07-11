"""Build compact, offline-first real-data extracts used by the course notebooks.

The source dataset is UCI's Online Retail dataset (CC BY 4.0):
https://archive.ics.uci.edu/dataset/352/online+retail

Run from the repository root:

    python course_data/build_samples.py

Use ``--refresh`` to retrieve the upstream source again before rebuilding the
same deterministic extracts. The generated files contain no customer names or
other unnecessary personal fields.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


SOURCE_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
SOURCE_PAGE = "https://archive.ics.uci.edu/dataset/352/online+retail"
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "online_retail_source.zip"
RAW_SAMPLE = ROOT / "online_retail_sample.csv"
CUSTOMERS = ROOT / "lesson2_customers_base.csv"
TRANSACTIONS = ROOT / "lesson2_transactions_base.csv"
MANIFEST = ROOT / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_source(refresh: bool) -> Path:
    if CACHE.exists() and not refresh:
        return CACHE

    request = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": "intro-to-cs-course-data/1.0"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        CACHE.write_bytes(response.read())
    return CACHE


def load_source(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        xlsx_name = next(name for name in archive.namelist() if name.endswith(".xlsx"))
        with archive.open(xlsx_name) as workbook:
            return pd.read_excel(io.BytesIO(workbook.read()), engine="openpyxl")


def build_extracts(source: pd.DataFrame) -> None:
    clean = source.rename(columns={"InvoiceNo": "invoice_id", "CustomerID": "source_customer_id"})
    clean = clean[
        clean["source_customer_id"].notna()
        & clean["Description"].notna()
        & (clean["Quantity"] > 0)
        & (clean["UnitPrice"] > 0)
        & ~clean["invoice_id"].astype(str).str.startswith("C")
    ].copy()
    clean["source_customer_id"] = clean["source_customer_id"].astype("int64").astype(str)
    clean["InvoiceDate"] = pd.to_datetime(clean["InvoiceDate"])
    clean = clean.sort_values(["source_customer_id", "InvoiceDate", "invoice_id", "StockCode"])

    eligible = clean.groupby("source_customer_id").filter(lambda rows: len(rows) >= 6)
    customer_ids = (
        eligible.groupby("source_customer_id")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    sample = (
        eligible[eligible["source_customer_id"].isin(customer_ids)]
        .groupby("source_customer_id", group_keys=False)
        .head(6)
        .sort_values(["InvoiceDate", "invoice_id", "source_customer_id", "StockCode"])
        .reset_index(drop=True)
    )

    sample.to_csv(RAW_SAMPLE, index=False)

    customer_map = {
        source_id: f"C{int(source_id):05d}" for source_id in sample["source_customer_id"].unique()
    }
    customers = (
        sample.groupby("source_customer_id", as_index=False)
        .agg(
            country=("Country", "first"),
            first_purchase_date=("InvoiceDate", "min"),
        )
        .assign(
            customer_id=lambda frame: frame["source_customer_id"].map(customer_map),
            customer_label=lambda frame: "Customer " + frame["source_customer_id"],
        )
        [["customer_id", "customer_label", "country", "first_purchase_date"]]
        .sort_values("customer_id")
    )
    customers["first_purchase_date"] = pd.to_datetime(
        customers["first_purchase_date"]
    ).dt.strftime("%Y-%m-%d")
    customers.to_csv(CUSTOMERS, index=False)

    transactions = sample.assign(
        customer_id=sample["source_customer_id"].map(customer_map),
        transaction_id=[
            f"{invoice}-{line:02d}" for line, invoice in enumerate(sample["invoice_id"], start=1)
        ],
        transaction_date=sample["InvoiceDate"].dt.strftime("%Y-%m-%d"),
        product=lambda frame: frame["Description"].str.strip(),
        unit_price=lambda frame: frame["UnitPrice"].astype(float).round(2),
    )[
        [
            "transaction_id",
            "customer_id",
            "transaction_date",
            "product",
            "Quantity",
            "unit_price",
            "Country",
        ]
    ].rename(columns={"Quantity": "quantity", "Country": "source_country"})
    transactions.to_csv(TRANSACTIONS, index=False)


def write_manifest() -> None:
    files = [RAW_SAMPLE, CUSTOMERS, TRANSACTIONS]
    MANIFEST.write_text(
        json.dumps(
            {
                "dataset": "UCI Online Retail",
                "source_url": SOURCE_PAGE,
                "download_url": SOURCE_URL,
                "license": "CC BY 4.0",
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "selection": (
                    "Ten customers with at least six positive-price, non-cancellation "
                    "transactions; first six qualifying transactions per customer."
                ),
                "files": [
                    {
                        "path": path.name,
                        "rows": len(pd.read_csv(path)),
                        "sha256": sha256(path),
                    }
                    for path in files
                ],
            },
            indent=2,
        )
        + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Download the upstream ZIP again.")
    args = parser.parse_args()

    source_path = download_source(args.refresh)
    build_extracts(load_source(source_path))
    write_manifest()
    print(f"Built {RAW_SAMPLE.name}, {CUSTOMERS.name}, and {TRANSACTIONS.name}.")


if __name__ == "__main__":
    main()
