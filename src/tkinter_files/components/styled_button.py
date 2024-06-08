import tkinter as tk
from tkinter import ttk
from ..enums import *
from typing import Callable
from .style import get_style, apply_style



def styled_button(
        root : ttk.Frame | ttk.Label | ttk.LabelFrame,

        text : str,
        command : Callable,
        size : Size = Size.MEDIUM,
        variant : Variant = Variant.PRIMARY,
        enabled : Enabled = Enabled.ENABLED
    ) -> ttk.Button:
    """Returns a styled button
    Args:
        root (ttk.Frame | ttk.Label): The parent element
        text (str): The text to display on the button
        command (Callable): The function to call when the button is clicked
        size (Size, optional): The size of the button. Defaults to Size.MEDIUM.
        variant (Variant, optional): The variant of the button. Defaults to Variant.PRIMARY.
        enabled (Enabled, optional): The state of the button. Defaults to Enabled.ENABLED.
    Returns:
        ttk.Button: The styled button
    """
    button = ttk.Button(root, text=text, command=command)
    apply_style(button, size, variant, enabled)  
    return button