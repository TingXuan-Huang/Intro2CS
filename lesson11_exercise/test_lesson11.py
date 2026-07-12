"""Tests for the Lesson 11 headline-classification exercise.

These tests import from ``classify.py`` -- the module YOU complete. In the
shipped state its three functions raise NotImplementedError, so every test
below fails on purpose: that is the intended starting point, not something
you broke. Implement validate_response, classify_headline, and
summarize_run until they pass.

Run from inside lesson11_exercise/ :

    python3 -m pytest test_lesson11.py -v

What the checker pins down:

  * validation REJECTS every malformed shape (missing key, out-of-range or
    non-numeric confidence, unknown category, extra keys, non-dict) and
    ACCEPTS a well-formed payload;
  * a headline whose first reply is malformed but whose retry is valid
    reports exactly one retry;
  * a headline that never returns a valid payload within MAX_ATTEMPTS is
    reported failed -- never classified from an invalid payload;
  * the whole run reproduces the pinned reference: 19 classified, 1 failed,
    7 retries, and the fixed per-category counts below.

The reference numbers come from the authored fixtures with MAX_ATTEMPTS = 3.
They are outcomes of correct validate + retry logic; you cannot shortcut
them by guessing, only by making the pipeline behave.
"""

import pytest

from classify import (
    CATEGORIES,
    MAX_ATTEMPTS,
    classify_headline,
    load_headlines,
    summarize_run,
    validate_response,
)

# Pinned reference for the full run (authored fixtures, MAX_ATTEMPTS = 3).
REFERENCE_COUNTS = {
    "monetary_policy": 3,
    "inflation": 3,
    "employment": 3,
    "markets": 4,
    "trade": 3,
    "housing": 3,
}
REFERENCE_RETRIES = 7
REFERENCE_CLASSIFIED = 19
REFERENCE_FAILED = 1


def headline_text(headline_id):
    """The exact headline text for an id, read from headlines.csv."""
    for row in load_headlines():
        if row["id"] == headline_id:
            return row["headline"]
    raise AssertionError(f"no headline with id {headline_id!r}")


# ------------------------------------------------------------- validation

def test_validate_accepts_a_well_formed_payload():
    assert validate_response({"category": "inflation", "confidence": 0.9}) is True


def test_validate_accepts_confidence_at_the_boundaries():
    assert validate_response({"category": "markets", "confidence": 0.0}) is True
    assert validate_response({"category": "markets", "confidence": 1.0}) is True


def test_validate_rejects_a_missing_required_key():
    assert validate_response({"category": "employment"}) is False


def test_validate_rejects_confidence_out_of_range():
    assert validate_response({"category": "markets", "confidence": 1.4}) is False


def test_validate_rejects_non_numeric_confidence():
    assert validate_response({"category": "markets", "confidence": "high"}) is False


def test_validate_rejects_a_boolean_confidence():
    # bool is a subclass of int in Python -- a validator must not let True
    # sneak through as the number 1.
    assert validate_response({"category": "markets", "confidence": True}) is False


def test_validate_rejects_a_category_outside_the_set():
    assert validate_response({"category": "recession", "confidence": 0.8}) is False


def test_validate_rejects_extra_keys():
    payload = {"category": "trade", "confidence": 0.7, "reason": "tariffs"}
    assert validate_response(payload) is False


def test_validate_rejects_a_non_dict_payload():
    assert validate_response(["markets", 0.9]) is False
    assert validate_response("markets") is False


def test_validate_covers_every_legal_category():
    for category in CATEGORIES:
        assert validate_response({"category": category, "confidence": 0.5}) is True


# ------------------------------------------------------- single headline

def test_clean_headline_needs_no_retries():
    # h01's first reply is already valid JSON matching the schema.
    result = classify_headline(headline_text("h01"))
    assert result["ok"] is True
    assert result["category"] in CATEGORIES
    assert result["retries"] == 0


def test_recoverable_headline_reports_one_retry():
    # h06's first reply is code-fence-wrapped (unparseable); its retry is clean.
    result = classify_headline(headline_text("h06"))
    assert result["ok"] is True
    assert result["category"] == "housing"
    assert result["retries"] == 1


def test_headline_that_never_validates_is_reported_failed():
    # h19's three replies are all malformed (prose, wrong key, unknown
    # category): it must fail, not slip through classified.
    result = classify_headline(headline_text("h19"))
    assert result["ok"] is False
    assert result["category"] is None
    assert result["confidence"] is None
    assert result["retries"] == MAX_ATTEMPTS - 1


def test_headline_recovers_on_the_last_allowed_attempt():
    # h20 is invalid twice, then valid on the third attempt.
    result = classify_headline(headline_text("h20"))
    assert result["ok"] is True
    assert result["category"] == "markets"
    assert result["retries"] == 2


# ------------------------------------------------------------- whole run

def test_run_category_counts_match_reference():
    assert dict(summarize_run()["category_counts"]) == REFERENCE_COUNTS


def test_run_total_retries_match_reference():
    assert summarize_run()["retries"] == REFERENCE_RETRIES


def test_run_classified_and_failed_counts():
    summary = summarize_run()
    assert summary["classified"] == REFERENCE_CLASSIFIED
    assert summary["failed"] == REFERENCE_FAILED


def test_run_totals_are_internally_consistent():
    summary = summarize_run()
    assert summary["classified"] + summary["failed"] == len(load_headlines())
    assert sum(summary["category_counts"].values()) == summary["classified"]


def test_no_headline_is_classified_from_an_invalid_payload():
    # Every headline reported ok must carry a legal category and an in-range
    # confidence; every failed one must carry neither.
    for row in load_headlines():
        result = classify_headline(row["headline"])
        if result["ok"]:
            assert result["category"] in CATEGORIES
            assert 0.0 <= result["confidence"] <= 1.0
        else:
            assert result["category"] is None
            assert result["confidence"] is None
