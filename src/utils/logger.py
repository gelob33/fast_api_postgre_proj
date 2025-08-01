import logging
import sys

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Prevent adding multiple handlers if logger is imported multiple times
if not logger.hasHandlers():
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Formatter with exception info
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
