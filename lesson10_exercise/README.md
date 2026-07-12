# Lesson 10 exercise — Spark queries without a cluster

Spark lets the same DataFrame-style analysis run on multiple machines. This
exercise deliberately uses **one local worker**: the goal is to practice Spark's
lazy DataFrame and window APIs without hiding the ideas behind cluster setup.

## Setup

Install `pyspark` and a supported Java runtime first. From this folder, run:

```bash
python3 -m pytest test_lesson10.py -v
```

The checker reads the pinned retail CSVs already in `course_data/`. It creates no
network requests and no remote cluster.

## Your job

Open `spark_queries.py` and implement:

- `monthly_revenue_by_country(transactions, customers)` — a join, derived revenue,
  month-level aggregation, and deterministic sort.
- `customer_revenue_rank(transactions, customers)` — the same join and aggregation,
  then a `dense_rank` window within each country.

Both functions must return a **Spark DataFrame**. Do not use `collect()` or
`toPandas()` in your solution: those are actions that move results to the driver.
The checker does that only after your transformation plan is complete.

## What done looks like

All three tests pass. The two query tests compare your results with pinned retail
answers; the last test checks that your functions leave their input schemas alone.

## Where this leads

Spark uses the joins, groups, and windows from Lesson 9, but its lazy plan can be
executed across partitions. Lesson 11 returns to HTTP APIs for LLMs, where the
same discipline applies: inspect a contract, validate outputs, and keep expensive
work bounded.
