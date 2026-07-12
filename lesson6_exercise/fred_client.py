"""fred_client.py -- the Lesson 6 API exercise starts here.

You are building the small client that Assignment 1's snapshots could have come
from: fetch a FRED economic series and tidy it to a monthly table. Lesson 7 will
give that table a schema and durable SQLite storage.

Fill in the two functions below. The checker (test_lesson6.py) runs entirely on
the offline fixtures in ./fixtures with NO network and NO API key, so you can
develop completely offline. Run it from inside lesson6_exercise/ :

    python3 -m pytest test_lesson6.py -v

Until you implement a function it raises NotImplementedError and its tests fail
with that message -- that is the intended starting line, not a bug you
introduced.

------------------------------------------------------------------------------
THE CONTRACT (implement exactly this behaviour)
------------------------------------------------------------------------------

get_series(series_id, *, cache_dir=CACHE_DIR, fixtures_dir=FIXTURES_DIR,
           api_key=None) -> pandas.DataFrame
    Return the RAW observations for one FRED series as a two-column DataFrame
    with columns ["date", "value"] -- both strings, exactly FRED's wire shape,
    where a "value" of "." means a missing observation. (Tidying comes later.)

    Resolve the source in this order -- the FIRST hit wins:

        1. cache hit   cache_dir / f"{series_id}.json" already exists
                       -> load that file, perform NO fetch.
        2. live        an API key is available (the api_key argument, else the
                       FRED_API_KEY environment variable)
                       -> fetch from the real FRED endpoint over HTTP, then WRITE
                          the JSON response into the cache.
        3. fixture     no cache and no key
                       -> load fixtures_dir / f"{series_id}.json" (the offline
                          fallback that keeps this course runnable), then WRITE it
                          into the cache.

    Create cache_dir if it does not exist. The cache write in steps 2 and 3 is
    the whole point: a SECOND call for the same series is served from the cache
    without re-reading the fixture or re-hitting the network. This
    cache-first-with-fallback pattern is reused by every later lesson.

    Why cache the raw JSON (rather than a tidied CSV)? Lesson 2's lesson: the JSON
    is the exact bytes the server sent, so a cached copy re-parses identically to
    a live response -- downstream code cannot tell them apart.

tidy_monthly(observations) -> pandas.DataFrame
    Given a raw observations frame (string columns "date" and "value"), return a
    NEW frame with EXACTLY two columns, in this order:

        month : datetime64, the first day of each month, ascending, one row/month
        value : float64, that month's MEAN reading, with no missing values

    Turn "." (and any other non-numeric token) into NaN and DROP it before
    aggregating. A daily series (DGS10) collapses to one average per month; an
    already-monthly series (UNRATE) keeps its single reading per month. Reset the
    index to 0..n-1. Never invent a month that has no observation. Must not modify
    the frame it is given. An empty input returns an empty frame that still has
    the two columns.

"""

import json  # noqa: F401  (you will need this to read/write the JSON cache)
import os  # noqa: F401  (you will need this to read FRED_API_KEY)
from pathlib import Path

import pandas as pd

# Paths resolve relative to THIS file, so the client behaves the same no matter
# which directory you run it from. Anything written under data/ is gitignored.
HERE = Path(__file__).resolve().parent
FIXTURES_DIR = HERE / "fixtures"
CACHE_DIR = HERE / "data" / "api_cache"

# The real endpoint, used only when an API key is present (never in the checker).
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"


def get_series(series_id, *, cache_dir=CACHE_DIR, fixtures_dir=FIXTURES_DIR,
               api_key=None):
    """Fetch raw FRED observations with cache -> live -> fixture resolution.

    Returns a DataFrame with string columns ["date", "value"].
    See the module docstring for the full contract.
    """
    raise NotImplementedError("implement get_series (see the contract in the module docstring)")


def tidy_monthly(observations):
    """Tidy a raw observations frame to a monthly ['month', 'value'] frame.

    See the module docstring for the full contract.
    """
    raise NotImplementedError("implement tidy_monthly (see the contract in the module docstring)")


# A tiny manual smoke test, so you can watch the pipeline work before pytest.
# Runs fully offline (no key) against the fixtures; writes the raw JSON cache under
# ./data (ignored). Lesson 7 is where this tidy table becomes a database table.
if __name__ == "__main__":
    raw = get_series("DGS10")
    print("raw rows:", len(raw))
    monthly = tidy_monthly(raw)
    print(monthly.head())
