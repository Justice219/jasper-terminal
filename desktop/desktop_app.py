import os
import sys
# import the SocketsServer class from the sockets_server.py file
from networking.sockets_server import SocketsServer

class MeridiumApp:
    def __init__(self):
        self.name = "Jasper Desktop App"
        self.sockets_server = SocketsServer()

        # notify the user that the desktop app is running
        print (f"CLIENT: {self.name} is running")

    async def run(self):
        print(f"{self.name} is running")
        await self.sockets_server.start_server()