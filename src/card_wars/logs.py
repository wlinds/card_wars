import os

import loguru

# Import this module and put logs.logger.info("log entry example") to add anything to log

logger = loguru.logger

LOG_DIR = "logs/test/"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger.add(LOG_DIR + "logfile.log")


def game_state(func):
    """
    Use as decorator.
    """

    def wrapper(*args, **kwargs):
        logger.info(f"Starting: {func.__name__}")
        func(*args, **kwargs)
        logger.info(f"Finished: {func.__name__}")

    return wrapper
