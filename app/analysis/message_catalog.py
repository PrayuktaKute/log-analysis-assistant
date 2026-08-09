"""Deterministic categorization of log messages into failure categories
(e.g. 'database', 'network'), loaded from a configurable JSON file rather
than hardcoded -- so this module isn't tied to any one log source.

This is the "related error patterns" signal `EventCorrelator` uses: two
events with different messages but the same category (e.g. "Redis
connection lost" and "Redis cache miss") are considered related, without
any embedding/similarity model.

The config file (default: `config/message_categories.json`, overridable via
`settings.message_category_config_path`) has two sections:

- "categories": an exact message-text -> category lookup.
- "keyword_fallback": category -> list of substrings, checked
  case-insensitively against any message not found in "categories".

If the configured file is missing or invalid, `categorize()` degrades to
returning `UNCATEGORIZED` for everything (logged once) rather than raising
-- a missing/misconfigured category file should never crash analysis.
"""

import json
from functools import lru_cache
from pathlib import Path

from loguru import logger

from app.config import settings

UNCATEGORIZED = "uncategorized"


@lru_cache(maxsize=8)
def _load_category_config(path_str: str) -> tuple[dict[str, str], tuple[tuple[str, str], ...]]:
    """Load and flatten the category config at `path_str`. Cached per path
    so repeated `categorize()` calls don't re-read/re-parse the file."""
    path = Path(path_str)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.warning("Message category config not found at {} -- categorize() will return '{}' for everything", path, UNCATEGORIZED)
        return {}, ()
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load message category config at {}: {} -- falling back to '{}'", path, exc, UNCATEGORIZED)
        return {}, ()

    message_to_category: dict[str, str] = {}
    for category, messages in raw.get("categories", {}).items():
        for message in messages:
            message_to_category[message] = category

    keyword_pairs: list[tuple[str, str]] = []
    for category, keywords in raw.get("keyword_fallback", {}).items():
        for keyword in keywords:
            keyword_pairs.append((keyword.lower(), category))

    return message_to_category, tuple(keyword_pairs)


def categorize(message: str, config_path: Path | str | None = None) -> str:
    """Return the failure category for a message: exact match against the
    config's "categories" first, then "keyword_fallback" substring match,
    else `UNCATEGORIZED`."""
    path = str(config_path) if config_path is not None else str(settings.message_category_config_path)
    message_to_category, keyword_pairs = _load_category_config(path)

    if message in message_to_category:
        return message_to_category[message]

    lowered = message.lower()
    for keyword, category in keyword_pairs:
        if keyword in lowered:
            return category

    return UNCATEGORIZED


def categories_mentioned_in(text: str, config_path: Path | str | None = None) -> set[str]:
    """Return every known category whose name or keywords appear in `text`
    (case-insensitive substring match). Used to deterministically filter
    "current evidence" down to what's relevant to a free-text question
    (e.g. QAEngine matching "Show PostgreSQL errors" to the 'database'
    category) without any LLM call."""
    path = str(config_path) if config_path is not None else str(settings.message_category_config_path)
    message_to_category, keyword_pairs = _load_category_config(path)

    lowered = text.lower()
    matches: set[str] = set()

    all_categories = set(message_to_category.values()) | {category for _, category in keyword_pairs}
    for category in all_categories:
        if category.lower() in lowered:
            matches.add(category)

    for keyword, category in keyword_pairs:
        if keyword in lowered:
            matches.add(category)

    return matches
