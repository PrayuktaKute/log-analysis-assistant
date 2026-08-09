"""Group similar (non-INFO) log messages into ErrorGroup summaries.

Responsible for requirement 1, "Error Grouping". Grouping is exact string
match on `message` by default -- verified empirically that the wilston
message catalog is a fixed, finite set of template strings with no embedded
dynamic content, so no fuzzy/NLP matching is needed there.

To stay reusable for other log sources whose messages *do* embed dynamic
content (e.g. "User 12345 not found"), `normalize_signature()` optionally
collapses embedded digits before grouping (toggle via
`settings.error_grouping_normalize_dynamic_content`, on by default). This
is a no-op on wilston's messages (none contain digits) but lets
structurally-identical messages from other sources group together despite
differing IDs/counts.
"""

import hashlib
import re
from collections import Counter, defaultdict

from app.analysis.message_catalog import categorize
from app.config import settings
from app.models.schemas import ErrorGroup, LogEntry, LogSeverity

_SEVERITY_RANK: dict[LogSeverity, int] = {
    LogSeverity.DEBUG: 0,
    LogSeverity.INFO: 1,
    LogSeverity.UNKNOWN: 1,
    LogSeverity.WARNING: 2,
    LogSeverity.ERROR: 3,
    LogSeverity.CRITICAL: 4,
}

_DYNAMIC_CONTENT_PATTERN = re.compile(r"\d+")


def normalize_signature(message: str) -> str:
    """Collapse embedded numeric content into `<NUM>` so structurally
    identical messages group together even when exact values (IDs, counts,
    ...) differ. No-op for messages with no digits."""
    return _DYNAMIC_CONTENT_PATTERN.sub("<NUM>", message)


class ErrorGrouper:
    """Groups qualifying LogEntries by message signature into ErrorGroups."""

    def __init__(
        self,
        severities: frozenset[LogSeverity] = settings.error_grouping_severities_set,
        sample_size: int = settings.error_grouping_sample_size,
        normalize_dynamic_content: bool = settings.error_grouping_normalize_dynamic_content,
    ):
        self.severities = severities
        self.sample_size = sample_size
        self.normalize_dynamic_content = normalize_dynamic_content

    def _signature(self, message: str) -> str:
        return normalize_signature(message) if self.normalize_dynamic_content else message

    def group_raw(self, entries: list[LogEntry]) -> dict[str, list[LogEntry]]:
        """Group entries whose severity is in `self.severities` by message
        signature, each list sorted by timestamp. Unlike `group()`, this
        returns the full entry lists (not truncated samples) -- e.g. for
        burst detection over the complete timestamp series.
        """
        by_signature: dict[str, list[LogEntry]] = defaultdict(list)
        for entry in entries:
            if entry.severity in self.severities:
                by_signature[self._signature(entry.message)].append(entry)
        for group_entries in by_signature.values():
            group_entries.sort(key=lambda e: e.timestamp)
        return dict(by_signature)

    def group(self, entries: list[LogEntry]) -> list[ErrorGroup]:
        """Group entries whose severity is in `self.severities` by message
        signature. Returned groups are sorted by count descending (largest
        recurring problem first), tie-broken alphabetically for determinism.
        """
        by_signature = self.group_raw(entries)
        groups = [self._build_group(signature, group_entries) for signature, group_entries in by_signature.items()]
        groups.sort(key=lambda g: (-g.count, g.message))
        return groups

    def _build_group(self, signature: str, ordered: list[LogEntry]) -> ErrorGroup:
        """`ordered` must already be sorted by timestamp (as `group_raw` produces)."""
        severity_counts = Counter(e.severity.value for e in ordered)
        dominant_severity = max((e.severity for e in ordered), key=lambda s: _SEVERITY_RANK.get(s, 0))

        return ErrorGroup(
            group_id=f"grp-{hashlib.md5(signature.encode('utf-8')).hexdigest()[:10]}",
            message=signature,
            category=categorize(signature),
            count=len(ordered),
            severity_counts=dict(severity_counts),
            dominant_severity=dominant_severity,
            first_seen=ordered[0].timestamp,
            last_seen=ordered[-1].timestamp,
            affected_services=sorted({e.service for e in ordered}),
            affected_hosts=sorted({e.host for e in ordered}),
            affected_sources=sorted({e.source for e in ordered}),
            sample_entries=ordered[: self.sample_size],
        )
