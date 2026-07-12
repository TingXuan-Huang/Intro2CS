"""Regenerate the Lesson 6 FRED-shaped fixture files from pinned repo data.

These fixtures are AUTHORED TEACHING FIXTURES, not a live retrieval. Every
observation is copied, value-for-value, from data already pinned in this
repository for Assignment 1:

    pandas-finance-assignment/data_offline/DGS10.csv        -> DGS10.json    (daily)
    pandas-finance-assignment/data_offline/fred_macro.xlsx  -> CPIAUCSL.json (monthly)
        (sheet 'Monthly' holds the values)                     UNRATE.json   (monthly)

The ONLY transformation is reshaping those rows into the JSON envelope the real
FRED ``/fred/series/observations`` endpoint returns, so the lesson can run a real
``requests.get`` against a local replay server and receive a response with the
same shape the live API would send. Values are preserved verbatim, including
FRED's "." token for a missing daily observation (already present in DGS10.csv).

This script writes both the *.json fixtures and manifest.json next to itself, so
the manifest can never drift from the fixtures. Run from anywhere:

    python3 lesson6_exercise/fixtures/make_fixtures.py
"""

import hashlib
import json
from datetime import date
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent          # lesson6_exercise/fixtures
REPO = HERE.parents[1]                           # repo root
SOURCE = REPO / "pandas-finance-assignment" / "data_offline"

# The date Assignment 1's snapshot was captured (see that folder's manifest.json).
# FRED stamps every observation with the realtime window it was valid for; we
# reuse the honest capture date rather than invent one.
REALTIME = "2026-07-11"

# Keep the 2021+ era, the window Assignment 1 works in and where DGS10 begins.
CUTOFF = date(2021, 1, 1)


def observation(date_str, value_str):
    return {
        "realtime_start": REALTIME,
        "realtime_end": REALTIME,
        "date": date_str,
        "value": value_str,
    }


def envelope(observations):
    """Wrap rows in the FRED /series/observations envelope (faithful field set).

    Note: the real observations endpoint does NOT echo the series id or a human
    title -- the series identity is carried by the request, so here it is the
    filename. Keeping the envelope faithful is what lets a cached copy be
    indistinguishable from a live response (a Unit 3 teaching point).
    """
    return {
        "realtime_start": REALTIME,
        "realtime_end": REALTIME,
        "observation_start": observations[0]["date"],
        "observation_end": observations[-1]["date"],
        "units": "lin",              # the data-transform the endpoint applied: levels
        "output_type": 1,
        "file_type": "json",
        "order_by": "observation_date",
        "sort_order": "asc",
        "count": len(observations),
        "offset": 0,
        "limit": 100000,
        "observations": observations,
    }


def build_dgs10():
    """Daily 10-year Treasury yield, straight from DGS10.csv (value strings kept)."""
    rows = []
    with open(SOURCE / "DGS10.csv", newline="") as handle:
        header = handle.readline()            # DATE,DGS10
        for line in handle:
            day, value = line.rstrip("\n").split(",")
            if date.fromisoformat(day) < CUTOFF:
                continue
            rows.append(observation(day, value))   # value already "." for a gap
    return rows


def build_monthly(column, decimals):
    """One monthly series from the workbook's 'Monthly' sheet, values as FRED strings."""
    workbook = openpyxl.load_workbook(SOURCE / "fred_macro.xlsx", data_only=True)
    records = list(workbook["Monthly"].iter_rows(values_only=True))
    header = records[4]                         # ('observation_date', 'CPIAUCSL', 'UNRATE')
    col = header.index(column)
    rows = []
    for record in records[5:]:
        when, value = record[0], record[col]
        if when is None or when.date() < CUTOFF or value is None:
            continue                            # this series has no reading that month
        rows.append(observation(when.date().isoformat(), f"{float(value):.{decimals}f}"))
    return rows


SERIES = {
    # series_id: (row builder, human description for the manifest, source note)
    "DGS10": (
        build_dgs10,
        "Market Yield on U.S. 10-Year Treasury (daily, percent)",
        "pandas-finance-assignment/data_offline/DGS10.csv (columns DATE, DGS10)",
    ),
    "CPIAUCSL": (
        lambda: build_monthly("CPIAUCSL", 3),
        "Consumer Price Index for All Urban Consumers: All Items (monthly, index)",
        "pandas-finance-assignment/data_offline/fred_macro.xlsx, sheet 'Monthly', column CPIAUCSL",
    ),
    "UNRATE": (
        lambda: build_monthly("UNRATE", 1),
        "Unemployment Rate (monthly, percent)",
        "pandas-finance-assignment/data_offline/fred_macro.xlsx, sheet 'Monthly', column UNRATE",
    ),
}


def main():
    manifest_files = []
    for series_id, (builder, description, source_note) in SERIES.items():
        observations = builder()
        text = json.dumps(envelope(observations), indent=2) + "\n"
        (HERE / f"{series_id}.json").write_text(text)
        missing = sum(1 for row in observations if row["value"] == ".")
        manifest_files.append({
            "path": f"{series_id}.json",
            "series_id": series_id,
            "description": description,
            "derived_from": source_note,
            "observation_start": observations[0]["date"],
            "observation_end": observations[-1]["date"],
            "count": len(observations),
            "missing_value_dots": missing,
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
        })
        print(f"wrote {series_id + '.json':16} {len(observations):>5} observations, "
              f"{missing} '.' missing  ({observations[0]['date']} -> {observations[-1]['date']})")

    manifest = {
        "kind": "authored teaching fixtures",
        "what_these_are": (
            "FRED /series/observations-shaped JSON reformatted from data ALREADY pinned in "
            "this repository for Assignment 1. No live FRED retrieval was performed to create "
            "these files; they exist so the lesson runs fully offline."
        ),
        "shape": (
            "Each file mirrors the real FRED observations endpoint response: a top-level "
            "envelope (realtime_start/end, units, count, ...) plus an 'observations' list of "
            "{realtime_start, realtime_end, date, value} objects. Every value is a string; "
            "'.' marks a missing observation, exactly as FRED serves it."
        ),
        "derivation": [
            "Rows dated 2021-01-01 or later were kept (the era Assignment 1 uses; where DGS10 begins).",
            "Daily DGS10 values are copied verbatim from the CSV, '.' tokens included.",
            "Monthly CPIAUCSL/UNRATE values are formatted to FRED's decimal precision (3 and 1).",
            "The source Monthly sheet has no October 2025 row, so the monthly fixtures skip that month.",
            "Envelope fields (count, observation_start/end) describe the reformatted rows honestly.",
        ],
        "regenerate_with": "python3 lesson6_exercise/fixtures/make_fixtures.py",
        "realtime_date": REALTIME,
        "files": manifest_files,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote manifest.json")


if __name__ == "__main__":
    main()
