# Lesson 7 exercise — Design a schema, load it, break it on purpose

In the notebook you watched a database reject bad rows. Now you build the schema
yourself. This is Unit 2 in your own hands: **a schema is Lesson 1's property
checklist, and here you write it down so the software enforces it.**

## Goal

Finish `build_database.py` so that it:

1. creates a two-table SQLite database for the retail extract, with the integrity
   rules declared in the schema —
   - **customers**: `customer_id` is the `PRIMARY KEY`, `country` is `NOT NULL`;
   - **transactions**: `transaction_id` is the `PRIMARY KEY`, `customer_id` is
     `NOT NULL` and a `FOREIGN KEY` referencing `customers(customer_id)`;
2. loads the real data — 10 customers and 60 transactions — from
   `../course_data/lesson2_customers_base.csv` and
   `../course_data/lesson2_transactions_base.csv`;
3. returns an open connection with foreign keys switched **on**; and
4. implements `demonstrate_rejection()` — attempt one bad insert (a duplicate key,
   a blank required field, or an orphan foreign key), catch the
   `sqlite3.IntegrityError`, and return its message.

The full contract is written next to each function in `build_database.py`, and
again in the docstring of `test_lesson7.py`.

## Commands

Run everything from inside this folder:

```bash
cd lesson7_exercise

# See your own rejection message once the functions are written:
python3 build_database.py

# Grade yourself:
python3 -m pytest test_lesson7.py -v
```

The checker builds your database into a fresh temporary directory, so it never
leaves files behind. (Running `build_database.py` directly writes to
`lesson7_exercise/data/`, which is gitignored.)

## Where to start

The shipped functions raise `NotImplementedError`, so the checker fails on every
test until you implement them — that is the expected starting point. Work in this
order:

1. Open the connection and turn foreign keys on.
2. `CREATE TABLE customers (...)` — read the DDL as a list of Lesson 1 properties.
3. Load customers, then `CREATE TABLE transactions (...)` with the foreign key.
4. Load transactions (customers must exist first, or the foreign key refuses them).
5. Write `demonstrate_rejection()` — the satisfying part: make the database say no.

Tip for loading: create the table first, then use
`df.to_sql(name, conn, if_exists="append", index=False)`. `append` inserts rows
into the table *you* declared, instead of letting pandas invent a schema with no
keys (the Unit 3 warning).

### Optional Lesson 6 integration

Once the required retail schema passes, take the tidy `monthly` DataFrame from
the FRED client and design an `observations` table before calling `to_sql`. Decide
which columns should be `NOT NULL`, how to represent the series ID, and why
SQLite stores a month as ISO text. This is intentionally *after* the API lesson:
fetching and caching are API concerns; choosing a durable schema is a database
concern.

## What "done" looks like

```
$ python3 -m pytest test_lesson7.py -v
...
test_lesson7.py::test_customers_customer_id_is_the_primary_key PASSED
test_lesson7.py::test_customers_country_is_not_null PASSED
test_lesson7.py::test_transactions_transaction_id_is_the_primary_key PASSED
test_lesson7.py::test_transactions_customer_id_is_not_null PASSED
test_lesson7.py::test_transactions_have_a_foreign_key_to_customers PASSED
test_lesson7.py::test_customers_row_count_is_10 PASSED
test_lesson7.py::test_transactions_row_count_is_60 PASSED
test_lesson7.py::test_foreign_keys_are_enforced_on_the_connection PASSED
test_lesson7.py::test_duplicate_primary_key_is_rejected PASSED
test_lesson7.py::test_null_country_is_rejected PASSED
test_lesson7.py::test_demonstrate_rejection_reports_a_real_integrity_error PASSED

11 passed
```

All 11 green means your schema enforces the property checklist and your database
refuses a bad row on its own — no discipline required.

## Where this leads

The two-table schema you design here is the retail database that Lessons 8 and 9
query, and it is the same design the "One Analysis, Two Engines" assignment
(`sql-two-engines-assignment/`) grades you against — there you will answer real
business questions in SQL and pandas on top of exactly this structure.
