from contextlib import contextmanager
from typing import Optional, Dict
from components.menu import menu  # Assuming 'menu' is a function or context manager you want to import

from nicegui import ui

@contextmanager
def frame(navtitle: str):
    """Creates a styled frame for the web application."""
    # Add external styles and set UI colors
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
    ui.colors(primary='#1a1919', secondary='#242424', accent='#242424', positive='#00ff00')
    ui.query('body').style('background-color: #242424; color: #ffffff;')

    with ui.header().classes('justify-between text-white'):
        ui.label('Meridium Web App 1.1').classes('font-bold')
        ui.label(navtitle)
        with ui.row():
            menu()

    yield

    # Footer with GitHub link
    with ui.footer().classes('justify-center text-white'):
        with ui.row().classes("justify-center items-center"):
            ui.label('Developed by Justice219').style('font-weight: bold;')
            ui.button(icon='eva-github', on_click=lambda: ui.open("https://github.com/Justice219/meridium", new_tab=True)).classes('text-3xl').style('position: absolute; right: 0; padding-right: 20px;')

@contextmanager
def box(title: str, style: Optional[Dict[str, str]] = None):
    """Creates a styled box with an optional title and custom styles."""
    default_style = {
        'padding': '10px',
        'margin': '10px',
        'border': '1px solid #34495E',
        'border-radius': '5px',
        'background-color': '#242424',
        'box-sizing': 'border-box',
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'stretch',
        'min-height': '200px',
        'flex': '1',
        'min-width': '0',
    }
    final_style = {**default_style, **(style or {})}

    final_style_string = '; '.join(f"{key}: {value}" for key, value in final_style.items())
    with ui.card().style(final_style_string):
        if title:
            ui.label(title).classes('text-white').style('font-weight: bold; margin-bottom: 10px;')
        yield