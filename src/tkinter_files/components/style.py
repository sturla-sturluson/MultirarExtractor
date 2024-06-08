from tkinter import ttk
from ..enums import *

def get_style():
    style = ttk.Style()
    # Adding default borders to frames
    style.configure("TFrame", borderwidth=2, relief="groove")
    
    # Variants
    variant_colors = {
        Variant.PRIMARY: "blue",
        Variant.SECONDARY: "green",
        Variant.TERTIARY: "yellow",
        Variant.SUCCESS: "green",
        Variant.WARNING: "orange",
        Variant.DANGER: "red",
        Variant.INFO: "lightblue",
        Variant.LIGHT: "lightgrey",
        Variant.DARK: "black",
                    }
    # Enabled
    # Sizes
    _pad_y = 5
    size_options = {
        # 2 xs can same width as 1 small
        Size.FIT: {"padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 10)},
        Size.XSMALL: {"width": 3, "padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 10)},
        Size.SMALL: {"width": 7, "padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 10)},
        Size.MEDIUM: {"width": 12, "padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 10)},
        Size.LARGE: {"width": 19, "padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 12)},
        Size.XLARGE: {"width": 25, "padx": 5, "pady": _pad_y, "height": 1, "font": ("Arial", 14)}
    }
    
    for variant, color in variant_colors.items():
        for size, options in size_options.items():
            style_name = f"{variant.name.lower()}.{size.name.lower()}.TButton"
            style.configure(style_name, background=color, **options)
    
    return style


def apply_style(button: ttk.Button, size: Size, variant: Variant, enabled: Enabled = Enabled.ENABLED) -> ttk.Button:
    if(enabled == Enabled.DISABLED):
        button.config(state="disabled")
        variant = Variant.LIGHT
    else:
        button.config(state="enabled")
    style = f"{variant.name.lower()}.{size.name.lower()}.TButton"
    button.config(style=style)
    return button