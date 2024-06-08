import tkinter as tk
from tkinter import ttk
from typing import Callable
from .styled_button import styled_button
from ..enums import Size, Variant,Action

def action_buttons(
            root: ttk.Frame,
            on_button_click: Callable[[list[Action]], None],
            ) -> None:
    """Renders the action buttons for the found rar files"""
    button_row_label = ttk.Frame(root)
    button_row_label.pack(pady=10, fill="x")
    _button_size = Size.FIT
    # First button is extract all button
    extract_all_button = styled_button(button_row_label, "Extract All", lambda: on_button_click([Action.EXTRACT]), size=_button_size, variant=Variant.PRIMARY)
    extract_all_button.grid(row=0, column=0, padx=5)
    # Delete all button
    delete_all_button = styled_button(button_row_label, "Delete All", lambda: on_button_click([Action.DELETE]), size=_button_size, variant=Variant.DANGER)
    delete_all_button.grid(row=0, column=1, padx=5)
    # Delete extracted button
    delete_extracted_button = styled_button(button_row_label, "Delete Extracted", lambda: on_button_click([Action.DELETE_EXTRACTED]), size=_button_size, variant=Variant.PRIMARY)
    delete_extracted_button.grid(row=0, column=2, padx=5)
    # Extract and then delete
    extract_and_delete_button = styled_button(button_row_label, "Extract and Delete", lambda: on_button_click([Action.EXTRACT, Action.DELETE_EXTRACTED]), size=_button_size, variant=Variant.DANGER)
    extract_and_delete_button.grid(row=0, column=3, padx=5)

    