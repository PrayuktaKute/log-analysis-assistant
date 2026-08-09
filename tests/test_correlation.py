"""Tests for app.correlation.* (FailureDetector, EventCorrelator) -- both
against synthetic entries and, for regression coverage, the real wilston
sample data.
"""

from datetime import datetime, timedelta, timezone

from app.config import settings
from app.correlation.event_correlator import EventCorrelator
from app.correlation.failure_detector import FailureDetector
from app.ingestion.log_parser import LogParser
from app.ingestion.log_reader import LogReader
from app.ingestion.normalizer import LogNormalizer
from app.models.schemas import LogSeverity

BASE = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


def t(seconds: float) -> datetime:
    return BASE + timedelta(seconds=seconds)


# ---- FailureDetector ----


def test_failure_detector_excludes_below_threshold(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom"),
        make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="boom"),
    ]
    detector = FailureDetector(threshold=3, window_minutes=15)

    patterns = detector.detect_repeated_failures(entries)

    assert patterns == []


def test_failure_detector_basic_repeated_failure(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", service="order-service", host="wilston-prod-01"),
        make_entry(timestamp=t(60), severity=LogSeverity.ERROR, message="boom", service="payment-service", host="wilston-prod-02"),
        make_entry(timestamp=t(120), severity=LogSeverity.CRITICAL, message="boom", service="order-service", host="wilston-prod-01"),
    ]
    detector = FailureDetector(threshold=3, window_minutes=1)  # 60s window -- too small to burst here

    patterns = detector.detect_repeated_failures(entries)

    assert len(patterns) == 1
    pattern = patterns[0]
    assert pattern.message == "boom"
    assert pattern.occurrences == 3
    assert pattern.first_seen == t(0)
    assert pattern.last_seen == t(120)
    assert pattern.affected_services == ["order-service", "payment-service"]
    assert pattern.affected_hosts == ["wilston-prod-01", "wilston-prod-02"]
    assert pattern.is_burst is False  # spread 120s apart, window is only 60s


def test_failure_detector_detects_burst(make_entry):
    # 4 occurrences packed within 10 seconds -> should burst against a 15-minute window/threshold=3
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom"),
        make_entry(timestamp=t(3), severity=LogSeverity.ERROR, message="boom"),
        make_entry(timestamp=t(6), severity=LogSeverity.ERROR, message="boom"),
        make_entry(timestamp=t(9), severity=LogSeverity.CRITICAL, message="boom"),
    ]
    detector = FailureDetector(threshold=3, window_minutes=15)

    patterns = detector.detect_repeated_failures(entries)

    assert len(patterns) == 1
    pattern = patterns[0]
    assert pattern.is_burst is True
    assert pattern.peak_window_count == 4
    assert pattern.peak_window_start == t(0)


def test_failure_detector_pattern_id_is_deterministic(make_entry):
    entries = [make_entry(timestamp=t(i), severity=LogSeverity.ERROR, message="boom") for i in range(3)]
    detector = FailureDetector(threshold=3, window_minutes=15)

    id_a = detector.detect_repeated_failures(entries)[0].pattern_id
    id_b = detector.detect_repeated_failures(entries)[0].pattern_id

    assert id_a == id_b
    assert id_a.startswith("pattern-")


# ---- EventCorrelator ----


def test_event_correlator_links_same_host_and_service(make_entry):
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(10), severity=LogSeverity.ERROR, message="different", host="wilston-prod-01", service="order-service")

    clusters = EventCorrelator(window_seconds=30).correlate([a, b])

    assert len(clusters) == 1
    cluster = clusters[0]
    assert len(cluster.related_events) == 2
    assert cluster.involved_hosts == ["wilston-prod-01"]
    assert cluster.involved_components == ["order-service"]
    assert cluster.start_time == t(0)
    assert cluster.end_time == t(10)


def test_event_correlator_excludes_info_severity(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.INFO, message="Session validated"),
        make_entry(timestamp=t(1), severity=LogSeverity.INFO, message="Session validated"),
    ]

    assert EventCorrelator(window_seconds=30).correlate(entries) == []


def test_event_correlator_drops_singleton_clusters(make_entry):
    # Two ERROR entries that share nothing (different host, service, category) -> no link -> no cluster
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="Kafka publish failed", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="Session validated", host="wilston-prod-02", service="auth-service")

    assert EventCorrelator(window_seconds=30).correlate([a, b]) == []


def test_event_correlator_respects_time_window(make_entry):
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(31), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")

    assert EventCorrelator(window_seconds=30).correlate([a, b]) == []


def test_event_correlator_bounds_cluster_span_against_chaining(make_entry):
    """Regression test: A-B linked (gap 20s), B-C linked (gap 20s), but A-C
    gap is 40s > window (30s). A naive union-find would still merge all
    three transitively; span-bounded union-find must keep C separate.
    """
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(20), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
    c = make_entry(timestamp=t(40), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")

    clusters = EventCorrelator(window_seconds=30).correlate([a, b, c])

    assert len(clusters) == 1
    assert len(clusters[0].related_events) == 2
    assert {e.timestamp for e in clusters[0].related_events} == {t(0), t(20)}


def test_event_correlator_confidence_reflects_shared_dimensions(make_entry):
    # All 3 dimensions shared (host, service, category via identical message) + extra corroboration
    tight = [
        make_entry(timestamp=t(i), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
        for i in range(4)
    ]
    # Exactly 2 of 3 dimensions shared (host + service), message/category differs --
    # still meets the 2-of-3 linkage rule, but with a lower confidence score than `tight`.
    loose = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="Kafka publish failed", host="wilston-prod-02", service="order-service"),
        make_entry(timestamp=t(1), severity=LogSeverity.WARNING, message="Memory usage high", host="wilston-prod-02", service="order-service"),
    ]

    tight_cluster = EventCorrelator(window_seconds=30).correlate(tight)[0]
    loose_cluster = EventCorrelator(window_seconds=30).correlate(loose)[0]

    assert tight_cluster.confidence_score > loose_cluster.confidence_score
    assert 0.0 <= loose_cluster.confidence_score <= 1.0
    assert 0.0 <= tight_cluster.confidence_score <= 1.0


def test_event_correlator_structured_evidence_fields(make_entry):
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(10), severity=LogSeverity.ERROR, message="boom", host="wilston-prod-01", service="order-service")

    cluster = EventCorrelator(window_seconds=30).correlate([a, b])[0]

    evidence = cluster.structured_evidence
    assert evidence.shared_host == "wilston-prod-01"
    assert evidence.shared_service == "order-service"
    assert evidence.shared_category is not None  # identical message -> identical category
    assert evidence.cluster_size == 2
    assert evidence.time_span_seconds == 10.0
    assert evidence.involved_hosts_count == 1
    assert evidence.involved_components_count == 1
    assert evidence.severity_counts == {"ERROR": 2}
    assert evidence.distinct_messages == ["boom"]
    # human-readable evidence still present alongside the structured version
    assert any("share host" in line for line in cluster.supporting_evidence)


def test_event_correlator_structured_evidence_none_when_not_shared(make_entry):
    # host + category shared (both "network"), service differs -> exactly 2
    # of 3 dimensions shared, enough to link, with shared_service left None.
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="ECONNRESET while calling payment gateway", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(1), severity=LogSeverity.WARNING, message="Retrying downstream request", host="wilston-prod-01", service="auth-service")

    cluster = EventCorrelator(window_seconds=30).correlate([a, b])[0]

    evidence = cluster.structured_evidence
    assert evidence.shared_host == "wilston-prod-01"
    assert evidence.shared_service is None
    assert evidence.shared_category == "network"


def test_event_correlator_respects_configurable_thresholds(make_entry):
    # Sharing only 1 dimension (host) normally doesn't link -- but with
    # min_matching_dimensions=1, it should.
    a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="Kafka publish failed", host="wilston-prod-01", service="order-service")
    b = make_entry(timestamp=t(1), severity=LogSeverity.WARNING, message="Memory usage high", host="wilston-prod-01", service="auth-service")

    assert EventCorrelator(window_seconds=30, min_matching_dimensions=2).correlate([a, b]) == []
    relaxed = EventCorrelator(window_seconds=30, min_matching_dimensions=1).correlate([a, b])
    assert len(relaxed) == 1


def test_event_correlator_probable_trigger_is_earliest_worst_severity(make_entry):
    warn = make_entry(timestamp=t(0), severity=LogSeverity.WARNING, message="boom", host="wilston-prod-01", service="order-service")
    late_critical = make_entry(timestamp=t(5), severity=LogSeverity.CRITICAL, message="boom", host="wilston-prod-01", service="order-service")
    early_critical = make_entry(timestamp=t(2), severity=LogSeverity.CRITICAL, message="boom", host="wilston-prod-01", service="order-service")

    cluster = EventCorrelator(window_seconds=30).correlate([warn, late_critical, early_critical])[0]

    assert cluster.probable_trigger.timestamp == t(2)
    assert cluster.probable_trigger.severity == LogSeverity.CRITICAL


# ---- Integration / regression guard against real data ----


def test_event_correlator_no_mega_cluster_on_real_data():
    """The span-bounding fix exists specifically because, without it, ~89%
    of all real candidates (8928 of ~10000) collapsed into one meaningless
    80-minute cluster. Guard against that regressing.
    """
    reader = LogReader(settings.log_input_dir)
    parser = LogParser()
    entries = []
    for f in reader.discover_log_files():
        entries.extend(parser.parse_lines(reader.read_lines(f), source_file=f.name).entries)
    normalized = LogNormalizer().normalize(entries)

    clusters = EventCorrelator().correlate(normalized)

    assert len(clusters) > 50  # many small/medium clusters, not a handful of huge ones
    largest = max(len(c.related_events) for c in clusters)
    assert largest < 500  # nowhere near the 8928-event mega-cluster the old algorithm produced
    for cluster in clusters:
        span = (cluster.end_time - cluster.start_time).total_seconds()
        assert span <= settings.correlation_window_seconds
