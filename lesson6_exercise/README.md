# Lesson 6 exercise — a FRED client with caching and tidy data

Assignment 1 handed you dated snapshots of economic data and asked you to trust
them. This exercise builds the other half: the small client those snapshots could
have come from. You write three functions and the checker proves they behave — the
data pipeline quietly assembling itself, one function at a time.

Everything runs **offline**. The checker never touches the network and never needs
an API key: it reads the pinned JSON fixtures in `fixtures/`, which are FRED
`/series/observations`-shaped files reformatted from data already in this repo
(see `fixtures/manifest.json` for the honest provenance).

## Your job

Open `fred_client.py` and implement the two functions documented in its
docstring:

- **`get_series(series_id, ...)`** — return a series' raw observations as a
  `["date", "value"]` DataFrame, resolving the source in order: **cache hit →
  live (only if `FRED_API_KEY` is set) → fixture fallback**, and writing the
  response to the cache so the *second* call is served from disk.
- **`tidy_monthly(observations)`** — turn the raw string observations into a tidy
  `["month", "value"]` monthly frame: numbers coerced (`"."` → dropped), collapsed
  to one row per month.
The exact contract (types, column order, edge cases) is in the `fred_client.py`
module docstring. Read it first — it is the specification.

## Commands

From **inside this folder** (`lesson6_exercise/`):

```bash
# see the starting state: every test fails with NotImplementedError
python3 -m pytest test_lesson6.py -v

# watch your own pipeline run once, end to end (writes under ./data, gitignored)
python3 fred_client.py
```

## What "done" looks like

`python3 -m pytest test_lesson6.py -v` reports **all tests passing**. That means:

- `get_series` returns the raw two-column frame, writes a JSON cache, and serves
  the second call from that cache (the checker proves it by pointing the fallback
  at an empty directory — only the cache could answer).
- `tidy_monthly` produces the monthly schema (a `datetime64` `month`, a `float64`
  `value`, ascending, no gaps invented, missing readings dropped) and averages
  a daily series down to months.

## Files

- `fred_client.py` — **you edit this** (the two functions).
- `test_lesson6.py` — the checker. Read it; it never reveals the implementations.
- `fixtures/` — pinned FRED-shaped JSON (`DGS10`, `CPIAUCSL`, `UNRATE`) plus
  `manifest.json` and `make_fixtures.py` (how they were derived — no live fetch).
- `data/` — created at runtime for the raw JSON cache; gitignored.

## Where this leads

Lesson 7 turns this tidy table into a SQLite table with an explicit schema. The
cached client then becomes the ingestion step for the integrated mini-project
assignment (A4, after Lesson 11) and the capstone agent.
