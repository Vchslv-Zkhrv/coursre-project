from PyQt6 import QtWidgets, QtSvgWidgets, QtCore

from . import config as cfg
from . import qt_shortcuts as qts

"""
Module with customized PyQt6 basic widgets /
Модуль с модифицированными базовыми виджетами библиотеки PyQt6

There are widgets with extended functionality and behavour /
Виджеты с расширенным функционалом и поведением

"""


class SvgIcon(QtSvgWidgets.QSvgWidget):

    """
    Widget wrapping svg icon /
    Виджет - обертка для svg
    """

    def __init__(
            self,
            filename: str,
            size: tuple[int, int] = cfg.ICONS_SIZE):

        QtSvgWidgets.QSvgWidget.__init__(self, f"{cfg.ICONS_PATH}\\{filename}.svg")
        self.setFixedSize(size)


class SvgButton(QtWidgets.QPushButton):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(
            self,
            ico: QtSvgWidgets.QSvgWidget,
            size: tuple[int, int] = cfg.BUTTONS_SIZE):

        QtWidgets.QPushButton.__init__(self)
        self.setFixedSize(size)
        layout = qts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ico = ico
        layout.addWidget(ico)
