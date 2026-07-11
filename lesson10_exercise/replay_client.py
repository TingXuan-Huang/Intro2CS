"""Replay client for the Lesson 10 exercise -- PROVIDED, do not edit.

This is an offline stand-in for a real LLM call. Instead of reaching the
network, it replays an *authored teaching fixture* recorded in the exact
Anthropic Messages API wire shape (see fixtures/manifest.json). It is the
same idea as the lesson notebook's ``call_llm``, narrowed to exactly what
this exercise needs so you can spend your effort on validation, not I/O.

The mapping lives in ``fixtures/index.json``: each headline points to an
ordered list of response files. Asking for attempt 0 replays the first
file, attempt 1 the second, and so on -- so a headline whose first reply is
malformed can have a better reply waiting at the next attempt. The sequence
is deterministic: the same (headline, attempt) always returns the same
authored response.

You will call two functions from ``classify.py``:

    call_model(headline, attempt=0) -> dict
        The raw response payload for this attempt, in wire shape. Raises
        IndexError if you ask for an attempt that was never recorded --
        that means your retry loop ran past MAX_ATTEMPTS.

    response_text(payload) -> str
        Pull the model's generated text out of a wire-shape payload. This
        text is what you must parse and validate -- it carries no promise
        of being valid JSON.
"""

import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

_INDEX = None


def _index():
    """Load fixtures/index.json once: {headline text -> [response files...]}."""
    global _INDEX
    if _INDEX is None:
        _INDEX = json.loads((FIXTURES_DIR / "index.json").read_text(encoding="utf-8"))
    return _INDEX


def call_model(headline, attempt=0):
    """Replay the recorded response for ``headline`` at this ``attempt``.

    ``attempt`` is 0-based: 0 is the first reply, 1 the first retry, etc.
    Returns the raw payload (a dict) exactly as an API call would, in the
    Anthropic Messages wire shape.
    """
    responses = _index().get(headline)
    if responses is None:
        raise KeyError(f"no fixtures were recorded for headline: {headline!r}")
    if attempt >= len(responses):
        raise IndexError(
            f"headline {headline!r} has only {len(responses)} recorded "
            f"response(s); your retry loop asked for attempt {attempt}. "
            f"A bounded retry loop should stop at MAX_ATTEMPTS."
        )
    path = FIXTURES_DIR / responses[attempt]
    return json.loads(path.read_text(encoding="utf-8"))


def response_text(payload):
    """Return the model's generated text from a wire-shape response payload."""
    return payload["content"][0]["text"]
