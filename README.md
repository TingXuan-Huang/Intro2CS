# Course Logistics

A hands-on Intro to Computer Science course for non-CS students, taught through Python, pandas, and real datasets. Each lesson is a runnable Jupyter notebook paired with instructor notes and, where relevant, a self-grading assignment.

> The course is data and application centric, focus on introducing common Python or Computer Science data processing workflows while keeping some rigorousness of the Computer Science ideas

## Lesson plan

### Phase 1 — Fundamentals

#### Lesson 1 — Data Types and Data Structures ✅

`[Lesson1_Data_Types_and_Structures.ipynb](Lesson1_Data_Types_and_Structures.ipynb)` · [Instructor notes](Lesson1_Instructor_Notes.md) · [Teaching notes on properties](note.md)

This lesson builds the representation mindset: choose native Python
structures by the operations they support, then connect mutability, references,
stacks, queues, NumPy arrays, DataFrames, and file representations.

**Extensions:** [Python data structures](https://docs.python.org/3/tutorial/datastructures.html) · [copying objects](https://docs.python.org/3/library/copy.html) · [NumPy absolute basics](https://numpy.org/doc/stable/user/absolute_beginners.html) · [Think Python](https://allendowney.github.io/ThinkPython/)

#### Lesson 2 — Files and pandas ✅

`[Lesson2_Files_and_pandas.ipynb](Lesson2_Files_and_pandas.ipynb)`

This lesson treats files as persistence with tradeoffs: load and inspect CSV,
JSON, Excel, and Parquet; select, filter, sort, transform, clean, group, merge,
and export DataFrames; and preserve enough metadata to make the analysis
reproducible.

**Extensions:** [pandas read/write tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html) · [pandas selection tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html) · [missing-data guide](https://pandas.pydata.org/docs/user_guide/missing_data.html) · [PyArrow and Parquet](https://arrow.apache.org/docs/python/parquet.html) · [Python for Data Analysis](https://wesmckinney.com/book/)

#### Assignment A1 — Four Formats, One Analysis ✅

`[pandas-finance-assignment/](pandas-finance-assignment/)` · [Assignment README](pandas-finance-assignment/README.md)

A self-grading pandas assignment that carries one financial analysis through CSV, JSON, Excel, and Parquet, so students experience firsthand what each format remembers, forgets, and costs. Includes a small finance library, dated FRED and Yahoo Finance snapshots, realistic data-cleaning tasks, and a final benchmark of the four formats. Checks live in `utils/test.py` and never reveal answers; nudges are in `hints.md`.

**Extensions:** [FRED API overview](https://fred.stlouisfed.org/docs/api/fred/overview.html) · [yfinance documentation](https://ranaroussi.github.io/yfinance/) · [pandas I/O guide](https://pandas.pydata.org/docs/user_guide/io.html) · [Jupyter getting started](https://docs.jupyter.org/en/stable/start/)

#### Lesson 3 — Bash, Virtual Environments, Git

**Three sessions.** The shell as a REPL for the computer; filesystem trees,
paths, pipes, and inspecting the retail CSV before pandas reads it; virtual
environments and dependency snapshots; Git status, commits, diffs, branches,
merges, and `.gitignore`; and running Python scripts outside Jupyter.

The exercise is a deliberately broken project with a wrong working directory,
missing dependency, and absent Git history. A checker verifies the environment,
requirements, and at least three meaningful commits.

#### Lesson 4 — Algorithms and Big-O ✅

`[Lesson3_Algorithms_and_BigO.ipynb](Lesson3_Algorithms_and_BigO.ipynb)`

This lesson turns everyday data tasks into algorithms: searching, sorting,
aggregation, matching, and hash joins, with Big-O used to explain why an
approach scales or fails on larger inputs.

**Extensions:** [Problem Solving with Algorithms and Data Structures using Python](https://runestone.academy/ns/books/published/pythonds3/index.html) · [Python](https://docs.python.org/3/library/bisect.html) `bisect` · [Python](https://docs.python.org/3/library/timeit.html) `timeit` · [sorting algorithms in Python](https://realpython.com/sorting-algorithms-python/)

#### Assignment A2 — Easy Algorithms

`[Lesson3_Assignment.md](Lesson3_Assignment.md)` — seven established LeetCode
problems plus a Big-O question bank.

#### Lesson 5 — Code Quality, Functional Programming, Testing

**Three sessions.** Functions as contracts; pure versus side-effecting
functions; type hints; comprehensions, `map`, `filter`, `sorted`, `zip`, and
`enumerate`; pandas method chains and vectorization; naming, refactoring,
modules, imports, tracebacks, narrow exception handling, validation, `assert`,
and `pytest`.

The exercise refactors a working-but-awful retail analysis script while making
a failing test suite pass, with Git checkpoints for each step.

### Phase 2 — Databases, APIs, and LLMs

#### Lesson 6 — Why Databases Exist + SQLite

**Two sessions.** File failure modes such as leading-zero loss and inconsistent
customer data → tables, schemas, keys, `NOT NULL`, primary keys, and foreign
keys → Python and SQLite with `sqlite3`, `to_sql`, and `read_sql` →
parameterized queries → when a database is preferable to a DataFrame or CSV.
The exercise designs and loads `customers` and `transactions` tables and
demonstrates an intentional integrity rejection.

#### Lesson 7 — SQL Fundamentals

**Two to three sessions.** `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, and
`DISTINCT` beside pandas equivalents → aggregates and `GROUP BY` → `HAVING`
versus `WHERE` → `NULL`, `IS NULL`, `COALESCE`, and dates → logical query
evaluation order. The exercise computes monthly revenue by country in SQL and
pandas, then uses `assert_frame_equal` to prove the results agree.

#### Lesson 8 — SQL Joins and Analytics

**Three sessions.** `INNER JOIN` and `LEFT JOIN` beside pandas `merge` →
`CASE WHEN` and conditional aggregation → CTEs and subqueries → window
functions (`ROW_NUMBER`, `RANK`, partitions, running totals, and top-k) →
interview patterns such as duplicates, gaps, and month-over-month change.

#### Assignment A3 — One Analysis, Two Engines

Answer the same business questions in SQL and pandas against the retail
database. A checker compares both engines with reference outputs, benchmarks
filtered SQL reads against loading everything into pandas, and includes
established interview-style drills.

#### Lesson 9 — APIs and HTTP

**Two sessions.** Clients, servers, URLs, endpoints, requests, responses,
headers, methods, and status codes → `requests` and FRED → API keys in
environment variables → JSON to DataFrame → rate limits, retries, pagination,
timeouts, disk caching, and reading unfamiliar API documentation. The exercise
fetches two FRED series, caches them, makes them monthly, and stores them in
the Lesson 6 SQLite database.

#### Lesson 10 — LLMs: First API Call

**Two sessions.** Tokens, next-token prediction, context windows, temperature,
and hallucination → messages and system/user prompts → raw HTTP and SDK calls
→ token-cost arithmetic → structured JSON output and validation → retries,
privacy, verification, and offline recorded-response fixtures. The exercise
classifies pinned economic-news headlines with structured JSON, validates every
response, and counts retries.

#### Assignment A4 — Integrated Mini-Project

Fetch two FRED series through the cached client, store them in SQLite, use SQL
for aggregates and joins, pandas for derived metrics, and an LLM for a
structured JSON summary whose numbers Python validates. The checker verifies
the schema, query results, and detection of a planted wrong number.

### Phase 3 — Uncertainty

#### Lesson 12 — Visualization with matplotlib

Figure and axes anatomy → explicit `fig, ax` usage → labels, titles, and
saving → line, bar, scatter, histogram, and box plots → pandas plotting,
subplots, dates, skew, and misleading charts. The exercise answers four
retail/FRED questions with appropriate labeled figures.

#### Lesson 13 — Probability and Monte Carlo

Random variables, expectation, variance, and reproducible seeds → Bernoulli,
Binomial, Normal, and Poisson distributions → conditional probability,
independence, and base rates → Monte Carlo decision analysis. The exercise
compares two inventory policies using expected profit and the 5th-percentile
outcome.

#### Lesson 14 — Inference Through A/B Testing

Samples and populations → bootstrap confidence intervals → permutation tests
and p-values → effect size, significance, power, randomization, p-hacking, and
multiple comparisons.

#### Assignment A5 — A/B Test

Students produce a lift estimate, bootstrap interval, permutation p-value, and
plain-language verdict from a pinned conversion dataset. The checker includes
a planted double-counting trap.

#### Lesson 15 — Linear and Logistic Regression

Linear regression, coefficients, units, residuals, and R² → multiple features
and dummy variables → logistic probabilities, thresholds, and log-odds →
standard errors and the bridge back to inference. The exercise predicts
monthly sales and customer churn from retail-derived features.

### Phase 4 — LLM Systems

#### Lesson 16 — RAG: Embeddings and Retrieval

Text to vectors and cosine similarity → chunking and brute-force retrieval →
retrieve-then-generate with source IDs → evaluating retrieval hits and
grounded answers. The exercise builds a mini-RAG over a pinned corpus and
requires the system to identify a question the corpus cannot answer.

#### Lesson 17 — LLM Tools and Agents

Function schemas as contracts → model-requested tool calls → a hand-written
think–act–observe loop → multiple tools and state → input validation, stop
conditions, and human oversight. The exercise adds one student-designed tool.

#### Lesson 18 — Cost-Aware Routing

Measure SQLite, Python, small-model, and large-model answers by latency, price,
and failure mode → route from cheap/certain to expensive/flexible → connect
routing graphs to shortest paths and priority queues. The exercise routes
twelve questions and compares total cost with an always-largest-model policy.

### Phase 5 — Machine Learning

#### Lesson 19 — ML Foundations

Features, labels, training, prediction, loss, and the `fit`/`predict` contract
→ decision trees and overfitting → random forests and boosting → k-means
segmentation, scaling, and choosing the number of clusters.

#### Lesson 20 — Evaluation Before Complexity

Train/test splits → overfitting and underfitting → baselines → cross-validation
and leakage → distribution shift → regression and classification metrics,
confusion matrices, and calibration.

#### Assignment A6 — Churn Model

An end-to-end pinned churn project. The checker validates metric ranges and
inspects that the test set was not used before final evaluation; a planted
leakage feature is the central debugging challenge.

#### Lesson 21 — Neural Networks, Conceptual

Neurons as logistic regression → layers and nonlinearities → gradient descent,
backpropagation, epochs, and batches → an MLP comparison against the logistic
baseline → when deep learning is appropriate for tabular data. The exercise
varies hidden-layer size and identifies where overfitting begins.

### Phase 6 — Statistical Extensions

#### Lesson 22 — Time-Series Forecasting

Trend, seasonality, residuals, lags, and autocorrelation → naive and
seasonal-naive baselines → moving averages and exponential smoothing →
autoregression and ARIMA → rolling-origin, time-respecting validation. The
exercise forecasts a FRED indicator six months ahead.

#### Lesson 23 — Markov Chains + Bayesian Updating

Customer lifecycle states and transition matrices → matrix powers and long-run
behavior → Bayesian prior, likelihood, posterior, and credible intervals →
MCMC as the conceptual connection between Bayesian models and Markov chains.
The exercise estimates customer transitions and updates a conversion-rate
posterior week by week.

### Phase 7 — Capstone

#### Lesson 24 — Capstone: Economic Question Agent

Choose an economic question → fetch FRED data through the cached client →
store and query it in SQLite → compute trends and bootstrap uncertainty bands
→ compare a statistical forecast with a naive baseline → retrieve supporting
passages → draft an explanation from verified numbers and sources → re-check
every figure and citation with an evaluator.

The deliverable is a Git project whose rubric maps each pipeline stage to the
lesson that taught it. Catching a planted error is required.

### Optional lessons

- **O1 — Stacks and Queues in Practice:** implement a stack and expression
  evaluator, use `deque` for a support-ticket queue, and measure why list
  front-pops are slow.
- **O2 — ANOVA and Poisson Regression:** compare four variants with ANOVA and
  model order counts with Poisson regression.
- **O3 — Graph Algorithms in Depth:** implement BFS, DFS, Dijkstra, and top-k
  with `heapq`; practice with established graph problems.
- **O4 — Advanced Probabilistic Models:** tour survival analysis, HMMs,
  state-space models, Kalman filtering, and one library-based MCMC example.

Assignments are spaced as A1 (Lesson 2), A2 (Lesson 4), A3 (Lesson 8), A4
(Lesson 11), A5 (Lesson 14), A6 (Lesson 20), and the capstone (Lesson 24).

## Dataset provenance and offline use

The course ships small, pinned extracts so class time never depends on a network connection:

- `course_data/online_retail_sample.csv` is a compact extract from the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail), licensed CC BY 4.0. Lesson 2 derives its controlled cleaning cases from this extract, and Lesson 3 uses it for one real-data algorithms application.
- Lesson 1 uses Fisher's Iris data through `scikit-learn` and selected views of the course retail extract.
- The finance assignment stores dated snapshots in `pandas-finance-assignment/data_offline/`. FRED data is public economic data. The Yahoo-derived snapshot is for this private educational course only and must not be redistributed; see [yfinance's usage notice](https://ranaroussi.github.io/yfinance/).

Each dataset source, retrieval date, row count, and checksum are recorded in `course_data/manifest.json`. Refreshing a snapshot is optional and never required to run a lesson.

## Setup

```bash
pip install pandas numpy pyarrow openpyxl yfinance matplotlib jupyter scikit-learn
```

Python 3.10+ recommended. A CSV stores textual fields, not pandas column dtypes; pandas may infer types when it reads one. JSON preserves JSON values but not pandas-specific dtypes, datetimes, or indexes. Run each notebook with:

```bash
jupyter lab <notebook>.ipynb
```
