"""Detect repeated failure signatures and bursts within a configurable
time window.

Responsible for requirement 4, "Failure Pattern Detection". Built directly
on top of `ErrorGrouper`: every message signature occurring at least
`threshold` times becomes a `FailurePattern`; a sliding-window scan then
finds that signature's densest cluster of occurrences, flagging it as a
"burst" if that peak *also* reaches `threshold` within `window_minutes`.
"""

from datetime import datetime, timedelta
from typing import Optional

from app.analysis.error_grouping import ErrorGrouper
from app.config import settings
from app.models.schemas import FailurePattern, LogEntry


class FailureDetector:
    """Identifies recurring and bursting failure signatures within LogEntries."""

    def __init__(
        self,
        threshold: int = settings.repeated_failure_threshold,
        window_minutes: int = settings.repeated_failure_window_minutes,
        grouper: Optional[ErrorGrouper] = None,
    ):
        self.threshold = threshold
        self.window_minutes = window_minutes
        self.window = timedelta(minutes=window_minutes)
        self.grouper = grouper or ErrorGrouper()

    def detect_repeated_failures(self, entries: list[LogEntry]) -> list[FailurePattern]:
        """Return a FailurePattern for every message signature occurring
        `threshold` times or more, enriched with burst metrics.

        Sorted by occurrence count descending (biggest recurring problem
        first), tie-broken alphabetically by message for determinism.
        """
        raw_groups = self.grouper.group_raw(entries)
        summaries = {group.message: group for group in self.grouper.group(entries)}

        patterns: list[FailurePattern] = []
        for message, ordered_entries in raw_groups.items():
            if len(ordered_entries) < self.threshold:
                continue

            summary = summaries[message]
            peak_start, peak_count = self._find_peak_window([e.timestamp for e in ordered_entries])
            is_burst = peak_count >= self.threshold

            description = f"'{message}' recurred {summary.count} time(s)"
            if is_burst:
                description += (
                    f", including a burst of {peak_count} within {self.window_minutes} minute(s)"
                )

            patterns.append(
                FailurePattern(
                    pattern_id=f"pattern-{summary.group_id.removeprefix('grp-')}",
                    description=description,
                    message=message,
                    occurrences=summary.count,
                    first_seen=summary.first_seen,
                    last_seen=summary.last_seen,
                    affected_sources=summary.affected_sources,
                    affected_services=summary.affected_services,
                    affected_hosts=summary.affected_hosts,
                    sample_events=summary.sample_entries,
                    is_burst=is_burst,
                    peak_window_start=peak_start if is_burst else None,
                    peak_window_count=peak_count,
                )
            )

        patterns.sort(key=lambda p: (-p.occurrences, p.message))
        return patterns

    def _find_peak_window(self, timestamps: list[datetime]) -> tuple[Optional[datetime], int]:
        """Two-pointer sliding window over sorted timestamps: returns the
        (window_start, count) of the densest cluster within `self.window`."""
        if not timestamps:
            return None, 0

        best_count = 0
        best_start: Optional[datetime] = None
        left = 0
        for right in range(len(timestamps)):
            while timestamps[right] - timestamps[left] > self.window:
                left += 1
            count = right - left + 1
            if count > best_count:
                best_count = count
                best_start = timestamps[left]
        return best_start, best_count
