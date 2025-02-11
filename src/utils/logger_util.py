import logging
import os
from datetime import datetime

def setup_logger(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger("TestLogger")

    # Avoid duplicate handlers
    if logger.hasHandlers():
        logger.setLevel(level)
        return logger  

    logger.setLevel(level)

    log_dir = "output/logs/"
    os.makedirs(log_dir, exist_ok=True)

    test_files = ["test_screenshot_matching", "test_thumbnail_matching"]
    log_files = {
        testfile: os.path.join(log_dir, f"test_log_{testfile}_{datetime.now().strftime('%Y%m%d')}.log")
        for testfile in test_files
    }

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handlers (one per test file)
    for testfile, log_file in log_files.items():
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Initialize logger
logger = setup_logger()
