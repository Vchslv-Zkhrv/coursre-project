import os
from typing import Literal

from PyQt6.QtCore import QSize

"""
Module containing structures, global constants and state variables /
Модуль, содержащий зависимости, структуры данных,
глобальные константы и переменные состояния.

Must be imported by each module /
Должен быть импортирован всеми остальными модулями.
"""

FORMS = Literal["main", "auth", "nofile"]

NARROW_START = 1000

ICONS_SIZE: QSize = QSize(30, 30)
ICONS_BIG_SIZE: QSize = QSize(64, 64)
ICONS_PATH = ".\\icons"
FONTS_PATH = ".\\fonts"

BUTTONS_SIZE: QSize = QSize(38, 38)
APP_DATABASE_PATH = ".\\programdata\\database.db"

DATABASE_FINDER_FILTER = "Sqlite3 database (*.db *.sqlite3)"
DATABASE_FINDER_PATH = f"C:\\users\\{os.getlogin()}\\Desktop"

GAP = 8
BORDER_RADUIS = 12
MAIN_FONTSIZE = 12
TEXT_FONTSIZE = 14
HEAD_FONTSIZE = 16


MAIN_FONT_FAMILY = "Ubuntu"
HEAD_FONT_FAMILY = "Montserrat"
MONO_FONT_FAMILY = "Ubuntu_Mono"


def icon(color: Literal["black", "white"], name: str) -> str:
    return f"{os.getcwd()}{ICONS_PATH}\\{color}\\{name}.svg"


def radius(size: QSize = BUTTONS_SIZE):
    return int(size.height()/2)
