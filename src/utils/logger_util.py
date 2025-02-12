import logging
import os
from datetime import datetime

def setup_logger(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger("TestLogger")
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_dir = "output/logs/"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
