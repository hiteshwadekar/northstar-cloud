import logging
import logging.config

import os

DEFAULT_LOGGING_FILE_NAME = "etc/logging.ini"
ROOT_DIR = os.path.abspath(os.curdir)
print(ROOT_DIR)

def init_logging():
    log_file_path = ROOT_DIR + "/" + DEFAULT_LOGGING_FILE_NAME
    print(log_file_path)
    logging.config.fileConfig(log_file_path)


def getLogger(logger_name):
    return logging.getLogger(logger_name)


init_logging()
