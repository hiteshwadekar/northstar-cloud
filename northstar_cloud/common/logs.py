import logging
import logging.config

import os

DEFAULT_LOGGING_FILE_NAME = "logging.ini"
ROOT_DIR = os.path.abspath(os.curdir)


def init_logging():
    log_file_path = ROOT_DIR + "/" + DEFAULT_LOGGING_FILE_NAME
    logging.config.fileConfig(log_file_path)


def getLogger(logger_name):
    return logging.getLogger(logger_name)


init_logging()
