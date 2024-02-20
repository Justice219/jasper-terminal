from typing import Any
from styling import theme

from nicegui import APIRouter, ui

router = APIRouter(prefix='/c')

def create_link(label: str, href: str, classes: str = 'text-xl text-grey-8') -> Any:
    """Creates a styled link component.

    Args:
        label: The text to display for the link.
        href: The URL or route the link points to.
        classes: Optional; CSS classes to apply for styling. Default is 'text-xl text-grey-8'.

    Returns:
        A NiceGUI link component with applied styles.
    """
    return ui.link(label, href).classes(classes)

@router.page('/')
def example_page() -> None:
    """Defines the main page for the '/c' route."""
    with theme.frame('- Example C -'):
        for i in range(1, 4):
            create_link(f'Item {i}', f'/c/items/{i}')

@router.page('/items/{item_id}', dark=True)
def item_page(item_id: str) -> None:
    """Displays a specific item based on its ID.

    Args:
        item_id: The unique identifier of the item.
    """
    with theme.frame(f'- Example C{item_id} -'):
        create_link('Go back', router.prefix)