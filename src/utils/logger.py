import logging

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# You can attach more handlers here
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)