# Four Formats, One Analysis

A pandas assignment where one financial analysis flows through **four file formats** —
CSV, JSON, Excel, and Parquet — so you experience firsthand what each format
remembers, forgets, and costs.

## What this teaches

| Format | Human-readable? | Nested data? | Dtypes survive? | Size | Read speed |
|---|---|---|---|---|---|
| CSV | ✅ | ❌ | ❌ everything is text | medium | medium |
| JSON | ✅ | ✅ | ❌ | large | slow |
| Excel | via app | sheets, sort of | partially | large | slowest |
| Parquet | ❌ binary | ✅ | ✅ | smallest | fastest |

You will download real data (FRED, Yahoo Finance), load all four formats, clean
realistic messes, build a small finance library in a Python module, and finally
**benchmark the four formats yourself** to rebuild that table from your own
measurements.

## Setup

```bash
pip install pandas numpy pyarrow openpyxl yfinance matplotlib jupyter
```

Python 3.10 or newer. Then, **from this folder** (the repo root — the notebook
resolves `utils/` and `data/` relative to it):

```bash
jupyter lab assignment.ipynb    # or: jupyter notebook assignment.ipynb
```

## How grading works

- After each task there is a ✅ cell that calls a check from `utils/test.py`
  (imported as `grader`). Run it — it prints pass/fail immediately.
- Checks **never reveal answers** and never crash your notebook. When stuck,
  open [hints.md](hints.md) — one nudge per task.
- Re-running a check overwrites its previous result, so iterate freely.
- At the end, `grader.summary()` prints the full score table.

## The `utils/finance.py` workflow (Part 3)

Part 3 moves your logic out of notebook cells into a real Python module:
you implement five functions in `utils/finance.py`. The notebook's setup cell
enables `%autoreload`, so the loop is simply:

1. Edit `utils/finance.py` in any editor and **save**.
2. Rerun `grader.check_finance_module()` in the notebook — no kernel restart.
3. Repeat until all five functions are green, then use them on real data.

## Offline mode

No network, or a download failed? The repo ships dated snapshots from the same
FRED and Yahoo Finance acquisition paths in `data_offline/`. Either uncomment
and run the `use_offline_data()` cell in Part 0, or copy the files by hand:

```bash
cp data_offline/* data/
```

Everything — every task, every check — works identically. One difference: the
offline stock file already contains the Part-2 mess, so skip the chaos cell
(it detects this and skips itself). To intentionally refresh the dated snapshots,
run `python utils/make_offline_data.py`. The script records source metadata and
checksums in `data_offline/manifest.json`.

## Data sources

| File | Source | Link |
|---|---|---|
| `DGS10.csv` | FRED: 10-Year Treasury Constant Maturity | https://fred.stlouisfed.org/series/DGS10 |
| `fred_macro.xlsx` | FRED: CPI + Unemployment | https://fred.stlouisfed.org/series/CPIAUCSL · https://fred.stlouisfed.org/series/UNRATE |
| `stock_market.parquet` | Yahoo Finance via [yfinance](https://ranaroussi.github.io/yfinance/) | AAPL, MSFT, SPY since 2021 |
| `portfolio.json` | generated locally (broker-API style) | — |

The FRED snapshots are public economic data. The Yahoo-derived snapshot is for
this private educational course only and must not be redistributed. The nested
`portfolio.json` remains a deterministic instructional scenario so the exercises
and grader have a safe, reproducible trade history.

## Rubric

| Part | Weight | Checks (see `grader.summary()`) |
|---|---|---|
| Part 0–1: acquisition & loading | 30% | `0`, `1.1`, `1.2`, `1.3`, `1.4` (6% each) |
| Part 2: cleaning | 20% | `2.1`, `2.2` (10% each) |
| Part 3: finance & the module | 35% | `3.1`, `3.2 module`, `3.3`, `3.4`, `3.5`, `3.6` (~5.8% each) |
| Part 4: benchmark capstone | 15% | `4` (10%) + reflection answers (5%, graded by hand) |

Markdown answers (format takeaways, checkpoint table, reflection scenarios) are
part of the submission — the checks can't read your prose, your instructor will.
