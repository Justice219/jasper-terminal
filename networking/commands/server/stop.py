# commands/server/stop.py
from typing import Any
import logging

logging.basicConfig(level=logging.INFO, format='SERVER: %(message)s')
logger = logging.getLogger(__name__)

async def execute(context: Any, args: Any) -> None:
    """
    Stops the server by calling the stop method on the server object.
    The `context` would be the server object that has the stop method.
    """
    # send a message to the client
    await context.send_message("executed:stop:" + args)
    await context.stop()