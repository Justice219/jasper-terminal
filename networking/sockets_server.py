import logging
from typing import Set, Dict, Any

import websockets
from websockets.server import WebSocketServerProtocol
from nicegui import ui

from networking.command_handler import CommandHandler

CONNECTIONS: Set[WebSocketServerProtocol] = set()

# Initialize simpler logging as per the new preference
logging.basicConfig(level=logging.INFO, format='SERVER: %(message)s')
logger = logging.getLogger(__name__)

# Define the SocketsServer class
class SocketsServer():
    def __init__(self):
        self.command_handler = CommandHandler(self, "server")
        logger.info('SocketsServer initialized')

    # Define the handle_message method
    async def handle_message(self, websocket: WebSocketServerProtocol) -> None:
        while True:
            try:
                message = await websocket.recv()
                logger.info(f"Received message: {message}")
                command, *args = message.split(":", 1)
                await self.command_handler.handle_command(command, args[0] if args else "")
            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"Connection closed with error: {e}")
                CONNECTIONS.remove(websocket)
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                break

    # Define the send_message method
    async def send_message(self, message: str) -> None:
        disconnected_sockets = set()
        for websocket in CONNECTIONS:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_sockets.add(websocket)
        CONNECTIONS.difference_update(disconnected_sockets)
        
        logger.info(f"Sent message to {len(CONNECTIONS)} clients")

    # Define the handle_connection method
    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        # Add the new connection to the set
        CONNECTIONS.add(websocket)
        # Log the new connection
        logger.info(f"New connection from {websocket.remote_address}")

        # Handle the message
        await self.handle_message(websocket)

    # Define the start_server method
    async def start_server(self) -> None:
        # Start the WebSocket server
        server = await websockets.serve(self.handle_connection, "localhost", 4327)
        # Log the server start
        logger.info("WebSocket server started")

        # Keep the server running until it is closed
        await server.wait_closed()
        # Sometimes the server will not close properly


    async def stop_server(self) -> None:
        # Close all the connections
        for websocket in CONNECTIONS:
            await websocket.close()
        # Log the server stop
        logger.info("WebSocket server stopped")
        # exit the program
        exit(0)