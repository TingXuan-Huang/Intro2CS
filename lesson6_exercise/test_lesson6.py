"""Tests for the Lesson 6 FRED-client exercise.

These tests import the two functions you write in ``fred_client.py`` and
exercise them entirely against the pinned fixtures in ./fixtures -- NO network
and NO API key (any real key in your environment is scrubbed below, so it cannot
leak into the checker). Until you implement a function it raises
NotImplementedError and its tests fail with that message: that is the intended
starting line, not something you broke.

Run from inside lesson6_exercise/ :

    python3 -m pytest test_lesson6.py -v

The full contract lives in the fred_client.py module docstring. The pinned
numbers below come straight from the fixtures (see fixtures/manifest.json):

    DGS10     1439 daily observations, 60 of them "."  -> 67 monthly rows
    UNRATE      65 monthly observations                 -> 65 monthly rows
    CPIAUCSL    64 monthly observations                 -> 64 monthly rows
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from fred_client import get_series, tidy_monthly

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _force_offline(monkeypatch):
    """No test may depend on a live key -- scrub it for every test."""
    monkeypatch.delenv("FRED_API_KEY", raising=False)


def raw_frame(series_id):
    """Read a fixture the way a correct get_series would return it.

    Lets the tidy_monthly tests run on realistic input even before
    get_series is finished, so you can make progress one function at a time.
    """
    payload = json.loads((FIXTURES / f"{series_id}.json").read_text())
    return pd.DataFrame(payload["observations"])[["date", "value"]]


# ----------------------------------------------- get_series: fetch + caching

def test_get_series_returns_raw_two_column_frame(tmp_path):
    raw = get_series("DGS10", cache_dir=tmp_path / "cache", fixtures_dir=FIXTURES)
    assert list(raw.columns) == ["date", "value"]
    assert len(raw) == 1439
    assert raw.iloc[0]["date"] == "2021-01-04"
    # Values arrive as strings in FRED's wire shape, "." included (not yet numbers).
    assert (raw["value"] == ".").sum() == 60


def test_get_series_writes_a_json_cache_file(tmp_path):
    cache = tmp_path / "cache"
    get_series("DGS10", cache_dir=cache, fixtures_dir=FIXTURES)
    assert (cache / "DGS10.json").exists()          # the cache the next call will reuse


def test_second_call_is_served_from_cache(tmp_path):
    cache = tmp_path / "cache"
    first = get_series("UNRATE", cache_dir=cache, fixtures_dir=FIXTURES)

    # Point the fallback at an EMPTY directory. If the second call still returns
    # the same data, it can only have come from the cache -- exactly the
    # resolution order the contract requires (cache hit beats everything).
    empty = tmp_path / "no_fixtures_here"
    empty.mkdir()
    second = get_series("UNRATE", cache_dir=cache, fixtures_dir=empty)
    pd.testing.assert_frame_equal(first, second)


# --------------------------------------------------------------- tidy_monthly

def test_tidy_monthly_schema():
    monthly = tidy_monthly(raw_frame("DGS10"))
    assert list(monthly.columns) == ["month", "value"]
    assert pd.api.types.is_datetime64_any_dtype(monthly["month"])
    assert pd.api.types.is_float_dtype(monthly["value"])
    assert monthly["month"].is_monotonic_increasing
    assert monthly["value"].notna().all()           # missing "." rows were dropped
    assert list(monthly.index) == list(range(len(monthly)))


def test_tidy_monthly_collapses_daily_to_months():
    monthly = tidy_monthly(raw_frame("DGS10"))
    assert len(monthly) == 67                        # Jan 2021 .. Jul 2026
    first = monthly.iloc[0]
    assert first["month"] == pd.Timestamp("2021-01-01")
    assert first["value"] == pytest.approx(1.0811, abs=1e-3)   # mean of Jan-2021 dailies


def test_tidy_monthly_keeps_monthly_series_intact():
    monthly = tidy_monthly(raw_frame("UNRATE"))
    assert len(monthly) == 65
    assert monthly.iloc[0]["month"] == pd.Timestamp("2021-01-01")
    assert monthly.iloc[0]["value"] == pytest.approx(6.4)
    assert monthly.iloc[-1]["value"] == pytest.approx(4.2)


def test_tidy_monthly_averages_and_drops_missing():
    # Two March readings average to 2.0; April is "." (dropped, NOT reinvented as
    # an empty month); May stands alone.
    raw = pd.DataFrame({
        "date": ["2020-03-05", "2020-03-25", "2020-04-01", "2020-05-10"],
        "value": ["1.0", "3.0", ".", "5.0"],
    })
    monthly = tidy_monthly(raw)
    assert list(monthly["month"]) == [pd.Timestamp("2020-03-01"), pd.Timestamp("2020-05-01")]
    assert list(monthly["value"]) == pytest.approx([2.0, 5.0])


def test_tidy_monthly_does_not_mutate_its_input():
    raw = raw_frame("UNRATE")
    before = raw.copy()
    tidy_monthly(raw)
    pd.testing.assert_frame_equal(raw, before)


def test_tidy_monthly_on_an_empty_frame():
    empty = raw_frame("UNRATE").head(0)
    out = tidy_monthly(empty)
    assert list(out.columns) == ["month", "value"]
    assert len(out) == 0
