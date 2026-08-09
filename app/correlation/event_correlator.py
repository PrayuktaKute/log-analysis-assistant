"""Correlate log events across multiple sources.

Responsible for requirement 5, "Event Correlation" -- entirely deterministic,
no LLM/embeddings. See the module-level algorithm summary below.

`trace_id` is NOT used as a correlation key. Empirically (see the ingestion
review), `trace_id` is generated independently per source over a shared
~900k-value random range, so cross-file `trace_id` matches are statistical
coincidence (birthday-paradox noise), not genuine shared requests.

Algorithm
---------
1. Candidates are entries whose severity is in `candidate_severities`
   (default WARNING/ERROR/CRITICAL; pure INFO noise is excluded -- with
   ~7000 INFO lines per 10k-line file, including it would make almost
   everything within `window_seconds` of everything else, collapsing the
   graph into one meaningless cluster).
2. Two candidates are "linked" if they fall within `window_seconds` of each
   other AND agree on at least `min_matching_dimensions` (default 2) of
   these 3 independent dimensions: same host, same service/component, same
   failure category (the "related error patterns" signal -- see
   `app.analysis.message_catalog`). Requiring 2-of-3 (not just time + any
   single dimension) avoids over-merging: with only a handful of hosts and
   services in a typical deployment, time + a single shared attribute is
   often coincidental at this data volume.
3. Candidates are merged via Union-Find, but a merge is only committed if
   the *resulting cluster's total timestamp span* still fits within
   `window_seconds`. Plain "linked if adjacent-pair gap <= window" union-find
   chains indefinitely (A-B within window, B-C within window => A,B,C
   unioned even if A and C are far apart) -- empirically, on the wilston
   sample data that chaining collapsed 89% of all candidates into one
   meaningless 80-minute cluster. Bounding the whole cluster's span, not
   just each pairwise gap, keeps "time window" meaning what it says: a
   correlated incident happened within one window, not a chain that
   drifted across the whole run.
4. Clusters of size 1 (an isolated candidate with nothing nearby that
   matches) are dropped -- correlation implies more than one corroborating
   event.
5. Each surviving cluster becomes one `CorrelatedEvent`, carrying both a
   human-readable `supporting_evidence` list and a structured
   `CorrelationEvidence` object (shared_host/shared_service/shared_category/
   cluster_size/time_span_seconds/...) for later RAG/LLM consumption.
   Processing order is chronological (earliest candidate first) so results
   are fully deterministic and reproducible for the same input.

Every threshold/weight used here is read from `app.config.settings` (see
the `correlation_*` fields) rather than hardcoded, so behavior can be
retuned per deployment without code changes.
"""

from collections import Counter
from datetime import datetime

from app.analysis.message_catalog import categorize
from app.config import settings
from app.models.schemas import CorrelatedEvent, CorrelationEvidence, LogEntry, LogSeverity

_SEVERITY_RANK: dict[LogSeverity, int] = {
    LogSeverity.DEBUG: 0,
    LogSeverity.INFO: 1,
    LogSeverity.UNKNOWN: 1,
    LogSeverity.WARNING: 2,
    LogSeverity.ERROR: 3,
    LogSeverity.CRITICAL: 4,
}


class _UnionFind:
    """Union-Find that tracks each cluster's timestamp span and refuses to
    merge two clusters if doing so would exceed a maximum span -- this is
    what prevents single-linkage chaining from drifting a cluster across
    the whole dataset (see module docstring, point 3)."""

    def __init__(self, timestamps: list[datetime]):
        self.parent = list(range(len(timestamps)))
        self.min_ts = list(timestamps)
        self.max_ts = list(timestamps)

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def try_union(self, a: int, b: int, max_span_seconds: float) -> bool:
        """Union the clusters containing a and b if the merged cluster's
        timestamp span would still fit within max_span_seconds. Returns
        whether a and b ended up in the same cluster."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return True

        merged_min = min(self.min_ts[ra], self.min_ts[rb])
        merged_max = max(self.max_ts[ra], self.max_ts[rb])
        if (merged_max - merged_min).total_seconds() > max_span_seconds:
            return False

        self.parent[ra] = rb
        self.min_ts[rb] = merged_min
        self.max_ts[rb] = merged_max
        return True


class EventCorrelator:
    """Groups related LogEntries (from possibly different sources) together
    using time-window + attribute-overlap clustering (see module docstring)."""

    def __init__(
        self,
        window_seconds: int = settings.correlation_window_seconds,
        candidate_severities: frozenset[LogSeverity] = settings.correlation_candidate_severities_set,
        min_matching_dimensions: int = settings.correlation_min_matching_dimensions,
        confidence_base: float = settings.correlation_confidence_base,
        confidence_per_dimension: float = settings.correlation_confidence_per_dimension,
        confidence_corroboration_bonus_max: float = settings.correlation_confidence_corroboration_bonus_max,
        confidence_corroboration_per_event: float = settings.correlation_confidence_corroboration_per_event,
    ):
        self.window_seconds = window_seconds
        self.candidate_severities = candidate_severities
        self.min_matching_dimensions = min_matching_dimensions
        self.confidence_base = confidence_base
        self.confidence_per_dimension = confidence_per_dimension
        self.confidence_corroboration_bonus_max = confidence_corroboration_bonus_max
        self.confidence_corroboration_per_event = confidence_corroboration_per_event

    def correlate(self, entries: list[LogEntry]) -> list[CorrelatedEvent]:
        candidates = sorted(
            (e for e in entries if e.severity in self.candidate_severities),
            key=lambda e: e.timestamp,
        )
        if len(candidates) < 2:
            return []

        uf = _UnionFind([e.timestamp for e in candidates])
        window = self.window_seconds

        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                gap = (candidates[j].timestamp - candidates[i].timestamp).total_seconds()
                if gap > window:
                    break
                if self._linked(candidates[i], candidates[j]):
                    uf.try_union(i, j, window)

        clusters: dict[int, list[LogEntry]] = {}
        for idx, entry in enumerate(candidates):
            root = uf.find(idx)
            clusters.setdefault(root, []).append(entry)

        cluster_lists = [cluster for cluster in clusters.values() if len(cluster) >= 2]
        cluster_lists.sort(key=lambda cluster: min(e.timestamp for e in cluster))

        return [
            self._build_correlated_event(f"corr-{index:04d}", cluster)
            for index, cluster in enumerate(cluster_lists, start=1)
        ]

    def _linked(self, a: LogEntry, b: LogEntry) -> bool:
        matches = 0
        if a.host == b.host:
            matches += 1
        if a.service == b.service:
            matches += 1
        if categorize(a.message) == categorize(b.message):
            matches += 1
        return matches >= self.min_matching_dimensions

    def _build_correlated_event(self, correlation_id: str, cluster: list[LogEntry]) -> CorrelatedEvent:
        ordered = sorted(cluster, key=lambda e: e.timestamp)
        start_time = ordered[0].timestamp
        end_time = ordered[-1].timestamp
        span_seconds = (end_time - start_time).total_seconds()

        hosts = sorted({e.host for e in ordered})
        components = sorted({e.component for e in ordered})
        categories = {categorize(e.message) for e in ordered}
        messages = sorted({e.message for e in ordered})
        severity_counts = Counter(e.severity.value for e in ordered)

        same_host = len(hosts) == 1
        same_service = len(components) == 1
        same_category = len(categories) == 1

        trigger = min(ordered, key=lambda e: (-_SEVERITY_RANK.get(e.severity, 0), e.timestamp))

        confidence = self._confidence_score(
            size=len(ordered), same_host=same_host, same_service=same_service, same_category=same_category
        )

        structured_evidence = CorrelationEvidence(
            shared_host=hosts[0] if same_host else None,
            shared_service=components[0] if same_service else None,
            shared_category=next(iter(categories)) if same_category else None,
            cluster_size=len(ordered),
            time_span_seconds=span_seconds,
            involved_hosts_count=len(hosts),
            involved_components_count=len(components),
            severity_counts=dict(severity_counts),
            distinct_messages=messages,
        )

        human_evidence = self._human_evidence(
            ordered=ordered,
            hosts=hosts,
            components=components,
            messages=messages,
            severity_counts=severity_counts,
            same_host=same_host,
            same_service=same_service,
            same_category=same_category,
            span_seconds=span_seconds,
        )

        return CorrelatedEvent(
            correlation_id=correlation_id,
            start_time=start_time,
            end_time=end_time,
            involved_components=components,
            involved_hosts=hosts,
            related_events=ordered,
            probable_trigger=trigger,
            confidence_score=confidence,
            supporting_evidence=human_evidence,
            structured_evidence=structured_evidence,
        )

    def _confidence_score(self, size: int, same_host: bool, same_service: bool, same_category: bool) -> float:
        dims_matched = sum([same_host, same_service, same_category])
        base_score = self.confidence_base + self.confidence_per_dimension * dims_matched
        corroboration_bonus = (
            min(self.confidence_corroboration_bonus_max, self.confidence_corroboration_per_event * (size - 2))
            if size > 2
            else 0.0
        )
        return round(min(1.0, base_score + corroboration_bonus), 3)

    @staticmethod
    def _human_evidence(
        ordered: list[LogEntry],
        hosts: list[str],
        components: list[str],
        messages: list[str],
        severity_counts: Counter,
        same_host: bool,
        same_service: bool,
        same_category: bool,
        span_seconds: float,
    ) -> list[str]:
        evidence = [
            f"{len(ordered)} events across {len(components)} component(s) and {len(hosts)} host(s) "
            f"within {span_seconds:.1f}s"
        ]
        if same_host:
            evidence.append(f"All events share host '{hosts[0]}'")
        if same_service:
            evidence.append(f"All events share service '{components[0]}'")
        if same_category:
            evidence.append(f"All events share failure category '{categorize(ordered[0].message)}'")

        evidence.append(
            "Severity mix: " + ", ".join(f"{sev}={count}" for sev, count in sorted(severity_counts.items()))
        )
        evidence.append(f"Messages involved: {', '.join(messages)}")
        return evidence
