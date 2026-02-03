import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from from_root import from_root

#constants for logging
LOG_DIR = "logs"
LOG_FILE = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5

LOG_DIR_PATH = os.path.join(from_root(), LOG_DIR)
os.makedirs(LOG_DIR_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR_PATH, LOG_FILE)

def configure_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a rotating file handler
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)
    #file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    #console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
     
    # Add the handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

configure_logger()