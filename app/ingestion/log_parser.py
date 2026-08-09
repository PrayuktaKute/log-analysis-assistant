"""Parse raw log lines into structured `LogEntry` objects.

Responsible for requirement #2: "Parse and normalize logs" (parsing half).

The wilston logs (application/docker/plc) all share one grammar:

    <timestamp> [<SEVERITY>] source=<src> service=<svc> host=<host> traceId=<id> [orderId=<id>] <message>

`_LINE_PATTERN` encodes that grammar. Timestamps appear either with or
without a fractional-seconds component; `_parse_timestamp` handles both.
Lines that don't match the grammar (or whose timestamp still fails to
parse) are not fatal -- `parse_line` logs a warning with the offending
source file/line number and returns None so the caller can skip them.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Optional

from loguru import logger

from app.models.schemas import LogEntry, LogSeverity

_LINE_PATTERN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)"
    r" \[(?P<severity>[A-Za-z]+)\]"
    r" source=(?P<source>\S+)"
    r" service=(?P<service>\S+)"
    r" host=(?P<host>\S+)"
    r" traceId=(?P<trace_id>\S+)"
    r"(?: orderId=(?P<order_id>\S+))?"
    r" +(?P<message>.+)$"
)

_SEVERITY_MAP: dict[str, LogSeverity] = {
    "DEBUG": LogSeverity.DEBUG,
    "INFO": LogSeverity.INFO,
    "WARN": LogSeverity.WARNING,
    "WARNING": LogSeverity.WARNING,
    "ERROR": LogSeverity.ERROR,
    "FATAL": LogSeverity.CRITICAL,
    "CRITICAL": LogSeverity.CRITICAL,
}


@dataclass
class ParsedFileResult:
    """Outcome of parsing one file: the entries that parsed successfully,
    plus the line numbers of anything that didn't -- for debugging and
    error reporting."""

    source_file: str
    entries: list[LogEntry] = field(default_factory=list)
    skipped_line_numbers: list[int] = field(default_factory=list)


class LogParser:
    """Parses raw log lines (in the wilston `key=value` format) into LogEntry objects."""

    def parse_line(self, raw_line: str, source_file: str, line_number: int) -> Optional[LogEntry]:
        """Parse a single raw line into a LogEntry.

        Returns None for blank lines or lines that don't match the expected
        grammar. Non-blank unparseable lines are logged as warnings
        (source_file + line_number + a snippet) rather than raising, so one
        bad line never aborts ingestion of the rest of the file.
        """
        if not raw_line.strip():
            return None

        match = _LINE_PATTERN.match(raw_line)
        if match is None:
            logger.warning(
                "Unparseable log line: {}:{} -> {!r}", source_file, line_number, raw_line[:200]
            )
            return None

        groups = match.groupdict()

        try:
            timestamp = self._parse_timestamp(groups["ts"])
        except ValueError:
            logger.warning(
                "Unparseable timestamp: {}:{} -> {!r}", source_file, line_number, groups["ts"]
            )
            return None

        severity = _SEVERITY_MAP.get(groups["severity"].upper())
        if severity is None:
            logger.warning(
                "Unrecognized severity token: {}:{} -> {!r}",
                source_file,
                line_number,
                groups["severity"],
            )
            severity = LogSeverity.UNKNOWN

        service = groups["service"]

        return LogEntry(
            timestamp=timestamp,
            severity=severity,
            message=groups["message"].strip(),
            source=groups["source"],
            source_file=source_file,
            line_number=line_number,
            service=service,
            component=service,
            host=groups["host"],
            trace_id=groups.get("trace_id"),
            order_id=groups.get("order_id"),
            raw_line=raw_line,
        )

    def parse_lines(self, lines: Iterable[tuple[int, str]], source_file: str) -> ParsedFileResult:
        """Parse every (line_number, raw_line) pair from one file, collecting
        valid entries and the line numbers of anything skipped."""
        result = ParsedFileResult(source_file=source_file)
        for line_number, raw_line in lines:
            entry = self.parse_line(raw_line, source_file=source_file, line_number=line_number)
            if entry is not None:
                result.entries.append(entry)
            elif raw_line.strip():
                result.skipped_line_numbers.append(line_number)
        return result

    @staticmethod
    def _parse_timestamp(raw_ts: str) -> datetime:
        fmt = "%Y-%m-%dT%H:%M:%S.%fZ" if "." in raw_ts else "%Y-%m-%dT%H:%M:%SZ"
        return datetime.strptime(raw_ts, fmt).replace(tzinfo=timezone.utc)
