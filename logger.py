"""
logger.py — Centralized Logging

Sets up a file-based logger under ``logs/operations.log``.
Every module calls ``get_logger()`` to obtain the shared logger instance.
"""

import logging
import os

from config import LOG_DIR, LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def _ensure_log_dir() -> str:
    """Create the logs directory next to this script if it doesn't exist."""
    base = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base, LOG_DIR)
    os.makedirs(log_path, exist_ok=True)
    return os.path.join(log_path, LOG_FILE)


def get_logger(name: str = "SmartFileOrganizer") -> logging.Logger:
    """Return (or create) the application-wide logger.

    Uses a ``FileHandler`` so every operation is persisted to disk.
    A ``StreamHandler`` is intentionally *not* added — the CLI layer
    handles user-facing output separately.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers on repeated calls
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(
            _ensure_log_dir(), encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
