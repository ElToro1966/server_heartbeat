import asyncio


class HttpServer:
    def __init__(self, server):
        server_details = server[1]
        self.name = server_details.split(",")[0].strip()
        self.address = server_details.split(",")[1].strip()
        self.wait = int(server_details.split(",")[2].strip())
        self.down_check_interval = int(server_details.split(",")[3].strip())