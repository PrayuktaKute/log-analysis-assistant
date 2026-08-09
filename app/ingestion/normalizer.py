"""Normalize parsed log entries into a consistent shape across sources.

Responsible for requirement #2: "Parse and normalize logs" (normalization
half). For the wilston dataset the three sources already share identical
field vocabulary, so normalization here is intentionally narrow:

- ensure every timestamp is timezone-aware UTC
- collapse incidental whitespace in messages (e.g. the double space left
  behind on lines with no `orderId`)
- sort the batch chronologically, since entries are read one file at a
  time and later stages need a unified timeline across sources

This does NOT correlate events across sources -- that's `app.correlation`.
"""

from datetime import timezone

from app.models.schemas import LogEntry


class LogNormalizer:
    """Normalizes a batch of parsed LogEntries from one or more sources."""

    def normalize(self, entries: list[LogEntry]) -> list[LogEntry]:
        normalized: list[LogEntry] = []

        for entry in entries:
            timestamp = entry.timestamp
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            else:
                timestamp = timestamp.astimezone(timezone.utc)

            message = " ".join(entry.message.split())

            if timestamp != entry.timestamp or message != entry.message:
                entry = entry.model_copy(update={"timestamp": timestamp, "message": message})
            normalized.append(entry)

        normalized.sort(key=lambda e: e.timestamp)
        return normalized
