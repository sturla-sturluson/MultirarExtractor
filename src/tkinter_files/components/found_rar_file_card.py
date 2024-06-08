import tkinter as tk
from tkinter import ttk
from typing import Callable
from pathlib import Path
from ..models import FoundRarFile
from ...utils import get_plural_suffix

def _extracted_text(rarfile:FoundRarFile):
    """Returns the text for the extracted label
    if it has been extracted show the name of the file"""
    if rarfile.extracted:
        return f"Extracted: {rarfile.extracted_name}"
    return "Not extracted"



def found_rar_file_card(root:ttk.Frame, rarfile:FoundRarFile):
    """Returns a card, with the top level rar file, and the other rar files
    that are part of the same archive"""
    card = ttk.LabelFrame(root, text=f"Rar file: {rarfile.path.name}")
    card.pack(pady=10, fill="x")
    # if its extracting show a progress bar
    if rarfile.is_extracting:
        label = ttk.Label(card, text="Extracting...")
        label.pack(pady=5)
        return card
    # The number of extra rar files
    count = len(rarfile.cleanup_files)
    # The label that shows the number of extra rar files
    count_label = ttk.Label(card, text=f"\t{count} cleanup file{get_plural_suffix(count,'s')} found")
    count_label.pack(pady=5, side="left")
    # To show if it has been extracted
    extracted_label = ttk.Label(card, text=_extracted_text(rarfile))
    extracted_label.pack(pady=5, side="right")
    return card