
import os
import asyncio
import sys
import logging
# add the root directory to the path
# I cant figure out how to avoid this :(
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the needed modules explicitly
from pages import home
import router as router_c

# Socket client import
from networking.sockets_client import SocketsClient

# Initialize simpler logging as per the new preference
logging.basicConfig(level=logging.INFO, format='CLIENT: %(message)s')
logger = logging.getLogger(__name__)

# NiceGUI imports
from nicegui import app, ui

class WebApp:
    """A web application built with NiceGUI for managing different pages and socket communications."""

    def __init__(self):
        self.name = "Jasper Web App"
        self.app = app
        self.ui = ui
        self.router = router_c.router  # Use a more descriptive name for the router
        self.sockets_client = SocketsClient(server_address='ws://localhost:4327', app=self.app, ui=self.ui)
        self.sockets_client.register_callback(self.handle_message)
        self.initialize_pages()

        # Notify the user that the web app is running
        print (f"CLIENT: {self.name} is running")

    def initialize_pages(self) -> None:
        """Initializes the pages of the web application."""
        self.pages = {
            '/': home.content,
        }
        for path, content in self.pages.items():
            self.create_page(path, content)

    def create_page(self, path: str, content_callable: callable) -> None:
        """Creates a page for the web application.

        Args:
            path: The URL path for the page.
            content_callable: A callable that defines the content of the page.
        """
        @self.ui.page(path)
        def page() -> None:
            content_callable(self.ui, self.app, self.sockets_client)

    def notify(self, message: str, notification_type: str) -> None:
        """Sends a notification through the UI.

        Args:
            message: The notification message.
            notification_type: The type of notification (e.g., 'info', 'error').
        """
        self.ui.notify(message, type=notification_type)

    def run(self) -> None:
        """Runs the web application."""
        self.app.include_router(self.router)
        self.app.on_startup(self.sockets_client.connect)
        self.ui.run(title='Meridium Web App')

    async def handle_message(self, message: str, ui):
        command, *args = message.split(":")
        action_map = {
            "ping": lambda: self.sockets_client.send_message("pong:Successful Client Handshake:no_args"),
            "pong": lambda: logger.info("Successful Server Handshake"),
            "recieved": lambda: logger.info(f"Recieved message: {args}"),
            "executed": lambda: logger.info(f"Executed command: {args}"),
        }

        if command in action_map:
            # 1 = command, 2 = description, 3 = args , all split with :
            action = action_map[command]
            # Log the action dynamically
            logger.info("-------------------")
            logger.info(f"Executing action for command: {command}")
            logger.info(f"Description: {args[0]}")
            logger.info(f"Args: {args[1:]}")
            logger.info("-------------------")
            

            # Ensure the action is callable and handle async vs sync appropriately
            if callable(action):
                result = action()  # Execute the lambda or function
                if asyncio.iscoroutine(result):
                    await result  # Await the result if it's a coroutine
                else:
                    # Handle synchronous action if not a coroutine
                    print(f"CLIENT: Executed synchronous action for command: {command}\n")
            else:
                print(f"CLIENT: Unknown command or mismatch in parameters for: {command}")
        else:
            print(f"CLIENT: Unknown command: {command}")


app = WebApp()
app.run()