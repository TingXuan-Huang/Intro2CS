# Lesson 5 exercise — refactor and test

You have a script that **works** and a test suite that **fails**. Your job is to
make the tests pass by refactoring the script into clean, importable functions —
*without changing a single number the script prints.*

This is the whole lesson in one sitting: extract functions (Unit 3), keep them
honest with pytest (Unit 5), and checkpoint each green step with git (Lesson 3).

## What's in this folder

- **`messy_analysis.py`** — a working retail analysis. It prints correct numbers
  and commits every code smell from Unit 3: copy-pasted country loops, a magic
  `1.0`, a deeply nested top-3 loop, and `print` where a `return` belongs. It is
  your reference for *correct behaviour*. **Do not edit it.**
- **`test_lesson5.py`** — the checker. It imports from `analysis.py` (a file you
  create) and pins down the contract in its module docstring. **Do not edit it.**
- **`analysis.py`** — *you create this.* It is where your refactored functions live.

## The goal

Create `analysis.py` in this folder with four functions —
`load_transactions`, `clean_prices`, `revenue_by_country`, `top_customers` —
so that every test in `test_lesson5.py` passes. The full contract (arguments,
return types, rounding, tie-breaks, edge cases) is written out in the docstring
at the top of `test_lesson5.py`. Read it first; it is the spec.

The one rule: the numbers must not change. `messy_analysis.py` already computes
the right answers — your refactor only changes the *shape* of the code, never its
results.

## The loop

Work one function at a time. After each function, run the tests and commit.

```bash
# 0. See the correct numbers you must preserve (run once, keep the output handy).
python3 messy_analysis.py

# 1. Read the contract — the docstring at the top of the checker IS the spec.
#    Open test_lesson5.py in your editor (its first ~30 lines spell out every
#    function's arguments, return type, rounding, and tie-break rule).

# 2. In shipped state the checker fails to even import, because analysis.py
#    does not exist yet. That is the intended starting point:
python3 -m pytest test_lesson5.py -v      # -> ModuleNotFoundError: No module named 'analysis'

# 3. Create analysis.py and extract ONE function into it (start with load_transactions).
#    Re-run the tests: some now pass, the rest still fail. That is progress.
python3 -m pytest test_lesson5.py -v

# 4. Commit the green step, the way Lesson 3 taught — small, honest checkpoints.
git add analysis.py
git commit -m "Add load_transactions: tests for loading now pass"

# 5. Repeat 3–4 for clean_prices, revenue_by_country, and top_customers.
```

Run just one test while you work on it, with `-k`:

```bash
python3 -m pytest test_lesson5.py -v -k top_customers
```

Read a failure bottom-up, like a traceback (Unit 4): the last lines show the
assert that broke and the two values it compared.

## What "done" looks like

```
============================== 12 passed in 0.04s ==============================
```

All **12 tests** pass, and your git log tells the story as a sequence of green
steps:

```bash
git log --oneline      # ideally one commit per function, each message saying WHY
```

## One warning

A few tests describe inputs `messy_analysis.py` never actually meets — an empty
table, three customers tied on spend, a single row, more customers requested than
exist. You **cannot** discover those answers by running the script; it never hits
those cases. Decide what the script's logic *would* do by reading it:

- What does the tie-break in the top-3 selection loop prefer when totals are equal?
- What should `revenue_by_country` return when there are no rows to total?
- What should `top_customers(frame, 3)` return when the frame has only one customer?

Reading the logic and encoding it — that is the skill this exercise is training.

## Where this leads

Every self-grading checker in this course — including the one grading you right
now — is a pytest suite exactly like the ones you are learning to satisfy. The
module-plus-tests shape you build here (named functions with contracts, edge
cases answered by reading logic) is the shape the integrated mini-project
assignment and the capstone are graded in.
