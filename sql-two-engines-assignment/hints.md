# Hints — one nudge per task

No full solutions here. Each hint points at the door; you still walk through it.
Every question is answered **twice** — get the SQL right first (it reads like the
question), then make pandas produce the *same* tidy table.

### 0 — database
Run the `data_setup.build_database(...)` cell in Part 0, then reconnect. The check
wants three tables and 12 / 61 rows. If it says a table is missing, the build cell
didn't run (or ran in a different folder — launch from `sql-two-engines-assignment/`).

### 1 — the one cleaning step
The raw `transactions` table has 61 rows but only 60 distinct `transaction_id`s.
SQL: `SELECT DISTINCT * FROM transactions`. pandas: `raw_tx.drop_duplicates()`.
Keep every column — you're dropping a duplicate **row**, not a column. Build this
60-row `tx` once and reuse it everywhere below.

### Q1 — revenue by country (INNER JOIN)
Join `tx` to `customers` on `customer_id`, `GROUP BY country`, `SUM(quantity*unit_price)`.
Only countries with transactions appear — that's what INNER means. Columns:
`country`, `revenue`. In pandas: `tx.merge(customers, on="customer_id").groupby("country")["revenue"].sum()`.

### Q2 — customers with no transactions (LEFT JOIN + IS NULL)
`customers LEFT JOIN transactions ON customer_id`, then keep rows where a
transaction column came back NULL — those are the customers with no match. Column:
`customer_id`. In pandas: `merge(..., how="left", indicator=True)`, keep
`_merge == "left_only"`. (This is the canonical interview phrasing of the pattern.)

### Q3 — spend bands (CASE WHEN)
First total each customer's spend (a CTE / a groupby). Then bucket the total:
`CASE WHEN total >= 300 THEN 'high' WHEN total >= 100 THEN 'mid' ELSE 'low' END`,
and `COUNT(*)` per band. Columns: `band`, `n_customers`. pandas: `pd.cut(per,
bins=[-inf, 100, 300, inf], labels=["low","mid","high"], right=False).value_counts()`.
Band only the 10 *transacting* customers here.

### Q4 — top 3 customers by spend
Total per customer, `ORDER BY total DESC`, `LIMIT 3`. Columns: `customer_id`,
`total`. pandas: `groupby(...).sum().sort_values(ascending=False).head(3)`.

### Q5 — monthly revenue
The month is the first 7 characters of the date: SQL `substr(transaction_date,1,7)`,
pandas `transaction_date.str.slice(0,7)`. Group by it, sum revenue. Columns:
`month`, `revenue`.

### Q6 — top customer per country (window)
Total per (customer, country), then rank *within* each country:
`ROW_NUMBER() OVER (PARTITION BY country ORDER BY total DESC, customer_id)`, keep
`= 1`. Columns: `country`, `customer_id`, `total`. pandas: sort by
`[country, revenue desc, customer_id]`, then `groupby("country").cumcount()+1 == 1`.
Note the window **keeps** the customer_id column — a plain GROUP BY would collapse it.

### Q7 — country revenue share (window)
Revenue per country, then divide each by the grand total *without collapsing the
rows*: `100.0 * revenue / SUM(revenue) OVER ()`. Columns: `country`, `revenue`,
`pct_of_total` (round to 2 dp). pandas: compute the per-country sum, then divide by
its `.sum()`. `SUM() OVER ()` is "the whole-table total, glued onto every row".

### B — benchmark
Two ways to get the EIRE rows out of `transactions_big` (60,000 rows):
- **sql_filter:** `pd.read_sql("... WHERE source_country='EIRE'", con)` — the database
  filters and hands pandas only the 6,000 matches.
- **pandas_filter:** `pd.read_sql("SELECT * FROM transactions_big", con)` then
  `.query("source_country=='EIRE'")` — pandas drags all 60,000 rows across first.
Time each with `time.perf_counter()` (best of a few runs). Build `results_df` with
columns `approach`, `rows_returned`, `seconds`. Both must return 6,000 rows.

### D1 — 2nd highest customer (Nth highest)
Total per customer, then rank descending and keep rank 2. SQL: `DENSE_RANK() OVER
(ORDER BY total DESC)`, `WHERE rnk = 2`. pandas: `per.rank(method="dense",
ascending=False) == 2`. Columns: `customer_id`, `total`. (Swap the 2 for any N.)

### D2 — find the duplicate transactions
`GROUP BY transaction_id HAVING COUNT(*) > 1`. Column: `transaction_id`. pandas:
`transaction_id.duplicated(keep=False)` then take the unique ids. Use the RAW
61-row table here, not your de-duplicated `tx` (that already removed the evidence).

### D3 — month-over-month revenue change (window LAG)
Monthly revenue (like Q5), then subtract the previous month:
`revenue - LAG(revenue) OVER (ORDER BY month)`. The first month has no previous, so
its change is NULL/NaN — leave it. pandas: `revenue - revenue.shift()`. Columns:
`month`, `revenue`, `mom_change`.

### D4 — longest gap between purchases (window LAG on dates)
Per customer, over their **distinct** purchase dates in order, the gap to the
previous date: SQL `julianday(date) - julianday(LAG(date) OVER (PARTITION BY
customer_id ORDER BY date))`; take the `MAX` per customer. pandas:
`groupby("customer_id")["date"].diff().dt.days`, then `.max()`. Only customers who
bought on more than one day have a gap. Columns: `customer_id`, `longest_gap_days`.
