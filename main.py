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


def path_to_cwd(filename):
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, filename)


config_file = path_to_cwd("config.ini")
config = configparser.ConfigParser()
config.read(config_file)

log_file = config["logging"]["log_file"]
log_level = config["logging"]["log_level"]
servers = config["servers"].items()
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)


async def main():
    while True:
        for server in servers:
            server_details = server[1]
            server_name = server_details.split(",")[0]
            server_address = server_details.split(",")[1]
            server_wait = server_details.split(",")[2]
            message = str(time.ctime()) + " Checking server: " + server_name + " at address: " \
                      + server_address + " with wait time: " + server_wait + " seconds. "
            response = requests.get(server_address).status_code
            if response == 200:
                logging.info(message + server_name + " is up!")
            else:
                logging.error(message + server_name + " is down!")
        await asyncio.sleep(60)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
