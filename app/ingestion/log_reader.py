"""Discover and read raw log files from disk.

Responsible for requirement #1: "Read log files from the provided ZIP
archive" and "Read multiple production log files."
"""

import zipfile
from pathlib import Path
from typing import Iterator

from loguru import logger


class LogReader:
    """Discovers log files under a directory and yields their raw lines.

    Also accepts the input as-is if a `.zip` archive (e.g. `wilston_logs.zip`)
    is dropped into `log_dir` instead of pre-extracted `.log` files -- see
    `_extract_zip_archives`.
    """

    DEFAULT_PATTERN = "*.log"

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir

    def discover_log_files(self, pattern: str = DEFAULT_PATTERN) -> list[Path]:
        """Extract any `.zip` archives found in `log_dir`, then return all
        files matching `pattern`, sorted by name."""
        self._extract_zip_archives()
        return sorted(self.log_dir.glob(pattern))

    def _extract_zip_archives(self) -> None:
        """Extract every `.zip` archive in `log_dir` into `log_dir` itself,
        so dropping the raw `wilston_logs.zip` in is enough -- no manual
        unzip step required.

        Only `.log` members are extracted, flattened to their base filename
        (deliberately ignoring any directory structure inside the archive --
        this is also what prevents a "zip slip" path-traversal write outside
        `log_dir` from a malicious/corrupt archive). A file already present
        in `log_dir` is left untouched rather than overwritten, and a
        corrupt/unreadable archive is logged and skipped rather than
        aborting ingestion.
        """
        if not self.log_dir.exists():
            return

        for zip_path in sorted(self.log_dir.glob("*.zip")):
            try:
                with zipfile.ZipFile(zip_path) as archive:
                    for member in archive.namelist():
                        name = Path(member).name
                        if not name.lower().endswith(".log"):
                            continue
                        target = self.log_dir / name
                        if target.exists():
                            continue
                        with archive.open(member) as src, target.open("wb") as dst:
                            dst.write(src.read())
                logger.info("Extracted log files from {}", zip_path.name)
            except (zipfile.BadZipFile, OSError) as exc:
                logger.error("Failed to extract {}: {}", zip_path, exc)

    def read_lines(self, file_path: Path) -> Iterator[tuple[int, str]]:
        """Stream (1-indexed line_number, raw_line) pairs from a single log file.

        `errors="replace"` means a stray encoding issue degrades a single
        character instead of aborting ingestion of the whole file.
        """
        with file_path.open("r", encoding="utf-8", errors="replace") as f:
            for line_number, raw_line in enumerate(f, start=1):
                yield line_number, raw_line.rstrip("\n\r")
