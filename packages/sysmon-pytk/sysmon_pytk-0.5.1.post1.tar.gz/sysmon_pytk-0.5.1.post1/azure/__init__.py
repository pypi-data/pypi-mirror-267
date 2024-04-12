# SPDX-FileCopyrightText: © 2023 rdbende <rdbende@proton.me>
# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Azure theme for ttk.
"""

from __future__ import annotations

import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import ttk

TCL_THEME_FILE_PATH = Path(__file__).with_name("azure.tcl").absolute()


def init_theme(root: tk.Tk) -> None:
    """
    Initialize the theme.

    Parameters
    ----------
    root : Tk
        A Tk instance.
    """
    if not isinstance(root, tk.Tk):
        msg = "root must be a `tk.Tk` instance!"
        raise TypeError(msg)
    style = ttk.Style(root)
    if "azure-light" not in style.theme_names():
        root.tk.call("source", str(TCL_THEME_FILE_PATH))


def get_theme(root: tk.Tk) -> str:
    """
    Get the current theme.

    Parameters
    ----------
    root : Tk
        A Tk instance.
    """
    init_theme(root)
    style = ttk.Style(master=root)
    theme = style.theme_use()
    return {"azure-dark": "dark", "azure-light": "light"}.get(theme, theme)


def set_theme(theme: str, root: tk.Tk) -> None:
    """
    Set the theme.

    Parameters
    ----------
    theme : str
        One of "light" or "dark".
    root : Tk
        A Tk instance.
    """
    init_theme(root)
    theme = theme.lower()
    if theme not in {"dark", "light"}:
        msg = f"not a valid azure_ttk theme: {theme}"
        raise ValueError(msg)
    root.tk.call("set_theme", theme)


def toggle_theme(root: tk.Tk) -> None:
    """
    Toggle the theme between Light and Dark.

    Parameters
    ----------
    root : Tk
        A Tk instance.
    """
    init_theme(root)
    style = ttk.Style(master=root)
    set_theme("light" if style.theme_use() == "azure-dark" else "dark", root)


use_dark_theme = partial(set_theme, "dark")
use_light_theme = partial(set_theme, "light")
