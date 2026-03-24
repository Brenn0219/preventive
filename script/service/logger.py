import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "..", "..", "log")
LOG_DIR = os.path.abspath(LOG_DIR)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "log.log")

def get_logger():
    logger = logging.getLogger("preventiva")

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger