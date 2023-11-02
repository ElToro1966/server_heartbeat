import requests


class HttpServer:
    def __init__(self, server):
        server_details = server[1]
        self.name = server_details.split(",")[0]
        self.address = server_details.split(",")[1]
        self.wait = int(server_details.split(",")[2])
        self.down_check_interval = int(server_details.split(",")[3])

    def status(self):
        return requests.get(self.address).status_code
