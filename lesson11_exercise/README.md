# Lesson 11 exercise — Classify headlines with validated JSON

An LLM's reply is the first data in this course with **no guaranteed
properties**. You will ask a model to sort economic-news headlines into a
fixed set of categories and to answer in JSON — and then you will refuse to
believe a single reply until you have checked it against a schema, retrying
when a reply fails.

You write no networking code and make no real API calls. A provided
`replay_client` replays **authored teaching fixtures** (responses written by
hand in the real Anthropic Messages API wire shape — see
`fixtures/manifest.json`), so the exercise runs offline and gives the same
result every time. Some of those replies are deliberately malformed: a
code-fence wrapper, prose wrapped around the JSON, a missing key, an
out-of-range confidence, a category that isn't on the list, and one reply
that is not JSON at all. Your validation has to catch every one.

## Your job

Open `classify.py` and implement the three functions marked `TODO`. The full
contract is in that file's docstring; in short:

- **`validate_response(payload)`** — return `True` only if `payload` is a dict
  with exactly the keys `{"category", "confidence"}`, a `category` drawn from
  the legal set, and a numeric `confidence` in `0.0..1.0`. Never raise on bad
  input; just return `False`.
- **`classify_headline(headline)`** — ask the model (via `call_model`) up to
  `MAX_ATTEMPTS` times, parsing and validating each reply, stopping at the
  first valid one. Report the category, the confidence, and how many
  **retries** it took — or that it failed. A headline must never be reported
  classified from a payload that failed validation.
- **`summarize_run()`** — classify every headline and tally the run: per-category
  counts, total retries, how many were classified, and how many failed.

`load_headlines()` and the whole `replay_client` are provided — the exercise
is about validation and control flow, not I/O.

## Commands

Run from inside this folder:

```bash
cd lesson11_exercise
python3 -m pytest test_lesson11.py -v
```

Before you start, run it once and watch it fail: the three functions raise
`NotImplementedError`, so every test errors out. That is the intended starting
state. You are done when the whole suite is green.

You can also smoke-test your work directly:

```bash
python3 classify.py
```

## What "done" looks like

- `python3 -m pytest test_lesson11.py -v` reports all tests passing.
- The full run reproduces the pinned reference: **19** headlines classified,
  **1** failed, **7** retries in total.
- No headline is ever reported classified from a reply that failed the schema
  — the failing headline stays failed, and its revenue-of-trust stays zero.

## Files

| File | Role |
| --- | --- |
| `headlines.csv` | 20 authored economic-news-style headlines (`id,headline`) |
| `fixtures/` | 27 authored response fixtures in wire shape + `manifest.json` + `index.json` |
| `replay_client.py` | Provided offline stand-in for an API call — do not edit |
| `classify.py` | **You edit this** — three functions to implement |
| `test_lesson11.py` | The checker — pins the schema, the retry counts, and the run totals |

The categories are `monetary_policy`, `inflation`, `employment`, `markets`,
`trade`, `housing`. The headlines and the model replies are teaching fixtures
authored for this exercise, not real quotations or recordings of live calls.

## Where this leads

Validate-then-trust is the whole game with LLM output. The classify-validate-retry
loop you build here becomes the LLM layer of the integrated mini-project
assignment (A4, after Lesson 11), where every number the model writes gets checked by your
Python before anyone believes it.
