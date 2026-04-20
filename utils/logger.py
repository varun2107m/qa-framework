import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "artifacts/logs"


def get_logger(name="framework_logger"):
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # --- File Handler ---
    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/test.log",
        maxBytes=1_000_000,
        backupCount=3
    )
    file_handler.setFormatter(_get_formatter())

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(_get_formatter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def _get_formatter():
    return logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

