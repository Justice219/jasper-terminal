
import os
import asyncio
import sys
# add the root directory to the path
# I cant figure out how to avoid this :(
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the needed modules explicitly
from pages import home
import router as router_c

# Socket client import
from networking.sockets_client import SocketsClient

# NiceGUI imports
from nicegui import app, ui

class WebApp:
    """A web application built with NiceGUI for managing different pages and socket communications."""

    def __init__(self):
        self.name = "Jasper Web App"
        self.app = app
        self.ui = ui
        self.router = router_c.router  # Use a more descriptive name for the router
        self.sockets_client = SocketsClient(server_address='ws://localhost:8756')
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
            content_callable(self.ui, self.app, self.sockets)

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

    async def handle_message(self, message: str):
        command, *args = message.split(" ")
        action_map = {
            "cleanTempFiles": lambda: self.cleaner.clean_temp_files(message),
            "cleanCacheFiles": self.cleaner.clean_cache_files,  # Assumes no args needed
            "emptyRecycleBin": self.cleaner.empty_recycle_bin,  # Assumes no args needed
            "cleanBrowserData": lambda: self.cleaner.clean_browser_data(message),
        }

        if command in action_map:
            action = action_map[command]
            # Log the action dynamically
            action_description = command[4:].lower().replace('files', '').replace('data', '').replace('_', ' ')
            print(f"CLIENT: Received message from web app to {action_description}")

            # Call the action with or without "message" based on its requirement
            if callable(action):
                await action()  # Calls the lambda or function directly
            else:
                print(f"CLIENT: Unknown command or mismatch in parameters for: {command}")
        else:
            print(f"CLIENT: Unknown command: {command}")

app = WebApp()
app.run()