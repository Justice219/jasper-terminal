from nicegui import ui

def menu() -> None:
    ui.link('Home', '/').classes(replace='text-white')
    ui.link('Clean', '/clean').classes(replace='text-white')
    ui.link("Tweaks", '/tweaks').classes(replace='text-white')
    
    # add margin to the bottom of the men