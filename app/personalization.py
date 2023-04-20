from dataclasses import dataclass

from PyQt6 import QtGui

"""
module manageing appearance /
модуль, управляющий внешним видом
"""


@dataclass
class Color():
    r: int
    g: int
    b: int
    a: int = 255


@dataclass
class Colors():
    fore: QtGui.QColor
    back: QtGui.QColor
    highlight1: QtGui.QColor
    highlight2: QtGui.QColor
