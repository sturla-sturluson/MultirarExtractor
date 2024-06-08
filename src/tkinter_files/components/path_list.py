
from tkinter import ttk
from typing import Callable
from ..models import SavedPath
from ...utils import get_shortened_path_name
from .styled_button import styled_button
from .style import apply_style
from ..enums import *

def toggle_command(button:ttk.Button, link:SavedPath,is_toggled:bool, command:Callable):
    _is_toggled = not is_toggled    
    apply_style(button, Size.MEDIUM, _is_toggled and Variant.SUCCESS or Variant.LIGHT)
    command(link)

def _get_row(root:ttk.Frame, link:SavedPath, command:Callable, delete_command:Callable):
    """Returns a row, with a clickable link, and a delete button"""
    # Creating a frame to hold the row
    label = ttk.Label(root)
    label.pack(pady=0,fill="x")
    # Creating the clickable link
    _variant = link.toggled and Variant.SUCCESS or Variant.LIGHT

    _command = lambda button: toggle_command(button, link, link.toggled, command)
    

    text_name = get_shortened_path_name(link.path)
    button = styled_button(label, text_name, lambda : _command(button), Size.FIT, _variant)
    button.pack(side="left", pady=5, padx=5,fill="x", expand=True)
    _delete_command = lambda link=link: delete_command(link)
    # Adding the delete button to the right side of the row
    delete_button = styled_button(label, "X", _delete_command, Size.XSMALL, Variant.DANGER)
    delete_button.pack(side="right", pady=5, padx=5)
    return label


def list_of_toggleable_links(root:ttk.Frame, links:list[SavedPath], command:Callable, delete_command:Callable):
    """Returns a vertical list, of all the paths the user wants to search
    for, each link being clickable and toggling the search on and off"""
    frame = ttk.Frame(root)
    frame.pack(pady=10,fill="x")
    for link in links:
        _row = _get_row(frame, link, command, delete_command)
        _row.pack(pady=5, padx=5)
        
    return frame