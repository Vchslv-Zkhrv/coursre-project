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

ICONS_SIZE: QSize = QSize(25, 25)
ICONS_PATH = "./icons"
BUTTONS_SIZE: QSize = QSize(44, 44)


class Theme(TypedDict):
    fore: QColor
    back: QColor
    highlight1: QColor
    highlight2: QColor



MAIN_THEME = Theme()
MAIN_THEME["back"] = QColor(14, 14, 14)
MAIN_THEME["fore"] = QColor(255, 0, 0)
MAIN_THEME["highlight1"] = QColor(250, 250, 250)
MAIN_THEME["highlight2"] = QColor(240, 240, 240)


CURRENT_THEME = MAIN_THEME
