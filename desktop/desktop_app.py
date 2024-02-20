import os
import sys
import asyncio

# add the root directory to the path
# I cant figure out how to avoid this :(
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from networking.sockets_server import SocketsServer

class DesktopApp:
    def __init__(self):
        self.name = "Jasper Desktop App"
        self.sockets_server = SocketsServer()

        # notify the user that the desktop app is running
        print (f"CLIENT: {self.name} is running")

    async def run(self):
        print(f"{self.name} is running")
        await self.sockets_server.start_server()

app = DesktopApp()
asyncio.run(app.run())