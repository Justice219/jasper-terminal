import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from styling import theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    with theme.frame('- Home -'):
        with ui.card().style('background-color: #242424; color: #ffffff; border: none; width: 150%;') as card:
            # header
            ui.label('Welcome to Meridium!').style('font-size: 24px; font-weight: bold;')
            
            ui.html('''
            <p>
                Meridium is a web app that allows you to control your desktop from your browser!
                You can do things like clean your recycle bin, clean your browser data, and more!
                Meridium is a work in progress and is being developed by <a href="https://github.com/Justice219/meridium" style="color: #f23a3a;">Justice219</a>
                    </p>
            ''').style('font-size: 16px;')

            ui.html('''
            <p> 
                Meridium uses websockets to communicate with a <span style="color: #e8234a;">desktop subprocess</span>, which controls the desktop.
                This project was an experiment to learn how to use <span style="color: #e8234a;">websockets</span>, and create a server/client application.
                The desktop subprocess is written in Python, and the web app is written in Python using the NiceGUI package.
                <br></br>
                This project may not be the most <span style="color: #e8234a;">SECURE</span>, and is not recommended for use in a production environment.
                However, it does work as intended, and is a fun project to play around with!
                
            </p>
            ''').style('font-size: 16px;')

        ui.label('incoming messages:')
        messages = ui.column().classes('ml-4')
        
        async def display_messages(message: str) -> None:
            def update_ui():
                messages.append(ui.label(message))

            ui.run(update_ui)

        sockets.register_callback(display_messages)

        # enter command to send to server
        ui.input(label='Send Command', placeholder='Enter command',
                on_change=lambda e: sockets.send_message(str(e.value)))
        