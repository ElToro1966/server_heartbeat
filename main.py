# Server Heartbeat.

# Script checking whether a webserver is running or not.
# Writes to a logfile if the server is not running.
# Runs as a service, see service file for details.

import configparser
import logging
import asyncio
import os
import time
import requests
import httpserver


def path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


config_file = path_to_cwd("config.ini")
config = configparser.ConfigParser()
config.read(config_file)

log_file = config["logging"]["log_file"]
info_message = config["logging"]["info_message"]
error_message = config["logging"]["error_message"]
down_check_message = config["logging"]["down_check_message"]
servers = config["servers"].items()
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)


def log_status(server, response):
    message = str(time.ctime()) + " Checking server: " + server.name + " at address: " \
              + server.address + " with wait time: " + str(server.wait) + " seconds. "
    if response == 200:
        logging.info(message + server.name + " - All is well.")
    else:
        logging.error(message + server.name + " is down!")


async def fail_check(server):
    while True:
        http_code = requests.get(server.address).status_code
        if http_code == 200:
            logging.info(info_message + server.name + " is back up!")
            break
        else:
            logging.error(error_message + server.name + " is still down!")
        await asyncio.sleep(server.down_check_interval)


async def main():
    while True:
        for server in servers:
            current_server = httpserver.HttpServer(server)
            http_code = requests.get(current_server.address).status_code
            log_status(current_server, http_code)
            if http_code != 200:
                logging.error(down_check_message + current_server.name + " is down!")
                fail_check(current_server)
            await asyncio.sleep(current_server.wait)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
