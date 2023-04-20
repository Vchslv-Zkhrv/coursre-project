from dataclasses import dataclass

from PyQt6.QtGui import QColor

"""
Module containing structures, global constants and state variables /
Модуль, содержащий зависимости, структуры данных,
глобальные константы и переменные состояния.

Must be imported by each module /
Должен быть импортирован всеми остальными модулями.
"""

ICONS_SIZE = (25, 25)
ICONS_PATH = "./icons"
BUTTONS_SIZE = (44, 44)


@dataclass
class Theme():
    fore: QColor
    back: QColor
    highlight1: QColor
    highlight2: QColor


@dataclass
class Themes():
    main = Theme(
        QColor(14, 14, 14),
        QColor(255, 255, 255),
        QColor(250, 250, 250),
        QColor(240, 240, 240)),
    dark = Theme( 
        QColor(14, 14, 14),
        QColor(255, 255, 255),
        QColor(30, 30, 30),
        QColor(45, 45, 45))


CURRENT_THEME = Themes.main
