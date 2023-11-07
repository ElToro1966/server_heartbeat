# Log rotation scripot for the log files of the application
# To be run with cron or similar
# cron entry example (run every day at midnight):
# 0 0 * * * python3 /path/to/log_rotation.py

import configparser
import logging.handlers
import os


def path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


config_file = path_to_cwd("config.ini")
config = configparser.ConfigParser()
try:
    config.read(config_file)
except OSError:
    print("Config file not found, exiting.")
    exit(1)


log_file = config["logging"]["log_file"]
log_file_max_bytes = config["logging"]["log_file_max_bytes"]
log_file_backup_count = config["logging"]["log_file_backup_count"]
server_logger = logging.getLogger("ServerLogger")
server_logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=int(log_file_max_bytes),
                                               backupCount=int(log_file_backup_count))
server_logger.addHandler(handler)