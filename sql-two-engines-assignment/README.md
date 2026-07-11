# One Analysis, Two Engines

A SQL assignment where you answer the **same business questions twice** — once in
**SQL** and once in **pandas** — against one small retail database, and a grader
checks that both engines agree with a pinned reference *and with each other*.

This is the sibling of Assignment 1 ("Four Formats, One Analysis"). That one
carried a single analysis through four **file formats**; this one carries a
single analysis through two **query engines**. The punchline is the same shape:
the tool changes, the truth does not — and when two tools disagree, one of them
has a bug.

## What this teaches

| SQL you'll write | The pandas twin you already know (Lesson 2) |
|---|---|
| `JOIN ... ON` (INNER / LEFT) | `df.merge(..., how="inner"/"left")` |
| `LEFT JOIN ... WHERE key IS NULL` | `merge(..., indicator=True)` then `_merge == "left_only"` |
| `CASE WHEN ... THEN ... END` | `pd.cut` / `np.where` / boolean masks |
| `GROUP BY` + `SUM/COUNT` | `groupby().agg()` |
| `WITH cte AS (...)` | naming an intermediate DataFrame |
| `ROW_NUMBER()/RANK() OVER (PARTITION BY ...)` | `sort_values` + `groupby().cumcount()` / `rank()` |
| `SUM(...) OVER ()` | a groupby total divided back in |

You will also **benchmark** pushing a filter into the database versus loading a
whole table into pandas and filtering there — and settle four classic interview
drills (Nth-highest, find-the-duplicates, month-over-month, gaps between events).

## Setup

```bash
pip install pandas jupyter        # sqlite3 ships with Python — nothing else needed
```

Python 3.10 or newer (window functions need a reasonably modern SQLite; Python
3.12's bundled SQLite is fine). Then, **from this folder** (the notebook resolves
`utils/` and `data/` relative to it):

```bash
jupyter lab assignment.ipynb      # or: jupyter notebook assignment.ipynb
```

## The database

`utils/data_setup.py` builds `data/retail.sqlite` deterministically from the
pinned extracts in `data_source/` (real UCI Online Retail data, same source as
the course notebooks) plus two clearly-labelled teaching fixtures:

- **two customers with no transactions** (`C99001`, `C99002`) — so "customers who
  never bought" is a real LEFT JOIN + `IS NULL` result, not an empty set;
- **one exact-duplicate transaction line** (`536381-01`) — so de-duplication
  actually matters, and drill D2 has something to find.

Three tables result: `customers` (12 rows), `transactions` (61 rows — 60 real +
1 duplicate), and `transactions_big` (60,000 rows, used only by the benchmark).
Full provenance is in `manifest.json`. `data/` is git-ignored and fully
rebuildable — delete it and rerun Part 0.

> ⚠️ **One cleaning rule for the whole assignment:** the `transactions` table has
> exactly one duplicated row. Part 1 removes it into a 60-row working set, and
> **every business question uses the de-duplicated data**. In SQL that's
> `WITH tx AS (SELECT DISTINCT * FROM transactions)`; in pandas it's
> `transactions.drop_duplicates()`. Forget it and your totals double-count.

## How grading works

- After each task there is a ✅ cell that calls a check from `utils/test.py`
  (imported as `grader`). Each check verifies **both** your SQL answer and your
  pandas answer against a hidden reference **and against each other**.
- Checks **never reveal answers** and never crash your notebook — a failed check
  prints a `❌` pointer. Re-running a check overwrites its previous result.
- Stuck? Open [hints.md](hints.md) — one nudge per task.
- At the end, `grader.summary()` prints the full score table (14 checks).

## Output contracts

Each check needs a tidy result with **exact column names** (so a SQL frame and a
pandas frame are comparable). The columns for every task are stated in the
notebook's TODO comment and in `hints.md`. Row order and index never matter; the
grader sorts and rounds (2 dp) before comparing.

## Rubric

| Part | Weight | Checks |
|---|---|---|
| Part 0–1: build + de-duplicate | 15% | `0`, `1` |
| Part 2: six business questions, two engines each | 50% | `Q1`–`Q7` |
| Part 3: benchmark | 10% | `B` |
| Part 4: four interview drills | 25% | `D1`–`D4` |

The short written interpretations (revenue-share reading, benchmark takeaway,
the "when does GROUP BY lose a row that a window keeps" note) are part of the
submission — the checks can't read your prose; your instructor will.

## Data sources

| File | Source | Link |
|---|---|---|
| `data_source/customers_base.csv` | UCI Online Retail extract (anonymised) | https://archive.ics.uci.edu/dataset/352/online+retail |
| `data_source/transactions_base.csv` | UCI Online Retail extract | https://archive.ics.uci.edu/dataset/352/online+retail |

The UCI Online Retail dataset is licensed CC BY 4.0. The two teaching fixtures
(no-order customers, duplicate line) are authored for this exercise and are
**not** claims about the source data — see `manifest.json`.
