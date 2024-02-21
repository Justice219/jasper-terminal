import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from styling import theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    ui.add_head_html('''
        <style>
            .terminal-container {
                background-color: #333; /* Dark background for terminal */
                color: #fff; /* White text color */
                padding: 20px;
                border-radius: 5px;
                width: 100%;
                max-width: 600px; /* Maximum width of terminal */
                overflow-y: auto; /* Make terminal scrollable */
                height: 300px; /* Fixed height for terminal */
                margin-bottom: 20px;
            }
            .terminal-message {
                background: #222; /* Slightly darker background for messages */
                padding: 5px 10px;
                border-radius: 4px;
                margin-bottom: 5px;
            }
            .command-input-row {
                width: 100%;
                max-width: 600px; /* Align input width with terminal */
                display: flex;
                flex-direction: row;
                justify-content: space-between; /* Space between input and button */
                margin-bottom: 20px;
            }
            .command-input {
                flex-grow: 1; /* Input field takes up remaining space */
                margin-right: 10px; /* Space between input and button */
            }
            .send-button {
                white-space: nowrap; /* Prevent button text from wrapping */
            }
        </style>
    ''')

    with theme.frame("Terminal"):
        # div to center the terminal
        with ui.column().classes('absolute-center items-center').style('width: 100%;'):
            # Terminal-like container for incoming messages
            messages = ui.column().classes('terminal-container')

            async def display_messages(message: str, ui) -> None:
                with messages:
                    ui.label(message).classes('terminal-message')

            sockets.register_callback(display_messages)

            # Row for command input and send button
            with ui.row().classes("command-input-row"):
                options=["ping", "stop", "print", "run"]
                box = ui.input(placeholder="Enter command here, ex. ping", autocomplete=options).classes("command-input").props('outlined input-style="color: white"  dense')
                ui.button('Send', on_click=(lambda: sockets.send_message(box.value))).classes("send-button")
    
    # return these so we can handle
    return messages
