# commands/server/ping.py
from typing import Any

async def execute(context: Any, args: Any) -> None:
    """
    Responds to a ping command by sending a "pong" message back.
    The `context` would be the server object that has the send_message method.
    """
    await context.send_message("pong:Successful Server Handshake:no_args")
    