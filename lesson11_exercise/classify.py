"""Lesson 11 exercise -- classify economic-news headlines with validated JSON.

An LLM's reply is the first data in this course with NO guaranteed
properties. You asked for JSON of the shape {"category", "confidence"};
what comes back is *text* that is usually that JSON and sometimes is not.
Your job is to trust nothing until you have checked it, and to retry when a
reply fails the check -- exactly Lesson 5's validate-early habit, applied to
a source that can hand you anything.

Fill in the three functions marked TODO, then run the checker from inside
this folder:

    python3 -m pytest test_lesson11.py -v

You do not make any real API calls. ``replay_client`` replays authored
teaching fixtures (see fixtures/manifest.json) so the whole exercise runs
offline and deterministically.

------------------------------------------------------------------ contract

validate_response(payload) -> bool
    ``payload`` is whatever ``json.loads`` produced from the model's text.
    Return True only if it satisfies the schema, and False otherwise:
      - it is a dict whose keys are EXACTLY {"category", "confidence"};
      - "category" is one of CATEGORIES;
      - "confidence" is a real number (int or float, but NOT a bool) with
        0.0 <= confidence <= 1.0.
    Never raise on a bad payload -- a validator that crashes is no safer
    than no validator. Just return False.

classify_headline(headline) -> dict
    Ask the model (via call_model) for a classification, up to MAX_ATTEMPTS
    times. On each attempt: read the reply text, try to json.loads it (a
    parse failure is just an invalid attempt -- catch it and retry), then
    validate_response the parsed payload. Stop at the first VALID payload.
    Return a dict:
        {"category": str,   "confidence": float, "retries": int, "ok": True}
    where "retries" is how many RETRIES it took (0 if the first attempt was
    valid, 1 if the second, ...). If no attempt within MAX_ATTEMPTS produces
    a valid payload, return:
        {"category": None, "confidence": None, "retries": MAX_ATTEMPTS - 1,
         "ok": False}
    A headline must NEVER be reported classified from a payload that failed
    validation.

summarize_run() -> dict
    Classify every headline from load_headlines() and tally the run:
        {"category_counts": {category: count of headlines classified as it},
         "retries": total retries across all headlines,
         "classified": how many headlines got a valid classification,
         "failed": how many exhausted MAX_ATTEMPTS without one}
    Count a headline under a category only if it was actually classified.
"""

import csv
from pathlib import Path

from replay_client import call_model, response_text

# The fixed set of legal categories -- the "set membership" property a valid
# response must respect (Lesson 1). Anything outside this set is invalid.
CATEGORIES = {
    "monetary_policy",
    "inflation",
    "employment",
    "markets",
    "trade",
    "housing",
}

# The retry budget: how many attempts a single headline gets before we give
# up on it. Changing this changes the pinned reference numbers.
MAX_ATTEMPTS = 3

HEADLINES_PATH = Path(__file__).parent / "headlines.csv"


def load_headlines():
    """Return the headlines as a list of {"id", "headline"} dicts. PROVIDED."""
    with open(HEADLINES_PATH, newline="", encoding="utf-8") as handle:
        return [
            {"id": row["id"], "headline": row["headline"]}
            for row in csv.DictReader(handle)
        ]


def validate_response(payload):
    """Return True only if ``payload`` satisfies the schema (see contract)."""
    # TODO: implement the property checks described in the contract above.
    raise NotImplementedError("implement validate_response(payload)")


def classify_headline(headline):
    """Classify one headline with a bounded retry loop (see contract)."""
    # TODO: loop up to MAX_ATTEMPTS times over call_model / response_text,
    # parse + validate each reply, and return the result dict.
    raise NotImplementedError("implement classify_headline(headline)")


def summarize_run():
    """Classify every headline and tally the run (see contract)."""
    # TODO: call classify_headline for each row of load_headlines() and
    # aggregate category_counts, retries, classified, and failed.
    raise NotImplementedError("implement summarize_run()")


if __name__ == "__main__":
    # A tiny manual smoke test once you have implemented the functions.
    summary = summarize_run()
    print("category counts:", summary["category_counts"])
    print("total retries  :", summary["retries"])
    print("classified     :", summary["classified"], "| failed:", summary["failed"])
