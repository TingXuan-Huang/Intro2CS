# Intro to CS

A hands-on Intro to Computer Science course for non-CS students, taught through Python, pandas, and real datasets. Each lesson is a runnable Jupyter notebook paired with instructor notes and, where relevant, a self-grading assignment.

## Lesson plan

### Lesson 1 — Data Types and Data Structures
[`Lesson1_Data_Types_and_Structures.ipynb`](Lesson1_Data_Types_and_Structures.ipynb) · [Instructor notes](Lesson1_Instructor_Notes.md) · [Teaching notes on properties](note.md)

Builds the reasoning students carry through the rest of the course: *"This is one customer, so a dictionary. Many customers, so a list of dictionaries or a DataFrame. IDs must be unique, so a set. Fast lookup by ID, so a dictionary."*

| Unit | Topic | Time |
|---|---|---|
| Review | Python's built-in types and structures, dynamic typing vs. C/Java | — |
| 3 | Core data structures — list, tuple, set, dictionary | ~70 min |
| 4 | Mutability, references, and copying | ~30 min |
| 5 | Stacks and queues; hash maps and trees as mental models | ~30 min |
| 6 | NumPy and pandas with a real dataset (Iris) | ~60 min |
| 7 | How data structures shape file storage | ~35 min |

Recommended split: **Session A** (Units 1–4, ~2 hrs) covers the conceptual core; **Session B** (Units 5–8, ~2 hrs) covers stacks/queues, arrays/DataFrames, file formats, and the integrated exercise.

### Lesson 2 — Files and pandas
[`Lesson2_Files_and_pandas.ipynb`](Lesson2_Files_and_pandas.ipynb)

Takes a dataset from raw file to trustworthy analysis: load it, interrogate it, clean it, and export it reproducibly.

| Unit | Topic | Time |
|---|---|---|
| 1 | Files and persistence | ~20 min |
| 2 | Four file formats (CSV, JSON, Excel, Parquet) | ~30 min |
| 3 | Paths and loading | ~35 min |
| 4 | Interview the DataFrame before trusting it — seven questions | ~40 min |
| 5 | Selecting, filtering, sorting, transforming | ~45 min |
| 6 | Cleaning — types, missing values, duplicates, text normalization, range checks | ~55 min |
| 7 | Grouping and summarizing — aggregation, `groupby`, pivot tables | ~35 min |
| 8 | Combining tables with `merge` | ~40 min |
| 9 | Exporting and reproducibility | ~25 min |

### Lesson 3 — Algorithms and Big-O
[`Lesson3_Algorithms_and_BigO.ipynb`](Lesson3_Algorithms_and_BigO.ipynb)

Reopens the pandas operations from Lesson 2 as algorithms, then names how their cost grows.

| Unit | Topic | Time |
|---|---|---|
| 1 | What is an algorithm? Anatomy, the linear scan, analytics verbs as scans | ~75 min |
| 2 | Searching and sorting — linear search, binary search, sorting, the preparation trade-off | ~80 min |
| 3 | Big-O — the five complexity classes: O(1), O(log n), O(n), O(n log n), O(n²) | ~80 min |
| 4 | Aggregation, matching, and joins — the algorithm inside `merge` | ~80 min |

### Assignment — Four Formats, One Analysis
[`pandas-finance-assignment/`](pandas-finance-assignment/) · [Assignment README](pandas-finance-assignment/README.md)

A self-grading pandas assignment that carries one financial analysis through CSV, JSON, Excel, and Parquet, so students experience firsthand what each format remembers, forgets, and costs. Includes a small finance library, real data (FRED, Yahoo Finance), realistic data-cleaning tasks, and a final benchmark of the four formats. Checks live in `utils/test.py` and never reveal answers; nudges are in `hints.md`.

## Setup

```bash
pip install pandas numpy pyarrow openpyxl yfinance matplotlib jupyter
```

Python 3.10+ recommended. Run each notebook with:

```bash
jupyter lab <notebook>.ipynb
```
