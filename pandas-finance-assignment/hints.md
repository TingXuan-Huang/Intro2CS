# Hints — one nudge per task

No full solutions here. Each hint points at the door; you still walk through it.

### Part 0 — downloads fail?
Use offline mode: uncomment the `use_offline_data()` cell (or `cp data_offline/* data/`).
Everything downstream works the same — just skip the chaos cell in Part 2.

### 1.1 — CSV
Open `data/DGS10.csv` in a text editor and scan the value column: FRED marks
market holidays with a literal `"."`. `read_csv` has an `na_values=` argument —
its docs even mention this exact convention. Dates: `parse_dates=`.

### 1.2 — JSON
`pd.json_normalize` has two arguments made for exactly this shape:
`record_path=` (which nested list becomes the rows) and `meta=` (which
parent-level fields get carried along). `meta_prefix=` names them. Read the
examples in its docstring — they're better than any hint.

### 1.3 — Excel
First reconnaissance: `pd.ExcelFile("data/fred_macro.xlsx").sheet_names`.
Then aim `read_excel` at the right sheet with `sheet_name=`, and jump over the
decorative rows with `skiprows=` (count them in the naive load). `index_col=`
plus `pd.to_datetime` finish the job.

### 1.4 — Parquet
`read_parquet` has a `columns=` argument — hand it the list of columns you want
and Parquet reads *only those* from disk. That's what columnar means.

### 2.1 — cleaning the stocks
- **Casing:** `.str.upper()` — do this *first*, or your duplicates won't match.
- **Duplicates:** `drop_duplicates(subset=["Ticker", "Date"])` — subset matters;
  the injected copies are identical rows, but why trust that?
- **Sorting:** `sort_values(["Ticker", "Date"])` — `shift` and `ffill` assume order.
- **Outlier:** divide each Close by the *previous* Close **within its ticker**
  (`groupby("Ticker")["Close"].shift()`). Honest prices rarely change 5× overnight;
  a typo does. Flag ratios > 5 or < 0.2, set those Closes to NaN.
- **Gaps:** `groupby("Ticker")["Close"].ffill()` — grouped, or one ticker's last
  price leaks into the next ticker's first gap.

### 2.2 — ffill vs interpolate
`ffill` says "nothing changed while we weren't looking" — right for a yield on a
day the market was closed. `interpolate` says "it moved smoothly between the
points I have" — right for a slow monthly indicator like unemployment. Neither
deletes rows; `dropna` is the tool of last resort here.

### 3.1 — long to wide
`stocks_clean.pivot(index=..., columns=..., values=...)` — you want one column
per ticker, one row per date, Close as the values. Returns: `pct_change()`.
Compounding: grow $1 through every return — a product, not a sum.

### 3.2 — the module functions
- `daily_returns`: it's one method on the DataFrame. Truly.
- `cumulative_return`: `(1 + returns).prod() - 1`. `prod()` skips NaN on its own.
- `annualized_volatility`: `std()` (pandas default), times the square root of
  `periods_per_year` — don't hardcode 252.
- `sharpe_ratio`: annualize the mean (`mean() * periods_per_year`), subtract the
  *annual* risk-free rate, divide by your own `annualized_volatility`. Reuse it —
  that's why modules exist.
- `max_drawdown`: `cummax()` gives the running peak; compare every price to the
  peak so far, take the worst.

### 3.3 — vol, Sharpe, rf
DGS10 is in *percent* (3.5 means 3.5%) — your functions want a decimal. The
mean of the cleaned series, divided by 100, is the whole trick.

### 3.4 — drawdown per ticker
`close.apply(your_function)` runs it once per column.

### 3.5 — portfolio valuation
Two truths in two places: the **cost basis lives in the trades** (Σ shares ×
price per holding — group the flattened `trades` table from 1.2), and the
**current value lives in the prices** (`close.iloc[-1]` is the latest close per
ticker). shares × latest − cost = your answer.

### 3.6 — macro correlation
`close["SPY"].resample("MS").first()` gives month-start prices; `pct_change()`
makes them returns. `diff()` turns UNRATE levels into changes. `Series.corr`
aligns the two on their shared monthly index by itself.

### 4 — benchmark
Wrap each call in `t0 = time.perf_counter()` … `elapsed = time.perf_counter() - t0`.
`os.path.getsize(path)` gives bytes — you want KB. Dtype survival:
`pd.api.types.is_datetime64_any_dtype(reloaded["Date"])`.
