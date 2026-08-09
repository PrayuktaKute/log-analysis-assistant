"""Generic filesystem helpers used across modules."""

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """Create `path` (and parents) if it doesn't exist yet; return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path
