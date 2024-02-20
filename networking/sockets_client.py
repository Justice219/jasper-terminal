import asyncio
import logging
from typing import List, Callable
from websockets import connect
from websockets.client import WebSocketClientProtocol

# Initialize simpler logging as per the new preference
logging.basicConfig(level=logging.INFO, format='CLIENT: %(message)s')
logger = logging.getLogger(__name__)

# Create the SocketClient class
class SocketsClient:
    def __init__(self, server_address: str):
        # Set the server address
        self.server_address: str = server_address
        # Set the websocket to None
        self.websocket: WebSocketClientProtocol | None = None
        # Set the callbacks to an empty list
        self.callbacks: List[Callable[[str], None]] = []

    # Define the connect method
    async def connect(self):
        try:
            # Connect to the server
            async with connect(self.server_address) as websocket:
                # Set the websocket
                self.websocket = websocket
                # Log the connection
                logger.info('Connected to the server.')

                # Send a message to the server
                await self.send_message('ping')
                # Start the check_for_messages loop
                await self.check_for_messages()
        # Handle the exceptions
        except Exception as e:
            logger.error(f'Failed to connect or error during message handling. Error: {e}')

    # Define the send_message method
    async def send_message(self, message: str):
        # Check if the websocket is set
        if self.websocket:
            # Try to send the message
            try:
                # Send the message
                await self.websocket.send(message)
                # Log the message
                logger.info(f'Sent message: {message}')
            # Handle the exceptions
            except Exception as e:
                logger.error(f'Failed to send message. Error: {e}')

    # Define the receive_message method
    async def receive_message(self):
        # Check if the websocket is set
        if self.websocket:
            try:
                # Receive the message
                response = await self.websocket.recv()
                # Log the response
                logger.info(f'Received response: {response}')

                # Execute callbacks concurrently
                await asyncio.gather(*(callback(response) for callback in self.callbacks))

                # Return the response
                return response
            # Handle the exceptions
            except Exception as e:
                logger.error(f'Failed to receive message. Error: {e}')

    # Define the check_for_messages method
    async def check_for_messages(self):
        # Keep checking for messages while the websocket is set
        while self.websocket:
            # Receive the message
            await self.receive_message()

    # Define the close method
    async def close(self):
        # Check if the websocket is set
        if self.websocket:
            # Close the websocket
            await self.websocket.close()
            # Log the close
            logger.info('Connection closed.')

    # Define the register_callback method
    def register_callback(self, callback: Callable[[str], None]):
        # Append the callback to the list
        self.callbacks.append(callback)