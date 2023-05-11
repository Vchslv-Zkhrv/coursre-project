from typing import TypedDict

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QSize

"""
Module containing structures, global constants and state variables /
Модуль, содержащий зависимости, структуры данных,
глобальные константы и переменные состояния.

Must be imported by each module /
Должен быть импортирован всеми остальными модулями.
"""

ICONS_SIZE: QSize = QSize(34, 34)
ICONS_BIG_SIZE: QSize = QSize(64, 64)
ICONS_PATH = ".\\icons"
FONTS_PATH = ".\\fonts"

BUTTONS_SIZE: QSize = QSize(38, 38)
USERS_DATABASE_PATH = ".\\programdata\\users.db"


class Theme(TypedDict):
    fore: QColor
    back: QColor
    highlight1: QColor
    highlight2: QColor


RED = QColor(255, 61, 61)
ORANGE = QColor(255, 160, 32)
GREEN = QColor(32, 213, 32)
BLUE = QColor(36, 138, 255)

MAIN_THEME = Theme()
MAIN_THEME["back"] = QColor(255, 255, 255)
MAIN_THEME["fore"] = QColor(14, 14, 14)
MAIN_THEME["highlight1"] = QColor(250, 250, 250)
MAIN_THEME["highlight2"] = QColor(240, 240, 240)

CURRENT_THEME = MAIN_THEME

MAIN_FONT_FAMILY = "Ubuntu"
HEAD_FONT_FAMILY = "Montserrat"
MONO_FONT_FAMILY = "Ubuntu_Mono"


def rgba(color: QColor):
    r, g, b, a = color.getRgb()
    return f"rgba({r}, {g}, {b}, {a})"
