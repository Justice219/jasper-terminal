# commands/server/run.py
from typing import Any
import asyncio

async def run_windows_command(self, command: str) -> None:
        # Run the command
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
     # Wait for the command to complete
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

async def execute(context: Any, args: Any) -> None:
    """
    Runs a windows command on the server and returns the output.
    The `context` would be the server object that has the send_message method.
    """
    command = args
    stdout, stderr = await run_windows_command(command)
    if stdout:
        await context.send_message(f"Command: {command}\nOutput: {stdout}")
    if stderr:
        await context.send_message(f"Command: {command}\nError: {stderr}")

    # send a message to the client
    await context.send_message("executed:run:" + args)