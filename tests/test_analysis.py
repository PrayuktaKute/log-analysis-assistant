"""Tests for app.analysis.* (error grouping, severity, component, timeline,
statistics, message categorization)."""

from datetime import datetime, timedelta, timezone

from app.analysis import message_catalog
from app.analysis.component_analysis import ComponentAnalyzer
from app.analysis.error_grouping import ErrorGrouper
from app.analysis.severity_analysis import SeverityAnalyzer
from app.analysis.statistics import StatisticsGenerator
from app.analysis.timeline import TimelineGenerator
from app.models.schemas import (
    ComponentAnalysisResult,
    ComponentHealth,
    FailurePattern,
    LogSeverity,
    TimelineEventType,
)

BASE = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


def t(seconds: float) -> datetime:
    return BASE + timedelta(seconds=seconds)


# ---- message_catalog ----


def test_categorize_known_message():
    assert message_catalog.categorize("Redis connection lost") == "cache"
    assert message_catalog.categorize("PLC communication timeout") == "plc"


def test_categorize_unknown_message_uses_keyword_fallback():
    assert message_catalog.categorize("Totally new Postgres outage") == "database"


def test_categorize_unknown_message_defaults_to_uncategorized():
    assert message_catalog.categorize("completely novel gibberish xyz") == message_catalog.UNCATEGORIZED


def test_categorize_uses_configurable_json_path(tmp_path):
    custom_config = tmp_path / "custom_categories.json"
    custom_config.write_text(
        '{"categories": {"widgets": ["Widget exploded"]}, "keyword_fallback": {"widgets": ["widget"]}}',
        encoding="utf-8",
    )

    assert message_catalog.categorize("Widget exploded", config_path=custom_config) == "widgets"
    assert message_catalog.categorize("A widget broke", config_path=custom_config) == "widgets"
    # a message that would categorize under the default (bundled) config
    # does NOT match under this unrelated custom config
    assert message_catalog.categorize("Redis connection lost", config_path=custom_config) == message_catalog.UNCATEGORIZED


def test_categorize_missing_config_file_degrades_gracefully(tmp_path):
    missing_path = tmp_path / "does_not_exist.json"
    assert message_catalog.categorize("anything at all", config_path=missing_path) == message_catalog.UNCATEGORIZED


# ---- ErrorGrouper ----


def test_error_grouper_groups_by_message_and_excludes_info(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.INFO, message="Session validated"),
        make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="Kafka publish failed", service="order-service", host="wilston-prod-02"),
        make_entry(timestamp=t(5), severity=LogSeverity.CRITICAL, message="Kafka publish failed", service="payment-service", host="wilston-prod-03"),
        make_entry(timestamp=t(3), severity=LogSeverity.WARNING, message="Slow response detected"),
    ]

    groups = ErrorGrouper().group(entries)

    assert len(groups) == 2  # INFO entry excluded entirely
    kafka_group = next(g for g in groups if g.message == "Kafka publish failed")
    assert kafka_group.count == 2
    assert kafka_group.category == "messaging"
    assert kafka_group.first_seen == t(1)
    assert kafka_group.last_seen == t(5)
    assert kafka_group.affected_services == ["order-service", "payment-service"]
    assert kafka_group.affected_hosts == ["wilston-prod-02", "wilston-prod-03"]
    assert kafka_group.dominant_severity == LogSeverity.CRITICAL
    assert kafka_group.severity_counts == {"ERROR": 1, "CRITICAL": 1}

    # sorted by count descending: kafka_group (2) before slow-response (1)
    assert groups[0].message == "Kafka publish failed"


def test_error_grouper_group_raw_returns_full_entries_sorted():
    grouper = ErrorGrouper()
    entries_dict = grouper.group_raw([])
    assert entries_dict == {}


def test_error_grouper_normalizes_dynamic_content_by_default(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="User 12345 not found"),
        make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="User 67890 not found"),
    ]

    groups = ErrorGrouper().group(entries)

    assert len(groups) == 1
    assert groups[0].message == "User <NUM> not found"
    assert groups[0].count == 2


def test_error_grouper_normalization_can_be_disabled(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="User 12345 not found"),
        make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="User 67890 not found"),
    ]

    groups = ErrorGrouper(normalize_dynamic_content=False).group(entries)

    assert len(groups) == 2


def test_error_grouper_normalization_is_noop_on_digit_free_messages(make_entry):
    # Regression guard: wilston's real messages contain no digits, so
    # normalization must not change grouping behavior on that dataset.
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="Kafka publish failed"),
        make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="Kafka publish failed"),
    ]

    normalized_on = ErrorGrouper(normalize_dynamic_content=True).group(entries)
    normalized_off = ErrorGrouper(normalize_dynamic_content=False).group(entries)

    assert normalized_on[0].message == normalized_off[0].message == "Kafka publish failed"
    assert normalized_on[0].count == normalized_off[0].count == 2


# ---- SeverityAnalyzer ----


def test_severity_analyzer_counts_and_distribution(make_entry):
    entries = [
        make_entry(severity=LogSeverity.INFO),
        make_entry(severity=LogSeverity.INFO),
        make_entry(severity=LogSeverity.WARNING),
        make_entry(severity=LogSeverity.ERROR),
    ]

    result = SeverityAnalyzer().analyze(entries)

    assert result.total_logs == 4
    assert result.counts == {"INFO": 2, "WARNING": 1, "ERROR": 1}
    assert result.distribution_pct["INFO"] == 50.0


def test_severity_analyzer_most_critical_events_ranked_by_severity_then_time(make_entry):
    warn = make_entry(timestamp=t(0), severity=LogSeverity.WARNING, message="w")
    early_error = make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="e1")
    late_critical = make_entry(timestamp=t(5), severity=LogSeverity.CRITICAL, message="c1")
    early_critical = make_entry(timestamp=t(2), severity=LogSeverity.CRITICAL, message="c2")

    result = SeverityAnalyzer().analyze([warn, early_error, late_critical, early_critical], top_n=3)

    assert [e.message for e in result.most_critical_events] == ["c2", "c1", "e1"]


# ---- ComponentAnalyzer ----


def test_component_analyzer_ranks_and_labels_health(make_entry):
    healthy = [make_entry(service="auth-service", component="auth-service", severity=LogSeverity.INFO) for _ in range(20)]
    degraded = [make_entry(service="order-service", component="order-service", severity=LogSeverity.INFO) for _ in range(9)]
    degraded += [make_entry(service="order-service", component="order-service", severity=LogSeverity.ERROR, message="boom")]
    critical = [make_entry(service="payment-service", component="payment-service", severity=LogSeverity.INFO) for _ in range(4)]
    critical += [make_entry(service="payment-service", component="payment-service", severity=LogSeverity.ERROR, message="boom")] * 3

    result = ComponentAnalyzer().analyze(healthy + degraded + critical)

    by_name = {c.component: c for c in result.components}
    assert by_name["auth-service"].health_status == "healthy"
    assert by_name["order-service"].health_status == "degraded"
    assert by_name["payment-service"].health_status == "critical"
    assert by_name["payment-service"].top_failure_message == "boom"

    # ranked by failure_count descending
    assert result.components[0].component == "payment-service"
    assert result.most_failing_component == "payment-service"


def test_component_analyzer_thresholds_are_configurable(make_entry):
    entries = [make_entry(severity=LogSeverity.INFO) for _ in range(9)]
    entries.append(make_entry(severity=LogSeverity.ERROR, message="boom"))  # error_rate = 0.1

    default_result = ComponentAnalyzer().analyze(entries)
    assert default_result.components[0].health_status == "degraded"  # 0.05 <= 0.1 < 0.15

    lenient_result = ComponentAnalyzer(degraded_threshold=0.2, critical_threshold=0.5).analyze(entries)
    assert lenient_result.components[0].health_status == "healthy"  # 0.1 < 0.2 now


# ---- StatisticsGenerator ----


def test_statistics_generator_produces_expected_summary(make_entry):
    entries = [
        make_entry(severity=LogSeverity.INFO, message="Session validated", host="wilston-prod-01", service="auth-service"),
        make_entry(severity=LogSeverity.INFO, message="Session validated", host="wilston-prod-02", service="auth-service"),
        make_entry(severity=LogSeverity.WARNING, message="Slow response detected", host="wilston-prod-01", service="order-service"),
        make_entry(severity=LogSeverity.ERROR, message="Kafka publish failed", host="wilston-prod-03", service="order-service"),
        make_entry(severity=LogSeverity.CRITICAL, message="Kafka publish failed", host="wilston-prod-03", service="order-service"),
    ]
    component_analysis = ComponentAnalyzer().analyze(entries)

    stats = StatisticsGenerator().generate(entries, component_analysis, top_n=2)

    assert stats.total_logs == 5
    assert stats.error_count == 1
    assert stats.warning_count == 1
    assert stats.fatal_count == 1
    assert stats.affected_hosts == ["wilston-prod-01", "wilston-prod-02", "wilston-prod-03"]
    assert stats.affected_services == ["auth-service", "order-service"]
    assert stats.top_recurring_messages[0].message == "Session validated"
    assert stats.top_recurring_messages[0].count == 2
    assert stats.top_failing_components[0].component == "order-service"


# ---- TimelineGenerator ----


def test_timeline_first_critical_error_and_fatal_events_are_curated(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.INFO, message="Session validated"),
        make_entry(timestamp=t(5), severity=LogSeverity.ERROR, message="Kafka publish failed"),
        make_entry(timestamp=t(10), severity=LogSeverity.CRITICAL, message="Kafka publish failed"),
        make_entry(timestamp=t(20), severity=LogSeverity.CRITICAL, message="Kafka publish failed"),  # same message, later
        make_entry(timestamp=t(15), severity=LogSeverity.CRITICAL, message="Redis connection lost"),
    ]
    empty_components = ComponentAnalysisResult(components=[], most_failing_component=None)

    timeline = TimelineGenerator().generate(
        entries=entries, failure_patterns=[], correlated_events=[], component_analysis=empty_components
    )

    first_critical = [e for e in timeline if e.event_type == TimelineEventType.FIRST_CRITICAL_ERROR]
    assert len(first_critical) == 1
    assert first_critical[0].timestamp == t(5)

    fatals = [e for e in timeline if e.event_type == TimelineEventType.FATAL_EVENT]
    # one per distinct message, at its FIRST critical occurrence -- not one per raw occurrence
    assert len(fatals) == 2
    kafka_fatal = next(e for e in fatals if "Kafka" in e.title)
    assert kafka_fatal.timestamp == t(10)


def test_timeline_service_failure_uses_component_analysis(make_entry):
    entries = [
        make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", component="payment-service", service="payment-service"),
        make_entry(timestamp=t(5), severity=LogSeverity.ERROR, message="boom", component="payment-service", service="payment-service"),
    ]
    critical_component = ComponentAnalysisResult(
        components=[
            ComponentHealth(
                component="payment-service",
                total_logs=2,
                severity_counts={"ERROR": 2},
                failure_count=2,
                error_rate=1.0,
                top_failure_message="boom",
                health_status="critical",
            )
        ],
        most_failing_component="payment-service",
    )

    timeline = TimelineGenerator().generate(
        entries=entries, failure_patterns=[], correlated_events=[], component_analysis=critical_component
    )

    service_failures = [e for e in timeline if e.event_type == TimelineEventType.SERVICE_FAILURE]
    assert len(service_failures) == 1
    assert service_failures[0].timestamp == t(0)
    assert service_failures[0].component == "payment-service"


def test_timeline_burst_event_from_failure_pattern(make_entry):
    pattern = FailurePattern(
        pattern_id="pattern-x",
        description="'boom' recurred 5 times",
        message="boom",
        occurrences=5,
        first_seen=t(0),
        last_seen=t(30),
        affected_sources=["application"],
        affected_services=["order-service"],
        affected_hosts=["wilston-prod-01"],
        sample_events=[],
        is_burst=True,
        peak_window_start=t(10),
        peak_window_count=4,
    )
    empty_components = ComponentAnalysisResult(components=[], most_failing_component=None)

    timeline = TimelineGenerator().generate(
        entries=[], failure_patterns=[pattern], correlated_events=[], component_analysis=empty_components
    )

    bursts = [e for e in timeline if e.event_type == TimelineEventType.BURST_OF_FAILURES]
    assert len(bursts) == 1
    assert bursts[0].timestamp == t(10)


def test_timeline_recovery_requires_all_involved_pairs_to_recover(make_entry, make_correlated_event):
    trigger_a = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom", component="order-service", host="wilston-prod-01")
    trigger_a2 = make_entry(timestamp=t(0.5), severity=LogSeverity.ERROR, message="boom", component="order-service", host="wilston-prod-01")
    trigger_b = make_entry(timestamp=t(1), severity=LogSeverity.ERROR, message="boom", component="payment-service", host="wilston-prod-02")
    recovery_a = make_entry(timestamp=t(10), severity=LogSeverity.INFO, message="Health check passed", component="order-service", host="wilston-prod-01")
    recovery_b = make_entry(timestamp=t(12), severity=LogSeverity.INFO, message="Health check passed", component="payment-service", host="wilston-prod-02")

    cluster = make_correlated_event(
        correlation_id="corr-0001",
        related_events=[trigger_a, trigger_a2, trigger_b],  # size 3, meets min_recovery_cluster_size
        confidence_score=0.7,
    )
    empty_components = ComponentAnalysisResult(components=[], most_failing_component=None)

    all_entries = [trigger_a, trigger_a2, trigger_b, recovery_a, recovery_b]
    timeline = TimelineGenerator().generate(
        entries=all_entries, failure_patterns=[], correlated_events=[cluster], component_analysis=empty_components
    )
    recoveries = [e for e in timeline if e.event_type == TimelineEventType.RECOVERY]
    assert len(recoveries) == 1
    assert recoveries[0].timestamp == t(12)  # latest of the two per-pair recoveries

    # now drop recovery_b -- payment-service never recovers -> no recovery event at all
    timeline_partial = TimelineGenerator().generate(
        entries=[trigger_a, trigger_a2, trigger_b, recovery_a],
        failure_patterns=[],
        correlated_events=[cluster],
        component_analysis=empty_components,
    )
    assert [e for e in timeline_partial if e.event_type == TimelineEventType.RECOVERY] == []


def test_timeline_recovery_skips_low_confidence_clusters(make_entry, make_correlated_event):
    trigger = make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom")
    recovery = make_entry(timestamp=t(5), severity=LogSeverity.INFO, message="Health check passed")

    weak_cluster = make_correlated_event(
        correlation_id="corr-weak",
        related_events=[trigger, trigger],
        confidence_score=0.3,  # below default min_recovery_confidence
    )
    empty_components = ComponentAnalysisResult(components=[], most_failing_component=None)

    timeline = TimelineGenerator().generate(
        entries=[trigger, recovery],
        failure_patterns=[],
        correlated_events=[weak_cluster],
        component_analysis=empty_components,
    )
    assert [e for e in timeline if e.event_type == TimelineEventType.RECOVERY] == []
