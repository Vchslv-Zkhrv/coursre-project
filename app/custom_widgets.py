from PyQt6 import QtWidgets, QtSvg, QtCore, QtGui

from . import config as cfg
from . import qt_shortcuts as qts

"""
Module with customized PyQt6 basic widgets /
Модуль с модифицированными базовыми виджетами библиотеки PyQt6

There are widgets with extended functionality and behavour /
Виджеты с расширенным функционалом и поведением

"""


class SvgLabel(QtWidgets.QLabel):

    """
    Button contains svg - iconn /
    Кнопка, содержащая svg - иконку
    """

    def __init__(self, icon_name: str, color: str = "none"):

        QtWidgets.QLabel.__init__(self)
        self.setFixedSize(cfg.BUTTONS_SIZE)
        layout = qts.GLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.set_icon(icon_name, cfg.BUTTONS_SIZE)
        br = int(self.height() / 2)
        self.setStyleSheet(f"border-radius: {br}px; background-color: {color};")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def set_icon(
            self,
            icon_name: str,
            size: QtCore.QSize):

        renderer = QtSvg.QSvgRenderer(f"{cfg.ICONS_PATH}\\black\\{icon_name}.svg")
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setPixmap(pixmap)
