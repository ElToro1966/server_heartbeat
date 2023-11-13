# Server Heartbeat.

# Script checking whether a webserver is running or not.
# Writes to a logfile if the server is not running.
# Runs as a service, see service file for details.

import configparser
import logging
import logging.handlers
import asyncio
import os
import time
import httpserver


def path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


def get_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(path_to_cwd(config_file))
    except OSError:
        print("Config file not found, exiting.")
        exit(1)
    return config


def create_rotating_log_file(log_file, log_file_max_bytes, log_file_backup_count):
    logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
    server_logger = logging.getLogger("ServerLogger")
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=int(log_file_max_bytes),
                                                   backupCount=int(log_file_backup_count))
    server_logger.addHandler(handler)


config_file = get_config("config.ini")
log_file = config_file["logging"]["log_file"]
log_file_max_bytes = int(config_file["logging"]["log_file_max_bytes"])
log_file_backup_count = int(config_file["logging"]["log_file_backup_count"])
create_rotating_log_file(log_file, log_file_max_bytes, log_file_backup_count)

info_message = config_file["logging"]["info_message"]
error_message = config_file["logging"]["error_message"]
down_check_message = config_file["logging"]["down_check_message"]
servers = config_file["servers"].items()


def log_status(server, response):
    message = str(time.ctime()) + " Checking server: " + server.name + " at address: " \
              + server.address + " with wait time: " + str(server.wait) + " seconds. "
    if response == 200:
        logging.info(message + server.name + " - " + info_message)
    else:
        logging.error(message + server.name + " - " + error_message)


async def fail_check(server):
    while True:
        if server.status() == 200:
            logging.info(server.name + " - " + info_message)
            break
        else:
            logging.error(server.name + " - " + down_check_message)
        await asyncio.sleep(server.down_check_interval)


async def server_up_check(server):
    while True:
        current_server = httpserver.HttpServer(server)
        log_status(current_server, current_server.status())
        print(current_server.status())
        if current_server.status() != 200:
            fail_check(current_server)
        await asyncio.sleep(current_server.wait)


async def main(*servers):
    await asyncio.gather(*[server_up_check(server) for server in servers])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main(*servers))
