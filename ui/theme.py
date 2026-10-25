"""Light/dark theme palettes and stylesheet generation.

resources/style.qss is a string.Template (``$token`` placeholders, not
str.format's ``{token}`` -- QSS's own rule-block braces would collide with
format-string syntax). build_stylesheet() substitutes the active mode's
palette into it.
"""
from __future__ import annotations

from pathlib import Path
from string import Template

_STYLE_PATH = Path(__file__).resolve().parent.parent / "resources" / "style.qss"

MODES = ("dark", "light")
DEFAULT_MODE = "dark"

_PALETTES: dict[str, dict[str, str]] = {
    "dark": {
        "bg": "#1b1e23",
        "bg_deep": "#14161a",
        "fg": "#eaeaea",
        "muted": "#cfd3da",
        "border": "#2a2e35",
        "button_bg": "#262a31",
        "button_border": "#3a3f47",
        "card_bg": "#23272e",
        "card_border": "#333842",
        "banner_bg": "#10352a",
        "accent": "#00b371",
        "accent_contrast": "#0b0c0e",
        "danger_border": "#7a2b2b",
        "danger_text": "#e08080",
        "danger_solid": "#c0392b",
        "hms_bg": "#4a2a12",
        "hms_border": "#c0392b",
        "hms_text": "#ffd9b3",
        "swatch_border": "#444444",
        "icon": "#cfd3da",
    },
    "light": {
        "bg": "#f5f6f8",
        "bg_deep": "#e7e9ed",
        "fg": "#1b1e23",
        "muted": "#5a6072",
        "border": "#d7dae0",
        "button_bg": "#ffffff",
        "button_border": "#c7cbd3",
        "card_bg": "#ffffff",
        "card_border": "#dde1e7",
        "banner_bg": "#e3f7ec",
        "accent": "#00a862",
        "accent_contrast": "#ffffff",
        "danger_border": "#c23b3b",
        "danger_text": "#b33a3a",
        "danger_solid": "#c0392b",
        "hms_bg": "#fff3e0",
        "hms_border": "#c0392b",
        "hms_text": "#7a4a12",
        "swatch_border": "#b0b0b0",
        "icon": "#3a4150",
    },
}


def palette(mode: str) -> dict[str, str]:
    return _PALETTES.get(mode, _PALETTES[DEFAULT_MODE])


def build_stylesheet(mode: str) -> str:
    template = Template(_STYLE_PATH.read_text())
    return template.substitute(palette(mode))
