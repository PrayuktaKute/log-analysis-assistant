"""Tests for app.ingestion.* against both synthetic lines and the real
sample data in data/logs/wilston_*.log.
"""

from collections import Counter
from datetime import timezone

from app.config import settings
from app.ingestion.log_parser import LogParser
from app.ingestion.log_reader import LogReader
from app.ingestion.normalizer import LogNormalizer
from app.models.schemas import LogEntry, LogSeverity

VALID_LINE = (
    "2026-08-01T09:00:00.704000Z [INFO] source=application service=api-gateway "
    "host=wilston-prod-01 traceId=trace-877572  Session validated"
)
ORDER_ID_LINE = (
    "2026-08-01T09:00:12.700000Z [INFO] source=docker service=inventory-service "
    "host=wilston-prod-02 traceId=trace-171460 orderId=85270 Connected to PostgreSQL"
)
NO_FRACTION_LINE = (
    "2026-08-01T09:03:57Z [INFO] source=application service=api-gateway "
    "host=wilston-prod-03 traceId=trace-469082  Connected to PostgreSQL"
)
UNKNOWN_SEVERITY_LINE = (
    "2026-08-01T09:00:00.704000Z [WEIRD] source=application service=api-gateway "
    "host=wilston-prod-01 traceId=trace-877572  Something odd"
)


# ---- LogReader ----


def test_log_reader_discovers_wilston_files():
    reader = LogReader(settings.log_input_dir)
    files = reader.discover_log_files()
    names = [f.name for f in files]
    assert "wilston_application.log" in names
    assert "wilston_docker.log" in names
    assert "wilston_plc.log" in names
    assert names == sorted(names)


def test_log_reader_read_lines_yields_line_numbers(tmp_path):
    sample = tmp_path / "sample.log"
    sample.write_text(f"{VALID_LINE}\n{VALID_LINE}\n", encoding="utf-8")

    reader = LogReader(tmp_path)
    lines = list(reader.read_lines(sample))

    assert lines[0][0] == 1
    assert lines[1][0] == 2
    assert lines[0][1] == VALID_LINE


# ---- LogParser: single line ----


def test_parse_line_valid():
    entry = LogParser().parse_line(VALID_LINE, source_file="wilston_application.log", line_number=1)

    assert isinstance(entry, LogEntry)
    assert entry.timestamp.year == 2026
    assert entry.timestamp.tzinfo is not None
    assert entry.timestamp.microsecond == 704000
    assert entry.severity == LogSeverity.INFO
    assert entry.message == "Session validated"
    assert entry.source == "application"
    assert entry.source_file == "wilston_application.log"
    assert entry.line_number == 1
    assert entry.service == "api-gateway"
    assert entry.component == "api-gateway"
    assert entry.host == "wilston-prod-01"
    assert entry.trace_id == "trace-877572"
    assert entry.order_id is None
    assert entry.raw_line == VALID_LINE


def test_parse_line_with_order_id():
    entry = LogParser().parse_line(ORDER_ID_LINE, source_file="wilston_docker.log", line_number=27)

    assert entry is not None
    assert entry.order_id == "85270"
    assert entry.message == "Connected to PostgreSQL"
    assert entry.trace_id == "trace-171460"


def test_parse_line_missing_fractional_seconds():
    entry = LogParser().parse_line(
        NO_FRACTION_LINE, source_file="wilston_application.log", line_number=99
    )

    assert entry is not None
    assert entry.timestamp.microsecond == 0
    assert entry.timestamp.tzinfo is not None


def test_parse_line_unrecognized_severity_is_kept_as_unknown():
    entry = LogParser().parse_line(
        UNKNOWN_SEVERITY_LINE, source_file="wilston_application.log", line_number=1
    )

    assert entry is not None
    assert entry.severity == LogSeverity.UNKNOWN


def test_parse_line_blank_returns_none():
    assert LogParser().parse_line("", source_file="x.log", line_number=1) is None
    assert LogParser().parse_line("   \n", source_file="x.log", line_number=2) is None


def test_parse_line_malformed_returns_none():
    assert (
        LogParser().parse_line("this is not a log line", source_file="x.log", line_number=1)
        is None
    )


# ---- LogParser: batch ----


def test_parse_lines_collects_entries_and_skips():
    lines = [
        (1, VALID_LINE),
        (2, "not a valid log line"),
        (3, ""),
        (4, ORDER_ID_LINE),
    ]
    result = LogParser().parse_lines(lines, source_file="mixed.log")

    assert len(result.entries) == 2
    assert result.skipped_line_numbers == [2]  # blank line 3 is not counted as "skipped"


def test_parse_lines_full_application_log_has_zero_skips():
    reader = LogReader(settings.log_input_dir)
    parser = LogParser()
    file_path = settings.log_input_dir / "wilston_application.log"

    result = parser.parse_lines(reader.read_lines(file_path), source_file=file_path.name)

    assert len(result.entries) == 10000
    assert result.skipped_line_numbers == []

    counts = Counter(e.severity for e in result.entries)
    assert counts[LogSeverity.INFO] == 7034
    assert counts[LogSeverity.WARNING] == 1757
    assert counts[LogSeverity.ERROR] == 989
    assert counts[LogSeverity.CRITICAL] == 220


# ---- LogNormalizer ----


def test_normalizer_sorts_and_normalizes():
    base_kwargs = dict(
        severity=LogSeverity.INFO,
        source="application",
        source_file="x.log",
        service="api-gateway",
        component="api-gateway",
        host="wilston-prod-01",
        raw_line="raw",
    )
    later = LogEntry(
        timestamp="2026-08-01T09:00:05.000000+00:00",
        message="second",
        line_number=2,
        **base_kwargs,
    )
    earlier = LogEntry(
        timestamp="2026-08-01T09:00:01.000000",  # naive, no tzinfo
        message="first   with   extra   spaces",
        line_number=1,
        **base_kwargs,
    )

    normalized = LogNormalizer().normalize([later, earlier])

    assert [e.message for e in normalized] == ["first with extra spaces", "second"]
    assert all(e.timestamp.tzinfo == timezone.utc for e in normalized)
