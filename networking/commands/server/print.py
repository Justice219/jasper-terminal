# commands/server/print.py
from typing import Any

async def execute(context: Any, args: Any) -> None:
    """
    Responds to a print command by logging the message.
    The `context` would be the client object that has the handle_message method.
    """
    # send a message to the client
    await context.send_message("executed:print:" + args)
    print(f"Print: {args}")