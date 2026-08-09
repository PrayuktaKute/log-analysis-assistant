"""Application-wide logging configuration using loguru.

Call `configure_logging()` once, as early as possible (e.g. at the top of
`streamlit_app.py` or any CLI entrypoint). Every other module should log via
`from loguru import logger` directly.
"""

import sys

from loguru import logger

from app.config import settings

_configured = False


def configure_logging() -> None:
    """Configure loguru sinks (console + rotating file) from settings.

    Safe to call multiple times; only the first call takes effect.
    """
    global _configured
    if _configured:
        return

    settings.log_file.parent.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
            "- <level>{message}</level>"
        ),
    )
    logger.add(
        settings.log_file,
        level=settings.log_level,
        rotation="10 MB",
        retention="14 days",
        enqueue=True,
    )

    _configured = True
