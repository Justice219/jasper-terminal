# commands/server/pong.py
from typing import Any
import logging

logging.basicConfig(level=logging.INFO, format='SERVER: %(message)s')
logger = logging.getLogger(__name__)

async def execute(context: Any, args: Any) -> None:
    """
    Responds to a pong command by logging the message.
    The `context` would be the client object that has the handle_message method.
    """
    # send a message to the client
    await context.send_message("recieved:pong:" + args)
