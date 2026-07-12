# Lesson 8 exercise — Monthly revenue by country, in SQL and pandas

## Goal

Compute one small report — **monthly revenue by country** — two ways, and prove
the two ways agree.

1. Write it as a **SQL** query string (`monthly_revenue_by_country_sql`).
2. Write it in **pandas** (`monthly_revenue_by_country_pandas`).
3. The checker runs both, compares them with `assert_frame_equal`, and checks a
   few pinned reference numbers.

This is the whole through-line of the lesson made concrete: a SQL query and its
pandas twin are two spellings of the same answer. If they disagree, one of them
is wrong — and the test tells you so without revealing the numbers.

## The report

For the `transactions` table (the real 60-row UCI extract you met in Lessons 2
and 4):

- **revenue of one line** = `quantity * unit_price`
- **month** = the `YYYY-MM` part of `transaction_date` (e.g. `2010-12`)
- one row per **(month, country)** pair, where country is `source_country`
- **revenue rounded to 2 decimals**
- sorted by **month** ascending, then **country** ascending

Output columns, in this exact order, with these names and types:

| column    | type  | example          |
| --------- | ----- | ---------------- |
| `month`   | str   | `'2010-12'`      |
| `country` | str   | `'United Kingdom'` |
| `revenue` | float | `1209.90`        |

## What to edit

Open `queries.py` and fill in the two functions. Their docstrings restate the
contract; the lesson notebook (Unit 3.4) shows the exact SQL and pandas moves you
need. Do not change the function names or signatures.

You do **not** build the database — the checker builds its own SQLite file from
`../course_data/lesson2_transactions_base.csv` (under `data/`, which is
gitignored) every time it runs.

## Run the checker

From inside this folder:

```bash
python3 -m pytest test_lesson8.py -v
```

## What "done" looks like

- **Before you start:** nothing is implemented yet, so pytest reports
  `1 failed, 9 errors in 0.14s` — every test ends in the same graceful
  `NotImplementedError: Fill in ...` message. (Nine ERROR because the stub
  raises while a fixture is building their input; one — the "does not mutate"
  test — is marked FAILED because it calls the function in the test body
  instead, but it is the identical message and cause.) That is the intended
  starting state, not something you broke.
- **When you are done:** all tests pass. That means your SQL report and your
  pandas report are byte-for-byte the same DataFrame, and both match the pinned
  totals.

## Hints (only if stuck)

- SQL month: `strftime('%Y-%m', transaction_date)`. Rounding: `ROUND(x, 2)`.
  Group by the month and the country; order by month then country.
- pandas month: `df["transaction_date"].str.slice(0, 7)` (or
  `pd.to_datetime(...).dt.strftime('%Y-%m')`) — both give a `'YYYY-MM'` **string**,
  not a Period. Group with `groupby([...])`, sum, `round(2)`, `sort_values`, and
  finish with `reset_index(drop=True)`.
- If `assert_frame_equal` complains about **dtype**, your `month` is probably a
  Period, not a string — the contract asks for a string.
- If it complains about **index**, you forgot `reset_index(drop=True)`.

## Where this leads

"Two tools, one answer, proven equal" is the core move of the "One Analysis,
Two Engines" assignment (`sql-two-engines-assignment/`): every question there is
answered in SQL and in pandas and both must agree. This exercise is the dress
rehearsal for that assignment, one question at a time.
