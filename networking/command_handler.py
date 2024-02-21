# command_handler.py
import importlib
from typing import Any

class CommandHandler:
    def __init__(self, context: Any, context_type: str):
        self.context = context
        self.context_type = context_type  # "server" or "client"

    async def handle_command(self, command: str, args: Any) -> None:
        try:
            # Construct the module path based on context type
            module_path = f".commands.{self.context_type}.{command}"
            command_module = importlib.import_module(module_path, package="networking")
            await command_module.execute(self.context, args)
        except ModuleNotFoundError:
            print(f"Command not found in {self.context_type} commands: {command}")
        except AttributeError:
            print(f"Command module {command} in {self.context_type} does not have an execute function.")
