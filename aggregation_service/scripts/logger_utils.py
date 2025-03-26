import os
import logging

def setup_logger(name, log_file):
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(f"logs/{log_file}")
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    if not logger.hasHandlers():
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler()) #prints to console
    return logger
