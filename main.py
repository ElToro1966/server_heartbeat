# Server Heartbeat.

# Script checking whether a webserver is running or not.
# Writes to a logfile if the server is not running.
# Runs as a service, see service file for details.

import aiohttp
import configparser
import logging
import logging.handlers
import asyncio
import os
import httpserver


def get_path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


def get_config(cfg_file):
    config = configparser.ConfigParser()
    try:
        config.read(get_path_to_cwd(cfg_file))
    except OSError:
        print("Config file not found, exiting.")
        exit(1)
    return config


config_file = get_config("config.ini")
log_file = config_file["logging"]["log_file"]
log_file_max_bytes = int(config_file["logging"]["log_file_max_bytes"])
log_file_backup_count = int(config_file["logging"]["log_file_backup_count"])

info_message = config_file["logging"]["info_message"]
error_message = config_file["logging"]["error_message"]
down_check_message = config_file["logging"]["down_check_message"]
servers = config_file["servers"].items()


def create_rotating_log_file(logger_file, logger_file_max_bytes, logger_file_backup_count):
    server_logger = logging.getLogger("ServerLogger")
    handler = logging.handlers.RotatingFileHandler(logger_file,
                                                   maxBytes=int(logger_file_max_bytes),
                                                   backupCount=int(logger_file_backup_count))
    log_format = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
    handler.setFormatter(log_format)
    server_logger.setLevel(logging.INFO)
    server_logger.propagate = False
    server_logger.addHandler(handler)
    return server_logger


def log_status(server, response, logger, failcheck=False):
    message = str(" Checking server: " + server.name + " at address: " \
              + server.address + " with wait time: " + str(server.wait)
                  + " seconds. Response: " + str(response.status))
    if response.status == 200:
        logger.info(message + " - " + info_message)
    elif not failcheck and response.status != 200:
        logger.error(message + " - " + error_message)
    elif failcheck and response.status != 200:
        logger.error(message + " - "
                     + down_check_message.format(server.down_check_interval))


async def fail_check(current_server, logger):
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(current_server.address) as response:
                if response.status == 200:
                    log_status(current_server, response, logger)
                    break
                else:
                    log_status(current_server, response, logger, failcheck=True)
                await asyncio.sleep(current_server.down_check_interval)


async def server_up_check(current_server, logger):
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(current_server.address) as response:
                log_status(current_server, response, logger)
                if response.status != 200:
                    await fail_check(current_server, logger)
                await asyncio.sleep(current_server.wait)


async def main(http_servers):
    logger = create_rotating_log_file(log_file, log_file_max_bytes,
                                      log_file_backup_count)
    for server in http_servers:
        current_server = httpserver.HttpServer(server)
        asyncio.create_task(
            *[server_up_check(current_server, logger)]
        )
    await asyncio.gather(*asyncio.all_tasks())


if __name__ == '__main__':
    asyncio.run(main(servers))
