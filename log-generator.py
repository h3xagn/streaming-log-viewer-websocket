"""
Log Generator

Generates random log entries for testing FastAPI Streaming Log Viewer over WebSockets
"""

# import libraries
import logging
import random
import time
import os

# set path and file names
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = f"{dir_path}/app.log"

# create logger and configure
logger = logging.getLogger("log_app")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# randomly generate a log entry and then wait 1 second before generating the next one
while True:
    random_number = random.randint(0, 10)
    if random_number == 9:
        logger.error(f"Random message generated: {random_number}")
    elif random_number in [3, 5, 7]:
        logger.warning(f"Random message generated: {random_number}")
    else:
        logger.info(f"Random message generated: {random_number}")
    time.sleep(1)
