# src/utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.expanduser("~/.ai_hub_logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("ai_hub")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=3)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug("Logger initialized.")
